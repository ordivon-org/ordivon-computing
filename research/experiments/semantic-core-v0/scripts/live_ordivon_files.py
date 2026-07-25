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
    Claim,
    CompletionSemantics,
    EffectMode,
    EvidenceKind,
    EvidenceRef,
    Fact,
    Verification,
    VerificationDecision,
    VerificationPlan,
    WorldObjectRef,
)
from anc_semantic_core.ordivon import (
    OrdivonFileMutation,
    OrdivonMutationMode,
    OrdivonRead,
    OrdivonSemanticAdapter,
)
from anc_semantic_core.state import EffectState
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


def admit_digest_fact(
    kernel: ReferenceKernel,
    *,
    name: str,
    origin_effect: Any,
    subject: WorldObjectRef,
    evidence_observation: Any,
    clock: Any,
) -> Fact:
    claim = Claim(
        claim_id=sid(IdKind.CLAIM, f"{name}:claim"),
        origin_effect_id=origin_effect.effect_id,
        subject=subject,
        predicate="file_digest_equals",
        value_digest=subject.version or "unknown",
    )
    kernel.admit_claim(claim)
    verified_at_ms = clock()
    verification = Verification(
        verification_id=sid(IdKind.VERIFICATION, f"{name}:verification"),
        claim_id=claim.claim_id,
        method=origin_effect.verification.method,
        evidence=(
            EvidenceRef(
                EvidenceKind.OBSERVATION,
                evidence_observation.observation_id,
            ),
        ),
        decision=VerificationDecision.ACCEPTED,
        verified_at_ms=verified_at_ms,
    )
    kernel.record_verification(verification)
    fact = Fact(
        fact_id=sid(IdKind.FACT, f"{name}:fact"),
        claim_id=claim.claim_id,
        verification_id=verification.verification_id,
        accepted_at_ms=clock(),
    )
    kernel.commit_fact(fact)
    return fact


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
        object_id = SemanticId(
            IdKind.WORLD_OBJECT,
            f"ordivon-file:{workspace_id}:{relative_path}",
        )
        kernel = ReferenceKernel()
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        adapter = OrdivonSemanticAdapter(kernel, client, clock_ms=clock)

        create_target = WorldObjectRef(object_id)
        create_effect = prepare_effect(
            kernel,
            name=f"live-file-create:{stamp}",
            target=create_target,
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            method="independent-file-digest",
            clock=clock,
        )
        created = adapter.mutate_file(
            create_effect.effect_id,
            OrdivonFileMutation(
                workspace_id,
                relative_path,
                OrdivonMutationMode.WRITE,
                content="before\n",
            ),
        )
        if created.state is not EffectState.SUCCEEDED or created.observation is None:
            raise AssertionError("initial semantic mutation did not succeed")
        before_digest = created.observation.target.version
        if not before_digest:
            raise AssertionError("initial mutation produced no file digest")

        read_before_target = WorldObjectRef(object_id, version=before_digest)
        read_before_effect = prepare_effect(
            kernel,
            name=f"live-file-read-before:{stamp}",
            target=read_before_target,
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            method="file-digest",
            clock=clock,
        )
        read_before = adapter.read_file(
            read_before_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if read_before.payload is None or read_before.payload.get("content") != "before\n":
            raise AssertionError("independent read did not observe initial content")
        if read_before.observation is None:
            raise AssertionError("independent read produced no Observation")
        if read_before.observation.target.version != before_digest:
            raise AssertionError("independent read digest differs from mutation result")
        admit_digest_fact(
            kernel,
            name=f"live-file-before:{stamp}",
            origin_effect=create_effect,
            subject=read_before_target,
            evidence_observation=read_before.observation,
            clock=clock,
        )

        replace_target = WorldObjectRef(object_id, version=before_digest)
        replace_effect = prepare_effect(
            kernel,
            name=f"live-file-replace:{stamp}",
            target=replace_target,
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            method="independent-file-digest",
            clock=clock,
        )
        replaced = adapter.mutate_file(
            replace_effect.effect_id,
            OrdivonFileMutation(
                workspace_id,
                relative_path,
                OrdivonMutationMode.REPLACE_EXACT,
                content="after",
                expected_digest=before_digest,
                expected_text="before",
            ),
        )
        if replaced.state is not EffectState.SUCCEEDED or replaced.observation is None:
            raise AssertionError("replacement semantic mutation did not succeed")
        after_digest = replaced.observation.target.version
        if not after_digest or after_digest == before_digest:
            raise AssertionError("replacement did not produce a new digest")

        read_after_target = WorldObjectRef(object_id, version=after_digest)
        read_after_effect = prepare_effect(
            kernel,
            name=f"live-file-read-after:{stamp}",
            target=read_after_target,
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            method="file-digest",
            clock=clock,
        )
        read_after = adapter.read_file(
            read_after_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if read_after.payload is None or read_after.payload.get("content") != "after\n":
            raise AssertionError("independent read did not observe replacement content")
        if read_after.observation is None:
            raise AssertionError("replacement read produced no Observation")
        if read_after.observation.target.version != after_digest:
            raise AssertionError("replacement read digest differs from mutation result")
        admit_digest_fact(
            kernel,
            name=f"live-file-after:{stamp}",
            origin_effect=replace_effect,
            subject=read_after_target,
            evidence_observation=read_after.observation,
            clock=clock,
        )

        stale_effect = prepare_effect(
            kernel,
            name=f"live-file-stale:{stamp}",
            target=WorldObjectRef(object_id, version=before_digest),
            operation="workspace.mutate",
            mode=EffectMode.CHANGE,
            method="independent-file-digest",
            clock=clock,
        )
        stale = adapter.mutate_file(
            stale_effect.effect_id,
            OrdivonFileMutation(
                workspace_id,
                relative_path,
                OrdivonMutationMode.REPLACE_EXACT,
                content="corrupted",
                expected_digest=before_digest,
                expected_text="after",
            ),
        )
        if stale.state is not EffectState.FAILED:
            raise AssertionError(f"stale mutation was not rejected: {stale.state}")

        final_read_effect = prepare_effect(
            kernel,
            name=f"live-file-final-read:{stamp}",
            target=read_after_target,
            operation="workspace.read",
            mode=EffectMode.OBSERVE,
            method="file-digest",
            clock=clock,
        )
        final_read = adapter.read_file(
            final_read_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if final_read.payload is None or final_read.payload.get("content") != "after\n":
            raise AssertionError("stale mutation changed file content")
        if final_read.observation is None:
            raise AssertionError("final read produced no Observation")
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
                    "mutationFactsCommitted": 2,
                    "staleMutationState": stale.state.value,
                    "staleMutationErrorCode": stale.error_code,
                    "finalContentStable": True,
                    "finalDigestStable": True,
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
