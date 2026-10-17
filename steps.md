# Steps: Turn the Product Idea Workbook into an Installable Skill Repo

**Goal:** a public repo of agent skills that walks anyone through the Product
Idea Workbook for a new competitive product. People can install it with one
command, see a finished example right away, and want to star it.

**The workbook is used as structure only.** Its sections become the skill
procedures and templates. None of the original workbook's product content
goes into the repo, and neither does the `.docx`.

The workbook is one pipeline in four stages plus a summary. Each stage feeds
the next and ends with a gate:

```
Problem Space ──▶ Market Space ──▶ Solution Space ──▶ Value Space ──▶ Idea Brief
 (is it real?)    (who, how many,    (what we build)    (why they'd     (1-page
                   who else wins?)                       switch + pay)   summary)
```

The most expensive PM mistake is building for a problem that isn't real.
If a stage's evidence is weak, the skill should say **stop** or **pivot**,
not keep filling in forms.

**Status:** Steps 1–8 are done, plus the quality and release setup:
`market-research` and `stage-review` skills, a worked example
(`examples/shiftplate.md`), the checker, tests, evals, CI, and one-command
releases. Next up: Step 9.

### Day-to-day commands

| When | Command |
|---|---|
| After editing `examples/shiftplate.md` | `python3 scripts/build.py` (regenerates each skill's `example.md`) |
| Before every commit | `python3 -m unittest discover -s tests` |
| Check any workbook | `python3 skills/new-product-idea/scripts/check_workbook.py workbooks/<slug>.md --complete` |
| Before a release (≈$0.50) | `claude plugin eval . --tag trigger` |
| Before a big release (slow, costs more) | `claude plugin eval . --tag full --allow-tools Write Edit WebSearch WebFetch "Bash(python3 *)"` |
| Release | Add notes under `## [Unreleased]` in `CHANGELOG.md`, then `python3 scripts/release.py 0.1.0` and `git push origin main --follow-tags` |

The tag push runs `.github/workflows/release.yml`. It checks that the tag
matches `plugin.json`, reruns every check, builds one zip per skill for
claude.ai, and publishes the GitHub Release with the changelog notes. If any
check fails, nothing is published.

---

## Step 1 — Pick a name that won't get lost

GitHub already has popular repos called `product-manager-skills`
(e.g. deanpeters/Product-Manager-Skills, ~7k stars). Choose a name that says
what's different about yours. This guide uses:

- Repo: `product-idea-workbook`
- Plugin: `product-idea-workbook`
- Marketplace: `product-idea`

Swap in your own names everywhere below if you pick different ones.

## Step 2 — Keep the `.docx` out of the repo

The template's section structure is already written out in Step 4, so the
`.docx` isn't needed in the repo.

```bash
mv "Product Idea Workbook template.docx" ~/Documents/   # keep it outside the repo
echo "*.docx" >> .gitignore                             # so it never gets committed
```

## Step 3 — Create the layout

This one layout works for **Claude Code plugins** *and* the cross-agent
`npx skills` installer (Codex, Cursor, Copilot, Gemini, and 40+ more). Both
look for `skills/<name>/SKILL.md`.

```
product-idea-workbook/
├── .claude-plugin/
│   ├── marketplace.json          # makes the repo installable via /plugin
│   └── plugin.json
├── skills/
│   ├── new-product-idea/         # orchestrator: coach or autopilot, runs stages 1→5
│   │   ├── SKILL.md
│   │   └── scripts/check_workbook.py   # stdlib checker the skill runs after each stage
│   ├── customer-problem-space/   # SKILL.md, template.md, example.md (generated)
│   ├── market-space/             # same
│   ├── solution-space/           # same
│   ├── customer-value-space/     # same
│   ├── product-idea-brief/       # same
│   ├── market-research/          # SKILL.md: sourced numbers, URL for each one
│   ├── idea-screen/              # SKILL.md: cheap 1–5 idea comparison before a full run
│   └── stage-review/             # SKILL.md: skeptical review before each decision
├── examples/shiftplate.md        # the worked example, the single source for every example.md
├── evals/                        # claude plugin eval cases (--tag trigger | full)
├── tests/test_repo.py            # checker and repo checks (stdlib unittest)
├── scripts/
│   ├── build.py                  # regenerates example.md files, builds dist/*.zip
│   └── release.py                # one-command release
├── .github/workflows/            # ci.yml (every push), release.yml (on a v* tag)
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

Every skill is self-contained (it never reads another skill's folder), so it
works the same when uploaded to claude.ai one zip at a time. There are no
subagents or hooks, because neither runs in claude.ai or most other agents.

## Step 4 — Write each stage's procedure (from the workbook sections)

Each `SKILL.md` lists its sub-steps in order, with a one-line **"good looks
like"** for each one. The sub-steps below come straight from the workbook's
sections.

### `customer-problem-space`
1. **Fertile land**: the product area or trend being entered.
2. **Customer**: one specific actor, not "everyone."
3. **Job to be done**: a verb plus an object.
4. **Outcomes**: for each one, list *actual → desired → measurement method*. Every outcome must be a number.
5. **Problem**: (a) the gap between actual and desired, quantified; (b) its root causes.
6. **Customer journey map**: the stages, what the customer does at each one, and the pain points.
7. **Use cases**: short names, each tagged with who it's for.
8. **Problem sizing**: per instance → per actor per year → total per year. Show the math and a source for every assumption.
9. **Problem category**: a 2–4 word label.
10. **Problem statement**: one paragraph covering the expectation, the reality, the gap, its size, and the need, all cited.

### `market-space`
1. **Overall market**: the actor population, with the estimate's reasoning and sources.
2. **TAM**: filled in after pricing is known (see `customer-value-space`).
3. **Market segmentation**: 2–3 variables, each with about 3 values.
4. **Target market profiles**: name, definition, and actor count for each segment, plus why this segmentation works (it must be measurable, accessible, substantial, distinct, and predictive).
5. **Competition**: direct competitors (product | company → their unique positioning) plus at least one **indirect category**, including "do nothing." The indirect alternative is the one most often missed, and often the one that actually wins.
6. **Positioning analysis**: a current-state map, a future-state map, the gaps you found, and a one-line **position to own**.
7. **Market focus decision**: the segment(s) to serve first and why.

### `solution-space`
1. **Product concept outline**: name, purpose, category, main attributes (taken from the positioning gaps), software and physical deliverables, input/output methods, production infrastructure.
2. **User views**: a numbered flow from first launch to the core value moment, plus wireframes or screen descriptions.
3. **Functional requirements**: what the system must do.
4. **Context view**: the system boundary, its users, and the external systems it connects to.
5. **Non-functional requirements**: performance, security, privacy and compliance, availability, accessibility.

### `customer-value-space`
1. **Product features and benefits**: for each feature, which outcome it improves.
2. **Customer value proposition strategy**: better / cheaper / easier / new, compared with the named competitors.
3. **Pricing model**: subscription, freemium, usage-based, one-time, etc., and why.
4. **Customer cost items**: money, time, switching cost, learning curve, risk.
5. **Customer value proposition evaluation**: does the benefit clearly beat the cost, compared with the competitors *and* the indirect alternative? Then go back and fill in TAM: focus-segment actors × annual price.

### `product-idea-brief`
Written last, on one page: problem, customer, size, position to own,
solution, value proposition, price, biggest risk, and the decision.

### `new-product-idea` (orchestrator)
1. Asks for the product idea (and the target customer, if the user knows it).
2. Runs the four stage skills in order, showing each gate's result.
3. Writes the finished workbook to `workbooks/<product-name>.md`.

## Step 5 — Write each `SKILL.md`

Use the same shape for every skill:

```markdown
---
name: market-space
description: Use when a product idea needs its market sized, segmented, or
  positioned against competitors — "how big is the market?", "who are the
  competitors?", "which segment first?"
---

# Market Space

## Input
- The output of customer-problem-space (ask for it if missing)

## Procedure
1. Overall market — ... Good looks like: ...
2. ...

## Quality gate (all must pass before finishing)
- [ ] Every number has a source or is marked ASSUMPTION
- [ ] At least one indirect competitor, including "do nothing"
- [ ] Position to own fits in one sentence and fills a gap on the map

## Decision
End with: PROCEED / PIVOT / STOP, plus one sentence on why.

## Output
Fill in `template.md` in this folder.
```

Tips:
- The `description` is what triggers the skill. Start it with "Use when…" and list only the situations it covers, never its steps. If the description summarizes the steps, agents tend to follow that summary and skip the body.
- Keep `SKILL.md` short and put the long template in `template.md`. The agent only loads the template when it needs it.
- Inside a plugin, skills are called as `/product-idea-workbook:market-space`.

## Step 6 — Write each `template.md`

Use the workbook's headings, with `[placeholders]` and one hint per field:

```markdown
## 4. Outcomes
| Actual outcome | Desired outcome | Measurement method |
|---|---|---|
| [current metric + number] | [target number] | [formula] |
```

## Step 7 — Add the checks a senior PM would make

Add these to the quality gates. They're what make the output stand out from
generic AI writing:

- **Evidence over opinion**: every market number is cited with a recent date, or marked `ASSUMPTION`.
- **Internal consistency**: a number that appears in more than one place must match everywhere (sizing vs. statement, segment definitions vs. profiles). Problem sizing and segment definitions are where mismatches usually creep in.
- **Traceability**: each outcome links to a cause, each cause to a feature, each feature to a benefit, and each benefit to pricing. Cut any requirement that doesn't trace back to a use case or a positioning gap.
- **Indirect competition**: at least one non-obvious alternative.
- **Kill criteria**: every stage ends with proceed / pivot / stop.

## Step 8 — Make the plugin installable

`.claude-plugin/plugin.json`:

```json
{
  "name": "product-idea-workbook",
  "description": "Turn a product idea into a validated, competitive product concept: problem, market, solution, value.",
  "version": "0.1.0",
  "author": { "name": "Benjamin Zhuang" },
  "repository": "https://github.com/<you>/product-idea-workbook",
  "license": "MIT",
  "keywords": ["product-management", "product-discovery", "jtbd", "positioning", "skills"]
}
```

`.claude-plugin/marketplace.json` (the whole repo is the plugin, so its
`source` is `"./"`):

```json
{
  "name": "product-idea",
  "owner": { "name": "Benjamin Zhuang" },
  "plugins": [
    {
      "name": "product-idea-workbook",
      "source": "./",
      "description": "Turn a product idea into a validated, competitive product concept."
    }
  ]
}
```

Check the files and test the install locally before you push:

```bash
claude plugin validate .                  # last line should be: ✔ Validation passed
claude plugin marketplace add ./
claude plugin install product-idea-workbook@product-idea
```

Keep the plugin `name` the same in both files. A mismatch is the most common
cause of failed installs.

## Step 9 — Test it, and keep the output as your public example

Run it on 2–3 products from different industries:

```
/product-idea-workbook:new-product-idea a meal-planning app for shift-working nurses
```

- Check the output against Step 7's gates. Wherever it was vague, tighten that skill's procedure.
- Use a product other than ShiftPlate, which is already the worked example. The skills read it, so it can't serve as a fair test.
- Run the checker on each output. Every miss it doesn't catch is a candidate for a new check in `check_workbook.py`, plus a test.
- The worked example is `examples/shiftplate.md`. Every number in it was checked against its source on 2026-10-16. Recheck prices before each release, since they change; Mealime's shutdown on 21 Oct 2026 will date that example.

## Step 10 — Write a README that gets installs and stars

Most popular skill repos use this order:

1. **One-line hook + badges** (stars, license, version, "Claude Code plugin").
2. **Why this exists**: one short paragraph. Generic AI product ideas skip the hard parts (evidence, sizing, competition), and this repo enforces them.
3. **Install in 30 seconds**, one block per agent:
   ```bash
   # Claude Code
   /plugin marketplace add <you>/product-idea-workbook
   /plugin install product-idea-workbook@product-idea

   # Codex, Cursor, Copilot, Gemini CLI, and 40+ other agents
   npx skills add <you>/product-idea-workbook
   ```
   For claude.ai users: download the skill zips from the latest GitHub Release (the release workflow attaches them) and upload each one under Settings → Skills.
4. **Try it now**: 3 copy-paste prompts, each for a different situation ("I have an idea", "I have a competitor to beat", "I need to size a market").
5. **See an example**: link to `examples/`, plus a short GIF of a run.
6. **The pipeline**: the diagram from the top of this file, and one line per skill.
7. **Contributing + license.**

## Step 11 — Publish and get discovered

```bash
gh repo create product-idea-workbook --public --source . --push
gh repo edit --add-topic claude-code,claude-skills,agent-skills,product-management,product-discovery
python3 scripts/release.py 0.1.0
git push origin main --follow-tags     # the release workflow publishes v0.1.0 with the zips
```

Then:
- Submit the repo to directories: Anthropic's plugin directory, skills.sh, and the "awesome-claude-skills" style lists (by PR).
- Post one example output, not just a link, where PMs gather (LinkedIn, r/ProductManagement, X). The example is what convinces people to try it.
- Ship small updates often with a short changelog. Repos that stay active keep getting stars.

## Step 12 — Keep improving it

After each real run, add any new mistake you caught as a gate, and add your
strongest demo runs to `examples/`. Open GitHub issues for skill requests
so users have an easy way to contribute.

---

### Research sources
- [anthropics/skills](https://github.com/anthropics/skills): the reference layout and the `/plugin marketplace add` install method
- [Claude Code: create a marketplace](https://code.claude.com/docs/en/plugin-marketplaces): `marketplace.json` and `plugin.json` rules, plus `claude plugin validate`
- [obra/superpowers](https://github.com/obra/superpowers): a single-repo plugin using `"source": "./"`
- [vercel-labs/skills](https://github.com/vercel-labs/skills): `npx skills add`, which finds `skills/<name>/SKILL.md` and plugin manifests
- [deanpeters/Product-Manager-Skills](https://github.com/deanpeters/Product-Manager-Skills): a popular PM skill repo with situation-based prompts, themed packs, Release zips, and a playground
