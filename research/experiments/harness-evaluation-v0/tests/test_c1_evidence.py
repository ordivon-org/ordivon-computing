from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = (
    ROOT
    / "research"
    / "experiments"
    / "harness-evaluation-v0"
    / "evidence"
    / "c1-independent-runtime-c29b648"
)
OBSERVATION_CORE = (
    ROOT
    / "research"
    / "experiments"
    / "observation-plane-v0"
    / "implementation"
)
if str(OBSERVATION_CORE) not in sys.path:
    sys.path.insert(0, str(OBSERVATION_CORE))

from ordivon_observation_core import ObservationSelectionManifest  # noqa: E402


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: dict) -> str:
    payload = {key: item for key, item in value.items() if key != "integrity"}
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


class C1EvidenceTests(unittest.TestCase):
    def test_fixed_real_model_set_retains_all_three_outcomes(self) -> None:
        value = json.loads((EVIDENCE / "canary-set.json").read_text())
        self.assertEqual(value["summary"]["replicas"], 3)
        self.assertEqual(value["summary"]["passed"], 0)
        self.assertEqual(value["summary"]["incomplete"], 3)
        self.assertTrue(value["replicaPolicy"]["successDoesNotStopSet"])
        self.assertEqual(
            value["integrity"]["payloadDigest"],
            canonical_digest(value),
        )

        third = next(item for item in value["results"] if item["replica"] == 3)
        self.assertEqual(third["runReceipt"]["terminationCode"], "budget_exhausted")
        self.assertIsNone(third["completionProposal"])
        self.assertTrue(third["verification"]["visiblePassed"])
        self.assertTrue(third["verification"]["hiddenPassed"])
        self.assertTrue(third["execution"]["injectedPatchResponseLoss"])
        self.assertEqual(len(third["runReceipt"]["runtimeJobRefs"]), 2)

    def test_independent_selection_is_complete_without_trial_validity(self) -> None:
        value = json.loads((EVIDENCE / "observation-selection.json").read_text())
        selection = ObservationSelectionManifest.from_dict(value)
        self.assertTrue(selection.completeness["complete"])
        self.assertFalse(selection.completeness["trialValidityInferred"])
        self.assertEqual(len(selection.selected_events), 63)
        self.assertEqual(
            {entry["projectId"] for entry in selection.producer_mapping_versions},
            {"ordivon-harness", "ordivon-runtime"},
        )
        claims = {
            item["claimId"]: item["status"]
            for item in selection.completeness["claims"]
        }
        self.assertEqual(claims["harness_terminal_receipt_recorded"], "satisfied")
        self.assertEqual(claims["runtime_jobs_covered"], "satisfied")
        self.assertNotIn("harness_completion_proposed", claims)

    def test_closeout_binds_evidence_and_keeps_harness_promotion_blocked(self) -> None:
        receipt = json.loads((EVIDENCE / "receipt.json").read_text())
        self.assertEqual(receipt["status"], "validated_with_promotion_blocked")
        self.assertFalse(receipt["decisions"]["moreRealModelReplicasAuthorized"])
        self.assertFalse(receipt["decisions"]["harnessCandidatePromotionAuthorized"])
        self.assertEqual(
            receipt["artifacts"]["canarySetDigest"],
            file_digest(EVIDENCE / "canary-set.json"),
        )
        self.assertEqual(
            receipt["artifacts"]["observationSelectionFileDigest"],
            file_digest(EVIDENCE / "observation-selection.json"),
        )
        encoded_diff = EVIDENCE / "harness-candidate.diff.b64"
        self.assertEqual(
            receipt["artifacts"]["harnessCandidateDiffEncodedFileDigest"],
            file_digest(encoded_diff),
        )
        self.assertEqual(
            receipt["artifacts"]["harnessCandidateDiffDecodedDigest"],
            "sha256:" + hashlib.sha256(
                base64.b64decode(encoded_diff.read_bytes())
            ).hexdigest(),
        )
        self.assertEqual(
            receipt["artifacts"]["harnessH4SideFindingDigest"],
            file_digest(EVIDENCE / "harness-h4-side-finding.json"),
        )
        side_finding = json.loads(
            (EVIDENCE / "harness-h4-side-finding.json").read_text()
        )
        self.assertFalse(side_finding["decision"]["retryUntilGreen"])
        self.assertFalse(side_finding["decision"]["weakenH4Freshness"])
        self.assertFalse(side_finding["decision"]["promoteCandidateToHarnessRoot"])
        self.assertEqual(
            side_finding["integrity"]["payloadDigest"],
            canonical_digest(side_finding),
        )
        self.assertEqual(
            receipt["integrity"]["payloadDigest"],
            canonical_digest(receipt),
        )


if __name__ == "__main__":
    unittest.main()
