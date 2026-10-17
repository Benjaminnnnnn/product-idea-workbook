#!/usr/bin/env python3
"""Check a Product Idea Workbook for structural problems.

Usage:
    python3 check_workbook.py workbooks/<product-slug>.md [--complete]

Checks the sections that are present. With --complete, every section must be
present. Prints one line per problem ("<file>:<line>: <message>") and exits
1 if any problem is found, or prints "OK" and exits 0.

Standard library only, so it runs anywhere Python 3.8+ runs.
"""
import re
import sys

# Section heading -> required "###" subsection headings, in order.
# tests/test_check_workbook.py verifies these match the skills' template.md files.
SECTIONS = {
    "Product Idea Brief": [],
    "1. Customer Problem Space": [
        "1. Fertile Land", "2. Customer", "3. Job To Be Done", "4. Outcomes",
        "5. Problem", "6. Customer Journey Map", "7. Use Cases",
        "8. Problem Sizing", "9. Problem Category", "10. Problem Statement",
        "Stage decision",
    ],
    "2. Market Space": [
        "1. Overall Market", "2. Total Addressable Market (TAM)",
        "3. Market Segmentation", "4. Target Market Profiles", "5. Competition",
        "6. Positioning Analysis", "7. Market Focus Decision", "Stage decision",
    ],
    "3. Solution Space": [
        "1. Product Concept Outline", "2. User Views",
        "3. Functional Requirements", "4. Context View",
        "5. Non-Functional Requirements", "Stage decision",
    ],
    "4. Customer Value Space": [
        "1. Product Features and Benefits",
        "2. Customer Value Proposition Strategy", "3. Pricing Model",
        "4. Customer Cost Items", "5. Customer Value Proposition Evaluation",
        "Stage decision",
    ],
    "Appendix — References": [],
}
STAGES = [s for s in SECTIONS if s[0].isdigit()]
APPENDIX = "Appendix — References"
# Subsections whose numbers must be cited or marked ASSUMPTION.
NEEDS_EVIDENCE = {
    "1. Customer Problem Space": ["8. Problem Sizing", "10. Problem Statement"],
    "2. Market Space": ["1. Overall Market"],
}

# "[...]" placeholders outside code fences. Skips links "[a](b)", checkboxes
# "[ ]"/"[x]", footnotes "[^1]", and numeric references like "[1]" or "[1, 2]".
PLACEHOLDER = re.compile(r"\[(?![ xX]?\]|\^|\d+(?:\s*,\s*\d+)*\])[^\]\n]+\](?!\()")
# Inside code fences (Mermaid, wireframes), only template leftovers are flagged.
FENCE_PLACEHOLDER = re.compile(r"\"\[[^\]\"\n]*\]\"|\bAXIS[12]\b|\bCompetitor [AB]\b")
# Many viewers (GitHub, VS Code, Obsidian) render "$...$" as LaTeX math, so currency must be "\$".
UNESCAPED_DOLLAR = re.compile(r"(?<!\\)\$")
INLINE_CODE = re.compile(r"`[^`]*`")
# Lines that may follow a "**Label**" line directly: lists, tables, headings, code fences.
LINE_STARTS_BLOCK = re.compile(r"\s*(?:[-*+]\s|\d+\.\s|\||#|```)")
STAGE_DECISION = re.compile(r"\*\*(PROCEED|PIVOT|STOP)\*\*")
BRIEF_DECISION = re.compile(r"\*\*Decision:\*\*\s*(GO|PIVOT|NO-GO)\b")
# "(Publisher, 2025)" or "(A, 2020; B et al., 2021)".
CITATION_GROUP = re.compile(r"\(([^()]*\b(?:19|20)\d{2}[a-z]?)\)")
CITATION = re.compile(r"^\s*([A-Z][^,;]*?),\s*(?:19|20)\d{2}[a-z]?\s*$")


def parse(lines):
    """Return {section: (start, end)} and {(section, sub): (start, end)} line ranges."""
    sections, subs = {}, {}
    current, sub = None, None
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        if line.startswith("## "):
            current, sub = line[3:].strip(), None
            sections[current] = [i, len(lines)]
        elif line.startswith("### ") and current:
            sub = line[4:].strip()
            subs[(current, sub)] = [i, len(lines)]
    # Close each range at the next heading of the same or higher level.
    starts = sorted(v[0] for v in sections.values())
    for rng in sections.values():
        later = [s for s in starts if s > rng[0]]
        rng[1] = later[0] if later else len(lines)
    for (sec, _), rng in subs.items():
        later = [v[0] for (s2, _), v in subs.items() if s2 == sec and v[0] > rng[0]]
        rng[1] = min(later + [sections[sec][1]])
    return sections, subs


def text(lines, rng):
    return "\n".join(lines[rng[0]:rng[1]])


def check(path, complete=False):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    problems = []

    def problem(line_index, message):
        problems.append(f"{path}:{line_index + 1}: {message}")

    if not lines or not (lines[0].startswith("# ") and "Product Idea Workbook" in lines[0]):
        problem(0, 'first line must be "# <Product> — Product Idea Workbook"')

    sections, subs = parse(lines)

    # Unknown, missing, and out-of-order sections.
    for name, (start, _) in sections.items():
        if name not in SECTIONS:
            problem(start, f'unknown section "## {name}" (expected one of: {", ".join(SECTIONS)})')
    present = [s for s in SECTIONS if s in sections]
    if [s for s in sorted(sections, key=lambda s: sections[s][0]) if s in SECTIONS] != present:
        problem(0, f"sections are out of order; expected: {', '.join(SECTIONS)}")
    if complete:
        for name in SECTIONS:
            if name not in sections:
                problem(0, f'missing section "## {name}"')

    # Required subsections inside each present section.
    for name in present:
        for sub in SECTIONS[name]:
            if (name, sub) not in subs:
                problem(sections[name][0], f'section "{name}" is missing "### {sub}"')

    # Placeholders left over from the templates.
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        pattern = FENCE_PLACEHOLDER if in_fence else PLACEHOLDER
        for m in pattern.finditer(line):
            problem(i, f"unfilled placeholder {m.group(0)}")

    # Markdown that renders wrong: "$" read as math, or a table or line glued to the line above it.
    in_fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if UNESCAPED_DOLLAR.search(INLINE_CODE.sub("", line)):
            problem(i, r"write dollar signs as \$, or text between two $ renders as math")
        prev = lines[i - 1].strip() if i else ""
        if not line.strip() or not prev or prev.startswith(("```", "#")):
            continue
        if line.lstrip().startswith("|") and not prev.startswith("|"):
            problem(i, "add a blank line before this table, or it renders as plain text")
        elif prev.startswith("*") and not prev.startswith("* ") and not LINE_STARTS_BLOCK.match(line):
            problem(i, "add a blank line before this line, or it joins the line above it")

    # Stage decisions.
    decisions = {}
    for stage in STAGES:
        rng = subs.get((stage, "Stage decision"))
        if not rng:
            continue
        m = STAGE_DECISION.search(text(lines, rng))
        if m:
            decisions[stage] = m.group(1)
        else:
            problem(rng[0], f'"{stage}" stage decision must be **PROCEED**, **PIVOT**, or **STOP**')

    # Brief decision must exist and follow from the stage decisions.
    if "Product Idea Brief" in sections:
        rng = sections["Product Idea Brief"]
        m = BRIEF_DECISION.search(text(lines, rng))
        if not m:
            problem(rng[0], "brief needs a line: **Decision:** GO | PIVOT | NO-GO")
        else:
            got = m.group(1)
            if "STOP" in decisions.values():
                expected = "NO-GO"
            elif "PIVOT" in decisions.values():
                expected = "PIVOT"
            elif len(decisions) == len(STAGES):
                expected = "GO"
            else:
                expected = None  # stages unfinished; GO isn't justified yet
            if expected and got != expected:
                problem(rng[0], f"brief decision is {got} but the stage decisions imply {expected}")
            if expected is None and got == "GO":
                problem(rng[0], "brief says GO but not every stage has a PROCEED decision")
        if "**Next step:**" not in text(lines, rng):
            problem(rng[0], "brief needs a line: **Next step:** <the single next action>")

    # TAM must be filled once pricing exists.
    tam = subs.get(("2. Market Space", "2. Total Addressable Market (TAM)"))
    if tam and "4. Customer Value Space" in sections and "pending" in text(lines, tam).lower():
        problem(tam[0], "TAM is still pending, but Customer Value Space exists; fill in 2.2")

    # Evidence-heavy subsections must cite a source or label assumptions.
    for sec, wanted in NEEDS_EVIDENCE.items():
        for sub in wanted:
            rng = subs.get((sec, sub))
            if rng and not (CITATION_GROUP.search(text(lines, rng)) or "ASSUMPTION" in text(lines, rng)):
                problem(rng[0], f'"{sub}" has no citation and no ASSUMPTION label')

    # Every inline citation needs an entry in the appendix.
    appendix = text(lines, sections[APPENDIX]) if APPENDIX in sections else ""
    appendix_start = sections[APPENDIX][0] if APPENDIX in sections else len(lines)
    in_fence = False
    for i, line in enumerate(lines[:appendix_start]):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        for group in CITATION_GROUP.finditer(line):
            for part in group.group(1).split(";"):
                m = CITATION.match(part)
                if not m:
                    continue
                key = re.split(r"[\s.]", m.group(1).strip())[0]
                if not appendix:
                    problem(i, f'citation "{part.strip()}" but no "## {APPENDIX}" section')
                elif key.lower() not in appendix.lower():
                    problem(i, f'citation "{part.strip()}" has no matching entry in the appendix')

    return problems


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1 or any(a not in ("--complete",) for a in argv if a.startswith("--")):
        print(__doc__.strip())
        return 2
    try:
        problems = check(args[0], complete="--complete" in argv)
    except OSError as e:
        print(f"cannot read {args[0]}: {e}")
        return 2
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problem(s) found. Fix them and run this check again.")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
