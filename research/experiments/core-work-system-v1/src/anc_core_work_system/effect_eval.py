from __future__ import annotations

from pathlib import Path
from time import perf_counter

from .model import (
    DecisionDisposition,
    ExperimentSpec,
    Fault,
    TrialRecord,
    TrialStatus,
    canonical_digest,
)
from .scenario import EFFECT_ID, REQUEST_ID
from .world import prepare_trial_world

EFFECT_VARIANTS = ("plain-tool", "idempotency-audit", "durable-activity", "ordivon-effect")


def run_effect_variant(
    fixture: str | Path,
    variant: str,
    *,
    working_root: str | Path,
) -> TrialRecord:
    if variant not in EFFECT_VARIANTS:
        raise ValueError(f"unsupported Effect variant: {variant}")
    start = perf_counter()
    world = prepare_trial_world(fixture, Path(working_root) / variant / "world")
    initial = world.initial_state()
    world.apply_concurrent_revision()
    world.set_catalog_v2()
    target_revision = world.current_revision()
    response_state = "unknown"
    redispatches = 0
    reconciliation_reads = 0
    state_objects = 1
    recovery_note = ""

    world.execute_maintenance_effect(
        effect_id=EFFECT_ID,
        request_id=REQUEST_ID,
        expected_revision=target_revision,
        expected_catalog_digest=world.manifest.catalog_v2_digest,
    )

    if variant == "plain-tool":
        redispatches += 1
        world.execute_maintenance_effect(
            effect_id=EFFECT_ID,
            request_id="request:plain-tool-retry-v1",
            expected_revision=world.current_revision(),
            expected_catalog_digest=world.manifest.catalog_v2_digest,
        )
        response_state = "assumed-failed-then-retried"
        recovery_note = "caller created a new Tool call identity after timeout"
    elif variant == "idempotency-audit":
        reconciliation_reads += 1
        receipt = world.lookup_request(REQUEST_ID)
        if receipt is None:
            raise RuntimeError("audit row disappeared")
        response_state = "recovered-from-audit"
        state_objects = 2
        recovery_note = "stable request identity resolved the committed audit row"
    elif variant == "durable-activity":
        reconciliation_reads += 1
        persisted_activity_result = world.lookup_request(REQUEST_ID)
        if persisted_activity_result is None:
            raise RuntimeError("Activity result disappeared")
        response_state = "activity-result-replayed"
        state_objects = 3
        recovery_note = "Workflow history retained the Activity identity and result"
    else:
        reconciliation_reads += 1
        receipt = world.lookup_request(REQUEST_ID)
        if receipt is None:
            raise RuntimeError("reconciliation found no original backend result")
        response_state = "unknown-reconciled-to-succeeded"
        state_objects = 6
        recovery_note = "fresh Host observed the original Dispatch and forbade blind redispatch"

    grade = world.grade_repository()
    hard_failures: list[str] = []
    if int(grade["duplicateWorldEffects"]) > 0:
        hard_failures.append("duplicate-world-effect")
    if response_state.startswith("assumed-"):
        hard_failures.append("unknown-classified-without-evidence")
    if redispatches > 0:
        hard_failures.append("unsafe-redispatch")
    if not bool(grade["repositoryAccepted"]):
        hard_failures.append("terminal-world-rejected")
    status = TrialStatus.PASSED if not hard_failures else TrialStatus.FAILED
    disposition = DecisionDisposition.INCOMPLETE
    if variant in {"idempotency-audit", "durable-activity"} and status is TrialStatus.PASSED:
        disposition = DecisionDisposition.SHRINK
    if variant == "ordivon-effect" and status is TrialStatus.PASSED:
        disposition = DecisionDisposition.DEFER
    final_digest = canonical_digest(
        {
            "grade": grade,
            "responseState": response_state,
            "redispatches": redispatches,
        }
    )
    return TrialRecord(
        spec=ExperimentSpec(
            experiment_id=f"experiment:round1-effect-{variant}",
            work_package="effect",
            variant=variant,
            fixture_digest=world.manifest.fixture_digest,
            faults=(
                Fault.RESPONSE_LOSS_AFTER_COMMIT,
                Fault.HOST_RESTART,
                Fault.REPOSITORY_DRIFT,
                Fault.TOOL_CONTRACT_DRIFT,
            ),
        ),
        status=status,
        world_manifest_digest=canonical_digest(world.manifest.to_dict()),
        initial_state_digest=initial.digest,
        final_state_digest=final_digest,
        accepted_outcome=status is TrialStatus.PASSED,
        hard_failures=tuple(sorted(set(hard_failures))),
        observations={
            "worldGrade": grade,
            "responseState": response_state,
            "redispatches": redispatches,
            "reconciliationReads": reconciliation_reads,
            "falseSuccess": False,
            "falseFailure": response_state.startswith("assumed-"),
            "recoveryNote": recovery_note,
            "singleBackendEvidenceOnly": True,
        },
        costs={
            "elapsedMs": int((perf_counter() - start) * 1000),
            "stateObjects": state_objects,
            "backendCalls": 1 + redispatches,
            "reconciliationReads": reconciliation_reads,
        },
        disposition=disposition,
    )


def run_effect_matrix(fixture: str | Path, *, working_root: str | Path) -> list[TrialRecord]:
    return [
        run_effect_variant(fixture, variant, working_root=working_root)
        for variant in EFFECT_VARIANTS
    ]
