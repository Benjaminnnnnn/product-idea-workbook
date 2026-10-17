---
name: solution-space
description: Use when turning a validated customer problem and market position into a product concept — "what should we build?", product concept outline, user flow, wireframes, functional requirements, non-functional requirements, context diagram, MVP scope.
---

# Solution Space

Stage 3 of the Product Idea Workbook. Design the product that fills the
position to own, and nothing more. Every requirement must trace back to a
customer problem or a market gap.

## Input

Sections 1 and 2 of `workbooks/<product-slug>.md`. If either is missing, tell
the user the solution won't rest on a validated problem or position, and ask
whether to continue anyway.

## Procedure

Fill in `template.md` (in this skill's folder) in order:

| # | Field | Good looks like |
|---|---|---|
| 1 | Product concept outline | Name, a one-line purpose, and the category in the customer's words (the one competitors are compared in). 3–5 **main attributes**, each mapped to a gap from section 2.6. Software deliverables, physical deliverables (or "Not applicable"), input/output methods, production infrastructure. |
| 2 | User views | One primary platform. A numbered flow of 6–12 steps, from first launch to the **first value moment**. Each step: what the user does → what the system does. State the time to value. Add a text wireframe for each key screen. |
| 3 | Functional requirements | "The system shall…" statements. Each one traces to a use case (1.7) or a gap (2.6) and has a priority (Must / Should / Could). Mark the MVP set. |
| 4 | Context view | A Mermaid flowchart: the product in the middle, the customer and other actors, external systems (identity, payments, data providers, notifications, etc.), and labeled data flows. |
| 5 | Non-functional requirements | Performance, availability, security, privacy and compliance (name the regulations that apply to this domain and geography), accessibility, scalability. Every one has a **measurable target**. |

## Quality gate

- [ ] Every main attribute maps to a positioning gap from section 2
- [ ] The flow reaches the first value moment, and the time to value is stated
- [ ] Every Must requirement traces to a use case or gap (anything that doesn't is cut or moved to Could)
- [ ] The MVP is the smallest set of Musts that delivers the position to own
- [ ] Every non-functional requirement has a number
- [ ] The regulations that apply to this domain are named

## Decision

Fill in the template's **Stage decision**:
- **PROCEED**: the MVP is buildable and delivers the position.
- **PIVOT**: the scope is too big for a first release. Name what to cut.
- **STOP**: it can't be built or legally offered within realistic limits.

## Output

Write or replace the section in `workbooks/<product-slug>.md`.

## Common mistakes

| Mistake | Fix |
|---|---|
| A feature list that ignores the position to own | Start from the gaps in 2.6 and add only what fills them. |
| Functional requirements that describe screens ("a blue button") | Write what the system does, not how it looks. |
| Non-functional requirements like "fast" or "secure" | Give targets: "p95 response < 300 ms," "WCAG 2.2 AA." |
| A Must list nobody could ship in a quarter | Mark the MVP, and push the rest to Should or Could. |
