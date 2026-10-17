"""Repository checks. Run: python3 -m unittest discover -s tests -v

Standard library only. These run in CI on every push, and in scripts/release.py.
"""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EXAMPLE = ROOT / "examples" / "shiftplate.md"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = load("check_workbook", SKILLS / "new-product-idea" / "scripts" / "check_workbook.py")
sys.path.insert(0, str(ROOT / "scripts"))
build = load("build", ROOT / "scripts" / "build.py")


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert m, f"{path} has no frontmatter"
    return dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M))


class CheckerTest(unittest.TestCase):
    def run_checker(self, text, complete=True):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(text)
        try:
            return checker.check(f.name, complete=complete)
        finally:
            Path(f.name).unlink()

    def assert_problem(self, text, fragment, complete=True):
        problems = self.run_checker(text, complete)
        self.assertTrue(any(fragment in p for p in problems),
                        f"expected a problem containing {fragment!r}, got: {problems}")

    def setUp(self):
        self.example = EXAMPLE.read_text(encoding="utf-8")

    def test_worked_example_passes(self):
        self.assertEqual(self.run_checker(self.example), [])

    def test_leftover_placeholder(self):
        self.assert_problem(self.example.replace("Shift-work nutrition gap", "[2–4 word label]"),
                            "unfilled placeholder")

    def test_leftover_placeholder_in_diagram(self):
        self.assert_problem(self.example.replace('nurse(["Nurse"])', 'nurse(["[Customer]"])'),
                            "unfilled placeholder")

    def test_missing_stage_decision(self):
        self.assert_problem(self.example.replace("**PROCEED**: the MVP", "Looks good: the MVP"),
                            "stage decision must be")

    def test_brief_decision_must_follow_stages(self):
        text = self.example.replace("**PROCEED**: the MVP", "**PIVOT**: the MVP")
        self.assert_problem(text, "imply PIVOT")

    def test_citation_without_reference(self):
        self.assert_problem(self.example.replace("(Mealime, 2026), and", "(Gartner, 2025), and"),
                            "no matching entry in the appendix")

    def test_pending_tam_after_pricing(self):
        text = self.example.replace(r"**\$43.2M per year:** 899,618", "*Pending pricing; 899,618")
        self.assert_problem(text, "TAM is still pending")

    def test_sizing_needs_evidence(self):
        start = self.example.index("### 8. Problem Sizing")
        end = self.example.index("### 9. Problem Category")
        text = self.example[:start] + "### 8. Problem Sizing\n- About $1B a year.\n\n" + self.example[end:]
        self.assert_problem(text, "no citation and no ASSUMPTION")

    def test_table_glued_to_text(self):
        self.assert_problem(self.example.replace("**Direct**\n\n|", "**Direct**\n|"),
                            "blank line before this table")

    def test_label_lines_glued_together(self):
        self.assert_problem(self.example.replace("before building.\n\n**Next step:**", "before building.\n**Next step:**"),
                            "joins the line above")

    def test_unescaped_dollar(self):
        self.assert_problem(self.example.replace(r"\$47.99/year", "$47.99/year", 1), "dollar signs")

    def test_missing_subsection(self):
        self.assert_problem(self.example.replace("### 4. Context View", "### Context"),
                            'missing "### 4. Context View"')

    def test_sections_out_of_order(self):
        a = self.example.index("## 3. Solution Space")
        b = self.example.index("## 4. Customer Value Space")
        c = self.example.index("## Appendix — References")
        text = self.example[:a] + self.example[b:c] + self.example[a:b] + self.example[c:]
        self.assert_problem(text, "out of order")

    def test_partial_workbook_passes_until_complete(self):
        start = self.example.index("## 1. Customer Problem Space")
        end = self.example.index("## 2. Market Space")
        appendix = self.example.index("## Appendix — References")
        title = self.example.splitlines()[0] + "\n\n"
        partial = title + self.example[start:end] + self.example[appendix:]
        self.assertEqual(self.run_checker(partial, complete=False), [])
        self.assert_problem(partial, 'missing section "## 2. Market Space"', complete=True)


class TemplatesMatchCheckerTest(unittest.TestCase):
    def test_unfilled_templates_are_flagged(self):
        for template in sorted(SKILLS.glob("*/template.md")):
            with self.subTest(template=template.parent.name):
                problems = checker.check(str(template))
                self.assertTrue(any("unfilled placeholder" in p for p in problems))

    def test_template_headings_match_checker(self):
        for template in sorted(SKILLS.glob("*/template.md")):
            text = template.read_text(encoding="utf-8")
            section = re.search(r"^## (.+)$", text, re.M).group(1).strip()
            subs = [s.strip() for s in re.findall(r"^### (.+)$", text, re.M)]
            with self.subTest(template=str(template.relative_to(ROOT))):
                self.assertIn(section, checker.SECTIONS)
                self.assertEqual(subs, checker.SECTIONS[section])


class SkillsTest(unittest.TestCase):
    def skill_dirs(self):
        return sorted(p for p in SKILLS.iterdir() if p.is_dir())

    def test_every_skill_is_valid(self):
        for skill in self.skill_dirs():
            path = skill / "SKILL.md"
            with self.subTest(skill=skill.name):
                self.assertTrue(path.exists(), "missing SKILL.md")
                meta = frontmatter(path)
                self.assertEqual(meta.get("name"), skill.name)
                self.assertRegex(skill.name, r"^[a-z0-9-]{1,64}$")
                self.assertNotRegex(skill.name, r"claude|anthropic")
                description = meta.get("description", "")
                self.assertTrue(description.startswith("Use when"), "description must start with 'Use when'")
                self.assertLessEqual(len(description), 1024)
                self.assertNotRegex(description, r"[<>]")
                self.assertLess(len(path.read_text(encoding="utf-8").splitlines()), 500)

    def test_referenced_files_exist(self):
        for skill in self.skill_dirs():
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            for name in ("template.md", "example.md", "scripts/check_workbook.py"):
                if f"`{name}`" in text or f"{name}`" in text:
                    with self.subTest(skill=skill.name, file=name):
                        self.assertTrue((skill / name).exists(), f"{skill.name}/SKILL.md mentions {name}")

    def test_skills_with_templates_have_examples(self):
        for template in SKILLS.glob("*/template.md"):
            with self.subTest(skill=template.parent.name):
                self.assertTrue((template.parent / "example.md").exists())

    def test_generated_examples_are_current(self):
        for path, body in build.generated_examples().items():
            with self.subTest(file=str(path.relative_to(ROOT))):
                self.assertEqual(path.read_text(encoding="utf-8"), body,
                                 "out of date; run: python3 scripts/build.py")


release = load("release", ROOT / "scripts" / "release.py")


class ReleaseVersionTest(unittest.TestCase):
    def test_strict_semver(self):
        self.assertEqual(release.parse("1.20.3"), (1, 20, 3))
        self.assertEqual(release.parse("0.0.0"), (0, 0, 0))
        for bad in ("01.2.3", "1.02.3", "1.2.03", "1.2", "1.2.3-beta.1", "v1.2.3"):
            with self.subTest(version=bad):
                self.assertIsNone(release.parse(bad))

    def test_bump_of(self):
        self.assertEqual(release.bump_of((0, 1, 0), (0, 1, 1)), "patch")
        self.assertEqual(release.bump_of((0, 1, 5), (0, 2, 0)), "minor")
        self.assertEqual(release.bump_of((0, 9, 0), (1, 0, 0)), "major")

    def test_required_bump(self):
        fix = ["fix(checker): handle empty files"]
        feat = fix + ["feat(market-space): add a pricing table"]
        bang = fix + ["feat(checker)!: require an appendix"]
        footer = fix + ["refactor: rename templates\n\nBREAKING CHANGE: template paths changed"]
        self.assertEqual(release.required_bump(fix, (1, 0, 0)), "patch")
        self.assertEqual(release.required_bump(feat, (1, 0, 0)), "minor")
        self.assertEqual(release.required_bump(bang, (1, 0, 0)), "major")
        self.assertEqual(release.required_bump(footer, (1, 0, 0)), "major")
        # Before 1.0.0, breaking changes need only a minor bump.
        self.assertEqual(release.required_bump(bang, (0, 3, 0)), "minor")


class BundleTest(unittest.TestCase):
    def test_bundle_contains_all_skill_files_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(build, "DIST", Path(tmp)):
            (Path(tmp) / "old-skill.zip").write_bytes(b"old archive")
            archive = build.build_zip()
            self.assertEqual(archive.name, f"product-idea-workbook-{build.plugin_version()}.zip")
            self.assertEqual(list(Path(tmp).glob("*.zip")), [archive])
            expected = {p.relative_to(SKILLS).as_posix(): p.read_bytes()
                        for skill in SKILLS.iterdir() if (skill / "SKILL.md").is_file()
                        for p in skill.rglob("*") if p.is_file()
                        and "__pycache__" not in p.parts
                        and p.suffix not in (".pyc", ".pyo") and p.name != ".DS_Store"}
            expected["LICENSE"] = (ROOT / "LICENSE").read_bytes()
            with zipfile.ZipFile(archive) as z:
                self.assertEqual(set(z.namelist()), set(expected))
                self.assertIsNone(z.testzip())
                for name, content in expected.items():
                    self.assertEqual(z.read(name), content)
                info = z.getinfo("new-product-idea/scripts/check_workbook.py")
                self.assertEqual(info.external_attr >> 16, 0o755)
            original = archive.read_bytes()
            self.assertEqual(build.build_zip().read_bytes(), original)


class ManifestTest(unittest.TestCase):
    def test_plugin_and_marketplace_agree(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
        self.assertRegex(plugin["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual([p["name"] for p in market["plugins"]], [plugin["name"]])
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_changelog_has_unreleased_section(self):
        self.assertIn("## [Unreleased]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
