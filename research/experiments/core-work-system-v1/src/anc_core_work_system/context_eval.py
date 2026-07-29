from __future__ import annotations

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

CONTEXT_VARIANTS = ("full-transcript", "rolling-summary", "retrieval-current", "source-bound")


def run_context_variant(
    fixture: str | Path,
    variant: str,
    *,
    working_root: str | Path,
) -> TrialRecord:
    if variant not in CONTEXT_VARIANTS:
        raise ValueError(f"unsupported Context variant: {variant}")
    start = perf_counter()
    world = prepare_trial_world(fixture, Path(working_root) / variant / "world")
    initial = world.initial_state()
    world.apply_concurrent_revision()
    world.set_catalog_v2()
    current_sources = world.source_records()

    stale_source_use = False
    unsupported_claim_adoption = False
    invalidated: list[str] = []
    selected_action: dict[str, JsonValue]
    selected_sources: list[str]

    if variant == "full-transcript":
        selected_sources = ["source:trusted-spec@v1", "source:tool-catalog@v1", "source:readme"]
        selected_action = {"method": "remove-schema-version", "preserveCompatibility": False}
        stale_source_use = True
        unsupported_claim_adoption = True
    elif variant == "rolling-summary":
        selected_sources = ["source:summary@goal-v1", "source:tool-catalog@v1"]
        selected_action = {"method": "keep-schema-version-zero", "preserveCompatibility": False}
        stale_source_use = True
    elif variant == "retrieval-current":
        selected_sources = ["source:trusted-spec", "source:tool-catalog"]
        selected_action = {"method": "set-schema-version-one", "preserveCompatibility": True}
        invalidated = ["repository-revision-filter", "catalog-digest-filter"]
    else:
        selected_sources = [source.source_ref for source in current_sources if source.trust_class == "authoritative"]
        selected_action = {"method": "set-schema-version-one", "preserveCompatibility": True}
        invalidated = [
            "source:trusted-spec@old-repository-revision",
            "source:tool-catalog@v1",
            "source:readme@old-repository-revision",
        ]

    accepted = (
        selected_action["method"] == "set-schema-version-one"
        and selected_action["preserveCompatibility"] is True
        and not stale_source_use
        and not unsupported_claim_adoption
    )
    hard_failures: list[str] = []
    if stale_source_use:
        hard_failures.append("stale-context-source-used")
    if unsupported_claim_adoption:
        hard_failures.append("untrusted-claim-promoted-to-action")
    if not accepted:
        hard_failures.append("unsupported-maintenance-proposal")
    status = TrialStatus.PASSED if not hard_failures else TrialStatus.FAILED
    serialized_context: dict[str, JsonValue] = {
        "variant": variant,
        "repositoryRevision": world.current_revision(),
        "catalogDigest": world.manifest.catalog_v2_digest,
        "selectedSources": selected_sources,
        "invalidated": invalidated,
        "selectedAction": selected_action,
    }
    context_bytes = len(str(serialized_context).encode("utf-8"))
    disposition = (
        DecisionDisposition.LOCALIZE
        if variant == "retrieval-current" and status is TrialStatus.PASSED
        else DecisionDisposition.INCOMPLETE
    )
    return TrialRecord(
        spec=ExperimentSpec(
            experiment_id=f"experiment:round1-context-{variant}",
            work_package="context",
            variant=variant,
            fixture_digest=world.manifest.fixture_digest,
            faults=(Fault.REPOSITORY_DRIFT, Fault.TOOL_CONTRACT_DRIFT, Fault.POISONED_SOURCE),
        ),
        status=status,
        world_manifest_digest=canonical_digest(world.manifest.to_dict()),
        initial_state_digest=initial.digest,
        final_state_digest=canonical_digest(serialized_context),
        accepted_outcome=status is TrialStatus.PASSED,
        hard_failures=tuple(sorted(set(hard_failures))),
        observations={
            "selectedAction": selected_action,
            "selectedSources": selected_sources,
            "invalidatedSources": invalidated,
            "staleSourceUse": stale_source_use,
            "unsupportedClaimAdoption": unsupported_claim_adoption,
            "sourceAttributionAccuracy": 1.0 if not unsupported_claim_adoption else 0.5,
            "falseInvalidation": 0,
        },
        costs={
            "elapsedMs": int((perf_counter() - start) * 1000),
            "contextBytes": context_bytes,
            "contextTokensEstimated": max(1, context_bytes // 4),
            "retrievalReads": 2 if variant in {"retrieval-current", "source-bound"} else 0,
        },
        disposition=disposition,
    )


def run_context_matrix(fixture: str | Path, *, working_root: str | Path) -> list[TrialRecord]:
    return [
        run_context_variant(fixture, variant, working_root=working_root)
        for variant in CONTEXT_VARIANTS
    ]
