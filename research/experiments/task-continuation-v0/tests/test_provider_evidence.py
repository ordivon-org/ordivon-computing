from __future__ import annotations

import json
import unittest
from pathlib import Path

from anc_continuation.evaluation import continuation_evaluation_report


EXPERIMENT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_REVISION = "1cdbbdc13514a3eb3663e2aa5bb66d077651c310"
CAPSULE_DIGEST = "sha256:4669df335a15401fbdcd3fa8f686998029c9e05787656c2c3dede4f835657f50"
CONTEXT_DIGEST = "sha256:37f2705795d01d41f275f300e56fec1afd5615ab901499a9a33138b799402d56"


class ProviderEvidenceTests(unittest.TestCase):
    def test_exact_codex_hermes_receipt_proves_provider_replacement(self) -> None:
        evidence = json.loads(
            (EXPERIMENT / "evidence/provider-comparison-1cdbbdc.json").read_text()
        )
        checked = json.loads(
            (EXPERIMENT / "evidence/provider-evaluation-1cdbbdc.json").read_text()
        )
        regenerated = continuation_evaluation_report(evidence)
        self.assertEqual(evidence["sourceRevision"], IMPLEMENTATION_REVISION)
        self.assertEqual(evidence["capsuleDigest"], CAPSULE_DIGEST)
        self.assertEqual(checked, regenerated)
        self.assertTrue(checked["allRequiredCriteriaPassed"])
        comparison = checked["providerComparison"]
        self.assertTrue(comparison["completed"])
        for key in (
            "sameCapsule",
            "sameContext",
            "sameDecision",
            "sameExecution",
            "distinctAdapters",
            "bothCompleted",
            "transcriptFree",
        ):
            self.assertTrue(comparison[key], key)
        codex = evidence["freshProcessCodex"]
        hermes = evidence["freshProcessHermes"]
        self.assertEqual(codex["host"]["contextDigest"], CONTEXT_DIGEST)
        self.assertEqual(hermes["host"]["contextDigest"], CONTEXT_DIGEST)
        self.assertEqual(codex["host"]["contextBytes"], 2573)
        self.assertEqual(hermes["host"]["contextBytes"], 2573)
        self.assertEqual(
            codex["host"]["adapterId"], "codex-cli-ephemeral-v1:gpt-5.5"
        )
        self.assertEqual(
            hermes["host"]["adapterId"],
            "hermes-cli-isolated-v1:deepseek/deepseek-v4-pro",
        )
        adapter = hermes["modelAdapterEvidence"]
        self.assertEqual(adapter["model"], "deepseek-v4-pro")
        self.assertEqual(adapter["provider"], "deepseek")
        self.assertGreaterEqual(adapter["apiCalls"], 1)
        self.assertEqual(adapter["enabledToolsets"], [])
        self.assertFalse(adapter["memoryLoaded"])
        self.assertFalse(adapter["persistentSessionRetained"])


if __name__ == "__main__":
    unittest.main()
