from __future__ import annotations

from typing import Any


def assess_shared_lifecycle_promotion(consumers: list[dict[str, Any]]) -> dict[str, Any]:
    exact = [
        item
        for item in consumers
        if item.get("materiallyDifferent") is True
        and item.get("requiresExactSharedVocabulary") is True
        and item.get("deletionFailure")
    ]
    owner_ids = sorted({str(item.get("owner")) for item in exact})
    earned = len(owner_ids) >= 2
    return {
        "consumerEvidence": consumers,
        "exactConsumers": owner_ids,
        "materiallyDifferentExactConsumers": len(owner_ids),
        "productionSharedPackageEarned": earned,
        "decision": "promote_smallest_shared_contract" if earned else "keep_experiment_local",
        "newRepositoryEarned": False,
        "reason": (
            "at least two materially different owners require the exact lifecycle semantics"
            if earned
            else "only one materially different owner currently requires the exact shared lifecycle vocabulary"
        ),
    }
