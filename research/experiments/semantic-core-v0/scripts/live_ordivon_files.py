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
    EvidenceKind,
    VerificationPlan,
    WorldObjectRef,
)
from anc_semantic_core.ordivon_io import (
    MutationMode,
    OrdivonIoAdapter,
    OrdivonMutation,
    OrdivonRead,
    ordivon_file_object_id,
)
from anc_semantic_core.state import EffectState
from anc_semantic_core.verification import verify_digest_fact
from live_support import LocalMcpToolCaller


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run live Ordivon read/mutate semantic conformance"
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


def prepare_effect(
    kernel: ReferenceKernel,
    *,
    name: str,
    target: WorldObjectRef,
    operation: str,
    mode: EffectMode,
    method: str,
    clock: Any,
) -> Any:
    base = sample_effect(name)
    spec = replace(
        base,
        target=target,
        operation=operation,
        mode=mode,
        capability=CapabilityRef(
            SemanticId(IdKind.PRINCIPAL, "agent:live-file-conformance"),
            operation,
            target.object_id,
        ),
        completion=CompletionSemantics.VERIFIED,
        verification=VerificationPlan(
            method=method,
            required_evidence=(EvidenceKind.OBSERVATION,),
        ),
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


def main() -> None:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")
    client = LocalMcpToolCaller(args.endpoint, token)
    stamp = int(time.time() * 1000)
    workspace_id = f"anc-live-files-{stamp}"
    relative_path = "semantic-live-file.txt"
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

        # Harness setup is deliberately outside the semantic mutation under test.
        setup = client.call_tool(
            "workspace.mutate",
            {
                "schemaVersion": 1,
                "workspaceId": workspace_id,
                "mutations": [
                    {
                        "relativePath": relative_path,
                        "mode": "WRITE",
                        "content": "before\n",
                    }
                ],
            },
        )
        before_digest = setup["mutations"][0]["afterDigest"]

        object_id = ordivon_file_object_id(workspace_id, relative_path)
        kernel = ReferenceKernel()
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        adapter = OrdivonIoAdapter(kernel, client, clock_ms=clock)

        read_before_effect = prepare_effect(
            kernel,
            name=f"live-file-read-before:{stamp}",
            target=WorldObjectRef(object_id, version=before_digest),
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            method="file-digest",
            clock=clock,
        )
        read_before = adapter.dispatch_read(
            read_before_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if read_before.payload.get("content") != "before\n":
            raise AssertionError("versioned read did not observe initial content")
        if read_before.observation.target.version != before_digest:
            raise AssertionError("initial read digest differs from setup receipt")

        mutation_effect = prepare_effect(
            kernel,
            name=f"live-file-replace:{stamp}",
            target=WorldObjectRef(object_id, version=before_digest),
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            method="independent-file-digest",
            clock=clock,
        )
        replaced = adapter.dispatch_mutation(
            mutation_effect.effect_id,
            OrdivonMutation(
                workspace_id,
                relative_path,
                MutationMode.REPLACE_EXACT,
                "after\n",
                before_digest,
                "before\n",
            ),
        )
        if replaced.state is not EffectState.SUCCEEDED:
            raise AssertionError("atomic replacement did not succeed")
        if replaced.observation is None or replaced.observation.target.version is None:
            raise AssertionError("atomic replacement produced no digest Observation")
        after_digest = replaced.observation.target.version
        if after_digest == before_digest:
            raise AssertionError("atomic replacement did not change the digest")

        read_after_effect = prepare_effect(
            kernel,
            name=f"live-file-read-after:{stamp}",
            target=WorldObjectRef(object_id, version=after_digest),
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            method="file-digest",
            clock=clock,
        )
        read_after = adapter.dispatch_read(
            read_after_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if read_after.payload.get("content") != "after\n":
            raise AssertionError("independent read did not observe replacement content")
        fact_result = verify_digest_fact(
            kernel,
            claim_effect_id=mutation_effect.effect_id,
            observation=read_after.observation,
            expected_digest=after_digest,
            verified_at_ms=clock(),
            accepted_at_ms=clock(),
        )
        if fact_result.fact is None:
            raise AssertionError("independent replacement verification did not admit Fact")

        stale_effect = prepare_effect(
            kernel,
            name=f"live-file-stale:{stamp}",
            target=WorldObjectRef(object_id, version=before_digest),
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            method="independent-file-digest",
            clock=clock,
        )
        stale = adapter.dispatch_mutation(
            stale_effect.effect_id,
            OrdivonMutation(
                workspace_id,
                relative_path,
                MutationMode.REPLACE_EXACT,
                "corrupted\n",
                before_digest,
                "after\n",
            ),
        )
        if stale.state is not EffectState.FAILED:
            raise AssertionError(f"stale mutation was not rejected: {stale.state}")

        final_read_effect = prepare_effect(
            kernel,
            name=f"live-file-final-read:{stamp}",
            target=WorldObjectRef(object_id, version=after_digest),
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            method="file-digest",
            clock=clock,
        )
        final_read = adapter.dispatch_read(
            final_read_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if final_read.payload.get("content") != "after\n":
            raise AssertionError("stale mutation changed file content")
        if final_read.observation.target.version != after_digest:
            raise AssertionError("stale mutation changed file digest")

        kernel.validate_invariants()
        operation_counts: dict[str, int] = {}
        for name, _ in client.calls:
            operation_counts[name] = operation_counts.get(name, 0) + 1
        print(
            json.dumps(
                {
                    "workspaceId": workspace_id,
                    "sourceRevision": resolved_revision,
                    "beforeDigest": before_digest,
                    "afterDigest": after_digest,
                    "mutationFactsCommitted": 1,
                    "staleMutationState": stale.state.value,
                    "staleMutationErrorCode": stale.error_code,
                    "finalContentStable": True,
                    "finalDigestStable": True,
                    "mutationReceiptId": replaced.receipt_id,
                    "readReceiptIds": [
                        read_before.receipt_id,
                        read_after.receipt_id,
                        final_read.receipt_id,
                    ],
                    "toolCallCounts": operation_counts,
                },
                indent=2,
                sort_keys=True,
            )
        )
    finally:
        if opened:
            closed = client.call_tool(
                "workspace.close",
                {"schemaVersion": 1, "workspaceId": workspace_id, "force": True},
            )
            if closed.get("workspaceId") != workspace_id:
                raise AssertionError("workspace close identity mismatch")


if __name__ == "__main__":
    main()
