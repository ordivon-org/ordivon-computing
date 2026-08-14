from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVIDENCE = {
    "deepseek-v4-flash": ROOT / "evidence/f6-flash-v0.json",
    "deepseek-v4-pro": ROOT / "evidence/f6-pro-v0.json",
}
COUNTED_JOBS = {
    "deepseek-v4-flash": "job-019ffbfa-8a87-7502-82b1-13c35ac9af14",
    "deepseek-v4-pro": "job-019ffc41-3a6e-7a52-8513-d81620693b74",
}
TREATMENTS = ("raw", "static", "calibrated")
RETENTION_TIER = {
    "REJECT": 0,
    "DEFER": 0,
    "CONDITIONAL": 1,
    "RETAIN_ON_DEMAND": 1,
    "RETAIN_METHOD": 1,
    "PROMOTE_OWNER_UTILITY": 2,
}

rows = []
for model, path in EVIDENCE.items():
    doc = json.loads(path.read_text())
    assert doc["model"] == model
    assert len(doc["rows"]) == 48
    rows.extend(doc["rows"])
assert len(rows) == 96


def digest(path: Path) -> str:
    return "sha256:" + sha256(path.read_bytes()).hexdigest()


def token_tuple(row):
    usage = row.get("usage") or {}
    provider = usage.get("providerUsage", [])
    return (
        sum(int(x.get("prompt_tokens", 0) or 0) for x in provider),
        sum(int(x.get("completion_tokens", 0) or 0) for x in provider),
        int(usage.get("totalTokens", 0) or sum(int(x.get("total_tokens", 0) or 0) for x in provider)),
    )


def error_class(row):
    if not row["valid"]:
        return "invalid"
    if row["exactCorrect"]:
        return "exact"
    oracle = row["oracleDecision"]
    choice = row["decision"]
    ot, ct = RETENTION_TIER[oracle], RETENTION_TIER[choice]
    if ct > ot:
        return "over_retention_tier"
    if ct < ot:
        return "under_retention_tier"
    return "same_tier_class_mismatch"


for row in rows:
    row["errorClass"] = error_class(row)


def aggregate(pred):
    rs = [r for r in rows if pred(r)]
    valid = [r for r in rs if r["valid"]]
    p = c = t = 0
    for r in rs:
        rp, rc, rt = token_tuple(r)
        p += rp
        c += rc
        t += rt
    exact = sum(bool(r["exactCorrect"]) for r in valid)
    return {
        "slots": len(rs),
        "valid": len(valid),
        "invalid": len(rs) - len(valid),
        "validityRate": len(valid) / len(rs) if rs else None,
        "exact": exact,
        "accuracyAmongValid": exact / len(valid) if valid else None,
        "errorClasses": dict(Counter(r["errorClass"] for r in rs)),
        "stopCodes": dict(Counter(r["stopCode"] for r in rs)),
        "promptTokens": p,
        "completionTokens": c,
        "totalTokens": t,
        "meanTotalTokensPerSlot": t / len(rs) if rs else None,
    }


summary = {t: aggregate(lambda r, t=t: r["treatment"] == t) for t in TREATMENTS}
by_model = {
    model: {t: aggregate(lambda r, m=model, t=t: r["model"] == m and r["treatment"] == t) for t in TREATMENTS}
    for model in sorted(EVIDENCE)
}
by_split = {
    split: {t: aggregate(lambda r, s=split, t=t: r["split"] == s and r["treatment"] == t) for t in TREATMENTS}
    for split in ("development", "holdout")
}
by_case = {
    case: {t: aggregate(lambda r, c=case, t=t: r["caseId"] == c and r["treatment"] == t) for t in TREATMENTS}
    for case in sorted({r["caseId"] for r in rows})
}


def two_sided_sign_p(wins: int, losses: int):
    n = wins + losses
    if n == 0:
        return None
    k = min(wins, losses)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


groups = defaultdict(dict)
for row in rows:
    groups[(row["model"], row["caseId"], row["replica"])][row["treatment"]] = row


def paired_comparison(a: str, b: str, split: str | None = None, model: str | None = None):
    pair_rows = []
    for (m, case, replica), arms in sorted(groups.items()):
        if model is not None and m != model:
            continue
        if set(arms) != set(TREATMENTS):
            continue
        if split is not None and arms[a]["split"] != split:
            continue
        ra, rb = arms[a], arms[b]
        both_valid = bool(ra["valid"] and rb["valid"])
        _, _, ta = token_tuple(ra)
        _, _, tb = token_tuple(rb)
        delta = None
        if both_valid:
            delta = int(bool(ra["exactCorrect"])) - int(bool(rb["exactCorrect"]))
        pair_rows.append({
            "model": m,
            "caseId": case,
            "replica": replica,
            "split": ra["split"],
            "bothValid": both_valid,
            "aCorrect": bool(ra["exactCorrect"]) if both_valid else None,
            "bCorrect": bool(rb["exactCorrect"]) if both_valid else None,
            "accuracyDelta": delta,
            "aDecision": ra["decision"],
            "bDecision": rb["decision"],
            "oracle": ra["oracleDecision"],
            "aErrorClass": ra["errorClass"],
            "bErrorClass": rb["errorClass"],
            "totalTokenDelta": ta - tb,
        })
    valid_pairs = [p for p in pair_rows if p["bothValid"]]
    wins = sum(p["accuracyDelta"] > 0 for p in valid_pairs)
    losses = sum(p["accuracyDelta"] < 0 for p in valid_pairs)
    ties = sum(p["accuracyDelta"] == 0 for p in valid_pairs)
    return {
        "a": a,
        "b": b,
        "pairs": len(pair_rows),
        "bothValid": len(valid_pairs),
        "invalidPair": len(pair_rows) - len(valid_pairs),
        "aWins": wins,
        "bWins": losses,
        "ties": ties,
        "twoSidedSignP": two_sided_sign_p(wins, losses),
        "meanTotalTokenDeltaAllPairs": sum(p["totalTokenDelta"] for p in pair_rows) / len(pair_rows) if pair_rows else None,
        "rows": pair_rows,
    }

pairwise = {}
for a, b in (("calibrated", "raw"), ("calibrated", "static"), ("static", "raw")):
    key = f"{a}_vs_{b}"
    pairwise[key] = {
        "all": paired_comparison(a, b),
        "holdout": paired_comparison(a, b, split="holdout"),
        "byModel": {m: paired_comparison(a, b, model=m) for m in sorted(EVIDENCE)},
    }

raw_tokens = summary["raw"]["totalTokens"]
static_tokens = summary["static"]["totalTokens"]
cal_tokens = summary["calibrated"]["totalTokens"]

result = {
    "schemaVersion": 1,
    "kind": "ordivon.computing.pal-f6-calibrated-meta-selection-analysis",
    "status": "completed",
    "countedJobs": COUNTED_JOBS,
    "evidenceDigests": {model: digest(path) for model, path in EVIDENCE.items()},
    "summary": summary,
    "byModel": by_model,
    "bySplit": by_split,
    "byCase": by_case,
    "pairwise": pairwise,
    "costDelta": {
        "staticVsRawTotalTokens": static_tokens - raw_tokens,
        "staticVsRawFraction": (static_tokens - raw_tokens) / raw_tokens,
        "calibratedVsRawTotalTokens": cal_tokens - raw_tokens,
        "calibratedVsRawFraction": (cal_tokens - raw_tokens) / raw_tokens,
        "calibratedVsStaticTotalTokens": cal_tokens - static_tokens,
        "calibratedVsStaticFraction": (cal_tokens - static_tokens) / static_tokens,
    },
    "interpretation": {
        "calibratedMetaSelectionGeneralizationSupported": False,
        "staticMetaSelectionPriorSupported": False,
        "reason": "CALIBRATED has the highest aggregate exact accuracy among valid outputs (16/26) but does not beat RAW in exact both-valid paired decisions: 3 wins, 3 losses, 16 ties. It also consumes materially more tokens. STATIC is worse than RAW in aggregate and likewise shows no paired advantage. Holdout CALIBRATED has a small directional edge, but only two paired wins over RAW with zero losses among eleven both-valid holdout pairs; this is far below a stable cross-model admission threshold. The result therefore falsifies the preregistered claim that this general calibration procedure reliably improves cross-model decision quality over both RAW and STATIC.",
        "modelInteraction": "Flash shows a small aggregate CALIBRATED advantage; Pro has higher semantic accuracy among valid RAW outputs and substantial treatment-independent no_progress invalidity on several cases. CALIBRATED improves Pro validity relative to RAW/STATIC but not enough to establish semantic decision superiority. Structured-result validity must remain a separate apparatus outcome.",
        "caseInteraction": "The treatment effect is case-specific: calibration helps some DEFER/REJECT judgments such as Firefox/WebKit and osquery, but harms or fails on mutation-testing, TShark and mitmproxy. This is evidence against a universal scalar promotion bias or one fixed checklist acting as general meta-selection capital.",
        "strongerCandidate": "Meta-selection may require decision-family-specific causal features, confidence/uncertainty representation, or learned calibration from prospective outcomes rather than a static general rule. That is a new hypothesis, not an earned PAL mechanism.",
        "nextFalsifier": "Do not tune CALIBRATED v2 on these same cases. Move to a different foundational question with stronger discrimination: prospectively test whether explicit negative feedback/regulation prevents false self-reinforcement under repeated adaptive rounds, or test open-ended variation where the correct candidate is absent from the supplied menu. Revisit meta-selection only with a new decision family and a mechanism that was fixed before seeing its outcomes.",
    },
    "claimBoundary": "Eight frozen professional-equipment decisions, two DeepSeek model families, two replicas, and three predeclared treatments. Invalid structured outputs are validity/apparatus outcomes rather than semantic errors; exact semantic comparisons use valid outputs and paired comparisons require both arms valid. F6 does not authorize an architecture governor, promotion service, owner policy, PAL controller, or tuned calibration rule.",
}

(ROOT / "f6-results-v0.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
print(json.dumps({
    "summary": summary,
    "byModel": by_model,
    "bySplit": by_split,
    "pairwise": {k: {kk: vv for kk, vv in v.items() if kk != "byModel"} for k, v in pairwise.items()},
    "costDelta": result["costDelta"],
    "interpretation": result["interpretation"],
}, ensure_ascii=False, indent=2))
