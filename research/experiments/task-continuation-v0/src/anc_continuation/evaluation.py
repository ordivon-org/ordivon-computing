from __future__ import annotations

from typing import Any

from anc_canonical import JsonValue


class EvaluationError(RuntimeError):
    pass


def continuation_evaluation_report(evidence: dict[str, Any]) -> dict[str, JsonValue]:
    if evidence.get("kind") != "anc.continuation-evidence":
        raise EvaluationError("input is not an ANC continuation evidence receipt")
    baselines = evidence.get("baselines", {}).get("results")
    variants = evidence.get("ablations", {}).get("capsuleVariants")
    scripted = evidence.get("freshProcessScripted")
    drift = evidence.get("freshProcessDrift")
    codex = evidence.get("freshProcessCodex")
    if not isinstance(baselines, list) or not isinstance(variants, list):
        raise EvaluationError("continuation baselines or ablations are missing")
    if not isinstance(scripted, dict) or not isinstance(drift, dict):
        raise EvaluationError("fresh-process reference cases are missing")

    baseline_by_name = {
        item["baseline"]: item for item in baselines if isinstance(item, dict)
    }
    variant_by_name = {
        item["variant"]: item for item in variants if isinstance(item, dict)
    }
    required_baselines = {"fullTranscript", "manualHandoff", "noMemory"}
    required_variants = {
        "full",
        "withoutDecisionArtifact",
        "withoutCheckpointFact",
        "withoutCurrentBinding",
        "withoutCompletedEffects",
    }
    if set(baseline_by_name) != required_baselines:
        raise EvaluationError("continuation baseline set differs")
    if set(variant_by_name) != required_variants:
        raise EvaluationError("TaskCapsule ablation set differs")

    scripted_host = scripted.get("host")
    drift_host = drift.get("host")
    if not isinstance(scripted_host, dict) or not isinstance(drift_host, dict):
        raise EvaluationError("fresh-process Host receipts are missing")
    scripted_decision = scripted_host.get("decision")
    if not isinstance(scripted_decision, dict):
        raise EvaluationError("scripted Host decision is missing")

    codex_case: JsonValue = None
    model_agreement: JsonValue = None
    if codex is not None:
        if not isinstance(codex, dict) or not isinstance(codex.get("host"), dict):
            raise EvaluationError("Codex Host receipt is invalid")
        codex_host = codex["host"]
        codex_decision = codex_host.get("decision")
        if not isinstance(codex_decision, dict):
            raise EvaluationError("Codex decision is missing")
        model_agreement = all(
            codex_decision.get(field) == scripted_decision.get(field)
            for field in ("actionId", "kind", "effectId", "bindingId", "dispatchId")
        )
        codex_case = {
            "adapterId": codex_host.get("adapterId"),
            "status": codex_host.get("status"),
            "correctFirstAction": codex_decision.get("actionId")
            == evidence["baselines"]["expectedFirstAction"],
            "modelAgreement": model_agreement,
            "contextBytes": codex_host.get("contextBytes"),
            "elapsedMs": codex.get("elapsedMs"),
            "modelCallCount": codex.get("modelCallCount"),
            "humanCorrectionCount": codex.get("humanCorrectionCount"),
            "originalTranscriptLoaded": codex.get("originalTranscriptLoaded"),
        }

    hard_dependencies = [
        name
        for name in (
            "withoutDecisionArtifact",
            "withoutCheckpointFact",
            "withoutCurrentBinding",
        )
        if variant_by_name[name]["outcome"] == "fail-closed"
    ]
    provenance_dependency = (
        variant_by_name["withoutCompletedEffects"]["outcome"] == "valid"
        and not variant_by_name["withoutCompletedEffects"]["provenanceComplete"]
        and variant_by_name["withoutCompletedEffects"]["forbiddenEffectCount"] == 0
    )
    scripted_executed = scripted_host.get("executedEffects", [])
    repeated = sorted(
        set(evidence["baselines"]["results"][0].get("knownCompletedEffects", []))
        & set(scripted_executed)
    )
    criteria = {
        "fullTranscriptFirstActionCorrect": baseline_by_name["fullTranscript"][
            "correctFirstAction"
        ],
        "manualHandoffFirstActionCorrect": baseline_by_name["manualHandoff"][
            "correctFirstAction"
        ],
        "noMemoryExposesRepeatedEffect": bool(
            baseline_by_name["noMemory"]["repeatedCompletedEffects"]
        ),
        "capsuleCompletesInFreshProcess": scripted_host.get("status") == "completed",
        "freshProcessDoesNotLoadTranscript": scripted.get("originalTranscriptLoaded")
        is False,
        "worldDriftBlocksMutation": drift_host.get("status")
        == "blocked-world-drift",
        "completedEffectsNotRepeated": not repeated,
        "hardDependenciesFailClosed": len(hard_dependencies) == 3,
        "completedEffectsPreserveProvenance": provenance_dependency,
        "realModelAgreesWhenPresent": model_agreement in {None, True},
    }
    return {
        "schemaVersion": 1,
        "kind": "anc.continuation-evaluation-report",
        "sourceRevision": evidence.get("sourceRevision"),
        "capsuleDigest": evidence.get("capsuleDigest"),
        "criteria": criteria,
        "allRequiredCriteriaPassed": all(criteria.values()),
        "baselineComparison": {
            "fullTranscriptBytes": baseline_by_name["fullTranscript"]["bytes"],
            "manualHandoffBytes": baseline_by_name["manualHandoff"]["bytes"],
            "noMemoryBytes": baseline_by_name["noMemory"]["bytes"],
            "manualToTranscriptPermille": (
                1000
                * baseline_by_name["manualHandoff"]["bytes"]
                // baseline_by_name["fullTranscript"]["bytes"]
            ),
        },
        "capsuleAblation": {
            "fullCapsuleBytes": variant_by_name["full"]["bytes"],
            "hardDependencies": hard_dependencies,
            "completedEffectsAreProvenanceDependency": provenance_dependency,
        },
        "scriptedFreshHost": {
            "status": scripted_host.get("status"),
            "contextBytes": scripted_host.get("contextBytes"),
            "elapsedMs": scripted.get("elapsedMs"),
            "executedEffects": scripted_executed,
            "committedFacts": scripted_host.get("committedFacts"),
            "repeatedCompletedEffects": repeated,
        },
        "driftCase": {
            "status": drift_host.get("status"),
            "executedEffects": drift_host.get("executedEffects"),
            "worldBefore": drift_host.get("worldBefore"),
            "worldAfter": drift_host.get("worldAfter"),
        },
        "codexFreshHost": codex_case,
        "recommendation": {
            "retain": [
                "decision Artifact reference",
                "checkpoint Fact reference",
                "current Binding reference",
                "completed Effect references",
                "world binding and reread",
            ],
            "defer": [
                "provider router",
                "vector memory database",
                "generic Task graph runtime",
                "automatic Tool catalog service",
            ],
            "nextExperiment": (
                "Run #32 only with a second real provider/model adapter over the same Capsule; "
                "do not change stored Task state between models."
            ),
        },
    }
