---
name: customer-problem-space
description: Use when a product idea needs its customer problem defined or validated before market or solution work — "is this a real problem?", "who is the customer?", "what's the job to be done?", "how big is this problem?", outcomes, root causes, journey map, problem statement.
---

# Customer Problem Space

Stage 1 of the Product Idea Workbook. Prove the problem is real, measurable,
and big enough **before** anyone talks about solutions.

## Input

The product idea or area. Optional: target customer and geography. If these
are missing, ask at most 3 questions in one message, then write a draft. Don't
question the user field by field.

## Procedure

Fill in `template.md` (in this skill's folder) in order:

| # | Field | Good looks like |
|---|---|---|
| 1 | Fertile land | One sentence on a growing area or trend, plus why now. |
| 2 | Customer | One actor, specific enough that you could find 10 of them this week. Not "users" or "SMBs." |
| 3 | Job to be done | A verb plus an object, in the customer's words, with no solution in it. "Get paid for finished work," not "use our invoicing app." |
| 4 | Outcomes | 2–4 rows. Each one has an actual number, a desired number, and a measurement formula someone could compute from real data. |
| 5 | Problem | **Gap** = desired − actual, in the outcome's unit. **Causes**: 3–6 root causes of the gap. A cause is never a missing feature. |
| 6 | Customer journey map | 4–7 stages. For each: what they're doing, what they're thinking or feeling, the pain point, the opportunity. |
| 7 | Use cases | 4–8 short names, each tagged with the actor variant it serves. |
| 8 | Problem sizing | Per instance → per actor per year → total per year. Show every multiplier with its source. Give a low–high range, not false precision. |
| 9 | Problem category | A 2–4 word label. |
| 10 | Problem statement | One paragraph: expectation → reality → gap → size → "Therefore, a solution is needed to help [customer] [job]." |

## Evidence rules

- Search the web for data if you have a search tool. Cite inline as (Source, Year) and add the full entry to the workbook's `Appendix — References`.
- Never invent a source, a statistic, or a quote. If a number has no source someone can check, label it **ASSUMPTION** and say how to verify it.
- Prefer data from the last 3 years, and flag anything older.

## Quality gate

- [ ] The customer is one actor you could actually find
- [ ] The job to be done names no solution or product
- [ ] Every outcome has an actual number, a desired number, and a computable measurement
- [ ] The sizing math is shown, and every input is sourced or marked ASSUMPTION
- [ ] Every number in the problem statement matches section 8 exactly

Fix any failure before you finish. If a fix needs information you don't have, say so in the decision.

## Decision

Fill in the template's **Stage decision**:
- **PROCEED**: the problem is real and has been sized.
- **PIVOT**: the problem is real, but it's too small or belongs to a different customer. Name the better customer or job.
- **STOP**: there's no evidence anyone has this problem.

Add the single riskiest assumption, and how to test it with real customers.

## Output

Write the section to `workbooks/<product-slug>.md`. Create the file if it doesn't exist, or replace this section if it does.

## Common mistakes

| Mistake | Fix |
|---|---|
| The customer is "everyone" | Narrow it until the outcomes are the same for all of them. |
| A cause is really a feature ("there's no app for X") | Ask why the gap exists, not what's missing. |
| Industry revenue presented as problem size | Size the **loss caused by the gap**, not the size of the market. |
