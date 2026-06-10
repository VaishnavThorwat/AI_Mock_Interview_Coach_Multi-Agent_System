import re
import json
import pytest
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from crew import run_evaluation

# ── Load fixtures ─────────────────────────────────────────────────────────────

FIXTURE_DIR = Path(__file__).parent / "fixtures"

def load_fixture(filename: str) -> str:
    with open(FIXTURE_DIR / filename, encoding="utf-8") as f:
        return f.read()

# Minimal research brief — just enough for Agent 3 to have context
# We're testing edge case handling, not research quality
MINIMAL_BRIEF = """
## Role Snapshot
A data analyst owns reporting, data cleaning, and metric investigation.

## Key Concepts & Topics
- SQL aggregation and filtering
- Data cleaning approaches
- Metric investigation frameworks

## Red Flags to Watch
- Vague answers with no structure
- No concrete examples given
"""

EDGE_CASE_LOG = load_fixture("edge_case_transcript.json")


# ── Single shared report fixture ──────────────────────────────────────────────
# We generate the report ONCE and reuse it across all edge case tests.
# Without this, every test would make a separate API call — wasteful and slow.

@pytest.fixture(scope="module")
def edge_case_report():
    report = run_evaluation(
        research_brief=MINIMAL_BRIEF,
        conversation_log=EDGE_CASE_LOG,
        target_role="Data Analyst",
        interview_type="technical",
    )
    return report


# ── Helper: extract the score block for a specific question turn ──────────────

def get_question_block(report: str, turn: int) -> str:
    """
    Extracts the text block for Q{turn} from the Per-Answer Evaluation section.
    Returns everything from Q{turn} up to the next Q or the Overall Assessment.
    """
    pattern = rf"### Q{turn}:.*?(?=### Q\d+:|## Overall Assessment)"
    match = re.search(pattern, report, re.DOTALL)
    assert match, f"Could not find Q{turn} block in report"
    return match.group(0)


# ── Rule 1: Background question (turn 1) must not have rubric scores ──────────

def test_background_question_not_scored(edge_case_report):
    """
    Turn 1 asks about background.
    It must appear only in Background Note, never in Per-Answer Evaluation.
    """
    # Background Note must exist and reference the answer
    assert "## Background Note" in edge_case_report, \
        "Background Note section missing"

    # Q1 must not appear as a scored question in Per-Answer Evaluation
    per_answer_match = re.search(
        r"## Per-Answer Evaluation(.*?)## Overall Assessment",
        edge_case_report,
        re.DOTALL,
    )
    assert per_answer_match, "Per-Answer Evaluation section missing"
    per_answer_section = per_answer_match.group(1)

    assert "### Q1:" not in per_answer_section, \
        "Q1 (background question) must not appear as a scored answer"


# ── Rule 2: Skipped answer (turn 2) must have all scores as 0/5 ──────────────

def test_skipped_answer_scores_zero(edge_case_report):
    """
    Turn 2 is tagged 'skipped'.
    Every dimension score in that block must be 0/5.
    """
    block = get_question_block(edge_case_report, turn=2)

    # Find all X/5 scores in this block
    scores = re.findall(r"\|\s*(\d+)/5\s*\|", block)
    assert len(scores) > 0, "No dimension scores found for Q2 (skipped)"

    for score in scores:
        assert int(score) == 0, \
            f"Skipped answer Q2 has score {score}/5 — expected 0/5"


# ── Rule 3: Blank answer (turn 3) must have all scores as 1/5 ────────────────

def test_blank_answer_scores_one(edge_case_report):
    """
    Turn 3 is tagged 'blank'.
    Every dimension score in that block must be 1/5.
    """
    block = get_question_block(edge_case_report, turn=3)

    scores = re.findall(r"\|\s*(\d+)/5\s*\|", block)
    assert len(scores) > 0, "No dimension scores found for Q3 (blank)"

    for score in scores:
        assert int(score) == 1, \
            f"Blank answer Q3 has score {score}/5 — expected 1/5"


# ── Rule 4: i_dont_know with reasoning must note intellectual honesty ─────────

def test_i_dont_know_with_reasoning_acknowledged(edge_case_report):
    """
    Turn 4 is tagged 'i_dont_know' but contains actual reasoning.
    The report must acknowledge intellectual honesty somewhere in Q4's block.
    """
    block = get_question_block(edge_case_report, turn=4)

    honesty_signals = [
        "intellectual honesty",
        "honest",
        "acknowledged",
        "reasoned through",
        "attempted",
    ]
    found = any(signal in block.lower() for signal in honesty_signals)
    assert found, \
        "Q4 (i_dont_know with reasoning) — report did not acknowledge intellectual honesty"


# ── Rule 5: Normal answer (turn 5) must have scores between 1–5 ──────────────

def test_normal_answer_scores_in_range(edge_case_report):
    """
    Turn 5 is a normal answer with no edge case.
    Scores must be between 1 and 5 — not 0.
    """
    block = get_question_block(edge_case_report, turn=5)

    scores = re.findall(r"\|\s*(\d+)/5\s*\|", block)
    assert len(scores) > 0, "No dimension scores found for Q5 (normal answer)"

    for score in scores:
        assert 1 <= int(score) <= 5, \
            f"Normal answer Q5 has score {score}/5 — outside valid range"