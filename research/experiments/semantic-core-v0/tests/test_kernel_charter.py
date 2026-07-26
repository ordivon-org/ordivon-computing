from __future__ import annotations

import sqlite3
import tempfile
import unittest
from anc_semantic_core.testing import journal_kernel, reference_kernel
from collections import defaultdict, deque
from dataclasses import replace
from pathlib import Path
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.journal import JournalCorruption
from anc_semantic_core.kernel import IdentityConflict, NotFound
from anc_semantic_core.model import (
    CapabilityRef,
    Claim,
    CompletionSemantics,
    DispatchState,
    EffectMode,
    Fact,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import (
    OrdivonExecution,
    OrdivonSemanticAdapter,
    ordivon_workspace_object_id,
)
from anc_semantic_core.state import EffectState
from anc_semantic_core.transport import ToolRejected, ToolTransportError


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


def prepared_exec(kernel: Any, name: str) -> Any:
    base = sample_effect(name)
    target_id = ordivon_workspace_object_id("workspace-charter")
    spec = replace(
        base,
        target=WorldObjectRef(target_id),
        mode=EffectMode.CHANGE,
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


class KernelCharterConformanceTests(unittest.TestCase):
    def test_k1_identity_survives_journal_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "identity.sqlite3"
            kernel = journal_kernel(path)
            spec = sample_effect("charter-k1")
            dispatch_id = sid(IdKind.DISPATCH, "charter-k1:dispatch")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "charter-k1:admit"),
                recorded_at_ms=1,
            )
            kernel.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, "charter-k1:prepare"),
                recorded_at_ms=2,
            )
            kernel.begin_dispatch(
                spec.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=sid(IdKind.EVENT, "charter-k1:started"),
                recorded_at_ms=3,
                request_digest="sha256:k1-request",
            )
            kernel.mark_dispatch_unknown(
                spec.effect_id,
                dispatch_id,
                expected_revision=2,
                event_id=sid(IdKind.EVENT, "charter-k1:unknown"),
                recorded_at_ms=4,
                evidence_digest="sha256:k1-response-loss",
            )
            kernel.close()

            reopened = journal_kernel(path)
            self.assertEqual(reopened.get_effect(spec.effect_id).spec.effect_id, spec.effect_id)
            self.assertEqual(reopened.get_effect(spec.effect_id).dispatch_id, dispatch_id)
            self.assertEqual(reopened.get_dispatch(dispatch_id).effect_id, spec.effect_id)
            self.assertIs(reopened.get_effect(spec.effect_id).state, EffectState.UNKNOWN)
            reopened.validate_invariants()
            reopened.close()

    def test_k2_dispatch_identity_cannot_cross_effects(self) -> None:
        kernel = reference_kernel()
        first = sample_effect("charter-k2-first")
        second = sample_effect("charter-k2-second")
        for index, spec in enumerate((first, second), start=1):
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, f"charter-k2:{index}:admit"),
                recorded_at_ms=index,
            )
            kernel.prepare_effect(
                spec.effect_id,
                expected_revision=0,
                event_id=sid(IdKind.EVENT, f"charter-k2:{index}:prepare"),
                recorded_at_ms=index + 2,
            )
        dispatch_id = sid(IdKind.DISPATCH, "charter-k2:shared-dispatch")
        kernel.begin_dispatch(
            first.effect_id,
            expected_revision=1,
            dispatch_id=dispatch_id,
            event_id=sid(IdKind.EVENT, "charter-k2:first-started"),
            recorded_at_ms=5,
            request_digest="sha256:first-request",
        )
        second_before = kernel.get_effect(second.effect_id)
        with self.assertRaises(IdentityConflict):
            kernel.begin_dispatch(
                second.effect_id,
                expected_revision=1,
                dispatch_id=dispatch_id,
                event_id=sid(IdKind.EVENT, "charter-k2:second-started"),
                recorded_at_ms=6,
                request_digest="sha256:second-request",
            )
        self.assertEqual(kernel.get_effect(second.effect_id), second_before)
        self.assertEqual(kernel.get_dispatch(dispatch_id).effect_id, first.effect_id)
        kernel.validate_invariants()

    def test_k3_transport_loss_is_unknown_not_failed(self) -> None:
        kernel = reference_kernel()
        spec = prepared_exec(kernel, "charter-k3")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            ToolTransportError("response lost after possible delivery"),
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(10, 100)).__next__,
        )
        result = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-charter", "/usr/bin/true"),
        )
        dispatch_id = kernel.get_effect(spec.effect_id).dispatch_id
        self.assertIs(result.state, EffectState.UNKNOWN)
        self.assertIsNotNone(dispatch_id)
        self.assertIs(kernel.get_dispatch(dispatch_id).state, DispatchState.UNKNOWN)
        self.assertNotEqual(result.state, EffectState.FAILED)
        kernel.validate_invariants()

    def test_k4_reconciliation_reuses_original_dispatch(self) -> None:
        kernel = reference_kernel()
        spec = prepared_exec(kernel, "charter-k4")
        client = ScriptedClient()
        client.add("workspace.exec", ToolTransportError("response lost"))
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(100, 200)).__next__,
        )
        first = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-charter", "/usr/bin/true"),
        )
        self.assertIs(first.state, EffectState.UNKNOWN)
        original_dispatch = kernel.get_effect(spec.effect_id).dispatch_id
        client_request_id = client.calls[0][1]["clientRequestId"]
        client.add(
            "task.list",
            {
                "jobs": [
                    {
                        "jobId": "job-charter-k4",
                        "attemptId": "attempt-charter-k4",
                        "clientRequestId": client_request_id,
                        "workspaceId": "workspace-charter",
                        "status": "working",
                    }
                ]
            },
        )
        client.add(
            "task.observe",
            {
                "jobId": "job-charter-k4",
                "attemptId": "attempt-charter-k4",
                "workspaceId": "workspace-charter",
                "status": "succeeded",
                "exitCode": 0,
                "artifacts": [],
            },
        )
        recovered = adapter.reconcile(spec.effect_id)
        self.assertIs(recovered.state, EffectState.SUCCEEDED)
        self.assertEqual(recovered.binding.dispatch_id, original_dispatch)
        self.assertEqual(
            [name for name, _ in client.calls].count("workspace.exec"),
            1,
        )
        kernel.validate_invariants()

    def test_k5_cancel_request_is_not_terminal_cancellation(self) -> None:
        kernel = reference_kernel()
        spec = prepared_exec(kernel, "charter-k5")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            {
                "jobId": "job-charter-k5",
                "attemptId": "attempt-charter-k5",
                "workspaceId": "workspace-charter",
                "status": "working",
                "artifacts": [],
            },
        )
        client.add(
            "task.cancel",
            ToolRejected(
                "task.cancel",
                code="TEMPORARY_CONFLICT",
                message="cancellation has not reached a terminal outcome",
                retryable=True,
            ),
        )
        client.add(
            "task.observe",
            {
                "jobId": "job-charter-k5",
                "attemptId": "attempt-charter-k5",
                "workspaceId": "workspace-charter",
                "status": "working",
                "artifacts": [],
            },
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(200, 300)).__next__,
        )
        running = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-charter", "/usr/bin/sleep", ("10",)),
        )
        self.assertIs(running.state, EffectState.RUNNING)
        pending = adapter.cancel(spec.effect_id)
        self.assertIs(pending.state, EffectState.CANCEL_REQUESTED)
        self.assertNotEqual(pending.state, EffectState.CANCELLED)
        kernel.validate_invariants()

    def test_k6_observation_cannot_bypass_verification(self) -> None:
        kernel = reference_kernel()
        spec = prepared_exec(kernel, "charter-k6")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            {
                "jobId": "job-charter-k6",
                "attemptId": "attempt-charter-k6",
                "workspaceId": "workspace-charter",
                "status": "succeeded",
                "exitCode": 0,
                "artifacts": [],
            },
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(300, 400)).__next__,
        )
        result = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-charter", "/usr/bin/true"),
        )
        self.assertIsNotNone(result.observation)
        claim = Claim(
            claim_id=sid(IdKind.CLAIM, "charter-k6:claim"),
            origin_effect_id=spec.effect_id,
            subject=spec.target,
            predicate="tool_succeeded",
            value_digest=result.observation.payload_digest,
        )
        kernel.admit_claim(claim)
        fact = Fact(
            fact_id=sid(IdKind.FACT, "charter-k6:fact"),
            claim_id=claim.claim_id,
            verification_id=sid(IdKind.VERIFICATION, "charter-k6:missing-verification"),
            accepted_at_ms=500,
        )
        with self.assertRaises(NotFound):
            kernel.commit_fact(fact)
        with self.assertRaises(NotFound):
            kernel.get_fact(fact.fact_id)
        kernel.validate_invariants()

    def test_k7_failed_admission_restores_all_projections(self) -> None:
        kernel = reference_kernel()
        spec = sample_effect("charter-k7")
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, "charter-k7:admit"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "charter-k7:prepare"),
            recorded_at_ms=2,
        )
        dispatch_id = sid(IdKind.DISPATCH, "charter-k7:dispatch")
        started_event = sid(IdKind.EVENT, "charter-k7:started")
        kernel.begin_dispatch(
            spec.effect_id,
            expected_revision=1,
            dispatch_id=dispatch_id,
            event_id=started_event,
            recorded_at_ms=3,
            request_digest="sha256:k7-request",
        )
        before = kernel.state_snapshot()
        with self.assertRaises(IdentityConflict):
            kernel.admit_dispatch(
                spec.effect_id,
                dispatch_id,
                expected_revision=2,
                event_id=started_event,
                recorded_at_ms=4,
                backend_operation_id="job-charter-k7",
                evidence_digest="sha256:k7-admission",
            )
        self.assertEqual(kernel.state_snapshot(), before)
        self.assertIs(kernel.get_dispatch(dispatch_id).state, DispatchState.STARTED)
        kernel.validate_invariants()

    def test_k8_corrupt_durable_history_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "corrupt.sqlite3"
            kernel = journal_kernel(path)
            spec = sample_effect("charter-k8")
            kernel.admit_effect(
                spec,
                event_id=sid(IdKind.EVENT, "charter-k8:admit"),
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

            with self.assertRaises(JournalCorruption):
                journal_kernel(path)

    def test_charter_documents_bind_every_guarantee_to_evidence(self) -> None:
        root = Path(__file__).resolve().parents[1]
        charter = (root / "KERNEL-CHARTER.md").read_text()
        conformance = (root / "CONFORMANCE.md").read_text()
        canonical_tests = {
            "K1": "test_k1_identity_survives_journal_restart",
            "K2": "test_k2_dispatch_identity_cannot_cross_effects",
            "K3": "test_k3_transport_loss_is_unknown_not_failed",
            "K4": "test_k4_reconciliation_reuses_original_dispatch",
            "K5": "test_k5_cancel_request_is_not_terminal_cancellation",
            "K6": "test_k6_observation_cannot_bypass_verification",
            "K7": "test_k7_failed_admission_restores_all_projections",
            "K8": "test_k8_corrupt_durable_history_fails_closed",
            "K9": "test_role_specific_signer_cannot_escalate_to_another_role",
            "K10": "test_attestation_provenance_survives_journal_replay",
            "K11": "test_same_semantic_contract_runs_against_two_backends",
            "K12": "test_k12_effect_binding_separation_survives_journal_restart",
        }
        test_sources = "\n".join(
            path.read_text() for path in (root / "tests").glob("test_*.py")
        )
        for guarantee_id, test_name in canonical_tests.items():
            self.assertIn(f"### {guarantee_id} —", charter)
            self.assertIn(test_name, conformance)
            self.assertIn(f"def {test_name}", test_sources)


if __name__ == "__main__":
    unittest.main()
