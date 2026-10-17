# Changelog

All notable changes to this project are listed here. Add new entries under
"Unreleased"; `python3 scripts/release.py <version>` moves them into a dated
section.

## [Unreleased]

### Changed
- Default to autopilot when no mode is specified; request coach mode to pause for input after each stage.
- Separate README installation instructions by agent, link to released skill ZIPs, and add coach and autopilot examples.

## [0.1.0] - 2026-10-16

### Changed
- Recommend installing the GitHub marketplace directly in claude.ai or Claude Desktop on paid plans, with manual skill uploads as a fallback.

### Removed
- The internal `steps.md` planning document and the README checker GIF.

### Added
- A concise README with installation commands, a starter prompt, and an illustrated workflow.
- The Product Idea Workbook pipeline: `new-product-idea` (coach or autopilot), `customer-problem-space`, `market-space`, `solution-space`, `customer-value-space`, `product-idea-brief`.
- `market-research` (cited numbers) and `stage-review` (skeptical review before each decision).
- A worked example for a fictional product (`examples/shiftplate.md`), shown in each skill's `example.md`.
- `check_workbook.py`, a standard-library checker that catches missing sections, leftover placeholders, missing decisions, and citations without references.
- A Claude Code plugin marketplace, `npx skills` support, and per-skill zips for claude.ai.
- `idea-screen`: a cheap pass that scores 1–5 ideas on problem, market, gap, and willingness to pay, so the full workbook runs only on the winner.
- A research and turn budget: at most 8 researched numbers per stage, searches batched in one turn, and no reading PDFs or saved fetch files. The full-run eval now fails above 60 turns.
