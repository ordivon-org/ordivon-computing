from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC = ROOT / "diagnostics" / "b5-native-005-32ec1ea"


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


class B5ProDiagnosticEvidenceTests(unittest.TestCase):
    def test_pro_improved_exploration_but_failed_the_frozen_patch_gate(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(index["classification"], "model_tool_use_no_progress_pro")
        self.assertEqual(
            index["sourceAttemptRevision"],
            "32ec1eaa9a9e65e7cd87192de3964a012c2297f2",
        )
        self.assertEqual(
            index["runnerRevision"],
            "ac7116082198f705cb03ef7d1aae5fa71e1e08a6",
        )
        self.assertEqual(index["requestedModelId"], "deepseek-v4-pro")
        self.assertEqual(index["effectiveModelIds"], ["deepseek-v4-pro"])
        self.assertFalse(index["baselineEligible"])
        self.assertFalse(index["comparisonEligible"])
        self.assertFalse(index["taskOutcomeAdjudicated"])
        self.assertTrue(index["toolInteractionQualityObserved"])
        self.assertEqual(index["stopCode"], "no_progress")
        self.assertEqual(index["failureClass"], "MODEL")
        self.assertEqual(index["failureCode"], "repeated_plan")
        self.assertEqual(index["responsibleBoundary"], "model")
        self.assertEqual(
            index["providerCapabilityConclusion"],
            "tested_deepseek_models_do_not_satisfy_frozen_patch_tool_fidelity_gate",
        )

    def test_three_model_correctable_patch_rejections_are_bound(self) -> None:
        index = load("diagnostic.json")
        self.assertEqual(
            index["actionCounts"],
            {
                "workspaceReads": 3,
                "visibleChecks": 1,
                "workspaceDiffs": 1,
                "workspacePatches": 3,
                "rejectedPatches": 3,
            },
        )
        rejections = index["patchRejections"]
        self.assertEqual(len(rejections), 3)
        self.assertEqual(
            [item["correction"] for item in rejections],
            [1, 2, 3],
        )
        self.assertTrue(all(item["type"] == "ToolBridgeError" for item in rejections))
        self.assertTrue(all(item["kind"] == "model_correctable" for item in rejections))
        self.assertTrue(all(item["safeToCorrect"] for item in rejections))
        self.assertTrue(
            all(item["messageDigest"].startswith("sha256:") for item in rejections)
        )
        self.assertEqual(index["metrics"]["modelCalls"], 6)
        self.assertEqual(index["metrics"]["toolCalls"], 8)
        self.assertEqual(index["metrics"]["invalidToolCalls"], 3)
        self.assertEqual(index["metrics"]["runtimeJobs"], 1)

    def test_runtime_terminal_evidence_exists_without_claiming_check_outcome(self) -> None:
        index = load("diagnostic.json")
        runtime = index["runtimeEvidence"]
        self.assertEqual(len(runtime["jobIds"]), 1)
        self.assertEqual(runtime["selectedRuntimeEventCount"], 8)
        self.assertTrue(runtime["terminalEventObserved"])
        self.assertFalse(runtime["checkOutcomeTextRetained"])
        self.assertFalse(index["selectionComplete"])
        self.assertTrue(index["workspaceClosed"])
        self.assertEqual(index["verifierStatus"], "not_run")
        self.assertFalse(index["completionArtifactPresent"])
        comparison = index["flashComparison"]
        self.assertFalse(comparison["flashReachedRuntimeJob"])
        self.assertTrue(comparison["proReachedRuntimeJob"])
        self.assertFalse(comparison["bothProducedUsablePatch"])
        self.assertFalse(comparison["bothReachedVerifier"])

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
