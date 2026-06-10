import re
import json
import pytest
from pathlib import Path
from dotenv import load_dotenv
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

load_dotenv()

from crew import run_evaluation

# ── Load one real report as the test subject ──────────────────────────────────
# We use the strong candidate report — it has the most content to judge against.

REPORTS_DIR = Path(__file__).parent.parent / "reports"

def load_report(filename: str) -> str:
    with open(REPORTS_DIR / filename, encoding="utf-8") as f:
        return f.read()


# ── Shared report fixture ─────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def strong_candidate_report():
    return load_report("report_data_analyst_technical_20260503_042400.md")


# ── Helper: build a LLMTestCase ───────────────────────────────────────────────
# LLMTestCase is DeepEval's container for one evaluation unit.
# input  = what went into the system (the conversation log)
# actual_output = what came out (the report)
# DeepEval's judge reads both when scoring.

def make_test_case(report: str) -> LLMTestCase:
    return LLMTestCase(
        input="Evaluate the quality of this interview coaching report.",
        actual_output=report,
    )


# ── Test 1: Feedback specificity ──────────────────────────────────────────────

def test_feedback_is_specific(strong_candidate_report, judge):
    metric = GEval(
        name="Feedback Specificity",
        criteria=(
            "In the Per-Answer Evaluation section, the 'What was missing' and "
            "'What worked' fields must reference specific words, phrases, or moments "
            "from the candidate's actual answer. Generic statements like 'add more depth', "
            "'be more specific', or 'good use of examples' without quoting or referencing "
            "actual content from the answer should score low. "
            "High scores require at least one direct reference to the candidate's words "
            "per evaluated answer."
        ),
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge,
        threshold=0.6,
    )

    test_case = make_test_case(strong_candidate_report)
    metric.measure(test_case)

    print(f"\n  Score: {metric.score:.2f}")
    print(f"  Reason: {metric.reason}")

    assert metric.score >= metric.threshold, (
        f"Feedback Specificity score {metric.score:.2f} below threshold {metric.threshold}.\n"
        f"Reason: {metric.reason}"
    )


# ── Test 2: Model answer quality ──────────────────────────────────────────────

def test_model_answer_sounds_human(strong_candidate_report, judge):
    metric = GEval(
        name="Model Answer Quality",
        criteria=(
            "The 'Weakest Answer — Rewritten' section must contain a model answer that: "
            "(1) reads like a real person speaking in complete sentences, not a bullet list, "
            "(2) uses structured reasoning for technical or case questions, "
            "or STAR format (Situation, Task, Action, Result) for behavioral questions, "
            "(3) is specific enough that a candidate could read it and understand "
            "exactly what a strong answer looks like for that question. "
            "Vague or generic model answers should score low."
        ),
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge,
        threshold=0.6,
    )

    test_case = make_test_case(strong_candidate_report)
    metric.measure(test_case)

    print(f"\n  Score: {metric.score:.2f}")
    print(f"  Reason: {metric.reason}")

    assert metric.score >= metric.threshold, (
        f"Model Answer Quality score {metric.score:.2f} below threshold {metric.threshold}.\n"
        f"Reason: {metric.reason}"
    )


# ── Test 3: Practice drill actionability ─────────────────────────────────────

def test_drills_are_actionable(strong_candidate_report, judge):
    metric = GEval(
        name="Drill Actionability",
        criteria=(
            "The three items under 'Practice Recommendations' must each describe "
            "a concrete action the candidate can take — including what to do, how to do it, "
            "and ideally how often or for how long. "
            "Vague recommendations like 'practice SQL', 'work on communication', or "
            "'study more examples' with no method or frequency should score low. "
            "A high-scoring drill example: 'Write two SQL aggregation queries per day on "
            "the Mode Analytics public datasets, time-boxed to 10 minutes each, "
            "focusing on GROUP BY and date filtering.' "
        ),
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge,
        threshold=0.6,
    )

    test_case = make_test_case(strong_candidate_report)
    metric.measure(test_case)

    print(f"\n  Score: {metric.score:.2f}")
    print(f"  Reason: {metric.reason}")

    assert metric.score >= metric.threshold, (
        f"Drill Actionability score {metric.score:.2f} below threshold {metric.threshold}.\n"
        f"Reason: {metric.reason}"
    )


# ── Test 4: Score justification ───────────────────────────────────────────────

def test_scores_are_justified(strong_candidate_report, judge):
    metric = GEval(
        name="Score Justification",
        criteria=(
            "In the Per-Answer Evaluation section, every dimension score (Clarity, Depth, "
            "Relevance, Evidence, Role Fit) must have an observation in the same table row "
            "that explains why that specific score was given. "
            "Observations like 'good', 'needs work', or 'could be better' with no reference "
            "to what the candidate actually said should score low. "
            "High-scoring observations name something specific from the answer — "
            "a method used, a phrase said, a concept missed, a framework applied or absent."
        ),
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
        model=judge,
        threshold=0.6,
    )

    test_case = make_test_case(strong_candidate_report)
    metric.measure(test_case)

    print(f"\n  Score: {metric.score:.2f}")
    print(f"  Reason: {metric.reason}")

    assert metric.score >= metric.threshold, (
        f"Score Justification score {metric.score:.2f} below threshold {metric.threshold}.\n"
        f"Reason: {metric.reason}"
    )