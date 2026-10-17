---
name: new-product-idea
description: Use when someone has a new product idea, wants to build a product that competes in an existing market, or asks to evaluate, validate, or work through a product idea end to end.
---

# New Product Idea

Run the full Product Idea Workbook on one idea: four stages and a brief, each
building on the one before. Every stage ends with a PROCEED / PIVOT / STOP
decision. Stopping a weak idea early is a good result, because it saves the
time and money of building it.

## Start

1. Ask for anything that's missing, in **one** message with at most 3 questions: the idea, the target customer (if known), and the geography or market. Skip anything the user has already given.
2. Create `workbooks/<product-slug>.md` with this heading: `# <Product or idea name> — Product Idea Workbook`, then the date.
3. Keep the sections in workbook order: `Product Idea Brief`, `1. Customer Problem Space`, `2. Market Space`, `3. Solution Space`, `4. Customer Value Space`, `Appendix — References`.

## Stages

| # | Stage | Skill |
|---|---|---|
| 1 | Is the problem real and big enough? | `customer-problem-space` |
| 2 | Who exactly, how many, and who else competes? | `market-space` |
| 3 | What do we build? | `solution-space` |
| 4 | Why would they switch and pay? | `customer-value-space` |
| 5 | One-page summary and go/no-go | `product-idea-brief` |

Run each skill and follow it all the way through. In a Claude Code plugin the skills are named `product-idea-workbook:<skill>`. If your agent can't run skills by name, read `../<skill>/SKILL.md` and follow it.

## After each stage

Show the user a 3–5 bullet summary, the quality gate result, and the decision. Then:

- **PROCEED**: ask "Continue to <next stage>?", unless the user asked you to run straight through.
- **PIVOT**: propose the specific pivot. If the user agrees, update the earlier sections it affects, then run that stage's gate again.
- **STOP**: don't run the remaining stages. Run `product-idea-brief` with the decision set to NO-GO.

## Rules

- Each stage reads the earlier sections from the workbook file. If new information changes an earlier number or definition, update it where it first appears. Never let two sections disagree.
- Before the brief, do a consistency pass: every number, segment definition, and name that appears more than once must match everywhere.
