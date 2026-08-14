from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
files = [ROOT / "evidence/f4-flash-v0.json", ROOT / "evidence/f4-pro-v0.json"]
rows = []
for path in files:
    doc = json.loads(path.read_text())
    rows.extend(doc["rows"])


def token_parts(row):
    usage = row["usage"]
    provider = usage.get("providerUsage", [])
    prompt = sum(int(x.get("prompt_tokens", 0) or 0) for x in provider)
    completion = sum(int(x.get("completion_tokens", 0) or 0) for x in provider)
    total = sum(int(x.get("total_tokens", 0) or 0) for x in provider)
    return prompt, completion, total


def aggregate(filter_fn):
    rs = [r for r in rows if filter_fn(r)]
    valid = [r for r in rs if r["treatmentShapeValid"]]
    prompt = completion = total = 0
    for r in rs:
        p, c, t = token_parts(r)
        prompt += p
        completion += c
        total += t
    return {
        "logicalSlots": len(rs),
        "validSlots": len(valid),
        "validityRate": len(valid) / len(rs) if rs else None,
        "causeCorrectAmongValid": sum(r["causeCorrect"] for r in valid),
        "testCorrectAmongValid": sum(r["testCorrect"] for r in valid),
        "jointCorrectAmongValid": sum(r["jointCorrect"] for r in valid),
        "jointAccuracyAmongValid": sum(r["jointCorrect"] for r in valid) / len(valid) if valid else None,
        "oracleCoverageAmongValid": sum(r["oracleCoveredByConsidered"] for r in valid),
        "modelCalls": sum(int(r.get("modelCalls", 0) or 0) for r in rs),
        "promptTokens": prompt,
        "completionTokens": completion,
        "totalTokens": total,
        "meanCompletionTokensPerSlot": completion / len(rs) if rs else None,
        "meanTotalTokensPerSlot": total / len(rs) if rs else None,
    }

summary = {
    treatment: aggregate(lambda r, t=treatment: r["treatment"] == t)
    for treatment in ("single", "variation")
}
by_model = {
    model: {
        treatment: aggregate(
            lambda r, m=model, t=treatment: r["model"] == m and r["treatment"] == t
        )
        for treatment in ("single", "variation")
    }
    for model in sorted({r["model"] for r in rows})
}
by_split = {
    split: {
        treatment: aggregate(
            lambda r, s=split, t=treatment: r["split"] == s and r["treatment"] == t
        )
        for treatment in ("single", "variation")
    }
    for split in ("development", "holdout")
}

# Exact within model/case/replica paired comparison only when both arms are valid.
groups = defaultdict(dict)
for r in rows:
    groups[(r["model"], r["caseId"], r["replica"])][r["treatment"]] = r
paired = []
for key, arms in sorted(groups.items()):
    if set(arms) != {"single", "variation"}:
        continue
    single, variation = arms["single"], arms["variation"]
    both_valid = single["treatmentShapeValid"] and variation["treatmentShapeValid"]
    sp, sc, st = token_parts(single)
    vp, vc, vt = token_parts(variation)
    paired.append(
        {
            "model": key[0],
            "caseId": key[1],
            "replica": key[2],
            "bothValid": both_valid,
            "singleJoint": single["jointCorrect"] if both_valid else None,
            "variationJoint": variation["jointCorrect"] if both_valid else None,
            "jointDelta": int(variation["jointCorrect"]) - int(single["jointCorrect"])
            if both_valid
            else None,
            "completionTokenDelta": vc - sc,
            "totalTokenDelta": vt - st,
        }
    )
valid_pairs = [p for p in paired if p["bothValid"]]

invalid = [
    {
        "model": r["model"],
        "caseId": r["caseId"],
        "replica": r["replica"],
        "treatment": r["treatment"],
        "stopCode": r["stopCode"],
        "modelCalls": r["modelCalls"],
        "result": r["result"],
        "totalTokens": token_parts(r)[2],
    }
    for r in rows
    if not r["treatmentShapeValid"]
]

result = {
    "schemaVersion": 1,
    "kind": "ordivon.computing.pal-f4-variation-analysis",
    "status": "completed",
    "logicalTrials": len(rows),
    "summary": summary,
    "byModel": by_model,
    "bySplit": by_split,
    "paired": {
        "totalPairs": len(paired),
        "bothValidPairs": len(valid_pairs),
        "variationSemanticWins": sum(p["jointDelta"] > 0 for p in valid_pairs),
        "singleSemanticWins": sum(p["jointDelta"] < 0 for p in valid_pairs),
        "semanticTies": sum(p["jointDelta"] == 0 for p in valid_pairs),
        "meanCompletionTokenDelta": sum(p["completionTokenDelta"] for p in paired) / len(paired),
        "meanTotalTokenDelta": sum(p["totalTokenDelta"] for p in paired) / len(paired),
    },
    "invalidSlots": invalid,
    "interpretation": {
        "hVariationSupportedAsSemanticBottleneck": False,
        "reason": "Among every valid logical trial in both treatments, the selected cause+test is correct. Across exact pairs where both arms are valid, explicit four-cause variation produces no semantic wins. Variation slightly changes validity/compliance and costs more completion tokens, but coverage/compliance without final diagnosis gain does not satisfy the preregistered H-VARIATION admission rule.",
        "scope": "Six bounded historical diagnosis tasks with explicit candidate cause/test menus and strong DeepSeek models. This does not show variation is never useful in open-ended generation where the correct candidate is absent from a supplied menu.",
        "nextFalsifier": "Test variation only where candidate generation itself is the uncertainty: remove the closed cause menu, freeze an external oracle, and compare independently generated candidate sets under matched total token budget. Do not build variation infrastructure from F4.",
    },
    "claimBoundary": "Invalid structured Provider slots are validity/apparatus outcomes, not semantic misses. Semantic comparisons are restricted to valid results and exact both-valid pairs.",
}
(ROOT / "f4-results-v0.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
)
print(json.dumps({
    "summary": summary,
    "byModel": by_model,
    "bySplit": by_split,
    "paired": result["paired"],
    "invalidCount": len(invalid),
    "interpretation": result["interpretation"],
}, ensure_ascii=False, indent=2))
