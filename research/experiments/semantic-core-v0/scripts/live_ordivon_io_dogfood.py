from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import time
from dataclasses import replace

from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.authorized import AuthorizedKernel
from anc_semantic_core.bootstrap import authorized_reference_views
from live_support import LocalMcpToolCaller
from anc_semantic_core.model import (
    CapabilityRef,
    CompletionSemantics,
    EffectMode,
    EvidenceKind,
    IdempotencyKind,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run versioned read, atomic mutation, reread verification, and Fact admission."
    )
    parser.add_argument("--target-workspace", required=True)
    parser.add_argument("--relative-path", required=True)
    parser.add_argument("--new-content", required=True)
    parser.add_argument(
        "--run-id",
        default=f"live-io-{time.time_ns()}",
        help="Unique identity suffix for this semantic trajectory.",
    )
    parser.add_argument(
        "--endpoint",
        default=f"http://{os.environ.get('ORDIVON_BIND', '127.0.0.1:8897')}/mcp",
    )
    return parser.parse_args()


def prepare_effect(
    kernel: AuthorizedKernel,
    *,
    name: str,
    workspace_id: str,
    relative_path: str,
    operation: str,
    mode: EffectMode,
    target_version: str | None,
):
    base = sample_effect(name)
    target_id = ordivon_file_object_id(workspace_id, relative_path)
    spec = replace(
        base,
        target=WorldObjectRef(target_id, version=target_version),
        mode=mode,
        operation=operation,
        capability=CapabilityRef(base.capability.principal_id, operation, target_id),
        idempotency=IdempotencyKind.NATURAL,
        completion=(
            CompletionSemantics.ACCEPTED
            if mode is EffectMode.CHANGE
            else CompletionSemantics.VERIFIED
        ),
        verification=VerificationPlan(
            method="independent-reread-digest",
            required_evidence=(EvidenceKind.OBSERVATION,),
        ),
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


def main() -> int:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")
    client = LocalMcpToolCaller(args.endpoint, token)
    server_name = client.initialize().get("serverInfo", {}).get("name")
    if not isinstance(server_name, str) or not server_name.startswith("ordivon-"):
        raise SystemExit("endpoint is not an Ordivon MCP server")

    views = authorized_reference_views(
        secrets.token_bytes(32), namespace="live-io-dogfood"
    )
    adapter = OrdivonIoAdapter(views.execution, client)

    initial_read = prepare_effect(
        views.effects,
        name=f"{args.run_id}-initial-read",
        workspace_id=args.target_workspace,
        relative_path=args.relative_path,
        operation="workspace.read",
        mode=EffectMode.OBSERVE,
        target_version=None,
    )
    initial = adapter.dispatch_read(
        initial_read.effect_id,
        OrdivonRead(args.target_workspace, args.relative_path),
    )
    if initial.state is not EffectState.SUCCEEDED or initial.observation is None:
        raise SystemExit(json.dumps({"stage": "initial-read", "state": initial.state.value}))
    before_digest = initial.observation.target.version
    assert before_digest is not None

    mutation = prepare_effect(
        views.effects,
        name=f"{args.run_id}-mutation",
        workspace_id=args.target_workspace,
        relative_path=args.relative_path,
        operation="workspace.mutate",
        mode=EffectMode.CHANGE,
        target_version=before_digest,
    )
    mutated = adapter.dispatch_mutation(
        mutation.effect_id,
        OrdivonMutation(
            args.target_workspace,
            args.relative_path,
            MutationMode.WRITE,
            args.new_content,
            before_digest,
        ),
    )
    if mutated.state is not EffectState.SUCCEEDED or mutated.observation is None:
        raise SystemExit(json.dumps({"stage": "mutation", "state": mutated.state.value}))
    after_digest = mutated.observation.target.version
    assert after_digest is not None
    local_digest = f"sha256:{hashlib.sha256(args.new_content.encode('utf-8')).hexdigest()}"
    if after_digest != local_digest:
        raise SystemExit("mutation receipt digest does not match requested content")

    reread = prepare_effect(
        views.effects,
        name=f"{args.run_id}-reread",
        workspace_id=args.target_workspace,
        relative_path=args.relative_path,
        operation="workspace.read",
        mode=EffectMode.OBSERVE,
        target_version=after_digest,
    )
    reread_result = adapter.dispatch_read(
        reread.effect_id,
        OrdivonRead(args.target_workspace, args.relative_path),
    )
    if reread_result.state is not EffectState.SUCCEEDED or reread_result.observation is None:
        raise SystemExit(json.dumps({"stage": "reread", "state": reread_result.state.value}))

    fact_result = verify_digest_fact(
        views.verification,
        views.facts,
        claim_effect_id=mutation.effect_id,
        observation=reread_result.observation,
        expected_digest=after_digest,
        verified_at_ms=time.time_ns() // 1_000_000,
    )
    if fact_result.fact is None:
        raise SystemExit("independent reread rejected the mutation digest claim")

    stale = prepare_effect(
        views.effects,
        name=f"{args.run_id}-stale-guard",
        workspace_id=args.target_workspace,
        relative_path=args.relative_path,
        operation="workspace.mutate",
        mode=EffectMode.CHANGE,
        target_version=before_digest,
    )
    stale_result = adapter.dispatch_mutation(
        stale.effect_id,
        OrdivonMutation(
            args.target_workspace,
            args.relative_path,
            MutationMode.WRITE,
            args.new_content + "stale-attempt",
            before_digest,
        ),
    )
    if stale_result.state is not EffectState.FAILED:
        raise SystemExit("stale precondition was not rejected")

    views.read.validate_invariants()
    print(
        json.dumps(
            {
                "serverName": server_name,
                "worldObjectId": str(mutated.observation.target.object_id),
                "beforeDigest": before_digest,
                "afterDigest": after_digest,
                "mutationReceiptId": mutated.receipt_id,
                "rereadObservationId": str(reread_result.observation.observation_id),
                "verificationId": str(fact_result.verification.verification_id),
                "factId": str(fact_result.fact.fact_id),
                "staleGuardState": stale_result.state.value,
                "staleGuardCode": stale_result.error_code,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
