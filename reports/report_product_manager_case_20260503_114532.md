# Interview Coaching Report

## Session Summary
| Field | Value |
|-------|-------|
| Role | Product Manager |
| Interview type | Case |
| Candidate background | 3 years in B2B SaaS as a customer success manager; recently completed a PM certification; no prior PM title; strong domain knowledge in CRM and workflow automation tools |
| Questions scored | 5 |
| Overall score | 6/10 |
| Verdict | Demonstrates strong user empathy and domain credibility, but answers reveal a gap in structured product thinking — especially prioritization frameworks and metric selection — that will limit performance in senior PM screens. |

---

## Background Note
Provided upfront. The candidate transitioned from a customer success background and brings genuine proximity to users, which is a real asset in PM case interviews. Evaluation adjusted accordingly — penalizing for lack of engineering or data background would be unfair. The focus was on structured thinking, user empathy, and prioritization clarity rather than technical depth.

---

## Per-Answer Evaluation

### Q1: How would you decide what to build next for a B2B project management tool with 50,000 SMB users?

**What they said:** The candidate said they would "talk to customers," look at support tickets, and "see what features come up most often." They mentioned building a feedback form and running NPS surveys. They did not describe how they would synthesize the inputs, prioritize across them, or connect findings to business goals.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 3/5   | Methods were listed but not organized into a process |
| Depth     | 2/5   | No mention of segmentation (which 50K users?), no framework for prioritization, no mention of business strategy alignment |
| Relevance | 4/5   | Discovery methods were appropriate; the problem is what happens after |
| Evidence  | 2/5   | No example of having done this, no tool or format named (Jobs-to-be-Done, opportunity solution tree, etc.) |
| Role Fit  | 2/5   | PMs are expected to synthesize and prioritize, not just collect — the answer stopped at collection |

**What worked:** The instinct to go to customers first is correct and consistent with the candidate's CS background. Support tickets as a signal source is a practical, high-signal choice that many candidates overlook.

**What was missing:** After gathering inputs, the answer needs a synthesis and prioritization step. How do you decide which of the 30 things customers ask for is the one to build? A strong answer introduces a mental model — RICE, impact vs. effort, strategic bets — and connects the output to a business metric (retention, expansion revenue, activation).

---

### Q2: You're a PM at a company that makes scheduling software. DAU dropped 15% over the past two weeks. Walk me through your investigation.

**What they said:** The candidate described checking "if there's a bug" and looking at user complaints. They mentioned asking engineering if anything was deployed recently. They did not segment the drop, did not describe a systematic investigation sequence, and offered no hypothesis about likely causes.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 2/5   | No structure — three unconnected actions with no sequence or logic |
| Depth     | 2/5   | No segmentation by cohort, platform, geography, or feature area; no mention of funnel analysis |
| Relevance | 3/5   | Asking about recent deploys is a valid starting point; the rest was too thin |
| Evidence  | 1/5   | No prior investigation cited; no framework used |
| Role Fit  | 2/5   | Metric investigation is a core PM skill; this answer does not demonstrate a structured analytical mind |

**What worked:** Checking with engineering for recent deploys is the right first move for a sudden drop — it rules out regressions before looking for behavioral causes. This instinct reflects practical experience.

**What was missing:** A structured answer moves through: (1) confirm the data is real, (2) isolate the segment — is the drop across all users or concentrated in one cohort, platform, or feature? (3) check the funnel — where in the product flow is engagement falling? (4) cross-reference external factors. The candidate skipped steps 2–4 entirely.

---

### Q3: How would you prioritize three feature requests: (A) a mobile app, (B) a Slack integration, and (C) an advanced reporting dashboard?

**What they said:** The candidate said they would "survey customers to see what they want most" and pick based on the results. They then said the mobile app "seems important because everyone uses their phone." They did not apply a prioritization framework, did not ask clarifying questions about user segments or business strategy, and stated a preference without reasoning.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 2/5   | Survey-then-vote is not a prioritization strategy; the preference for mobile was stated without support |
| Depth     | 1/5   | No consideration of development cost, strategic fit, or who the 3 features serve |
| Relevance | 3/5   | The three features were addressed, but the approach to choosing among them was not |
| Evidence  | 1/5   | No framework, no example, no data source cited beyond a hypothetical survey |
| Role Fit  | 2/5   | Prioritization is the central PM skill being tested in this question; the answer did not demonstrate it |

**What worked:** The instinct to gather customer input before committing is sound. Recognizing that different features may serve different user segments — even if not explicitly stated — was implied in the answer.

**What was missing:** This question requires a framework. A strong answer would: (1) ask clarifying questions (who are the primary users? what's the company's strategic priority this quarter?), (2) evaluate each feature on impact, reach, confidence, and effort, (3) state a recommendation with explicit reasoning. Even a simple 2x2 (high impact / low effort) applied out loud shows more analytical rigor than "survey them."

---

### Q4: How do you define success for a new onboarding flow?

**What they said:** The candidate said they would look at whether users "complete the onboarding" and whether they "come back after the first session." They mentioned NPS as a metric. They did not connect onboarding completion to downstream business outcomes or describe how to measure "coming back."

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 3/5   | Two metrics named, but loosely defined — what counts as "completing" onboarding? |
| Depth     | 3/5   | Retention angle was correct but NPS was a misfit — onboarding NPS measures sentiment, not behavior |
| Relevance | 4/5   | Directly addressed the question with metrics that are genuinely relevant |
| Evidence  | 2/5   | No specific metric formula or target range; no prior onboarding project mentioned |
| Role Fit  | 3/5   | Shows awareness of leading and lagging indicators, even if loosely |

**What worked:** Pairing a completion metric with a return metric shows the candidate understands that finishing the flow and actually activating are different things. That distinction is more sophisticated than most candidates reach for.

**What was missing:** Activation metrics need precision. "Completion" should be defined as a specific event (e.g., "user completes 4 of 5 onboarding steps and creates their first project within 7 days"). "Comes back" should be a D7 or D30 retention figure. NPS is a relationship metric — it doesn't tell you whether onboarding *caused* the return. A better pairing: completion rate + time-to-value (how long until first meaningful action).

---

### Q5: You have 6 weeks and one engineer. You need to improve user retention. What do you do?

**What they said:** The candidate suggested adding a "tips and tricks" email sequence and building an in-app checklist to guide users through key features. They said these would help users "get more value" from the product. They did not explain how they chose these two solutions, what data led them there, or how they'd measure success.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 3/5   | Two concrete ideas were presented, but the constraint (6 weeks, 1 engineer) was not factored in |
| Depth     | 3/5   | Both ideas are valid retention levers but were presented as assumptions, not conclusions from analysis |
| Relevance | 4/5   | Onboarding emails and feature discovery checklists are genuinely linked to early retention |
| Evidence  | 2/5   | No data reference, no explanation of why these two over other options |
| Role Fit  | 3/5   | Shows product intuition but not the structured thinking expected in a PM case |

**What worked:** Both solutions the candidate proposed are real, practical, and scoped appropriately for a 6-week constraint with one engineer. Email sequences and in-app checklists are among the highest-ROI retention interventions at that resource level.

**What was missing:** The answer skipped the diagnostic step — *why* is retention low? The right move is to hypothesize a cause first (e.g., users who complete onboarding retain at 70%; those who don't retain at 20%) and then select an intervention that addresses that cause. The answer also needed a success metric: "I'd define success as a 5-point improvement in D30 retention within the cohort that receives the new flow."

---

## Overall Assessment

### Strengths (top 3)

**User Proximity and Empathy** — Across turns 1 and 5, the candidate consistently centered answers on user experience and what helps users "get value." This is a genuine asset that came through without prompting — a direct reflection of the CS background.

**Practical Tool Awareness** — The candidate repeatedly reached for real, commonly-used PM tools: NPS surveys, support ticket analysis, email sequences, in-app checklists. These aren't abstract — they reflect someone who has seen these tools work in practice.

**Correct Directional Instincts** — In turns 4 and 5, the candidate identified the right levers (activation, feature discovery, return behavior) even when the reasoning was incomplete. The instincts are sound; the structure is what needs development.

### Gaps (top 3)

**Prioritization Frameworks** — Turn 3 exposed the central weakness: the candidate does not have a repeatable method for choosing among competing options. Defaulting to "survey customers" avoids the hard intellectual work of prioritization and will fail in structured PM screens.

**Metric Precision** — Turns 1, 4, and 5 all produced loosely defined metrics ("comes back," "completes onboarding," "gets more value"). PMs are expected to operationalize metrics — define what counts as the event, the measurement window, and the target.

**Structured Investigation** — Turn 2 showed the candidate cannot yet walk through a metric drop investigation systematically. At senior PM level, this is table-stakes; at entry PM it's a strong differentiator. The gap here will limit performance at companies that emphasize data-driven product thinking.

### Practice Recommendations

1. **Prioritization Framework Drill (RICE):** Learn and practice the RICE framework (Reach, Impact, Confidence, Effort) until you can apply it out loud in under 2 minutes. Take the Q3 scenario and score each of the three features on each dimension, then defend your ranking. Do this for 3 different feature sets this week. The goal is not to memorize RICE — it's to have a structure that forces you to be explicit about trade-offs instead of going with instinct.

2. **Metric Operationalization Practice:** For every metric you name in a practice answer, immediately follow it with: what event triggers it, what time window it covers, and what a "good" number looks like. Example: "D30 retention — meaning the percentage of users who log in at least once between day 7 and day 30 — and I'd want to see it above 40% for SMB users based on industry benchmarks." Practice this habit until vague terms like "engagement" and "retention" no longer appear in your answers without a definition.

3. **Case Investigation Structure:** Memorize a 4-step metric drop structure and practice narrating it on unfamiliar scenarios. Step 1: validate the data. Step 2: segment the drop (which cohort, platform, or feature area?). Step 3: isolate the funnel step. Step 4: generate and rank hypotheses. Time yourself — you should be able to get through all 4 steps in 90 seconds before going deep on any one. Practice Q2 again using this structure from scratch before your next screen.

---

## Weakest Answer — Rewritten

**Question:** How would you prioritize three feature requests: (A) a mobile app, (B) a Slack integration, and (C) an advanced reporting dashboard?

**What they said:** The candidate said they'd survey customers and pick the most-requested option. They then expressed a preference for the mobile app based on general assumptions about phone usage.

**Why it fell short:** The answer had no framework, no clarifying questions, and no reasoning about cost or strategic fit. Expressing a preference without analysis is the exact behavior PM interviews are designed to screen out — it signals that decisions will be made on gut rather than structured thinking.

**Model answer:**

"Before I prioritize, I'd want to ask a few clarifying questions: Who are the primary users — individual contributors, team leads, or both? Is the company focused on acquiring new users, retaining existing ones, or expanding accounts? And what's the engineering scope for each — I'd assume mobile is a 3–4 month investment, Slack is 2–4 weeks, and reporting is somewhere in between.

Given that framing, here's how I'd think about it. The Slack integration has the highest reach and lowest effort — in B2B SaaS, Slack is where work actually happens, and a lightweight integration (create task from Slack, receive updates in channel) could drive daily active usage for users who aren't currently in the product every day. That maps directly to retention.

The reporting dashboard serves a different user — probably team leads and ops stakeholders who are already retained but need to demonstrate ROI upward. That's an expansion revenue play, not an activation play. High value, but narrower reach.

Mobile is the most expensive and the most dependent on how users work. I'd want to see whether mobile sessions are being attempted today — if our web product is already being accessed on mobile and the experience is broken, that's a clear signal. If not, mobile is a bet on a new use pattern, which is a higher-risk investment.

My recommendation given a short-term retention focus: Slack integration first, followed by a scoped version of reporting for team leads. Mobile goes on the roadmap with a decision gate at 90 days once we have data on whether the other two moves the retention needle."
