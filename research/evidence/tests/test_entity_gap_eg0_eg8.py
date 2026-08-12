from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

RESEARCH = Path(__file__).resolve().parents[2]
EXP = RESEARCH / "experiments" / "entity-gap-eg0-eg8-v0"
RESULTS = EXP / "results"


def load(name: str):
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


class EntityGapCurrentEvidence(unittest.TestCase):
    def test_phase_apparatus_is_contracted_but_git_bound(self):
        archive = json.loads((EXP / "apparatus-archive-v0.json").read_text(encoding="utf-8"))
        self.assertEqual(archive["snapshotRevision"], "d9cd4f53764e8ef164cdd48f919d19701fe0d5e7")
        for item in archive["apparatus"]:
            self.assertFalse((RESEARCH.parent / item["path"]).exists(), item["path"])
            self.assertTrue(item["sha256"].startswith("sha256:"))

    def test_core_falsifiers_survive_contraction(self):
        eg1 = load("eg1-formal-verifier-result.json")
        eg2 = load("eg2-optimizer-result.json")
        eg3 = load("eg3-estimator-result.json")
        eg7 = load("eg7-archivist-indexer-result.json")
        eg8 = load("eg8-entity-dispositions.json")
        self.assertEqual((eg1["boundedExampleMutantsDetected"], eg1["exactEnumerationMutantsDetected"]), (1, 12))
        self.assertEqual((eg2["minimumResourceCount"], eg2["minimumSolutionCount"]), (7, 6))
        self.assertTrue(eg3["intervalsOverlap"])
        self.assertAlmostEqual(eg7["expectedSourceHitRateTop10"], 4/6)
        self.assertEqual(eg8["promotedSharedServices"], [])
        self.assertEqual(eg8["promotedSharedProtocols"], [])

    def test_run_receipt_still_binds_retained_result_bytes(self):
        receipt = load("run-receipt.json")
        for name, expected in receipt["resultDigests"].items():
            actual = "sha256:" + hashlib.sha256((RESULTS / name).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, name)


if __name__ == "__main__":
    unittest.main()
