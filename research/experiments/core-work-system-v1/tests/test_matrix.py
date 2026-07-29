from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from anc_core_work_system.matrix import run_deterministic_matrix
from anc_core_work_system.world import freeze_fixture


class MatrixTests(unittest.TestCase):
    def test_deterministic_matrix_preserves_strong_baseline_outcomes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = root / "fixture"
            freeze_fixture(fixture)
            matrix = run_deterministic_matrix(
                fixture,
                working_root=root / "trials",
                temporal_cache=root / "temporal-cache",
            )
            summary = matrix["summary"]
            self.assertEqual(summary["trialCount"], 16)
            self.assertEqual(summary["passed"], 10)
            trials = {item["spec"]["variant"]: item for item in matrix["trials"]}
            self.assertTrue(trials["langgraph-sqlite"]["acceptedOutcome"])
            self.assertTrue(trials["temporal-workflow"]["acceptedOutcome"])
            self.assertTrue(trials["retrieval-current"]["acceptedOutcome"])
            self.assertTrue(trials["idempotency-audit"]["acceptedOutcome"])
            self.assertFalse(trials["transcript-summary"]["acceptedOutcome"])
            self.assertFalse(trials["plain-tool"]["acceptedOutcome"])
            self.assertTrue(summary["crossBackendEffectPromotionBlocked"])


if __name__ == "__main__":
    unittest.main()
