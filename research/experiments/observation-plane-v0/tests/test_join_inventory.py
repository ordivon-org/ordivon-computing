from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "join-key-inventory-v1.json"


class ObservationJoinInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(INVENTORY.read_text(encoding="utf-8"))

    def test_identity_integrity_and_owner_revisions(self) -> None:
        self.assertEqual(self.value["inventoryId"], "OBS-JOIN-001")
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
        for revision in self.value["ownerRevisions"].values():
            self.assertEqual(len(revision), 40)
            int(revision, 16)

    def test_typed_key_extraction_is_closed_and_content_free(self) -> None:
        policy = self.value["policy"]["typedPayloadKeyExtraction"]
        self.assertTrue(policy["authorized"])
        self.assertEqual(policy["purpose"], "stable_foreign_identity_only")
        self.assertIn("raw_payload_not_copied", policy["requirements"])
        self.assertIn("prompt", policy["forbidden"])
        self.assertIn("stdout", policy["forbidden"])
        self.assertIn("correlationContext", policy["forbidden"])

    def test_cross_owner_join_paths_are_available(self) -> None:
        paths = {item["pathId"]: item for item in self.value["joinPaths"]}
        self.assertEqual(paths["host-task-to-harness-run"]["status"], "available")
        self.assertEqual(
            paths["harness-tool-step-to-runtime-job"]["status"],
            "available_via_typed_key_extraction",
        )
        self.assertEqual(paths["runtime-request-backlink"]["status"], "available")
        self.assertEqual(
            self.value["disposition"],
            "sufficient_for_run_once_exporters_and_future_b3",
        )


if __name__ == "__main__":
    unittest.main()
