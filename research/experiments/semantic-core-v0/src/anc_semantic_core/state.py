from __future__ import annotations

from enum import StrEnum


class EffectState(StrEnum):
    PROPOSED = "proposed"
    PREPARED = "prepared"
    DISPATCHED = "dispatched"
    RUNNING = "running"
    CANCEL_REQUESTED = "cancel_requested"
    UNKNOWN = "unknown"
    RECONCILING = "reconciling"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @property
    def terminal(self) -> bool:
        return self in {
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.CANCELLED,
        }

    @property
    def safe_to_dispatch(self) -> bool:
        return self is EffectState.PREPARED

    @property
    def requires_reconciliation(self) -> bool:
        return self in {EffectState.UNKNOWN, EffectState.RECONCILING}


class NextAction(StrEnum):
    PREPARE = "prepare"
    DISPATCH = "dispatch"
    OBSERVE = "observe"
    RECONCILE = "reconcile"
    NONE = "none"


def next_action(state: EffectState) -> NextAction:
    if state is EffectState.PROPOSED:
        return NextAction.PREPARE
    if state is EffectState.PREPARED:
        return NextAction.DISPATCH
    if state in {
        EffectState.DISPATCHED,
        EffectState.RUNNING,
        EffectState.CANCEL_REQUESTED,
    }:
        return NextAction.OBSERVE
    if state in {EffectState.UNKNOWN, EffectState.RECONCILING}:
        return NextAction.RECONCILE
    return NextAction.NONE


def can_transition(current: EffectState, target: EffectState) -> bool:
    allowed: dict[EffectState, set[EffectState]] = {
        EffectState.PROPOSED: {
            EffectState.PREPARED,
            EffectState.CANCELLED,
        },
        EffectState.PREPARED: {
            EffectState.DISPATCHED,
            EffectState.CANCELLED,
        },
        EffectState.DISPATCHED: {
            EffectState.RUNNING,
            EffectState.CANCEL_REQUESTED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.UNKNOWN,
        },
        EffectState.RUNNING: {
            EffectState.CANCEL_REQUESTED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.UNKNOWN,
        },
        EffectState.CANCEL_REQUESTED: {
            EffectState.CANCELLED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.UNKNOWN,
        },
        EffectState.UNKNOWN: {EffectState.RECONCILING},
        EffectState.RECONCILING: {
            EffectState.RUNNING,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.CANCELLED,
            EffectState.UNKNOWN,
        },
        EffectState.SUCCEEDED: set(),
        EffectState.FAILED: set(),
        EffectState.CANCELLED: set(),
    }
    return target in allowed[current]
