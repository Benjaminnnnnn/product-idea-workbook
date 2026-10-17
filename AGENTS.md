# AGENTS.md

## Before committing
- `python3 -m unittest discover -s tests` and `python3 scripts/build.py --check` must pass.
- Edit `examples/shiftplate.md`, then run `python3 scripts/build.py`. Never edit the generated `skills/*/example.md` files.
- Never bump versions by hand: add notes under `## [Unreleased]` in `CHANGELOG.md`, then run `python3 scripts/release.py <version>`.

## Commits: Conventional Commits 1.0.0
- Format: `<type>(<scope>): <description>`. Imperative, lowercase, no period, at most 72 characters. The body explains why. One logical change per commit.
- Types: `feat` `fix` `docs` `test` `refactor` `ci` `build` `chore` `revert`.
- Optional scopes: a skill name, or `templates` `checker` `example` `evals` `release` `plugin`.
- Breaking changes (a renamed skill, a changed workbook format) take `!` and a `BREAKING CHANGE:` footer, e.g. `feat(checker)!: …`.
