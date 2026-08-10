from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

EXPERIMENT = Path(__file__).resolve().parents[1]
if str(EXPERIMENT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT))

import run_p0_live as live


class LiveP0SemanticsTests(unittest.TestCase):
    def test_a_validity_is_independent_of_semantic_success(self) -> None:
        cells = {
            "S": {
                "cellId": "S",
                "visibleTaskDigest": "sha256:" + "1" * 64,
                "trialValid": True,
                "semanticAccepted": False,
            },
            "H": {
                "cellId": "H",
                "visibleTaskDigest": "sha256:" + "1" * 64,
                "trialValid": True,
                "semanticAccepted": True,
            },
        }

        def fake_runner(*, settings, replicate):
            return cells["S"] if fake_runner.calls == 0 else cells["H"]

        fake_runner.calls = 0

        def first(*, settings, replicate):
            fake_runner.calls += 1
            return cells["S"]

        def second(*, settings, replicate):
            return cells["H"]

        with (
            patch.object(live, "run_a_cell_s", first),
            patch.object(live, "run_a_cell_h", second),
            patch.object(live, "repo_vector", return_value={}),
            patch.object(live, "provider_identity", return_value={}),
        ):
            receipt = live.run_a_pair(settings=object(), replicate=7, order="SH")
        self.assertTrue(receipt["trialValidPair"])
        self.assertEqual(receipt["semanticOutcome"], {"S": "rejected", "H": "accepted"})

    def test_b_validity_is_independent_of_oracle_correctness(self) -> None:
        direct = {
            "treatment": "direct",
            "contextDigest": "sha256:" + "2" * 64,
            "requestToolCounts": [1],
            "trialValid": True,
            "oracleConsistent": False,
        }
        late = {
            "treatment": "late-authority",
            "contextDigest": "sha256:" + "2" * 64,
            "requestToolCounts": [0, 1],
            "trialValid": True,
            "oracleConsistent": True,
        }

        with (
            patch.object(live, "run_b_cell", side_effect=[direct, late]),
            patch.object(live, "repo_vector", return_value={}),
            patch.object(live, "provider_identity", return_value={}),
        ):
            receipt = live.run_b_pair(settings=object(), fixture={"fixtureId": "x"}, replicate=3)
        self.assertTrue(receipt["trialValidPair"])
        self.assertEqual(receipt["oracleOutcome"], {"direct": "incorrect", "late-authority": "correct"})


if __name__ == "__main__":
    unittest.main()
