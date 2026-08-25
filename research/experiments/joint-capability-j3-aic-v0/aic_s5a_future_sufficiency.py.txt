from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


sem = load("aic_sem_s5a", ROOT / "aic_semantic_falsify.py")
s2 = load("aic_s2_s5a", ROOT / "aic_s2_cases.py")


def frontier_core(state) -> dict[str, Any]:
    f = deepcopy(s2.orthogonal_frontier(state))
    f.pop("occurrenceDigest", None)
    f.pop("eventCount", None)
    return f


def current_support_claimants(state) -> list[str]:
    return sorted({c["claimant"] for c in state.authority_claims if c.get("standing") == "CURRENT_SUPPORT"})


def sanction_transition_registry(state) -> list[dict[str, Any]]:
    # Only fields read by future invalidate_sanction semantics or needed to preserve
    # deterministic sanction identity/continuity are retained here.
    return sorted([
        {
            "id": s["id"],
            "target": s["target"],
            "amount": s["amount"],
            "executed": s["executed"],
            "currentStatus": s["currentStatus"],
        }
        for s in state.sanctions
    ], key=lambda x: x["id"])


def continuation_kernel(state) -> dict[str, Any]:
    return {
        "validMonitor": state.valid_monitor,
        "effectiveController": state.effective_controller,
        "normativeQuota": state.normative_quota,
        "physicalQuota": state.physical_quota,
        "institutionLineage": state.institution_lineage,
        "identityRelation": state.identity_relation,
        "compromisedRoots": sorted(state.compromised_roots),
        "activeAnchor": state.active_anchor,
        "currentSupportClaimants": current_support_claimants(state),
        "remedyDue": dict(sorted(state.remedy_due.items())),
        "sanctions": sanction_transition_registry(state),
    }


def institutional_observables(state) -> dict[str, Any]:
    return {
        "frontierCore": frontier_core(state),
        "oracle": s2.expected(state),
    }


def replay_suffix(history: list[dict[str, Any]], suffix: list[dict[str, Any]]):
    return sem.replay(history + suffix)


def divergence(left: list[dict[str, Any]], right: list[dict[str, Any]], suffix: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    ls = replay_suffix(left, suffix)
    rs = replay_suffix(right, suffix)
    lo, ro = institutional_observables(ls), institutional_observables(rs)
    return lo != ro, {"leftFinal": lo, "rightFinal": ro}


def shrink(left, right, suffix, abstraction):
    def pre_ok(l, r):
        ls, rs = sem.replay(l), sem.replay(r)
        return abstraction(ls) == abstraction(rs) and sem.canonical(l) != sem.canonical(r)

    def fails(l, r, f):
        if not pre_ok(l, r):
            return False
        return divergence(l, r, f)[0]

    l, r, f = deepcopy(left), deepcopy(right), deepcopy(suffix)
    changed = True
    while changed:
        changed = False
        for target_name in ("l", "r", "f"):
            arr = {"l": l, "r": r, "f": f}[target_name]
            for i in range(len(arr)):
                cand = arr[:i] + arr[i+1:]
                nl, nr, nf = (cand, r, f) if target_name == "l" else ((l, cand, f) if target_name == "r" else (l, r, cand))
                if fails(nl, nr, nf):
                    l, r, f = nl, nr, nf
                    changed = True
                    break
            if changed:
                break
    detail = divergence(l, r, f)[1]
    return {"left": l, "right": r, "futureSuffix": f, **detail}


def targeted_cases() -> list[dict[str, Any]]:
    cases = []

    # T1: Frontier only exposes DEGRADED, not which root is already compromised.
    l = [{"type": "compromise_root", "root": "R1"}]
    r = [{"type": "compromise_root", "root": "R2"}]
    f = [{"type": "compromise_root", "root": "R1"}]
    cases.append(("T1_HIDDEN_COMPROMISED_ROOT_IDENTITY", l, r, f, True))

    # T2: A single current-support claimant is not shown while standing remains CURRENT.
    l = [{"type": "authority_claim", "claimant": "A", "source": "t2-a", "standing": "CURRENT_SUPPORT"}]
    r = []
    f = [{"type": "authority_claim", "claimant": "B", "source": "t2-b", "standing": "CURRENT_SUPPORT"}]
    cases.append(("T2_HIDDEN_SINGLE_AUTHORITY_CLAIM", l, r, f, True))

    # T3: Same brute resources/frontier/history-invalidity, but different live valid sanction IDs.
    common = [
        {"type": "steal_control_key", "actor": "B"},
        {"type": "sanction", "actor": "B", "target": "C", "amount": 1, "sanctionId": "S0"},
        {"type": "recover_control", "actor": "A"},
        {"type": "restitute", "target": "C", "amount": 1},
    ]
    l = common + [{"type": "sanction", "actor": "A", "target": "C", "amount": 1, "sanctionId": "S1"}]
    r = common + [{"type": "sanction", "actor": "A", "target": "C", "amount": 1, "sanctionId": "S2"}]
    f = [{"type": "invalidate_sanction", "sanctionId": "S1"}]
    cases.append(("T3_HIDDEN_SANCTION_REGISTRY", l, r, f, True))

    out = []
    for name, left, right, suffix, expected_frontier_failure in cases:
        ls, rs = sem.replay(left), sem.replay(right)
        same_frontier = frontier_core(ls) == frontier_core(rs)
        same_resources = ls.resources == rs.resources
        div, detail = divergence(left, right, suffix)
        same_kernel = continuation_kernel(ls) == continuation_kernel(rs)
        out.append({
            "case": name,
            "sameFrontierBefore": same_frontier,
            "sameBruteResourcesBefore": same_resources,
            "sameContinuationKernelBefore": same_kernel,
            "divergesAfterCommonFuture": div,
            "expectedFrontierFailure": expected_frontier_failure,
            "counterexample": shrink(left, right, suffix, frontier_core) if same_frontier and div else None,
            **detail,
        })
    return out


ACTORS = ["A", "B", "C"]
ROOTS = ["R1", "R2", "R3"]
SANCTION_IDS = ["S0", "S1", "S2"]


def random_event(rng: random.Random) -> dict[str, Any]:
    kind = rng.randrange(15)
    if kind == 0:
        return {"type": "valid_election", "candidate": rng.choice(ACTORS), "votes": rng.choice([1, 2, 3])}
    if kind == 1:
        return {"type": "invalid_election", "candidate": rng.choice(ACTORS), "votes": rng.choice([0, 1])}
    if kind == 2:
        return {"type": "transfer_control", "actor": rng.choice(ACTORS)}
    if kind == 3:
        return {"type": "steal_control_key", "actor": rng.choice(ACTORS)}
    if kind == 4:
        return {"type": "disable_control"}
    if kind == 5:
        return {"type": "recover_control", "actor": rng.choice(ACTORS)}
    if kind == 6:
        return {"type": "valid_amendment", "votes": rng.choice([2, 3]), "quota": rng.choice([1, 2]), "revision": rng.choice(["C1", "C2", "C3"])}
    if kind == 7:
        return {"type": "tamper_physical_quota", "quota": rng.choice([1, 2]), "physicalRevision": rng.choice(["T1", "T2"])}
    if kind == 8:
        return {"type": "sanction", "actor": rng.choice(ACTORS), "target": "C", "amount": rng.choice([1, 2]), "sanctionId": rng.choice(SANCTION_IDS)}
    if kind == 9:
        return {"type": "invalidate_sanction", "sanctionId": rng.choice(SANCTION_IDS)}
    if kind == 10:
        return {"type": "restitute", "target": "C", "amount": rng.choice([1, 2, 3])}
    if kind == 11:
        return {"type": "compromise_root", "root": rng.choice(ROOTS)}
    if kind == 12:
        return {"type": "in_band_root_rotation", "newAnchor": rng.choice(["ROT-A", "ROT-B"])}
    if kind == 13:
        return {"type": "authority_claim", "claimant": rng.choice(ACTORS), "source": rng.choice(["ctx-a", "ctx-b"]), "standing": "CURRENT_SUPPORT"}
    return {"type": "clear_claims"}


def generate_history(rng, max_len):
    return [random_event(rng) for _ in range(rng.randint(0, max_len))]


def generate_future(rng, max_len):
    return [random_event(rng) for _ in range(rng.randint(1, max_len))]


def random_search(seed: int, history_count: int, future_checks: int, max_history_len: int, max_future_len: int):
    rng = random.Random(seed)
    histories = [generate_history(rng, max_history_len) for _ in range(history_count)]
    frontier_buckets: dict[str, list[list[dict[str, Any]]]] = {}
    kernel_buckets: dict[str, list[list[dict[str, Any]]]] = {}
    for h in histories:
        st = sem.replay(h)
        frontier_buckets.setdefault(sem.canonical(frontier_core(st)), []).append(h)
        kernel_buckets.setdefault(sem.canonical(continuation_kernel(st)), []).append(h)

    frontier_pairs = [bucket for bucket in frontier_buckets.values() if len(bucket) >= 2]
    kernel_pairs = [bucket for bucket in kernel_buckets.values() if len(bucket) >= 2]
    first_frontier_failure = None
    first_kernel_failure = None
    frontier_tested = 0
    kernel_tested = 0

    for i in range(future_checks):
        suffix = generate_future(rng, max_future_len)
        if frontier_pairs:
            bucket = rng.choice(frontier_pairs)
            left, right = rng.sample(bucket, 2)
            if sem.canonical(left) != sem.canonical(right):
                frontier_tested += 1
                if first_frontier_failure is None and divergence(left, right, suffix)[0]:
                    first_frontier_failure = shrink(left, right, suffix, frontier_core)
        if kernel_pairs:
            bucket = rng.choice(kernel_pairs)
            left, right = rng.sample(bucket, 2)
            if sem.canonical(left) != sem.canonical(right):
                kernel_tested += 1
                if first_kernel_failure is None and divergence(left, right, suffix)[0]:
                    first_kernel_failure = shrink(left, right, suffix, continuation_kernel)
        if first_frontier_failure is not None and first_kernel_failure is not None:
            break

    return {
        "historiesGenerated": len(histories),
        "frontierEquivalenceClassesWithCollisions": len(frontier_pairs),
        "kernelEquivalenceClassesWithCollisions": len(kernel_pairs),
        "frontierFuturePairsTested": frontier_tested,
        "kernelFuturePairsTested": kernel_tested,
        "frontierCounterexample": first_frontier_failure,
        "kernelCounterexample": first_kernel_failure,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=202608258)
    ap.add_argument("--histories", type=int, default=120000)
    ap.add_argument("--future-checks", type=int, default=150000)
    ap.add_argument("--max-history-len", type=int, default=8)
    ap.add_argument("--max-future-len", type=int, default=3)
    args = ap.parse_args()

    targeted = targeted_cases()
    random_result = random_search(args.seed, args.histories, args.future_checks, args.max_history_len, args.max_future_len)
    frontier_targeted_failures = [x for x in targeted if x["sameFrontierBefore"] and x["divergesAfterCommonFuture"]]
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s5a-future-sufficiency-result",
        "experimentId": "COJC-J3-AIC-FUTURE-SUFFICIENCY-S5A",
        "seed": args.seed,
        "targeted": targeted,
        "random": random_result,
        "registeredDispositions": [
            "FRONTIER_IS_CURRENT_SUMMARY_NOT_STATE" if frontier_targeted_failures or random_result["frontierCounterexample"] else "FRONTIER_IS_TRANSITION_SUFFICIENT_CANDIDATE",
            "CONTINUATION_KERNEL_SURVIVES_GENERATIVE_TEST" if random_result["kernelCounterexample"] is None else "CONTINUATION_KERNEL_COUNTEREXAMPLE_FOUND",
            "LATENT_OWNER_STATE_NEEDED" if frontier_targeted_failures else "NO_TARGETED_LATENT_OWNER_STATE_EVIDENCE",
        ],
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
