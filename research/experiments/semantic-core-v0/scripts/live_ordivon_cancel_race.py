#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import time
from dataclasses import replace
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.authorized import AuthorizedKernel
from anc_semantic_core.bootstrap import authorized_reference_views
from anc_semantic_core.model import (
    CapabilityRef,
    CompletionSemantics,
    EffectMode,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import (
    OrdivonExecution,
    OrdivonSemanticAdapter,
    ordivon_workspace_object_id,
)
from anc_semantic_core.state import EffectState
from live_support import LocalMcpToolCaller


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run live Ordivon cancellation races")
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument(
        "--source-repo",
        default="/root/projects/ordivon-computing",
    )
    parser.add_argument("--source-revision", required=True)
    return parser.parse_args()


def prepare_exec_effect(
    kernel: AuthorizedKernel,
    *,
    name: str,
    workspace_id: str,
    source_revision: str,
    clock: Any,
) -> Any:
    target_id = ordivon_workspace_object_id(workspace_id)
    base = sample_effect(name)
    spec = replace(
        base,
        target=WorldObjectRef(target_id, version=source_revision),
        mode=EffectMode.CHANGE,
        operation="workspace.exec",
        capability=CapabilityRef(
            SemanticId(IdKind.PRINCIPAL, "agent:cancel-race-conformance"),
            "workspace.exec",
            target_id,
        ),
        completion=CompletionSemantics.VERIFIED,
    )
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"{name}:admit"),
        recorded_at_ms=clock(),
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"{name}:prepare"),
        recorded_at_ms=clock(),
    )
    return spec


def observe_terminal(
    adapter: OrdivonSemanticAdapter,
    effect_id: SemanticId,
    projection: Any,
) -> Any:
    for _ in range(5):
        if projection.state.terminal:
            return projection
        projection = adapter.observe(effect_id, wait_ms=10_000)
    return projection


def main() -> None:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")

    client = LocalMcpToolCaller(args.endpoint, token)
    stamp = int(time.time() * 1000)
    workspace_id = f"anc-live-cancel-race-{stamp}"
    opened = False
    try:
        opened_payload = client.call_tool(
            "workspace.open",
            {
                "schemaVersion": 1,
                "sourceRepo": args.source_repo,
                "sourceRevision": args.source_revision,
                "workspaceId": workspace_id,
            },
        )
        opened = True
        resolved_revision = opened_payload["sourceRevision"]
        views = authorized_reference_views(
            secrets.token_bytes(32), namespace="live-cancel-race"
        )
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        adapter = OrdivonSemanticAdapter(views.execution, client, clock_ms=clock)

        # Case A: cancellation reaches the backend before natural completion.
        cancelled_effect = prepare_exec_effect(
            views.effects,
            name=f"cancel-applied:{stamp}",
            workspace_id=workspace_id,
            source_revision=resolved_revision,
            clock=clock,
        )
        running = adapter.dispatch_exec(
            cancelled_effect.effect_id,
            OrdivonExecution(
                workspace_id,
                "/usr/bin/bash",
                (
                    "-lc",
                    "printf 'cancel-start\\n'; sleep 10; printf 'cancel-end\\n'",
                ),
                timeout_ms=20_000,
            ),
            wait_ms=0,
        )
        if running.state not in {EffectState.DISPATCHED, EffectState.RUNNING}:
            raise AssertionError(f"long command was not cancellable: {running.state}")
        cancelled = adapter.cancel(cancelled_effect.effect_id, wait_ms=10_000)
        cancelled = observe_terminal(adapter, cancelled_effect.effect_id, cancelled)
        if cancelled.state is not EffectState.CANCELLED:
            raise AssertionError(
                f"long command did not reach cancelled: {cancelled.state}"
            )
        if cancelled.binding is None:
            raise AssertionError("cancelled Effect lost its Job binding")

        # Case B: the process completes naturally before cancellation is applied.
        completed_effect = prepare_exec_effect(
            views.effects,
            name=f"natural-completion:{stamp}",
            workspace_id=workspace_id,
            source_revision=resolved_revision,
            clock=clock,
        )
        racing = adapter.dispatch_exec(
            completed_effect.effect_id,
            OrdivonExecution(
                workspace_id,
                "/usr/bin/bash",
                (
                    "-lc",
                    "printf 'race-start\\n'; sleep 0.4; printf 'race-done\\n'",
                ),
                timeout_ms=10_000,
            ),
            wait_ms=0,
        )
        if racing.state not in {EffectState.DISPATCHED, EffectState.RUNNING}:
            raise AssertionError(f"race command resolved too early: {racing.state}")
        time.sleep(1.0)
        completed = adapter.cancel(completed_effect.effect_id, wait_ms=10_000)
        completed = observe_terminal(adapter, completed_effect.effect_id, completed)
        if completed.state is not EffectState.SUCCEEDED:
            raise AssertionError(
                "natural completion was overwritten by cancellation intent: "
                f"{completed.state}"
            )
        if completed.binding is None:
            raise AssertionError("naturally completed Effect lost its Job binding")

        exec_calls = [name for name, _ in client.calls if name == "workspace.exec"]
        cancel_calls = [name for name, _ in client.calls if name == "task.cancel"]
        if len(exec_calls) != 2:
            raise AssertionError(f"expected two executions, observed {len(exec_calls)}")
        if len(cancel_calls) != 2:
            raise AssertionError(f"expected two cancel calls, observed {len(cancel_calls)}")
        views.read.validate_invariants()

        print(
            json.dumps(
                {
                    "workspaceId": workspace_id,
                    "sourceRevision": resolved_revision,
                    "cancelApplied": {
                        "state": cancelled.state.value,
                        "jobId": cancelled.binding.job_id,
                        "attemptId": cancelled.binding.attempt_id,
                    },
                    "naturalCompletionWon": {
                        "state": completed.state.value,
                        "jobId": completed.binding.job_id,
                        "attemptId": completed.binding.attempt_id,
                    },
                    "workspaceExecDeliveries": len(exec_calls),
                    "taskCancelCalls": len(cancel_calls),
                    "invariantsValid": True,
                },
                indent=2,
                sort_keys=True,
            )
        )
    finally:
        if opened:
            closed = client.call_tool(
                "workspace.close",
                {"schemaVersion": 1, "workspaceId": workspace_id, "force": False},
            )
            if closed.get("workspaceId") != workspace_id:
                raise AssertionError("workspace close identity mismatch")


if __name__ == "__main__":
    main()
