from __future__ import annotations

import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parents[1]
EVIDENCE = HERE / "evidence" / "p2-live-acceptance.json"


class LiveEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(EVIDENCE.read_text())

    def test_projection_only_agent_actions_passed(self) -> None:
        self.assertEqual(self.document["agentEvaluation"]["passRate"], 1.0)
        self.assertEqual(self.document["agentEvaluation"]["passed"], self.document["agentEvaluation"]["total"])

    def test_private_backing_reuse_is_real_without_shared_mutable_target(self) -> None:
        build = self.document["buildReuse"]
        self.assertGreater(build["rustHits"], 0)
        self.assertTrue(build["binaryDigestsEqual"])
        self.assertTrue(build["privateBackingIsolationPreserved"])
        self.assertFalse(self.document["decisions"]["sharedMutableCargoTarget"])

    def test_temporary_equipment_left_no_active_lease_or_package_authority(self) -> None:
        equipment = self.document["temporaryEquipment"]
        self.assertEqual(equipment["currentLeaseState"], "absent")
        self.assertTrue(equipment["releaseReplayConverged"])
        self.assertTrue(equipment["packageAuthorityStayedPacman"])
        self.assertFalse(self.document["decisions"]["temporaryEquipmentPackageManager"])

    def test_event_driven_evidence_did_not_earn_a_daemon(self) -> None:
        targeted = self.document["targetedReobservation"]
        self.assertGreater(targeted["runtimeTargetedVsFullMedianSpeedup"], 1)
        self.assertGreater(targeted["workstationTargetedVsFullMedianSpeedup"], 1)
        self.assertFalse(targeted["newMaintenanceDaemonEarned"])
        self.assertFalse(self.document["decisions"]["globalMaintenanceDaemon"])

    def test_projection_never_gained_release_authority(self) -> None:
        self.assertFalse(self.document["decisions"]["centralMaintenanceAuthority"])
        self.assertFalse(self.document["decisions"]["projectionCanPublishOrDeploy"])


if __name__ == "__main__":
    unittest.main()
