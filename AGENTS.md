# AGENTS.md

Instructions for AI coding agents (and people) working in this repository.

## Before you commit

```bash
python3 -m unittest discover -s tests     # all tests pass
python3 scripts/build.py --check          # generated example.md files are current
```

After editing `examples/shiftplate.md`, run `python3 scripts/build.py` to regenerate each skill's `example.md`. Never edit the generated files directly.

## Commit messages: Conventional Commits

Every commit follows [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<scope>): <description>

[optional body: what changed and why]

[optional footer(s)]
```

**Types**

| Type | Use for |
|---|---|
| `feat` | A new skill, or new behavior in a skill |
| `fix` | A bug fix in a skill, template, script, or the checker |
| `docs` | README, `steps.md`, `AGENTS.md`, or comments only |
| `test` | Adding or changing tests or eval cases |
| `refactor` | A code or wording change that doesn't change behavior |
| `ci` | GitHub Actions workflows |
| `build` | `scripts/build.py`, packaging, or the zips |
| `chore` | Maintenance, including releases (`chore(release): v0.2.0`) |
| `revert` | Reverting an earlier commit |

**Scopes**: a skill name (`market-space`, `stage-review`, ...), or `templates`, `checker`, `example`, `evals`, `release`, `plugin`. Leave out the scope when a change spans several areas.

**Rules**
- The description is in the imperative mood ("add", not "added"), lowercase, with no trailing period, and the whole subject line is at most 72 characters.
- Put one logical change in each commit.
- In the body, explain *why* the change was made. The diff already shows what changed.
- For a breaking change (a renamed skill, a changed workbook format, or a removed template field), add `!` after the type or scope and a `BREAKING CHANGE:` footer describing the migration.

**Examples**

```
feat(market-research): require the date checked for competitor prices
fix(templates): add blank lines so tables and label lines render
docs: add install steps for Cursor
chore(release): v0.2.0
feat(checker)!: require an Appendix section in every workbook

BREAKING CHANGE: workbooks without "## Appendix — References" now fail the check.
```

## Releases

Don't edit the version by hand. Add notes under `## [Unreleased]` in `CHANGELOG.md`, then run `python3 scripts/release.py <version>`. It creates the `chore(release): v<version>` commit and the tag.
