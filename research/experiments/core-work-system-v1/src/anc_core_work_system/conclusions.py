from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Any, Mapping

from .model import JsonValue, canonical_digest


class ConclusionError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class EvidenceInputs:
    matrix_path: Path
    live_path: Path
    host_source_revision: str
    host_receipt_digest: str


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ConclusionError(f"evidence is not an object: {path}")
    return value


def _trial_by_variant(matrix: Mapping[str, Any], variant: str) -> Mapping[str, Any]:
    trials = matrix.get("trials")
    if not isinstance(trials, list):
        raise ConclusionError("matrix trials are missing")
    matches = [
        item
        for item in trials
        if isinstance(item, dict)
        and isinstance(item.get("spec"), dict)
        and item["spec"].get("variant") == variant
    ]
    if len(matches) != 1:
        raise ConclusionError(f"matrix variant is missing or duplicated: {variant}")
    return matches[0]


def _require_status(trial: Mapping[str, Any], status: str) -> None:
    if trial.get("status") != status:
        spec = trial.get("spec")
        variant = spec.get("variant") if isinstance(spec, dict) else None
        raise ConclusionError(f"unexpected status for {variant}: {trial.get('status')}")


def derive_closeout(inputs: EvidenceInputs) -> dict[str, JsonValue]:
    matrix = _load_object(inputs.matrix_path)
    live = _load_object(inputs.live_path)
    if matrix.get("kind") != "anc.core-work-system-deterministic-matrix":
        raise ConclusionError("unexpected deterministic matrix kind")
    if live.get("kind") != "anc.round1-live-provider-gauntlet":
        raise ConclusionError("unexpected live gauntlet kind")
    summary = matrix.get("summary")
    if not isinstance(summary, dict) or summary.get("trialCount") != 16:
        raise ConclusionError("deterministic matrix is incomplete")
    if summary.get("passed") != 10 or summary.get("failed") != 6:
        raise ConclusionError("deterministic matrix outcome differs")
    if live.get("trialCount") != 6 or live.get("acceptedTrials") != 6 or live.get("failedTrials") != 0:
        raise ConclusionError("live Provider gauntlet is incomplete")

    for variant in (
        "langgraph-sqlite",
        "temporal-workflow",
        "ordivon-typed",
        "retrieval-current",
        "source-bound",
        "idempotency-audit",
        "durable-activity",
        "ordivon-effect",
        "approval-everywhere",
        "evidence-rich",
    ):
        _require_status(_trial_by_variant(matrix, variant), "passed")
    for variant in (
        "transcript-summary",
        "full-transcript",
        "rolling-summary",
        "plain-tool",
        "static-risk",
        "model-selected",
    ):
        _require_status(_trial_by_variant(matrix, variant), "failed")

    live_trials = live.get("trials")
    if not isinstance(live_trials, list) or any(
        not isinstance(item, dict)
        or item.get("acceptedOutcome") is not True
        or item.get("hardFailures") != []
        or item.get("originalTranscriptLoaded") is not False
        or item.get("persistentProviderSessionRetained") is not False
        or not isinstance(item.get("worldGrade"), dict)
        or item["worldGrade"].get("duplicateWorldEffects") != 0
        for item in live_trials
    ):
        raise ConclusionError("live trial invariants differ")

    payload: dict[str, JsonValue] = {
        "schemaVersion": 1,
        "kind": "anc.core-work-system-round1-closeout",
        "evidence": {
            "deterministicMatrixDigest": matrix.get("matrixDigest"),
            "liveGauntletDigest": live.get("gauntletDigest"),
            "fixtureDigest": live.get("fixtureDigest"),
            "hostSourceRevision": inputs.host_source_revision,
            "hostReceiptDigest": inputs.host_receipt_digest,
        },
        "observedResults": {
            "deterministicTrials": 16,
            "deterministicPassed": 10,
            "deterministicFailed": 6,
            "liveProviderTrials": 6,
            "liveProviderAccepted": 6,
            "providerOrders": live.get("orders"),
            "crossBackendEffectPromotionBlocked": summary.get(
                "crossBackendEffectPromotionBlocked"
            ),
        },
        "dispositions": {
            "E1-open-work-continuity": {
                "decision": "localize",
                "scope": "Host application schema and handoff projection",
                "reason": (
                    "LangGraph SQLite, Temporal Workflow state, and Ordivon typed state all "
                    "recovered the pending operation without duplicate world Effects. No separate "
                    "Ordivon Task Runtime advantage was demonstrated."
                ),
            },
            "E2-effect-commitment": {
                "decision": "shrink",
                "scope": (
                    "stable request/effect identity, explicit UNKNOWN, backend correlation, "
                    "reconciliation, and no blind redispatch"
                ),
                "reason": (
                    "Idempotency plus audit and a durable Activity matched the single-backend "
                    "outcome with fewer state objects. Full cross-backend Effect/Binding/Dispatch "
                    "promotion remains deferred to the Edge experiment."
                ),
            },
            "E3-context-provenance": {
                "decision": "shrink",
                "scope": "revision, trust, attribution, and invalidation metadata in Host Context",
                "reason": (
                    "Revision-filtered retrieval matched source-bound Context on the frozen "
                    "workload with lower measured context size. A generalized Context Kernel was "
                    "not justified."
                ),
            },
            "E5-operator-attention": {
                "decision": "localize",
                "scope": "Host DecisionRequest UX and lifecycle",
                "reason": (
                    "Evidence-rich routing avoided missed escalations with fewer interruptions than "
                    "approval-everywhere, but the evidence is mechanical and single-operator claims "
                    "remain untested. No universal attention plane is promoted."
                ),
            },
            "E7-provider-replacement": {
                "decision": "retain",
                "scope": "provider-neutral semantic state and replaceable Host adapters",
                "reason": (
                    "Six live trials in both Codex/Hermes orders continued after response loss "
                    "without original transcript, persistent Provider session, blind retry, or "
                    "duplicate world Effects. This proves bounded state portability, not equal model "
                    "performance."
                ),
            },
        },
        "repositoryActions": {
            "runtimeProductionChanged": False,
            "defaultOpenProposalHostBroadened": False,
            "protocolPromoted": False,
            "round2Dependency": "Edge structured Fetch/Browser Effect backend",
        },
    }
    payload["closeoutDigest"] = canonical_digest(payload)
    return payload


def write_closeout(inputs: EvidenceInputs, output: Path) -> dict[str, JsonValue]:
    payload = derive_closeout(inputs)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return payload
