from __future__ import annotations

from typing import Any

REQUIRED_FIELDS = {
    "id",
    "owner",
    "path",
    "reason",
    "removalPredicate",
    "evidenceRefs",
}


def evaluate_entry(entry: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED_FIELDS - set(entry))
    if missing:
        raise ValueError("missing compatibility fields: " + ", ".join(missing))
    current_consumers = [value for value in entry.get("currentConsumers", []) if value]
    protected_state = [value for value in entry.get("protectedState", []) if value]
    recovery = [value for value in entry.get("recoveryRequirements", []) if value]
    external = [value for value in entry.get("externalContracts", []) if value]
    evidence = [value for value in entry.get("evidenceRefs", []) if value]
    blockers = {
        "currentConsumers": current_consumers,
        "protectedState": protected_state,
        "recoveryRequirements": recovery,
        "externalContracts": external,
    }
    removed = entry.get("removed") is True
    if removed and any(blockers.values()):
        raise ValueError(f"removed compatibility entry still has blockers: {entry['id']}")
    if removed:
        disposition = "removed"
    elif any(blockers.values()):
        disposition = "retain_narrowest_compatible_form"
    elif entry.get("removalPredicate") and evidence:
        disposition = "removable_candidate"
    else:
        disposition = "unsupported_debt"
    return {
        "id": entry["id"],
        "owner": entry["owner"],
        "path": entry["path"],
        "disposition": disposition,
        "blockers": blockers,
    }


def summarize(entries: list[dict[str, Any]]) -> dict[str, Any]:
    evaluated = [evaluate_entry(entry) for entry in entries]
    return {
        "entries": len(evaluated),
        "removed": sum(item["disposition"] == "removed" for item in evaluated),
        "retained": sum(item["disposition"] == "retain_narrowest_compatible_form" for item in evaluated),
        "removableCandidates": sum(item["disposition"] == "removable_candidate" for item in evaluated),
        "unsupportedDebt": sum(item["disposition"] == "unsupported_debt" for item in evaluated),
        "evaluated": evaluated,
    }
