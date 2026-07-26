from __future__ import annotations

from pathlib import Path
from typing import Any

from anc_semantic_core.bootstrap import issue_authority_views
from anc_semantic_core.conformance import sample_effect, sid
from anc_semantic_core.identity import IdKind
from anc_semantic_core.journal import JournalReducer
from anc_semantic_core.reducer import ReferenceReducer
from anc_semantic_core.testing import test_authority_policy


def open_reducer(kind: str, namespace: str, path: Path | None = None) -> tuple[Any, Any]:
    policy = test_authority_policy()
    if kind == "memory":
        reducer = ReferenceReducer(policy)
    elif kind == "journal":
        if path is None:
            raise ValueError("journal benchmark requires a path")
        reducer = JournalReducer(path, policy)
    else:
        raise ValueError(f"unsupported benchmark reducer: {kind}")
    return reducer, issue_authority_views(reducer, policy, namespace=namespace)


def admit_and_prepare(views: Any, index: int, *, prefix: str) -> None:
    name = f"{prefix}-{index}"
    spec = sample_effect(name)
    views.effects.admit_effect(
        spec,
        event_id=sid(IdKind.EVENT, f"event:{name}:0"),
        recorded_at_ms=index * 2 + 1,
    )
    views.effects.prepare_effect(
        spec.effect_id,
        expected_revision=0,
        event_id=sid(IdKind.EVENT, f"event:{name}:1"),
        recorded_at_ms=index * 2 + 2,
    )
