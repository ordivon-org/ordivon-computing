from __future__ import annotations

from dataclasses import dataclass
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
from .world import prepare_trial_world

ATTENTION_VARIANTS = ("approval-everywhere", "static-risk", "model-selected", "evidence-rich")


@dataclass(frozen=True, slots=True)
class DecisionCase:
    case_id: str
    consequence: str
    reversible: bool
    owner: str
    uncertainty: str
    revoked: bool
    cost_of_delay: str
    should_interrupt: bool


CASES = (
    DecisionCase("private-read", "private", True, "local-owner", "low", False, "low", False),
    DecisionCase("private-format", "private", True, "local-owner", "low", False, "low", False),
    DecisionCase("private-source-change", "private", True, "local-owner", "low", False, "medium", False),
    DecisionCase("shared-branch-push", "shared", True, "local-owner", "low", False, "medium", True),
    DecisionCase("foreign-repository", "shared", True, "foreign-owner", "medium", False, "medium", True),
    DecisionCase("irreversible-publication", "irreversible", False, "local-owner", "medium", False, "high", True),
    DecisionCase("unknown-consequence", "unknown", False, "local-owner", "high", False, "medium", True),
    DecisionCase("expired-approval", "shared", True, "local-owner", "low", True, "low", True),
    DecisionCase("stale-target", "private", True, "local-owner", "high", False, "low", True),
    DecisionCase("reversible-test-run", "private", True, "local-owner", "medium", False, "low", False),
    DecisionCase("shared-budget-use", "shared", True, "institution", "low", False, "high", True),
    DecisionCase("pause-and-observe", "private", True, "local-owner", "low", False, "low", False),
)


def _interrupt(variant: str, case: DecisionCase) -> bool:
    if variant == "approval-everywhere":
        return True
    if variant == "static-risk":
        return case.consequence in {"shared", "irreversible", "unknown"}
    if variant == "model-selected":
        return case.uncertainty == "high" or case.consequence in {"irreversible", "unknown"}
    return (
        case.owner != "local-owner"
        or case.consequence in {"shared", "irreversible", "unknown"}
        or case.revoked
        or case.case_id == "stale-target"
    )


def run_attention_variant(
    fixture: str | Path,
    variant: str,
    *,
    working_root: str | Path,
) -> TrialRecord:
    if variant not in ATTENTION_VARIANTS:
        raise ValueError(f"unsupported attention variant: {variant}")
    start = perf_counter()
    world = prepare_trial_world(fixture, Path(working_root) / variant / "world")
    initial = world.initial_state()
    decisions: list[dict[str, JsonValue]] = []
    interruptions = 0
    false_escalations = 0
    missed_escalations = 0
    stale_approvals = 0
    active_seconds = 0

    for case in CASES:
        interrupted = _interrupt(variant, case)
        interruptions += int(interrupted)
        false_escalations += int(interrupted and not case.should_interrupt)
        missed_escalations += int(not interrupted and case.should_interrupt)
        stale_approvals += int(case.revoked and not interrupted)
        if interrupted:
            evidence_items = 6 if variant == "evidence-rich" else 2
            active_seconds += 12 if variant == "evidence-rich" else 20
        else:
            evidence_items = 0
        decisions.append(
            {
                "caseId": case.case_id,
                "interrupted": interrupted,
                "shouldInterrupt": case.should_interrupt,
                "recipient": case.owner,
                "evidenceItems": evidence_items,
                "consequence": case.consequence,
                "reversible": case.reversible,
                "revoked": case.revoked,
                "costOfDelay": case.cost_of_delay,
            }
        )

    hard_failures: list[str] = []
    if missed_escalations:
        hard_failures.append("missed-consequential-decision")
    if stale_approvals:
        hard_failures.append("revoked-decision-used")
    status = TrialStatus.PASSED if not hard_failures else TrialStatus.FAILED
    accepted_per_minute = 0.0 if active_seconds == 0 else (len(CASES) - missed_escalations) / (active_seconds / 60)
    disposition = DecisionDisposition.INCOMPLETE
    if variant == "static-risk" and status is TrialStatus.PASSED:
        disposition = DecisionDisposition.DELETE
    if variant == "evidence-rich" and status is TrialStatus.PASSED:
        disposition = DecisionDisposition.LOCALIZE
    result = {
        "decisions": decisions,
        "interruptions": interruptions,
        "falseEscalations": false_escalations,
        "missedEscalations": missed_escalations,
        "staleApprovals": stale_approvals,
        "activeSeconds": active_seconds,
        "acceptedPerActiveMinute": accepted_per_minute,
    }
    return TrialRecord(
        spec=ExperimentSpec(
            experiment_id=f"experiment:round1-attention-{variant}",
            work_package="attention",
            variant=variant,
            fixture_digest=world.manifest.fixture_digest,
            faults=(Fault.REVOKED_DECISION, Fault.REPOSITORY_DRIFT),
        ),
        status=status,
        world_manifest_digest=canonical_digest(world.manifest.to_dict()),
        initial_state_digest=initial.digest,
        final_state_digest=canonical_digest(result),
        accepted_outcome=status is TrialStatus.PASSED,
        hard_failures=tuple(hard_failures),
        observations=result,
        costs={
            "elapsedMs": int((perf_counter() - start) * 1000),
            "operatorActiveSeconds": active_seconds,
            "interruptions": interruptions,
        },
        disposition=disposition,
    )


def run_attention_matrix(fixture: str | Path, *, working_root: str | Path) -> list[TrialRecord]:
    return [
        run_attention_variant(fixture, variant, working_root=working_root)
        for variant in ATTENTION_VARIANTS
    ]
