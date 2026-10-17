---
name: new-product-idea
description: Use when someone has a new product idea, wants to build a product that competes in an existing market, or asks to evaluate, validate, or work through a product idea end to end.
---

# New Product Idea

Run the full Product Idea Workbook on one idea: four stages and a brief, each
building on the one before. Every stage ends with a PROCEED / PIVOT / STOP
decision. Stopping a weak idea early is a good result, because it saves the
time and money of building it.

If the user has several ideas, or wants a quick check before the full
workbook, use `idea-screen` first and then run this on the idea that advances.

## Mode

- **Coach** (default): pause after each stage and ask before continuing.
- **Autopilot**: use this when the user says "autopilot," asks you to "run straight through," or asks not to be interrupted. Don't pause or ask questions. Make reasonable assumptions, label each one **ASSUMPTION**, and still run every review and check.

## Start

1. **Coach only:** ask for anything that's missing, in **one** message with at most 3 questions: the idea, the target customer (if known), and the geography or market. Skip anything the user has already given.
2. Choose the product name, and its slug: lowercase, with every run of non-alphanumeric characters replaced by `-`. "Shift Plate!" becomes `shift-plate`.
3. Create `workbooks/<slug>.md`. The first line is `# <Product name> — Product Idea Workbook`, then the date.
4. Keep the sections in this order: `## Product Idea Brief`, `## 1. Customer Problem Space`, `## 2. Market Space`, `## 3. Solution Space`, `## 4. Customer Value Space`, `## Appendix — References`.

## Each stage

| # | Stage | Skill |
|---|---|---|
| 1 | Is the problem real and big enough? | `customer-problem-space` |
| 2 | Who exactly, how many, and who else competes? | `market-space` |
| 3 | What do we build? | `solution-space` |
| 4 | Why would they switch and pay? | `customer-value-space` |
| 5 | One-page summary and go/no-go | `product-idea-brief` |

For each stage:
1. Run its skill and follow it all the way through. That skill uses `market-research` for numbers and `stage-review` before making its decision.
2. **Run the checker** on the workbook, fix every problem it reports, and run it again until it prints `OK`:
   ```
   python3 scripts/check_workbook.py workbooks/<slug>.md
   ```
   The script is in this skill's folder (in Claude Code: `${CLAUDE_SKILL_DIR}/scripts/check_workbook.py`). If you can't run Python, check the stage's quality gate by hand instead.
3. **Coach:** show a 3–5 bullet summary, the review verdict, and the decision, then ask "Continue to <next stage>?" **Autopilot:** keep going.

How to act on each decision:
- **PROCEED**: go on to the next stage.
- **PIVOT**: Coach: propose the specific pivot, and once the user agrees, update the earlier sections it affects. Autopilot: apply the pivot and note it in the decision. Either way, run that stage's gate again.
- **STOP**: skip the remaining stages and run `product-idea-brief` with the decision NO-GO.

In a Claude Code plugin the skills are named `product-idea-workbook:<skill>`. If your agent can't run skills by name, read that skill's `SKILL.md` and follow it.

## Finish

1. Do a consistency pass: every number, segment definition, and name that appears more than once must match everywhere. Fix any mismatch where the value first appears.
2. Run the checker with `--complete`, and fix problems until it prints `OK`. A stopped idea can't pass `--complete`, so run it without the flag.
3. Tell the user the file path, the decision, the top risk, and the next step.

## Rules

- Each stage reads the earlier sections from the workbook file. Never let two sections disagree.
- Never invent a source. A number with no source you can check is an ASSUMPTION.
- Keep the template's blank lines: put one before every table, and between label lines such as `**PROCEED**: …` and `**Riskiest assumption:** …`. Without them, tables render as plain text and lines run together. Write money as `\$47.99`, never `$47.99`, because many viewers render text between two `$` signs as math.
