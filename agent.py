import os
from crewai import Agent, LLM, tools
from crewai.llms.cache import CACHE_BREAKPOINT_KEY
from crewai_tools import SerperDevTool
from crewai.utilities.types import LLMMessage
from dotenv import load_dotenv

load_dotenv()

MODEL = "groq/llama-3.3-70b-versatile"

class GroqCompatibleLLM(LLM):
    """Drop CrewAI cache_breakpoint markers — Groq rejects them on messages."""

    def _format_messages_for_provider(
        self, messages: list[LLMMessage]
    ) -> list[dict[str, str]]:
        formatted = super()._format_messages_for_provider(messages)
        if self.is_anthropic:
            return formatted
        return [
            {k: v for k, v in msg.items() if k != CACHE_BREAKPOINT_KEY}
            for msg in formatted
        ]

llm = GroqCompatibleLLM(model=MODEL, temperature=0.7)
research_llm = GroqCompatibleLLM(model=MODEL, temperature=0.1)
search_tool = SerperDevTool(name="internet_search", num_results=5)

def load_prompt(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "prompts", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Agent 1: Researcher
research_agent = Agent(
    role="Technical Interview Researcher",
    goal=(
        "Use web search to find the latest interview questions and patterns "
        "for the given role and interview type, then produce a comprehensive research brief"
        "brief covering key concepts, important topics, and the most commonly "
        "asked interview questions. Optionally personalise it using the "
        "candidate's background if provided."
    ),
    backstory=load_prompt("research_agent.txt"),
    tools=[search_tool],
    verbose=False,
    allow_delegation=False,
    llm=research_llm,
)

# Agent 2: Interviewer
# This agent's backstory is used as the system prompt for the live chat loop
# in main.py. It is not run as a CrewAI task — the loop is driven by
# litellm directly so every turn is truly interactive with full history.
interviewer_agent = Agent(
    role="Senior Interviewer",
    goal=(
        "Conduct a realistic, adaptive interview for the candidate. "
        "Ask one question at a time. Listen to every answer. "
        "Ask follow-ups when answers are vague. Wrap up after 7-8 turns."
    ),
    backstory=load_prompt("interviewer.txt"),
    verbose=False,
    allow_delegation=False,
    llm=llm,
)


# Agent 3: Evaluator
evaluator_agent = Agent(
    role="Expert Interview Coach",
    goal=(
        "Using the research brief and the full interview transcript, "
        "evaluate the candidate's performance with specific, evidence-based "
        "feedback and deliver a structured coaching report."
    ),
    backstory=load_prompt("evaluator_agent.txt"),
    verbose=False,
    allow_delegation=False,
    llm=llm,
)