from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "evidence" / "p5-live-acceptance.json").read_text())

    def test_court_has_no_inconclusive_feature(self):
        court = self.doc["featureCourt"]
        self.assertGreaterEqual(court["rows"], 30)
        self.assertEqual(court["verdictCounts"].get("inconclusive", 0), 0)
        self.assertFalse(court["universalTemporalAdapterEarned"])

    def test_real_contraction_survived(self):
        row = self.doc["contraction"]
        self.assertEqual(row["removedFamilies"], 5)
        self.assertEqual(row["removedFiles"], 87)
        self.assertEqual(row["removedLines"], 10722)
        self.assertEqual(row["gitRecoveryFamiliesVerified"], 5)
        self.assertTrue(row["fullComputingGatePassed"])
        self.assertEqual(row["existenceGauntletPassed"], 28)

    def test_promotion_boundary_is_contracted(self):
        decision = self.doc["promotionDecision"]
        self.assertTrue(decision["sharedTemporalSemanticLaw"])
        self.assertFalse(decision["sharedTemporalImplementation"])
        self.assertFalse(decision["centralEventBroker"])
        self.assertFalse(decision["globalFreshnessTtl"])
        self.assertFalse(decision["globalTimeOntology"])
        self.assertFalse(decision["p0ToP4ExecutableApparatusActive"])
        self.assertTrue(decision["ownerNativeContractsPreferred"])
        self.assertTrue(decision["gitHistoryIsArchive"])
        self.assertFalse(decision["coreEditRequired"])

    def test_runtime_is_currently_source_active_converged(self):
        runtime = self.doc["runtime"]
        self.assertEqual(runtime["status"], "healthy")
        self.assertEqual(runtime["sourceRevision"], runtime["activeRevision"])
        self.assertEqual(runtime["recoveryRequired"], 0)


if __name__ == "__main__":
    unittest.main()
