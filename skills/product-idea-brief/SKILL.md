---
name: product-idea-brief
description: Use when a product idea workbook is complete or partly complete and needs a one-page summary, executive brief, pitch summary, or go/no-go recommendation for stakeholders or investors.
---

# Product Idea Brief

The one-page summary that opens the Product Idea Workbook. It's written last,
and it's often the only part a stakeholder reads.

## Input

`workbooks/<product-slug>.md`, with as many stages done as possible.

## Procedure

1. Fill in `template.md` (in this skill's folder) using **only** what's in the workbook. Don't add new numbers or claims. `example.md` shows a finished brief for a fictional product.
2. If a stage isn't done, write "Not yet done: run `<skill>`" in its rows. Never fill a gap with a guess.
3. Choose the top 3 risks from the riskiest assumptions, the ASSUMPTION labels, and the stage decisions. For each, give the cheapest test that would confirm or kill it.
4. Make the decision:
   - **GO**: every stage says PROCEED.
   - **PIVOT**: any stage says PIVOT.
   - **NO-GO**: any stage says STOP.

   Then give the single next action.

## Quality gate

- [ ] Fits on one page (about 400 words)
- [ ] Every number matches the workbook exactly
- [ ] Unfinished stages are marked, not invented
- [ ] Each risk has a concrete, cheap test
- [ ] The decision follows from the stage decisions

## Output

Write or replace the `Product Idea Brief` section, which is the first section after the workbook heading in `workbooks/<product-slug>.md`.
