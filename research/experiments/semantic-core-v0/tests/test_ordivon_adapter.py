from __future__ import annotations

import unittest
from collections import defaultdict, deque
from dataclasses import replace
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.kernel import InvalidTransition, ReferenceKernel
from anc_semantic_core.transport import ToolRejected, ToolTransportError
from anc_semantic_core.model import (
    CapabilityRef,
    CompletionSemantics,
    DispatchState,
    EffectMode,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import (
    OrdivonExecution,
    OrdivonFileMutation,
    OrdivonMutationMode,
    OrdivonRead,
    OrdivonReadMode,
    OrdivonSemanticAdapter,
    ordivon_file_object_id,
    ordivon_workspace_object_id,
    semantic_state_from_status,
)
from anc_semantic_core.state import EffectState


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


def prepared_operation(
    kernel: ReferenceKernel,
    name: str,
    operation: str,
    mode: EffectMode,
    *,
    workspace_id: str = "workspace-test",
    relative_path: str | None = None,
) -> Any:
    base = sample_effect(name)
    if operation == "workspace.exec":
        target_id = ordivon_workspace_object_id(workspace_id)
    else:
        if relative_path is None:
            raise ValueError("file operation fixture requires relative_path")
        target_id = ordivon_file_object_id(workspace_id, relative_path)
    spec = replace(
        base,
        target=WorldObjectRef(target_id),
        mode=mode,
        operation=operation,
        capability=CapabilityRef(
            base.capability.principal_id,
            operation,
            target_id,
        ),
        completion=CompletionSemantics.VERIFIED,
    )
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"event:{name}:admit"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"event:{name}:prepare"),
        recorded_at_ms=2,
    )
    return spec


def prepared_exec(kernel: ReferenceKernel, name: str) -> Any:
    return prepared_operation(kernel, name, "workspace.exec", EffectMode.CHANGE)


class OrdivonAdapterTests(unittest.TestCase):
    def test_public_status_projection_preserves_uncertainty(self) -> None:
        self.assertIs(semantic_state_from_status("queued"), EffectState.DISPATCHED)
        self.assertIs(semantic_state_from_status("working"), EffectState.RUNNING)
        self.assertIs(semantic_state_from_status("succeeded"), EffectState.SUCCEEDED)
        self.assertIs(semantic_state_from_status("failed"), EffectState.FAILED)
        self.assertIs(semantic_state_from_status("timed_out"), EffectState.FAILED)
        self.assertIs(semantic_state_from_status("cancelled"), EffectState.CANCELLED)
        self.assertIs(semantic_state_from_status("lost"), EffectState.UNKNOWN)
        self.assertIs(semantic_state_from_status("orphaned"), EffectState.UNKNOWN)

    def test_effect_target_must_match_execution_workspace(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_operation(
            kernel,
            "ordivon-target",
            "workspace.exec",
            EffectMode.CHANGE,
            workspace_id="workspace-a",
        )
        client = ScriptedClient()
        adapter = OrdivonSemanticAdapter(kernel, client)
        with self.assertRaisesRegex(ValueError, "target does not match"):
            adapter.dispatch_exec(
                spec.effect_id,
                OrdivonExecution("workspace-b", "/usr/bin/true"),
            )
        self.assertEqual(client.calls, [])
        self.assertIs(kernel.get_effect(spec.effect_id).state, EffectState.PREPARED)

    def test_workspace_read_projects_versioned_observation(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_operation(
            kernel,
            "ordivon-read",
            "workspace.read",
            EffectMode.OBSERVE,
            relative_path="README.md",
        )
        client = ScriptedClient()
        client.add(
            "workspace.read",
            {
                "content": "hello\n",
                "digest": "sha256:file-digest",
                "eof": True,
                "fileByteLength": 6,
            },
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(5, 100)).__next__,
        )
        result = adapter.read_file(
            spec.effect_id,
            OrdivonRead(
                "workspace-test",
                "README.md",
                mode=OrdivonReadMode.SLICE,
                max_bytes=1024,
            ),
        )
        self.assertIs(result.state, EffectState.SUCCEEDED)
        self.assertEqual(result.observation.target.version, "sha256:file-digest")
        self.assertEqual(client.calls[0][0], "workspace.read")
        self.assertEqual(client.calls[0][1]["relativePath"], "README.md")
        kernel.validate_invariants()

    def test_identical_reads_keep_distinct_causal_observation_identity(self) -> None:
        kernel = ReferenceKernel()
        first = prepared_operation(
            kernel,
            "ordivon-read-first",
            "workspace.read",
            EffectMode.OBSERVE,
            relative_path="same.txt",
        )
        second_base = sample_effect("ordivon-read-second")
        second = replace(
            second_base,
            target=first.target,
            mode=EffectMode.OBSERVE,
            operation="workspace.read",
            capability=CapabilityRef(
                second_base.capability.principal_id,
                "workspace.read",
                first.target.object_id,
            ),
            completion=CompletionSemantics.VERIFIED,
        )
        kernel.admit_effect(
            second,
            event_id=sid(IdKind.EVENT, "event:ordivon-read-second:admit"),
            recorded_at_ms=1,
        )
        kernel.prepare_effect(
            second.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, "event:ordivon-read-second:prepare"),
            recorded_at_ms=2,
        )
        payload = {
            "content": "same\n",
            "digest": "sha256:same",
        }
        client = ScriptedClient()
        client.add("workspace.read", dict(payload))
        client.add("workspace.read", dict(payload))
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(5, 100)).__next__,
        )
        first_result = adapter.read_file(
            first.effect_id,
            OrdivonRead("workspace-test", "same.txt"),
        )
        second_result = adapter.read_file(
            second.effect_id,
            OrdivonRead("workspace-test", "same.txt"),
        )
        self.assertEqual(
            first_result.observation.payload_digest,
            second_result.observation.payload_digest,
        )
        self.assertNotEqual(
            first_result.observation.observation_id,
            second_result.observation.observation_id,
        )
        kernel.validate_invariants()

    def test_workspace_mutation_projects_after_digest(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_operation(
            kernel,
            "ordivon-mutate",
            "workspace.mutate",
            EffectMode.CHANGE,
            relative_path="result.txt",
        )
        client = ScriptedClient()
        client.add(
            "workspace.mutate",
            {
                "mutations": [
                    {
                        "relativePath": "result.txt",
                        "afterDigest": "sha256:after",
                        "byteLength": 6,
                    }
                ]
            },
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(5, 100)).__next__,
        )
        result = adapter.mutate_file(
            spec.effect_id,
            OrdivonFileMutation(
                "workspace-test",
                "result.txt",
                OrdivonMutationMode.REPLACE_EXACT,
                content="after",
                expected_digest="sha256:before",
                expected_text="before",
            ),
        )
        self.assertIs(result.state, EffectState.SUCCEEDED)
        self.assertEqual(result.observation.target.version, "sha256:after")
        mutation = client.calls[0][1]["mutations"][0]
        self.assertEqual(mutation["expectedDigest"], "sha256:before")
        self.assertEqual(mutation["expectedText"], "before")
        kernel.validate_invariants()

    def test_workspace_mutation_response_loss_is_unknown_and_not_repeated(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_operation(
            kernel,
            "ordivon-mutate-loss",
            "workspace.mutate",
            EffectMode.CHANGE,
            relative_path="result.txt",
        )
        client = ScriptedClient()
        client.add(
            "workspace.mutate",
            ToolTransportError("response lost after delivery"),
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(5, 100)).__next__,
        )
        mutation = OrdivonFileMutation(
            "workspace-test",
            "result.txt",
            OrdivonMutationMode.WRITE,
            content="value\n",
        )
        result = adapter.mutate_file(spec.effect_id, mutation)
        self.assertIs(result.state, EffectState.UNKNOWN)
        with self.assertRaises(InvalidTransition):
            adapter.mutate_file(spec.effect_id, mutation)
        self.assertEqual(
            [name for name, _ in client.calls].count("workspace.mutate"),
            1,
        )
        kernel.validate_invariants()

    def test_successful_job_projects_observation_and_artifacts(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_exec(kernel, "ordivon-success")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            {
                "jobId": "job-success",
                "attemptId": "attempt-success",
                "workspaceId": "workspace-test",
                "status": "succeeded",
                "exitCode": 0,
                "artifactsAvailable": True,
                "artifacts": [
                    {
                        "artifactId": "result",
                        "kind": "execution_result",
                        "digest": "sha256:artifact",
                        "retainedBytes": 42,
                        "truncated": False,
                    }
                ],
            },
        )
        adapter = OrdivonSemanticAdapter(kernel, client, clock_ms=iter(range(10, 100)).__next__)
        result = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(result.state, EffectState.SUCCEEDED)
        self.assertEqual(result.binding.job_id, "job-success")
        self.assertEqual(len(result.artifacts), 1)
        self.assertIsNotNone(result.observation)
        kernel.validate_invariants()
        with self.assertRaises(InvalidTransition):
            adapter.dispatch_exec(
                spec.effect_id,
                OrdivonExecution("workspace-test", "/usr/bin/true"),
            )
        self.assertEqual(
            [name for name, _ in client.calls].count("workspace.exec"),
            1,
        )

    def test_running_job_can_be_observed_to_terminal_without_reconcile(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_exec(kernel, "ordivon-running")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            {
                "jobId": "job-running",
                "attemptId": "attempt-running",
                "workspaceId": "workspace-test",
                "status": "working",
                "artifacts": [],
            },
        )
        client.add(
            "task.observe",
            {
                "jobId": "job-running",
                "attemptId": "attempt-running",
                "status": "succeeded",
                "exitCode": 0,
                "artifacts": [],
            },
        )
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(15, 100)).__next__,
        )
        first = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(first.state, EffectState.RUNNING)
        terminal = adapter.observe(spec.effect_id, wait_ms=30_000)
        self.assertIs(terminal.state, EffectState.SUCCEEDED)
        self.assertEqual(
            [name for name, _ in client.calls],
            ["workspace.exec", "task.observe"],
        )
        kernel.validate_invariants()

    def test_response_loss_reconciles_without_redispatch(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_exec(kernel, "ordivon-response-loss")
        client = ScriptedClient()
        client.add("workspace.exec", ToolTransportError("response lost after delivery"))
        client.add(
            "task.list",
            {
                "jobs": [
                    {
                        "jobId": "job-recovered",
                        "attemptId": "attempt-recovered",
                        "workspaceId": "workspace-test",
                        "clientRequestId": "anc-effect-9553c914c1746ffc33c901f1def35132",
                        "status": "working",
                    }
                ]
            },
        )
        client.add(
            "task.observe",
            {
                "jobId": "job-recovered",
                "attemptId": "attempt-recovered",
                "status": "succeeded",
                "exitCode": 0,
                "artifacts": [],
            },
        )
        adapter = OrdivonSemanticAdapter(kernel, client, clock_ms=iter(range(20, 100)).__next__)
        first = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(first.state, EffectState.UNKNOWN)
        expected_client_request_id = client.calls[0][1]["clientRequestId"]
        client.responses["task.list"][0]["jobs"][0][
            "clientRequestId"
        ] = expected_client_request_id
        recovered = adapter.reconcile(spec.effect_id)
        self.assertIs(recovered.state, EffectState.SUCCEEDED)
        self.assertEqual(recovered.binding.job_id, "job-recovered")
        self.assertEqual(
            [name for name, _ in client.calls].count("workspace.exec"),
            1,
        )
        kernel.validate_invariants()

    def test_retryable_pre_admission_rejection_preserves_effect(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_exec(kernel, "ordivon-rejected")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            ToolRejected(
                "workspace.exec",
                code="CONCURRENCY_LIMIT",
                message="workspace execution concurrency limit reached",
                field="workspaceId",
                retryable=True,
            ),
        )
        client.add("task.list", {"jobs": []})
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(25, 100)).__next__,
        )
        result = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(result.state, EffectState.PREPARED)
        self.assertEqual(result.error_code, "CONCURRENCY_LIMIT")
        self.assertEqual(
            [name for name, _ in client.calls].count("workspace.exec"),
            1,
        )
        self.assertEqual(
            [name for name, _ in client.calls].count("task.list"),
            1,
        )
        rejected_event = kernel.events_for(spec.effect_id)[-1]
        rejected_dispatch = kernel.get_dispatch(rejected_event.dispatch_id)
        self.assertIs(rejected_dispatch.state, DispatchState.REJECTED)
        self.assertTrue(rejected_dispatch.retryable)
        self.assertIsNone(kernel.get_effect(spec.effect_id).dispatch_id)

        client.add(
            "workspace.exec",
            {
                "jobId": "job-after-rejection",
                "attemptId": "attempt-after-rejection",
                "workspaceId": "workspace-test",
                "status": "succeeded",
                "exitCode": 0,
                "artifacts": [],
            },
        )
        second = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(second.state, EffectState.SUCCEEDED)
        self.assertNotEqual(second.binding.dispatch_id, rejected_dispatch.dispatch_id)
        self.assertEqual(
            [name for name, _ in client.calls].count("workspace.exec"),
            2,
        )
        kernel.validate_invariants()

    def test_non_retryable_pre_admission_rejection_fails_effect(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_exec(kernel, "ordivon-rejected-terminal")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            ToolRejected(
                "workspace.exec",
                code="INVALID_REQUEST",
                message="execution contract rejected",
                field="execution",
                retryable=False,
            ),
        )
        client.add("task.list", {"jobs": []})
        adapter = OrdivonSemanticAdapter(
            kernel,
            client,
            clock_ms=iter(range(25, 100)).__next__,
        )
        result = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(result.state, EffectState.FAILED)
        self.assertEqual(result.error_code, "INVALID_REQUEST")
        rejected_event = kernel.events_for(spec.effect_id)[-1]
        rejected_dispatch = kernel.get_dispatch(rejected_event.dispatch_id)
        self.assertIs(rejected_dispatch.state, DispatchState.REJECTED)
        self.assertFalse(rejected_dispatch.retryable)
        self.assertIsNone(kernel.get_effect(spec.effect_id).dispatch_id)
        kernel.validate_invariants()

    def test_orphaned_job_remains_semantically_unknown(self) -> None:
        kernel = ReferenceKernel()
        spec = prepared_exec(kernel, "ordivon-orphaned")
        client = ScriptedClient()
        client.add(
            "workspace.exec",
            {
                "jobId": "job-orphaned",
                "attemptId": "attempt-orphaned",
                "workspaceId": "workspace-test",
                "status": "orphaned",
                "artifacts": [],
            },
        )
        adapter = OrdivonSemanticAdapter(kernel, client, clock_ms=iter(range(30, 100)).__next__)
        result = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution("workspace-test", "/usr/bin/true"),
        )
        self.assertIs(result.state, EffectState.UNKNOWN)
        kernel.validate_invariants()


if __name__ == "__main__":
    unittest.main()
