from __future__ import annotations

import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1]
EVIDENCE = HERE / "evidence"


class LiveAblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.live = json.loads((EVIDENCE / "live-event-ablation.json").read_text())
        cls.world = json.loads((EVIDENCE / "world-temporal-consumer.json").read_text())

    def test_real_noop_publish_eliminates_key_only_false_positive_reobserve(self):
        row = self.live["realNoOpPublish"]
        self.assertFalse(row["ownerStateChanged"])
        self.assertGreater(row["p3UnnecessaryReobservations"], 0)
        self.assertEqual(row["p4UnnecessaryReobservations"], 0)
        self.assertGreater(row["p3WorkloadFalsePositiveRate"], 0)
        self.assertEqual(row["p4WorkloadFalsePositiveRate"], 0.0)

    def test_owner_scoping_removes_cross_owner_invalidations(self):
        row = self.live["ownerScopeCounterfactualChangedPublish"]
        self.assertEqual(row["p4ReobserveSignals"], row["expectedReobserveSignals"])
        self.assertGreater(row["p3FalsePositiveReobservations"], 0)
        self.assertEqual(row["p4FalsePositiveReobservations"], 0)

    def test_real_runtime_revision_change_invalidates_old_build_applicability(self):
        build = self.live["stableBuildEvidence"]
        self.assertNotEqual(build["boundIdentity"], build["currentIdentity"])
        self.assertEqual(build["validity"]["freshnessState"], "binding_changed")
        release = self.live["runtimeRelease"]
        self.assertEqual(release["historicalP3SnapshotValidityAtRelease"]["freshnessState"], "invalidated")

    def test_sparse_events_are_acceleration_not_completeness(self):
        conclusion = self.live["sparseEvents"]["conclusion"]
        self.assertFalse(conclusion["eventsEliminateStaleness"])
        self.assertTrue(conclusion["eventsAccelerateInvalidation"])
        self.assertTrue(conclusion["ownerFreshnessBoundStillNeededWhenActionableWithoutEvent"])

    def test_world_is_independent_second_consumer_but_not_shared_code_contract(self):
        test = self.world["focusedOwnerNativeTest"]
        self.assertEqual(test["passed"], 22)
        self.assertEqual(test["failed"], 0)
        laws = self.world["independentTemporalLaws"]
        self.assertTrue(all(laws.values()))
        difference = self.world["implementationDifference"]
        self.assertFalse(difference["worldUsesEventInvalidationOverlay"])
        self.assertFalse(difference["exactSharedCodeContractEarned"])
        self.assertTrue(difference["sharedSemanticInvariantSupported"])


if __name__ == "__main__":
    unittest.main()
