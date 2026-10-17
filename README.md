# Product Idea Workbook

Test a product idea before you build it. Agent skills for researching the problem, finding a market, and deciding whether to proceed.

[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-d97757)](#quick-start)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-287568)](https://github.com/vercel-labs/skills)
[![MIT](https://img.shields.io/badge/license-MIT-536174)](LICENSE)

[![Five steps from idea to decision: problem, market, solution, value, and a one-page brief. Review the evidence at each stage to proceed, pivot, or stop.](docs/workflow.svg)](examples/shiftplate.md)

## Quick start

In a **Claude Code** session:

```text
/plugin marketplace add Benjaminnnnnn/product-idea-workbook
/plugin install product-idea-workbook@product-idea
```

For **Codex, Cursor, Copilot, Gemini CLI**, or another supported agent, run this in your terminal (requires Node.js and npm). Select your agent and all skills:

```bash
npx skills add Benjaminnnnnn/product-idea-workbook
```

Then paste this into your agent:

```text
Use new-product-idea to evaluate a meal-planning app for US nurses working
12-hour shifts. Coach me through it, starting with whether the problem is real.
```

Coach mode pauses after each stage. Say “run on autopilot” to continue without questions. In Claude Code, you can also start with `/product-idea-workbook:new-product-idea`.

<details>
<summary>Install on claude.ai</summary>

Download skill ZIPs from [Releases](https://github.com/Benjaminnnnnn/product-idea-workbook/releases). Until the first release, build them locally with Python 3:

```bash
git clone https://github.com/Benjaminnnnnn/product-idea-workbook.git
cd product-idea-workbook
python3 scripts/build.py
```

Enable code execution, then upload each ZIP from `dist/` under **Customize → Skills → + → Create skill → Upload a skill**. Enable all skills for the full workflow. [Claude's setup guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

</details>

## How it works

Your agent follows four stages: problem → market → solution → value. It reviews the evidence after each one, then writes a one-page brief with a GO / NO-GO decision.

- **Evidence:** research numbers with web access; label anything unverified `ASSUMPTION`.
- **Competition:** compare direct competitors, indirect alternatives, and doing nothing.
- **Decisions:** proceed, pivot, or stop at each stage. A weak idea can end early.

You get `workbooks/<product-name>.md` with the research, sources, biggest risk, and next step. The included checker catches missing sections and references; customer validation still needs real people.

Use `market-space` on its own to size a market or compare competitors. [Browse all nine skills →](skills/)

## See the result

[Read the ShiftPlate workbook →](examples/shiftplate.md), a fictional meal planner for shift-working nurses. It includes customer journeys, positioning maps, pricing, and assumptions to test. Its next step is a two-week food diary with 15 nurses.

## Contributing

[Report a vague output or missing check](https://github.com/Benjaminnnnnn/product-idea-workbook/issues), or send a focused PR. Follow [AGENTS.md](AGENTS.md) and run:

```bash
python3 -m unittest discover -s tests
python3 scripts/build.py --check
```

[MIT license](LICENSE) · [Changelog](CHANGELOG.md)
