#!/usr/bin/env python3
"""Build generated files and release assets. Standard library only.

    python3 scripts/build.py                  regenerate examples and build one all-skills ZIP in dist/
    python3 scripts/build.py --check          fail if any generated example.md is out of date (CI)
    python3 scripts/build.py notes 0.2.0      print the CHANGELOG section for a version
    python3 scripts/build.py verify-tag v0.2.0  fail unless the tag matches plugin.json's version
"""
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "shiftplate.md"
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
APPENDIX = "## Appendix — References"
# Workbook section -> the skill whose example.md shows it.
SECTION_SKILL = {
    "## Product Idea Brief": "product-idea-brief",
    "## 1. Customer Problem Space": "customer-problem-space",
    "## 2. Market Space": "market-space",
    "## 3. Solution Space": "solution-space",
    "## 4. Customer Value Space": "customer-value-space",
}
HEADER = """<!-- Generated from examples/shiftplate.md by scripts/build.py. Edit that file, then run: python3 scripts/build.py -->
# Worked example: ShiftPlate (fictional product)

This shows the depth and evidence standard to match. Don't copy its content or numbers; research the user's own product.

"""


def split_sections(markdown):
    """Return {"## Heading": text} for each top-level section (headings inside code fences ignored)."""
    sections, current, in_fence = {}, None, False
    for line in markdown.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            current = line.strip()
            sections[current] = ""
        if current:
            sections[current] += line
    return sections


def generated_examples():
    sections = split_sections(EXAMPLE.read_text(encoding="utf-8"))
    out = {}
    for heading, skill in SECTION_SKILL.items():
        body = sections[heading].rstrip() + "\n\n" + sections[APPENDIX].rstrip() + "\n"
        out[SKILLS / skill / "example.md"] = HEADER + body
    return out


def build_zip():
    """One versioned ZIP with every skill folder at the root. Byte-for-byte reproducible."""
    DIST.mkdir(exist_ok=True)
    for old in DIST.glob("*.zip"):
        old.unlink()
    archive = DIST / f"product-idea-workbook-{plugin_version()}.zip"
    files = [ROOT / "LICENSE"]
    for skill in sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()):
        files.extend(f for f in sorted(skill.rglob("*"))
                     if f.is_file() and "__pycache__" not in f.parts
                     and f.suffix not in (".pyc", ".pyo") and f.name != ".DS_Store")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            name = f.name if f == ROOT / "LICENSE" else f.relative_to(SKILLS).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.external_attr = (0o755 if f.suffix == ".py" else 0o644) << 16
            z.writestr(info, f.read_bytes(), zipfile.ZIP_DEFLATED)
    return archive


def plugin_version():
    return json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())["version"]


def changelog_notes(version):
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(rf"^## \[{re.escape(version)}\][^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m or not m.group(1).strip():
        sys.exit(f"CHANGELOG.md has no notes for {version}")
    return m.group(1).strip()


def main(argv):
    if argv[:1] == ["notes"] and len(argv) == 2:
        print(changelog_notes(argv[1]))
        return 0
    if argv[:1] == ["verify-tag"] and len(argv) == 2:
        if argv[1] != f"v{plugin_version()}":
            print(f"tag {argv[1]} does not match plugin.json version {plugin_version()}")
            return 1
        print(f"tag {argv[1]} matches plugin.json")
        return 0
    if argv == ["--check"]:
        stale = [p for p, body in generated_examples().items()
                 if not p.exists() or p.read_text(encoding="utf-8") != body]
        for p in stale:
            print(f"out of date: {p.relative_to(ROOT)}")
        if stale:
            print("Run: python3 scripts/build.py")
            return 1
        print("OK: generated files are up to date")
        return 0
    if argv:
        print(__doc__.strip())
        return 2
    for path, body in generated_examples().items():
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"built {build_zip().relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
