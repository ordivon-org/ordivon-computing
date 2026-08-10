from __future__ import annotations

import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
EVIDENCE = HERE / "evidence" / "p1-live-acceptance.json"


class LiveEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_no_unearned_global_promotion(self) -> None:
        decisions = self.document["decisions"]
        self.assertFalse(decisions["defaultSccacheForRuntime"])
        self.assertFalse(decisions["sharedMutableCargoTarget"])
        self.assertFalse(decisions["automaticDirtyDeletion"])
        self.assertFalse(decisions["newHourlyLifecycleTimer"])
        self.assertFalse(decisions["centralCrossOwnerPolicy"])
        self.assertFalse(decisions["sharedLifecycleProductionPackage"])
        self.assertFalse(decisions["newCrosscutRepository"])

    def test_owner_health_and_conformance_are_explicit(self) -> None:
        self.assertEqual(self.document["computingConformance"]["status"], "passed")
        self.assertEqual(self.document["worldDoctor"]["status"], "ok")
        self.assertIn(self.document["workstationDoctor"]["status"], {"ok", "warn", "fail"})

    def test_dirty_review_proved_non_mutation(self) -> None:
        dirty = self.document["dirtyReview"]
        self.assertFalse(dirty["automaticDeletionAllowed"])
        self.assertFalse(dirty["workspaceMutationObserved"])
        self.assertEqual(dirty["sourceStateDigestBefore"], dirty["sourceStateDigestAfter"])

    def test_sccache_same_path_helped_but_cross_target_did_not(self) -> None:
        evidence = self.document["sccache"]
        self.assertEqual(evidence["differentTargetPaths"]["rustHits"], 0)
        self.assertEqual(evidence["normalizedDifferentTargetPaths"]["rustHits"], 0)
        self.assertGreater(evidence["sameTargetPathRebuild"]["cumulativeRustHits"][-1], 0)
        self.assertFalse(evidence["runtimeDefaultIntegrationEarned"])


if __name__ == "__main__":
    unittest.main()
