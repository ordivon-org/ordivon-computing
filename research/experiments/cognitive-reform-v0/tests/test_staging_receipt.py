from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "evidence" / "a4-staging-rehearsal-f6173b2.json"


class A4StagingReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    def test_identity_and_integrity(self) -> None:
        self.assertEqual(
            self.receipt["kind"],
            "ordivon.cognitive-reform-a4-staging-rehearsal",
        )
        payload = dict(self.receipt)
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
        self.assertEqual(
            self.receipt["rehearsalImplementationRevision"],
            "f6173b2c327c232a70b272cc947dc98bb857ae2a",
        )

    def test_staging_is_clean_and_production_is_untouched(self) -> None:
        staging = self.receipt["staging"]
        self.assertFalse(staging["productionActivated"])
        self.assertTrue(staging["productionRootsUnchanged"])
        self.assertEqual(
            staging["productionRootsObservedBefore"],
            staging["productionRootsObservedAfter"],
        )
        self.assertTrue(self.receipt["cleanup"]["requested"])
        self.assertTrue(self.receipt["cleanup"]["completed"])

    def test_both_rollback_boundaries_are_proved(self) -> None:
        allowed = self.receipt["rollbackAllowed"]
        self.assertTrue(allowed["initialCanActivate"])
        self.assertTrue(allowed["legacyWriterRejectedWhileActive"])
        self.assertEqual(allowed["receiptChainLength"], 2)
        self.assertEqual(allowed["finalMode"], "legacy_host")

        fenced = self.receipt["rollbackFenced"]
        self.assertTrue(fenced["rollbackRejected"])
        self.assertEqual(fenced["finalMode"], "independent")
        self.assertEqual(
            fenced["rollbackErrorClass"],
            "post_activation_independent_work",
        )
        self.assertTrue(fenced["hostDoctorHealthy"])
        self.assertTrue(fenced["harnessDoctorHealthy"])

    def test_receipt_matches_release_vector(self) -> None:
        vector = json.loads((ROOT / "system-version-vector-v1.json").read_text())
        self.assertEqual(self.receipt["vectorId"], vector["vectorId"])
        self.assertEqual(
            self.receipt["vectorPayloadDigest"],
            vector["integrity"]["payloadDigest"],
        )
        self.assertEqual(
            self.receipt["revisions"]["harness"],
            vector["repositories"]["harness"]["revision"],
        )
        self.assertEqual(
            self.receipt["revisions"]["host"],
            vector["repositories"]["host"]["revision"],
        )


if __name__ == "__main__":
    unittest.main()
