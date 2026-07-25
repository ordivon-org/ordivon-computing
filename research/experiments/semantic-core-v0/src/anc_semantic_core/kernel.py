from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace
from functools import wraps
from typing import Any, Callable, Iterator, Protocol, TypeVar

from .identity import IdKind, SemanticId
from .model import (
    Admission,
    Artifact,
    Claim,
    DispatchRecord,
    DispatchState,
    EffectEvent,
    EffectRecord,
    EffectSpec,
    EventKind,
    EvidenceKind,
    Fact,
    Observation,
    Verification,
    VerificationDecision,
    WorldObjectRef,
)
from .state import EffectState, can_transition


class SemanticError(RuntimeError):
    pass


class NotFound(SemanticError):
    pass


class IdentityConflict(SemanticError):
    pass


class RevisionConflict(SemanticError):
    pass


class InvalidTransition(SemanticError):
    pass


class InvariantViolation(SemanticError):
    pass


_Result = TypeVar("_Result")


def _atomic_mutation(
    method: Callable[..., _Result],
) -> Callable[..., _Result]:
    """Make one in-memory semantic command all-or-nothing."""

    @wraps(method)
    def wrapped(self: "ReferenceKernel", *args: Any, **kwargs: Any) -> _Result:
        before = self._snapshot()
        try:
            result = method(self, *args, **kwargs)
            self.validate_invariants()
            return result
        except BaseException:
            self._restore(before)
            raise

    return wrapped


class SemanticKernel(Protocol):
    def admit_effect(
        self, spec: EffectSpec, *, event_id: SemanticId, recorded_at_ms: int
    ) -> Admission: ...

    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
    ) -> EffectRecord: ...

    def begin_dispatch(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        dispatch_id: SemanticId,
        event_id: SemanticId,
        recorded_at_ms: int,
        request_digest: str,
    ) -> EffectRecord: ...

    def admit_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        backend_operation_id: str,
        evidence_digest: str,
    ) -> EffectRecord: ...

    def mark_dispatch_unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str,
    ) -> EffectRecord: ...

    def reject_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        reason_code: str,
        retryable: bool,
        evidence_digest: str,
    ) -> EffectRecord: ...

    def advance_effect(
        self,
        effect_id: SemanticId,
        target: EffectState,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str | None = None,
    ) -> EffectRecord: ...

    def get_effect(self, effect_id: SemanticId) -> EffectRecord: ...

    def get_dispatch(self, dispatch_id: SemanticId) -> DispatchRecord: ...

    def events_for(self, effect_id: SemanticId) -> tuple[EffectEvent, ...]: ...

    def get_observation(self, observation_id: SemanticId) -> Observation: ...

    def get_artifact(self, artifact_id: SemanticId) -> Artifact: ...

    def get_claim(self, claim_id: SemanticId) -> Claim: ...

    def get_verification(self, verification_id: SemanticId) -> Verification: ...

    def get_fact(self, fact_id: SemanticId) -> Fact: ...

    def record_observation(self, observation: Observation) -> Admission: ...

    def register_artifact(self, artifact: Artifact) -> Admission: ...

    def admit_claim(self, claim: Claim) -> Admission: ...

    def record_verification(self, verification: Verification) -> Admission: ...

    def commit_fact(self, fact: Fact) -> Admission: ...

    def validate_invariants(self) -> None: ...

    def transaction(self) -> Any: ...


_STATE_EVENT: dict[EffectState, EventKind] = {
    EffectState.PREPARED: EventKind.EFFECT_PREPARED,
    EffectState.RUNNING: EventKind.RUNNING_OBSERVED,
    EffectState.CANCEL_REQUESTED: EventKind.CANCELLATION_REQUESTED,
    EffectState.UNKNOWN: EventKind.OUTCOME_UNKNOWN,
    EffectState.RECONCILING: EventKind.RECONCILIATION_STARTED,
    EffectState.SUCCEEDED: EventKind.EFFECT_SUCCEEDED,
    EffectState.FAILED: EventKind.EFFECT_FAILED,
    EffectState.CANCELLED: EventKind.EFFECT_CANCELLED,
}

_EVIDENCE_REQUIRED = {
    EffectState.RUNNING,
    EffectState.CANCEL_REQUESTED,
    EffectState.UNKNOWN,
    EffectState.RECONCILING,
    EffectState.SUCCEEDED,
    EffectState.FAILED,
    EffectState.CANCELLED,
}


class ReferenceKernel:
    """In-memory executable reference model for Agent-native semantics."""

    def __init__(self) -> None:
        self._effects: dict[SemanticId, EffectRecord] = {}
        self._dispatches: dict[SemanticId, DispatchRecord] = {}
        self._events: dict[SemanticId, EffectEvent] = {}
        self._events_by_effect: dict[SemanticId, list[EffectEvent]] = {}
        self._observations: dict[SemanticId, Observation] = {}
        self._artifacts: dict[SemanticId, Artifact] = {}
        self._claims: dict[SemanticId, Claim] = {}
        self._verifications: dict[SemanticId, Verification] = {}
        self._facts: dict[SemanticId, Fact] = {}

    def _snapshot(self) -> tuple[dict[Any, Any], ...]:
        return (
            dict(self._effects),
            dict(self._dispatches),
            dict(self._events),
            {key: list(value) for key, value in self._events_by_effect.items()},
            dict(self._observations),
            dict(self._artifacts),
            dict(self._claims),
            dict(self._verifications),
            dict(self._facts),
        )

    def _restore(self, snapshot: tuple[dict[Any, Any], ...]) -> None:
        (
            self._effects,
            self._dispatches,
            self._events,
            self._events_by_effect,
            self._observations,
            self._artifacts,
            self._claims,
            self._verifications,
            self._facts,
        ) = snapshot

    def clone(self) -> "ReferenceKernel":
        cloned = ReferenceKernel()
        cloned._restore(self._snapshot())
        return cloned

    def state_snapshot(self) -> tuple[dict[Any, Any], ...]:
        """Return a detached equality-comparable state snapshot for tests and stores."""
        return self._snapshot()

    @contextmanager
    def transaction(self) -> Iterator["ReferenceKernel"]:
        before = self._snapshot()
        try:
            yield self
            self.validate_invariants()
        except BaseException:
            self._restore(before)
            raise

    @_atomic_mutation
    def admit_effect(
        self, spec: EffectSpec, *, event_id: SemanticId, recorded_at_ms: int
    ) -> Admission:
        event_id.require(IdKind.EVENT)
        self._require_time(recorded_at_ms)
        existing = self._effects.get(spec.effect_id)
        if existing is not None:
            if existing.spec == spec:
                return Admission.EXISTING
            raise IdentityConflict(f"effect identity conflict: {spec.effect_id}")
        self._require_new_event(event_id)
        record = EffectRecord(spec=spec, state=EffectState.PROPOSED, revision=0)
        event = EffectEvent(
            event_id=event_id,
            effect_id=spec.effect_id,
            sequence=0,
            kind=EventKind.EFFECT_ADMITTED,
            recorded_at_ms=recorded_at_ms,
        )
        self._effects[spec.effect_id] = record
        self._events[event_id] = event
        self._events_by_effect[spec.effect_id] = [event]
        return Admission.CREATED

    @_atomic_mutation
    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
    ) -> EffectRecord:
        return self._transition(
            effect_id,
            EffectState.PREPARED,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=None,
        )

    @_atomic_mutation
    def begin_dispatch(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        dispatch_id: SemanticId,
        event_id: SemanticId,
        recorded_at_ms: int,
        request_digest: str,
    ) -> EffectRecord:
        dispatch = DispatchRecord(
            dispatch_id=dispatch_id,
            effect_id=effect_id,
            request_digest=request_digest,
            state=DispatchState.STARTED,
            started_at_ms=recorded_at_ms,
            updated_at_ms=recorded_at_ms,
        )
        existing = self._dispatches.get(dispatch_id)
        if existing is not None:
            if existing == dispatch:
                raise InvalidTransition("dispatch is already started")
            raise IdentityConflict(f"dispatch identity conflict: {dispatch_id}")
        record = self._transition(
            effect_id,
            EffectState.DISPATCHED,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=request_digest,
            dispatch_id=dispatch_id,
            event_kind=EventKind.DISPATCH_STARTED,
        )
        self._dispatches[dispatch_id] = dispatch
        return record

    @_atomic_mutation
    def admit_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        backend_operation_id: str,
        evidence_digest: str,
    ) -> EffectRecord:
        if not backend_operation_id or not evidence_digest:
            raise ValueError("dispatch admission requires backend identity and evidence")
        record, dispatch = self._require_current_dispatch(
            effect_id, dispatch_id, expected_revision=expected_revision
        )
        if dispatch.state is DispatchState.ADMITTED:
            if dispatch.backend_operation_id == backend_operation_id:
                return record
            raise IdentityConflict("Dispatch is already bound to a different backend operation")
        if dispatch.state not in {DispatchState.STARTED, DispatchState.UNKNOWN}:
            raise InvalidTransition(f"cannot admit Dispatch from {dispatch.state.value}")
        self._dispatches[dispatch_id] = replace(
            dispatch,
            state=DispatchState.ADMITTED,
            updated_at_ms=recorded_at_ms,
            backend_operation_id=backend_operation_id,
            reason_code=None,
            retryable=None,
        )
        return self._append_effect_event(
            record,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            kind=EventKind.DISPATCH_ADMITTED,
            evidence_digest=evidence_digest,
            dispatch_id=dispatch_id,
        )

    @_atomic_mutation
    def mark_dispatch_unknown(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str,
    ) -> EffectRecord:
        if not evidence_digest:
            raise ValueError("unknown Dispatch requires evidence")
        record, dispatch = self._require_current_dispatch(
            effect_id, dispatch_id, expected_revision=expected_revision
        )
        if dispatch.state is DispatchState.REJECTED:
            raise InvalidTransition("rejected Dispatch cannot become unknown")
        self._dispatches[dispatch_id] = replace(
            dispatch,
            state=DispatchState.UNKNOWN,
            updated_at_ms=recorded_at_ms,
            reason_code=None,
            retryable=None,
        )
        if record.state is EffectState.UNKNOWN:
            return record
        return self._transition(
            effect_id,
            EffectState.UNKNOWN,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
        )

    @_atomic_mutation
    def reject_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        reason_code: str,
        retryable: bool,
        evidence_digest: str,
    ) -> EffectRecord:
        if not reason_code or not evidence_digest:
            raise ValueError("Dispatch rejection requires reason and evidence")
        record, dispatch = self._require_current_dispatch(
            effect_id, dispatch_id, expected_revision=expected_revision
        )
        if dispatch.state is DispatchState.ADMITTED or dispatch.backend_operation_id is not None:
            raise InvalidTransition(
                "Dispatch proven admitted cannot be reclassified as rejected"
            )
        if dispatch.state is DispatchState.REJECTED:
            if dispatch.reason_code == reason_code and dispatch.retryable is retryable:
                return record
            raise IdentityConflict("Dispatch rejection conflicts with existing outcome")
        self._dispatches[dispatch_id] = replace(
            dispatch,
            state=DispatchState.REJECTED,
            updated_at_ms=recorded_at_ms,
            backend_operation_id=None,
            reason_code=reason_code,
            retryable=retryable,
        )
        target = EffectState.PREPARED if retryable else EffectState.FAILED
        return self._append_effect_event(
            replace(record, state=target, dispatch_id=None),
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            kind=EventKind.DISPATCH_REJECTED,
            evidence_digest=evidence_digest,
            dispatch_id=dispatch_id,
            previous_record=record,
        )

    @_atomic_mutation
    def advance_effect(
        self,
        effect_id: SemanticId,
        target: EffectState,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str | None = None,
    ) -> EffectRecord:
        if target in {
            EffectState.PROPOSED,
            EffectState.PREPARED,
            EffectState.DISPATCHED,
            EffectState.UNKNOWN,
        }:
            raise InvalidTransition(f"use the dedicated operation for target state {target.value}")
        record = self.get_effect(effect_id)
        if record.dispatch_id is not None and target in {
            EffectState.RUNNING,
            EffectState.CANCEL_REQUESTED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.CANCELLED,
        }:
            dispatch = self.get_dispatch(record.dispatch_id)
            if dispatch.state is not DispatchState.ADMITTED:
                raise InvariantViolation(
                    f"transition to {target.value} requires an admitted Dispatch"
                )
        return self._transition(
            effect_id,
            target,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
        )

    def get_effect(self, effect_id: SemanticId) -> EffectRecord:
        effect_id.require(IdKind.EFFECT)
        record = self._effects.get(effect_id)
        if record is None:
            raise NotFound(f"effect not found: {effect_id}")
        return record

    def get_dispatch(self, dispatch_id: SemanticId) -> DispatchRecord:
        dispatch_id.require(IdKind.DISPATCH)
        record = self._dispatches.get(dispatch_id)
        if record is None:
            raise NotFound(f"dispatch not found: {dispatch_id}")
        return record

    def events_for(self, effect_id: SemanticId) -> tuple[EffectEvent, ...]:
        self.get_effect(effect_id)
        return tuple(self._events_by_effect[effect_id])

    def get_observation(self, observation_id: SemanticId) -> Observation:
        observation_id.require(IdKind.OBSERVATION)
        record = self._observations.get(observation_id)
        if record is None:
            raise NotFound(f"observation not found: {observation_id}")
        return record

    def get_artifact(self, artifact_id: SemanticId) -> Artifact:
        artifact_id.require(IdKind.ARTIFACT)
        record = self._artifacts.get(artifact_id)
        if record is None:
            raise NotFound(f"artifact not found: {artifact_id}")
        return record

    def get_claim(self, claim_id: SemanticId) -> Claim:
        claim_id.require(IdKind.CLAIM)
        record = self._claims.get(claim_id)
        if record is None:
            raise NotFound(f"claim not found: {claim_id}")
        return record

    def get_verification(self, verification_id: SemanticId) -> Verification:
        verification_id.require(IdKind.VERIFICATION)
        record = self._verifications.get(verification_id)
        if record is None:
            raise NotFound(f"verification not found: {verification_id}")
        return record

    def get_fact(self, fact_id: SemanticId) -> Fact:
        fact_id.require(IdKind.FACT)
        record = self._facts.get(fact_id)
        if record is None:
            raise NotFound(f"fact not found: {fact_id}")
        return record

    @_atomic_mutation
    def record_observation(self, observation: Observation) -> Admission:
        existing = self._observations.get(observation.observation_id)
        if existing is not None:
            if existing == observation:
                return Admission.EXISTING
            raise IdentityConflict(
                f"observation identity conflict: {observation.observation_id}"
            )
        record = self.get_effect(observation.effect_id)
        self._require_admitted_dispatch(record, observation.dispatch_id)
        if record.state in {EffectState.PROPOSED, EffectState.PREPARED}:
            raise InvariantViolation("pre-dispatch effect cannot produce an observation")
        if observation.target.object_id != record.spec.target.object_id:
            raise InvariantViolation("observation target does not match effect target")
        self._observations[observation.observation_id] = observation
        return Admission.CREATED

    @_atomic_mutation
    def register_artifact(self, artifact: Artifact) -> Admission:
        existing = self._artifacts.get(artifact.artifact_id)
        if existing is not None:
            if existing == artifact:
                return Admission.EXISTING
            raise IdentityConflict(f"artifact identity conflict: {artifact.artifact_id}")
        record = self.get_effect(artifact.effect_id)
        self._require_admitted_dispatch(record, artifact.dispatch_id)
        if record.state in {EffectState.PROPOSED, EffectState.PREPARED}:
            raise InvariantViolation("pre-dispatch effect cannot produce an artifact")
        self._artifacts[artifact.artifact_id] = artifact
        return Admission.CREATED

    @_atomic_mutation
    def admit_claim(self, claim: Claim) -> Admission:
        existing = self._claims.get(claim.claim_id)
        if existing is not None:
            if existing == claim:
                return Admission.EXISTING
            raise IdentityConflict(f"claim identity conflict: {claim.claim_id}")
        origin = self.get_effect(claim.origin_effect_id)
        if claim.subject.object_id != origin.spec.target.object_id:
            raise InvariantViolation("claim subject does not match origin Effect target")
        self._claims[claim.claim_id] = claim
        return Admission.CREATED

    @_atomic_mutation
    def record_verification(self, verification: Verification) -> Admission:
        existing = self._verifications.get(verification.verification_id)
        if existing is not None:
            if existing == verification:
                return Admission.EXISTING
            raise IdentityConflict(
                f"verification identity conflict: {verification.verification_id}"
            )
        self._validate_verification(verification)
        self._verifications[verification.verification_id] = verification
        return Admission.CREATED

    @_atomic_mutation
    def commit_fact(self, fact: Fact) -> Admission:
        existing = self._facts.get(fact.fact_id)
        if existing is not None:
            if existing == fact:
                return Admission.EXISTING
            raise IdentityConflict(f"fact identity conflict: {fact.fact_id}")
        claim = self._claims.get(fact.claim_id)
        if claim is None:
            raise NotFound(f"claim not found: {fact.claim_id}")
        verification = self._verifications.get(fact.verification_id)
        if verification is None:
            raise NotFound(f"verification not found: {fact.verification_id}")
        if verification.claim_id != claim.claim_id:
            raise InvariantViolation("fact verification belongs to a different claim")
        if verification.decision is not VerificationDecision.ACCEPTED:
            raise InvariantViolation("only an accepted verification can create a fact")
        if fact.accepted_at_ms < verification.verified_at_ms:
            raise InvariantViolation("fact cannot predate its verification")
        self._facts[fact.fact_id] = fact
        return Admission.CREATED

    def validate_invariants(self) -> None:
        for effect_id, record in self._effects.items():
            events = self._events_by_effect.get(effect_id, [])
            if not events:
                raise InvariantViolation(f"effect has no events: {effect_id}")
            if events[0].kind is not EventKind.EFFECT_ADMITTED:
                raise InvariantViolation(f"effect does not begin with admission: {effect_id}")
            if len(events) != record.revision + 1:
                raise InvariantViolation(f"event/revision mismatch: {effect_id}")
            previous_time = -1
            for sequence, event in enumerate(events):
                if event.sequence != sequence:
                    raise InvariantViolation(f"non-contiguous event sequence: {effect_id}")
                if event.effect_id != effect_id:
                    raise InvariantViolation(f"event points to wrong effect: {event.event_id}")
                if event.recorded_at_ms < previous_time:
                    raise InvariantViolation(f"event time regressed: {effect_id}")
                previous_time = event.recorded_at_ms
            requires_current_dispatch = record.state in {
                EffectState.DISPATCHED,
                EffectState.RUNNING,
                EffectState.CANCEL_REQUESTED,
                EffectState.UNKNOWN,
                EffectState.RECONCILING,
                EffectState.SUCCEEDED,
            }
            if requires_current_dispatch and record.dispatch_id is None:
                raise InvariantViolation(f"post-dispatch state lacks dispatch identity: {effect_id}")
            if record.dispatch_id is not None:
                dispatch = self.get_dispatch(record.dispatch_id)
                if dispatch.effect_id != effect_id:
                    raise InvariantViolation(f"dispatch owner mismatch: {record.dispatch_id}")
                if dispatch.state is DispatchState.REJECTED:
                    raise InvariantViolation("Effect cannot remain bound to rejected Dispatch")
                if record.state in {
                    EffectState.RUNNING,
                    EffectState.CANCEL_REQUESTED,
                    EffectState.SUCCEEDED,
                    EffectState.FAILED,
                    EffectState.CANCELLED,
                } and dispatch.state is not DispatchState.ADMITTED:
                    raise InvariantViolation(
                        f"Effect state {record.state.value} requires admitted Dispatch"
                    )
                if record.state in {EffectState.UNKNOWN, EffectState.RECONCILING} and dispatch.state not in {
                    DispatchState.UNKNOWN,
                    DispatchState.ADMITTED,
                }:
                    raise InvariantViolation("uncertain Effect has incompatible Dispatch state")
        for dispatch_id, dispatch in self._dispatches.items():
            effect = self.get_effect(dispatch.effect_id)
            dispatch_events = [
                event
                for event in self._events_by_effect[dispatch.effect_id]
                if event.dispatch_id == dispatch_id
            ]
            started_events = [
                event for event in dispatch_events if event.kind is EventKind.DISPATCH_STARTED
            ]
            if len(started_events) != 1:
                raise InvariantViolation(
                    f"Dispatch must have exactly one start event: {dispatch_id}"
                )
            if dispatch.state is DispatchState.ADMITTED and not any(
                event.kind is EventKind.DISPATCH_ADMITTED for event in dispatch_events
            ):
                raise InvariantViolation(
                    f"admitted Dispatch lacks admission event: {dispatch_id}"
                )
            if dispatch.state is DispatchState.UNKNOWN and not any(
                event.kind is EventKind.OUTCOME_UNKNOWN for event in dispatch_events
            ):
                raise InvariantViolation(
                    f"unknown Dispatch lacks outcome event: {dispatch_id}"
                )
            if dispatch.state is DispatchState.REJECTED and not any(
                event.kind is EventKind.DISPATCH_REJECTED for event in dispatch_events
            ):
                raise InvariantViolation(
                    f"rejected Dispatch lacks rejection event: {dispatch_id}"
                )
            if dispatch.state is DispatchState.REJECTED:
                if effect.dispatch_id == dispatch_id:
                    raise InvariantViolation(f"rejected Dispatch remains current: {dispatch_id}")
            elif effect.dispatch_id != dispatch_id:
                raise InvariantViolation(f"active Dispatch is not bound by its Effect: {dispatch_id}")
        for observation in self._observations.values():
            record = self.get_effect(observation.effect_id)
            self._require_admitted_dispatch(record, observation.dispatch_id)
        for artifact in self._artifacts.values():
            record = self.get_effect(artifact.effect_id)
            self._require_admitted_dispatch(record, artifact.dispatch_id)
        for verification in self._verifications.values():
            self._validate_verification(verification)
        for fact in self._facts.values():
            verification = self._verifications.get(fact.verification_id)
            if verification is None or verification.decision is not VerificationDecision.ACCEPTED:
                raise InvariantViolation(f"fact lacks accepted verification: {fact.fact_id}")
            if verification.claim_id != fact.claim_id:
                raise InvariantViolation(f"fact/verification claim mismatch: {fact.fact_id}")
            if fact.accepted_at_ms < verification.verified_at_ms:
                raise InvariantViolation(f"fact predates verification: {fact.fact_id}")

    def _validate_verification(self, verification: Verification) -> None:
        claim = self._claims.get(verification.claim_id)
        if claim is None:
            raise NotFound(f"claim not found: {verification.claim_id}")
        origin = self.get_effect(claim.origin_effect_id)
        plan = origin.spec.verification
        if verification.method != plan.method:
            raise InvariantViolation("verification method does not match origin Effect plan")
        observed_kinds: set[EvidenceKind] = set()
        for reference in verification.evidence:
            observed_kinds.add(reference.kind)
            if reference.kind is EvidenceKind.OBSERVATION:
                observation = self._observations.get(reference.evidence_id)
                if observation is None:
                    raise NotFound(f"observation not found: {reference.evidence_id}")
                self._require_evidence_scope(
                    claim,
                    self.get_effect(observation.effect_id).spec.target,
                    evidence_time_ms=observation.observed_at_ms,
                    verification_time_ms=verification.verified_at_ms,
                    evidence_kind="observation",
                    require_version_match=(
                        verification.decision is VerificationDecision.ACCEPTED
                    ),
                )
            elif reference.kind is EvidenceKind.ARTIFACT:
                artifact = self._artifacts.get(reference.evidence_id)
                if artifact is None:
                    raise NotFound(f"artifact not found: {reference.evidence_id}")
                self._require_evidence_scope(
                    claim,
                    self.get_effect(artifact.effect_id).spec.target,
                    evidence_time_ms=artifact.created_at_ms,
                    verification_time_ms=verification.verified_at_ms,
                    evidence_kind="artifact",
                    require_version_match=(
                        verification.decision is VerificationDecision.ACCEPTED
                    ),
                )
        if verification.decision is VerificationDecision.ACCEPTED:
            missing = set(plan.required_evidence) - observed_kinds
            if missing:
                names = ", ".join(sorted(kind.value for kind in missing))
                raise InvariantViolation(f"accepted verification lacks required evidence: {names}")

    @staticmethod
    def _require_evidence_scope(
        claim: Claim,
        evidence_target: WorldObjectRef,
        *,
        evidence_time_ms: int,
        verification_time_ms: int,
        evidence_kind: str,
        require_version_match: bool,
    ) -> None:
        if evidence_target.object_id != claim.subject.object_id:
            raise InvariantViolation(
                f"verification {evidence_kind} has the wrong subject"
            )
        if (
            require_version_match
            and claim.subject.version is not None
            and evidence_target.version != claim.subject.version
        ):
            raise InvariantViolation(
                f"verification {evidence_kind} has the wrong version"
            )
        if evidence_time_ms > verification_time_ms:
            raise InvariantViolation(
                f"verification predates its {evidence_kind} evidence"
            )

    def _require_current_dispatch(
        self,
        effect_id: SemanticId,
        dispatch_id: SemanticId,
        *,
        expected_revision: int,
    ) -> tuple[EffectRecord, DispatchRecord]:
        record = self.get_effect(effect_id)
        if record.revision != expected_revision:
            raise RevisionConflict(
                f"expected revision {expected_revision}, found {record.revision}"
            )
        if record.dispatch_id != dispatch_id:
            raise InvariantViolation("Dispatch is not current for Effect")
        dispatch = self.get_dispatch(dispatch_id)
        if dispatch.effect_id != effect_id:
            raise InvariantViolation("Dispatch belongs to a different Effect")
        return record, dispatch

    def _append_effect_event(
        self,
        updated_record: EffectRecord,
        *,
        event_id: SemanticId,
        recorded_at_ms: int,
        kind: EventKind,
        evidence_digest: str,
        dispatch_id: SemanticId | None,
        previous_record: EffectRecord | None = None,
    ) -> EffectRecord:
        event_id.require(IdKind.EVENT)
        self._require_time(recorded_at_ms)
        self._require_new_event(event_id)
        previous = previous_record or self.get_effect(updated_record.spec.effect_id)
        if recorded_at_ms < self._events_by_effect[previous.spec.effect_id][-1].recorded_at_ms:
            raise InvariantViolation("effect event time cannot move backwards")
        updated = replace(updated_record, revision=previous.revision + 1)
        event = EffectEvent(
            event_id=event_id,
            effect_id=updated.spec.effect_id,
            sequence=updated.revision,
            kind=kind,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            dispatch_id=dispatch_id,
        )
        self._effects[updated.spec.effect_id] = updated
        self._events[event_id] = event
        self._events_by_effect[updated.spec.effect_id].append(event)
        return updated

    def _transition(
        self,
        effect_id: SemanticId,
        target: EffectState,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        evidence_digest: str | None,
        dispatch_id: SemanticId | None = None,
        event_kind: EventKind | None = None,
    ) -> EffectRecord:
        event_id.require(IdKind.EVENT)
        self._require_time(recorded_at_ms)
        self._require_new_event(event_id)
        current = self.get_effect(effect_id)
        if current.revision != expected_revision:
            raise RevisionConflict(
                f"expected revision {expected_revision}, found {current.revision}"
            )
        previous_event = self._events_by_effect[effect_id][-1]
        if recorded_at_ms < previous_event.recorded_at_ms:
            raise InvariantViolation("effect event time cannot move backwards")
        if not can_transition(current.state, target):
            raise InvalidTransition(f"{current.state.value} -> {target.value} is forbidden")
        if target in _EVIDENCE_REQUIRED and not evidence_digest:
            raise InvariantViolation(f"transition to {target.value} requires evidence")
        if target is EffectState.DISPATCHED:
            if dispatch_id is None:
                raise InvariantViolation("dispatch transition requires dispatch identity")
            dispatch_id.require(IdKind.DISPATCH)
        elif dispatch_id is not None:
            raise InvariantViolation("dispatch identity may only be bound when dispatch starts")
        bound_dispatch = dispatch_id if dispatch_id is not None else current.dispatch_id
        updated = replace(
            current,
            state=target,
            revision=current.revision + 1,
            dispatch_id=bound_dispatch,
        )
        event = EffectEvent(
            event_id=event_id,
            effect_id=effect_id,
            sequence=updated.revision,
            kind=event_kind or _STATE_EVENT[target],
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            dispatch_id=bound_dispatch,
        )
        self._effects[effect_id] = updated
        self._events[event_id] = event
        self._events_by_effect[effect_id].append(event)
        return updated

    def _require_admitted_dispatch(
        self, record: EffectRecord, dispatch_id: SemanticId
    ) -> DispatchRecord:
        if record.dispatch_id != dispatch_id:
            raise InvariantViolation("evidence dispatch does not match effect dispatch")
        dispatch = self.get_dispatch(dispatch_id)
        admitted_or_later_unknown = (
            dispatch.state is DispatchState.ADMITTED
            or (
                dispatch.state is DispatchState.UNKNOWN
                and dispatch.backend_operation_id is not None
            )
        )
        if not admitted_or_later_unknown:
            raise InvariantViolation("evidence requires a Dispatch proven admitted")
        return dispatch

    def _require_new_event(self, event_id: SemanticId) -> None:
        if event_id in self._events:
            raise IdentityConflict(f"event identity conflict: {event_id}")

    @staticmethod
    def _require_time(recorded_at_ms: int) -> None:
        if recorded_at_ms < 0:
            raise ValueError("time must be non-negative")
