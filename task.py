from crewai import Task


def create_research_task(research_agent):
    """
    Agent 1 task — produces the interview brief.
    Runs once before the interview loop starts.
    """
    return Task(
        description="""
        Produce a comprehensive interview research brief for the session below.

        Target Role:            {target_role}
        Interview Type:         {interview_type}
        Candidate Background:   {candidate_background}

        STEP 1 — CHECK INPUTS:
        Decide whether candidate_background contains real content or is
        "Not provided". This changes the Candidate Profile Notes section.

        STEP 2 — RESEARCH:
        You MUST use the web search tool to gather recent data. Do NOT answer purely from memory.
        
        Recommended search queries to run with the tool:
        - "{target_role} interview questions {interview_type} 2026"
        - "{target_role} {interview_type} interview what companies test for"
        - "{target_role} common interview mistakes"

        Find:
        - What this role actually does day-to-day
        - The core knowledge areas tested in a {interview_type} interview
          for {target_role}
        - The most commonly asked questions in real interviews for this role
        - What separates strong candidates from weak ones

        STEP 3 — BUILD THE BRIEF:
        Return exactly this structure. Do not skip any section.

        ---

        ## Role Snapshot
        [2-3 sentences — what does a {target_role} own, decide, and deliver?
        Be specific, not generic.]

        ## Key Concepts & Topics
        [6-8 bullets — core knowledge areas for a {interview_type} interview
        at this role. Each bullet: concept name + one line on why it matters.]

        ## Most Asked Interview Questions (10 questions)
        [CRITICAL: You MUST extract real, advanced questions found in the search results (e.g., LLMOps, Hallucinations, System Design). 
        DO NOT output generic beginner questions like "What is supervised learning?" or "What is overfitting?".]
        
        For each question use this format:

        Q: [question text]
        Why asked: [what competency or concept this tests]
        Strong answer contains: [2-3 key elements]
        Common mistake: [what weak candidates typically say]

        ## Candidate Profile Notes
        [If background provided:
          - Apparent experience level
          - Likely strengths based on what they shared
          - 2-3 specific areas worth probing

        If NOT provided:
          Write: "No background provided. The interviewer will open with a
          background question to calibrate depth before proceeding."]

        ## Red Flags to Watch
        [3-4 concrete answer patterns that signal concern for this role.
        Not generic — specific to {target_role} and {interview_type}.]

        ---

        RULES:
        - Do not invent candidate experience not mentioned in the background
        - Every line must be specific to this role and interview type
        - You MUST use the web search tool at least once before providing the final answer.
        - Read the tool's Observation results carefully before writing the brief.
        - EXTRACT the exact questions from the search snippets. DO NOT invent generic ML questions.
        - If search returns nothing, use training knowledge and note:
          "[Based on general knowledge — search unavailable]"
        """,
        expected_output="""
        A structured research brief with all five sections:
        1. Role Snapshot
        2. Key Concepts & Topics (6-8 bullets)
        3. Most Asked Interview Questions (10, each with why asked /
           strong answer / common mistake)
        4. Candidate Profile Notes
        5. Red Flags to Watch
        """,
        agent=research_agent,
    )


def create_evaluation_task(evaluator_agent, research_brief: str, conversation_log: str):
    """
    Agent 3 task — evaluates the candidate and outputs a markdown report.

    research_brief   : plain string from Agent 1
    conversation_log : JSON string from the chat loop in main.py
                       Each entry has: turn, question, answer, edge_case
    """
    return Task(
        description=f"""
        You have two inputs below. Read both carefully before writing anything.

        ════════════════════════════════════════
        RESEARCH BRIEF (what a strong candidate should know)
        ════════════════════════════════════════
        {research_brief}

        ════════════════════════════════════════
        INTERVIEW LOG (structured JSON)
        ════════════════════════════════════════
        {conversation_log}
        ════════════════════════════════════════

        The JSON log is already structured. Each entry contains:
          - turn       : question number
          - question   : exact question asked by the interviewer
          - answer     : exact answer given by the candidate
          - edge_case  : null | "skipped" | "blank" | "i_dont_know"
                         (pre-detected — use this, do not re-detect)

        STEP 1 — CHECK TURN 1:
        Does the turn 1 question ask about background / experience?
          YES → Do NOT score turn 1. Write a Background Note summarising
                what the candidate shared in their answer. Score from turn 2.
          NO  → Score from turn 1. Background Note = "Provided upfront."

        STEP 2 — SCORE EACH ANSWER (1-5 per dimension):
          Clarity   5=well-structured, easy to follow
                    3=followable but meandering
                    1=confusing or no discernible structure

          Depth     5=nuanced, addresses tradeoffs
                    3=surface level only
                    1=one-liner or blank

          Relevance 5=directly answers the question
                    3=partially on-topic
                    1=off-topic or missed the question

          Evidence  5=specific concrete example with context + outcome
                    3=vague reference to experience
                    1=hypothetical only ("I would...") or none

          Role Fit  5=clearly reflects understanding of the role
                    3=generic, could apply to any role
                    1=misaligned with what the role requires

        STEP 3 — APPLY EDGE CASE RULES (use the edge_case field from JSON):
          "skipped"    → all scores = 0, note as gap, do not over-penalise overall
          "blank"      → all scores = 1
          "i_dont_know" with no reasoning in answer → all scores = 1
          "i_dont_know" with reasoning in answer    → Depth = 2, Evidence = 1,
                                                      note "showed intellectual honesty"
          edge_case = null but answer is vague      → Depth + Evidence = 2-3,
                                                      name exactly what was missing
          edge_case = null but answer is off-topic  → Relevance = 1,
                                                      score others on what they did say

        STEP 4 — OUTPUT this exact markdown. Nothing before it, nothing after.

        ---

        # Interview Coaching Report

        ## Session Summary
        | Field | Value |
        |-------|-------|
        | Role | {{target_role}} |
        | Interview type | {{interview_type}} |
        | Candidate background | [summary / "Not provided"] |
        | Questions scored | [n] |
        | Overall score | [X/10] |
        | Verdict | [one honest, specific sentence] |

        ---

        ## Background Note
        [What turn 1 answer revealed, or "Provided upfront."]

        ---

        ## Per-Answer Evaluation

        ### Q[n]: [question field from JSON]

        **What they said:** [2-3 sentence summary — content only, no judgment]

        | Dimension | Score | Observation |
        |-----------|-------|-------------|
        | Clarity   | X/5   | [specific — reference structure or wording] |
        | Depth     | X/5   | [specific — what they did or didn't address] |
        | Relevance | X/5   | [did it answer the question?] |
        | Evidence  | X/5   | [concrete example present? quality?] |
        | Role Fit  | X/5   | [does it reflect role understanding?] |

        **What worked:** [reference actual words or moments from their answer.
        If nothing worked: "No notable strengths in this answer."]
        **What was missing:** [specific — not "more depth" but what depth,
        on what aspect, and why it matters for this role]

        [repeat for every scored turn]

        ---

        ## Overall Assessment

        ### Strengths (top 3)
        **[Label]** — [2 sentences referencing specific turns by number]

        ### Gaps (top 3)
        **[Label]** — [2 sentences pointing to specific turns by number]

        ### Practice Recommendations
        1. **[Drill]:** [exactly what to do and how — not "practice more"]
        2. **[Drill]:** [exactly what to do and how]
        3. **[Drill]:** [exactly what to do and how]

        ---

        ## Weakest Answer — Rewritten
        **Question:** [from JSON]
        **What they said:** [1-2 sentence summary]
        **Why it fell short:** [specific diagnosis]
        **Model answer:** [strong, human-sounding answer — STAR if behavioral,
        structured reasoning if technical/case. Do not invent specific company
        names if no background was provided.]

        ---

        STRICT RULES:
        - Read question and answer from JSON — do not paraphrase the question
        - Never penalise a candidate for experience they never claimed to have
        - Overall score is holistic judgment, not a mathematical average
        - If fewer than 4 answers were scored, add a note:
          "Limited data — score reflects [n] answers only"
        """,
        expected_output="""
        A complete markdown coaching report starting from the
        # Interview Coaching Report header. No JSON, no preamble.
        Contains: Session Summary, Background Note, Per-Answer Evaluation
        for every scored turn, Overall Assessment (3 strengths, 3 gaps,
        3 drills), and Weakest Answer rewritten as a model answer.
        """,
        agent=evaluator_agent,
    )