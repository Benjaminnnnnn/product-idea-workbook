---
name: customer-value-space
description: Use when a product concept needs its value proposition, pricing, or customer costs worked out — "why would customers switch?", "how should we price this?", "is it worth the cost?", features vs benefits, willingness to pay, TAM from price.
---

# Customer Value Space

Stage 4 of the Product Idea Workbook. Show that the customer comes out
clearly ahead compared with the best alternative, including doing nothing,
after paying every cost, not just the price.

## Input

Sections 1–3 of `workbooks/<product-slug>.md`. If any are missing, ask for the
outcomes, the competitors, and the main features, or suggest running the
earlier stages first.

## Procedure

Fill in `template.md` (in this skill's folder) in order:

| # | Field | Good looks like |
|---|---|---|
| 1 | Product features and benefits | Each main feature → its benefit in the customer's words → the section 1 outcome it moves (actual → expected). |
| 2 | Value proposition strategy | One primary strategy (Better / Cheaper / Easier / Faster / New) compared with named competitors. Then: "For [focus segment] who [job], [product] is a [category] that [key benefit]. Unlike [main alternative], it [differentiator]." |
| 3 | Pricing model | The model (subscription, freemium, usage-based, one-time, take rate, ...) and price points. Justify the price against **both** competitor prices and the value created per actor per year (1.8). The price should capture part of that value and leave the customer clearly ahead. |
| 4 | Customer cost items | Money, time, effort, switching cost, learning curve, risk. An estimate for each, and how the product reduces it. |
| 5 | Value proposition evaluation | Value, total cost, and net value per actor per year for: your product, the top direct competitor, and the indirect alternative or doing nothing. Then a verdict. |

Then go back and fill in **TAM** in section 2.2: focus-segment actors × annual price per actor. Show the math.

## Evidence rules

The same as `customer-problem-space`: cite competitor prices with a source and date, never invent one, and label anything you can't check as **ASSUMPTION**.

## Quality gate

- [ ] Every feature maps to a section 1 outcome
- [ ] The value proposition names the alternative it beats
- [ ] The price is justified by competitor prices and by the value created
- [ ] Non-money costs (time, switching, learning, risk) are included
- [ ] Net value is clearly positive compared with the best alternative, including doing nothing
- [ ] TAM is filled in at 2.2, with the math shown

## Decision

Fill in the template's **Stage decision**:
- **PROCEED**: the customer clearly comes out ahead at a price that sustains the business.
- **PIVOT**: the value is real, but the price or cost structure doesn't work. Name the change (model, segment, scope).
- **STOP**: the customer doesn't come out ahead of what they do today.

## Output

Write or replace the section in `workbooks/<product-slug>.md`, and update 2.2.

## Common mistakes

| Mistake | Fix |
|---|---|
| Benefits that just restate features | Write the outcome the customer gets, using numbers from section 1. |
| Pricing set by gut feeling or cost-plus | Anchor it to the value created and to the alternatives. |
| Price is the only cost listed | Switching and learning costs are often what kill adoption. |
| Leaving "do nothing" out of the comparison | It's free and familiar. Show why the product is clearly better. |
