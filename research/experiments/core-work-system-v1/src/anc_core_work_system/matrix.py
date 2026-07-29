from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .attention_eval import run_attention_matrix
from .context_eval import run_context_matrix
from .continuity import run_continuity_matrix
from .effect_eval import run_effect_matrix
from .model import JsonValue, TrialRecord, canonical_bytes, canonical_digest


def _summary(records: Iterable[TrialRecord]) -> dict[str, JsonValue]:
    items = list(records)
    packages: dict[str, dict[str, JsonValue]] = {}
    for record in items:
        package = record.spec.work_package
        current = packages.setdefault(
            package,
            {"trials": 0, "passed": 0, "failed": 0, "variants": [], "hardFailures": []},
        )
        current["trials"] = int(current["trials"]) + 1
        current["passed"] = int(current["passed"]) + int(record.accepted_outcome)
        current["failed"] = int(current["failed"]) + int(not record.accepted_outcome)
        variants = current["variants"]
        failures = current["hardFailures"]
        assert isinstance(variants, list) and isinstance(failures, list)
        variants.append(record.spec.variant)
        failures.extend(record.hard_failures)
    return {
        "trialCount": len(items),
        "passed": sum(int(item.accepted_outcome) for item in items),
        "failed": sum(int(not item.accepted_outcome) for item in items),
        "packages": packages,
        "crossBackendEffectPromotionBlocked": True,
    }


def run_deterministic_matrix(
    fixture: str | Path,
    *,
    working_root: str | Path,
    temporal_cache: str | Path,
) -> dict[str, JsonValue]:
    root = Path(working_root)
    root.mkdir(parents=True, exist_ok=True)
    records: list[TrialRecord] = []
    records.extend(
        run_continuity_matrix(
            fixture,
            working_root=root / "continuity",
            temporal_cache=temporal_cache,
        )
    )
    records.extend(run_context_matrix(fixture, working_root=root / "context"))
    records.extend(run_effect_matrix(fixture, working_root=root / "effect"))
    records.extend(run_attention_matrix(fixture, working_root=root / "attention"))
    payload: dict[str, JsonValue] = {
        "schemaVersion": 1,
        "kind": "anc.core-work-system-deterministic-matrix",
        "summary": _summary(records),
        "trials": [record.to_dict() for record in records],
    }
    payload["matrixDigest"] = canonical_digest(payload)
    return payload


def write_matrix(path: str | Path, value: dict[str, JsonValue]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_bytes(value) + b"\n")
