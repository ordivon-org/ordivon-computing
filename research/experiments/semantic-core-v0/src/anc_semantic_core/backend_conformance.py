from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from typing import Any, Protocol

from .authority import AuthorityRole
from .bootstrap import KernelAuthorityViews
from .identity import SemanticId
from .model import Artifact, EventKind, Observation, VerificationDecision
from .state import EffectState
from .verification import verify_digest_fact


class PortableJobPhase(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class PortableProjection:
    state: EffectState
    dispatch_id: SemanticId
    observation: Observation | None
    artifacts: tuple[Artifact, ...]
    error_code: str | None = None


class BackendPortabilityDriver(Protocol):
    name: str
    views: KernelAuthorityViews

    def seed_object(self, object_key: str, content: str) -> None: ...

    def object_content(self, object_key: str) -> str: ...

    def object_version(self, object_key: str) -> str: ...

    def prepare_read(
        self, name: str, object_key: str, *, version: str | None
    ) -> SemanticId: ...

    def prepare_mutation(
        self, name: str, object_key: str, *, expected_version: str
    ) -> SemanticId: ...

    def prepare_job(self, name: str, object_key: str) -> SemanticId: ...

    def dispatch_read(
        self, effect_id: SemanticId, object_key: str
    ) -> PortableProjection: ...

    def dispatch_mutation(
        self,
        effect_id: SemanticId,
        object_key: str,
        *,
        expected_version: str,
        content: str,
    ) -> PortableProjection: ...

    def dispatch_job(
        self,
        effect_id: SemanticId,
        object_key: str,
        *,
        phases: tuple[PortableJobPhase, ...],
        lose_response: bool = False,
        artifact: bool = False,
        inspection_failures: int = 0,
    ) -> PortableProjection: ...

    def observe_job(self, effect_id: SemanticId) -> PortableProjection: ...

    def reconcile_job(
        self, effect_id: SemanticId, *, restart_adapter: bool
    ) -> PortableProjection: ...

    def cancel_job(self, effect_id: SemanticId) -> PortableProjection: ...

    def delivery_count(self, effect_id: SemanticId) -> int: ...


@dataclass(frozen=True, slots=True)
class BackendPortabilityReport:
    mutation_state: EffectState
    read_state: EffectState
    stale_mutation_state: EffectState
    fact_decision: VerificationDecision
    fact_committed: bool
    success_state: EffectState
    success_events: tuple[EventKind, ...]
    success_observation_roles: tuple[AuthorityRole, ...]
    success_artifact_roles: tuple[AuthorityRole, ...]
    response_loss_initial_state: EffectState
    response_loss_recovered_state: EffectState
    response_loss_dispatch_preserved: bool
    response_loss_delivery_count: int
    response_loss_events: tuple[EventKind, ...]
    cancel_intent_state: EffectState
    cancel_terminal_state: EffectState
    cancel_events: tuple[EventKind, ...]
    broken_state: EffectState
    unrelated_state: EffectState
    backend_objects_leaked: bool


def run_backend_portability_conformance(
    driver: BackendPortabilityDriver,
) -> BackendPortabilityReport:
    object_key = "portable-object"
    before_content = "alpha\n"
    after_content = "beta\n"
    driver.seed_object(object_key, before_content)
    before_version = driver.object_version(object_key)

    mutation_id = driver.prepare_mutation(
        f"{driver.name}-mutation",
        object_key,
        expected_version=before_version,
    )
    mutation = driver.dispatch_mutation(
        mutation_id,
        object_key,
        expected_version=before_version,
        content=after_content,
    )
    _require_state(mutation.state, EffectState.SUCCEEDED, "guarded mutation")
    if mutation.observation is None:
        raise AssertionError("guarded mutation produced no Observation")
    after_version = driver.object_version(object_key)
    if mutation.observation.target.version != after_version:
        raise AssertionError("mutation Observation did not bind the resulting version")

    read_id = driver.prepare_read(
        f"{driver.name}-read",
        object_key,
        version=after_version,
    )
    read = driver.dispatch_read(read_id, object_key)
    _require_state(read.state, EffectState.SUCCEEDED, "versioned read")
    if read.observation is None:
        raise AssertionError("versioned read produced no Observation")
    if read.observation.target.version != after_version:
        raise AssertionError("read Observation did not bind the object version")

    fact_result = verify_digest_fact(
        driver.views.verification,
        driver.views.facts,
        claim_effect_id=mutation_id,
        observation=read.observation,
        expected_digest=after_version,
        verified_at_ms=90_000,
        accepted_at_ms=90_001,
    )
    if fact_result.verification.decision is not VerificationDecision.ACCEPTED:
        raise AssertionError("independent reread did not accept the digest claim")
    if fact_result.fact is None:
        raise AssertionError("accepted digest verification produced no Fact")

    stale_id = driver.prepare_mutation(
        f"{driver.name}-stale",
        object_key,
        expected_version=before_version,
    )
    stale = driver.dispatch_mutation(
        stale_id,
        object_key,
        expected_version=before_version,
        content="gamma\n",
    )
    _require_state(stale.state, EffectState.FAILED, "stale guarded mutation")
    if driver.object_content(object_key) != after_content:
        raise AssertionError("stale mutation changed the backend object")

    success_id = driver.prepare_job(f"{driver.name}-success", object_key)
    success = driver.dispatch_job(
        success_id,
        object_key,
        phases=(PortableJobPhase.SUCCEEDED,),
        artifact=True,
    )
    _require_state(success.state, EffectState.SUCCEEDED, "successful Job")
    if success.observation is None or len(success.artifacts) != 1:
        raise AssertionError("successful Job did not project Observation and Artifact")
    success_events = _event_kinds(driver, success_id)
    success_observation_roles = _observation_roles(driver, success_id)
    success_artifact_roles = _artifact_roles(driver, success_id)
    if success_observation_roles != (AuthorityRole.OBSERVATION,):
        raise AssertionError("Job Observation did not use Observation authority")
    if success_artifact_roles != (AuthorityRole.OBSERVATION,):
        raise AssertionError("Job Artifact did not use Observation authority")
    _require_dispatch_authority(driver, success_id)

    loss_id = driver.prepare_job(f"{driver.name}-loss", object_key)
    lost = driver.dispatch_job(
        loss_id,
        object_key,
        phases=(PortableJobPhase.RUNNING, PortableJobPhase.SUCCEEDED),
        lose_response=True,
    )
    _require_state(lost.state, EffectState.UNKNOWN, "response loss")
    original_dispatch = driver.views.read.get_effect(loss_id).dispatch_id
    if original_dispatch is None:
        raise AssertionError("response loss erased Dispatch identity")
    recovered = driver.reconcile_job(loss_id, restart_adapter=True)
    _require_state(recovered.state, EffectState.SUCCEEDED, "response-loss recovery")
    recovered_dispatch = driver.views.read.get_effect(loss_id).dispatch_id
    if driver.delivery_count(loss_id) != 1:
        raise AssertionError("ambiguous Dispatch was delivered more than once")
    _require_dispatch_authority(driver, loss_id)

    cancel_id = driver.prepare_job(f"{driver.name}-cancel", object_key)
    running = driver.dispatch_job(
        cancel_id,
        object_key,
        phases=(PortableJobPhase.RUNNING, PortableJobPhase.RUNNING),
    )
    _require_state(running.state, EffectState.RUNNING, "running Job")
    cancel_intent = driver.cancel_job(cancel_id)
    _require_state(
        cancel_intent.state,
        EffectState.CANCEL_REQUESTED,
        "cancellation intent",
    )
    cancelled = driver.observe_job(cancel_id)
    _require_state(cancelled.state, EffectState.CANCELLED, "observed cancellation")
    cancel_events = _event_kinds(driver, cancel_id)
    if cancel_events.index(EventKind.CANCELLATION_REQUESTED) > cancel_events.index(
        EventKind.EFFECT_CANCELLED
    ):
        raise AssertionError("cancellation outcome preceded cancellation intent")
    _require_dispatch_authority(driver, cancel_id)

    broken_id = driver.prepare_job(f"{driver.name}-broken", object_key)
    broken_initial = driver.dispatch_job(
        broken_id,
        object_key,
        phases=(PortableJobPhase.RUNNING, PortableJobPhase.SUCCEEDED),
        lose_response=True,
        inspection_failures=1,
    )
    _require_state(broken_initial.state, EffectState.UNKNOWN, "broken Job delivery")
    broken = driver.reconcile_job(broken_id, restart_adapter=True)
    _require_state(broken.state, EffectState.UNKNOWN, "broken Job recovery")

    unrelated_id = driver.prepare_job(f"{driver.name}-unrelated", object_key)
    unrelated = driver.dispatch_job(
        unrelated_id,
        object_key,
        phases=(PortableJobPhase.SUCCEEDED,),
    )
    _require_state(unrelated.state, EffectState.SUCCEEDED, "unrelated Job")
    if driver.delivery_count(broken_id) != 1:
        raise AssertionError("broken Job was silently redispatched")

    driver.views.read.validate_invariants()
    leaked = _contains_backend_object(driver.views.read.state_snapshot())
    if leaked:
        raise AssertionError("backend implementation object leaked into Kernel state")

    return BackendPortabilityReport(
        mutation_state=mutation.state,
        read_state=read.state,
        stale_mutation_state=stale.state,
        fact_decision=fact_result.verification.decision,
        fact_committed=fact_result.fact is not None,
        success_state=success.state,
        success_events=success_events,
        success_observation_roles=success_observation_roles,
        success_artifact_roles=success_artifact_roles,
        response_loss_initial_state=lost.state,
        response_loss_recovered_state=recovered.state,
        response_loss_dispatch_preserved=original_dispatch == recovered_dispatch,
        response_loss_delivery_count=driver.delivery_count(loss_id),
        response_loss_events=_event_kinds(driver, loss_id),
        cancel_intent_state=cancel_intent.state,
        cancel_terminal_state=cancelled.state,
        cancel_events=cancel_events,
        broken_state=broken.state,
        unrelated_state=unrelated.state,
        backend_objects_leaked=leaked,
    )


def _require_state(actual: EffectState, expected: EffectState, label: str) -> None:
    if actual is not expected:
        raise AssertionError(f"{label} expected {expected.value}, found {actual.value}")


def _event_kinds(
    driver: BackendPortabilityDriver, effect_id: SemanticId
) -> tuple[EventKind, ...]:
    return tuple(event.kind for event in driver.views.read.events_for(effect_id))


def _observation_roles(
    driver: BackendPortabilityDriver, effect_id: SemanticId
) -> tuple[AuthorityRole, ...]:
    roles: list[AuthorityRole] = []
    for observation in driver.views.read.observations_for(effect_id):
        if observation.attestation is None:
            raise AssertionError("official Observation has no Attestation")
        roles.append(observation.attestation.authority.role)
    return tuple(roles)


def _artifact_roles(
    driver: BackendPortabilityDriver, effect_id: SemanticId
) -> tuple[AuthorityRole, ...]:
    roles: list[AuthorityRole] = []
    for artifact in driver.views.read.artifacts_for(effect_id):
        if artifact.attestation is None:
            raise AssertionError("official Artifact has no Attestation")
        roles.append(artifact.attestation.authority.role)
    return tuple(roles)


def _require_dispatch_authority(
    driver: BackendPortabilityDriver, effect_id: SemanticId
) -> None:
    execution_events = driver.views.read.events_for(effect_id)[2:]
    if not execution_events:
        raise AssertionError("execution scenario has no backend events")
    if any(
        event.attestation.authority.role is not AuthorityRole.DISPATCH
        for event in execution_events
    ):
        raise AssertionError("backend event crossed the Dispatch authority boundary")


def _contains_backend_object(value: Any) -> bool:
    module = type(value).__module__
    if module.endswith(".ordivon") or module.endswith(".ordivon_io") or module.endswith(
        ".simulator"
    ):
        return True
    if is_dataclass(value) and not isinstance(value, type):
        return any(
            _contains_backend_object(getattr(value, field.name)) for field in fields(value)
        )
    if isinstance(value, dict):
        return any(
            _contains_backend_object(key) or _contains_backend_object(item)
            for key, item in value.items()
        )
    if isinstance(value, (tuple, list, set, frozenset)):
        return any(_contains_backend_object(item) for item in value)
    return False
