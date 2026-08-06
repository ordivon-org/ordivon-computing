from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "owner-exporter-closeout-v1.json"


class OwnerExporterCloseoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(CLOSEOUT.read_text(encoding="utf-8"))

    def test_identity_integrity_and_status(self) -> None:
        self.assertEqual(self.value["closeoutId"], "OBS-B2-M2-001")
        self.assertEqual(self.value["status"], "completed_b3_ready")
        payload = dict(self.value)
        integrity = payload.pop("integrity")
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        self.assertEqual(
            integrity["payloadDigest"],
            "sha256:" + hashlib.sha256(encoded).hexdigest(),
        )
        self.assertFalse(self.value["formalTrialUnlocked"])
        self.assertEqual(self.value["nextWorkPackage"], "B3")

    def test_three_exact_owner_exporters_are_closed(self) -> None:
        owners = self.value["owners"]
        self.assertEqual(set(owners), {"B2-H", "B2-A", "B2-R"})
        for package in owners.values():
            for field in (
                "selectedOwnerRevision",
                "implementationRevision",
                "receiptRevision",
            ):
                revision = package[field]
                self.assertEqual(len(revision), 40)
                int(revision, 16)
            self.assertEqual(package["tests"]["targeted"], 3)
        self.assertEqual(owners["B2-H"]["tests"]["ownerUnit"], 180)
        self.assertEqual(owners["B2-A"]["tests"]["ownerUnit"], 350)
        self.assertEqual(owners["B2-R"]["tests"]["transactionalCore"], 110)

    def test_authority_and_artifact_boundary_remain_bounded(self) -> None:
        acceptance = self.value["commonAcceptance"]
        self.assertFalse(acceptance["ownerDatabaseWrites"])
        self.assertFalse(acceptance["rawPrivateContentExported"])
        self.assertFalse(acceptance["productionActivated"])
        self.assertFalse(acceptance["daemonAdded"])
        artifact = self.value["runtimeArtifactDisposition"]
        self.assertEqual(artifact["status"], "deferred_to_B3_design_decision")
        self.assertIn("append-only Artifact observation", artifact["requiredDecision"])


if __name__ == "__main__":
    unittest.main()
