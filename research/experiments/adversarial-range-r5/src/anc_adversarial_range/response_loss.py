from __future__ import annotations

from .model import ResponseState, Scenario, TrialRecord, TrialStatus
from .world import SimulatedWorld

RESPONSE_LOSS_VARIANTS = (
    "blind-retry",
    "layered-retries",
    "provider-idempotency-only",
    "host-unknown-reconcile",
)
SEEDS = tuple(range(8))
EFFECT_ID = "effect:create-simulated-reservation"
RESOURCE_ID = "resource:simulated-reservation-ledger"
ACTOR_ID = "actor:authorized-client"
SOURCE_ID = "source:participant-task"


def run_response_loss_trial(variant: str, seed: int) -> TrialRecord:
    if variant not in RESPONSE_LOSS_VARIANTS:
        raise ValueError(f"unsupported response-loss variant: {variant}")
    world = SimulatedWorld()
    backend_calls = 0
    redispatches = 0
    reconciliation_reads = 0
    response_state = ResponseState.ABSENT
    key = f"idempotency-key:reservation-{seed}"
    payload = {"reservation": seed, "quantity": 1}

    world.commit(
        effect_id=EFFECT_ID,
        resource_id=RESOURCE_ID,
        payload=payload,
        actor_id=ACTOR_ID,
        source_id=SOURCE_ID,
        idempotency_key=key if variant in {"provider-idempotency-only", "host-unknown-reconcile"} else None,
    )
    backend_calls += 1
    response_state = ResponseState.UNKNOWN

    if variant == "blind-retry":
        response_state = ResponseState.FAILED
        redispatches += 1
        world.commit(
            effect_id=EFFECT_ID,
            resource_id=RESOURCE_ID,
            payload=payload,
            actor_id=ACTOR_ID,
            source_id=SOURCE_ID,
        )
        backend_calls += 1
        response_state = ResponseState.SUCCEEDED
    elif variant == "layered-retries":
        response_state = ResponseState.FAILED
        for _layer in ("host", "sdk", "proxy"):
            redispatches += 1
            world.commit(
                effect_id=EFFECT_ID,
                resource_id=RESOURCE_ID,
                payload=payload,
                actor_id=ACTOR_ID,
                source_id=SOURCE_ID,
            )
            backend_calls += 1
        response_state = ResponseState.SUCCEEDED
    elif variant == "provider-idempotency-only":
        redispatches += 1
        world.commit(
            effect_id=EFFECT_ID,
            resource_id=RESOURCE_ID,
            payload=payload,
            actor_id=ACTOR_ID,
            source_id=SOURCE_ID,
            idempotency_key=key,
        )
        backend_calls += 1
        response_state = ResponseState.SUCCEEDED
    else:
        reconciliation_reads += 1
        receipt = world.lookup_idempotency(key)
        response_state = ResponseState.SUCCEEDED if receipt is not None else ResponseState.UNKNOWN

    effect_count = world.count_effect(EFFECT_ID)
    duplicate_count = max(0, effect_count - 1)
    hard_failures: list[str] = []
    if duplicate_count:
        hard_failures.append("duplicate-world-effect")
    if variant in {"blind-retry", "layered-retries"}:
        hard_failures.append("unknown-misclassified-as-failure")
    if redispatches and variant not in {"provider-idempotency-only"}:
        hard_failures.append("unsafe-redispatch")
    if response_state is not ResponseState.SUCCEEDED:
        hard_failures.append("terminal-state-not-recovered")
    status = TrialStatus.PASSED if not hard_failures else TrialStatus.FAILED
    attack_residuals = tuple(f"duplicate-effect:{index}" for index in range(duplicate_count))
    reset = world.reset()
    if not bool(reset["resetVerified"]):
        hard_failures.append("reset-failed")
        status = TrialStatus.INVALID

    return TrialRecord(
        trial_id=f"trial:response-loss-{variant}-{seed:02d}",
        scenario=Scenario.RESPONSE_LOSS,
        variant=variant,
        seed=seed,
        status=status,
        accepted_outcome=status is TrialStatus.PASSED,
        hard_failures=tuple(sorted(set(hard_failures))),
        residuals=attack_residuals,
        observations={
            "responseLostAfterCommit": True,
            "responseState": response_state.value,
            "effectCount": effect_count,
            "duplicateEffectCount": duplicate_count,
            "redispatches": redispatches,
            "reconciliationReads": reconciliation_reads,
            "stableEffectIdentity": True,
            "providerIdempotencyKey": key if variant in {"provider-idempotency-only", "host-unknown-reconcile"} else None,
            "reset": reset,
        },
        costs={
            "backendCalls": backend_calls,
            "reconciliationReads": reconciliation_reads,
            "retryLayers": 3 if variant == "layered-retries" else int(redispatches > 0),
        },
    )


def run_response_loss_matrix() -> list[TrialRecord]:
    return [
        run_response_loss_trial(variant, seed)
        for variant in RESPONSE_LOSS_VARIANTS
        for seed in SEEDS
    ]
