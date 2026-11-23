# ruff: noqa: INP001, PT009 -- Standard-library unittest; no test package required.
import unittest
from pathlib import Path
from runpy import run_path

is_valid_branch = run_path(str(Path(__file__).resolve().parents[1] / "scripts/check_branch.py"))[
    "is_valid_branch"
]


class BranchTests(unittest.TestCase):
    def test_valid_branches(self):
        for branch in (
            "codex/chore/project-identity",
            "codex/feat/sample-screener",
            "codex/fix/bug-2",
        ):
            with self.subTest(branch=branch):
                self.assertTrue(is_valid_branch(branch))

    def test_invalid_branches(self):
        for branch in (
            "main",
            "feat/screener",
            "codex/unknown/screener",
            "codex/feat/",
            "codex/feat/Uppercase",
            "codex/feat/under_score",
            "codex/feat/-start",
            "codex/feat/end-",
            "codex/feat/two--hyphens",
            "codex/feat/nested/path",
            "codex/feat/name.lock",
            "codex/feat/name\n",
            "codex/feat/$(echo unsafe)",
        ):
            with self.subTest(branch=branch):
                self.assertFalse(is_valid_branch(branch))
