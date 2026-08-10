from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionFinalIntegrationTests(unittest.TestCase):
    def test_receipt_binds_latest_source_parent(self) -> None:
        doc = json.loads((ROOT / "evidence/computer-contraction-final-integration-receipt.json").read_text())
        parents = subprocess.check_output(["git", "-C", str(ROOT.parent), "show", "-s", "--format=%P", doc["mergeRevision"]], text=True).strip().split()
        self.assertEqual(parents, doc["parents"])
        self.assertEqual(doc["latestSourceRevision"], doc["parents"][1])

    def test_taste_priors_remain_evidence_only(self) -> None:
        doc = json.loads((ROOT / "evidence/computer-contraction-final-integration-receipt.json").read_text())
        taste = doc["tastePriorAssimilation"]
        self.assertEqual(taste["executableFiles"], 0)
        self.assertEqual(taste["newResponsibilitySlots"], 0)
        self.assertEqual(taste["portfolioActiveIds"], [])
        self.assertIn("prospective calibration", taste["promotionBoundary"].lower())


if __name__ == "__main__":
    unittest.main()
