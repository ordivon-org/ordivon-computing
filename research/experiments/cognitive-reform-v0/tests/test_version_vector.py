from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VECTOR = ROOT / "system-version-vector-v1.json"


class SystemVersionVectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.vector = json.loads(VECTOR.read_text(encoding="utf-8"))

    def test_identity_and_integrity(self) -> None:
        self.assertEqual(self.vector["schemaVersion"], 1)
        self.assertEqual(self.vector["kind"], "ordivon.system-version-vector")
        payload = dict(self.vector)
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

    def test_selected_revisions_are_exact(self) -> None:
        repositories = self.vector["repositories"]
        for name in ("computing", "protocol", "host", "harness", "runtime"):
            revision = repositories[name]["revision"]
            self.assertEqual(len(revision), 40, name)
            int(revision, 16)
        self.assertEqual(
            repositories["harness"]["hostPin"], repositories["host"]["revision"]
        )
        self.assertEqual(
            repositories["harness"]["protocolPin"],
            repositories["protocol"]["revision"],
        )

    def test_release_is_reproducible_but_not_production(self) -> None:
        gates = self.vector["gates"]
        self.assertTrue(gates["allSelectedRevisionsRemoteReachable"])
        self.assertTrue(gates["harnessCleanInstallUsesRemoteHostPin"])
        self.assertTrue(gates["crossRepositoryLiveJourneyPassed"])
        self.assertTrue(gates["runtimeRealSystemAcceptancePassed"])
        self.assertFalse(gates["productionActivated"])
        self.assertTrue(gates["stagingRehearsalRequired"])

    def test_every_owner_has_passed_acceptance(self) -> None:
        acceptance = self.vector["acceptance"]
        self.assertEqual(set(acceptance), {"host", "harness", "computing", "runtime"})
        for owner, value in acceptance.items():
            self.assertEqual(value["status"], "passed", owner)
        self.assertEqual(acceptance["harness"]["scale"]["events"], 100_000)
        self.assertEqual(acceptance["runtime"]["systemCheckCount"], 74)


if __name__ == "__main__":
    unittest.main()
