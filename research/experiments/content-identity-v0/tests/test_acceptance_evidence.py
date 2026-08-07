from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from content_identity import ContentIdentity, require_same_content  # noqa: E402


class AcceptanceEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        path = ROOT / "evidence" / "a1-content-identity-acceptance.json"
        cls.receipt = json.loads(path.read_text(encoding="utf-8"))

    def test_retained_five_owner_evidence_projects_to_shared_identity(self) -> None:
        owners = self.receipt["owners"]
        records = {owner: owners[owner]["record"] for owner in ("runtime", "finance", "security", "studio", "world")}
        projected = require_same_content(records)
        self.assertEqual(projected, ContentIdentity.from_dict(self.receipt["sharedIdentity"]))
        self.assertEqual(projected.digest, self.receipt["payload"]["digest"])
        self.assertEqual(projected.byte_length, self.receipt["payload"]["byteLength"])

    def test_evidence_proves_media_type_is_owner_descriptor_not_content_identity(self) -> None:
        owners = self.receipt["owners"]
        media_types = {
            owners["finance"]["record"]["mediaType"],
            owners["security"]["record"]["mediaType"],
            owners["studio"]["record"]["mediaType"],
            owners["world"]["record"]["media_type"],
        }
        self.assertGreater(len(media_types), 1)
        self.assertNotIn("mediaType", self.receipt["sharedIdentity"])
        self.assertTrue(self.receipt["checks"]["mediaTypeExcludedFromIdentity"])

    def test_crosscut_evidence_retains_no_payload_and_no_new_authority(self) -> None:
        self.assertFalse(self.receipt["payload"]["payloadBytesRetained"])
        self.assertTrue(self.receipt["checks"]["payloadBytesNotCopiedToCrosscutEvidence"])
        self.assertFalse(self.receipt["checks"]["newWritableAuthorityCreated"])
        self.assertFalse(self.receipt["checks"]["newServiceCreated"])
        self.assertFalse(self.receipt["checks"]["newRepositoryCreated"])
        self.assertFalse(self.receipt["disposition"]["promoteToOrdivonProtocolNow"])

    def test_world_contract_digest_is_bound(self) -> None:
        digest = self.receipt["owners"]["world"]["schemaDigest"]
        self.assertRegex(digest, r"^sha256:[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
