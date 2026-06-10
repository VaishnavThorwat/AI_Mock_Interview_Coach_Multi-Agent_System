import re
import pytest

# ── Fixtures — paste one real report per variable ─────────────────────────────
# We load your three existing reports as plain strings to test against.

def load_report(filename: str) -> str:
    with open(f"reports/{filename}", encoding="utf-8") as f:
        return f.read()

@pytest.fixture
def report_data_analyst():
    return load_report("report_data_analyst_technical_20260503_042400.md")

@pytest.fixture
def report_product_manager():
    return load_report("report_product_manager_case_20260503_114532.md")

@pytest.fixture
def report_frontend_intern():
    return load_report("report_frontend_engineer_intern_behavioral_20260503_083015.md")

@pytest.fixture(params=[
    "report_data_analyst_technical_20260503_042400.md",
    "report_product_manager_case_20260503_114532.md",
    "report_frontend_engineer_intern_behavioral_20260503_083015.md",
])
def any_report(request):
    return load_report(request.param)


# ── Section presence ──────────────────────────────────────────────────────────

REQUIRED_SECTIONS = [
    "## Session Summary",
    "## Background Note",
    "## Per-Answer Evaluation",
    "## Overall Assessment",
    "### Strengths",
    "### Gaps",
    "### Practice Recommendations",
    "## Weakest Answer",
]

def test_required_sections_present(any_report):
    for section in REQUIRED_SECTIONS:
        assert section in any_report, f"Missing section: {section}"


# ── Session Summary table fields ──────────────────────────────────────────────

SESSION_FIELDS = [
    "| Role",
    "| Interview type",
    "| Candidate background",
    "| Questions scored",
    "| Overall score",
    "| Verdict",
]

def test_session_summary_fields(any_report):
    for field in SESSION_FIELDS:
        assert field in any_report, f"Missing session summary field: {field}"


# ── Overall score is present and in X/10 format ───────────────────────────────

def test_overall_score_format(any_report):
    match = re.search(r"\|\s*Overall score\s*\|\s*(\d+(?:\.\d+)?)/10", any_report)
    assert match, "Overall score not found or not in X/10 format"
    score = float(match.group(1))
    assert 0 <= score <= 10, f"Score {score} is outside 0–10 range"


# ── Per-answer dimension scores are in X/5 format ────────────────────────────

def test_dimension_scores_format(any_report):
    # Find everything between Per-Answer Evaluation and Overall Assessment
    section_match = re.search(
        r"## Per-Answer Evaluation(.*?)## Overall Assessment",
        any_report,
        re.DOTALL,
    )
    assert section_match, "Could not extract Per-Answer Evaluation section"
    section = section_match.group(1)

    score_matches = re.findall(r"\|\s*\d+/5\s*\|", section)
    assert len(score_matches) > 0, "No dimension scores found in Per-Answer section"

    # Every score found must be 1–5
    values = re.findall(r"\|\s*(\d+)/5\s*\|", section)
    for v in values:
        assert 1 <= int(v) <= 5, f"Score {v}/5 is out of range"


# ── Weakest Answer has all four required parts ────────────────────────────────

def test_weakest_answer_completeness(any_report):
    required_parts = [
        "**Question:**",
        "**What they said:**",
        "**Why it fell short:**",
        "**Model answer:**",
    ]
    for part in required_parts:
        assert part in any_report, f"Weakest Answer section missing: {part}"


# ── Practice Recommendations has exactly 3 items ─────────────────────────────

def test_practice_recommendations_count(any_report):
    section_match = re.search(
        r"### Practice Recommendations(.*?)---",
        any_report,
        re.DOTALL,
    )
    assert section_match, "Could not find Practice Recommendations section"
    section = section_match.group(1)

    # Numbered list items: 1. 2. 3.
    items = re.findall(r"^\d+\.", section, re.MULTILINE)
    assert len(items) == 3, f"Expected 3 practice drills, found {len(items)}"


# ── Strengths and Gaps each have exactly 3 items ─────────────────────────────

def test_strengths_count(any_report):
    section_match = re.search(
        r"### Strengths.*?(### Gaps)",
        any_report,
        re.DOTALL,
    )
    assert section_match, "Could not find Strengths section"
    section = any_report[any_report.index("### Strengths"):any_report.index("### Gaps")]
    items = re.findall(r"^\*\*", section, re.MULTILINE)
    assert len(items) == 3, f"Expected 3 strengths, found {len(items)}"

def test_gaps_count(any_report):
    section_match = re.search(
        r"### Gaps(.*?)### Practice",
        any_report,
        re.DOTALL,
    )
    assert section_match, "Could not find Gaps section"
    section = section_match.group(1)
    items = re.findall(r"^\*\*", section, re.MULTILINE)
    assert len(items) == 3, f"Expected 3 gaps, found {len(items)}"