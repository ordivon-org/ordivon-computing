from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "diagnostics" / "b5-native-002-b7d2c47"


def load(name: str) -> dict[str, object]:
    value = json.loads((DIAGNOSTIC / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} must contain an object")
    return value


class B5PolicyDiagnosticEvidenceTests(unittest.TestCase):
    def test_attempt_is_retained_but_not_baseline_eligible(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(
            index["classification"],
            "runner_policy_error_incomplete",
        )
        self.assertFalse(index["baselineEligible"])
        self.assertFalse(index["comparisonEligible"])
        self.assertTrue(index["workspaceClosed"])
        self.assertEqual(index["runtimeJobCount"], 0)
        self.assertFalse(index["selectionComplete"])
        self.assertEqual(index["verifierStatus"], "not_run")
        self.assertFalse(index["productionActivated"])
        self.assertFalse(index["b6Implemented"])

    def test_diagnostic_binds_attempt_selection_and_provider_identity(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(
            index["sourceAttemptRevision"],
            "b7d2c476a71aa0d3e4e13639a7db091060763c29",
        )
        selection = load("observation-selection.json")
        self.assertFalse(selection["completeness"]["complete"])
        self.assertEqual(index["selectionDigest"], selection["selectionDigest"])
        self.assertEqual(index["selectedEventCount"], 19)
        self.assertEqual(index["sourceStreamCount"], 2)
        provider = load("provider-identity.json")
        self.assertEqual(provider["providerId"], "deepseek")
        self.assertEqual(provider["requestedModelId"], "deepseek-v4-flash")
        self.assertEqual(
            provider["credentialScopeId"],
            "credential-scope:deepseek:flash:0",
        )
        closeout = load("attempt-closeout.json")
        self.assertEqual(closeout["status"], "runner_error")
        self.assertEqual(closeout["runtimeJobCount"], 0)
        self.assertTrue(closeout["workspaceClosed"])

    def test_diagnostic_integrity_and_inventory(self) -> None:
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
        observed = {
            path.name
            for path in DIAGNOSTIC.glob("*.json")
            if path.name != "diagnostic.json"
        }
        self.assertEqual(set(index["retainedFiles"]), observed)
        self.assertNotIn("system-manifest.json", observed)
        state = load("runner-state.json")
        self.assertEqual(state["stage"], "evidence_collected")
        self.assertEqual(state["revision"], 4)

    def test_diagnostic_contains_no_sensitive_or_model_internal_material(self) -> None:
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
