from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from ordivon_observation_core import ObservationSelectionManifest  # noqa: E402

EVIDENCE = ROOT / "evidence" / "b3-owner-native-e9bc8b4"
RECEIPT = EVIDENCE / "receipt.json"
SELECTION = EVIDENCE / "observation-selection.json"


def canonical_digest(value: dict[str, object]) -> str:
    payload = dict(value)
    payload.pop("integrity", None)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


class B3OwnerNativeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
        cls.selection_value = json.loads(SELECTION.read_text(encoding="utf-8"))
        cls.selection = ObservationSelectionManifest.from_dict(cls.selection_value)

    def test_receipt_integrity_and_exact_revision(self) -> None:
        self.assertEqual(
            self.receipt["kind"],
            "ordivon.observation-b3-owner-native-acceptance",
        )
        self.assertEqual(self.receipt["workPackage"], "B3")
        self.assertEqual(
            self.receipt["computingRevision"],
            "e9bc8b49941fb332f9f1f5774588bddca72a5b49",
        )
        self.assertTrue(self.receipt["computingClean"])
        self.assertEqual(
            self.receipt["integrity"]["payloadDigest"],
            canonical_digest(self.receipt),
        )

    def test_selection_and_receipt_are_bound(self) -> None:
        self.assertEqual(
            self.receipt["selectionDigest"], self.selection.selection_digest
        )
        self.assertEqual(
            self.receipt["selectionIntegrityDigest"],
            self.selection.integrity_digest,
        )
        self.assertEqual(
            self.receipt["catalogDigest"], self.selection.catalog_digest
        )
        self.assertEqual(
            self.receipt["selectedEventCount"], len(self.selection.selected_events)
        )
        self.assertEqual(
            self.receipt["sourceStreamCount"],
            len(self.selection.source_stream_heads),
        )

    def test_b3_is_complete_without_claiming_trial_validity(self) -> None:
        self.assertTrue(all(self.receipt["checks"].values()))
        self.assertTrue(self.selection.completeness["complete"])
        self.assertFalse(self.selection.completeness["trialValidityInferred"])
        self.assertTrue(self.receipt["formalRunnerUnblocked"])
        self.assertFalse(self.receipt["liveTrialUnlocked"])
        self.assertFalse(self.receipt["productionActivated"])
        self.assertFalse(self.receipt["ownerStateRetained"])
        self.assertEqual(
            self.selection.query.artifact_coverage,
            "owner_native_only",
        )

    def test_evidence_contains_no_copied_private_content(self) -> None:
        encoded = (RECEIPT.read_text(encoding="utf-8") + SELECTION.read_text(
            encoding="utf-8"
        )).lower()
        for forbidden in (
            "api_key",
            "bearer_token",
            "private reasoning",
            "runtime command must not enter observation",
            "host task payload must not enter observation",
            "harness tool payload must not enter observation",
        ):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()
