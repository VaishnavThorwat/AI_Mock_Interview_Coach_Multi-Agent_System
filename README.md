# AI Mock Interview Coach

A multi-agent CLI tool that conducts realistic mock interviews and delivers structured coaching feedback. Built with [crewAI](https://www.crewai.com/), [LiteLLM](https://docs.litellm.ai/), and [Groq](https://console.groq.com/).

---

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Key Design Decisions & Tradeoffs](#key-design-decisions--tradeoffs)
- [Example Interview Transcripts](#example-interview-transcripts)
- [Project Structure](#project-structure)

---

## Quick Start

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com) (free tier available)

### 1. Clone and install

```bash
git clone https://github.com/your-username/ai-mock-interview-coach
cd ai-mock-interview-coach
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
cp .env_sample .env
```

Open `.env` and fill in your keys:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run

```bash
python main.py
```

You'll be prompted for:

| Prompt | Example |
|--------|---------|
| Target role | `Data Analyst` |
| Focus area | `Technical` / `Behavioral` / `Case` |
| Candidate background *(optional)* | Paste a short resume summary, or press Enter to skip |

The tool runs three agents in sequence, then prints your coaching report. You'll also be asked if you'd like to save it as a `.md` file.

### Requirements

```
crewai
litellm
python-dotenv
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## Architecture Overview

```
User input (role + focus area + optional background)
        │
        ▼
┌─────────────────────────────────────────────────┐
│  Agent 1 — Research Agent (crewAI task)         │
│                                                 │
│  Searches the web for role-specific interview   │
│  patterns. Outputs a structured brief:          │
│  key concepts, 10 recommended questions,        │
│  strong/weak answer guidance, red flags.        │
└────────────────────┬────────────────────────────┘
                     │  research brief (plain text)
                     ▼
┌─────────────────────────────────────────────────┐
│  Agent 2 — Interviewer (raw LiteLLM loop)       │
│                                                 │
│  Live chat loop — one question at a time.       │
│  Research brief lives in the system prompt.     │
│  Full conversation appended to `messages` list  │
│  on every turn (memory = message history).      │
│  Runs 5–7 turns, then a closing question.       │
└────────────────────┬────────────────────────────┘
                     │  conversation log (JSON)
                     ▼
┌─────────────────────────────────────────────────┐
│  Agent 3 — Evaluator / Coach (crewAI task)      │
│                                                 │
│  Receives the research brief + conversation     │
│  log. Scores each answer across 5 dimensions.   │
│  Outputs a full markdown coaching report.       │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
        Coaching report printed to stdout
        + optionally saved as report_<role>_<focus>_<timestamp>.md
```

### What each agent does

#### Agent 1 — Research Agent

Runs once before the interview starts. Uses the Serper tool to search what companies actually test for the target role and focus area. Outputs a structured brief containing:

- Role snapshot (what the job actually requires day-to-day)
- Key technical or behavioral concepts to probe
- 10 recommended questions with strong and weak answer guidance
- Candidate-specific angles (if background was provided)
- Red flags to watch for in answers

The brief is injected into Agent 2's system prompt, and also passed to Agent 3 so it knows what "good" looks like when scoring.

#### Agent 2 — Interviewer Agent

**Not a crewAI task** — runs as a raw LiteLLM chat loop in `main.py`. This is intentional: crewAI tasks are single-shot completions, but a real interview requires turn-by-turn interactivity with actual user input between each question.

How it works:

1. The research brief is injected into the system prompt at the start of the loop.
2. Agent 2 asks one question per turn.
3. The user types their answer in the terminal.
4. The question and answer are appended to the `messages` list.
5. The full `messages` list is sent with every API call — this is the agent's memory.
6. After 5–7 turns, Agent 2 closes with a forward-looking question ("What's one thing you'd work on before your next interview?").

If no background was provided, Agent 2 opens with a background-surfacing question before moving to role-specific questions.

Special answer handling — the agent gracefully handles:

| Input | Behaviour |
|-------|-----------|
| Blank / empty | Tagged as `blank`, not penalised |
| `skip` | Tagged as `skipped`, excluded from scoring |
| `i don't know` | Tagged as `i_dont_know`, Coach notes the gap without penalising |

#### Agent 3 — Evaluator / Coach Agent

A crewAI task that receives two inputs: the research brief and the conversation log as structured JSON. It outputs a complete markdown coaching report containing:

- **Session Summary** — role, type, background summary, overall score, verdict
- **Background Note** — what turn 1 revealed, or "Provided upfront"
- **Per-Answer Evaluation** — for every scored turn: what they said, scores across 5 dimensions (Clarity, Depth, Relevance, Evidence, Role Fit), what worked, what was missing
- **Overall Assessment** — top 3 strengths, top 3 gaps, 3 specific practice drills
- **Weakest Answer Rewritten** — the lowest-scoring answer rewritten as a model answer with explicit diagnosis

Agent 3 does not score background-surfacing questions (Q1 when no background was provided), and never penalises candidates for experience they never claimed to have.

---

## Key Design Decisions & Tradeoffs

### Why Agent 2 is not a crewAI task

crewAI's `crew.kickoff()` is a single completion — you give it a task and it returns one output. An interview is inherently multi-turn: the interviewer must wait for a real human answer before asking the next question. Running Agent 2 as a LiteLLM loop gives full control over the conversation cycle while keeping the research brief in the system prompt across all turns. The tradeoff is that Agent 2 is outside crewAI's observability and retry machinery.

### Why the conversation log is JSON, not plain text

The chat loop already knows the structure of every turn at collection time: turn number, question text, answer text, and whether it was skipped or blank. Capturing this as JSON means Agent 3 receives clean, pre-structured data instead of having to parse `Q3: ... A3: ...` strings from prose. Edge cases (`skipped`, `blank`, `i_dont_know`) are tagged at collection time — Agent 3 just reads the field. The only cost is a small `json` import in `main.py`.

### Why candidate background is optional

Requiring a resume creates friction and excludes early-career candidates who don't have one. When no background is provided, Agent 1 generates a general role brief and Agent 2 opens with a background-surfacing question. Agent 3 detects whether Q1 was a background question, skips scoring it, and writes a Background Note summarising what the candidate revealed instead. This keeps the session valid regardless of what the user provides.

### Why the research step exists

Without it, Agent 2 asks generic questions that could apply to any role. With it, the interviewer has role-specific context and asks questions grounded in what companies actually test — making a Data Analyst session meaningfully different from a Frontend Engineer Intern session or a Product Manager session. The research brief also gives Agent 3 a calibration anchor so it knows whether a given answer meets the bar for that specific role.

### Model choice

All three agents use `groq/llama-3.3-70b-versatile` via Groq's API — fast inference, low latency, and a free tier. The model string is defined once as a `MODEL` constant in `agent.py` and `main.py`. To switch providers, change the `MODEL` constant and add the corresponding API key to `.env`.

### Tradeoffs summary

| Decision | Benefit | Tradeoff |
|----------|---------|----------|
| LiteLLM loop for Agent 2 | Full turn-by-turn control, real user input | Agent 2 is outside crewAI observability |
| JSON conversation log | Clean structured input for Agent 3 | Small `json` dependency in `main.py` |
| Single model for all agents | Simple config, one API key | A stronger model for Agent 3 would improve report quality |
| Optional candidate background | Lower friction, broader accessibility | Brief is less personalised without context |
| CLI only | Fast to run and demo, no auth overhead | No session persistence across runs |

---

## Example Interview Transcripts

### Transcript 1 — Strong Candidate

**Role:** Data Analyst | **Focus:** Technical | **Background:** 3 years in analytics at a mid-size e-commerce company, proficient in SQL and Python

---

> **Interviewer:** Walk me through how you would approach cleaning a dataset that has missing values, duplicates, and inconsistent formatting before analysis.

**Candidate:** I'd start with a profiling pass — `df.info()` and `df.describe()` to understand the shape, types, and null counts before touching anything. For missing values, the first question is *why* they're missing. If a column is 60% null and the missingness isn't random, imputation can introduce bias — I'd either drop it or flag it as a separate boolean feature. For columns with sparse, random nulls in numeric fields, I'd impute with median rather than mean to avoid skew sensitivity. Duplicates I'd handle with `drop_duplicates()` after confirming which columns define a unique record — sometimes apparent duplicates are valid repeat events. For formatting, I'd normalise strings to lowercase stripped, parse dates into a consistent `datetime64` type, and validate categoricals against an expected value set. I'd log every transformation so the cleaning is reproducible and auditable.

> **Interviewer:** Good. Let's go hands-on. You have a table with `order_id`, `customer_id`, `product_id`, `order_date`, and `revenue`. Write a query to find the top 5 customers by total revenue in the last 90 days.

**Candidate:**

```sql
SELECT
    customer_id,
    SUM(revenue) AS total_revenue
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 5;
```

One thing I'd check first is whether `order_date` is a `DATE` or `TIMESTAMP` type — if it's a timestamp, I might cast or truncate to avoid edge cases at day boundaries. I'd also verify that `revenue` can be negative (refunds) and decide whether to include or exclude those rows depending on the business question.

> **Interviewer:** A key metric drops 20% week-over-week. Walk me through your investigation.

**Candidate:** First step is always confirming the signal is real — check the pipeline ran cleanly, there's no reporting lag, and the metric definition hasn't changed. Once I'm confident it's genuine, I decompose: I break the metric by every available dimension — region, channel, product line, platform, user cohort — to find where the drop is concentrated. A 20% overall drop that's 100% in one region is a very different problem from a broad decline. Then I look at the funnel — which step in the user journey shows the break? I'd also pull the same week from the prior year to control for seasonality. Once I have a leading hypothesis, I quantify its contribution to the total drop to confirm it explains the magnitude, then package it as a short brief for the relevant team — not just "here's the cause" but "here's the cause, here's the evidence, here's the recommended next step."

**Coaching note:** All three answers demonstrated a structured diagnostic process, used specific tools and syntax, and showed the candidate thinks about the *consumer* of the analysis, not just the computation. This candidate is interview-ready.

---

### Transcript 2 — Weak Candidate

**Role:** Product Manager | **Focus:** Case | **Background:** Not provided

---

> **Interviewer:** Before we dive in — could you give me a quick overview of your background?

**Candidate:** I've been working in marketing for about a year. I want to move into product because I think I'd be good at it.

> **Interviewer:** How would you decide what to build next for a B2B project management tool with 50,000 SMB users?

**Candidate:** I'd talk to customers and see what they want. You could also look at what competitors are doing and build something similar. Maybe run a survey.

> **Interviewer:** How would you prioritize three features: a mobile app, a Slack integration, and an advanced reporting dashboard?

**Candidate:** Probably the mobile app because everyone uses their phone now. The other two are useful too but mobile seems most important.

> **Interviewer:** A key product metric drops 20% week-over-week. How do you investigate?

**Candidate:** I'd look at the data and see what's different. Maybe ask the team if anything changed recently.

> **Interviewer:** How do you define success for a new onboarding flow?

**Candidate:** Whether users complete it and whether they like it. We could measure that with a survey after they finish.

**Coaching note:** Answers were consistently under-developed and lacked any analytical framework. The mobile-first prioritization was stated as preference with no reasoning. "Look at the data" is not an investigation method. The candidate has strong communication instincts but needs to learn prioritization frameworks (RICE, opportunity sizing) and a structured metric investigation approach before re-attempting PM screens.

---

### Transcript 3 — Tricky / Edge Case: The Overconfident Mid-Career Pivot

**Role:** Frontend Engineer Intern | **Focus:** Behavioral | **Background:** 8 years in QA engineering, no frontend development experience

---

> **Interviewer:** Before we dive in — could you give me a quick overview of your background?

**Candidate:** I have 8 years in QA at a fintech company. I've been doing automation testing in Selenium and Python. I've decided I want to move into frontend and I've been learning React for 3 months. I know software better than most interns — the intern label is just where I'm starting.

> **Interviewer:** Tell me about a time you had to learn something new quickly to complete a task.

**Candidate:** This happens constantly in QA. Last year our team migrated from REST to GraphQL APIs and I had to learn how to write GraphQL queries for our test suite in about two weeks. I read the docs, built test cases incrementally, and had full coverage before the deadline. I've been doing this kind of thing for 8 years.

> **Interviewer:** Describe a situation where you disagreed with a teammate. How did you handle it?

**Candidate:** I disagreed with a developer once about whether a bug was in scope for the release. I had evidence — a user flow that broke — and I presented it in the bug tracker with steps to reproduce and a video. They agreed to fix it. I'm usually right when I flag something, which is why I push when I think something matters.

> **Interviewer:** You're joining a team as an intern. A senior engineer reviews your first pull request and leaves 12 comments, some of which feel nitpicky. What do you do?

**Candidate:** I'd respond to each one, but honestly if some comments are nitpicky I'd probably push back on those. I know how code review works — I've reviewed code myself for years. I wouldn't just accept feedback I disagree with.

> **Interviewer:** What's the biggest gap between your QA background and what a frontend role requires?

**Candidate:** Mostly the React specifics — hooks, state management, that kind of thing. I'm learning fast though. I think my testing background is actually a huge advantage that most frontend devs don't have.

**Coaching note:** This candidate presents a legitimately interesting profile — strong systems thinking, genuine testing depth, and real software experience. The QA-to-frontend narrative has merit. However, two patterns surfaced that will hurt in intern interviews: (1) Framing 8 years of experience as a reason to push back on feedback in an intern context signals poor calibration — interns are expected to absorb feedback first and advocate second, once trust is built. (2) "I'm usually right" is a red flag regardless of seniority. The strongest answer to the PR question acknowledges the context honestly: "I'd engage with every comment genuinely, because even if some feel stylistic, understanding *why* the team codes a certain way is part of onboarding — I'd ask questions rather than push back on day one." The QA background is the differentiator; the attitude is the blocker.

---

## Project Structure

```
ai-mock-interview-coach/
├── prompts/
│   ├── research_agent.txt      # Agent 1 backstory and instructions
│   ├── interviewer.txt         # Agent 2 backstory and instructions
│   └── evaluator_agent.txt     # Agent 3 backstory and instructions
├── agent.py                    # Agent definitions + LLM config
├── task.py                     # Task descriptions for Agent 1 and Agent 3
├── crew.py                     # Crew assembly: run_research() and run_evaluation()
├── main.py                     # CLI entry point + Agent 2 chat loop
├── .env_sample                 # Environment variable template
reports/
│   ├── report_data_analyst_technical_20260503_042400.md      
│   ├── report_frontend_engineer_intern_behavioral_20260503_083015.md         
│   └── report_product_manager_case_20260503_114532.md     
├── requirements.txt
└── README.md
```

**Output file naming convention:**

```
report_<role>_<focus>_<timestamp>.md
```

Example: `report_data_analyst_technical_20260503_042400.md`
