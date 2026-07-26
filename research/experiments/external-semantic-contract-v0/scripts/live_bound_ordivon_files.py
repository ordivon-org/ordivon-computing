#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import time
from pathlib import Path

from live_bound_support import LiveBindingContext

from anc_effect_binding import lower_to_ordivon
from anc_tool_contract import contract_digest
from anc_effect_ir import (
    CanonicalInput,
    CapabilityRequirement,
    CompletionKind,
    DeliverySemantics,
    EffectEnvelope,
    EffectMode,
    EvidenceKind,
    ExecutionKind,
    IdempotencyKind,
    ResultSemantics,
    SemanticAction,
    TargetRef,
    VerificationPlan,
)
from integration import BoundExecutionView, admit_bound_effect, discover_ordivon_contracts
from anc_semantic_core.bootstrap import authorized_reference_views
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
        description="Prove real bound Ordivon read/mutate evidence and Fact admission"
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument("--source-repo", default="/root/projects/ordivon-architecture")
    parser.add_argument("--source-revision", required=True)
    return parser.parse_args()


def read_envelope(name: str, relative_path: str, version: str) -> EffectEnvelope:
    action = "anc.object.read.v1"
    target = TargetRef(f"world_object:workspace-file:{relative_path}", version)
    return EffectEnvelope(
        effect_id=f"effect:{name}",
        target=target,
        mode=EffectMode.OBSERVE,
        action=SemanticAction(action, "anc.object-read-input.v1"),
        input=CanonicalInput({}),
        capability=CapabilityRequirement(
            "principal:ordivon-live-agent", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=ResultSemantics(
            ExecutionKind.SYNCHRONOUS,
            CompletionKind.ACCEPTED_VERIFICATION,
        ),
        verification=VerificationPlan(
            "independent-file-digest.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


def mutation_envelope(
    name: str,
    relative_path: str,
    version: str,
    content: str,
    *,
    expected_text: str,
) -> EffectEnvelope:
    action = "anc.object.replace-if-version.v1"
    target = TargetRef(f"world_object:workspace-file:{relative_path}", version)
    return EffectEnvelope(
        effect_id=f"effect:{name}",
        target=target,
        mode=EffectMode.CHANGE,
        action=SemanticAction(action, "anc.object-replace-input.v1"),
        input=CanonicalInput(
            {
                "content": content,
                "mode": "REPLACE_EXACT",
                "expectedText": expected_text,
            }
        ),
        capability=CapabilityRequirement(
            "principal:ordivon-live-agent", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=ResultSemantics(ExecutionKind.SYNCHRONOUS, CompletionKind.RESPONSE),
        verification=VerificationPlan(
            "independent-file-digest.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


def prepare_bound(
    views,
    context: LiveBindingContext,
    contract,
    envelope: EffectEnvelope,
    *,
    workspace_id: str,
    relative_path: str,
    binding_id: str,
    client,
    clock,
):
    signed = context.sign(envelope, issued_at_ms=clock())
    binding = lower_to_ordivon(
        envelope,
        contract,
        binding_id=binding_id,
        workspace_id=workspace_id,
    )
    projection, admission = admit_bound_effect(
        views,
        signed,
        contract,
        binding,
        context.service,
        backend_target=ordivon_file_object_id(workspace_id, relative_path),
        event_namespace=envelope.effect_id,
        admitted_at_ms=clock(),
    )
    # admit_bound_effect consumes three logical timestamps from its base.
    clock()
    clock()
    complete = context.service.resolve(admission).binding
    adapter = OrdivonIoAdapter(
        BoundExecutionView(views.execution, admission, complete),
        client,
        clock_ms=clock,
    )
    return projection, admission, adapter


def assert_bound(
    views,
    context: LiveBindingContext,
    effect_id,
    *,
    dispatch_id=None,
) -> dict[str, str]:
    record = views.read.get_effect(effect_id)
    dispatch_id = dispatch_id or record.dispatch_id
    if dispatch_id is None:
        raise AssertionError("Effect produced no Dispatch history")
    dispatch = views.read.get_dispatch(dispatch_id)
    admission = views.read.current_binding_for(effect_id)
    if admission is None:
        raise AssertionError("Effect produced no Binding admission")
    if dispatch.binding_id != admission.binding_id:
        raise AssertionError("Dispatch does not reference the current Binding")
    if dispatch.binding_digest != admission.binding_digest:
        raise AssertionError("Dispatch Binding digest differs from admission")
    context.service.resolve(admission)
    return {
        "effectId": str(effect_id),
        "dispatchId": str(dispatch.dispatch_id),
        "bindingId": str(admission.binding_id),
        "bindingDigest": admission.binding_digest,
    }


def main() -> None:
    args = parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")
    client = LocalMcpToolCaller(args.endpoint, token)
    client.initialize()
    contracts = discover_ordivon_contracts(client)
    stamp = int(time.time() * 1_000)
    workspace_id = f"anc-live-bound-files-{stamp}"
    relative_path = "semantic-bound-live-file.txt"
    binding_store_path = Path(f"/tmp/anc-bound-file-bindings-{stamp}")
    context = LiveBindingContext.open(binding_store_path, create_secrets=True)
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
        views = authorized_reference_views(
            os.urandom(32), namespace="live-bound-files"
        )
        clock = iter(range(stamp, stamp + 1_000_000)).__next__
        bound_records: list[dict[str, str]] = []

        read_before_envelope = read_envelope(
            f"live-bound-read-before:{stamp}", relative_path, before_digest
        )
        read_before_effect, _, read_before_adapter = prepare_bound(
            views,
            context,
            contracts["workspace.read"],
            read_before_envelope,
            workspace_id=workspace_id,
            relative_path=relative_path,
            binding_id=f"binding:live-bound-read-before:{stamp}:r1",
            client=client,
            clock=clock,
        )
        read_before = read_before_adapter.dispatch_read(
            read_before_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if read_before.payload.get("content") != "before\n":
            raise AssertionError("bound read did not observe initial content")
        bound_records.append(
            assert_bound(views, context, read_before_effect.effect_id)
        )

        replace_envelope = mutation_envelope(
            f"live-bound-replace:{stamp}",
            relative_path,
            before_digest,
            "after\n",
            expected_text="before\n",
        )
        replace_effect, _, replace_adapter = prepare_bound(
            views,
            context,
            contracts["workspace.mutate"],
            replace_envelope,
            workspace_id=workspace_id,
            relative_path=relative_path,
            binding_id=f"binding:live-bound-replace:{stamp}:r1",
            client=client,
            clock=clock,
        )
        replaced = replace_adapter.dispatch_mutation(
            replace_effect.effect_id,
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
            raise AssertionError("bound atomic replacement did not succeed")
        if replaced.observation is None or replaced.observation.target.version is None:
            raise AssertionError("bound replacement produced no digest Observation")
        after_digest = replaced.observation.target.version
        bound_records.append(assert_bound(views, context, replace_effect.effect_id))

        read_after_envelope = read_envelope(
            f"live-bound-read-after:{stamp}", relative_path, after_digest
        )
        read_after_effect, _, read_after_adapter = prepare_bound(
            views,
            context,
            contracts["workspace.read"],
            read_after_envelope,
            workspace_id=workspace_id,
            relative_path=relative_path,
            binding_id=f"binding:live-bound-read-after:{stamp}:r1",
            client=client,
            clock=clock,
        )
        read_after = read_after_adapter.dispatch_read(
            read_after_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if read_after.payload.get("content") != "after\n":
            raise AssertionError("bound independent read did not observe replacement")
        fact_result = verify_digest_fact(
            views.verification,
            views.facts,
            claim_effect_id=replace_effect.effect_id,
            observation=read_after.observation,
            expected_digest=after_digest,
            verified_at_ms=clock(),
            accepted_at_ms=clock(),
        )
        if fact_result.fact is None:
            raise AssertionError("bound independent read did not admit Fact")
        bound_records.append(assert_bound(views, context, read_after_effect.effect_id))

        stale_envelope = mutation_envelope(
            f"live-bound-stale:{stamp}",
            relative_path,
            before_digest,
            "corrupted\n",
            expected_text="after\n",
        )
        stale_effect, _, stale_adapter = prepare_bound(
            views,
            context,
            contracts["workspace.mutate"],
            stale_envelope,
            workspace_id=workspace_id,
            relative_path=relative_path,
            binding_id=f"binding:live-bound-stale:{stamp}:r1",
            client=client,
            clock=clock,
        )
        stale = stale_adapter.dispatch_mutation(
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
            raise AssertionError(f"bound stale mutation was not rejected: {stale.state}")
        bound_records.append(
            assert_bound(
                views,
                context,
                stale_effect.effect_id,
                dispatch_id=stale.dispatch_id,
            )
        )

        final_envelope = read_envelope(
            f"live-bound-final-read:{stamp}", relative_path, after_digest
        )
        final_effect, _, final_adapter = prepare_bound(
            views,
            context,
            contracts["workspace.read"],
            final_envelope,
            workspace_id=workspace_id,
            relative_path=relative_path,
            binding_id=f"binding:live-bound-final-read:{stamp}:r1",
            client=client,
            clock=clock,
        )
        final_read = final_adapter.dispatch_read(
            final_effect.effect_id,
            OrdivonRead(workspace_id, relative_path),
        )
        if final_read.payload.get("content") != "after\n":
            raise AssertionError("bound stale mutation changed file content")
        if final_read.observation.target.version != after_digest:
            raise AssertionError("bound stale mutation changed file digest")
        bound_records.append(assert_bound(views, context, final_effect.effect_id))

        views.read.validate_invariants()
        operation_counts: dict[str, int] = {}
        for name, _ in client.calls:
            operation_counts[name] = operation_counts.get(name, 0) + 1
        print(
            json.dumps(
                {
                    "workspaceId": workspace_id,
                    "sourceRevision": resolved_revision,
                    "catalogRevision": contracts["workspace.read"].revision,
                    "readContractDigest": contract_digest(
                        contracts["workspace.read"]
                    ),
                    "mutationContractDigest": contract_digest(
                        contracts["workspace.mutate"]
                    ),
                    "beforeDigest": before_digest,
                    "afterDigest": after_digest,
                    "boundDispatchCount": len(bound_records),
                    "allBindingArtifactsResolved": True,
                    "boundRecords": bound_records,
                    "mutationFactsCommitted": 1,
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
        shutil.rmtree(binding_store_path, ignore_errors=True)


if __name__ == "__main__":
    main()
