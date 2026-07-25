#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import replace
from typing import Any

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind, SemanticId
from anc_semantic_core.kernel import ReferenceKernel
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
from anc_semantic_core.transport import ToolTransportError
from live_support import LocalMcpToolCaller


class DropFirstSuccessfulResponse:
    """Deliver one real Tool call, then discard its successful response."""

    def __init__(self, underlying: LocalMcpToolCaller, tool_name: str) -> None:
        self.underlying = underlying
        self.tool_name = tool_name
        self.dropped = False

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        result = self.underlying.call_tool(name, arguments)
        if name == self.tool_name and not self.dropped:
            self.dropped = True
            raise ToolTransportError(
                f"injected response loss after successful {name} delivery"
            )
        return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inject response loss after durable Ordivon admission"
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument(
        "--source-repo",
        default="/root/projects/agent-native-computing",
    )
    parser.add_argument("--source-revision", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")

    real_client = LocalMcpToolCaller(args.endpoint, token)
    lossy_client = DropFirstSuccessfulResponse(real_client, "workspace.exec")
    stamp = int(time.time() * 1000)
    workspace_id = f"anc-live-response-loss-{stamp}"
    opened = False
    try:
        opened_payload = real_client.call_tool(
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
        target_id = ordivon_workspace_object_id(workspace_id)
        base = sample_effect(f"response-loss-{stamp}")
        spec = replace(
            base,
            target=WorldObjectRef(target_id, version=resolved_revision),
            mode=EffectMode.CHANGE,
            operation="workspace.exec",
            capability=CapabilityRef(
                SemanticId(IdKind.PRINCIPAL, "agent:response-loss-conformance"),
                "workspace.exec",
                target_id,
            ),
            completion=CompletionSemantics.VERIFIED,
        )
        kernel = ReferenceKernel()
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        kernel.admit_effect(
            spec,
            event_id=sid(IdKind.EVENT, f"response-loss:{stamp}:admit"),
            recorded_at_ms=clock(),
        )
        kernel.prepare_effect(
            spec.effect_id,
            expected_revision=0,
            event_id=sid(IdKind.EVENT, f"response-loss:{stamp}:prepare"),
            recorded_at_ms=clock(),
        )
        adapter = OrdivonSemanticAdapter(kernel, lossy_client, clock_ms=clock)
        first = adapter.dispatch_exec(
            spec.effect_id,
            OrdivonExecution(
                workspace_id=workspace_id,
                executable="/usr/bin/bash",
                args=(
                    "-lc",
                    "printf 'response-loss-start\\n'; sleep 1; "
                    "printf 'response-loss-done\\n'",
                ),
                timeout_ms=20_000,
            ),
            wait_ms=0,
        )
        if first.state is not EffectState.UNKNOWN:
            raise AssertionError(
                f"injected response loss did not produce UNKNOWN: {first.state}"
            )
        unknown_dispatch = kernel.get_effect(spec.effect_id).dispatch_id
        if unknown_dispatch is None:
            raise AssertionError("unknown Effect lost its Dispatch identity")

        # Simulate adapter-instance restart: no pending or Job bindings survive.
        restarted_adapter = OrdivonSemanticAdapter(
            kernel,
            real_client,
            clock_ms=clock,
        )
        projection = first
        for _ in range(5):
            projection = restarted_adapter.reconcile(
                spec.effect_id,
                wait_ms=10_000,
            )
            if projection.state.terminal:
                break
        if projection.state is not EffectState.SUCCEEDED:
            raise AssertionError(
                f"reconciliation did not recover terminal success: {projection.state}"
            )
        if projection.binding is None:
            raise AssertionError("reconciliation produced no Ordivon binding")
        if projection.binding.dispatch_id != unknown_dispatch:
            raise AssertionError("reconciliation replaced the original Dispatch identity")

        exec_calls = [
            arguments
            for name, arguments in real_client.calls
            if name == "workspace.exec"
        ]
        if len(exec_calls) != 1:
            raise AssertionError(
                f"expected one workspace.exec delivery, observed {len(exec_calls)}"
            )
        jobs = real_client.call_tool("task.list", {"limit": 100})["jobs"]
        matching_jobs = [
            job
            for job in jobs
            if job.get("clientRequestId") == projection.binding.client_request_id
        ]
        if len(matching_jobs) != 1:
            raise AssertionError(
                f"expected one correlated Job, observed {len(matching_jobs)}"
            )
        kernel.validate_invariants()

        print(
            json.dumps(
                {
                    "workspaceId": workspace_id,
                    "sourceRevision": resolved_revision,
                    "initialState": first.state.value,
                    "terminalState": projection.state.value,
                    "dispatchIdPreserved": True,
                    "jobId": projection.binding.job_id,
                    "attemptId": projection.binding.attempt_id,
                    "workspaceExecDeliveries": len(exec_calls),
                    "correlatedJobCount": len(matching_jobs),
                    "responseDroppedAfterSuccessfulDelivery": lossy_client.dropped,
                    "adapterInstanceRestarted": True,
                    "semanticArtifactCount": len(projection.artifacts),
                },
                indent=2,
                sort_keys=True,
            )
        )
    finally:
        if opened:
            closed = real_client.call_tool(
                "workspace.close",
                {"schemaVersion": 1, "workspaceId": workspace_id, "force": False},
            )
            if closed.get("workspaceId") != workspace_id:
                raise AssertionError("workspace close identity mismatch")


if __name__ == "__main__":
    main()
