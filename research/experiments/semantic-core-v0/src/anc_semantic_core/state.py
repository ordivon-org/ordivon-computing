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


class DispatchState(StrEnum):
    STARTED = "started"
    ADMITTED = "admitted"
    UNKNOWN = "unknown"
    REJECTED = "rejected"

    @property
    def terminal(self) -> bool:
        return self is DispatchState.REJECTED


class NextAction(StrEnum):
    PREPARE = "prepare"
    DISPATCH = "dispatch"
    OBSERVE = "observe"
    RECONCILE = "reconcile"
    NONE = "none"


_EFFECT_TRANSITIONS: dict[EffectState, frozenset[EffectState]] = {
    EffectState.PROPOSED: frozenset({EffectState.PREPARED, EffectState.CANCELLED}),
    EffectState.PREPARED: frozenset({EffectState.DISPATCHED, EffectState.CANCELLED}),
    EffectState.DISPATCHED: frozenset(
        {
            EffectState.RUNNING,
            EffectState.CANCEL_REQUESTED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.UNKNOWN,
        }
    ),
    EffectState.RUNNING: frozenset(
        {
            EffectState.CANCEL_REQUESTED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.UNKNOWN,
        }
    ),
    EffectState.CANCEL_REQUESTED: frozenset(
        {
            EffectState.CANCELLED,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.UNKNOWN,
        }
    ),
    EffectState.UNKNOWN: frozenset({EffectState.RECONCILING}),
    EffectState.RECONCILING: frozenset(
        {
            EffectState.RUNNING,
            EffectState.SUCCEEDED,
            EffectState.FAILED,
            EffectState.CANCELLED,
            EffectState.UNKNOWN,
        }
    ),
    EffectState.SUCCEEDED: frozenset(),
    EffectState.FAILED: frozenset(),
    EffectState.CANCELLED: frozenset(),
}


_DISPATCH_TRANSITIONS: dict[DispatchState, frozenset[DispatchState]] = {
    DispatchState.STARTED: frozenset(
        {DispatchState.ADMITTED, DispatchState.UNKNOWN, DispatchState.REJECTED}
    ),
    DispatchState.ADMITTED: frozenset({DispatchState.UNKNOWN}),
    DispatchState.UNKNOWN: frozenset({DispatchState.ADMITTED, DispatchState.REJECTED}),
    DispatchState.REJECTED: frozenset(),
}


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


def can_transition_effect(current: EffectState, target: EffectState) -> bool:
    return target in _EFFECT_TRANSITIONS[current]


def can_transition_dispatch(current: DispatchState, target: DispatchState) -> bool:
    return target in _DISPATCH_TRANSITIONS[current]


# Backward-compatible name for the Effect transition predicate.
can_transition = can_transition_effect
