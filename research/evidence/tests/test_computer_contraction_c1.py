from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionC1Tests(unittest.TestCase):
    def test_archive_manifest_is_current_and_historical_apparatus_absent(self) -> None:
        doc = json.loads((ROOT / "evidence/computer-contraction-c1-active-tree-archive.json").read_text())
        self.assertEqual(doc["archiveId"], "COMPUTER-CONTRACTION-C1")
        self.assertEqual(doc["removedFiles"], 296)
        self.assertGreater(doc["removedLines"], 50_000)
        for item in doc["files"]:
            self.assertFalse((ROOT.parent / item["path"]).exists(), item["path"])

    def test_current_freshness_utility_is_extracted(self) -> None:
        doc = json.loads((ROOT / "evidence/computer-contraction-c1-active-tree-archive.json").read_text())
        utility = ROOT.parent / doc["extractedLiveUtility"]["currentPath"]
        self.assertTrue(utility.is_file())

    def test_gate_does_not_reintroduce_archived_families(self) -> None:
        gate = (ROOT.parent / "scripts/ordivon_conformance.py").read_text()
        for family in (
            "semantic-core-v0",
            "task-continuation-v0",
            "harness-evaluation-v0",
            "experiment-loop-v0",
            "crosscut-maintenance-p0-v0",
            "crosscut-maintenance-p1-v0",
            "crosscut-maintenance-p2-v0",
            "crosscut-maintenance-p3-v0",
        ):
            self.assertNotIn(family, gate)


if __name__ == "__main__":
    unittest.main()
