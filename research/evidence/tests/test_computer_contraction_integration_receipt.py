from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionIntegrationReceiptTests(unittest.TestCase):
    def test_receipt_binds_exact_merge_parents(self) -> None:
        doc = json.loads((ROOT / "evidence/computer-contraction-integration-receipt.json").read_text())
        merge = doc["mergeRevision"]
        parents = subprocess.check_output(["git", "-C", str(ROOT.parent), "show", "-s", "--format=%P", merge], text=True).strip().split()
        self.assertEqual(parents, doc["parents"])
        self.assertFalse(doc["distributionBoundary"]["sourceLanded"])
        self.assertFalse(doc["distributionBoundary"]["pushed"])

    def test_merge_retains_null_research_state(self) -> None:
        doc = json.loads((ROOT / "evidence/computer-contraction-integration-receipt.json").read_text())
        tree = doc["finalValidatedTreeAtMerge"]
        self.assertEqual(tree["experimentExecutableLikeFiles"], 0)
        self.assertEqual(tree["portfolioActiveIds"], [])
        self.assertEqual(tree["portfolioReadyIds"], [])
        self.assertEqual(tree["responsibilitySlots"], 10)


if __name__ == "__main__":
    unittest.main()
