from __future__ import annotations

from pathlib import Path
import sys
import unittest

EXPERIMENT = Path(__file__).resolve().parents[1]
if str(EXPERIMENT) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT))

import run_p0_a0_scripted_comparator as a0
import run_p0_b0_authority_timing as b0


class P0A0ComparatorTests(unittest.TestCase):
    def test_scripted_cells_share_task_verifier_and_candidate(self) -> None:
        receipt = a0.run(allow_dirty_computing=True)
        self.assertTrue(receipt["disposition"]["a0Ready"])
        self.assertFalse(receipt["comparability"]["competitiveProviderEvidence"])
        self.assertTrue(receipt["comparability"]["sameVisibleTask"])
        self.assertTrue(receipt["comparability"]["sameFrozenVerifier"])
        self.assertTrue(receipt["comparability"]["sameCandidateBytesUnderScriptedOracle"])
        cells = {cell["cellId"]: cell for cell in receipt["cells"]}
        self.assertEqual(cells["S"]["metrics"]["modelCalls"], 1)
        self.assertEqual(cells["S"]["metrics"]["toolCalls"], 0)
        self.assertEqual(cells["H"]["metrics"]["modelCalls"], 5)
        self.assertEqual(cells["H"]["metrics"]["toolCalls"], 4)

    def test_high_level_agent_run_gap_is_explicit(self) -> None:
        probe = a0.probe_high_level_agent_run_gap()
        self.assertFalse(probe["supported"])
        self.assertEqual(probe["surface"], "HarnessAgentRun")
        self.assertIn("does not implement", probe["reason"])


class P0B0AuthorityTimingTests(unittest.TestCase):
    def test_fixture_oracles_are_mechanical_and_distinct(self) -> None:
        derived = [b0.derive_oracle_intent(fixture) for fixture in b0.FIXTURES]
        labels = [fixture["oracleIntent"] for fixture in b0.FIXTURES]
        self.assertEqual(derived, labels)
        self.assertEqual(set(derived), {"act", "hold"})

    def test_direct_and_late_treatments_isolate_tool_exposure_timing(self) -> None:
        receipt = b0.run(allow_dirty_computing=True)
        self.assertTrue(receipt["disposition"]["b0Ready"])
        self.assertFalse(receipt["disposition"]["liveProviderEvidence"])
        self.assertTrue(receipt["acceptance"]["directExposesToolInitially"])
        self.assertTrue(receipt["acceptance"]["lateHidesToolDuringDeliberation"])
        self.assertTrue(receipt["acceptance"]["lateExposesSameToolAfterDeliberation"])
        self.assertTrue(receipt["acceptance"]["sameContextPerPair"])
        self.assertTrue(receipt["acceptance"]["sameAggregateBudgetPerPair"])
        by_key = {(cell["fixtureId"], cell["treatment"]): cell for cell in receipt["cells"]}
        act_direct = by_key[("margin-window-a", "direct")]
        act_late = by_key[("margin-window-a", "late-authority")]
        hold_direct = by_key[("margin-window-b", "direct")]
        hold_late = by_key[("margin-window-b", "late-authority")]
        self.assertEqual(act_direct["firstAuthoritativeIntentPosition"], 1)
        self.assertEqual(act_late["firstAuthoritativeIntentPosition"], 2)
        self.assertIsNone(hold_direct["firstAuthoritativeIntentPosition"])
        self.assertIsNone(hold_late["firstAuthoritativeIntentPosition"])


if __name__ == "__main__":
    unittest.main()
