from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


EVIDENCE_ROOT = Path(__file__).resolve().parents[1]
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

    def test_committed_baseline_validates(self) -> None:
        validate(self.document)

    def test_digest_is_independent_of_json_key_order(self) -> None:
        reversed_document = dict(reversed(list(self.document.items())))
        self.assertEqual(canonical_payload(reversed_document), canonical_payload(self.document))
        self.assertEqual(payload_digest(reversed_document), payload_digest(self.document))

    def test_content_tampering_invalidates_snapshot(self) -> None:
        tampered = copy.deepcopy(self.document)
        tampered["purpose"] += " altered"
        with self.assertRaisesRegex(ValueError, "payloadDigest"):
            validate(tampered)

    def test_duplicate_repository_identity_is_rejected(self) -> None:
        duplicate = copy.deepcopy(self.document)
        duplicate["repositories"].append(copy.deepcopy(duplicate["repositories"][0]))
        duplicate["integrity"]["payloadDigest"] = payload_digest(duplicate)
        with self.assertRaisesRegex(ValueError, "duplicate repository"):
            validate(duplicate)

    def test_dynamic_project_maturity_is_not_in_registry(self) -> None:
        registry = (EVIDENCE_ROOT.parents[1] / "projects" / "registry.yaml").read_text()
        self.assertNotIn("maturity:", registry)


if __name__ == "__main__":
    unittest.main()
