# Interview Coaching Report

## Session Summary
| Field | Value |
|-------|-------|
| Role | Data Analyst |
| Interview type | Technical |
| Candidate background | 2 years experience in Excel-based reporting; transitioning from operations; no formal SQL or Python experience mentioned |
| Questions scored | 5 |
| Overall score | 5.5/10 |
| Verdict | Shows genuine analytical curiosity and solid business intuition, but answers lack technical grounding and specific evidence, which will be a blocker at most data analyst screenings. |

---

## Background Note
Turn 1 was a background-surfacing question. The candidate revealed they spent two years in an operations role doing Excel-based reporting and are self-teaching SQL via online courses. No formal analytics background but demonstrated clear motivation for the transition. Turn 1 was not scored; this context informed the evaluation of all subsequent answers.

---

## Per-Answer Evaluation

### Q2: Walk me through how you would approach cleaning a dataset that has missing values, duplicates, and inconsistent formatting before analysis.

**What they said:** The candidate said they would "go through the data and remove anything that looks wrong," handle missing values by filling them in with averages, and delete duplicates. They mentioned checking column names for consistency but did not describe any systematic process or tooling.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 2/5   | Answer was loosely structured — no sequence, no phases, jumped between ideas |
| Depth     | 2/5   | Did not address when to impute vs. drop, or how to assess missingness patterns |
| Relevance | 4/5   | Addressed all three issues mentioned in the question |
| Evidence  | 1/5   | No tool mentioned (SQL, pandas, Excel Power Query) and no real example cited |
| Role Fit  | 2/5   | Replacing missing values with averages without qualification is a red flag for a data analyst role |

**What worked:** The candidate correctly identified the three problem types from the question and attempted to address each one. Mentioning column name consistency showed awareness beyond just row-level issues.

**What was missing:** No discussion of *why* values are missing — MCAR vs. MAR matters before deciding on imputation strategy. No mention of profiling tools (e.g., `df.info()`, `COUNT(*)` vs `COUNT(col)`). The answer needed a concrete workflow, not a list of actions.

---

### Q3: You're given a sales table with columns: order_id, customer_id, product_id, order_date, and revenue. Write a query to find the top 5 customers by total revenue in the last 90 days.

**What they said:** The candidate said they would "use a SELECT statement to add up the revenue, filter by date, and sort it." They sketched a partial query mentally but could not produce working SQL syntax. They mentioned GROUP BY but placed it incorrectly in their verbal description.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 2/5   | Could not articulate clause order; verbal description was muddled |
| Depth     | 2/5   | Did not address the date filter using a proper interval or function |
| Relevance | 3/5   | Understood what the query needed to accomplish, even if execution fell short |
| Evidence  | 1/5   | No working syntax produced; could not demonstrate hands-on SQL ability |
| Role Fit  | 2/5   | Basic aggregation with filtering is a baseline requirement for data analyst roles |

**What worked:** The candidate correctly identified the key operations needed — aggregation, filtering, and sorting — which shows conceptual understanding of the problem even without fluent SQL.

**What was missing:** A working answer requires: `WHERE order_date >= CURRENT_DATE - INTERVAL '90 days'`, `GROUP BY customer_id`, `SUM(revenue)`, `ORDER BY total_revenue DESC`, `LIMIT 5`. None of these were produced correctly. The candidate needs hands-on query practice, not just conceptual familiarity.

---

### Q4: Describe a time you found something surprising or unexpected in data. What did you do with it?

**What they said:** The candidate described noticing that a weekly operations report showed a sudden 40% drop in a throughput metric. They flagged it to their manager, who confirmed it was a data entry error from an upstream team. The issue was corrected and the report was rerun.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 4/5   | Clear narrative with a beginning, middle, and resolution |
| Depth     | 3/5   | Did not describe how they diagnosed the anomaly or what they checked first |
| Relevance | 5/5   | Directly answered the question with a real, credible example |
| Evidence  | 4/5   | Specific metric (40% drop), specific cause (data entry error), specific action (flagged, corrected) |
| Role Fit  | 3/5   | Shows data quality awareness but resolution was passive — escalation only, no independent investigation |

**What worked:** This was the strongest answer in the session. The 40% figure made it concrete, and the upstream-error cause was realistic and believable. The candidate showed they treat anomalies as signals rather than ignoring them.

**What was missing:** The answer would have been stronger with one sentence on *how* they identified it as an error — did they cross-reference another source? Check historical baselines? That diagnostic step is what separates data analysts from report readers.

---

### Q5: How would you explain the difference between a mean and a median to a non-technical stakeholder, and when would you use each?

**What they said:** The candidate explained mean as "adding everything up and dividing," and median as "the middle number." They said they'd use median "when there are outliers, like salaries" and mean "for things that are more evenly spread." They did not give an example with actual numbers.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 3/5   | Definitions were accurate but the stakeholder framing was never actually applied |
| Depth     | 3/5   | The salary outlier example is correct but shallow — no elaboration on what skew means |
| Relevance | 4/5   | Addressed both definitions and the selection criteria |
| Evidence  | 2/5   | No concrete numbers or walkthrough — a stakeholder explanation needs a story, not a definition |
| Role Fit  | 4/5   | Shows awareness of when summary statistics mislead, which is a key analyst skill |

**What worked:** The instinct to reach for salaries as an outlier example was good — it's relatable and accurate. The candidate demonstrated they understand *why* the choice matters, not just the mechanics.

**What was missing:** A strong answer would give a quick example: "If 9 employees earn $50K and one earns $500K, the mean is $95K — which nobody earns. The median of $50K is what most people experience." Walking a stakeholder through a scenario is the actual skill being tested here.

---

### Q6: If a key business metric drops 20% week-over-week, how would you investigate the cause?

**What they said:** The candidate said they would "look at the data from both weeks and compare them," check if the metric was calculated the same way, and ask stakeholders if anything changed. They mentioned looking at "sub-segments" but did not name any specific dimensions or a structured framework.

| Dimension | Score | Observation |
|-----------|-------|-------------|
| Clarity   | 2/5   | No structure — answer reads as a list of things to check, not a diagnostic process |
| Depth     | 2/5   | Did not mention dimension slicing (time, geography, product, channel), data pipeline checks, or seasonality |
| Relevance | 4/5   | All three points were relevant, just underdeveloped |
| Evidence  | 1/5   | No example of having done this; no framework referenced (e.g., issue tree, top-down decomposition) |
| Role Fit  | 2/5   | Metric investigation is a core analyst skill; the answer does not demonstrate a structured approach |

**What worked:** Checking for calculation consistency before assuming a real business change is a mature instinct — many candidates skip straight to root-cause storytelling. Mentioning stakeholder interviews shows cross-functional awareness.

**What was missing:** A structured answer would move through layers: (1) confirm the data is correct, (2) isolate the segment — which dimension breaks show the drop? (3) check external factors, (4) form and test hypotheses. The candidate had the ingredients but no recipe.

---

## Overall Assessment

### Strengths (top 3)

**Anomaly Detection Instinct** — In Q4, the candidate demonstrated they notice when data behaves unexpectedly and treat it as a signal. The 40% drop example in turn 4 was specific and credible, and the response showed ownership of data quality.

**Conceptual Understanding Without Syntax** — Across Q3 and Q5, the candidate consistently understood *what* needed to happen even when they couldn't execute it technically. This is a genuine foundation to build on.

**Stakeholder Awareness** — Turn 5 and turn 6 both showed the candidate thinks about who consumes the output, not just the computation. Asking stakeholders if something changed (Q6) and framing median vs. mean in terms of what's relatable (Q5) reflect good communication instincts.

### Gaps (top 3)

**SQL Execution** — Turn 3 made clear that conceptual familiarity with SQL is not the same as being able to write it. Basic aggregation with a date filter is tested in virtually every data analyst screen; the candidate cannot currently pass that bar.

**Structured Problem-Solving** — Turns 2 and 6 both revealed the same pattern: the candidate lists actions rather than following a diagnostic process. Data cleaning and metric investigation both have standard frameworks that were absent here.

**Answer Evidence Density** — With the exception of turn 4, answers lacked concrete numbers, tools, or outcomes. Observations like "I would check sub-segments" carry no weight without specifying which dimensions, in which tool, with what result.

### Practice Recommendations

1. **SQL Daily Query Drill:** Write 2 queries per day on a real dataset (Mode Analytics public datasets or SQLZoo). Focus specifically on: `GROUP BY` + `HAVING`, date filtering with `INTERVAL`, window functions (`RANK`, `ROW_NUMBER`). Time yourself — analyst screens are often timed. Do not move on until you can write the Q3 query from memory in under 3 minutes.

2. **Metric Investigation Framework:** Memorize and practice a 4-step diagnostic: (1) data validity check, (2) dimensional decomposition (break by time, geography, product, segment), (3) external context (seasonality, releases, outages), (4) hypothesis ranking by impact. Practice narrating this out loud using a made-up scenario for 10 minutes, 3 times this week — interviewers evaluate your structure before your conclusion.

3. **Answer Anchoring with Numbers:** After writing any answer, review it and insert at least one concrete number, one tool name, and one outcome. "I checked the data" becomes "I ran a `COUNT(*)` vs `COUNT(order_id)` check in SQL and found 340 null rows, which I flagged in the Jira ticket." This habit alone will raise Evidence scores by 2 points across the board.

---

## Weakest Answer — Rewritten

**Question:** If a key business metric drops 20% week-over-week, how would you investigate the cause?

**What they said:** The candidate said they would compare the two weeks, check if the metric was calculated consistently, and ask stakeholders if anything changed. No structured framework or specific dimensions were mentioned.

**Why it fell short:** The answer had no diagnostic sequence and no specificity. "Look at the data from both weeks" is not a method — it's a restatement of the task. Analysts are evaluated on whether they can narrow a problem systematically, not just describe that they would look at it.

**Model answer:**

"The first thing I'd do is confirm the drop is real — check whether the data pipeline ran cleanly, whether there's a reporting lag, and whether the metric definition changed. Once I'm confident the signal is genuine, I'd move into decomposition: I'd break the metric down by every available dimension — time of day, channel, product line, geography — to find where the drop is concentrated. A 20% overall drop that's 100% concentrated in one region or one product tells a very different story than a broad decline across all segments.

From there I'd layer in external context — did a campaign end? Was there a pricing change? Is there a seasonal pattern I should account for? I'd pull the same week from the prior year to check. Once I have a hypothesis — say, 'mobile checkout conversion dropped in the Western region following the app update' — I'd quantify its contribution to the total drop to confirm it explains the magnitude, then bring that to the product or engineering team with the data packaged as a short brief. The goal isn't just to find the cause — it's to give the team something they can act on."
