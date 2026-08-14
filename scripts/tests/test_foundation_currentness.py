from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest

import sys

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from foundation_currentness import relation  # noqa: E402


class FoundationCurrentnessTests(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path, str, str]:
        temp = tempfile.TemporaryDirectory()
        repo = Path(temp.name)
        subprocess.run(["git", "init", "-q", "-b", "main", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "test"], check=True)
        (repo / "value.txt").write_text("one\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "add", "value.txt"], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "one"], check=True)
        first = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        (repo / "value.txt").write_text("two\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(repo), "commit", "-qam", "two"], check=True)
        second = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        return temp, repo, first, second

    def test_exact(self) -> None:
        temp, repo, _, second = self._repo()
        with temp:
            self.assertEqual(relation(repo, second, second), {"state": "exact", "ahead": 0, "behind": 0})

    def test_left_behind(self) -> None:
        temp, repo, first, second = self._repo()
        with temp:
            self.assertEqual(relation(repo, first, second), {"state": "left_behind", "ahead": 0, "behind": 1})

    def test_left_ahead(self) -> None:
        temp, repo, first, second = self._repo()
        with temp:
            self.assertEqual(relation(repo, second, first), {"state": "left_ahead", "ahead": 1, "behind": 0})


if __name__ == "__main__":
    unittest.main()
