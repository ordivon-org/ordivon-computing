from __future__ import annotations

import argparse
import importlib.util
import itertools
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
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


sem = load("aic_sem_s5b", ROOT / "aic_semantic_falsify.py")
s2 = load("aic_s2_s5b", ROOT / "aic_s2_cases.py")
s5a = load("aic_s5a_for_s5b", ROOT / "aic_s5a_future_sufficiency.py")


def unique_permutations(events: list[dict[str, Any]]):
    seen = set()
    out = []
    for p in itertools.permutations(events):
        key = sem.canonical(list(p))
        if key not in seen:
            seen.add(key)
            out.append(list(p))
    return out


def oracle_signature(state) -> dict[str, Any]:
    return s2.expected(state)


def dimension_signature(state) -> dict[str, Any]:
    f = s5a.frontier_core(state)
    return {
        "authority": {
            "officeHolder": f["authority"]["officeHolder"],
            "standing": f["authority"]["authorityStanding"],
            "consequence": f["authority"]["consequentialAuthorityStatus"],
        },
        "control": f["authority"]["effectiveController"],
        "root": f["root"],
        "norm": f["norm"],
        "remedy": f["remedy"],
        "history": f["historicalValidity"],
        "lineage": f["lineage"],
    }


def analyze_partial(base: list[dict[str, Any]], batch: list[dict[str, Any]]) -> dict[str, Any]:
    executions = []
    frontier_map: dict[str, dict[str, Any]] = {}
    kernel_map: dict[str, dict[str, Any]] = {}
    oracle_map: dict[str, dict[str, Any]] = {}
    dimension_values: dict[str, set[str]] = {k: set() for k in ["authority", "control", "root", "norm", "remedy", "history", "lineage"]}

    for order in unique_permutations(batch):
        state = sem.replay(base + order)
        fc = s5a.frontier_core(state)
        kc = s5a.continuation_kernel(state)
        oc = oracle_signature(state)
        ds = dimension_signature(state)
        fk, kk, ok = sem.canonical(fc), sem.canonical(kc), sem.canonical(oc)
        frontier_map[fk] = fc
        kernel_map[kk] = kc
        oracle_map[ok] = oc
        for dim, value in ds.items():
            dimension_values[dim].add(sem.canonical(value))
        executions.append({"order": order, "frontierCore": fc, "oracle": oc})

    if len(frontier_map) > 1:
        classification = "VISIBLE_BINDING_AMBIGUITY"
    elif len(kernel_map) > 1:
        classification = "LATENT_CONTINUATION_AMBIGUITY"
    else:
        classification = "DETERMINATE"

    statuses = {(x["oracle"]["consequentialAuthorityStatus"], x["oracle"]["officeHolder"], x["oracle"]["effectiveController"]) for x in executions}
    safe = len(statuses) == 1 and next(iter(statuses))[0] == "AUTHORIZED"
    response_sets = {tuple(x["oracle"]["requiredResponses"]) for x in executions}
    action_relevant = len(statuses) > 1 or len(response_sets) > 1
    ambiguous_dimensions = sorted([k for k, vals in dimension_values.items() if len(vals) > 1])

    return {
        "classification": classification,
        "admissibleLinearizations": len(executions),
        "uniqueBindingCores": len(frontier_map),
        "uniqueContinuationKernels": len(kernel_map),
        "uniqueOracles": len(oracle_map),
        "actionRelevantAmbiguity": action_relevant,
        "safeFreshConsequentialAction": "ALLOW" if safe else "HOLD",
        "ambiguousDimensions": ambiguous_dimensions,
        "executions": executions,
    }


def targeted():
    common_invalid = [
        {"type": "steal_control_key", "actor": "B"},
        {"type": "sanction", "actor": "B", "target": "C", "amount": 2, "sanctionId": "S1"},
        {"type": "recover_control", "actor": "A"},
    ]
    valid_sanction = [{"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "S1"}]
    cases = [
        ("C1_DUAL_ELECTION", [], [{"type": "valid_election", "candidate": "B", "votes": 2}, {"type": "valid_election", "candidate": "C", "votes": 2}]),
        ("C2_COMPROMISE_VS_ROTATE", [], [{"type": "compromise_root", "root": "R1"}, {"type": "in_band_root_rotation", "newAnchor": "S5B-ROT"}]),
        ("C3_INVALIDATE_VS_RESTITUTE", valid_sanction, [{"type": "invalidate_sanction", "sanctionId": "S1"}, {"type": "restitute", "target": "C", "amount": 2}]),
        ("C4_SUCCESSION_VS_SANCTION", [], [{"type": "valid_election", "candidate": "B", "votes": 2}, {"type": "sanction", "actor": "A", "target": "C", "amount": 1, "sanctionId": "S1"}]),
        ("C5_CLAIM_VS_CLEAR", [], [{"type": "authority_claim", "claimant": "B", "source": "s5b", "standing": "CURRENT_SUPPORT"}, {"type": "clear_claims"}]),
        ("C6_REFOUND_VS_COMPROMISE", [{"type": "compromise_root", "root": "R1"}, {"type": "compromise_root", "root": "R2"}], [{"type": "external_refoundation", "anchor": "S5B-EXT", "lineage": "I1", "monitor": "C"}, {"type": "compromise_root", "root": "R1"}]),
        ("C7_AMEND_VS_TAMPER", [], [{"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "S5B-C1"}, {"type": "tamper_physical_quota", "quota": 1, "physicalRevision": "S5B-T1"}]),
        ("C8_TRANSFER_VS_THEFT", [], [{"type": "transfer_control", "actor": "B"}, {"type": "steal_control_key", "actor": "C"}]),
        ("C9_DUAL_CLAIMS", [], [{"type": "authority_claim", "claimant": "A", "source": "s5b-a", "standing": "CURRENT_SUPPORT"}, {"type": "authority_claim", "claimant": "B", "source": "s5b-b", "standing": "CURRENT_SUPPORT"}]),
    ]
    return [{"case": name, "base": base, "concurrentBatch": batch, **analyze_partial(base, batch)} for name, base, batch in cases]


def random_event(rng: random.Random):
    return s5a.random_event(rng)


def random_search(seed: int, n: int):
    rng = random.Random(seed)
    counts = {"DETERMINATE": 0, "VISIBLE_BINDING_AMBIGUITY": 0, "LATENT_CONTINUATION_AMBIGUITY": 0}
    action_relevant = 0
    dimension_counts = {k: 0 for k in ["authority", "control", "root", "norm", "remedy", "history", "lineage"]}
    representative: dict[str, Any] = {}
    for i in range(n):
        base = [random_event(rng) for _ in range(rng.randint(0, 5))]
        batch = [random_event(rng) for _ in range(rng.choice([2, 2, 2, 3]))]
        a = analyze_partial(base, batch)
        counts[a["classification"]] += 1
        if a["actionRelevantAmbiguity"]:
            action_relevant += 1
        for d in a["ambiguousDimensions"]:
            dimension_counts[d] += 1
        if a["classification"] not in representative:
            representative[a["classification"]] = {"base": base, "concurrentBatch": batch, "analysis": a}
    return {
        "batches": n,
        "classificationCounts": counts,
        "classificationPct": {k: round(100*v/n, 2) for k, v in counts.items()},
        "actionRelevantAmbiguityCount": action_relevant,
        "actionRelevantAmbiguityPct": round(100*action_relevant/n, 2),
        "ambiguousDimensionCounts": dimension_counts,
        "representative": representative,
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--output", required=True); ap.add_argument("--seed", type=int, default=202608259); ap.add_argument("--batches", type=int, default=50000); args = ap.parse_args()
    t = targeted(); r = random_search(args.seed, args.batches)
    out = {"schemaVersion": 1, "kind": "ordivon.computing.aic-s5b-partial-order-result", "experimentId": "COJC-J3-AIC-PARTIAL-ORDER-S5B-A", "targeted": t, "random": r}
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))

if __name__ == "__main__": main()
