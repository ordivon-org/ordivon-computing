from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from anc_core_work_system.world import freeze_fixture, prepare_trial_world


class WorldTests(unittest.TestCase):
    def test_frozen_fixture_contains_no_nested_git_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "fixture"
            manifest = freeze_fixture(fixture)
            self.assertFalse(any(path.name == ".git" for path in fixture.rglob(".git")))
            trial = prepare_trial_world(fixture, Path(temporary) / "trial")
            self.assertEqual(trial.current_revision(), manifest.initial_revision)
            trial.apply_concurrent_revision()
            self.assertEqual(trial.current_revision(), manifest.concurrent_revision)

    def test_response_loss_backend_can_be_reconciled_by_request(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary) / "fixture"
            manifest = freeze_fixture(fixture)
            world = prepare_trial_world(fixture, Path(temporary) / "trial")
            world.apply_concurrent_revision()
            world.set_catalog_v2()
            world.execute_maintenance_effect(
                effect_id="effect:test",
                request_id="request:test",
                expected_revision=manifest.concurrent_revision,
                expected_catalog_digest=manifest.catalog_v2_digest,
            )
            self.assertIsNotNone(world.lookup_request("request:test"))
            self.assertEqual(world.grade_repository()["duplicateWorldEffects"], 0)


if __name__ == "__main__":
    unittest.main()
