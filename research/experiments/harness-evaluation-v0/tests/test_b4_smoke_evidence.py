from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "b4-smoke-78de3a6"
EXPECTED_FILES = {
    "closeout.json",
    "deterministic-fault-cells.json",
    "disposition.json",
    "grader-bundle.json",
    "integrated-fault-cells.json",
    "intent.json",
    "native-refs.json",
    "observation-selection.json",
    "result.json",
    "review.json",
    "runner-state.json",
    "system-manifest.json",
    "system-snapshot.json",
    "trial.json",
}


def load(name: str) -> dict[str, object]:
    value = json.loads((EVIDENCE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} must contain an object")
    return value


def payload_digest(value: dict[str, object]) -> str:
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


class B4SmokeEvidenceTests(unittest.TestCase):
    def test_inventory_and_all_record_integrity(self) -> None:
        observed = {path.name for path in EVIDENCE.glob("*.json")}
        self.assertEqual(observed, EXPECTED_FILES)
        for name in sorted(observed):
            with self.subTest(name=name):
                value = load(name)
                integrity = value.get("integrity")
                self.assertIsInstance(integrity, dict)
                self.assertEqual(
                    integrity["payloadDigest"],
                    payload_digest(value),
                )

    def test_runner_closed_state_binds_every_required_record(self) -> None:
        state = load("runner-state.json")
        self.assertEqual(state["stage"], "closed")
        self.assertEqual(state["revision"], 7)
        record_digests = state["recordDigests"]
        self.assertEqual(
            set(record_digests),
            EXPECTED_FILES - {"intent.json", "runner-state.json"},
        )
        for name, expected in record_digests.items():
            self.assertEqual(load(name)["integrity"]["payloadDigest"], expected)

    def test_exact_system_snapshot_and_nonproduction_boundary(self) -> None:
        snapshot = load("system-snapshot.json")
        self.assertEqual(
            snapshot["computingRevision"],
            "78de3a6225802ea6eb7d8970eaabc1cca1e25407",
        )
        self.assertEqual(
            snapshot["hostRevision"],
            "a76a620160b28d870670696e04c39e539296fe00",
        )
        self.assertEqual(
            snapshot["harnessRevision"],
            "ac10497f1b6e681899cfe98c347ed6d48941ba23",
        )
        self.assertEqual(
            snapshot["runtimeRevision"],
            "a455fd01ce0dea25684956e5e5da899d41832a1b",
        )
        self.assertFalse(snapshot["productionActivated"])
        closeout = load("closeout.json")
        self.assertTrue(closeout["computingClean"])
        self.assertTrue(closeout["workspaceClosed"])
        self.assertFalse(closeout["productionActivated"])
        self.assertFalse(closeout["b6Implemented"])

    def test_selection_disposition_and_result_form_valid_evidence_chain(self) -> None:
        selection = load("observation-selection.json")
        self.assertTrue(selection["completeness"]["complete"])
        self.assertFalse(selection["completeness"]["trialValidityInferred"])
        self.assertTrue(selection["privacy"]["metadataOnly"])
        self.assertFalse(selection["privacy"]["payloadBytesCopied"])
        self.assertFalse(selection["privacy"]["secretForbiddenPresent"])
        disposition = load("disposition.json")
        self.assertEqual(disposition["validity"], "valid")
        self.assertEqual(disposition["semanticOutcome"], "accepted")
        self.assertFalse(disposition["comparisonEligible"])
        self.assertEqual(
            disposition["selectionDigest"], selection["selectionDigest"]
        )
        result = load("result.json")
        self.assertEqual(result["acceptance"]["status"], "accepted")
        self.assertFalse(result["acceptance"]["falseCompletion"])
        self.assertEqual(result["acceptance"]["verifier"]["status"], "passed")

    def test_all_integrated_and_deterministic_fault_cells_passed(self) -> None:
        closeout = load("closeout.json")
        self.assertEqual(closeout["pendingDeterministicUnitCells"], [])
        self.assertTrue(all(closeout["integratedFaultCells"].values()))
        self.assertTrue(all(closeout["deterministicFaultCells"].values()))
        deterministic = load("deterministic-fault-cells.json")
        self.assertTrue(deterministic["allPassed"])
        self.assertEqual(
            closeout["deterministicFaultCellsDigest"],
            deterministic["integrity"]["payloadDigest"],
        )
        self.assertTrue(closeout["liveTrialUnlocked"])

    def test_committed_evidence_contains_no_secret_or_reasoning_material(self) -> None:
        encoded = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(EVIDENCE.glob("*.json"))
        ).lower()
        for forbidden in (
            "api_key",
            "bearer_token",
            "authorization",
            "/root/.config/ordivon/secrets",
            "private reasoning",
            "raw chain of thought",
        ):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()
