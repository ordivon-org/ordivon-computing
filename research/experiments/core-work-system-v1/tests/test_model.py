from __future__ import annotations

import unittest

from anc_core_work_system.model import WorkState
from anc_core_work_system.world import CATALOG_V1
from anc_core_work_system.model import canonical_digest


class ModelTests(unittest.TestCase):
    def test_work_state_round_trip_preserves_digest(self) -> None:
        state = WorkState(
            task_id="task:test",
            goal_revision=1,
            goal_statement="Test durable state.",
            repository_revision="0" * 40,
            catalog_digest=canonical_digest(CATALOG_V1),
            frontier=("next",),
        )
        decoded = WorkState.from_dict(state.to_dict())
        self.assertEqual(decoded, state)
        self.assertEqual(decoded.digest, state.digest)

    def test_work_state_rejects_duplicate_effects(self) -> None:
        with self.assertRaises(ValueError):
            WorkState(
                task_id="task:test",
                goal_revision=1,
                goal_statement="Reject duplicate Effects.",
                repository_revision="0" * 40,
                catalog_digest=canonical_digest(CATALOG_V1),
                frontier=("next",),
                completed_effects=("effect:one", "effect:one"),
            )


if __name__ == "__main__":
    unittest.main()
