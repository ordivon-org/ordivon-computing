from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from content_identity import (  # noqa: E402
    ContentIdentity,
    ContentIdentityError,
    from_finance_evidence,
    project_owner_content,
    require_same_content,
)


PAYLOAD = b"ordivon-a1-content-identity-v0\n"
HEX = hashlib.sha256(PAYLOAD).hexdigest()
DIGEST = "sha256:" + HEX
LENGTH = len(PAYLOAD)


def owner_records() -> dict[str, dict[str, object]]:
    return {
        "runtime": {
            "artifactId": "attempt-a1.stdout",
            "digest": DIGEST,
            "retainedBytes": LENGTH,
            "droppedBytes": 9,
            "truncated": True,
        },
        "finance": {
            "evidenceRef": "evidence://sha256/" + HEX,
            "digest": HEX,
            "algorithm": "sha256",
            "byteLength": LENGTH,
            "mediaType": "application/x-finance-test",
            "storageClass": "local-content-addressed",
        },
        "security": {
            "sampleId": "sample:" + HEX,
            "sha256": DIGEST,
            "byteLength": LENGTH,
            "mediaType": "application/x-security-test",
            "originalName": "sample.bin",
        },
        "studio": {
            "digest": DIGEST,
            "sizeBytes": LENGTH,
            "mediaType": "application/octet-stream",
            "rights": {"status": "owned"},
        },
        "world": {
            "key": "fetch/v2/a1/g1/body",
            "sha256": HEX,
            "bytes": LENGTH,
            "media_type": "text/plain; charset=utf-8",
            "etag": "provider-etag",
        },
    }


class ContentIdentityTests(unittest.TestCase):
    def test_five_materially_different_owner_shapes_share_one_identity(self) -> None:
        identity = require_same_content(owner_records())
        self.assertEqual(identity, ContentIdentity(DIGEST, LENGTH))
        self.assertEqual(identity.to_dict(), {
            "schemaVersion": 1,
            "kind": "ordivon.content-identity",
            "digest": DIGEST,
            "byteLength": LENGTH,
        })

    def test_media_type_is_not_part_of_byte_identity(self) -> None:
        records = owner_records()
        records["finance"]["mediaType"] = "application/json"
        records["security"]["mediaType"] = "application/zip"
        records["studio"]["mediaType"] = "video/mp4"
        records["world"]["media_type"] = "text/html"
        self.assertEqual(require_same_content(records), ContentIdentity(DIGEST, LENGTH))

    def test_owner_ids_storage_and_lifecycle_fields_are_not_part_of_identity(self) -> None:
        records = owner_records()
        records["runtime"].update({"artifactId": "another", "droppedBytes": 999, "truncated": True})
        records["finance"].update({"evidenceRef": "another-ref", "storageClass": "external-content-addressed"})
        records["security"].update({"sampleId": "sample:owner-semantic-id", "originalName": "renamed.exe"})
        records["studio"].update({"rights": {"status": "restricted"}})
        records["world"].update({"key": "different/key", "etag": "different-etag"})
        self.assertEqual(require_same_content(records), ContentIdentity(DIGEST, LENGTH))

    def test_finance_bare_hash_normalizes_to_shared_digest_form(self) -> None:
        identity = from_finance_evidence({"algorithm": "sha256", "digest": HEX, "byteLength": LENGTH})
        self.assertEqual(identity.digest, DIGEST)

    def test_digest_change_is_content_change(self) -> None:
        records = owner_records()
        records["world"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ContentIdentityError, "owner content identities differ"):
            require_same_content(records)

    def test_byte_length_change_is_content_change(self) -> None:
        records = owner_records()
        records["runtime"]["retainedBytes"] = LENGTH - 1
        with self.assertRaisesRegex(ContentIdentityError, "owner content identities differ"):
            require_same_content(records)

    def test_invalid_algorithm_and_digest_fail_closed(self) -> None:
        with self.assertRaisesRegex(ContentIdentityError, "algorithm must be sha256"):
            from_finance_evidence({"algorithm": "sha512", "digest": HEX, "byteLength": LENGTH})
        with self.assertRaisesRegex(ContentIdentityError, "64 lowercase"):
            project_owner_content("world", {"sha256": HEX.upper(), "bytes": LENGTH})

    def test_serialized_identity_is_strict(self) -> None:
        value = ContentIdentity(DIGEST, LENGTH).to_dict()
        self.assertEqual(ContentIdentity.from_dict(value), ContentIdentity(DIGEST, LENGTH))
        with self.assertRaisesRegex(ContentIdentityError, "fields differ"):
            ContentIdentity.from_dict({**value, "mediaType": "text/plain"})

    def test_negative_or_boolean_length_fails_closed(self) -> None:
        with self.assertRaisesRegex(ContentIdentityError, "non-negative integer"):
            ContentIdentity(DIGEST, -1)
        with self.assertRaisesRegex(ContentIdentityError, "non-negative integer"):
            ContentIdentity(DIGEST, True)


if __name__ == "__main__":
    unittest.main()
