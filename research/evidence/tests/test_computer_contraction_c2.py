from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionC2Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = json.loads((ROOT / "evidence/computer-contraction-c2-content.json").read_text())

    def test_removed_content_packages_are_absent_but_git_recoverable(self) -> None:
        revision = self.doc["baseRevision"]
        for item in self.doc["removedGitObjects"]:
            self.assertFalse((ROOT.parent / item["path"]).exists())
            actual = subprocess.check_output(["git", "-C", str(ROOT.parent), "rev-parse", f"{revision}:{item['path']}"], text=True).strip()
            self.assertEqual(actual, item["gitObject"])

    def test_shared_source_tree_consumer_contract_survives(self) -> None:
        after = self.doc["after"]
        self.assertEqual(after["humanConsumer"]["checkedDocuments"], 8)
        self.assertEqual(after["humanConsumer"]["blockingFailures"], 0)
        self.assertEqual(after["humanConsumer"]["exitCode"], 0)
        self.assertLess(after["currentLines"], self.doc["before"]["trackedLines"] // 3)

    def test_baseline_command_surface_is_removed(self) -> None:
        cli = (ROOT.parent / "packages/content-cli/src/ordivon_content/cli.py").read_text()
        self.assertNotIn("command_baseline", cli)
        self.assertNotIn("build_baseline", cli)


if __name__ == "__main__":
    unittest.main()
