from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "diagnostics" / "b5-native-003-1e8eda0"


def load(name: str) -> dict[str, object]:
    value = json.loads((DIAGNOSTIC / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} must contain an object")
    return value


def verify_integrity(value: dict[str, object]) -> None:
    payload = dict(value)
    integrity = payload.pop("integrity")
    if not isinstance(integrity, dict):
        raise AssertionError("integrity must be an object")
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    assert integrity["payloadDigest"] == (
        "sha256:" + hashlib.sha256(encoded).hexdigest()
    )


class B5RuntimeDiagnosticEvidenceTests(unittest.TestCase):
    def test_attempt_is_invalid_and_does_not_measure_model_quality(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(index["classification"], "harness_failed_incomplete")
        self.assertEqual(
            index["sourceAttemptRevision"],
            "1e8eda03fae04aa0c8092ddff2f08d5157918ea7",
        )
        self.assertEqual(
            index["runtimeExceptionAdapterRevision"],
            "4c885c2934d573eddfba01d826fd13633c3cafd6",
        )
        self.assertFalse(index["baselineEligible"])
        self.assertFalse(index["comparisonEligible"])
        self.assertFalse(index["modelQualityAdjudicated"])
        self.assertEqual(index["stopCode"], "harness_failed")
        self.assertEqual(index["failureClass"], "HARNESS")
        self.assertEqual(index["failureCode"], "state_loss")
        self.assertEqual(index["verifierStatus"], "not_run")
        self.assertEqual(index["runtimeJobCount"], 0)
        self.assertTrue(index["workspaceClosed"])

    def test_durable_boundary_and_selection_are_bound(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(
            index["lastDurableToolCounts"],
            {"prepared": 4, "recorded": 3},
        )
        self.assertEqual(index["traceEventCount"], 21)
        self.assertEqual(index["harnessEventCount"], 16)
        selection = load("observation-selection.json")
        self.assertFalse(selection["completeness"]["complete"])
        self.assertEqual(index["selectionDigest"], selection["selectionDigest"])
        self.assertEqual(index["selectedEventCount"], len(selection["selectedEvents"]))
        reservation = load("campaign-reservation.json")
        self.assertEqual(
            index["campaignReservationDigest"],
            reservation["integrity"]["payloadDigest"],
        )
        state = load("runner-state.json")
        self.assertEqual(state["stage"], "closed")
        self.assertIn("campaign-reservation.json", state["recordDigests"])

    def test_inventory_and_all_record_integrity(self) -> None:
        index = load("diagnostic.json")
        verify_integrity(index)
        observed = {
            path.name
            for path in DIAGNOSTIC.glob("*.json")
            if path.name != "diagnostic.json"
        }
        self.assertEqual(set(index["retainedFiles"]), observed)
        self.assertEqual(set(index["recordDigests"]), observed)
        for name in observed:
            value = load(name)
            verify_integrity(value)
            self.assertEqual(
                index["recordDigests"][name],
                value["integrity"]["payloadDigest"],
            )

    def test_diagnostic_contains_no_sensitive_or_unfiltered_payload_material(self) -> None:
        encoded = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(DIAGNOSTIC.glob("*.json"))
        ).lower()
        for forbidden in (
            "api_key",
            "bearer_token",
            "authorization",
            "/root/.config/ordivon/secrets",
            "raw chain of thought",
            "private reasoning",
            "raw reasoning",
        ):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()
