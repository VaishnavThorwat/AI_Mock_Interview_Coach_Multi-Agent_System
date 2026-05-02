from crewai import Crew, Process
from agent import research_agent, evaluator_agent
from task import create_research_task, create_evaluation_task


def run_research(target_role: str, interview_type: str, candidate_background: str) -> str:
    """
    Phase 1 — Agent 1 researches the role and produces the interview brief.
    Returns the brief as a plain string.
    """
    task = create_research_task(research_agent)

    crew = Crew(
        agents=[research_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "target_role": target_role,
            "interview_type": interview_type,
            "candidate_background": candidate_background,
        }
    )
    return result.raw if hasattr(result, "raw") else str(result)


def run_evaluation(
    research_brief: str,
    conversation_log: str,
    target_role: str,
    interview_type: str,
):
    """
    Phase 3 — Agent 3 evaluates the candidate.
    Receives Agent 1's brief + the full transcript from the chat loop.
    """
    task = create_evaluation_task(evaluator_agent, research_brief, conversation_log)

    crew = Crew(
        agents=[evaluator_agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff(
        inputs={
            "target_role": target_role,
            "interview_type": interview_type,
        }
    )
    return result.raw if hasattr(result, "raw") else str(result)