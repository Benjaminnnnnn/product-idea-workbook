"""Exercise releases in disposable Git repositories without publishing anything."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        for name in ("scripts", "skills", "examples", ".claude-plugin"):
            shutil.copytree(ROOT / name, self.repo / name,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for name in ("CHANGELOG.md", "LICENSE", ".gitignore"):
            shutil.copy2(ROOT / name, self.repo / name)
        (self.repo / "tests").mkdir()
        # Run the real repository checks inside the fixture, without recursively running these tests.
        shutil.copy2(ROOT / "tests" / "test_repo.py", self.repo / "tests" / "test_repo.py")
        current = json.loads((self.repo / ".claude-plugin/plugin.json").read_text())["version"]
        major, minor, _ = map(int, current.split("."))
        self.version = f"{major}.{minor + 1}.0"
        self.git("init", "-b", "release-test")
        self.git("config", "user.name", "Release Test")
        self.git("config", "user.email", "release@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "tag.gpgsign", "false")
        self.commit()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True,
                              capture_output=True, text=True).stdout.strip()

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-m", "feat(release): prepare fixture")

    def release(self):
        return subprocess.run([sys.executable, "scripts/release.py", self.version],
                              cwd=self.repo, capture_output=True, text=True)

    def assert_stopped_cleanly(self, result, reason):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(reason, result.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("tag", "--list"), "")

    def test_release_builds_one_bundle_and_tags_the_release_commit(self):
        result = self.release()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.git("log", "-1", "--format=%s"), f"chore(release): v{self.version}")
        self.assertEqual(self.git("rev-parse", f"v{self.version}^{{commit}}"),
                         self.git("rev-parse", "HEAD"))
        self.assertEqual([p.name for p in (self.repo / "dist").glob("*.zip")],
                         [f"product-idea-workbook-{self.version}.zip"])
        self.assertIn(f"git push --atomic origin refs/heads/release-test refs/tags/v{self.version}",
                      result.stdout)
        self.assertIn(f"## [{self.version}] - ", (self.repo / "CHANGELOG.md").read_text())

    def test_empty_unreleased_does_not_reuse_previous_release_notes(self):
        (self.repo / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [Unreleased]\n\n## [0.0.0]\n\n- Old release notes.\n")
        self.commit()
        self.assert_stopped_cleanly(self.release(), "add your changes")

    def test_detached_head_is_rejected(self):
        self.git("checkout", "--detach")
        self.assert_stopped_cleanly(self.release(), "HEAD is detached")

    def test_failed_checks_restore_version_and_changelog(self):
        (self.repo / "tests/test_failure.py").write_text(
            "import unittest\nclass Failure(unittest.TestCase):\n"
            "    def test_failure(self):\n        self.fail('release check failed')\n")
        self.commit()
        self.assert_stopped_cleanly(self.release(), "release check failed")

    def test_failed_build_restores_version_and_changelog(self):
        (self.repo / "dist").write_text("Blocks creation of the output directory")
        self.commit()
        self.assert_stopped_cleanly(self.release(), "checks or build failed")
