from __future__ import annotations

from collections import defaultdict
from statistics import mean, median
from typing import Any, Mapping

from .model import JsonValue, canonical_digest


class ReportStatisticsError(RuntimeError):
    pass


def _trials(value: Mapping[str, Any], kind: str) -> list[dict[str, Any]]:
    if value.get("kind") != kind:
        raise ReportStatisticsError(f"unexpected evidence kind: {value.get('kind')}")
    trials = value.get("trials")
    if not isinstance(trials, list) or any(not isinstance(item, dict) for item in trials):
        raise ReportStatisticsError("evidence trials are missing or malformed")
    return trials


def _round(value: float, digits: int = 6) -> float:
    return round(value, digits)


def derive_report_statistics(
    matrix: Mapping[str, Any],
    live: Mapping[str, Any],
) -> dict[str, JsonValue]:
    deterministic_trials = _trials(matrix, "anc.core-work-system-deterministic-matrix")
    live_trials = _trials(live, "anc.round1-live-provider-gauntlet")
    if len(deterministic_trials) != 16:
        raise ReportStatisticsError("Round 1 requires 16 deterministic trials")
    if len(live_trials) != 6:
        raise ReportStatisticsError("Round 1 requires six live Provider trials")

    packages: dict[str, list[dict[str, Any]]] = defaultdict(list)
    variants: dict[str, dict[str, Any]] = {}
    for trial in deterministic_trials:
        spec = trial.get("spec")
        if not isinstance(spec, dict):
            raise ReportStatisticsError("deterministic Trial has no ExperimentSpec")
        package = str(spec.get("workPackage"))
        variant = str(spec.get("variant"))
        packages[package].append(trial)
        variants[variant] = trial

    package_summary: dict[str, JsonValue] = {}
    for package, trials in sorted(packages.items()):
        passed = sum(int(item.get("acceptedOutcome") is True) for item in trials)
        package_summary[package] = {
            "trials": len(trials),
            "passed": passed,
            "failed": len(trials) - passed,
            "passRate": _round(passed / len(trials)),
        }

    order_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trial in live_trials:
        order_groups[str(trial.get("order"))].append(trial)

    live_by_order: dict[str, JsonValue] = {}
    for order, trials in sorted(order_groups.items()):
        elapsed = [int(item["elapsedMs"]) for item in trials]
        tokens = [int(item.get("reportedProviderTokens") or 0) for item in trials]
        costs = [float(item.get("reportedProviderCostUsd") or 0.0) for item in trials]
        live_by_order[order] = {
            "trials": len(trials),
            "accepted": sum(int(item.get("acceptedOutcome") is True) for item in trials),
            "elapsedMs": {
                "min": min(elapsed),
                "max": max(elapsed),
                "mean": _round(mean(elapsed), 3),
            },
            "reportedProviderTokens": {
                "total": sum(tokens),
                "mean": _round(mean(tokens), 3),
            },
            "reportedProviderCostUsd": {
                "total": _round(sum(costs), 8),
                "mean": _round(mean(costs), 8),
            },
        }

    live_elapsed = [int(item["elapsedMs"]) for item in live_trials]
    live_tokens = [int(item.get("reportedProviderTokens") or 0) for item in live_trials]
    live_costs = [float(item.get("reportedProviderCostUsd") or 0.0) for item in live_trials]

    def costs_for(variant: str) -> Mapping[str, Any]:
        trial = variants.get(variant)
        if trial is None or not isinstance(trial.get("costs"), dict):
            raise ReportStatisticsError(f"missing costs for {variant}")
        return trial["costs"]

    retrieval = costs_for("retrieval-current")
    source_bound = costs_for("source-bound")
    approval = costs_for("approval-everywhere")
    evidence_rich = costs_for("evidence-rich")

    payload: dict[str, JsonValue] = {
        "schemaVersion": 1,
        "kind": "anc.core-work-system-report-statistics",
        "source": {
            "deterministicMatrixDigest": matrix.get("matrixDigest"),
            "liveGauntletDigest": live.get("gauntletDigest"),
            "fixtureDigest": live.get("fixtureDigest"),
        },
        "deterministic": {
            "trials": len(deterministic_trials),
            "passed": sum(
                int(item.get("acceptedOutcome") is True) for item in deterministic_trials
            ),
            "failed": sum(
                int(item.get("acceptedOutcome") is not True) for item in deterministic_trials
            ),
            "packages": package_summary,
        },
        "live": {
            "trials": len(live_trials),
            "accepted": sum(int(item.get("acceptedOutcome") is True) for item in live_trials),
            "failed": sum(int(item.get("acceptedOutcome") is not True) for item in live_trials),
            "elapsedMs": {
                "total": sum(live_elapsed),
                "min": min(live_elapsed),
                "max": max(live_elapsed),
                "mean": _round(mean(live_elapsed), 3),
                "median": _round(median(live_elapsed), 3),
            },
            "reportedProviderTokens": {
                "total": sum(live_tokens),
                "mean": _round(mean(live_tokens), 3),
            },
            "reportedProviderCostUsd": {
                "total": _round(sum(live_costs), 8),
                "mean": _round(mean(live_costs), 8),
            },
            "byOrder": live_by_order,
        },
        "derivedComparisons": {
            "sourceBoundContextByteOverheadVsCurrentRetrieval": _round(
                int(source_bound["contextBytes"]) / int(retrieval["contextBytes"]) - 1
            ),
            "evidenceRichInterruptionReductionVsApprovalEverywhere": _round(
                1
                - int(evidence_rich["interruptions"])
                / int(approval["interruptions"])
            ),
            "evidenceRichActiveTimeReductionVsApprovalEverywhere": _round(
                1
                - int(evidence_rich["operatorActiveSeconds"])
                / int(approval["operatorActiveSeconds"])
            ),
            "effectStateObjects": {
                name: int(costs_for(name)["stateObjects"])
                for name in (
                    "plain-tool",
                    "idempotency-audit",
                    "durable-activity",
                    "ordivon-effect",
                )
            },
        },
        "measurementNotes": {
            "reportedProviderMetering": (
                "Token and USD values are reported by Hermes calls only; Codex usage was not "
                "metered into the receipt."
            ),
            "continuityStorage": (
                "Durable byte counts are representation-specific and do not measure full backend "
                "infrastructure cost."
            ),
            "attentionTime": (
                "Operator active seconds are deterministic scenario estimates, not observed human "
                "timings."
            ),
            "elapsedTime": (
                "Elapsed times include different setup paths and are descriptive, not a performance "
                "ranking."
            ),
        },
    }
    payload["statisticsDigest"] = canonical_digest(payload)
    return payload
