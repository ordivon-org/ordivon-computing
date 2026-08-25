from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


sem = load("aic_sem_s4", ROOT / "aic_semantic_falsify.py")
s2 = load("aic_s2_s4", ROOT / "aic_s2_cases.py")


def core(state) -> dict[str, Any]:
    f = deepcopy(s2.orthogonal_frontier(state))
    f.pop("occurrenceDigest", None)
    f.pop("eventCount", None)
    return f


def same_core(left_events: list[dict[str, Any]], right_events: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    ls, rs = sem.replay(left_events), sem.replay(right_events)
    lc, rc = core(ls), core(rs)
    return lc == rc, {"leftCore": lc, "rightCore": rc}


def random_base(rng: random.Random) -> list[dict[str, Any]]:
    return [rng.choice(sem.RANDOM_EVENTS)(rng) for _ in range(rng.randint(0, 8))]


def shrink_base(base: list[dict[str, Any]], still_fails: Callable[[list[dict[str, Any]]], bool]) -> list[dict[str, Any]]:
    current = deepcopy(base)
    changed = True
    while changed and current:
        changed = False
        for i in range(len(current)):
            candidate = current[:i] + current[i+1:]
            try:
                failed = still_fails(candidate)
            except Exception:
                failed = False
            if failed:
                current = candidate
                changed = True
                break
    return current


def relation_result(label: str, ok: bool, *, checked: int, counterexample: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"relation": label, "ok": ok, "checked": checked, "counterexample": counterexample}


def mr1(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    left = base
    right = base + [{"type": "invalid_election", "candidate": "C", "votes": 1}]
    return same_core(left, right)


def mr2(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]] | None:
    st = sem.replay(base)
    if st.effective_controller is None:
        return None
    left = base
    right = base + [{"type": "recover_control", "actor": st.effective_controller}]
    return same_core(left, right)


def mr3(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]] | None:
    st = sem.replay(base)
    if not st.compromised_roots:
        return None
    root = sorted(st.compromised_roots)[0]
    return same_core(base, base + [{"type": "compromise_root", "root": root}])


def mr4(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    a = base + [{"type": "compromise_root", "root": "R1"}, {"type": "compromise_root", "root": "R2"}]
    b = base + [{"type": "compromise_root", "root": "R2"}, {"type": "compromise_root", "root": "R1"}]
    return same_core(a, b)


def mr5(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    a = base + [
        {"type": "authority_claim", "claimant": "A", "source": "mr5-a", "standing": "CURRENT_SUPPORT"},
        {"type": "authority_claim", "claimant": "B", "source": "mr5-b", "standing": "CURRENT_SUPPORT"},
    ]
    b = base + [
        {"type": "authority_claim", "claimant": "B", "source": "mr5-b", "standing": "CURRENT_SUPPORT"},
        {"type": "authority_claim", "claimant": "A", "source": "mr5-a", "standing": "CURRENT_SUPPORT"},
    ]
    return same_core(a, b)


def mr6(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]] | None:
    # `clear_claims` is an institution-wide resolver in this apparatus. A transient
    # contest round-trip is semantics-preserving only when it does not erase an
    # already-live claim set from the base trajectory.
    st = sem.replay(base)
    if st.authority_claims:
        return None
    transient = [
        {"type": "authority_claim", "claimant": "A", "source": "mr6-a", "standing": "CURRENT_SUPPORT"},
        {"type": "authority_claim", "claimant": "B", "source": "mr6-b", "standing": "CURRENT_SUPPORT"},
        {"type": "clear_claims"},
    ]
    return same_core(base, base + transient)


def mr11(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]] | None:
    st = sem.replay(base)
    if st.binding_status != "CURRENT" or st.anchor_status == "THRESHOLD_COMPROMISED":
        return None
    a = base + [{"type": "valid_election", "candidate": "B", "votes": 2}, {"type": "transfer_control", "actor": "B"}]
    b = base + [{"type": "transfer_control", "actor": "B"}, {"type": "valid_election", "candidate": "B", "votes": 2}]
    return same_core(a, b)


def mr12(base: list[dict[str, Any]]) -> tuple[bool, dict[str, Any]]:
    st = sem.replay(base)
    event = {"type": "tamper_physical_quota", "quota": st.physical_quota, "physicalRevision": "MR12-NOOP"}
    return same_core(base, base + [event])


RANDOM_RELATIONS: list[tuple[str, Callable[[list[dict[str, Any]]], tuple[bool, dict[str, Any]] | None]]] = [
    ("MR1_INVALID_ELECTION_INSERTION", mr1),
    ("MR2_REDUNDANT_RECOVERY", mr2),
    ("MR3_REDUNDANT_ROOT_COMPROMISE", mr3),
    ("MR4_ROOT_COMPROMISE_ORDER", mr4),
    ("MR5_CLAIM_ORDER", mr5),
    ("MR6_TRANSIENT_CONTEST_CLEAR", mr6),
    ("MR11_ELECTION_TRANSFER_COMMUTE", mr11),
    ("MR12_NOOP_PHYSICAL_TAMPER", mr12),
]


def run_random_relations(seed: int, trials: int) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    first_failure: dict[str, tuple[list[dict[str, Any]], dict[str, Any]]] = {}
    checked = {name: 0 for name, _ in RANDOM_RELATIONS}
    for _ in range(trials):
        base = random_base(rng)
        for name, fn in RANDOM_RELATIONS:
            try:
                result = fn(base)
            except Exception as error:
                if name not in first_failure:
                    first_failure[name] = (deepcopy(base), {"exception": type(error).__name__, "message": str(error)})
                continue
            if result is None:
                continue
            checked[name] += 1
            ok, detail = result
            if not ok and name not in first_failure:
                first_failure[name] = (deepcopy(base), detail)

    out = []
    for name, fn in RANDOM_RELATIONS:
        if name not in first_failure:
            out.append(relation_result(name, True, checked=checked[name]))
            continue
        base, detail = first_failure[name]
        def still_fails(candidate):
            x = fn(candidate)
            return x is not None and not x[0]
        shrunk = shrink_base(base, still_fails)
        result = fn(shrunk)
        shrunk_detail = result[1] if result is not None else detail
        out.append(relation_result(name, False, checked=checked[name], counterexample={"base": shrunk, **shrunk_detail}))
    return out


def fixed_relations() -> list[dict[str, Any]]:
    results = []

    # MR7: failed in-band resurrection is absorbed by later independent refoundation.
    base = [
        {"type": "compromise_root", "root": "R1"},
        {"type": "compromise_root", "root": "R2"},
    ]
    left = base + [
        {"type": "in_band_root_rotation", "newAnchor": "FAILED-MR7"},
        {"type": "external_refoundation", "anchor": "MR7-EXT", "lineage": "I1", "monitor": "C"},
        {"type": "transfer_control", "actor": "C"},
    ]
    right = base + [
        {"type": "external_refoundation", "anchor": "MR7-EXT", "lineage": "I1", "monitor": "C"},
        {"type": "transfer_control", "actor": "C"},
    ]
    ok, detail = same_core(left, right)
    results.append(relation_result("MR7_FAILED_INBAND_BEFORE_REFOUNDATION", ok, checked=1, counterexample=None if ok else {"left": left, "right": right, **detail}))

    # MR8: equivalent restitution partition.
    failures = []
    for amount in range(1, 5):
        prefix = [
            {"type": "steal_control_key", "actor": "B"},
            {"type": "sanction", "actor": "B", "target": "C", "amount": amount, "sanctionId": f"MR8-S{amount}"},
            {"type": "recover_control", "actor": "A"},
        ]
        one = prefix + [{"type": "restitute", "target": "C", "amount": amount}]
        parts = prefix + [{"type": "restitute", "target": "C", "amount": 1} for _ in range(amount)]
        ok, detail = same_core(one, parts)
        s1, s2s = sem.replay(one), sem.replay(parts)
        ok = ok and s1.resources == s2s.resources and s1.remedy_due == s2s.remedy_due
        if not ok:
            failures.append({"amount": amount, "one": one, "parts": parts, **detail})
    results.append(relation_result("MR8_RESTITUTION_PARTITION", not failures, checked=4, counterexample=failures[0] if failures else None))

    # MR9: repeated invalidation should be idempotent including historical invalidity classification.
    once = [
        {"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "MR9-S1"},
        {"type": "invalidate_sanction", "sanctionId": "MR9-S1"},
    ]
    twice = once + [{"type": "invalidate_sanction", "sanctionId": "MR9-S1"}]
    a, b = sem.replay(once), sem.replay(twice)
    core_ok = core(a) == core(b)
    class_ok = a.sanctions[0]["currentStatus"] == b.sanctions[0]["currentStatus"]
    remedy_ok = a.remedy_due == b.remedy_due
    mr9_ok = core_ok and class_ok and remedy_ok
    results.append(relation_result("MR9_REPEAT_INVALIDATION_IDEMPOTENT", mr9_ok, checked=1, counterexample=None if mr9_ok else {
        "once": once,
        "twice": twice,
        "onceStatus": a.sanctions[0]["currentStatus"],
        "twiceStatus": b.sanctions[0]["currentStatus"],
        "onceRemedy": a.remedy_due,
        "twiceRemedy": b.remedy_due,
        "coreEqual": core_ok,
    }))

    # MR10: restitution after remedy is zero is a current no-op.
    prefix = [
        {"type": "steal_control_key", "actor": "B"},
        {"type": "sanction", "actor": "B", "target": "C", "amount": 2, "sanctionId": "MR10-S1"},
        {"type": "recover_control", "actor": "A"},
        {"type": "restitute", "target": "C", "amount": 2},
    ]
    extra = prefix + [{"type": "restitute", "target": "C", "amount": 99}]
    ok, detail = same_core(prefix, extra)
    a, b = sem.replay(prefix), sem.replay(extra)
    ok = ok and a.resources == b.resources and a.remedy_due == b.remedy_due
    results.append(relation_result("MR10_EXTRA_RESTITUTION_AFTER_ZERO", ok, checked=1, counterexample=None if ok else {"left": prefix, "right": extra, **detail}))
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=202608256)
    ap.add_argument("--trials", type=int, default=100000)
    args = ap.parse_args()

    random_results = run_random_relations(args.seed, args.trials)
    fixed = fixed_relations()
    relations = random_results + fixed
    failures = [r for r in relations if not r["ok"]]
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s4a-metamorphic-result",
        "experimentId": "COJC-J3-AIC-METAMORPHIC-S4",
        "seed": args.seed,
        "randomBaseTrials": args.trials,
        "semanticSourceDigest": sem.digest(Path(ROOT / "aic_semantic_falsify.py").read_text()),
        "relations": relations,
        "failureCount": len(failures),
        "mandatoryPass": not failures,
        "interpretation": "A failed relation is a substrate/domain-model counterexample candidate, not an Agent failure. Repair and refreeze semantics before S4B provider testing.",
    }
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if not failures else 2)


if __name__ == "__main__":
    main()
