from __future__ import annotations

from dataclasses import dataclass

from .model import Scenario, TrialRecord, TrialStatus
from .world import SimulatedWorld

DIFFERENTIAL_VARIANTS = (
    "front-first-back-last",
    "shared-last-policy",
    "strict-reject-duplicates",
    "typed-reserialize",
)
SEEDS = tuple(range(12))


@dataclass(frozen=True, slots=True)
class AbstractRequest:
    request_id: str
    target_values: tuple[str, ...]

    @property
    def is_ambiguous(self) -> bool:
        return len(self.target_values) != 1


def _request_for_seed(seed: int) -> AbstractRequest:
    if seed % 2 == 0:
        return AbstractRequest(f"request:clean-{seed}", ("public",))
    return AbstractRequest(f"request:ambiguous-{seed}", ("public", "private"))


def run_differential_trial(variant: str, seed: int) -> TrialRecord:
    if variant not in DIFFERENTIAL_VARIANTS:
        raise ValueError(f"unsupported differential variant: {variant}")
    world = SimulatedWorld()
    request = _request_for_seed(seed)
    front_target: str | None = None
    backend_target: str | None = None
    policy_allowed = False
    rejected_ambiguity = False
    canonicalized = False

    if variant == "front-first-back-last":
        front_target = request.target_values[0]
        policy_allowed = front_target == "public"
        backend_target = request.target_values[-1]
    elif variant == "shared-last-policy":
        front_target = request.target_values[-1]
        backend_target = request.target_values[-1]
        policy_allowed = front_target == "public"
    elif variant == "strict-reject-duplicates":
        if request.is_ambiguous:
            rejected_ambiguity = True
        else:
            front_target = request.target_values[0]
            backend_target = front_target
            policy_allowed = front_target == "public"
    else:
        front_target = request.target_values[0]
        policy_allowed = front_target == "public"
        backend_target = front_target
        canonicalized = True

    if policy_allowed and backend_target is not None:
        effect_id = (
            "effect:read-public-simulated"
            if backend_target == "public"
            else "effect:read-private-simulated"
        )
        resource_id = (
            "resource:public-simulated"
            if backend_target == "public"
            else "resource:private-simulated"
        )
        world.commit(
            effect_id=effect_id,
            resource_id=resource_id,
            payload={"requestId": request.request_id, "target": backend_target},
            actor_id="actor:proxy-chain",
            source_id="source:owned-differential-corpus",
        )

    public_count = world.count_effect("effect:read-public-simulated")
    private_count = world.count_effect("effect:read-private-simulated")
    interpretation_differential = front_target != backend_target and backend_target is not None
    hard_failures: list[str] = []
    if private_count:
        hard_failures.append("unauthorized-private-effect")
    if interpretation_differential and policy_allowed:
        hard_failures.append("policy-executor-differential")
    if not request.is_ambiguous and public_count != 1:
        hard_failures.append("clean-request-utility-lost")
    status = TrialStatus.PASSED if not hard_failures else TrialStatus.FAILED
    residuals = ("unauthorized-private-effect",) if private_count else ()
    reset = world.reset()
    if not bool(reset["resetVerified"]):
        hard_failures.append("reset-failed")
        status = TrialStatus.INVALID

    return TrialRecord(
        trial_id=f"trial:differential-{variant}-{seed:02d}",
        scenario=Scenario.INTERPRETATION_DIFFERENTIAL,
        variant=variant,
        seed=seed,
        status=status,
        accepted_outcome=status is TrialStatus.PASSED,
        hard_failures=tuple(sorted(set(hard_failures))),
        residuals=residuals,
        observations={
            "requestId": request.request_id,
            "inputClass": "ambiguous" if request.is_ambiguous else "clean",
            "targetValueCount": len(request.target_values),
            "frontTarget": front_target,
            "backendTarget": backend_target,
            "policyAllowed": policy_allowed,
            "rejectedAmbiguity": rejected_ambiguity,
            "typedReserialization": canonicalized,
            "interpretationDifferential": interpretation_differential,
            "publicEffects": public_count,
            "privateEffects": private_count,
            "rawOperationalPayloadAbsent": True,
            "reset": reset,
        },
        costs={
            "parserCount": 2,
            "policyChecks": 1,
            "worldCommits": public_count + private_count,
        },
    )


def run_differential_matrix() -> list[TrialRecord]:
    return [
        run_differential_trial(variant, seed)
        for variant in DIFFERENTIAL_VARIANTS
        for seed in SEEDS
    ]
