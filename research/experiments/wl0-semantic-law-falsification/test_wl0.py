from __future__ import annotations

import unittest

from law_falsification import physical_probes, run_all, run_l1, run_l2, run_l3, run_l4, run_l5


class SemanticLawFalsificationTests(unittest.TestCase):
    def _assert_law(self, result) -> None:
        self.assertGreater(result.hazard_trials, 0)
        self.assertGreater(result.naive_errors, 0)
        self.assertEqual(result.naive_errors, result.hazard_trials)
        self.assertEqual(result.guarded_errors, 0)
        self.assertGreater(result.guarded_benign_successes, 0)
        self.assertTrue(result.counterexample)

    def test_l1_representation_reality_separation_is_independently_necessary(self) -> None:
        self._assert_law(run_l1(5000, 0xA11CE))

    def test_l2_binding_is_independently_necessary(self) -> None:
        self._assert_law(run_l2(5000, 0xB1D1))

    def test_l3_partial_observation_is_independently_necessary(self) -> None:
        self._assert_law(run_l3(5000, 0x0B53))

    def test_l4_scoped_authority_is_independently_necessary(self) -> None:
        self._assert_law(run_l4(5000, 0xA07A))

    def test_l5_causal_noncollapse_is_independently_necessary(self) -> None:
        self._assert_law(run_l5(5000, 0xCA55A1))

    def test_physical_probes_reproduce_non_simulated_boundaries(self) -> None:
        probes = physical_probes()
        self.assertTrue(probes["L1"]["naiveSafe"])
        self.assertTrue(probes["L2"]["sameContentDigest"])
        self.assertTrue(probes["L3"]["staleWithoutEvent"])
        self.assertTrue(all(probes["L4"]["mechanicallyWritable"].values()))
        self.assertTrue(probes["L5"]["mechanicalSuccessWithoutSemanticSuccess"])

    def test_full_receipt_acceptance(self) -> None:
        receipt = run_all(5000)
        self.assertTrue(all(receipt["acceptance"].values()))
        self.assertTrue(receipt["receiptDigest"].startswith("sha256:"))


if __name__ == "__main__":
    unittest.main()
