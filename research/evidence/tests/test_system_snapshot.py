from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


EVIDENCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = EVIDENCE_ROOT.parents[1]
REPOSITORY_ROOTS = {
    "ordivon-computing": REPOSITORY_ROOT,
    "ordivon-architecture": REPOSITORY_ROOT,
    "agent-native-computing": REPOSITORY_ROOT,
}
sys.path.insert(0, str(EVIDENCE_ROOT))

from validate_system_snapshot import canonical_payload, payload_digest, validate  # noqa: E402


SNAPSHOT = (
    EVIDENCE_ROOT
    / "snapshots"
    / "semantic-core-boundary-baseline-20260726T071247p0800.json"
)


class SystemSnapshotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.document = json.loads(SNAPSHOT.read_text())

    def validate(self, document: dict) -> None:
        validate(document, repository_roots=REPOSITORY_ROOTS)

    def test_committed_baseline_validates(self) -> None:
        self.validate(self.document)

    def test_digest_is_independent_of_json_key_order(self) -> None:
        reversed_document = dict(reversed(list(self.document.items())))
        self.assertEqual(canonical_payload(reversed_document), canonical_payload(self.document))
        self.assertEqual(payload_digest(reversed_document), payload_digest(self.document))

    def test_content_tampering_invalidates_snapshot(self) -> None:
        tampered = copy.deepcopy(self.document)
        tampered["purpose"] += " altered"
        with self.assertRaisesRegex(ValueError, "payloadDigest"):
            self.validate(tampered)

    def test_duplicate_repository_identity_is_rejected(self) -> None:
        duplicate = copy.deepcopy(self.document)
        duplicate["repositories"].append(copy.deepcopy(duplicate["repositories"][0]))
        duplicate["integrity"]["payloadDigest"] = payload_digest(duplicate)
        with self.assertRaisesRegex(ValueError, "duplicate repository"):
            self.validate(duplicate)

    def test_unknown_service_repository_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.document)
        invalid["services"][0]["sourceRepositoryId"] = "missing"
        invalid["integrity"]["payloadDigest"] = payload_digest(invalid)
        with self.assertRaisesRegex(ValueError, "sourceRepositoryId"):
            self.validate(invalid)

    def test_unknown_service_contract_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.document)
        invalid["services"][0]["contractIds"] = ["missing"]
        invalid["integrity"]["payloadDigest"] = payload_digest(invalid)
        with self.assertRaisesRegex(ValueError, "unknown contract"):
            self.validate(invalid)


    def test_unknown_artifact_repository_is_rejected(self) -> None:
        invalid = copy.deepcopy(self.document)
        invalid["artifacts"][0]["repositoryId"] = "missing"
        invalid["integrity"]["payloadDigest"] = payload_digest(invalid)
        with self.assertRaisesRegex(ValueError, "artifact repositoryId"):
            self.validate(invalid)

    def test_local_artifact_digest_is_verified(self) -> None:
        invalid = copy.deepcopy(self.document)
        invalid["artifacts"][0]["digest"] = "sha256:" + "0" * 64
        invalid["integrity"]["payloadDigest"] = payload_digest(invalid)
        with self.assertRaisesRegex(ValueError, "artifact digest mismatch"):
            self.validate(invalid)


if __name__ == "__main__":
    unittest.main()
