from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "diagnostics" / "b5-native-004-ead663e"


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


class B5FlashDiagnosticEvidenceTests(unittest.TestCase):
    def test_attempt_is_a_negative_tool_signal_not_a_task_score(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(index["classification"], "model_tool_use_no_progress")
        self.assertEqual(
            index["sourceAttemptRevision"],
            "ead663ede46a1b166e08d68a4c472884be6783a6",
        )
        self.assertEqual(
            index["evidenceAndModelPivotRevision"],
            "ac7116082198f705cb03ef7d1aae5fa71e1e08a6",
        )
        self.assertEqual(index["requestedModelId"], "deepseek-v4-flash")
        self.assertEqual(index["effectiveModelIds"], ["deepseek-v4-flash"])
        self.assertFalse(index["baselineEligible"])
        self.assertFalse(index["comparisonEligible"])
        self.assertFalse(index["taskOutcomeAdjudicated"])
        self.assertTrue(index["toolInteractionQualityObserved"])
        self.assertEqual(
            index["modelQualityConclusion"],
            "negative_tool_use_signal_not_task_acceptance_score",
        )
        self.assertEqual(index["stopCode"], "no_progress")
        self.assertEqual(index["failureClass"], "MODEL")
        self.assertEqual(index["failureCode"], "repeated_plan")
        self.assertEqual(index["responsibleBoundary"], "model")

    def test_action_sequence_exposes_failed_patch_recovery(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(
            index["actionCounts"],
            {
                "workspaceReads": 4,
                "workspacePatches": 2,
                "rejectedPatches": 2,
                "visibleChecks": 0,
                "workspaceDiffs": 0,
            },
        )
        self.assertEqual(index["metrics"]["modelCalls"], 4)
        self.assertEqual(index["metrics"]["toolCalls"], 6)
        self.assertEqual(index["metrics"]["invalidToolCalls"], 2)
        self.assertEqual(index["metrics"]["runtimeJobs"], 0)
        translations = index["runtimeRejectionTranslations"]
        self.assertEqual(len(translations), 1)
        self.assertEqual(translations[0]["code"], "INVALID_REQUEST")
        self.assertEqual(translations[0]["commitState"], "not_committed")
        self.assertEqual(translations[0]["operation"], "workspace.patch")
        self.assertEqual(index["verifierStatus"], "not_run")
        self.assertFalse(index["completionArtifactPresent"])
        self.assertTrue(index["workspaceClosed"])
        control = index["controlEvidence"]
        self.assertTrue(control["samePatchSurfacePassedDeterministicSmoke"])
        self.assertEqual(
            control["b4CloseoutDigest"],
            "sha256:51ffa2bc77e474f355e99d07356d515b84718379412c93ab833e5a2c2b2e23f5",
        )

    def test_historical_ref_defect_is_retained_and_bounded(self) -> None:
        index = load("diagnostic.json")
        defects = {item["defect"]: item for item in index["knownEvidenceDefects"]}
        self.assertEqual(
            defects["harness_run_reference_double_prefix"]["fixedRevision"],
            "ac7116082198f705cb03ef7d1aae5fa71e1e08a6",
        )
        result = load("result.json")
        self.assertEqual(
            result["trace"]["ref"],
            "harness-run:harness-run:b5-native-004",
        )
        failure = load("failure.json")
        self.assertEqual(
            failure["evidenceRefs"][0],
            "harness-run:harness-run:b5-native-004",
        )

    def test_inventory_integrity_and_sensitive_content_policy(self) -> None:
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
