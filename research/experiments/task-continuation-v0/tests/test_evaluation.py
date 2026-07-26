from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from anc_continuation.evaluation import continuation_evaluation_report


EXPERIMENT = Path(__file__).resolve().parents[1]


class EvaluationTests(unittest.TestCase):
    def test_scripted_evidence_produces_passing_semantic_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            evidence_path = Path(temporary) / "evidence.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(EXPERIMENT / "scripts/run_continuation_evidence.py"),
                    "--source-revision",
                    "f" * 40,
                    "--output",
                    str(evidence_path),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            evidence = json.loads(evidence_path.read_text())
            report = continuation_evaluation_report(evidence)
            self.assertTrue(report["allRequiredCriteriaPassed"])
            self.assertEqual(
                report["capsuleAblation"]["hardDependencies"],
                [
                    "withoutDecisionArtifact",
                    "withoutCheckpointFact",
                    "withoutCurrentBinding",
                ],
            )
            self.assertTrue(
                report["capsuleAblation"]["completedEffectsAreProvenanceDependency"]
            )
            self.assertEqual(
                report["scriptedFreshHost"]["repeatedCompletedEffects"], []
            )
            self.assertEqual(report["driftCase"]["executedEffects"], [])

    def test_two_real_adapter_receipts_complete_provider_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            evidence_path = Path(temporary) / "evidence.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(EXPERIMENT / "scripts/run_continuation_evidence.py"),
                    "--source-revision",
                    "f" * 40,
                    "--output",
                    str(evidence_path),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            evidence = json.loads(evidence_path.read_text())
            scripted = evidence["freshProcessScripted"]
            codex = copy.deepcopy(scripted)
            codex["host"]["adapterId"] = "codex-cli-ephemeral-v1:gpt-5.5"
            hermes = copy.deepcopy(scripted)
            hermes["host"]["adapterId"] = (
                "hermes-cli-isolated-v1:deepseek/deepseek-v4-pro"
            )
            hermes["modelTokenCount"] = 900
            hermes["modelAdapterEvidence"] = {
                "model": "deepseek-v4-pro",
                "provider": "deepseek",
                "apiCalls": 1,
                "isolatedHome": True,
                "persistentSessionRetained": False,
                "enabledToolsets": [],
                "memoryLoaded": False,
            }
            evidence["freshProcessCodex"] = codex
            evidence["freshProcessHermes"] = hermes
            report = continuation_evaluation_report(evidence)
            self.assertTrue(report["allRequiredCriteriaPassed"])
            self.assertTrue(report["providerComparison"]["completed"])
            self.assertTrue(report["providerComparison"]["sameCapsule"])
            self.assertTrue(report["providerComparison"]["sameContext"])
            self.assertTrue(report["providerComparison"]["sameDecision"])
            self.assertTrue(report["providerComparison"]["distinctAdapters"])
            self.assertEqual(
                report["hermesFreshHost"]["modelAdapterEvidence"]["provider"],
                "deepseek",
            )


if __name__ == "__main__":
    unittest.main()
