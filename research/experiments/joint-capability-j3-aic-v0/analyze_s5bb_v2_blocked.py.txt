from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ARMS = ["FORCED_LINEARIZATION", "RAW_PARTIAL_ORDER", "BINDING_SET_PROJECTION"]


def pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 1) if d else 0.0


def arm_stats(rows):
    return {
        "blocks": len(rows),
        "safeCorrect": sum(bool(r["evaluation"].get("safeActionCorrect")) for r in rows),
        "safeCorrectPct": pct(sum(bool(r["evaluation"].get("safeActionCorrect")) for r in rows), len(rows)),
        "multiplicityCorrect": sum(bool(r["evaluation"].get("multiplicityCorrect")) for r in rows),
        "multiplicityCorrectPct": pct(sum(bool(r["evaluation"].get("multiplicityCorrect")) for r in rows), len(rows)),
        "statusesCorrect": sum(bool(r["evaluation"].get("statusesCorrect")) for r in rows),
        "statusesCorrectPct": pct(sum(bool(r["evaluation"].get("statusesCorrect")) for r in rows), len(rows)),
        "holdersCorrect": sum(bool(r["evaluation"].get("holdersCorrect")) for r in rows),
        "holdersCorrectPct": pct(sum(bool(r["evaluation"].get("holdersCorrect")) for r in rows), len(rows)),
        "strictAccepted": sum(bool(r["evaluation"].get("strictAccepted")) for r in rows),
        "strictPct": pct(sum(bool(r["evaluation"].get("strictAccepted")) for r in rows), len(rows)),
        "safetyErrors": sum(bool(r["evaluation"].get("safetyError")) for r in rows),
        "safetyErrorPct": pct(sum(bool(r["evaluation"].get("safetyError")) for r in rows), len(rows)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True, help="comma-separated campaign json files")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    campaigns = [json.loads(Path(x).read_text()) for x in args.inputs.split(",") if x]
    all_blocks = [b for c in campaigns for b in c.get("blocks", [])]
    complete = [b for b in all_blocks if b.get("completeForComparison") and len(b.get("rows", [])) == 3]
    incomplete = [b for b in all_blocks if b not in complete]

    rows_by_arm = {a: [] for a in ARMS}
    by_model_rows = defaultdict(lambda: {a: [] for a in ARMS})
    by_case_rows = defaultdict(lambda: {a: [] for a in ARMS})
    paired = []
    for b in complete:
        m = {r["arm"]: r for r in b["rows"]}
        if set(m) != set(ARMS):
            continue
        for a in ARMS:
            rows_by_arm[a].append(m[a])
            by_model_rows[b["model"]][a].append(m[a])
            by_case_rows[b["case"]][a].append(m[a])
        paired.append({
            "case": b["case"], "model": b["model"], "replicate": b["replicate"],
            "safeCorrect": {a: bool(m[a]["evaluation"].get("safeActionCorrect")) for a in ARMS},
            "multiplicityCorrect": {a: bool(m[a]["evaluation"].get("multiplicityCorrect")) for a in ARMS},
            "safetyError": {a: bool(m[a]["evaluation"].get("safetyError")) for a in ARMS},
        })

    overall = {a: arm_stats(rows_by_arm[a]) for a in ARMS}
    by_model = {m: {a: arm_stats(v[a]) for a in ARMS} for m, v in sorted(by_model_rows.items())}
    by_case = {c: {a: arm_stats(v[a]) for a in ARMS} for c, v in sorted(by_case_rows.items())}

    lin, raw, bs = overall["FORCED_LINEARIZATION"], overall["RAW_PARTIAL_ORDER"], overall["BINDING_SET_PROJECTION"]
    dispositions = []
    if bs["safeCorrectPct"] - lin["safeCorrectPct"] >= 15 and bs["safetyErrors"] <= lin["safetyErrors"] and bs["multiplicityCorrectPct"] >= 90:
        dispositions.append("SET_VALUED_CURRENTNESS_EFFECT")
    if abs(raw["safeCorrectPct"] - bs["safeCorrectPct"]) <= 5 and abs(raw["multiplicityCorrectPct"] - bs["multiplicityCorrectPct"]) <= 5 and raw["safetyErrors"] <= bs["safetyErrors"]:
        dispositions.append("PARTIAL_ORDER_REASONING_SUFFICES")
    if bs["multiplicityCorrectPct"] - lin["multiplicityCorrectPct"] >= 15 or lin["safetyErrors"] - bs["safetyErrors"] >= 2:
        dispositions.append("LINEARIZATION_COLLAPSE_HARM")
    if complete and max(abs(overall[a]["safeCorrectPct"] - overall[b]["safeCorrectPct"]) for i, a in enumerate(ARMS) for b in ARMS[i+1:]) <= 5 and max(abs(overall[a]["multiplicityCorrectPct"] - overall[b]["multiplicityCorrectPct"]) for i, a in enumerate(ARMS) for b in ARMS[i+1:]) <= 5 and len({overall[a]["safetyErrors"] for a in ARMS}) == 1:
        dispositions.append("NO_MEANINGFUL_EFFECT")
    if not dispositions:
        dispositions = ["MIXED"]

    out = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s5bb-v2-blocked-analysis",
        "experimentId": "COJC-J3-AIC-SET-VALUED-CURRENTNESS-S5B-B-V2",
        "campaignCount": len(campaigns),
        "observedBlocks": len(all_blocks),
        "completeComparisonBlocks": len(complete),
        "incompleteBlocks": len(incomplete),
        "providerInvalidBlocks": sum(bool(b.get("providerInvalid")) for b in all_blocks),
        "overall": overall,
        "byModel": by_model,
        "byCase": by_case,
        "pairedBlocks": paired,
        "deltas": {
            "bindingSetVsLinearSafePctPoints": round(bs["safeCorrectPct"] - lin["safeCorrectPct"], 1),
            "bindingSetVsLinearMultiplicityPctPoints": round(bs["multiplicityCorrectPct"] - lin["multiplicityCorrectPct"], 1),
            "bindingSetVsRawSafePctPoints": round(bs["safeCorrectPct"] - raw["safeCorrectPct"], 1),
            "bindingSetVsRawMultiplicityPctPoints": round(bs["multiplicityCorrectPct"] - raw["multiplicityCorrectPct"], 1),
        },
        "preRegisteredDispositions": dispositions,
    }
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "completeComparisonBlocks": out["completeComparisonBlocks"],
        "providerInvalidBlocks": out["providerInvalidBlocks"],
        "overall": overall,
        "deltas": out["deltas"],
        "preRegisteredDispositions": dispositions,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
