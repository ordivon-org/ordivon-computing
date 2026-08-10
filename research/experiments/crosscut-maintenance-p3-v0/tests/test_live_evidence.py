from __future__ import annotations

import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1]
EVIDENCE = HERE / "evidence" / "p3-live-acceptance.json"


class LiveEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(EVIDENCE.read_text())

    def test_agent_adversarial_holdout_has_zero_boundary_failures(self) -> None:
        holdout = self.document["agentHoldout"]
        self.assertEqual(holdout["passed"], 32)
        self.assertEqual(holdout["passRate"], 1.0)
        self.assertTrue(all(float(value) == 0.0 for value in holdout["metrics"].values()))

    def test_legacy_ablation_reproduces_stale_projection_failure(self) -> None:
        legacy = self.document["legacyAblation"]
        self.assertLess(legacy["passRate"], 1.0)
        self.assertEqual(legacy["metrics"]["staleTrustRate"], 1.0)
        self.assertGreater(legacy["metrics"]["overActionRate"], 0.0)

    def test_real_owner_events_prevented_nonzero_stale_windows(self) -> None:
        transitions = self.document["liveStaleTransitions"]
        self.assertGreater(transitions["beforeAcquireStaleWindowPreventedMs"], 0)
        self.assertGreater(transitions["beforeReleaseStaleWindowPreventedMs"], 0)
        self.assertFalse(transitions["leaseLeftActive"])

    def test_topic_similarity_does_not_authorize_temporary_equipment(self) -> None:
        boundary = self.document["temporaryEquipmentAmbiguity"]
        self.assertFalse(boundary["explicitOwnerNeedProved"])
        self.assertFalse(boundary["automaticLeaseAcquisitionAllowed"])
        self.assertFalse(boundary["automaticPackageRemovalAllowed"])

    def test_temporal_projection_did_not_become_a_new_authority(self) -> None:
        decisions = self.document["decisions"]
        self.assertTrue(decisions["ownerEventsAreInvalidationHintsOnly"])
        self.assertFalse(decisions["centralEventStore"])
        self.assertFalse(decisions["globalFreshnessTtl"])
        self.assertFalse(decisions["maintenanceDaemon"])
        self.assertFalse(decisions["crosscutEffectAuthority"])
        self.assertFalse(decisions["immutableEvidenceAgesOutByWallClock"])


if __name__ == "__main__":
    unittest.main()
