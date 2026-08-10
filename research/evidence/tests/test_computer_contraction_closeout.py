from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ComputerContractionCloseoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = json.loads((ROOT / "evidence/computer-contraction-implementation-closeout.json").read_text())

    def test_contraction_is_physical_not_only_a_shadow(self) -> None:
        self.assertTrue(self.doc["rsiInterpretation"]["selectiveSelfContractionNowPhysicallyImplemented"])
        self.assertGreater(self.doc["activeTree"]["c1PlusC5ArchivedLines"], 60_000)
        self.assertEqual(self.doc["activeTree"]["currentExperimentExecutableLikeFiles"], 0)

    def test_current_null_research_state_is_explicit(self) -> None:
        self.assertEqual(self.doc["activeTree"]["currentPortfolioActiveIds"], [])
        self.assertEqual(self.doc["activeTree"]["currentPortfolioReadyIds"], [])
        self.assertEqual(self.doc["responsibilityPrior"]["newSlots"], 10)

    def test_protocol_release_and_candidate_are_not_collapsed(self) -> None:
        protocol = self.doc["protocol"]
        self.assertEqual(protocol["released"], "0.3.0 immutable")
        self.assertEqual(protocol["currentCandidate"], "0.4.0.dev0 unreleased")
        self.assertFalse(protocol["automaticConsumerUpgrade"])

    def test_rsi_claim_remains_bounded(self) -> None:
        rsi = self.doc["rsiInterpretation"]
        self.assertTrue(rsi["boundedRecursiveSelfReformStillProven"])
        self.assertFalse(rsi["autonomousPressureSelectionProven"])
        self.assertFalse(rsi["openEndedRSIProven"])


if __name__ == "__main__":
    unittest.main()
