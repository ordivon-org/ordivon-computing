from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OwnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads((ROOT / "evidence" / "owner-temporal-contracts.json").read_text())
        cls.owners = {row["owner"]: row for row in cls.doc["owners"]}

    def test_five_materially_different_owners_are_evidenced(self):
        self.assertEqual(set(self.owners), {"ordivon-host", "workstation", "ordivon-world", "ordivon-runtime", "ordivon-computing"})
        self.assertFalse(self.doc["universalAdapterEarned"])
        self.assertTrue(all(not row["genericTemporalAdapterRequired"] for row in self.owners.values()))

    def test_host_uses_revision_fence_not_ttl(self):
        host = self.owners["ordivon-host"]
        self.assertIn("action-time-revision-fenced", host["contractClass"])
        self.assertEqual(host["focusedAcceptance"]["passed"], 25)
        self.assertEqual(host["liveStaleFence"]["result"], "REVISION_CONFLICT")
        self.assertEqual(host["liveStaleFence"]["commitState"], "not_committed")

    def test_workstation_combines_age_binding_and_revalidation(self):
        workstation = self.owners["workstation"]
        self.assertEqual(workstation["focusedAcceptance"]["passed"], 24)
        self.assertTrue({"owner-bounded-dynamic", "identity-bound", "action-time-revalidated"} <= set(workstation["contractClass"]))

    def test_world_deleted_the_p4_era_carrier_but_kept_current_temporal_distinction(self):
        world = self.owners["ordivon-world"]
        self.assertEqual(world["focusedAcceptance"]["passed"], 4)
        self.assertEqual(world["ownerSurvivalAcceptance"]["pythonTests"], 121)
        self.assertFalse(world["historicalComputingReferenceIsProductionConsumer"])
        self.assertIn("src/ordivon_world/foreign_egress.py", world["deletedP4EraCarriers"])
        self.assertIn("src/ordivon_world/effect_paths.py", world["deletedP4EraCarriers"])

    def test_runtime_release_result_status_does_not_equal_world_change(self):
        runtime = self.owners["ordivon-runtime"]
        window = runtime["releaseWindow"]
        self.assertEqual(window["firstEffect"]["status"], "not_committed")
        self.assertFalse(window["firstEffect"]["serviceWasStopped"])
        self.assertNotEqual(window["observedAfterFirstEffect"]["sourceRevision"], window["observedAfterFirstEffect"]["activeRevision"])
        self.assertEqual(window["secondEffect"]["status"], "deployed")
        self.assertEqual(window["finalSourceActive"], runtime["revision"])


if __name__ == "__main__":
    unittest.main()
