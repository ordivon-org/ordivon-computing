from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
paths = [ROOT / "evidence/f5-flash-v0.json", ROOT / "evidence/f5-pro-v0.json"]
rows = []
for path in paths:
    rows.extend(json.loads(path.read_text())["rows"])


def tokens(row):
    usage = row.get("usage") or {}
    provider = usage.get("providerUsage", [])
    return (
        sum(int(x.get("prompt_tokens", 0) or 0) for x in provider),
        sum(int(x.get("completion_tokens", 0) or 0) for x in provider),
        sum(int(x.get("total_tokens", 0) or 0) for x in provider),
    )


def error_class(row):
    if not row["valid"]:
        return "invalid"
    choice, oracle = row["decision"], row["oracleDecision"]
    if choice == oracle:
        return "exact"
    if choice == "INDEPENDENT_PLATFORM" and oracle != "INDEPENDENT_PLATFORM":
        return "false_platform"
    if choice == "SHARED_BOUNDARY" and oracle in {"OWNER_LOCAL", "RESEARCH_ONLY", "NO_CHANGE"}:
        return "over_shared"
    if choice == "OWNER_LOCAL" and oracle in {"RESEARCH_ONLY", "NO_CHANGE"}:
        return "over_local"
    if choice in {"NO_CHANGE", "RESEARCH_ONLY"} and oracle in {"OWNER_LOCAL", "SHARED_BOUNDARY"}:
        return "under_promoted"
    if choice == "OWNER_LOCAL" and oracle == "SHARED_BOUNDARY":
        return "under_shared"
    if choice == "NO_CHANGE" and oracle == "RESEARCH_ONLY":
        return "under_research"
    return "other_mismatch"

for row in rows:
    row["errorClass"] = error_class(row)


def agg(pred):
    rs = [r for r in rows if pred(r)]
    valid = [r for r in rs if r["valid"]]
    p = c = t = 0
    for r in rs:
        rp, rc, rt = tokens(r); p += rp; c += rc; t += rt
    return {
        "slots": len(rs),
        "valid": len(valid),
        "exact": sum(r["exactCorrect"] for r in valid),
        "accuracyAmongValid": sum(r["exactCorrect"] for r in valid) / len(valid) if valid else None,
        "errorClasses": dict(Counter(r["errorClass"] for r in rs)),
        "promptTokens": p,
        "completionTokens": c,
        "totalTokens": t,
        "meanTotalTokensPerSlot": t / len(rs) if rs else None,
    }

summary = {t: agg(lambda r, t=t: r["treatment"] == t) for t in ("raw", "prior")}
by_model = {
    model: {t: agg(lambda r, m=model, t=t: r["model"] == m and r["treatment"] == t) for t in ("raw", "prior")}
    for model in sorted({r["model"] for r in rows})
}
by_split = {
    split: {t: agg(lambda r, s=split, t=t: r["split"] == s and r["treatment"] == t) for t in ("raw", "prior")}
    for split in ("development", "holdout")
}

groups = defaultdict(dict)
for row in rows:
    groups[(row["model"], row["caseId"], row["replica"])][row["treatment"]] = row
paired = []
for key, arms in sorted(groups.items()):
    if set(arms) != {"raw", "prior"}:
        continue
    raw, prior = arms["raw"], arms["prior"]
    both = raw["valid"] and prior["valid"]
    rp, rc, rt = tokens(raw); pp, pc, pt = tokens(prior)
    paired.append({
        "model": key[0], "caseId": key[1], "replica": key[2], "bothValid": both,
        "rawDecision": raw["decision"], "priorDecision": prior["decision"], "oracle": raw["oracleDecision"],
        "rawCorrect": raw["exactCorrect"] if both else None,
        "priorCorrect": prior["exactCorrect"] if both else None,
        "accuracyDelta": int(prior["exactCorrect"]) - int(raw["exactCorrect"]) if both else None,
        "rawErrorClass": raw["errorClass"], "priorErrorClass": prior["errorClass"],
        "totalTokenDelta": pt - rt,
    })
valid_pairs = [p for p in paired if p["bothValid"]]
paired_summary = {
    "pairs": len(paired), "bothValid": len(valid_pairs),
    "priorWins": sum(p["accuracyDelta"] > 0 for p in valid_pairs),
    "rawWins": sum(p["accuracyDelta"] < 0 for p in valid_pairs),
    "ties": sum(p["accuracyDelta"] == 0 for p in valid_pairs),
    "meanTotalTokenDelta": sum(p["totalTokenDelta"] for p in paired) / len(paired),
    "byModel": {
        m: {
            "priorWins": sum(p["accuracyDelta"] > 0 for p in valid_pairs if p["model"] == m),
            "rawWins": sum(p["accuracyDelta"] < 0 for p in valid_pairs if p["model"] == m),
            "ties": sum(p["accuracyDelta"] == 0 for p in valid_pairs if p["model"] == m),
        }
        for m in sorted({p["model"] for p in valid_pairs})
    },
}

result = {
    "schemaVersion": 1,
    "kind": "ordivon.computing.pal-f5-meta-selection-analysis",
    "status": "completed",
    "excludedCampaign": {
        "jobId": "job-019ffbed-c48d-7fa3-8e6b-48c33199e2f8",
        "reason": "preliminary Pro v1 lost full row evidence after TLS EOF because the original runner only persisted at campaign end; whole campaign excluded before counted Pro v2 rerun",
    },
    "countedJobs": {
        "flash": "job-019ffbea-f177-7331-9795-d3cc264dd403",
        "pro": "job-019ffbf1-a019-7271-a6a6-78d4178d40ff",
    },
    "summary": summary,
    "byModel": by_model,
    "bySplit": by_split,
    "paired": paired_summary,
    "pairRows": paired,
    "interpretation": {
        "naiveMetaSelectionCompoundingSupported": False,
        "priorHasModelConditionalValue": True,
        "reason": "The same promotion prior improves several Flash owner-local decisions but pushes Pro toward systematic under-promotion on earned Observation/Usage/Security changes. Across models the net exact-decision benefit is small and the prior adds prompt cost. A meta-selection prior therefore behaves as a decision-boundary bias requiring calibration, not as universally beneficial delayed capital merely because it was historically reused.",
        "strongerCandidate": "Meta-selection value may come from coupling a reusable prior with evidence-sensitive calibration and explicit reopen/escalation conditions, rather than from static conservative rules alone.",
        "nextFalsifier": "Prospectively compare static prior versus calibrated prior that must report which promotion condition is missing/satisfied and an explicit reopen trigger. The calibrated form must improve both false promotion and missed earned-change rates across model families without becoming a hidden answer key.",
    },
    "claimBoundary": "Eight historical decision packets and two DeepSeek families. Exact disposition is intentionally strict; disagreements such as NO_CHANGE vs RESEARCH_ONLY are preserved rather than collapsed. No owner policy change is authorized.",
}
(ROOT / "f5-results-v0.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
print(json.dumps({"summary": summary, "byModel": by_model, "bySplit": by_split, "paired": paired_summary, "interpretation": result["interpretation"]}, ensure_ascii=False, indent=2))
