from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def load(name: str):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


class EntityGapAcceptance(unittest.TestCase):
    def test_eg1_exact_verifier_beats_bounded_examples(self):
        d = load("eg1-formal-verifier-result.json")
        self.assertFalse(d["currentAdmission"])
        self.assertEqual(d["stateSpace"], 4096)
        self.assertEqual(d["boundedExampleMutantsDetected"], 1)
        self.assertEqual(d["exactEnumerationMutantsDetected"], 12)
        self.assertEqual(d["baselineUnsafeAdmissionCounts"]["full"], 0)
        self.assertEqual(d["baselineUnsafeAdmissionCounts"]["local-only"], 511)

    def test_eg2_optimizer_certifies_but_does_not_choose_value(self):
        d = load("eg2-optimizer-result.json")
        self.assertEqual(d["minimumResourceCount"], 7)
        self.assertEqual(d["minimumSolutionCount"], 6)
        self.assertTrue(d["greedy"]["coversAllP0"])
        self.assertTrue(d["greedy"]["certifiedMinimum"])
        self.assertGreater(d["paretoFrontierBudget1to4Count"], 1)

    def test_eg3_small_n_point_rates_are_not_overstated(self):
        d = load("eg3-estimator-result.json")
        self.assertTrue(d["intervalsOverlap"])
        self.assertLess(d["rawTopChoiceStability"]["wilson95"][0], 0.6)
        self.assertGreater(d["negativeControlTopChoice"]["wilson95"][1], 0.25)
        self.assertLess(d["negativeControlDeferral"]["wilson95"][0], 0.75)

    def test_eg4_separates_observation_from_cognition(self):
        d = load("eg4-sensor-outcome-audit.json")
        blocking = [r for r in d["rows"] if r["gapType"]]
        self.assertGreaterEqual(len(blocking), 5)
        self.assertTrue(any("physical-resource" in r["gapType"] for r in blocking))
        self.assertTrue(any("external-observation" in r["gapType"] for r in blocking))
        self.assertEqual(d["sharedService"], "reject")

    def test_eg5_keeps_simulators_domain_local(self):
        d = load("eg5-simulator-adversary-audit.json")
        self.assertEqual(set(d["domains"]), {"finance", "security", "game"})
        self.assertEqual(d["sharedSimulatorService"], "reject")

    def test_eg6_human_is_scoped_sensor_not_gate(self):
        d = load("eg6-human-response-sensor-audit.json")
        self.assertEqual(d["universalApprovalGate"], "reject")
        self.assertEqual(d["sharedProtocolPromotion"], "defer")
        self.assertTrue(any(x["humanRequired"] for x in d["claims"]))
        self.assertTrue(any(not x["humanRequired"] for x in d["claims"]))

    def test_eg7_generic_index_does_not_earn_archivist(self):
        d = load("eg7-archivist-indexer-result.json")
        self.assertFalse(d["temporaryIndexRetained"])
        self.assertAlmostEqual(d["expectedSourceHitRateTop10"], 4/6)
        self.assertAlmostEqual(d["ownerScopedExpectedSourceHitRateTop10"], 4/6)
        self.assertIn("defer-dedicated-archivist", d["disposition"])

    def test_eg8_promotes_roles_not_shared_control_planes(self):
        d = load("eg8-entity-dispositions.json")
        self.assertEqual(d["promotedSharedServices"], [])
        self.assertEqual(d["promotedSharedProtocols"], [])
        by_entity = {x["entity"]: x for x in d["items"]}
        self.assertEqual(by_entity["formal verifier/constraint checker"]["disposition"], "retain-role-localize-owner")
        self.assertEqual(by_entity["statistical estimator/calibrator"]["disposition"], "retain-role-high-priority")
        self.assertEqual(by_entity["archivist/indexer"]["disposition"], "defer-dedicated-role")

    def test_run_receipt_binds_all_results(self):
        receipt = load("run-receipt.json")
        self.assertFalse(receipt["temporaryExternalStateRetained"])
        self.assertNotIn("run-receipt.json", receipt["resultFiles"])
        for name, expected in receipt["resultDigests"].items():
            actual = "sha256:" + hashlib.sha256((RESULTS / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)


if __name__ == "__main__":
    unittest.main()
