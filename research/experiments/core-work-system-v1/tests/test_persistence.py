from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from anc_core_work_system.persistence import JsonStateStore, LangGraphStateStore, TranscriptSummaryStore
from anc_core_work_system.scenario import ScenarioMachine
from anc_core_work_system.world import freeze_fixture, prepare_trial_world


class PersistenceTests(unittest.TestCase):
    def _checkpoint(self, temporary: str):
        fixture = Path(temporary) / "fixture"
        freeze_fixture(fixture)
        world = prepare_trial_world(fixture, Path(temporary) / "trial")
        machine = ScenarioMachine(world)
        state = machine.failed_attempt(world.initial_state())
        state = machine.revise_world_goal_and_catalog(state)
        return machine, machine.commit_with_lost_response(state)

    def test_typed_state_detects_and_recovers_exact_checkpoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, checkpoint = self._checkpoint(temporary)
            path = Path(temporary) / "typed.json"
            JsonStateStore(path).save(checkpoint)
            self.assertEqual(JsonStateStore(path).load().digest, checkpoint.digest)

    def test_langgraph_sqlite_recovers_pending_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, checkpoint = self._checkpoint(temporary)
            path = Path(temporary) / "graph.sqlite3"
            store = LangGraphStateStore(path, thread_id=checkpoint.task_id)
            store.save(checkpoint)
            store.close()
            fresh = LangGraphStateStore(path, thread_id=checkpoint.task_id)
            recovered = fresh.load()
            fresh.close()
            self.assertEqual(recovered.pending_operations, checkpoint.pending_operations)

    def test_bounded_summary_fault_omits_unknown_operation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            machine, checkpoint = self._checkpoint(temporary)
            store = TranscriptSummaryStore(Path(temporary) / "summary", omit_pending_on_summary=True)
            store.save(checkpoint, machine.events)
            self.assertFalse(store.load_for_resume().pending_operations)


if __name__ == "__main__":
    unittest.main()
