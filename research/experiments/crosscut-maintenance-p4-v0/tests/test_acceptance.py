from __future__ import annotations

import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1]
ACCEPTANCE = HERE / "evidence" / "p4-live-acceptance.json"


class AcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(ACCEPTANCE.read_text())

    def test_false_positive_invalidation_is_removed(self):
        noop = self.document["realNoOpPublish"]
        self.assertEqual(noop["p3UnnecessaryReobservations"], 4)
        self.assertEqual(noop["p4UnnecessaryReobservations"], 0)
        owner = self.document["ownerScope"]
        self.assertEqual(owner["p3FalsePositiveReobservations"], 3)
        self.assertEqual(owner["p4FalsePositiveReobservations"], 0)

    def test_real_cost_reduction_is_nonzero(self):
        costs = self.document["reobservationBenchmark"]["counterfactualCosts"]
        self.assertGreater(costs["p3KeyOnlyNoOpPublishMs"], 0)
        self.assertEqual(costs["p4OwnerScopedNoChangePublishMs"], 0.0)
        self.assertGreater(costs["p4ChangedPublishAvoidedMs"], 0)

    def test_runtime_revision_change_blocks_old_immutable_evidence(self):
        self.assertEqual(self.document["runtime"]["stableBuildEvidenceState"], "binding_changed")

    def test_second_consumer_supports_law_not_shared_package(self):
        world = self.document["worldSecondConsumer"]
        self.assertEqual(world["focusedTestsPassed"], 22)
        self.assertTrue(world["sharedSemanticInvariantSupported"])
        self.assertFalse(world["exactSharedCodeContractEarned"])

    def test_promotion_boundary_remains_thin(self):
        decision = self.document["promotionDecision"]
        self.assertTrue(decision["sharedTemporalSemanticLaw"])
        self.assertFalse(decision["sharedTemporalPackage"])
        self.assertFalse(decision["centralEventBroker"])
        self.assertFalse(decision["globalFreshnessTtl"])
        self.assertEqual(decision["invalidationIdentity"], "owner+key")
        self.assertTrue(decision["eventOccurrenceAndAvailabilitySeparated"])
        self.assertTrue(decision["eventsAreAccelerationNotCompleteness"])
        self.assertFalse(decision["noChangeResultInvalidates"])
        self.assertFalse(decision["exactReplayCreatesNewInvalidation"])
        self.assertFalse(decision["crossClockOrderingAssumed"])


if __name__ == "__main__":
    unittest.main()
