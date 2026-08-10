from __future__ import annotations

import json
import unittest
from pathlib import Path

from maintenance import canonical_digest

HERE = Path(__file__).resolve().parents[1]
EVIDENCE = HERE / "evidence" / "p0-live-acceptance.json"


class LiveEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_integrity_and_truth_boundary(self) -> None:
        document = dict(self.document)
        digest = document.pop("acceptanceDigest")
        self.assertEqual(digest, canonical_digest(document))
        boundary = self.document["maintenanceProjection"]["truthBoundary"]
        self.assertFalse(boundary["projectionAuthoritative"])
        self.assertTrue(boundary["ownerNativeFactsRemainAuthoritative"])
        self.assertTrue(boundary["unknownNeverAutoDeleted"])
        self.assertTrue(boundary["dirtyNeverAutoDeleted"])

    def test_fast_and_measured_lifecycle_are_split_by_evidence(self) -> None:
        cadence = self.document["cadenceExperiment"]
        self.assertEqual(cadence["decision"], "split_fast_classification_from_byte_measurement")
        self.assertGreater(cadence["byteMeasurementSlowdown"], 3.0)
        self.assertEqual(cadence["recommendedFastClassificationCadence"], "hourly")
        self.assertEqual(cadence["recommendedByteMeasurementCadence"], "daily")
        self.assertFalse(cadence["mutationAuthorized"])

    def test_compatibility_erasure_is_selective(self) -> None:
        erasure = self.document["compatibilityErasure"]
        self.assertEqual(set(erasure["removed"]), {"ReferenceKernel", "JournalKernel"})
        self.assertEqual(erasure["retained"], ["EffectSpec historical Journal decode"])
        summary = self.document["compatibility"]
        self.assertEqual(summary["removed"], 1)
        self.assertEqual(summary["removableCandidates"], 0)
        self.assertEqual(summary["retained"], 1)
        self.assertEqual(summary["unsupportedDebt"], 0)

    def test_owner_doctors_remain_owner_native_signals(self) -> None:
        doctors = {item["owner"]: item for item in self.document["ownerDoctors"]}
        self.assertEqual(doctors["ordivon-world"]["status"], "ok")
        self.assertEqual(doctors["workstation-lab"]["status"], "fail")
        signals = [
            item
            for item in self.document["maintenanceProjection"]["signals"]
            if item["area"] == "owner-doctor"
        ]
        states = {item["owner"]: item["state"] for item in signals}
        self.assertEqual(states["ordivon-world"], "healthy")
        self.assertEqual(states["workstation-lab"], "attention")

    def test_unavailable_conformance_tooling_is_explicit_not_success(self) -> None:
        conformance = self.document["conformanceStatus"]
        self.assertFalse(conformance["passed"])
        self.assertEqual(conformance["blockedBy"], "vale_missing")

    def test_dirty_aging_never_authorizes_deletion(self) -> None:
        dirty = self.document["dirtyAging"]
        self.assertGreater(dirty["dirtyWorkspaces"], 0)
        self.assertGreater(dirty["actionable"], 0)
        self.assertTrue(all(not item["automaticDeletionAllowed"] for item in dirty["queue"]))


if __name__ == "__main__":
    unittest.main()
