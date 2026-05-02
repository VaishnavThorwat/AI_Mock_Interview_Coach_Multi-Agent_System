# AI Mock Interview Coach

A multi-agent CLI tool that conducts realistic mock interviews and delivers structured coaching feedback. Built with crewAI, LiteLLM, and Groq.

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/your-username/ai-mock-interview-coach
cd ai-mock-interview-coach
pip install -r requirements.txt
```

### 2. Set up environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your-groq-api-key
SERPER_API_KEY=your-serper-api-key
```

Get your keys:
- Groq: https://console.groq.com
- Serper (web search): https://serper.dev

### 3. Run

```bash
python main.py
```

### Requirements

```
crewai
crewai-tools
litellm
python-dotenv
```

---

## How It Works

```
User input (role + focus area)
        │
        ▼
┌─────────────────────┐
│   Agent 1           │  Searches the web. Produces a role intelligence
│   Research Agent    │  brief: key concepts, top questions, red flags.
└────────┬────────────┘
         │  research brief (plain text)
         ▼
┌─────────────────────┐
│   Agent 2           │  Live chat loop via LiteLLM. Asks one question
│   Interviewer       │  at a time. Full conversation history = memory.
│   (LiteLLM loop)   │  Adapts based on each answer.
└────────┬────────────┘
         │  conversation log (JSON)
         ▼
┌─────────────────────┐
│   Agent 3           │  Reads the JSON log. Scores every answer across
│   Evaluator/Coach   │  5 dimensions. Outputs a markdown report.
└────────┬────────────┘
         │
         ▼
  Coaching report printed + optionally saved as .md
```

### What each agent does

**Agent 1 — Research Agent**
Runs once before the interview starts. Uses Serper to search what companies actually test for the target role and focus area. Outputs a structured brief: role snapshot, key concepts, 10 recommended questions with strong/weak answer guidance, candidate-specific angles (if background was provided), and red flags to watch.

**Agent 2 — Interviewer Agent**
Not a crewAI task — runs as a raw LiteLLM chat loop in `main.py`. This is intentional: crewAI tasks are single-shot completions; a real interview requires turn-by-turn interactivity with full history. The research brief is injected into the system prompt. Memory is the `messages` list — every question and answer is appended and sent with every call. Runs 5–7 turns with intelligent follow-ups, then closes with a forward-looking question.

**Agent 3 — Evaluator/Coach Agent**
Receives the research brief (so it knows what a strong answer looks like) and the conversation log as structured JSON (so it doesn't have to parse prose). Scores each answer on Clarity, Depth, Relevance, Evidence, and Role Fit. Outputs a full markdown coaching report.

---

## Architecture & Design Decisions

### Why Agent 2 is not a crewAI task

crewAI tasks are single completions — you call `crew.kickoff()` and get one output. An interview requires multiple turns with real user input between each one. Running Agent 2 as a LiteLLM loop gives full control over the conversation cycle while keeping the research brief in the system prompt across all turns.

### Why the conversation log is JSON, not plain text

The chat loop already knows the structure of each turn (turn number, question, answer, whether it was skipped or blank). Capturing this as JSON at collection time means Agent 3 receives clean, pre-structured data instead of having to parse `Q3: ... A3: ...` strings from prose. Edge cases (`skipped`, `blank`, `i_dont_know`) are tagged at capture time — Agent 3 just reads the field.

### Why candidate background is optional

Requiring a resume creates friction and excludes early-career candidates who don't have one. When no background is provided, Agent 1 generates a general brief and Agent 2 opens with a background-surfacing question (`"Before we dive in, could you give me a quick overview of your background?"`). Agent 3 detects whether Q1 was a background question and skips scoring it, writing a Background Note instead.

### Why the research step exists at all

Without it, the interviewer asks generic questions (`"Tell me about a time you worked in a team"`). With it, the interviewer has role-specific context and asks questions grounded in what companies actually test — making the session meaningfully different for a Data Analyst vs a Frontend Engineer Intern vs a Product Manager.

### Model choice

All three agents use `groq/llama-3.3-70b-versatile` via Groq's API — fast inference, low latency, and free tier available. The model string is defined once in `agent.py` and `main.py`. To switch providers, change the `MODEL` constant and the corresponding API key in `.env`.

### Tradeoffs

| Decision | Tradeoff |
|----------|----------|
| LiteLLM loop for Agent 2 | More control, but Agent 2 is outside crewAI's observability |
| JSON conversation log | Cleaner for Agent 3, but adds a small dependency on `json` in main |
| Single model for all agents | Simpler config, but a stronger model for Agent 3 would improve report quality |
| CLI only | Fast to run and demo, but no session persistence across runs |

---

## Project Structure

```
ai-mock-interview-coach/
|── prompts
    ── research_agent.txt     # research_agent backstory
    ── interviewer.txt        # interviewer_agent backstory
    ── evaluator_agent.txt    # evaluator_agent backstory      
├── agent.py          # Agent definitions + LLM config
├── task.py           # Task descriptions for Agent 1 and Agent 3
├── crew.py           # Crew assembly — run_research() and run_evaluation()
├── main.py           # CLI entry point + Agent 2 chat loop
├── .env_sample      # Environment variable template
├── requirements.txt
└── README.md
```

---


```

Example: `report_data_analyst_technical_20260503_042400.md`
