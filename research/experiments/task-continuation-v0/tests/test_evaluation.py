from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
