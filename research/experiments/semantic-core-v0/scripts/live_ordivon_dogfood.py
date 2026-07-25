from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from dataclasses import replace

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.kernel import ReferenceKernel
from anc_semantic_core.mcp_http import StreamableHttpMcpClient
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one Semantic Core Effect through the live Ordivon MCP boundary."
    )
    parser.add_argument("--target-workspace", required=True)
    parser.add_argument(
        "--effect-name",
        default=f"live-{time.time_ns()}",
        help="Unique semantic Effect suffix. Reusing it intentionally reuses identity.",
    )
    parser.add_argument("--message", default="semantic-core-live")
    parser.add_argument(
        "--expect-state",
        choices=[state.value for state in EffectState],
        default=EffectState.SUCCEEDED.value,
    )
    parser.add_argument(
        "--endpoint",
        default=f"http://{os.environ.get('ORDIVON_BIND', '127.0.0.1:8897')}/mcp",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")

    kernel = ReferenceKernel()
    base = sample_effect(args.effect_name)
    target_id = ordivon_workspace_object_id(args.target_workspace)
    input_digest = "sha256:" + hashlib.sha256(args.message.encode("utf-8")).hexdigest()
    spec = replace(
        base,
        target=WorldObjectRef(target_id),
        mode=EffectMode.OBSERVE,
        operation="workspace.exec",
        input_digest=input_digest,
        capability=CapabilityRef(
            base.capability.principal_id,
            "workspace.exec",
            target_id,
        ),
        completion=CompletionSemantics.VERIFIED,
    )
    kernel.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"event:{args.effect_name}:admit"),
        recorded_at_ms=1,
    )
    kernel.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"event:{args.effect_name}:prepare"),
        recorded_at_ms=2,
    )

    client = StreamableHttpMcpClient(args.endpoint, token)
    initialized = client.initialize()
    server_name = initialized.get("serverInfo", {}).get("name")
    if not isinstance(server_name, str) or not server_name.startswith("ordivon-"):
        raise SystemExit("endpoint is not an Ordivon MCP server")
    adapter = OrdivonSemanticAdapter(kernel, client)
    result = adapter.dispatch_exec(
        spec.effect_id,
        OrdivonExecution(
            workspace_id=args.target_workspace,
            executable="/usr/bin/printf",
            args=(f"{args.message}\n",),
            timeout_ms=5_000,
            stdout_limit_bytes=4_096,
            stderr_limit_bytes=4_096,
        ),
        wait_ms=30_000,
    )
    kernel.validate_invariants()

    summary = {
        "effectId": str(spec.effect_id),
        "state": result.state.value,
        "errorCode": result.error_code,
        "errorMessage": result.error_message,
        "jobId": result.binding.job_id if result.binding else None,
        "attemptId": result.binding.attempt_id if result.binding else None,
        "artifactCount": len(result.artifacts),
        "stdoutTail": (result.payload or {}).get("stdoutTail"),
        "observationDigest": (
            result.observation.payload_digest if result.observation else None
        ),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if result.state.value == args.expect_state else 1


if __name__ == "__main__":
    raise SystemExit(main())
