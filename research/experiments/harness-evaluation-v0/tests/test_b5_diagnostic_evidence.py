from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "diagnostics" / "b5-native-001-ad3ca58"


def load(name: str) -> dict[str, object]:
    value = json.loads((DIAGNOSTIC / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} must contain an object")
    return value


class B5DiagnosticEvidenceTests(unittest.TestCase):
    def test_initial_canary_is_preserved_but_not_baseline_eligible(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(index["classification"], "invalid_incomplete")
        self.assertFalse(index["baselineEligible"])
        self.assertFalse(index["comparisonEligible"])
        self.assertTrue(index["workspaceClosed"])
        self.assertEqual(index["runtimeJobCount"], 0)
        self.assertFalse(index["productionActivated"])
        self.assertFalse(index["b6Implemented"])

    def test_diagnostic_binds_exact_old_runner_and_attempt_closeout(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(
            index["sourceAttemptRevision"],
            "ad3ca5817a269b09d4ba5144933f6c8a59b24f01",
        )
        closeout = load("attempt-closeout.json")
        self.assertEqual(closeout["status"], "invalid_incomplete")
        self.assertEqual(closeout["runtimeJobCount"], 0)
        self.assertTrue(closeout["workspaceClosed"])
        state = load("runner-state.json")
        self.assertEqual(state["stage"], "executing")
        self.assertEqual(state["revision"], 3)

    def test_diagnostic_index_integrity_and_inventory(self) -> None:
        index = load("diagnostic.json")
        integrity = index.pop("integrity")
        encoded = json.dumps(
            index,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        self.assertEqual(
            integrity["payloadDigest"],
            "sha256:" + hashlib.sha256(encoded).hexdigest(),
        )
        self.assertEqual(
            set(index["retainedFiles"]),
            {
                "attempt-closeout.json",
                "intent.json",
                "runner-state.json",
                "system-manifest.json",
                "system-snapshot.json",
            },
        )

    def test_diagnostic_contains_no_secret_or_reasoning_material(self) -> None:
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
        ):
            self.assertNotIn(forbidden, encoded)


if __name__ == "__main__":
    unittest.main()
