from __future__ import annotations

from typing import Any


def classify_finding(
    finding: dict[str, Any],
    *,
    observer_path: str | None = None,
    canonical_human_path: str | None = None,
) -> dict[str, Any]:
    name = str(finding.get("name", "unknown"))
    severity = finding.get("severity")
    if name == "path:canonical-human" and observer_path and canonical_human_path and observer_path != canonical_human_path:
        classification = "observer_context_mismatch"
        owner_action = "reobserve_in_owner_context"
    elif name == "path:user-local-allowlist":
        classification = "provider_placement_drift"
        owner_action = "converge_provider_to_declared_authority"
    elif name.startswith("package-forbidden:"):
        classification = "owner_policy_drift"
        owner_action = "owner_review_temporary_equipment_or_remove"
    elif name == "windows-live:ambient-interop-privilege":
        classification = "ambient_privilege_warning"
        owner_action = "retain_explicit_limited_or_elevated_effect_boundary"
    elif name.startswith("network:"):
        classification = "owner_operational_drift"
        owner_action = "owner_network_review"
    else:
        classification = "owner_reported_finding"
        owner_action = "owner_review"
    return {
        "name": name,
        "severity": severity,
        "classification": classification,
        "ownerAction": owner_action,
        "centralPolicyMutationAllowed": False,
    }


def summarize_findings(
    findings: list[dict[str, Any]],
    *,
    observer_path: str | None = None,
    canonical_human_path: str | None = None,
) -> dict[str, Any]:
    classified = [
        classify_finding(
            finding,
            observer_path=observer_path,
            canonical_human_path=canonical_human_path,
        )
        for finding in findings
    ]
    counts: dict[str, int] = {}
    for item in classified:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
    return {
        "findings": classified,
        "counts": dict(sorted(counts.items())),
        "centralPolicyMutationAllowed": False,
    }
