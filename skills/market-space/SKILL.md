---
name: market-space
description: Use when a product idea needs its market sized, segmented, or positioned against competitors — "how big is the market?", "who are the competitors?", "where should we position?", "which segment first?", positioning map, position-to-own, market focus.
---

# Market Space

Stage 2 of the Product Idea Workbook. Count the customers, split them into
segments that need different things, map the competition (including what
customers do instead of buying anything), and pick a position you can own.

## Input

Section `1. Customer Problem Space` from `workbooks/<product-slug>.md`. If it's
missing, ask for the customer, the job to be done, and the problem statement,
or suggest running `customer-problem-space` first.

## Procedure

Fill in `template.md` (in this skill's folder) in order. `example.md` shows a finished section for a fictional product: match its depth and evidence, but don't copy its content.

| # | Field | Good looks like |
|---|---|---|
| 1 | Overall market | The actor population and its **count**, with the estimate chain (sourced number × factor). Count people or businesses, not dollars. |
| 2 | TAM | Leave as pending. `customer-value-space` fills it in once there's a price. |
| 3 | Segmentation | 2–3 variables with about 3 values each. Pick variables that change what the customer needs or buys (behavior, size, goal), not demographics alone. |
| 4 | Target market profiles | For each segment: a name, a definition with **numeric thresholds**, and an actor count. Then the estimation reasoning, and why this segmentation works: it's measurable, reachable, big enough, distinct, and changes what you'd build. |
| 5 | Competition | 2–4 **direct** competitors, each written as Product \| Company and its unique positioning in one sentence. At least one **indirect** category, with why customers treat it as a substitute and 2–3 examples. Plus **do nothing**: what customers do today without a product. |
| 6 | Positioning analysis | **a.** A current-state map on two axes the customer actually decides on (tie them to the section 1 outcomes), with the competitors placed. **b.** A future-state map with your product in a gap, plus the list of gaps. **c.** The position to own, in one sentence. |
| 7 | Market focus decision | The segment(s) to serve first. Explain why using size, how easy they are to reach, how well they fit the position, and their willingness to pay. |

Draw the maps as Mermaid `quadrantChart` blocks so they render on GitHub. Point coordinates run from 0 to 1.

## Evidence rules

Get every number through the `market-research` skill. If it isn't available, follow its rules yourself: research at most 8 numbers, with all the searches in one turn, open each source and find the number on it, cite it inline as (Publisher, Year), add the full entry to the workbook's `Appendix — References`, and label anything you can't check as **ASSUMPTION**. Never invent a source.

## Quality gate

- [ ] The overall market is a count of actors with an estimate chain
- [ ] The segment counts add up to the overall market (or the difference is explained)
- [ ] Segment thresholds are identical in the definitions, the profiles, and the focus decision
- [ ] There's at least one indirect category, and "do nothing" is covered
- [ ] The map axes tie to the section 1 outcomes, and the position to own sits in a visible gap
- [ ] The focus is one segment (or a tight adjacent pair), not all of them

## Decision

First run the `stage-review` skill on the section and apply its fixes. Then fill in the template's **Stage decision**:
- **PROCEED**: there's a gap worth owning and a focus segment you can reach.
- **PIVOT**: there's no real gap on these axes, or the focus segment is too small. Name the alternative position or segment.
- **STOP**: the market is already well served on every axis customers care about.

## Output

Write or replace the section in `workbooks/<product-slug>.md`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Axes nobody makes a buying decision on | Use the outcomes from section 1. |
| Only direct competitors listed | Ask what customers use today when they don't buy anything. |
| "We'll target all segments" | Pick the one where you win first, and say why. |
| Calculating TAM before there's a price | Leave it pending until stage 4. |
