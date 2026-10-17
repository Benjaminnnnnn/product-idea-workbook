# Steps: Turn the Product Idea Workbook into a Reusable Skill Repo

Goal: a repo of Claude skills that walks you (or anyone) through the workbook
for any new competitive product, and outputs a finished workbook.

The workbook is really one pipeline in four stages. Each stage takes the
previous stage's output as input:

```
Problem Space ──▶ Market Space ──▶ Solution Space ──▶ Value Space ──▶ Idea Brief
 (is it real?)    (who pays,        (what we build)    (why they'd     (1-page
                   who else wins?)                      switch + pay)   summary)
```

Treat each stage as a **gate**, not just a form. The most expensive PM mistake
is solving a problem nobody has. If a stage's evidence is weak, stop there.

---

## Step 1 — Set up the repo

```bash
cd product-manager-skills
git add "Product Idea Workbook template.docx" && git commit -m "Add source workbook"
```

Target layout (one folder per skill, flat, nothing extra):

```
product-manager-skills/
├── README.md                     # what this is + how to install
├── steps.md                      # this file
├── reference/
│   └── investpilot-example.md    # the filled workbook, converted to markdown
└── skills/
    ├── product-idea-workbook/    # orchestrator: runs stages 1→5 in order
    │   └── SKILL.md
    ├── customer-problem-space/
    │   ├── SKILL.md
    │   └── template.md
    ├── market-space/
    │   ├── SKILL.md
    │   └── template.md
    ├── solution-space/
    │   ├── SKILL.md
    │   └── template.md
    ├── customer-value-space/
    │   ├── SKILL.md
    │   └── template.md
    └── product-idea-brief/
        ├── SKILL.md
        └── template.md
```

## Step 2 — Convert the workbook to markdown (your worked example)

```bash
mkdir -p reference
pandoc "Product Idea Workbook template.docx" -t gfm \
  --extract-media=reference/media -o reference/investpilot-example.md
```

This is the "gold standard" example every skill points to. Models copy
examples far better than they follow abstract instructions.

## Step 3 — Write down the procedure for each stage

Each skill's `SKILL.md` lists the workbook's sub-steps in order, with **what
"good" looks like** for each one. Here's the procedure taken from the workbook:

### Skill 1: `customer-problem-space`
1. **Fertile land**: the product area or trend you're entering.
2. **Customer**: one specific actor (e.g. "individual beginner investor").
3. **Job to be done**: a verb plus an object ("build a diversified portfolio").
4. **Outcomes**: for each one, list *actual → desired → how it's measured*. Every outcome must be a number.
5. **Problem**: (a) the gap between actual and desired, quantified; (b) its root causes.
6. **Customer journey map**: the stages, what the customer does at each one, and the pain points.
7. **Use cases**: short names, each tagged with who it's for.
8. **Problem sizing**: per instance → per actor per year → total per year. Show the math and the source for every assumption.
9. **Problem category**: a 2–4 word label.
10. **Problem statement**: one paragraph covering the expectation, the reality, the gap, its size, and the need, all cited.

### Skill 2: `market-space`
1. **Overall market**: the actor population, with the estimate's reasoning and sources.
2. **TAM**: fill this in after pricing (Skill 4) is known.
3. **Segmentation**: 2–3 variables, each with 3 values.
4. **Target market profiles**: name, definition, and actor count for each segment, plus why this segmentation works (it must be measurable, accessible, substantial, distinct, and predictive).
5. **Competition**: direct competitors (product | company → their unique positioning) plus at least one **indirect category** (e.g. high-yield savings accounts). Most people forget the indirect one, and it's often the competitor that actually wins.
6. **Positioning analysis**: a current-state 2×2 map, a future-state map, the gaps you found, and a one-line **position to own**.
7. **Market focus decision**: the segment(s) you'll serve first and why.

### Skill 3: `solution-space`
1. **Product concept outline**: name, purpose, category, main attributes (taken from the positioning gaps), software and physical deliverables, input/output methods, infrastructure.
2. **User views**: a numbered user flow from launch to the core value moment, plus wireframes.
3. **Functional requirements**: what the system must do, traced back to the use cases.
4. **Context view**: the system boundary, its users, and the external systems and integrations it touches.
5. **Non-functional requirements**: performance, security, compliance, availability, accessibility.

> Steps 3–5 are empty in the template, so write them from standard PM practice.
> Rule of thumb: every functional requirement should trace back to a use case
> (Skill 1, step 7) or a positioning gap (Skill 2, step 6). If it doesn't, cut it.

### Skill 4: `customer-value-space`
1. **Features → benefits**: for each feature, which outcome from Skill 1 it improves.
2. **Value proposition strategy**: e.g. better / cheaper / easier / new, compared against the competitors named in Skill 2.
3. **Pricing model**: subscription, freemium, AUM %, usage-based, etc., and why.
4. **Customer cost items**: money, time, switching cost, learning curve, risk.
5. **Value proposition evaluation**: does the benefit clearly beat the cost, compared with the competitors *and* the indirect alternative?

> This section is also empty in the template. After pricing is set, go back
> and fill in TAM (Skill 2, step 2) = actors in the focus segment × annual price.

### Skill 5: `product-idea-brief`
A one-page summary written last: problem, who, size, position to own,
solution, value proposition, price, and the biggest risk.

### Skill 0: `product-idea-workbook` (orchestrator)
Runs Skills 1→5 in order, stops at each gate, and writes the finished
workbook to `workbooks/<product-name>.md`.

## Step 4 — Write each `SKILL.md`

Use this same shape for every skill:

```markdown
---
name: customer-problem-space
description: Use when defining or validating the customer problem for a new
  product idea — JTBD, outcomes, problem gap, root causes, journey map, use
  cases, problem sizing, problem statement.
---

# Customer Problem Space

## Inputs
- Product area or idea (ask if missing)

## Procedure
1. Fertile land — ...
2. ...  (the sub-steps from Step 3, each with a "good looks like" line)

## Quality gate (do not finish until all pass)
- [ ] Every outcome has actual, desired, and a measurement formula
- [ ] Sizing math is shown and every number has a cited source
- [ ] Problem statement numbers match the sizing section

## Output
Fill `template.md`. See `../../reference/investpilot-example.md` section 1.
```

Keep the `description` specific. It's what triggers the skill.

## Step 5 — Write each `template.md`

Copy the headings from the workbook section and replace the InvestPilot
content with `[placeholders]`, plus one hint line per field. Example:

```markdown
## 4. Outcomes
| Actual outcome | Desired outcome | Measurement method |
|---|---|---|
| [current metric + number] | [target number] | [formula] |
```

## Step 6 — Add the gates a senior PM would enforce

These are the checks that catch weak product ideas. Put them in each skill's
quality gate:

- **Evidence over opinion**: every market number is cited and the date is recent. Mark guesses as `ASSUMPTION`.
- **Internal consistency**: the same number must match everywhere it appears. The InvestPilot example breaks this twice: the statement says $4–8B while the sizing says $5–10B, and the segment thresholds are $500–10k in one place and <$2k in another. Have the skill check for this kind of mismatch automatically.
- **Traceability**: each outcome links to a cause, each cause to a feature, each feature to a benefit, and each benefit to pricing.
- **Indirect competition**: at least one non-obvious alternative, including "do nothing."
- **Kill criteria**: each stage ends with "proceed / pivot / stop" and one sentence on why.

## Step 7 — Test it on a new product

In Claude Code, run the orchestrator on an idea that has nothing to do with
investing:

```
Use product-idea-workbook for: a meal-planning app for shift-working nurses
```

Read the output against the gates from Step 6. Wherever it was vague or
skipped something, tighten that skill's procedure or "good looks like" line.
Run at least 2–3 different products before you trust it.

## Step 8 — Install the skills

Local use (all projects):

```bash
mkdir -p ~/.claude/skills
for d in skills/*/; do ln -s "$PWD/$d" ~/.claude/skills/; done
```

Restart Claude Code, then check that the skills show up in the skill list.

## Step 9 — Write the README and commit

README: one paragraph on what it does, the install command from Step 8, and
the test prompt from Step 7.

```bash
git add . && git commit -m "Add product idea workbook skills"
```

## Step 10 — Keep improving it

After each real product run, save the finished workbook to `reference/` as
another example, and add any new mistake you caught as a gate. The
skills get better as the set of examples grows.
