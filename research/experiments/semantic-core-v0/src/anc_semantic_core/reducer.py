from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace
from functools import wraps
from typing import Any, Callable, Iterator, TypeVar

from .authority import (
    Attestation,
    AttestationKind,
    AuthorityPolicy,
    AuthorityRole,
    semantic_digest,
)
from .errors import (
    IdentityConflict,
    InvalidTransition,
    InvariantViolation,
    NotFound,
    RevisionConflict,
)
from .identity import IdKind, SemanticId
from .model import (
    Admission,
    Artifact,
    Claim,
    DispatchRecord,
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
from .state import (
    DispatchState,
    EffectState,
    can_transition_dispatch,
    can_transition_effect,
)


_Result = TypeVar("_Result")


def _atomic_mutation(
    method: Callable[..., _Result],
) -> Callable[..., _Result]:
    """Make one semantic command atomic with a command-local undo savepoint."""

    @wraps(method)
    def wrapped(self: "ReferenceReducer", *args: Any, **kwargs: Any) -> _Result:
        savepoint = len(self._undo_log)
        serial = self._mutation_serial
        try:
            result = method(self, *args, **kwargs)
            if len(self._undo_log) != savepoint:
                self._mutation_serial += 1
            return result
        except BaseException:
            self._rollback_to(savepoint)
            self._mutation_serial = serial
            raise
        finally:
            if self._transaction_depth == 0:
                self._undo_log.clear()

    return wrapped


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


class ReferenceReducer:
    """In-memory executable reference model for Agent-native semantics."""

    def __init__(self, authority_policy: AuthorityPolicy) -> None:
        self._authority_policy = authority_policy
        self._effects: dict[SemanticId, EffectRecord] = {}
        self._dispatches: dict[SemanticId, DispatchRecord] = {}
        self._events: dict[SemanticId, EffectEvent] = {}
        self._events_by_effect: dict[SemanticId, list[EffectEvent]] = {}
        self._observations: dict[SemanticId, Observation] = {}
        self._artifacts: dict[SemanticId, Artifact] = {}
        self._claims: dict[SemanticId, Claim] = {}
        self._verifications: dict[SemanticId, Verification] = {}
        self._facts: dict[SemanticId, Fact] = {}
        self._undo_log: list[Callable[[], None]] = []
        self._transaction_depth = 0
        self._mutation_serial = 0

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

    def clone(self) -> "ReferenceReducer":
        cloned = ReferenceReducer(self._authority_policy)
        cloned._restore(self._snapshot())
        cloned._mutation_serial = self._mutation_serial
        return cloned

    @property
    def mutation_serial(self) -> int:
        return self._mutation_serial

    def _set_item(self, mapping: dict[Any, Any], key: Any, value: Any) -> None:
        existed = key in mapping
        previous = mapping.get(key)
        if existed and previous == value:
            return

        def undo() -> None:
            if existed:
                mapping[key] = previous
            else:
                mapping.pop(key, None)

        self._undo_log.append(undo)
        mapping[key] = value

    def _append_item(self, items: list[Any], value: Any) -> None:
        previous_length = len(items)

        def undo() -> None:
            del items[previous_length:]

        self._undo_log.append(undo)
        items.append(value)

    def _rollback_to(self, savepoint: int) -> None:
        while len(self._undo_log) > savepoint:
            self._undo_log.pop()()

    @property
    def authority_policy_fingerprint(self) -> str:
        return self._authority_policy.fingerprint

    def state_snapshot(self) -> tuple[dict[Any, Any], ...]:
        """Return a detached equality-comparable state snapshot for tests and stores."""
        return self._snapshot()

    def export_state(self) -> dict[str, tuple[Any, ...]]:
        """Return a deterministic canonical state payload for checkpoints."""

        def ordered(values: Any, identity: Callable[[Any], SemanticId]) -> tuple[Any, ...]:
            return tuple(sorted(values, key=lambda item: str(identity(item))))

        return {
            "effects": ordered(self._effects.values(), lambda item: item.spec.effect_id),
            "dispatches": ordered(self._dispatches.values(), lambda item: item.dispatch_id),
            "events": ordered(self._events.values(), lambda item: item.event_id),
            "observations": ordered(
                self._observations.values(), lambda item: item.observation_id
            ),
            "artifacts": ordered(self._artifacts.values(), lambda item: item.artifact_id),
            "claims": ordered(self._claims.values(), lambda item: item.claim_id),
            "verifications": ordered(
                self._verifications.values(), lambda item: item.verification_id
            ),
            "facts": ordered(self._facts.values(), lambda item: item.fact_id),
        }

    @classmethod
    def from_exported_state(
        cls, authority_policy: AuthorityPolicy, state: dict[str, tuple[Any, ...]]
    ) -> "ReferenceReducer":
        expected = {
            "effects",
            "dispatches",
            "events",
            "observations",
            "artifacts",
            "claims",
            "verifications",
            "facts",
        }
        if set(state) != expected or not all(
            isinstance(value, tuple) for value in state.values()
        ):
            raise InvariantViolation("checkpoint state shape is invalid")
        reducer = cls(authority_policy)
        reducer._effects = {item.spec.effect_id: item for item in state["effects"]}
        reducer._dispatches = {
            item.dispatch_id: item for item in state["dispatches"]
        }
        reducer._events = {item.event_id: item for item in state["events"]}
        reducer._events_by_effect = {effect_id: [] for effect_id in reducer._effects}
        for event in sorted(
            state["events"], key=lambda item: (str(item.effect_id), item.sequence)
        ):
            try:
                reducer._events_by_effect[event.effect_id].append(event)
            except KeyError as error:
                raise InvariantViolation(
                    f"checkpoint event references missing Effect: {event.event_id}"
                ) from error
        reducer._observations = {
            item.observation_id: item for item in state["observations"]
        }
        reducer._artifacts = {item.artifact_id: item for item in state["artifacts"]}
        reducer._claims = {item.claim_id: item for item in state["claims"]}
        reducer._verifications = {
            item.verification_id: item for item in state["verifications"]
        }
        reducer._facts = {item.fact_id: item for item in state["facts"]}
        reducer.validate_invariants()
        return reducer

    @property
    def journal_entry_count(self) -> int:
        return 0

    @property
    def checkpoint_sequence(self) -> int:
        return 0

    @property
    def checkpoint_count(self) -> int:
        return 0

    def checkpoint(self) -> int:
        self.validate_invariants()
        return 0

    def verify_from_genesis(self) -> None:
        self.validate_invariants()

    def close(self) -> None:
        return None

    @contextmanager
    def transaction(self) -> Iterator["ReferenceReducer"]:
        savepoint = len(self._undo_log)
        serial = self._mutation_serial
        self._transaction_depth += 1
        try:
            yield self
        except BaseException:
            self._rollback_to(savepoint)
            self._mutation_serial = serial
            raise
        finally:
            self._transaction_depth -= 1
            if self._transaction_depth == 0:
                self._undo_log.clear()

    @_atomic_mutation
    def admit_effect(
        self,
        spec: EffectSpec,
        *,
        event_id: SemanticId,
        recorded_at_ms: int,
        attestation: Attestation,
    ) -> Admission:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.EFFECT,
            kind=AttestationKind.EFFECT_PROPOSAL,
            operation="admit_effect",
            issued_at_ms=recorded_at_ms,
            args=(spec,),
            kwargs={"event_id": event_id, "recorded_at_ms": recorded_at_ms},
        )
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
            attestation=attestation,
        )
        self._set_item(self._effects, spec.effect_id, record)
        self._set_item(self._events, event_id, event)
        self._set_item(self._events_by_effect, spec.effect_id, [event])
        return Admission.CREATED

    @_atomic_mutation
    def prepare_effect(
        self,
        effect_id: SemanticId,
        *,
        expected_revision: int,
        event_id: SemanticId,
        recorded_at_ms: int,
        attestation: Attestation,
    ) -> EffectRecord:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.EFFECT,
            kind=AttestationKind.EFFECT_PREPARATION,
            operation="prepare_effect",
            issued_at_ms=recorded_at_ms,
            args=(effect_id,),
            kwargs={
                "expected_revision": expected_revision,
                "event_id": event_id,
                "recorded_at_ms": recorded_at_ms,
            },
        )
        return self._transition(
            effect_id,
            EffectState.PREPARED,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=None,
            attestation=attestation,
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
        attestation: Attestation,
    ) -> EffectRecord:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.DISPATCH,
            kind=AttestationKind.DISPATCH_INTENT,
            operation="begin_dispatch",
            issued_at_ms=recorded_at_ms,
            args=(effect_id,),
            kwargs={
                "expected_revision": expected_revision,
                "dispatch_id": dispatch_id,
                "event_id": event_id,
                "recorded_at_ms": recorded_at_ms,
                "request_digest": request_digest,
            },
        )
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
            attestation=attestation,
        )
        self._set_item(self._dispatches, dispatch_id, dispatch)
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
        attestation: Attestation,
    ) -> EffectRecord:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.DISPATCH,
            kind=AttestationKind.BACKEND_ADMISSION,
            operation="admit_dispatch",
            issued_at_ms=recorded_at_ms,
            args=(effect_id, dispatch_id),
            kwargs={
                "expected_revision": expected_revision,
                "event_id": event_id,
                "recorded_at_ms": recorded_at_ms,
                "backend_operation_id": backend_operation_id,
                "evidence_digest": evidence_digest,
            },
        )
        if not backend_operation_id or not evidence_digest:
            raise ValueError("dispatch admission requires backend identity and evidence")
        record, dispatch = self._require_current_dispatch(
            effect_id, dispatch_id, expected_revision=expected_revision
        )
        if dispatch.state is DispatchState.ADMITTED:
            if dispatch.backend_operation_id == backend_operation_id:
                return record
            raise IdentityConflict("Dispatch is already bound to a different backend operation")
        self._require_dispatch_transition(dispatch.state, DispatchState.ADMITTED)
        self._set_item(self._dispatches, dispatch_id, replace(
            dispatch,
            state=DispatchState.ADMITTED,
            updated_at_ms=recorded_at_ms,
            backend_operation_id=backend_operation_id,
            reason_code=None,
            retryable=None,
        ))
        return self._append_effect_event(
            record,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            kind=EventKind.DISPATCH_ADMITTED,
            evidence_digest=evidence_digest,
            dispatch_id=dispatch_id,
            attestation=attestation,
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
        attestation: Attestation,
    ) -> EffectRecord:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.DISPATCH,
            kind=AttestationKind.OUTCOME_UNCERTAINTY,
            operation="mark_dispatch_unknown",
            issued_at_ms=recorded_at_ms,
            args=(effect_id, dispatch_id),
            kwargs={
                "expected_revision": expected_revision,
                "event_id": event_id,
                "recorded_at_ms": recorded_at_ms,
                "evidence_digest": evidence_digest,
            },
        )
        if not evidence_digest:
            raise ValueError("unknown Dispatch requires evidence")
        record, dispatch = self._require_current_dispatch(
            effect_id, dispatch_id, expected_revision=expected_revision
        )
        if dispatch.state is not DispatchState.UNKNOWN:
            self._require_dispatch_transition(dispatch.state, DispatchState.UNKNOWN)
        self._set_item(self._dispatches, dispatch_id, replace(
            dispatch,
            state=DispatchState.UNKNOWN,
            updated_at_ms=recorded_at_ms,
            reason_code=None,
            retryable=None,
        ))
        if record.state is EffectState.UNKNOWN:
            return record
        return self._transition(
            effect_id,
            EffectState.UNKNOWN,
            expected_revision=expected_revision,
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            evidence_digest=evidence_digest,
            attestation=attestation,
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
        attestation: Attestation,
    ) -> EffectRecord:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.DISPATCH,
            kind=AttestationKind.DISPATCH_REJECTION,
            operation="reject_dispatch",
            issued_at_ms=recorded_at_ms,
            args=(effect_id, dispatch_id),
            kwargs={
                "expected_revision": expected_revision,
                "event_id": event_id,
                "recorded_at_ms": recorded_at_ms,
                "reason_code": reason_code,
                "retryable": retryable,
                "evidence_digest": evidence_digest,
            },
        )
        if not reason_code or not evidence_digest:
            raise ValueError("Dispatch rejection requires reason and evidence")
        record, dispatch = self._require_current_dispatch(
            effect_id, dispatch_id, expected_revision=expected_revision
        )
        if dispatch.backend_operation_id is not None:
            raise InvalidTransition(
                "Dispatch proven admitted cannot be reclassified as rejected"
            )
        if dispatch.state is DispatchState.REJECTED:
            if dispatch.reason_code == reason_code and dispatch.retryable is retryable:
                return record
            raise IdentityConflict("Dispatch rejection conflicts with existing outcome")
        self._require_dispatch_transition(dispatch.state, DispatchState.REJECTED)
        self._set_item(self._dispatches, dispatch_id, replace(
            dispatch,
            state=DispatchState.REJECTED,
            updated_at_ms=recorded_at_ms,
            backend_operation_id=None,
            reason_code=reason_code,
            retryable=retryable,
        ))
        target = EffectState.PREPARED if retryable else EffectState.FAILED
        return self._append_effect_event(
            replace(record, state=target, dispatch_id=None),
            event_id=event_id,
            recorded_at_ms=recorded_at_ms,
            kind=EventKind.DISPATCH_REJECTED,
            evidence_digest=evidence_digest,
            dispatch_id=dispatch_id,
            previous_record=record,
            attestation=attestation,
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
        attestation: Attestation,
    ) -> EffectRecord:
        self._verify_command_attestation(
            attestation,
            role=AuthorityRole.DISPATCH,
            kind=AttestationKind.EFFECT_TRANSITION,
            operation="advance_effect",
            issued_at_ms=recorded_at_ms,
            args=(effect_id, target),
            kwargs={
                "expected_revision": expected_revision,
                "event_id": event_id,
                "recorded_at_ms": recorded_at_ms,
                "evidence_digest": evidence_digest,
            },
        )
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
            attestation=attestation,
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

    def observations_for(self, effect_id: SemanticId) -> tuple[Observation, ...]:
        self.get_effect(effect_id)
        return tuple(
            sorted(
                (
                    observation
                    for observation in self._observations.values()
                    if observation.effect_id == effect_id
                ),
                key=lambda item: (item.observed_at_ms, str(item.observation_id)),
            )
        )

    def artifacts_for(self, effect_id: SemanticId) -> tuple[Artifact, ...]:
        self.get_effect(effect_id)
        return tuple(
            sorted(
                (
                    artifact
                    for artifact in self._artifacts.values()
                    if artifact.effect_id == effect_id
                ),
                key=lambda item: (item.created_at_ms, str(item.artifact_id)),
            )
        )

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
        self._verify_record_attestation(
            observation.attestation,
            role=AuthorityRole.OBSERVATION,
            kind=AttestationKind.OBSERVATION,
            operation="record_observation",
            record=replace(observation, attestation=None),
            issued_at_ms=observation.observed_at_ms,
        )
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
        self._set_item(self._observations, observation.observation_id, observation)
        return Admission.CREATED

    @_atomic_mutation
    def register_artifact(self, artifact: Artifact) -> Admission:
        self._verify_record_attestation(
            artifact.attestation,
            role=AuthorityRole.OBSERVATION,
            kind=AttestationKind.ARTIFACT,
            operation="register_artifact",
            record=replace(artifact, attestation=None),
            issued_at_ms=artifact.created_at_ms,
        )
        existing = self._artifacts.get(artifact.artifact_id)
        if existing is not None:
            if existing == artifact:
                return Admission.EXISTING
            raise IdentityConflict(f"artifact identity conflict: {artifact.artifact_id}")
        record = self.get_effect(artifact.effect_id)
        self._require_admitted_dispatch(record, artifact.dispatch_id)
        if record.state in {EffectState.PROPOSED, EffectState.PREPARED}:
            raise InvariantViolation("pre-dispatch effect cannot produce an artifact")
        self._set_item(self._artifacts, artifact.artifact_id, artifact)
        return Admission.CREATED

    @_atomic_mutation
    def admit_claim(self, claim: Claim, *, proposed_at_ms: int = 0) -> Admission:
        self._verify_record_attestation(
            claim.attestation,
            role=AuthorityRole.VERIFICATION,
            kind=AttestationKind.CLAIM,
            operation="admit_claim",
            record=replace(claim, attestation=None),
            issued_at_ms=proposed_at_ms,
            proposed_at_ms=proposed_at_ms,
        )
        existing = self._claims.get(claim.claim_id)
        if existing is not None:
            if existing == claim:
                return Admission.EXISTING
            raise IdentityConflict(f"claim identity conflict: {claim.claim_id}")
        origin = self.get_effect(claim.origin_effect_id)
        if claim.subject.object_id != origin.spec.target.object_id:
            raise InvariantViolation("claim subject does not match origin Effect target")
        self._set_item(self._claims, claim.claim_id, claim)
        return Admission.CREATED

    @_atomic_mutation
    def record_verification(self, verification: Verification) -> Admission:
        self._verify_record_attestation(
            verification.attestation,
            role=AuthorityRole.VERIFICATION,
            kind=AttestationKind.VERIFICATION,
            operation="record_verification",
            record=replace(verification, attestation=None),
            issued_at_ms=verification.verified_at_ms,
        )
        existing = self._verifications.get(verification.verification_id)
        if existing is not None:
            if existing == verification:
                return Admission.EXISTING
            raise IdentityConflict(
                f"verification identity conflict: {verification.verification_id}"
            )
        self._validate_verification(verification)
        self._set_item(self._verifications, verification.verification_id, verification)
        return Admission.CREATED

    @_atomic_mutation
    def commit_fact(self, fact: Fact) -> Admission:
        self._verify_record_attestation(
            fact.attestation,
            role=AuthorityRole.FACT,
            kind=AttestationKind.FACT_ACCEPTANCE,
            operation="commit_fact",
            record=replace(fact, attestation=None),
            issued_at_ms=fact.accepted_at_ms,
        )
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
        self._set_item(self._facts, fact.fact_id, fact)
        return Admission.CREATED

    def validate_invariants(self) -> None:
        self._validate_effect_histories()
        self._validate_dispatch_bindings()
        self._validate_evidence_provenance()
        self._validate_knowledge_admission()
        self._validate_attestations()

    def _validate_effect_histories(self) -> None:
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

    def _validate_dispatch_bindings(self) -> None:
        for effect_id, record in self._effects.items():
            requires_current_dispatch = record.state in {
                EffectState.DISPATCHED,
                EffectState.RUNNING,
                EffectState.CANCEL_REQUESTED,
                EffectState.UNKNOWN,
                EffectState.RECONCILING,
                EffectState.SUCCEEDED,
            }
            if requires_current_dispatch and record.dispatch_id is None:
                raise InvariantViolation(
                    f"post-dispatch state lacks dispatch identity: {effect_id}"
                )
            if record.dispatch_id is None:
                continue
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
            if record.state in {
                EffectState.UNKNOWN,
                EffectState.RECONCILING,
            } and dispatch.state not in {
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

    def _validate_evidence_provenance(self) -> None:
        for observation in self._observations.values():
            record = self.get_effect(observation.effect_id)
            self._require_admitted_dispatch(record, observation.dispatch_id)
        for artifact in self._artifacts.values():
            record = self.get_effect(artifact.effect_id)
            self._require_admitted_dispatch(record, artifact.dispatch_id)

    def _validate_knowledge_admission(self) -> None:
        for claim in self._claims.values():
            self.get_effect(claim.origin_effect_id)
        for verification in self._verifications.values():
            self._validate_verification(verification)
        for fact in self._facts.values():
            verification = self._verifications.get(fact.verification_id)
            if (
                verification is None
                or verification.decision is not VerificationDecision.ACCEPTED
            ):
                raise InvariantViolation(f"fact lacks accepted verification: {fact.fact_id}")
            if verification.claim_id != fact.claim_id:
                raise InvariantViolation(
                    f"fact/verification claim mismatch: {fact.fact_id}"
                )
            if fact.accepted_at_ms < verification.verified_at_ms:
                raise InvariantViolation(f"fact predates verification: {fact.fact_id}")

    def _validate_attestations(self) -> None:
        for effect_id, record in self._effects.items():
            for event in self._events_by_effect.get(effect_id, []):
                self._validate_event_attestation(record, event)
        for observation in self._observations.values():
            self._verify_record_attestation(
                observation.attestation,
                role=AuthorityRole.OBSERVATION,
                kind=AttestationKind.OBSERVATION,
                operation="record_observation",
                record=replace(observation, attestation=None),
                issued_at_ms=observation.observed_at_ms,
            )
        for artifact in self._artifacts.values():
            self._verify_record_attestation(
                artifact.attestation,
                role=AuthorityRole.OBSERVATION,
                kind=AttestationKind.ARTIFACT,
                operation="register_artifact",
                record=replace(artifact, attestation=None),
                issued_at_ms=artifact.created_at_ms,
            )
        for claim in self._claims.values():
            if claim.attestation is None:
                raise InvariantViolation("Claim lacks authority attestation")
            self._verify_record_attestation(
                claim.attestation,
                role=AuthorityRole.VERIFICATION,
                kind=AttestationKind.CLAIM,
                operation="admit_claim",
                record=replace(claim, attestation=None),
                issued_at_ms=claim.attestation.issued_at_ms,
                proposed_at_ms=claim.attestation.issued_at_ms,
            )
        for verification in self._verifications.values():
            self._verify_record_attestation(
                verification.attestation,
                role=AuthorityRole.VERIFICATION,
                kind=AttestationKind.VERIFICATION,
                operation="record_verification",
                record=replace(verification, attestation=None),
                issued_at_ms=verification.verified_at_ms,
            )
        for fact in self._facts.values():
            self._verify_record_attestation(
                fact.attestation,
                role=AuthorityRole.FACT,
                kind=AttestationKind.FACT_ACCEPTANCE,
                operation="commit_fact",
                record=replace(fact, attestation=None),
                issued_at_ms=fact.accepted_at_ms,
            )

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

    @staticmethod
    def _require_dispatch_transition(
        current: DispatchState, target: DispatchState
    ) -> None:
        if current is target:
            return
        if not can_transition_dispatch(current, target):
            raise InvalidTransition(
                f"cannot transition Dispatch from {current.value} to {target.value}"
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
        attestation: Attestation,
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
            attestation=attestation,
            evidence_digest=evidence_digest,
            dispatch_id=dispatch_id,
        )
        self._set_item(self._effects, updated.spec.effect_id, updated)
        self._set_item(self._events, event_id, event)
        self._append_item(self._events_by_effect[updated.spec.effect_id], event)
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
        attestation: Attestation,
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
        if not can_transition_effect(current.state, target):
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
            attestation=attestation,
            evidence_digest=evidence_digest,
            dispatch_id=bound_dispatch,
        )
        self._set_item(self._effects, effect_id, updated)
        self._set_item(self._events, event_id, event)
        self._append_item(self._events_by_effect[effect_id], event)
        return updated

    def _validate_event_attestation(
        self, record: EffectRecord, event: EffectEvent
    ) -> None:
        previous_revision = event.sequence - 1
        common = {
            "event_id": event.event_id,
            "recorded_at_ms": event.recorded_at_ms,
        }
        if event.kind is EventKind.EFFECT_ADMITTED:
            operation = "admit_effect"
            role = AuthorityRole.EFFECT
            kind = AttestationKind.EFFECT_PROPOSAL
            args = (record.spec,)
            kwargs = common
        elif event.kind is EventKind.EFFECT_PREPARED:
            operation = "prepare_effect"
            role = AuthorityRole.EFFECT
            kind = AttestationKind.EFFECT_PREPARATION
            args = (event.effect_id,)
            kwargs = {"expected_revision": previous_revision, **common}
        elif event.kind is EventKind.DISPATCH_STARTED:
            if event.dispatch_id is None:
                raise InvariantViolation("Dispatch start event lacks Dispatch identity")
            dispatch = self.get_dispatch(event.dispatch_id)
            operation = "begin_dispatch"
            role = AuthorityRole.DISPATCH
            kind = AttestationKind.DISPATCH_INTENT
            args = (event.effect_id,)
            kwargs = {
                "expected_revision": previous_revision,
                "dispatch_id": event.dispatch_id,
                **common,
                "request_digest": dispatch.request_digest,
            }
        elif event.kind is EventKind.DISPATCH_ADMITTED:
            if event.dispatch_id is None:
                raise InvariantViolation("Dispatch admission event lacks Dispatch identity")
            dispatch = self.get_dispatch(event.dispatch_id)
            operation = "admit_dispatch"
            role = AuthorityRole.DISPATCH
            kind = AttestationKind.BACKEND_ADMISSION
            args = (event.effect_id, event.dispatch_id)
            kwargs = {
                "expected_revision": previous_revision,
                **common,
                "backend_operation_id": dispatch.backend_operation_id,
                "evidence_digest": event.evidence_digest,
            }
        elif event.kind is EventKind.DISPATCH_REJECTED:
            if event.dispatch_id is None:
                raise InvariantViolation("Dispatch rejection event lacks Dispatch identity")
            dispatch = self.get_dispatch(event.dispatch_id)
            operation = "reject_dispatch"
            role = AuthorityRole.DISPATCH
            kind = AttestationKind.DISPATCH_REJECTION
            args = (event.effect_id, event.dispatch_id)
            kwargs = {
                "expected_revision": previous_revision,
                **common,
                "reason_code": dispatch.reason_code,
                "retryable": dispatch.retryable,
                "evidence_digest": event.evidence_digest,
            }
        elif event.kind is EventKind.OUTCOME_UNKNOWN:
            if event.dispatch_id is None:
                raise InvariantViolation("Unknown outcome event lacks Dispatch identity")
            operation = "mark_dispatch_unknown"
            role = AuthorityRole.DISPATCH
            kind = AttestationKind.OUTCOME_UNCERTAINTY
            args = (event.effect_id, event.dispatch_id)
            kwargs = {
                "expected_revision": previous_revision,
                **common,
                "evidence_digest": event.evidence_digest,
            }
        else:
            targets = {
                EventKind.RUNNING_OBSERVED: EffectState.RUNNING,
                EventKind.CANCELLATION_REQUESTED: EffectState.CANCEL_REQUESTED,
                EventKind.RECONCILIATION_STARTED: EffectState.RECONCILING,
                EventKind.EFFECT_SUCCEEDED: EffectState.SUCCEEDED,
                EventKind.EFFECT_FAILED: EffectState.FAILED,
                EventKind.EFFECT_CANCELLED: EffectState.CANCELLED,
            }
            target = targets.get(event.kind)
            if target is None:
                raise InvariantViolation(f"unsupported attested event kind: {event.kind}")
            operation = "advance_effect"
            role = AuthorityRole.DISPATCH
            kind = AttestationKind.EFFECT_TRANSITION
            args = (event.effect_id, target)
            kwargs = {
                "expected_revision": previous_revision,
                **common,
                "evidence_digest": event.evidence_digest,
            }
        self._verify_command_attestation(
            event.attestation,
            role=role,
            kind=kind,
            operation=operation,
            issued_at_ms=event.recorded_at_ms,
            args=args,
            kwargs=kwargs,
        )

    def _verify_command_attestation(
        self,
        attestation: Attestation,
        *,
        role: AuthorityRole,
        kind: AttestationKind,
        operation: str,
        issued_at_ms: int,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        self._authority_policy.verify_attestation(
            attestation,
            expected_role=role,
            expected_kind=kind,
            expected_subject_digest=semantic_digest(operation, *args, **kwargs),
            expected_issued_at_ms=issued_at_ms,
        )

    def _verify_record_attestation(
        self,
        attestation: Attestation | None,
        *,
        role: AuthorityRole,
        kind: AttestationKind,
        operation: str,
        record: Any,
        issued_at_ms: int,
        **kwargs: Any,
    ) -> None:
        if attestation is None:
            raise InvariantViolation(f"{operation} requires an authority attestation")
        self._authority_policy.verify_attestation(
            attestation,
            expected_role=role,
            expected_kind=kind,
            expected_subject_digest=semantic_digest(operation, record, **kwargs),
            expected_issued_at_ms=issued_at_ms,
        )

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
