#!/usr/bin/env python3
"""Cut a release in one command.

    python3 scripts/release.py 0.2.0

1. Checks that the working tree is clean and CHANGELOG.md has notes under "## [Unreleased]".
2. Sets the version in .claude-plugin/plugin.json and dates the CHANGELOG section.
3. Runs the tests and the generated-file check, and stops if either fails.
4. Commits "Release v0.2.0" and creates tag v0.2.0.

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


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def fail(message):
    sys.exit(f"release stopped: {message}")


def main(argv):
    if len(argv) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", argv[0]):
        sys.exit(__doc__.strip())
    version = argv[0]
    tag = f"v{version}"

    if run("git", "status", "--porcelain").strip():
        fail("working tree has uncommitted changes")
    if run("git", "tag", "--list", tag).strip():
        fail(f"tag {tag} already exists")

    plugin = PLUGIN.read_text(encoding="utf-8")
    current = re.search(r'"version"\s*:\s*"([^"]+)"', plugin).group(1)
    as_tuple = lambda v: tuple(int(x) for x in v.split("."))
    if as_tuple(version) <= as_tuple(current):
        fail(f"{version} is not newer than the current version {current}")

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
    run("git", "commit", "-m", f"Release {tag}")
    run("git", "tag", "-a", tag, "-m", f"Release {tag}")
    print(f"Released {tag} locally. Publish it with:\n  git push origin main --follow-tags")


if __name__ == "__main__":
    main(sys.argv[1:])
