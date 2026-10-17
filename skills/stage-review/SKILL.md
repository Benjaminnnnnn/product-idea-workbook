---
name: stage-review
description: Use when a section of a product idea workbook (customer problem, market, solution, value, or brief) has been drafted and needs a critical review before its PROCEED / PIVOT / STOP decision, or when someone asks to stress-test, red-team, or poke holes in a product idea.
---

# Stage Review

Review the section the way a skeptical investor or a VP of Product would.
Your job is to find what would make this idea fail, not to praise it.

## Input

The workbook file (`workbooks/<product-slug>.md`) and the section to review.
If there's no file, review the text the user gives you.

## Procedure

1. Read the section, and every earlier section it builds on.
2. Go through the section's quality gate, which is in that stage's skill (for example `market-space`). Mark each item pass or fail, quoting the line that proves it.
3. Ask these five questions:
   - **Evidence:** which claim would collapse if its source turned out to be wrong? Is that claim cited, or labeled ASSUMPTION?
   - **Consistency:** does any number, name, or definition differ from an earlier section?
   - **Customer:** would a real member of this customer group recognize this problem, in these words?
   - **Competition:** what would the strongest competitor say back? What about the option of doing nothing?
   - **Decision:** does the PROCEED / PIVOT / STOP decision follow from the evidence, or from enthusiasm?
4. List the findings, most serious first.

## Output

```
Review: <section>
Verdict: READY | FIX FIRST

| # | Severity | Where | Problem | Fix |
|---|---|---|---|---|
| 1 | blocker / major / minor | <subsection> | <quote + problem> | <specific fix> |

Checked: <gate items and questions that passed>
```

- **blocker**: a finding that would change the stage decision. Any blocker means the verdict is FIX FIRST.
- **major**: weakens the case, but doesn't change the decision.
- **minor**: wording or format.

## After the review

Apply every blocker and major fix to the section, then review it again. Stop
after 2 rounds. Any item that's still open becomes a named risk in the stage
decision.

## Rules

- Quote the exact line for every finding. "Could be stronger" isn't a finding.
- Don't include a praise section.
- If you find nothing, list what you checked, so it's clear the review was real.
