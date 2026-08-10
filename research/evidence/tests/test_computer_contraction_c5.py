from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionC5Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = json.loads((ROOT / "evidence/computer-contraction-c5-closeout.json").read_text())

    def test_no_executable_research_surface_remains_without_active_work(self) -> None:
        portfolio = json.loads((ROOT / "portfolio.json").read_text())
        self.assertFalse([q for q in portfolio["questions"] if q["status"] in {"active", "ready"}])
        executable = []
        for path in (ROOT / "experiments").rglob("*"):
            if path.is_file() and (path.suffix in {".py", ".sh", ".rs", ".ts"} or any(part in {"tests", "scripts", "src", "integration", "fixtures", "benchmarks"} for part in path.parts)):
                executable.append(path)
        self.assertEqual(executable, [])

    def test_v1_authority_is_absent_current_but_git_recoverable(self) -> None:
        authority = self.doc["responsibilityAuthority"]
        self.assertFalse((ROOT / "computer-responsibility-map-v1.json").exists())
        revision = self.doc["baseRevision"]
        old_map = subprocess.check_output(["git", "-C", str(ROOT.parent), "rev-parse", f"{revision}:{authority['oldMapPath']}"], text=True).strip()
        old_checker = subprocess.check_output(["git", "-C", str(ROOT.parent), "rev-parse", f"{revision}:scripts/check_computer_responsibility_map.py"], text=True).strip()
        self.assertEqual(old_map, authority["oldMapGitBlob"])
        self.assertEqual(old_checker, authority["oldCheckerGitBlob"])

    def test_v2_has_only_surviving_current_responsibilities(self) -> None:
        authority = self.doc["responsibilityAuthority"]
        current = json.loads((ROOT / "computer-responsibility-map-v2.json").read_text())
        self.assertEqual({item["id"] for item in current["responsibilities"]}, set(authority["activeIds"]))
        retired = set().union(*[set(values) for values in authority["retired"].values()])
        self.assertFalse(retired.intersection(authority["activeIds"]))
        self.assertLess(authority["surfaceRatio"], 0.5)

    def test_archived_executables_are_git_recoverable(self) -> None:
        archive = json.loads((ROOT / "evidence/computer-contraction-c5-final-apparatus-archive.json").read_text())
        revision = archive["sourceRevision"]
        self.assertEqual(archive["removedFiles"], 49)
        for item in archive["files"]:
            self.assertFalse((ROOT.parent / item["path"]).exists())
            actual = subprocess.check_output(["git", "-C", str(ROOT.parent), "rev-parse", f"{revision}:{item['path']}"], text=True).strip()
            self.assertEqual(actual, item["gitBlob"])


if __name__ == "__main__":
    unittest.main()
