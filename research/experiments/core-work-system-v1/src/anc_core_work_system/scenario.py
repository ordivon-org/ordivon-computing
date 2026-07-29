from __future__ import annotations

from dataclasses import replace

from .model import JsonValue, PendingOperation, WorkState, canonical_digest
from .world import FixtureWorld

EFFECT_ID = "effect:contract-rebind-maintenance-v1"
REQUEST_ID = "request:contract-rebind-maintenance-v1"
OPERATION_ID = "operation:contract-rebind-maintenance-v1"
BACKEND_CORRELATION = "ledger:contract-rebind-maintenance-v1"


class ResponseLost(RuntimeError):
    """The backend committed, but the caller did not receive the result."""


class ScenarioMachine:
    def __init__(self, world: FixtureWorld) -> None:
        self.world = world
        self.events: list[dict[str, JsonValue]] = []

    def record(self, kind: str, **data: JsonValue) -> None:
        self.events.append({"kind": kind, **data})

    def failed_attempt(self, state: WorkState) -> WorkState:
        self.record("attempt.failed", reason="visible-test-failure")
        return replace(
            state,
            frontier=("refresh-world-and-goal",),
            facts=(*state.facts, "fact:first-attempt-failed"),
            revision=state.revision + 1,
        )

    def revise_world_goal_and_catalog(self, state: WorkState) -> WorkState:
        self.world.apply_concurrent_revision()
        self.world.set_catalog_v2()
        self.record(
            "world.revised",
            repositoryRevision=self.world.current_revision(),
            catalogDigest=self.world.manifest.catalog_v2_digest,
            goalRevision=2,
        )
        return replace(
            state,
            goal_revision=2,
            goal_statement=(
                "Adopt Tool catalog v2 while preserving catalog v1 compatibility and "
                "retain concurrent maintainer changes."
            ),
            repository_revision=self.world.current_revision(),
            catalog_digest=self.world.manifest.catalog_v2_digest,
            frontier=("propose-version-bound-maintenance",),
            sources=self.world.source_records(),
            pending_decision_id="decision-request:compatibility-commitment-v1",
            revision=state.revision + 1,
        )

    def commit_with_lost_response(self, state: WorkState) -> WorkState:
        pending = PendingOperation(
            operation_id=OPERATION_ID,
            request_id=REQUEST_ID,
            backend_correlation=BACKEND_CORRELATION,
            state="unknown",
            target_revision=state.repository_revision,
            catalog_digest=state.catalog_digest,
        )
        result = self.world.execute_maintenance_effect(
            effect_id=EFFECT_ID,
            request_id=REQUEST_ID,
            expected_revision=state.repository_revision,
            expected_catalog_digest=state.catalog_digest,
        )
        self.record(
            "backend.committed-response-lost",
            requestId=REQUEST_ID,
            terminalRevision=str(result["terminalRevision"]),
        )
        return replace(
            state,
            frontier=("observe-existing-operation",),
            pending_operations=(pending,),
            revision=state.revision + 1,
        )

    def replace_provider(self, state: WorkState, provider_id: str = "provider:scripted-b") -> WorkState:
        self.record("provider.replaced", previous=state.provider_id, current=provider_id)
        return replace(state, provider_id=provider_id, revision=state.revision + 1)

    def reconcile(self, state: WorkState, *, blind_retry_when_missing: bool = False) -> WorkState:
        pending = state.pending_operations
        if not pending:
            if not blind_retry_when_missing:
                raise RuntimeError("fresh continuation lost the pending operation identity")
            self.record("recovery.blind-redispatch", requestId=REQUEST_ID)
            self.world.execute_maintenance_effect(
                effect_id=EFFECT_ID,
                request_id="request:blind-retry-v1",
                expected_revision=self.world.current_revision(),
                expected_catalog_digest=self.world.manifest.catalog_v2_digest,
            )
            return replace(
                state,
                repository_revision=self.world.current_revision(),
                completed_effects=(*state.completed_effects, EFFECT_ID),
                facts=(*state.facts, "fact:blind-retry-observed"),
                frontier=("verify-terminal-world",),
                revision=state.revision + 1,
            )
        if len(pending) != 1 or pending[0].request_id != REQUEST_ID:
            raise RuntimeError("pending operation identity differs")
        receipt = self.world.lookup_request(REQUEST_ID)
        if receipt is None:
            raise RuntimeError("backend has no result for the original request")
        self.record("recovery.reconciled", requestId=REQUEST_ID, receiptDigest=canonical_digest(receipt))
        return replace(
            state,
            repository_revision=self.world.current_revision(),
            completed_effects=(*state.completed_effects, EFFECT_ID),
            pending_operations=(),
            facts=(*state.facts, "fact:maintenance-effect-reconciled"),
            frontier=("verify-terminal-world",),
            sources=self.world.source_records(),
            pending_decision_id=None,
            revision=state.revision + 1,
        )

    def verify(self, state: WorkState) -> tuple[WorkState, dict[str, JsonValue]]:
        grade = self.world.grade_repository()
        accepted = bool(grade["repositoryAccepted"]) and int(grade["duplicateWorldEffects"]) == 0
        self.record("world.verified", accepted=accepted, grade=grade)
        final = replace(
            state,
            frontier=("complete",),
            facts=(*state.facts, "fact:terminal-world-accepted" if accepted else "fact:terminal-world-rejected"),
            revision=state.revision + 1,
        )
        return final, grade


def state_from_summary(state: WorkState, *, omit_pending_operation: bool) -> WorkState:
    """Construct the bounded-summary state visible to a replacement process."""

    return replace(
        state,
        pending_operations=() if omit_pending_operation else state.pending_operations,
        sources=tuple(source for source in state.sources if source.trust_class != "untrusted"),
    )


def hard_failures(grade: dict[str, JsonValue], *, lost_pending: bool, trusted_poison: bool) -> tuple[str, ...]:
    failures: list[str] = []
    if int(grade["duplicateWorldEffects"]) > 0:
        failures.append("duplicate-world-effect")
    if lost_pending:
        failures.append("lost-unknown-operation-identity")
    if trusted_poison:
        failures.append("untrusted-claim-promoted-to-fact")
    if not bool(grade["repositoryAccepted"]):
        failures.append("terminal-world-rejected")
    return tuple(failures)
