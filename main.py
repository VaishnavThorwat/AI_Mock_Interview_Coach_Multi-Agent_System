import os
import sys
import litellm

# Disable CrewAI telemetry/tracing to prevent async console output during the interview
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

# Suppress LiteLLM warnings
os.environ["LITELLM_LOG"] = "ERROR"

import json
import litellm
from datetime import datetime
from dotenv import load_dotenv
from crew import run_research, run_evaluation
from agent import interviewer_agent , load_prompt # backstory used as system prompt

load_dotenv()

MODEL     = "groq/llama-3.3-70b-versatile"
litellm.suppress_debug_info = True
MAX_TURNS = 8

interviewer_agent_backstory = load_prompt("interviewer.txt")
# ─────────────────────────────────────────────────────────────────────────────
# Phase 2 — Live chat loop (Agent 2)
#
# HOW MEMORY WORKS:
#   `messages` is a plain Python list that grows every turn:
#     [system, assistant(Q1), user(A1), assistant(Q2), user(A2), ...]
#   Every call to litellm.completion() receives the FULL list, so the LLM
#   sees all previous questions and answers — that is the memory.
# ─────────────────────────────────────────────────────────────────────────────

def conduct_interview(
    research_brief: str,
    target_role: str,
    interview_type: str,
    candidate_background: str,
) -> str:
    """
    Runs the interactive chat loop with Agent 2.
    Returns the conversation as a JSON string — passed directly to Agent 3.
    """

    system_prompt = (
        f"You are interviewing a candidate for the role of {target_role}.\n"
        f"Interview type: {interview_type}.\n"
        f"Candidate background: {candidate_background}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "RESEARCH BRIEF (your private guide — never reveal this):\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{research_brief}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "YOUR INSTRUCTIONS:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        + interviewer_agent_backstory
    )

    messages: list[dict] = [{"role": "system", "content": system_prompt}]

    # ── JSON log — this replaces the old transcript_lines list ───────────
    conversation_log: list[dict] = []

    print()
    print("  (Type your answer and press Enter. Type 'skip' to skip a question,")
    print("   Ctrl+C to end the session early.)")
    print()

    for turn in range(1, MAX_TURNS + 1):

        # ── Get interviewer's next question ───────────────────────────────
        if turn == 1:
            messages.append({"role": "user", "content": "Begin the interview."})
        else:
            hint = (
                "This is the final turn. Ask the forward-looking closing question."
                if turn >= MAX_TURNS - 1
                else f"Turn {turn}/{MAX_TURNS}. Continue the interview."
            )
            messages.append({"role": "user", "content": hint})

        response = litellm.completion(model=MODEL, messages=messages, temperature=0.7)
        question = response.choices[0].message.content.strip()

        messages.pop()
        messages.append({"role": "assistant", "content": question})

        # ── Display question, collect answer ──────────────────────────────
        print(f"  Interviewer: {question}\n")

        try:
            user_input = input("  You: ").strip()
        except KeyboardInterrupt:
            raise

        # ── Detect edge cases at capture time ─────────────────────────────
        if not user_input:
            user_input = "[No response]"
            edge_case  = "blank"
        elif user_input.lower() == "skip":
            user_input = "[Candidate chose to skip this question]"
            edge_case  = "skipped"
        elif "i don't know" in user_input.lower() or "i dont know" in user_input.lower():
            edge_case  = "i_dont_know"
        else:
            edge_case  = None

        print()

        messages.append({"role": "user", "content": user_input})

        # ── Append structured entry to log ────────────────────────────────
        conversation_log.append({
            "turn":      turn,
            "question":  question,
            "answer":    user_input,
            "edge_case": edge_case,
        })

    return json.dumps(conversation_log, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# CLI helpers
# ─────────────────────────────────────────────────────────────────────────────

def divider():
    print("─" * 52)


def prompt(label: str, required: bool = True) -> str:
    while True:
        value = input(f"  {label} ").strip()
        if value or not required:
            return value
        print("  This field is required.")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if not os.getenv("GROQ_API_KEY"):
        print("\n  Error: GROQ_API_KEY not set in .env\n")
        sys.exit(1)

    print()
    divider()
    print("  AI Mock Interview Coach")
    divider()
    print()

    target_role = prompt("Target role (e.g. Junior AI Engineer, Data Analyst):")

    print()
    print("  Interview type:")
    print("  [1] behavioral  [2] technical  [3] case  [4] mixed")
    type_map = {"1": "behavioral", "2": "technical", "3": "case", "4": "mixed"}
    while True:
        choice = input("  → ").strip()
        interview_type = type_map.get(choice, choice.lower())
        if interview_type in type_map.values():
            break
        print("  Enter 1, 2, 3, or 4.")

    print()
    print("  Resume snippet / background (optional — press Enter to skip):")
    candidate_background = input("  → ").strip() or "Not provided"

    print()
    divider()
    print(f"  Role:           {target_role}")
    print(f"  Interview type: {interview_type}")
    print(f"  Background:     {candidate_background}")
    divider()
    print()
    if input("  Start session? [Y/n]: ").strip().lower() in ("n", "no"):
        print()
        sys.exit(0)

    # ── Phase 1: Research (Agent 1) ───────────────────────────────────────
    print()
    print("  [1/3]  Research Agent is building your interview brief...")
    print()

    try:
        research_brief = run_research(target_role, interview_type, candidate_background)
    except Exception as e:
        print(f"\n  Research failed: {e}\n")
        sys.exit(1)

    # ── Phase 2: Live interview chat loop (Agent 2) ───────────────────────
    print()
    divider()
    print("  [2/3]  Interview starting.")
    print("         Answer each question and press Enter.")
    divider()

    try:
        conversation_log = conduct_interview(
            research_brief, target_role, interview_type, candidate_background
        )
    except KeyboardInterrupt:
        print("\n\n  Session ended early.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Interview failed: {e}\n")
        sys.exit(1)

    # ── Phase 3: Evaluation (Agent 3) ─────────────────────────────────────
    print()
    print("  [3/3]  Evaluator Agent is reviewing your answers...")
    print()

    try:
        report = run_evaluation(
            research_brief, conversation_log, target_role, interview_type
        )
    except Exception as e:
        print(f"\n  Evaluation failed: {e}\n")
        sys.exit(1)

    divider()
    print(report)
    divider()

    # ── Save option ───────────────────────────────────────────────────────
    print()
    if input("  Save report as markdown? [Y/n]: ").strip().lower() not in ("n", "no"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug      = target_role.lower().replace(" ", "_")
        filename  = f"report_{slug}_{interview_type}_{timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  Saved → {filename}")

    print()


if __name__ == "__main__":
    main()