from __future__ import annotations

import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from collections import defaultdict, deque
from dataclasses import replace
from pathlib import Path
from typing import Any

from anc_semantic_core.conformance import run_core_conformance, sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.journal import JournalConflict, JournalCorruption, JournalKernel
from anc_semantic_core.model import CapabilityRef, CompletionSemantics, EffectMode, WorldObjectRef
from anc_semantic_core.ordivon import (
    OrdivonExecution,
    OrdivonSemanticAdapter,
    ordivon_workspace_object_id,
)
from anc_semantic_core.kernel import InvalidTransition, NotFound
from anc_semantic_core.state import EffectState
from anc_semantic_core.transport import ToolTransportError


class ScriptedClient:
    def __init__(self) -> None:
        self.responses: dict[str, deque[dict[str, Any] | Exception]] = defaultdict(deque)
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def add(self, name: str, response: dict[str, Any] | Exception) -> None:
        self.responses[name].append(response)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((name, arguments))
        if not self.responses[name]:
            raise AssertionError(f"unexpected tool call: {name}")
        response = self.responses[name].popleft()
        if isinstance(response, Exception):
            raise response
        return response


def prepared_exec(kernel: JournalKernel, name: str) -> Any:
    base = sample_effect(name)
    target_id = ordivon_workspace_object_id("workspace-journal")
    spec = replace(
        base,
        target=WorldObjectRef(target_id),
        mode=EffectMode.CHANGE,
        operation="workspace.exec",
        capability=CapabilityRef(
            base.capability.principal_id,
            "workspace.exec",
            target_id,
        ),
        completion=CompletionSemantics.VERIFIED,
    )
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"{name}:admit"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"{name}:prepare"),
        recorded_at_ms=2,
    )
    return spec


class JournalKernelTests(unittest.TestCase):
    def test_reference_conformance_replays_through_journal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            kernels: list[JournalKernel] = []
            counter = 0

            def factory() -> JournalKernel:
                nonlocal counter
                counter += 1
                kernel = JournalKernel(Path(directory) / f"core-{counter}.sqlite3")
                kernels.append(kernel)
                return kernel

            try:
                run_core_conformance(factory)
                for kernel in kernels:
                    kernel.validate_invariants()
            finally:
                for kernel in kernels:
                    kernel.close()

    def test_reopen_rebuilds_projection_and_preserves_event_order(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "semantic.sqlite3"
            kernel = JournalKernel(path)
            spec = sample_effect("restart")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "restart:admit"),
                recorded_at_ms=10,
            )
            kernel.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, "restart:prepare"),
                recorded_at_ms=11,
            )
            dispatch_id = sid(IdKind.DISPATCH, "restart:dispatch")
            kernel.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=sid(IdKind.EVENT, "restart:started"),
                recorded_at_ms=12,
                request_digest="sha256:request",
            )
            kernel.mark_dispatch_unknown(
                spec.effect_id,
                dispatch_id,
                expected_revision=2,
                event_id=sid(IdKind.EVENT, "restart:unknown"),
                recorded_at_ms=13,
                evidence_digest="sha256:lost",
            )
            count = kernel.journal_entry_count
            kernel.close()

            reopened = JournalKernel(path)
            self.assertEqual(reopened.journal_entry_count, count)
            record = reopened.get_effect(spec.effect_id)
            self.assertIs(record.state, EffectState.UNKNOWN)
            self.assertEqual(record.revision, 3)
            self.assertEqual(
                [event.sequence for event in reopened.events_for(spec.effect_id)],
                [0, 1, 2, 3],
            )
            self.assertEqual(record.dispatch_id, dispatch_id)
            reopened.validate_invariants()
            reopened.close()

    def test_idempotent_existing_object_does_not_append_duplicate_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            kernel = JournalKernel(Path(directory) / "semantic.sqlite3")
            spec = sample_effect("idempotent-journal")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "idempotent:first"),
                recorded_at_ms=1,
            )
            self.assertEqual(kernel.journal_entry_count, 1)
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "idempotent:unused"),
                recorded_at_ms=1,
            )
            self.assertEqual(kernel.journal_entry_count, 1)
            kernel.close()

    def test_hash_chain_detects_tampered_entry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "semantic.sqlite3"
            kernel = JournalKernel(path)
            spec = sample_effect("tamper")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "tamper:admit"),
                recorded_at_ms=1,
            )
            kernel.close()
            connection = sqlite3.connect(path)
            connection.execute("DROP TRIGGER journal_entries_no_update")
            connection.execute(
                "UPDATE journal_entries SET payload_json = payload_json || ' ' WHERE sequence = 1"
            )
            connection.commit()
            connection.close()
            with self.assertRaisesRegex(JournalCorruption, "digest mismatch"):
                JournalKernel(path)

    def test_separate_process_can_rebuild_kernel(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "process.sqlite3"
            root = Path(__file__).resolve().parents[1]
            env = dict(os.environ)
            env["PYTHONPATH"] = str(root / "src")
            writer = """
from anc_semantic_core import JournalKernel
from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
import sys
k=JournalKernel(sys.argv[1]); s=sample_effect('process-restart')
k.admit_effect(s,event_id=sid(IdKind.EVENT,'process:admit'),recorded_at_ms=1)
k.prepare_effect(s.effect_id,expected_revision=0,event_id=sid(IdKind.EVENT,'process:prepare'),recorded_at_ms=2)
k.close()
"""
            reader = """
from anc_semantic_core import JournalKernel
from anc_semantic_core.conformance import sample_effect
import sys
k=JournalKernel(sys.argv[1]); s=sample_effect('process-restart')
r=k.get_effect(s.effect_id)
assert r.state.value == 'prepared' and r.revision == 1
assert [e.sequence for e in k.events_for(s.effect_id)] == [0,1]
k.validate_invariants(); print('process-rebuild-ok'); k.close()
"""
            subprocess.run([sys.executable, "-c", writer, str(path)], check=True, env=env)
            completed = subprocess.run(
                [sys.executable, "-c", reader, str(path)],
                check=True,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertIn("process-rebuild-ok", completed.stdout)

    def test_pending_job_correlation_survives_kernel_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "adapter.sqlite3"
            client = ScriptedClient()
            kernel = JournalKernel(path)
            spec = prepared_exec(kernel, "persistent-correlation")
            client.add(
                "workspace.exec",
                ToolTransportError("response lost after backend admission"),
            )
            first_adapter = OrdivonSemanticAdapter(
                kernel,
                client,
                clock_ms=iter(range(100, 160)).__next__,
            )
            first = first_adapter.dispatch_exec(
                spec.effect_id,
                OrdivonExecution("workspace-journal", "/usr/bin/true"),
            )
            self.assertIs(first.state, EffectState.UNKNOWN)
            dispatch_id = kernel.get_effect(spec.effect_id).dispatch_id
            client_request_id = client.calls[0][1]["clientRequestId"]
            kernel.close()

            client.add(
                "task.list",
                {
                    "jobs": [
                        {
                            "jobId": "job-persisted",
                            "attemptId": "attempt-persisted",
                            "clientRequestId": client_request_id,
                            "workspaceId": "workspace-journal",
                            "status": "working",
                        }
                    ]
                },
            )
            client.add(
                "task.observe",
                {
                    "jobId": "job-persisted",
                    "attemptId": "attempt-persisted",
                    "workspaceId": "workspace-journal",
                    "status": "succeeded",
                    "exitCode": 0,
                    "artifacts": [],
                },
            )
            reopened = JournalKernel(path)
            restarted_adapter = OrdivonSemanticAdapter(
                reopened,
                client,
                clock_ms=iter(range(160, 220)).__next__,
            )
            terminal = restarted_adapter.reconcile(spec.effect_id)
            self.assertIs(terminal.state, EffectState.SUCCEEDED)
            self.assertEqual(terminal.binding.dispatch_id, dispatch_id)
            self.assertEqual(
                [name for name, _ in client.calls].count("workspace.exec"),
                1,
            )
            reopened.validate_invariants()
            reopened.close()

    def test_failed_semantic_batch_appends_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "batch.sqlite3"
            kernel = JournalKernel(path)
            spec = sample_effect("journal-batch-rollback")
            with self.assertRaises(InvalidTransition):
                with kernel.transaction():
                    kernel.admit_effect(
                        spec,
                        event_id=sid(IdKind.EVENT, "journal-batch:admit"),
                        recorded_at_ms=1,
                    )
                    kernel.prepare_effect(
                        spec.effect_id,
                        expected_revision=0,
                        event_id=sid(IdKind.EVENT, "journal-batch:prepare"),
                        recorded_at_ms=2,
                    )
                    kernel.prepare_effect(
                        spec.effect_id,
                        expected_revision=1,
                        event_id=sid(IdKind.EVENT, "journal-batch:invalid"),
                        recorded_at_ms=3,
                    )
            self.assertEqual(kernel.journal_entry_count, 0)
            with self.assertRaises(NotFound):
                kernel.get_effect(spec.effect_id)
            kernel.close()
            reopened = JournalKernel(path)
            self.assertEqual(reopened.journal_entry_count, 0)
            reopened.validate_invariants()
            reopened.close()

    def test_stale_process_cannot_append_against_changed_journal_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "concurrent.sqlite3"
            first = JournalKernel(path)
            stale = JournalKernel(path)
            first_spec = sample_effect("first-writer")
            stale_spec = sample_effect("stale-writer")
            first.admit_effect(
                first_spec,
                event_id=sid(IdKind.EVENT, "first-writer:admit"),
                recorded_at_ms=1,
            )
            with self.assertRaises(JournalConflict):
                stale.admit_effect(
                    stale_spec,
                    event_id=sid(IdKind.EVENT, "stale-writer:admit"),
                    recorded_at_ms=1,
                )
            with self.assertRaises(NotFound):
                stale.get_effect(stale_spec.effect_id)
            self.assertEqual(stale.journal_entry_count, 1)
            first.close()
            stale.close()
            reopened = JournalKernel(path)
            self.assertEqual(reopened.get_effect(first_spec.effect_id).revision, 0)
            with self.assertRaises(NotFound):
                reopened.get_effect(stale_spec.effect_id)
            reopened.validate_invariants()
            reopened.close()

    def test_all_semantic_projections_rebuild_after_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "all-projections.sqlite3"
            kernel = JournalKernel(path)
            run_core_conformance(lambda: kernel)
            entry_count = kernel.journal_entry_count
            kernel.close()

            reopened = JournalKernel(path)
            self.assertEqual(reopened.journal_entry_count, entry_count)
            self.assertIs(
                reopened.get_effect(sid(IdKind.EFFECT, "effect:success")).state,
                EffectState.SUCCEEDED,
            )
            self.assertEqual(
                reopened.get_observation(
                    sid(IdKind.OBSERVATION, "observation:success")
                ).payload_digest,
                "sha256:payload",
            )
            self.assertEqual(
                reopened.get_artifact(
                    sid(IdKind.ARTIFACT, "artifact:success")
                ).digest,
                "sha256:artifact",
            )
            self.assertEqual(
                reopened.get_claim(sid(IdKind.CLAIM, "claim:success")).predicate,
                "content_digest_equals",
            )
            self.assertEqual(
                reopened.get_verification(
                    sid(IdKind.VERIFICATION, "verification:success")
                ).decision.value,
                "accepted",
            )
            self.assertEqual(
                reopened.get_fact(sid(IdKind.FACT, "fact:success")).claim_id,
                sid(IdKind.CLAIM, "claim:success"),
            )
            reopened.validate_invariants()
            reopened.close()

    def test_durable_head_detects_tail_truncation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "truncated.sqlite3"
            kernel = JournalKernel(path)
            spec = sample_effect("tail-truncation")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "tail:admit"),
                recorded_at_ms=1,
            )
            kernel.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, "tail:prepare"),
                recorded_at_ms=2,
            )
            kernel.close()
            connection = sqlite3.connect(path)
            connection.execute("DROP TRIGGER journal_entries_no_delete")
            connection.execute("DELETE FROM journal_entries WHERE sequence = 2")
            connection.commit()
            connection.close()
            with self.assertRaisesRegex(JournalCorruption, "durable head"):
                JournalKernel(path)

    def test_transaction_queries_see_staged_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "read-own-writes.sqlite3"
            kernel = JournalKernel(path)
            spec = sample_effect("read-own-writes")
            with kernel.transaction():
                kernel.admit_effect(
                    spec,
                    event_id=sid(IdKind.EVENT, "read-own-writes:admit"),
                    recorded_at_ms=1,
                )
                self.assertIs(
                    kernel.get_effect(spec.effect_id).state, EffectState.PROPOSED
                )
                kernel.prepare_effect(
                    spec.effect_id,
                    expected_revision=0,
                    event_id=sid(IdKind.EVENT, "read-own-writes:prepare"),
                    recorded_at_ms=2,
                )
                self.assertIs(
                    kernel.get_effect(spec.effect_id).state, EffectState.PREPARED
                )
            self.assertEqual(kernel.journal_entry_count, 2)
            self.assertIs(kernel.get_effect(spec.effect_id).state, EffectState.PREPARED)
            kernel.close()

    def test_journal_kernel_commits_successful_adapter_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "adapter-success.sqlite3"
            kernel = JournalKernel(path)
            spec = prepared_exec(kernel, "journal-adapter-success")
            client = ScriptedClient()
            client.add(
                "workspace.exec",
                {
                    "jobId": "job-journal-success",
                    "attemptId": "attempt-journal-success",
                    "workspaceId": "workspace-journal",
                    "status": "succeeded",
                    "exitCode": 0,
                    "artifacts": [
                        {
                            "artifactId": "stdout",
                            "kind": "stdout",
                            "digest": "sha256:stdout",
                            "retainedBytes": 12,
                        }
                    ],
                },
            )
            adapter = OrdivonSemanticAdapter(
                kernel,
                client,
                clock_ms=iter(range(500, 600)).__next__,
            )
            result = adapter.dispatch_exec(
                spec.effect_id,
                OrdivonExecution("workspace-journal", "/usr/bin/true"),
            )
            self.assertIs(result.state, EffectState.SUCCEEDED)
            self.assertIsNotNone(result.observation)
            self.assertEqual(len(result.artifacts), 1)
            observation_id = result.observation.observation_id
            artifact_id = result.artifacts[0].artifact_id
            kernel.validate_invariants()
            kernel.close()

            reopened = JournalKernel(path)
            self.assertIs(
                reopened.get_effect(spec.effect_id).state, EffectState.SUCCEEDED
            )
            self.assertEqual(
                reopened.get_observation(observation_id).effect_id, spec.effect_id
            )
            self.assertEqual(
                reopened.get_artifact(artifact_id).digest, "sha256:stdout"
            )
            reopened.validate_invariants()
            reopened.close()

    def test_nonempty_journal_without_head_metadata_is_corruption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing-head.sqlite3"
            kernel = JournalKernel(path)
            spec = sample_effect("missing-head")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "missing-head:admit"),
                recorded_at_ms=1,
            )
            kernel.close()
            connection = sqlite3.connect(path)
            connection.execute(
                "DELETE FROM journal_metadata "
                "WHERE key IN ('head_sequence', 'head_digest')"
            )
            connection.commit()
            connection.close()
            with self.assertRaisesRegex(JournalCorruption, "no durable head"):
                JournalKernel(path)


if __name__ == "__main__":
    unittest.main()
