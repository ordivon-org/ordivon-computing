from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from anc_canonical import JsonValue
from anc_effect_binding import FileBindingStore
from integration import BindingAuthorityService, BoundExecutionView, admit_bound_effect
from anc_semantic_core.simulator import (
    DeterministicBackend,
    DeterministicBackendAdapter,
    SimulatorMutation,
    SimulatorRead,
    simulator_object_id,
)
from anc_semantic_core.state import EffectState
from anc_semantic_core.testing import reference_authority_views
from anc_semantic_core.verification import verify_digest_fact

from .adapters import ModelAdapter, ModelDecision
from .context import CompiledContext, ContextCompiler
from .model import ActionKind, TaskCapsule, TaskPhase, WorldBinding, capsule_digest
from .store import FileObjectStore
from .validation import CapsuleValidator, ResolvedAction, ValidationReport
from .workload import (
    OBJECT_KEY,
    VERIFY_BINDING_ID,
    VERIFY_EFFECT_ID,
    StepClock,
    _binding_ref,
    _dispatch_snapshot,
    _effect_ref,
    _fact_ref,
    contract_fixture,
    effect_envelope,
    exact_read_binding,
    protocol_authorities,
    sha256_text,
    sign_effect,
)


class HostError(RuntimeError):
    pass


class HostInterrupted(HostError):
    pass


class HostDecisionRejected(HostError):
    pass


@dataclass(frozen=True, slots=True)
class HostReceipt:
    status: str
    adapter_id: str
    capsule_before: str
    capsule_after: str | None
    context_digest: str
    context_bytes: int
    decision: ModelDecision
    world_before: str
    world_after: str
    executed_effects: tuple[str, ...]
    committed_facts: tuple[str, ...]

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "schemaVersion": 1,
            "kind": "anc.fresh-host-receipt",
            "status": self.status,
            "adapterId": self.adapter_id,
            "capsuleBefore": self.capsule_before,
            "capsuleAfter": self.capsule_after,
            "contextDigest": self.context_digest,
            "contextBytes": self.context_bytes,
            "decision": self.decision.to_dict(),
            "worldBefore": self.world_before,
            "worldAfter": self.world_after,
            "executedEffects": list(self.executed_effects),
            "committedFacts": list(self.committed_facts),
        }


class FreshHost:
    """One replaceable Host process that continues from Capsule plus current world."""

    def __init__(
        self,
        checkpoint_root: str | Path,
        model: ModelAdapter,
    ) -> None:
        self.checkpoint_root = Path(checkpoint_root)
        self.store = FileObjectStore(self.checkpoint_root / "objects")
        self.model = model
        self.validator = CapsuleValidator(self.store)
        self.compiler = ContextCompiler()

    def run(
        self,
        capsule_digest_value: str,
        *,
        world_root: str | Path | None = None,
        stop_before_model: bool = False,
    ) -> HostReceipt:
        capsule = self.store.get_capsule(capsule_digest_value)
        active_world_root = self.checkpoint_root if world_root is None else Path(world_root)
        report = self.validator.validate(capsule, world_root=active_world_root)
        context = self.compiler.compile(capsule, report)
        if stop_before_model:
            raise HostInterrupted("fresh Host stopped before the model call")
        decision = self.model.decide(context)
        self._validate_decision(capsule, context, decision)
        if decision.kind is ActionKind.REFRESH_WORLD:
            return self._block_for_world_drift(
                capsule_digest_value,
                capsule,
                report,
                context,
                decision,
            )
        if decision.kind is ActionKind.OBSERVE_DISPATCH:
            return self._block_for_observation(
                capsule_digest_value,
                capsule,
                report,
                context,
                decision,
            )
        action = self._resolved_action(report, decision)
        return self._execute_mutation(
            capsule_digest_value,
            capsule,
            report,
            context,
            decision,
            action,
            active_world_root,
        )

    def _validate_decision(
        self,
        capsule: TaskCapsule,
        context: CompiledContext,
        decision: ModelDecision,
    ) -> None:
        allowed = context.payload["allowedActions"]
        if not isinstance(allowed, list):
            raise HostDecisionRejected("compiled context has no allowed action list")
        matches = [
            item
            for item in allowed
            if isinstance(item, dict)
            and item.get("actionId") == decision.action_id
            and item.get("kind") == decision.kind.value
            and item.get("effectId") == decision.effect_id
            and item.get("bindingId") == decision.binding_id
            and item.get("dispatchId") == decision.dispatch_id
        ]
        if len(matches) != 1:
            raise HostDecisionRejected("model decision is not one exact allowed action")
        completed = {ref.semantic_id for ref in capsule.completed_effects}
        if decision.effect_id is not None and decision.effect_id in completed:
            raise HostDecisionRejected("model attempted to repeat a completed Effect")

    def _resolved_action(
        self, report: ValidationReport, decision: ModelDecision
    ) -> ResolvedAction:
        matches = [
            item
            for item in report.resolved_actions
            if item.action.action_id == decision.action_id
            and item.action.effect.semantic_id == decision.effect_id
            and item.action.binding.semantic_id == decision.binding_id
        ]
        if len(matches) != 1:
            raise HostDecisionRejected("model decision has no resolved executable Binding")
        return matches[0]

    def _block_for_world_drift(
        self,
        old_digest: str,
        capsule: TaskCapsule,
        report: ValidationReport,
        context: CompiledContext,
        decision: ModelDecision,
    ) -> HostReceipt:
        blocked = replace(
            capsule,
            capsule_revision=capsule.capsule_revision + 1,
            supersedes_digest=old_digest,
            phase=TaskPhase.BLOCKED,
            world=capsule.world,
            blockers=(f"world-drift:{report.current_world_digest}",),
            next_ready=(),
            checkpoint_id="checkpoint:world-drift",
        )
        new_digest = self.store.put_capsule(blocked)
        return HostReceipt(
            status="blocked-world-drift",
            adapter_id=self.model.adapter_id,
            capsule_before=old_digest,
            capsule_after=new_digest,
            context_digest=context.digest,
            context_bytes=context.byte_length,
            decision=decision,
            world_before=capsule.world.observed_digest,
            world_after=report.current_world_digest,
            executed_effects=(),
            committed_facts=(),
        )

    def _block_for_observation(
        self,
        old_digest: str,
        capsule: TaskCapsule,
        report: ValidationReport,
        context: CompiledContext,
        decision: ModelDecision,
    ) -> HostReceipt:
        if decision.dispatch_id not in report.unresolved_dispatch_ids:
            raise HostDecisionRejected("observe decision targets another Dispatch")
        blocked = replace(
            capsule,
            capsule_revision=capsule.capsule_revision + 1,
            supersedes_digest=old_digest,
            phase=TaskPhase.BLOCKED,
            blockers=(f"observe-dispatch:{decision.dispatch_id}",),
            next_ready=(),
            checkpoint_id="checkpoint:unresolved-dispatch",
        )
        new_digest = self.store.put_capsule(blocked)
        return HostReceipt(
            status="blocked-observation-required",
            adapter_id=self.model.adapter_id,
            capsule_before=old_digest,
            capsule_after=new_digest,
            context_digest=context.digest,
            context_bytes=context.byte_length,
            decision=decision,
            world_before=report.current_world_digest,
            world_after=report.current_world_digest,
            executed_effects=(),
            committed_facts=(),
        )

    def _execute_mutation(
        self,
        old_digest: str,
        capsule: TaskCapsule,
        report: ValidationReport,
        context: CompiledContext,
        decision: ModelDecision,
        action: ResolvedAction,
        world_root: Path,
    ) -> HostReceipt:
        if report.world_status != "current":
            raise HostDecisionRejected("mutation is forbidden after world drift")
        input_value = action.signed_effect.envelope.input.value
        arguments = action.signed_binding.binding.arguments
        if not isinstance(input_value, dict) or not isinstance(arguments, dict):
            raise HostError("mutation Effect and Binding arguments must be objects")
        content = input_value.get("content")
        if not isinstance(content, str):
            raise HostError("mutation Effect has no string content")
        if arguments.get("object") != OBJECT_KEY:
            raise HostError("mutation Binding targets another world object")
        if arguments.get("expected") != report.current_world_digest:
            raise HostError("mutation Binding expected version differs from current world")
        if arguments.get("contentDigest") != sha256_text(content):
            raise HostError("mutation Binding content digest differs from Effect content")

        effect_authority, binding_authority = protocol_authorities()
        binding_service = BindingAuthorityService(
            effect_authority=effect_authority,
            binding_authority=binding_authority,
            store=FileBindingStore(self.checkpoint_root / "runtime-bindings"),
        )
        views = reference_authority_views(namespace="continuation-fresh-host")
        clock = StepClock(10_000)
        projection, admission = admit_bound_effect(
            views,
            action.signed_effect,
            action.contract,
            action.signed_binding.binding,
            binding_service,
            backend_target=simulator_object_id(OBJECT_KEY),
            event_namespace="continuation-host-mutation",
            admitted_at_ms=clock(),
        )
        runtime_binding = binding_service.resolve(admission)
        backend = DeterministicBackend()
        world_path = world_root / capsule.world.relative_path
        backend.seed_object(OBJECT_KEY, world_path.read_text())
        mutation_request = SimulatorMutation(OBJECT_KEY, report.current_world_digest, content)
        mutation_result = DeterministicBackendAdapter(
            BoundExecutionView(views.execution, admission, runtime_binding.binding),
            backend,
            clock_ms=clock,
        ).dispatch_mutation(projection.effect_id, mutation_request)
        if mutation_result.state is not EffectState.SUCCEEDED:
            raise HostError(f"guarded mutation did not succeed: {mutation_result.state}")
        mutated_content = backend.object_content(OBJECT_KEY)
        mutated_digest = sha256_text(mutated_content)
        if mutated_digest != action.action.expected_world_digest:
            raise HostError("guarded mutation produced another terminal digest")
        world_path.write_text(mutated_content)

        mutation_record = views.read.get_effect(projection.effect_id)
        mutation_dispatch = views.read.get_dispatch(mutation_result.dispatch_id)
        mutation_effect_ref = _effect_ref(
            self.store, action.signed_effect, mutation_record
        )
        self.store.put_semantic(
            "dispatch",
            str(mutation_dispatch.dispatch_id),
            _dispatch_snapshot(mutation_dispatch),
        )
        _binding_ref(self.store, runtime_binding, state="completed")

        verify_effect = effect_envelope(
            VERIFY_EFFECT_ID,
            "anc.object.read.v1",
            version=mutated_digest,
        )
        signed_verify = sign_effect(
            verify_effect, effect_authority, issued_at_ms=clock()
        )
        verify_contract = contract_fixture("simulator-object-read.json")
        verify_request = SimulatorRead(OBJECT_KEY)
        verify_binding = exact_read_binding(
            verify_effect,
            verify_contract,
            verify_request,
            binding_id=VERIFY_BINDING_ID,
        )
        verify_projection, verify_admission = admit_bound_effect(
            views,
            signed_verify,
            verify_contract,
            verify_binding,
            binding_service,
            backend_target=simulator_object_id(OBJECT_KEY),
            event_namespace="continuation-host-terminal-read",
            admitted_at_ms=clock(),
        )
        runtime_verify_binding = binding_service.resolve(verify_admission)
        verify_result = DeterministicBackendAdapter(
            BoundExecutionView(
                views.execution,
                verify_admission,
                runtime_verify_binding.binding,
            ),
            backend,
            clock_ms=clock,
        ).dispatch_read(verify_projection.effect_id, verify_request)
        if verify_result.state is not EffectState.SUCCEEDED or verify_result.observation is None:
            raise HostError("independent terminal reread did not succeed")
        fact_result = verify_digest_fact(
            views.verification,
            views.facts,
            claim_effect_id=projection.effect_id,
            observation=verify_result.observation,
            expected_digest=mutated_digest,
            verified_at_ms=clock(),
            accepted_at_ms=clock(),
        )
        verify_record = views.read.get_effect(verify_projection.effect_id)
        verify_dispatch = views.read.get_dispatch(verify_result.dispatch_id)
        verify_effect_ref = _effect_ref(self.store, signed_verify, verify_record)
        self.store.put_semantic(
            "dispatch",
            str(verify_dispatch.dispatch_id),
            _dispatch_snapshot(verify_dispatch),
        )
        terminal_fact_ref = _fact_ref(self.store, fact_result)

        complete = replace(
            capsule,
            capsule_revision=capsule.capsule_revision + 1,
            supersedes_digest=old_digest,
            phase=TaskPhase.COMPLETE,
            world=WorldBinding(
                capsule.world.world_id,
                capsule.world.source_revision,
                capsule.world.relative_path,
                mutated_digest,
                capsule.world.terminal_digest,
            ),
            completed_effects=(
                *capsule.completed_effects,
                mutation_effect_ref,
                verify_effect_ref,
            ),
            current_bindings=(),
            unresolved_dispatches=(),
            facts=(*capsule.facts, terminal_fact_ref),
            blockers=(),
            next_ready=(),
            checkpoint_id="checkpoint:terminal",
        )
        new_digest = self.store.put_capsule(complete)
        if capsule_digest(complete) != new_digest:
            raise HostError("final TaskCapsule digest differs from its store key")
        return HostReceipt(
            status="completed",
            adapter_id=self.model.adapter_id,
            capsule_before=old_digest,
            capsule_after=new_digest,
            context_digest=context.digest,
            context_bytes=context.byte_length,
            decision=decision,
            world_before=report.current_world_digest,
            world_after=mutated_digest,
            executed_effects=(str(projection.effect_id), str(verify_projection.effect_id)),
            committed_facts=(terminal_fact_ref.semantic_id,),
        )
