from __future__ import annotations

from typing import Any

HOUR_MS = 3_600_000


def classify_dirty_workspaces(
    lifecycle_report: dict[str, Any],
    *,
    now_ms: int,
    checkpoint_after_hours: float = 24.0,
    review_after_hours: float = 72.0,
    quarantine_review_after_hours: float = 168.0,
) -> dict[str, Any]:
    queue: list[dict[str, Any]] = []
    for item in lifecycle_report.get("candidates", []):
        if item.get("classification") != "blocked_dirty":
            continue
        basis = item.get("lastActivityUnixMs") or item.get("createdUnixMs")
        if not isinstance(basis, int):
            age_hours = None
            action = "identity_review"
        else:
            age_hours = max(0.0, (now_ms - basis) / HOUR_MS)
            if age_hours >= quarantine_review_after_hours:
                action = "quarantine_review"
            elif age_hours >= review_after_hours:
                action = "owner_review"
            elif age_hours >= checkpoint_after_hours:
                action = "checkpoint_or_export"
            else:
                action = "recent_dirty"
        queue.append(
            {
                "workspaceId": item.get("workspaceId"),
                "sourceRepo": item.get("sourceRepo"),
                "sourceRevision": item.get("sourceRevision"),
                "recordDigest": item.get("recordDigest"),
                "estimatedBytes": item.get("estimatedBytes"),
                "dirtyPaths": item.get("dirtyPaths", []),
                "ageHours": age_hours,
                "action": action,
                "automaticDeletionAllowed": False,
            }
        )
    counts: dict[str, int] = {}
    for item in queue:
        counts[item["action"]] = counts.get(item["action"], 0) + 1
    return {
        "dirtyWorkspaces": len(queue),
        "actionable": sum(item["action"] not in {"recent_dirty"} for item in queue),
        "counts": dict(sorted(counts.items())),
        "queue": sorted(queue, key=lambda item: (item["action"], -(item["ageHours"] or -1), str(item["workspaceId"]))),
        "policy": {
            "checkpointAfterHours": checkpoint_after_hours,
            "reviewAfterHours": review_after_hours,
            "quarantineReviewAfterHours": quarantine_review_after_hours,
            "automaticDeletionAllowed": False,
        },
    }
