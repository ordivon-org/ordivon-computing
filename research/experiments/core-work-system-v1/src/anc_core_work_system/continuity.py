from __future__ import annotations

import asyncio
from pathlib import Path
from time import perf_counter

from .model import (
    DecisionDisposition,
    ExperimentSpec,
    Fault,
    JsonValue,
    TrialRecord,
    TrialStatus,
    canonical_digest,
)
from .persistence import JsonStateStore, LangGraphStateStore, TranscriptSummaryStore, dependency_identity
from .scenario import ScenarioMachine, hard_failures
from .temporal_store import temporal_restart_roundtrip
from .world import prepare_trial_world

CONTINUITY_VARIANTS = ("transcript-summary", "langgraph-sqlite", "temporal-workflow", "ordivon-typed")


def _checkpoint(machine: ScenarioMachine):
    state = machine.world.initial_state()
    initial = state
    state = machine.failed_attempt(state)
    state = machine.revise_world_goal_and_catalog(state)
    state = machine.commit_with_lost_response(state)
    return initial, state


def run_continuity_variant(
    fixture: str | Path,
    variant: str,
    *,
    working_root: str | Path,
    temporal_cache: str | Path,
) -> TrialRecord:
    if variant not in CONTINUITY_VARIANTS:
        raise ValueError(f"unsupported continuity variant: {variant}")
    start = perf_counter()
    trial_root = Path(working_root) / variant
    world = prepare_trial_world(fixture, trial_root / "world")
    machine = ScenarioMachine(world)
    initial, checkpoint = _checkpoint(machine)
    durable_bytes = 0
    framework: dict[str, JsonValue] = {}
    lost_pending = False

    if variant == "transcript-summary":
        store = TranscriptSummaryStore(trial_root / "state", omit_pending_on_summary=True)
        store.save(checkpoint, machine.events)
        recovered = store.load_for_resume()
        durable_bytes = store.byte_length
        framework = {"rawTranscriptUsedForResume": False, "summaryBounded": True}
        lost_pending = not recovered.pending_operations
    elif variant == "langgraph-sqlite":
        db_path = trial_root / "state" / "langgraph.sqlite3"
        store = LangGraphStateStore(db_path, thread_id=checkpoint.task_id)
        store.save(checkpoint)
        durable_bytes = store.byte_length
        store.close()
        fresh = LangGraphStateStore(db_path, thread_id=checkpoint.task_id)
        recovered = fresh.load()
        durable_bytes = fresh.byte_length
        fresh.close()
        framework = {**dependency_identity(), "threadId": checkpoint.task_id, "processReopened": True}
    elif variant == "temporal-workflow":
        recovered, temporal_meta = asyncio.run(
            temporal_restart_roundtrip(
                initial,
                checkpoint,
                workflow_id=f"round1-{checkpoint.task_id.replace(':', '-')}",
                download_dir=temporal_cache,
            )
        )
        framework = dict(temporal_meta)
        durable_bytes = len(str(checkpoint.to_dict()).encode("utf-8"))
    else:
        state_path = trial_root / "state" / "ordivon-work-state.json"
        store = JsonStateStore(state_path)
        store.save(checkpoint)
        durable_bytes = store.byte_length
        recovered = JsonStateStore(state_path).load()
        framework = {"typedDigestValidated": True, "processReopened": True}

    recovered = machine.replace_provider(recovered)
    recovery_error: str | None = None
    try:
        reconciled = machine.reconcile(
            recovered,
            blind_retry_when_missing=variant == "transcript-summary",
        )
    except RuntimeError as error:
        recovery_error = str(error)
        reconciled = recovered
    final, grade = machine.verify(reconciled)
    failures = list(hard_failures(grade, lost_pending=lost_pending, trusted_poison=False))
    if recovery_error is not None:
        failures.append("recovery-error")
    failures = sorted(set(failures))
    status = TrialStatus.PASSED if not failures else TrialStatus.FAILED
    spec = ExperimentSpec(
        experiment_id=f"experiment:round1-continuity-{variant}",
        work_package="continuity",
        variant=variant,
        fixture_digest=world.manifest.fixture_digest,
        faults=(
            Fault.ATTEMPT_FAILURE,
            Fault.GOAL_CLARIFICATION,
            Fault.REPOSITORY_DRIFT,
            Fault.TOOL_CONTRACT_DRIFT,
            Fault.RESPONSE_LOSS_AFTER_COMMIT,
            Fault.HOST_RESTART,
            Fault.PROVIDER_REPLACEMENT,
        ),
    )
    elapsed_ms = int((perf_counter() - start) * 1000)
    disposition = (
        DecisionDisposition.LOCALIZE
        if variant in {"langgraph-sqlite", "temporal-workflow"} and status is TrialStatus.PASSED
        else DecisionDisposition.INCOMPLETE
    )
    return TrialRecord(
        spec=spec,
        status=status,
        world_manifest_digest=canonical_digest(world.manifest.to_dict()),
        initial_state_digest=initial.digest,
        final_state_digest=final.digest,
        accepted_outcome=status is TrialStatus.PASSED,
        hard_failures=tuple(failures),
        observations={
            "framework": framework,
            "checkpointDigest": checkpoint.digest,
            "recoveredDigest": recovered.digest,
            "providerReplaced": recovered.provider_id == "provider:scripted-b",
            "pendingOperationRecovered": bool(recovered.pending_operations),
            "recoveryError": recovery_error,
            "worldGrade": grade,
            "eventCount": len(machine.events),
            "firstUsefulAction": (
                "observe-existing-operation" if recovered.pending_operations else recovered.frontier[0]
            ),
        },
        costs={
            "elapsedMs": elapsed_ms,
            "durableBytes": durable_bytes,
            "contextTokensEstimated": max(1, durable_bytes // 4),
            "modelCalls": 0,
            "toolCalls": 4,
        },
        disposition=disposition,
    )


def run_continuity_matrix(
    fixture: str | Path,
    *,
    working_root: str | Path,
    temporal_cache: str | Path,
) -> list[TrialRecord]:
    return [
        run_continuity_variant(
            fixture,
            variant,
            working_root=working_root,
            temporal_cache=temporal_cache,
        )
        for variant in CONTINUITY_VARIANTS
    ]
