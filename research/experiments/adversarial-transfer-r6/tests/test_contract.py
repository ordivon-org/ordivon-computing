from __future__ import annotations

import unittest

from anc_adversarial_transfer.runner import ATTACKS, MODELS, PROFILES, _trial_plan


class R6ContractTests(unittest.TestCase):
    def test_default_plan_has_flash_full_matrix_and_pro_two_profiles(self) -> None:
        plan = _trial_plan(attacks=ATTACKS, profiles=PROFILES, models=MODELS)
        self.assertEqual(len(plan), 28)
        self.assertEqual(len({item.trial_id for item in plan}), 28)
        flash = [item for item in plan if item.model == "deepseek-v4-flash"]
        pro = [item for item in plan if item.model == "deepseek-v4-pro"]
        self.assertEqual(len(flash), 20)
        self.assertEqual(len(pro), 8)
        self.assertEqual({item.profile for item in pro}, {"raw-ambient", "harness-gated"})

    def test_output_paths_are_trial_unique_and_fixture_local(self) -> None:
        plan = _trial_plan(attacks=ATTACKS, profiles=PROFILES, models=("deepseek-v4-flash",))
        paths = {item.output_path for item in plan}
        self.assertEqual(len(paths), len(plan))
        self.assertTrue(all("adversarial-transfer-r6/fixture/output/" in item for item in paths))


if __name__ == "__main__":
    unittest.main()
