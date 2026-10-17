# Changelog

All notable changes to this project are listed here. Add new entries under
"Unreleased"; `python3 scripts/release.py <version>` moves them into a dated
section.

## [Unreleased]

### Added
- A README with installation instructions, three starter prompts, a worked-example checker GIF, and a guide to the skill pipeline.
- The Product Idea Workbook pipeline: `new-product-idea` (coach or autopilot), `customer-problem-space`, `market-space`, `solution-space`, `customer-value-space`, `product-idea-brief`.
- `market-research` (cited numbers) and `stage-review` (skeptical review before each decision).
- A worked example for a fictional product (`examples/shiftplate.md`), shown in each skill's `example.md`.
- `check_workbook.py`, a standard-library checker that catches missing sections, leftover placeholders, missing decisions, and citations without references.
- A Claude Code plugin marketplace, `npx skills` support, and per-skill zips for claude.ai.
