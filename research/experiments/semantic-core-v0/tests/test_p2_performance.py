from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest import mock

from anc_semantic_core.bootstrap import issue_authority_views
from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.errors import InvariantViolation, NotFound
from anc_semantic_core.identity import IdKind
from anc_semantic_core.journal import (
    JOURNAL_SCHEMA_VERSION,
    JournalReducer,
    _GENESIS_DIGEST,
    _entry_digest,
)
from anc_semantic_core.model import (
    CapabilityRef,
    IdempotencyKind,
    Precondition,
)
from anc_semantic_core.reducer import ReferenceReducer
from anc_semantic_core.testing import test_authority_policy


class P2PerformanceTests(unittest.TestCase):
    def _journal(self, path: Path, namespace: str = "p2"):
        policy = test_authority_policy()
        reducer = JournalReducer(path, policy)
        return reducer, issue_authority_views(reducer, policy, namespace=namespace)

    def _reference(self, namespace: str = "p2-reference"):
        policy = test_authority_policy()
        reducer = ReferenceReducer(policy)
        return reducer, issue_authority_views(reducer, policy, namespace=namespace)

    @staticmethod
    def _admit_and_prepare(views, name: str, start: int = 1):
        spec = sample_effect(name)
        views.effects.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"event:{name}:0"),
            recorded_at_ms=start,
        )
        views.effects.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"event:{name}:1"),
            recorded_at_ms=start + 1,
        )
        return spec

    def test_inactive_model_fields_are_rejected_for_new_effects(self) -> None:
        base = sample_effect("p2-slim")
        with self.assertRaisesRegex(ValueError, "preconditions"):
            replace(
                base,
                preconditions=(
                    Precondition(base.target, "free text is not executable"),
                ),
            )
        with self.assertRaisesRegex(ValueError, "Task and Attempt"):
            replace(base, parent_task_id=sid(IdKind.TASK, "task:p2"))
        with self.assertRaisesRegex(ValueError, "keyed idempotency"):
            replace(base, idempotency=IdempotencyKind.KEYED)
        with self.assertRaisesRegex(ValueError, "expiry"):
            replace(
                base,
                capability=CapabilityRef(
                    base.capability.principal_id,
                    base.capability.operation,
                    base.capability.object_scope,
                    valid_until_ms=10,
                ),
            )

    def test_command_hot_path_does_not_snapshot_complete_state(self) -> None:
        reducer, views = self._reference("p2-no-snapshot")
        with mock.patch.object(
            reducer, "_snapshot", side_effect=AssertionError("hot path snapshot")
        ):
            self._admit_and_prepare(views, "p2-no-snapshot")
        reducer.validate_invariants()

    def test_journal_hot_path_does_not_clone_reducer(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reducer, views = self._journal(
                Path(directory) / "no-clone.sqlite3", "p2-no-clone"
            )
            with mock.patch.object(
                ReferenceReducer, "clone", side_effect=AssertionError("journal clone")
            ):
                self._admit_and_prepare(views, "p2-no-clone")
            reducer.validate_invariants()
            reducer.close()

    def test_append_failure_rolls_back_in_memory_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            reducer, views = self._journal(
                Path(directory) / "append-failure.sqlite3", "p2-append-failure"
            )
            spec = sample_effect("p2-append-failure")
            with mock.patch.object(
                reducer._journal, "append", side_effect=OSError("disk unavailable")
            ):
                with self.assertRaisesRegex(OSError, "disk unavailable"):
                    views.effects.admit_effect(
                        spec,
                        event_id=sid(IdKind.EVENT, "event:p2-append-failure:0"),
                        recorded_at_ms=1,
                    )
            with self.assertRaises(NotFound):
                views.read.get_effect(spec.effect_id)
            self.assertEqual(reducer.journal_entry_count, 0)
            reducer.close()

    def test_full_audit_still_detects_cross_projection_corruption(self) -> None:
        reducer, views = self._reference("p2-audit")
        spec = self._admit_and_prepare(views, "p2-audit")
        reducer._effects[spec.effect_id] = replace(
            reducer.get_effect(spec.effect_id), revision=9
        )
        with self.assertRaisesRegex(InvariantViolation, "event/revision mismatch"):
            reducer.validate_invariants()

    def test_v2_journal_migrates_and_new_tail_uses_v3_commands(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy-v2.sqlite3"
            reducer, views = self._journal(path, "p2-v2-writer")
            spec = sample_effect("p2-v2")
            views.effects.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "event:p2-v2:0"),
                recorded_at_ms=1,
            )
            reducer.close()

            connection = sqlite3.connect(path)
            connection.execute("DROP TRIGGER journal_entries_no_update")
            row = connection.execute(
                "SELECT payload_json FROM journal_entries WHERE sequence = 1"
            ).fetchone()
            payload = json.loads(row[0])
            payload["schemaVersion"] = 2
            payload_json = json.dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            )
            digest = _entry_digest(_GENESIS_DIGEST, payload_json)
            connection.execute(
                """
                UPDATE journal_entries
                SET payload_json = ?, previous_digest = ?, entry_digest = ?
                WHERE sequence = 1
                """,
                (payload_json, _GENESIS_DIGEST, digest),
            )
            connection.execute(
                "UPDATE journal_metadata SET value = '2' WHERE key = 'schema_version'"
            )
            connection.execute(
                "UPDATE journal_metadata SET value = 'semantic-core-v2-authority' "
                "WHERE key = 'semantic_model_version'"
            )
            connection.execute(
                "UPDATE journal_metadata SET value = 'reference-reducer-v2' "
                "WHERE key = 'reducer_version'"
            )
            connection.execute(
                "UPDATE journal_metadata SET value = ? WHERE key = 'head_digest'",
                (digest,),
            )
            connection.commit()
            connection.close()

            migrated, migrated_views = self._journal(path, "p2-v2-reader")
            self.assertEqual(migrated_views.read.get_effect(spec.effect_id).revision, 0)
            migrated_views.effects.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, "event:p2-v2:1"),
                recorded_at_ms=2,
            )
            migrated.close()
            connection = sqlite3.connect(path)
            schema = connection.execute(
                "SELECT value FROM journal_metadata WHERE key = 'schema_version'"
            ).fetchone()[0]
            command_versions = [
                json.loads(row[0])["schemaVersion"]
                for row in connection.execute(
                    "SELECT payload_json FROM journal_entries ORDER BY sequence"
                ).fetchall()
            ]
            connection.close()
            self.assertEqual(schema, str(JOURNAL_SCHEMA_VERSION))
            self.assertEqual(command_versions, [2, 3])


if __name__ == "__main__":
    unittest.main()
