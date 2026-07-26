from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from anc_canonical import JsonValue, canonical_bytes
from anc_effect_binding import (
    FileBindingStore,
    SignedEffectBinding,
    bind_effect,
    binding_digest,
)
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
    ProtocolAuthority,
    ResultSemantics,
    SemanticAction,
    SignedEffectEnvelope,
    TargetRef,
    VerificationPlan,
    effect_digest,
)
from anc_tool_contract import ToolContract, normalize_tool_contract
from integration import BindingAuthorityService, BoundExecutionView, admit_bound_effect
from anc_semantic_core.simulator import (
    DeterministicBackend,
    DeterministicBackendAdapter,
    SimulatorArtifact,
    SimulatorJobRequest,
    SimulatorMutation,
    SimulatorRead,
    SimulatorStatus,
    simulator_object_id,
)
from anc_semantic_core.state import EffectState
from anc_semantic_core.testing import reference_authority_views
from anc_semantic_core.verification import DigestFactResult, verify_digest_fact

from .model import (
    ActionKind,
    GoalSpec,
    ReadyAction,
    SemanticRef,
    TaskCapsule,
    TaskPhase,
    WorldBinding,
)
from .store import FileObjectStore


TASK_ID = "task:continuation-config-promotion"
GOAL_ID = "goal:continuation-config-promotion"
CHECKPOINT_ID = "checkpoint:post-audit-pre-mutation"
WORLD_ID = "world:continuation-config"
WORLD_RELATIVE_PATH = "world/config.toml"
OBJECT_KEY = "continuation/config.toml"
AUDIT_EFFECT_ID = "effect:continuation-audit"
READ_EFFECT_ID = "effect:continuation-checkpoint-read"
MUTATION_EFFECT_ID = "effect:continuation-apply-promotion"
VERIFY_EFFECT_ID = "effect:continuation-terminal-read"
AUDIT_BINDING_ID = "binding:continuation-audit-r1"
READ_BINDING_ID = "binding:continuation-checkpoint-read-r1"
MUTATION_BINDING_ID = "binding:continuation-apply-r1"
VERIFY_BINDING_ID = "binding:continuation-terminal-read-r1"
ACTION_ID = "action:apply-config-promotion"
INITIAL_CONTENT = (
    "# Agent-native continuation fixture\n"
    "mode = candidate\n"
    "owner = agent-native-computing\n"
)
TERMINAL_CONTENT = (
    "# Agent-native continuation fixture\n"
    "mode = enabled\n"
    "owner = agent-native-computing\n"
)
DECISION: dict[str, JsonValue] = {
    "decisionId": "decision:preserve-config-layout",
    "statement": "Promote only mode=candidate to mode=enabled.",
    "consequence": "Preserve the comment, owner line, ordering, and final newline; use a guarded mutation.",
    "forbiddenActions": [
        "repeat-effect:continuation-audit",
        "rewrite-unrelated-lines",
        "mutate-without-world-version-check",
    ],
}


@dataclass(frozen=True, slots=True)
class FrozenCheckpoint:
    root: Path
    capsule_digest: str
    source_revision: str
    initial_digest: str
    terminal_digest: str
    manifest_path: Path


class StepClock:
    def __init__(self, start: int = 1_000) -> None:
        self.current = start

    def __call__(self) -> int:
        value = self.current
        self.current += 1
        return value


def sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def experiments_root() -> Path:
    return Path(__file__).resolve().parents[3]


def contract_fixture(name: str) -> ToolContract:
    path = experiments_root() / "external-semantic-contract-v0" / "fixtures" / "contracts" / name
    return normalize_tool_contract(json.loads(path.read_text()))


def protocol_authorities() -> tuple[ProtocolAuthority, ProtocolAuthority]:
    effect = ProtocolAuthority(
        authority_id="authority:continuation-effect",
        issuer_id="principal:continuation-issuer",
        principal_id="principal:continuation-host",
        role="effect",
        trust_domain="anc-continuation-v0",
        policy_version="continuation-authority-v1",
        key_id="continuation-effect-key-v1",
        secret=b"continuation-effect-authority-v1"[:32],
    )
    binding = ProtocolAuthority(
        authority_id="authority:continuation-binding",
        issuer_id="principal:continuation-issuer",
        principal_id="principal:continuation-binding-service",
        role="binding",
        trust_domain="anc-continuation-v0",
        policy_version="continuation-authority-v1",
        key_id="continuation-binding-key-v1",
        secret=b"continuation-binding-authority-v1"[:32],
    )
    return effect, binding


def sign_effect(
    effect: EffectEnvelope, authority: ProtocolAuthority, *, issued_at_ms: int
) -> SignedEffectEnvelope:
    return SignedEffectEnvelope(
        effect,
        authority.attest(
            kind="effect_proposal",
            contract_version="effect-envelope-v1",
            subject_digest=effect_digest(effect),
            issued_at_ms=issued_at_ms,
        ),
    )


def effect_envelope(
    effect_id: str,
    action: str,
    *,
    version: str | None = None,
    content: str | None = None,
) -> EffectEnvelope:
    target_id = str(simulator_object_id(OBJECT_KEY))
    if action == "anc.execution.launch.v1":
        value: JsonValue = {"executable": "anc.audit", "args": ["preserve-layout"]}
        result = ResultSemantics(
            ExecutionKind.ASYNCHRONOUS, CompletionKind.TERMINAL_OBSERVATION
        )
        mode = EffectMode.CHANGE
    elif action == "anc.object.replace-if-version.v1":
        if content is None:
            raise ValueError("mutation Effect requires content")
        value = {"content": content}
        result = ResultSemantics(ExecutionKind.SYNCHRONOUS, CompletionKind.RESPONSE)
        mode = EffectMode.CHANGE
    elif action == "anc.object.read.v1":
        value = {}
        result = ResultSemantics(
            ExecutionKind.SYNCHRONOUS, CompletionKind.ACCEPTED_VERIFICATION
        )
        mode = EffectMode.OBSERVE
    else:
        raise ValueError("unsupported continuation semantic action")
    target = TargetRef(target_id, version)
    return EffectEnvelope(
        effect_id=effect_id,
        target=target,
        mode=mode,
        action=SemanticAction(action, "anc.continuation-input.v1"),
        input=CanonicalInput(value),
        capability=CapabilityRequirement(
            "principal:continuation-host", action, target.object_id
        ),
        delivery=DeliverySemantics(IdempotencyKind.NATURAL),
        result=result,
        verification=VerificationPlan(
            "independent-reread-digest.v1", (EvidenceKind.OBSERVATION,)
        ),
    )


def exact_read_binding(
    effect: EffectEnvelope, contract: ToolContract, request: SimulatorRead, *, binding_id: str
):
    return bind_effect(
        effect,
        contract,
        encoder_id="anc.binding.simulator.continuation-read",
        binding_id=binding_id,
        revision=1,
        arguments={"method": "fetch", "object": request.object_key},
    )


def exact_mutation_binding(
    effect: EffectEnvelope,
    contract: ToolContract,
    request: SimulatorMutation,
    *,
    binding_id: str,
):
    return bind_effect(
        effect,
        contract,
        encoder_id="anc.binding.simulator.continuation-mutation",
        binding_id=binding_id,
        revision=1,
        arguments={
            "method": "replace_if_version",
            "object": request.object_key,
            "expected": request.expected_version,
            "contentDigest": sha256_text(request.content),
        },
    )


def exact_job_binding(
    effect: EffectEnvelope,
    contract: ToolContract,
    request: SimulatorJobRequest,
    *,
    binding_id: str,
):
    correlation = hashlib.sha256(effect.effect_id.encode("utf-8")).hexdigest()[:32]
    return bind_effect(
        effect,
        contract,
        encoder_id="anc.binding.simulator.continuation-job",
        binding_id=binding_id,
        revision=1,
        arguments={
            "method": "launch",
            "correlation": f"sim-correlation-{correlation}",
            "object": request.object_key,
            "action": request.action,
            "statusPlan": [status.value for status in request.status_plan],
            "artifacts": [
                {
                    "name": artifact.name,
                    "kind": artifact.kind,
                    "digest": artifact.digest,
                    "bytes": len(artifact.content),
                }
                for artifact in request.artifacts
            ],
        },
    )


def _dispatch_snapshot(record: Any) -> dict[str, JsonValue]:
    return {
        "dispatchId": str(record.dispatch_id),
        "effectId": str(record.effect_id),
        "requestDigest": record.request_digest,
        "state": record.state.value,
        "startedAtMs": record.started_at_ms,
        "updatedAtMs": record.updated_at_ms,
        "backendOperationId": record.backend_operation_id,
        "bindingId": None if record.binding_id is None else str(record.binding_id),
        "bindingDigest": record.binding_digest,
    }


def _effect_ref(
    store: FileObjectStore,
    signed_effect: SignedEffectEnvelope,
    record: Any,
) -> SemanticRef:
    payload: JsonValue = {
        "effectDigest": effect_digest(signed_effect.envelope),
        "state": record.state.value,
        "revision": record.revision,
        "dispatchId": None if record.dispatch_id is None else str(record.dispatch_id),
        "signedEffect": signed_effect.to_dict(),
    }
    return store.put_semantic("effect", signed_effect.envelope.effect_id, payload)


def _binding_ref(
    store: FileObjectStore,
    signed_binding: SignedEffectBinding,
    *,
    state: str,
) -> SemanticRef:
    payload: JsonValue = {
        "state": state,
        "bindingDigest": binding_digest(signed_binding.binding),
        "signedBinding": signed_binding.to_dict(),
    }
    return store.put_semantic("binding", signed_binding.binding.binding_id, payload)


def _artifact_ref(
    store: FileObjectStore, artifact: Any, *, content: bytes
) -> SemanticRef:
    if artifact.digest != "sha256:" + hashlib.sha256(content).hexdigest():
        raise AssertionError("Artifact metadata digest differs from content")
    payload: JsonValue = {
        "effectId": str(artifact.effect_id),
        "dispatchId": str(artifact.dispatch_id),
        "artifactKind": artifact.kind,
        "digest": artifact.digest,
        "mediaType": artifact.media_type,
        "byteLength": artifact.byte_length,
        "contentEncoding": "utf-8",
        "content": content.decode("utf-8"),
    }
    return store.put_semantic("artifact", str(artifact.artifact_id), payload)


def _fact_ref(store: FileObjectStore, result: DigestFactResult) -> SemanticRef:
    if result.fact is None:
        raise AssertionError("checkpoint Fact was not accepted")
    payload: JsonValue = {
        "claimId": str(result.claim.claim_id),
        "originEffectId": str(result.claim.origin_effect_id),
        "predicate": result.claim.predicate,
        "valueDigest": result.claim.value_digest,
        "verificationId": str(result.verification.verification_id),
        "decision": result.verification.decision.value,
        "factId": str(result.fact.fact_id),
        "acceptedAtMs": result.fact.accepted_at_ms,
    }
    return store.put_semantic("fact", str(result.fact.fact_id), payload)


def _write_json(path: Path, value: JsonValue) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def freeze_checkpoint(output_root: str | Path, *, source_revision: str) -> FrozenCheckpoint:
    root = Path(output_root)
    if root.exists():
        shutil.rmtree(root)
    (root / "world").mkdir(parents=True)
    (root / "baselines").mkdir(parents=True)
    store = FileObjectStore(root / "objects")
    binding_store = FileBindingStore(root / "bindings")
    effect_authority, binding_authority = protocol_authorities()
    binding_service = BindingAuthorityService(
        effect_authority=effect_authority,
        binding_authority=binding_authority,
        store=binding_store,
    )
    views = reference_authority_views(namespace="continuation-checkpoint")
    backend = DeterministicBackend()
    backend.seed_object(OBJECT_KEY, INITIAL_CONTENT)
    clock = StepClock()
    initial_digest = sha256_text(INITIAL_CONTENT)
    terminal_digest = sha256_text(TERMINAL_CONTENT)
    (root / WORLD_RELATIVE_PATH).write_text(INITIAL_CONTENT)

    audit_effect = effect_envelope(AUDIT_EFFECT_ID, "anc.execution.launch.v1")
    signed_audit = sign_effect(audit_effect, effect_authority, issued_at_ms=clock())
    decision_content = canonical_bytes(DECISION)
    audit_request = SimulatorJobRequest(
        OBJECT_KEY,
        "audit-preserve-layout",
        (SimulatorStatus.COMPLETE,),
        artifacts=(
            SimulatorArtifact(
                "continuation-decision.json",
                "decision",
                decision_content,
                "application/json",
            ),
        ),
    )
    audit_contract = contract_fixture("simulator-job-launch.json")
    audit_binding = exact_job_binding(
        audit_effect, audit_contract, audit_request, binding_id=AUDIT_BINDING_ID
    )
    audit_projection, audit_admission = admit_bound_effect(
        views,
        signed_audit,
        audit_contract,
        audit_binding,
        binding_service,
        backend_target=simulator_object_id(OBJECT_KEY),
        event_namespace="continuation-audit",
        admitted_at_ms=clock(),
    )
    audit_signed_binding = binding_service.resolve(audit_admission)
    audit_result = DeterministicBackendAdapter(
        BoundExecutionView(views.execution, audit_admission, audit_signed_binding.binding),
        backend,
        clock_ms=clock,
    ).dispatch_job(audit_projection.effect_id, audit_request)
    if audit_result.state is not EffectState.SUCCEEDED or len(audit_result.artifacts) != 1:
        raise AssertionError("audit checkpoint Effect did not succeed with one Artifact")
    audit_record = views.read.get_effect(audit_projection.effect_id)
    audit_dispatch = views.read.get_dispatch(audit_result.dispatch_id)
    audit_effect_ref = _effect_ref(store, signed_audit, audit_record)
    store.put_semantic("dispatch", str(audit_dispatch.dispatch_id), _dispatch_snapshot(audit_dispatch))
    decision_ref = _artifact_ref(
        store, audit_result.artifacts[0], content=decision_content
    )

    read_effect = effect_envelope(
        READ_EFFECT_ID, "anc.object.read.v1", version=initial_digest
    )
    signed_read = sign_effect(read_effect, effect_authority, issued_at_ms=clock())
    read_request = SimulatorRead(OBJECT_KEY)
    read_contract = contract_fixture("simulator-object-read.json")
    read_binding = exact_read_binding(
        read_effect, read_contract, read_request, binding_id=READ_BINDING_ID
    )
    read_projection, read_admission = admit_bound_effect(
        views,
        signed_read,
        read_contract,
        read_binding,
        binding_service,
        backend_target=simulator_object_id(OBJECT_KEY),
        event_namespace="continuation-checkpoint-read",
        admitted_at_ms=clock(),
    )
    read_signed_binding = binding_service.resolve(read_admission)
    read_result = DeterministicBackendAdapter(
        BoundExecutionView(views.execution, read_admission, read_signed_binding.binding),
        backend,
        clock_ms=clock,
    ).dispatch_read(read_projection.effect_id, read_request)
    if read_result.state is not EffectState.SUCCEEDED or read_result.observation is None:
        raise AssertionError("checkpoint reread did not succeed")
    fact_result = verify_digest_fact(
        views.verification,
        views.facts,
        claim_effect_id=audit_projection.effect_id,
        observation=read_result.observation,
        expected_digest=initial_digest,
        verified_at_ms=clock(),
        accepted_at_ms=clock(),
    )
    read_record = views.read.get_effect(read_projection.effect_id)
    read_dispatch = views.read.get_dispatch(read_result.dispatch_id)
    read_effect_ref = _effect_ref(store, signed_read, read_record)
    store.put_semantic("dispatch", str(read_dispatch.dispatch_id), _dispatch_snapshot(read_dispatch))
    fact_ref = _fact_ref(store, fact_result)

    mutation_effect = effect_envelope(
        MUTATION_EFFECT_ID,
        "anc.object.replace-if-version.v1",
        version=initial_digest,
        content=TERMINAL_CONTENT,
    )
    signed_mutation = sign_effect(
        mutation_effect, effect_authority, issued_at_ms=clock()
    )
    mutation_request = SimulatorMutation(OBJECT_KEY, initial_digest, TERMINAL_CONTENT)
    mutation_contract = contract_fixture("simulator-object-mutate.json")
    mutation_binding = exact_mutation_binding(
        mutation_effect,
        mutation_contract,
        mutation_request,
        binding_id=MUTATION_BINDING_ID,
    )
    mutation_artifact = binding_service.authorize(
        signed_mutation, mutation_contract, mutation_binding, issued_at_ms=clock()
    )
    pending_effect_ref = store.put_semantic(
        "effect",
        mutation_effect.effect_id,
        {
            "effectDigest": effect_digest(mutation_effect),
            "state": "proposed",
            "signedEffect": signed_mutation.to_dict(),
            "contract": mutation_contract.to_dict(),
        },
    )
    mutation_binding_ref = _binding_ref(
        store, mutation_artifact.signed_binding, state="selected"
    )

    goal = GoalSpec(
        GOAL_ID,
        "Promote the continuation fixture from candidate to enabled without changing unrelated bytes.",
        {
            "worldId": WORLD_ID,
            "relativePath": WORLD_RELATIVE_PATH,
            "terminalDigest": terminal_digest,
            "requiredFactPredicate": "content_digest_equals",
            "requiredDecisionArtifact": decision_ref.semantic_id,
        },
    )
    capsule = TaskCapsule(
        task_id=TASK_ID,
        capsule_revision=1,
        supersedes_digest=None,
        goal=goal,
        phase=TaskPhase.READY,
        world=WorldBinding(
            WORLD_ID,
            source_revision,
            WORLD_RELATIVE_PATH,
            initial_digest,
            terminal_digest,
        ),
        completed_effects=(audit_effect_ref, read_effect_ref),
        current_bindings=(mutation_binding_ref,),
        unresolved_dispatches=(),
        facts=(fact_ref,),
        artifacts=(decision_ref,),
        open_questions=(),
        blockers=(),
        next_ready=(
            ReadyAction(
                ACTION_ID,
                ActionKind.APPLY_GUARDED_MUTATION,
                pending_effect_ref,
                mutation_binding_ref,
                initial_digest,
                terminal_digest,
            ),
        ),
        checkpoint_id=CHECKPOINT_ID,
    )
    capsule_digest_value = store.put_capsule(capsule)

    full_transcript: JsonValue = {
        "schemaVersion": 1,
        "kind": "anc.full-transcript-baseline",
        "messages": [
            {
                "role": "user",
                "content": "Inspect the fixture, preserve its layout, then promote candidate to enabled and verify the result.",
            },
            {
                "role": "assistant",
                "content": "I will audit the file before changing it.",
            },
            {
                "role": "tool",
                "name": "semantic.audit",
                "payload": store.resolve_semantic(audit_effect_ref),
            },
            {
                "role": "tool",
                "name": "semantic.fact",
                "payload": store.resolve_semantic(fact_ref),
            },
            {
                "role": "assistant",
                "content": "Decision retained: change only the mode value with a guarded mutation; audit is complete; next action is apply-config-promotion.",
            },
        ],
        "nextAction": ACTION_ID,
        "worldDigest": initial_digest,
    }
    manual_handoff: JsonValue = {
        "schemaVersion": 1,
        "kind": "anc.manual-handoff-baseline",
        "taskId": TASK_ID,
        "goalDigest": goal.digest,
        "worldDigest": initial_digest,
        "completedEffects": [AUDIT_EFFECT_ID, READ_EFFECT_ID],
        "decision": DECISION,
        "nextAction": ACTION_ID,
        "terminalDigest": terminal_digest,
    }
    no_memory: JsonValue = {
        "schemaVersion": 1,
        "kind": "anc.no-memory-baseline",
        "taskId": TASK_ID,
        "worldPath": WORLD_RELATIVE_PATH,
    }
    _write_json(root / "baselines" / "full-transcript.json", full_transcript)
    _write_json(root / "baselines" / "manual-handoff.json", manual_handoff)
    _write_json(root / "baselines" / "no-memory.json", no_memory)
    rubric: JsonValue = {
        "schemaVersion": 1,
        "kind": "anc.continuation-rubric",
        "expectedFirstAction": ACTION_ID,
        "forbiddenRepeatedEffects": [AUDIT_EFFECT_ID, READ_EFFECT_ID],
        "requiredDecisionArtifact": decision_ref.semantic_id,
        "requiredCheckpointFact": fact_ref.semantic_id,
        "initialWorldDigest": initial_digest,
        "terminalWorldDigest": terminal_digest,
        "terminalContent": TERMINAL_CONTENT,
        "success": {
            "taskPhase": "complete",
            "newMutationEffect": MUTATION_EFFECT_ID,
            "independentReadEffect": VERIFY_EFFECT_ID,
            "factPredicate": "content_digest_equals",
        },
    }
    _write_json(root / "rubric.json", rubric)
    manifest: JsonValue = {
        "schemaVersion": 1,
        "kind": "anc.continuation-checkpoint",
        "sourceRevision": source_revision,
        "capsuleDigest": capsule_digest_value,
        "objectStore": "objects",
        "bindingStore": "bindings",
        "worldPath": WORLD_RELATIVE_PATH,
        "rubricPath": "rubric.json",
        "baselines": {
            "fullTranscript": "baselines/full-transcript.json",
            "manualHandoff": "baselines/manual-handoff.json",
            "noMemory": "baselines/no-memory.json",
        },
    }
    manifest_path = root / "manifest.json"
    _write_json(manifest_path, manifest)
    return FrozenCheckpoint(
        root=root,
        capsule_digest=capsule_digest_value,
        source_revision=source_revision,
        initial_digest=initial_digest,
        terminal_digest=terminal_digest,
        manifest_path=manifest_path,
    )


def load_manifest(root: str | Path) -> dict[str, Any]:
    value = json.loads((Path(root) / "manifest.json").read_text())
    if not isinstance(value, dict):
        raise ValueError("continuation manifest must be an object")
    return value


def baseline_receipt(root: str | Path) -> dict[str, JsonValue]:
    checkpoint = Path(root)
    manifest = load_manifest(checkpoint)
    rubric = json.loads((checkpoint / str(manifest["rubricPath"])).read_text())
    expected = rubric["expectedFirstAction"]
    forbidden = set(rubric["forbiddenRepeatedEffects"])
    results: list[JsonValue] = []
    baselines = manifest["baselines"]
    for name, relative in sorted(baselines.items()):
        path = checkpoint / relative
        value = json.loads(path.read_text())
        encoded = path.read_bytes()
        if name == "fullTranscript":
            action = value["nextAction"]
            completed = {
                item
                for message in value["messages"]
                if message.get("role") == "tool"
                for item in (
                    [message["payload"].get("signedEffect", {}).get("envelope", {}).get("effectId")]
                    if isinstance(message.get("payload"), dict)
                    else []
                )
                if item
            }
            knows_decision = "guarded mutation" in value["messages"][-1]["content"]
        elif name == "manualHandoff":
            action = value["nextAction"]
            completed = set(value["completedEffects"])
            knows_decision = bool(value.get("decision"))
        else:
            action = "action:repeat-continuation-audit"
            completed = set()
            knows_decision = False
        repeated = sorted(forbidden & ({AUDIT_EFFECT_ID} if action.endswith("audit") else set()))
        results.append(
            {
                "baseline": name,
                "bytes": len(encoded),
                "firstAction": action,
                "correctFirstAction": action == expected,
                "knowsDecision": knows_decision,
                "knownCompletedEffects": sorted(completed),
                "repeatedCompletedEffects": repeated,
            }
        )
    return {
        "schemaVersion": 1,
        "kind": "anc.continuation-baseline-receipt",
        "sourceRevision": manifest["sourceRevision"],
        "capsuleDigest": manifest["capsuleDigest"],
        "expectedFirstAction": expected,
        "results": results,
    }
