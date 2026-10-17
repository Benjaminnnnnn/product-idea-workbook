#!/usr/bin/env python3
"""Cut a release in one command.

    python3 scripts/release.py 0.2.0

1. Checks that the working tree is clean and CHANGELOG.md has notes under "## [Unreleased]".
   The version must be strict SemVer (MAJOR.MINOR.PATCH, no leading zeros) and at
   least the bump the Conventional Commits since the last tag require:
   breaking -> major (minor while < 1.0.0), feat -> minor, anything else -> patch.
2. Sets the version in .claude-plugin/plugin.json and dates the CHANGELOG section.
3. Runs the tests and the generated-file check, and stops if either fails.
4. Commits "chore(release): v0.2.0" (Conventional Commits, see AGENTS.md) and creates tag v0.2.0.

Then push with: git push origin main --follow-tags
The tag starts .github/workflows/release.yml, which publishes the GitHub Release.
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
CHANGELOG = ROOT / "CHANGELOG.md"
SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
BUMPS = ["patch", "minor", "major"]


def parse(version):
    m = SEMVER.fullmatch(version)
    return tuple(int(x) for x in m.groups()) if m else None


def bump_of(current, new):
    """The kind of bump from current to new: "major", "minor", or "patch"."""
    if new[0] > current[0]:
        return "major"
    if new[1] > current[1]:
        return "minor"
    return "patch"


def required_bump(messages, current):
    """The smallest bump the Conventional Commit messages since the last release allow."""
    breaking = any(re.match(r"\w+(\([^)]*\))?!:", m) or re.search(r"^BREAKING[ -]CHANGE:", m, re.M)
                   for m in messages)
    if breaking:
        return "major" if current[0] >= 1 else "minor"  # SemVer: anything may change before 1.0.0
    if any(re.match(r"feat(\([^)]*\))?:", m) for m in messages):
        return "minor"
    return "patch"


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def fail(message):
    sys.exit(f"release stopped: {message}")


def main(argv):
    if len(argv) != 1:
        sys.exit(__doc__.strip())
    version = argv[0]
    tag = f"v{version}"
    if not parse(version):
        fail(f"{version} is not a SemVer version (MAJOR.MINOR.PATCH, no leading zeros)")

    if run("git", "status", "--porcelain").strip():
        fail("working tree has uncommitted changes")
    if run("git", "tag", "--list", tag).strip():
        fail(f"tag {tag} already exists")

    plugin = PLUGIN.read_text(encoding="utf-8")
    current = re.search(r'"version"\s*:\s*"([^"]+)"', plugin).group(1)
    if parse(version) <= parse(current):
        fail(f"{version} is not newer than the current version {current}")

    last_tag = run("git", "tag", "--list", "v*", "--sort=-v:refname").split()
    since = f"{last_tag[0]}..HEAD" if last_tag else "HEAD"
    messages = [m.strip() for m in run("git", "log", "--format=%B%x1e", since).split("\x1e") if m.strip()]
    needed = required_bump(messages, parse(current))
    got = bump_of(parse(current), parse(version))
    if BUMPS.index(got) < BUMPS.index(needed):
        fail(f"commits since {last_tag[0] if last_tag else 'the first commit'} need at least a {needed} "
             f"bump, but {current} -> {version} is a {got} bump")

    changelog = CHANGELOG.read_text(encoding="utf-8")
    m = re.search(r"^## \[Unreleased\]\s*\n(.*?)(?=^## |\Z)", changelog, re.M | re.S)
    if not m or not m.group(1).strip():
        fail('add your changes under "## [Unreleased]" in CHANGELOG.md first')

    PLUGIN.write_text(plugin.replace(f'"version": "{current}"', f'"version": "{version}"', 1), encoding="utf-8")
    today = datetime.date.today().isoformat()
    CHANGELOG.write_text(
        changelog.replace("## [Unreleased]", f"## [Unreleased]\n\n## [{version}] - {today}", 1),
        encoding="utf-8")

    try:
        run(sys.executable, "-m", "unittest", "discover", "-s", "tests")
        run(sys.executable, "scripts/build.py", "--check")
    except subprocess.CalledProcessError as e:
        run("git", "checkout", "--", str(PLUGIN), str(CHANGELOG))
        fail(f"checks failed, version not changed:\n{e.stdout}{e.stderr}")

    run("git", "add", str(PLUGIN), str(CHANGELOG))
    run("git", "commit", "-m", f"chore(release): {tag}")
    run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    print(f"Released {tag} locally. Publish it with:\n  git push origin main --follow-tags")


if __name__ == "__main__":
    main(sys.argv[1:])
