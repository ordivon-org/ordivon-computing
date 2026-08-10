from __future__ import annotations

import hashlib
import json
from typing import Any

LIFECYCLE_CLASSES = (
    "authoritative",
    "evidence",
    "rebuildable",
    "ephemeral",
    "cache",
    "compatibility",
    "quarantine",
    "unknown",
)
AUTO_RECLAIMABLE_CLASSES = {"rebuildable", "ephemeral", "cache"}
PROTECTED_CLASSES = {"authoritative", "evidence", "compatibility", "quarantine", "unknown"}


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def cleanup_decision(
    lifecycle_class: str,
    *,
    active_references: bool,
    dirty: bool,
    owner_reclaim_operation: str | None,
    rebuildable: bool,
) -> dict[str, Any]:
    if lifecycle_class not in LIFECYCLE_CLASSES:
        raise ValueError(f"unknown lifecycle class: {lifecycle_class}")
    if active_references:
        return {"decision": "protect", "reason": "active_references", "automaticActionAllowed": False}
    if dirty:
        return {"decision": "review", "reason": "dirty_state", "automaticActionAllowed": False}
    if lifecycle_class in PROTECTED_CLASSES:
        return {"decision": "protect", "reason": f"protected_class:{lifecycle_class}", "automaticActionAllowed": False}
    if lifecycle_class in AUTO_RECLAIMABLE_CLASSES and owner_reclaim_operation and rebuildable:
        return {"decision": "owner_reclaim_candidate", "reason": "owner_declared_rebuildable_and_reclaimable", "automaticActionAllowed": True, "ownerReclaimOperation": owner_reclaim_operation}
    return {"decision": "review", "reason": "insufficient_reclaim_evidence", "automaticActionAllowed": False}


def _host_signal(host: dict[str, Any]) -> dict[str, Any]:
    doctor = host.get("doctor") or {}
    checks = doctor.get("checks") or []
    failing = [item.get("name") for item in checks if item.get("status") != "ok"]
    authority = host.get("authority") or {}
    return {"owner": "ordivon-host", "area": "authority-integrity", "state": "attention" if failing else "healthy", "facts": {"journalSchema": authority.get("journalSchema"), "events": authority.get("events"), "tasks": authority.get("tasks"), "leases": authority.get("leases"), "failingChecks": failing}}


def _runtime_health_signal(status: dict[str, Any]) -> dict[str, Any]:
    deployment = status.get("deployment") or {}
    artifacts = deployment.get("artifacts") or []
    mismatches = [item.get("name") for item in artifacts if item.get("matches") is False]
    health = status.get("health") or {}
    service = status.get("service") or {}
    registry = status.get("registry") or {}
    unhealthy = status.get("status") != "healthy" or health.get("status") != "healthy" or bool(mismatches)
    return {"owner": "ordivon-runtime", "area": "runtime-health-and-deployment", "state": "attention" if unhealthy else "healthy", "facts": {"deployedCommit": deployment.get("commit"), "toolCount": deployment.get("toolCount"), "serviceState": service.get("activeState"), "restarts": service.get("restarts"), "jobsActive": registry.get("jobsActive"), "recoveryRequired": registry.get("recoveryRequired"), "artifactMismatches": mismatches}}


def _runtime_lifecycle_signal(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary") or {}
    counts = summary.get("counts") or {}
    return {"owner": "ordivon-runtime", "area": "workspace-lifecycle", "state": "attention" if summary.get("policyEligible", 0) or counts.get("blocked_dirty", 0) else "healthy", "facts": {"counts": counts, "policyEligible": summary.get("policyEligible", 0), "policyEligibleEstimatedBytes": summary.get("policyEligibleEstimatedBytes", 0)}}


def _runtime_cache_signal(report: dict[str, Any]) -> dict[str, Any]:
    summary = report.get("summary") or {}
    issues = report.get("issues") or []
    legacy = int(summary.get("legacyBytes") or 0)
    return {"owner": "ordivon-runtime", "area": "execution-cache", "state": "attention" if issues or legacy else "healthy", "facts": {"legacyBytes": legacy, "issues": len(issues), "sourceGroups": summary.get("sourceGroups")}}


def _content_signal(report: dict[str, Any]) -> dict[str, Any]:
    repositories = report.get("repositories") or []
    blocked = [item.get("projectId") for item in repositories if item.get("contentState") == "BLOCKED"]
    degraded = [item.get("projectId") for item in repositories if item.get("contentState") == "DEGRADED"]
    totals = report.get("totals") or {}
    return {"owner": "ordivon-computing", "area": "content-lifecycle", "state": "attention" if blocked or degraded else "healthy", "facts": {"repositories": totals.get("repositories", len(repositories)), "documents": totals.get("documents"), "metadataDocuments": totals.get("metadataDocuments"), "blockedProjects": blocked, "degradedProjects": degraded}}


def _conformance_signal(report: dict[str, Any]) -> dict[str, Any]:
    return {"owner": "ordivon-computing", "area": "cross-project-conformance", "state": "healthy" if report.get("passed") is True else "attention", "facts": {"passed": report.get("passed"), "exitCode": report.get("exitCode"), "blockedBy": report.get("blockedBy")}}


def _owner_doctor_signal(report: dict[str, Any]) -> dict[str, Any]:
    status = report.get("status")
    failed = report.get("failedChecks") or []
    return {
        "owner": report.get("owner", "unknown-owner"),
        "area": "owner-doctor",
        "state": "healthy" if status in {"ok", "healthy"} and not failed else "attention",
        "facts": {
            "sourceKind": report.get("sourceKind"),
            "status": status,
            "checks": report.get("checks"),
            "failedChecks": failed,
            "skippedChecks": report.get("skippedChecks", 0),
        },
    }


def build_projection(*, host_status: dict[str, Any], runtime_status: dict[str, Any], runtime_lifecycle: dict[str, Any], runtime_cache: dict[str, Any], content_baseline: dict[str, Any], conformance_status: dict[str, Any], owner_doctors: list[dict[str, Any]], compatibility_summary: dict[str, Any], dirty_aging_summary: dict[str, Any]) -> dict[str, Any]:
    inputs = {"host": canonical_digest(host_status), "runtimeStatus": canonical_digest(runtime_status), "runtimeLifecycle": canonical_digest(runtime_lifecycle), "runtimeCache": canonical_digest(runtime_cache), "contentBaseline": canonical_digest(content_baseline), "conformanceStatus": canonical_digest(conformance_status), "ownerDoctors": canonical_digest(owner_doctors), "compatibility": canonical_digest(compatibility_summary), "dirtyAging": canonical_digest(dirty_aging_summary)}
    signals = [
        _host_signal(host_status),
        _runtime_health_signal(runtime_status),
        _runtime_lifecycle_signal(runtime_lifecycle),
        _runtime_cache_signal(runtime_cache),
        _content_signal(content_baseline),
        _conformance_signal(conformance_status),
        *[_owner_doctor_signal(report) for report in owner_doctors],
        {"owner": "crosscut-projection", "area": "compatibility-debt", "state": "attention" if compatibility_summary.get("removableCandidates") or compatibility_summary.get("unsupportedDebt") else "healthy", "facts": compatibility_summary},
        {"owner": "ordivon-runtime", "area": "dirty-workspace-aging", "state": "attention" if dirty_aging_summary.get("actionable") else "healthy", "facts": dirty_aging_summary},
    ]
    result = {"schemaVersion": 1, "kind": "ordivon.crosscut-maintenance-projection", "truthRole": "rebuildable-read-only-projection", "inputDigests": inputs, "lifecycleVocabulary": list(LIFECYCLE_CLASSES), "signals": signals, "summary": {"attentionSignals": sum(item["state"] == "attention" for item in signals), "healthySignals": sum(item["state"] == "healthy" for item in signals)}, "truthBoundary": {"projectionAuthoritative": False, "ownerNativeFactsRemainAuthoritative": True, "cleanupAuthorityDelegatedToOwner": True, "unknownNeverAutoDeleted": True, "dirtyNeverAutoDeleted": True}}
    result["projectionDigest"] = canonical_digest(result)
    return result
