from __future__ import annotations

import concurrent.futures
import json
from pathlib import Path

import ofr5_run as r

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "oracle-targeted-hydration-diagnostic-v1.json"


def main() -> None:
    source, atlas, queries, surfaces, contract = r.load()
    cases = {c["id"]: c for c in source["cases"]}
    qs = [q for q in queries["queries"] if q["split"] == "holdout"]
    specs = [(q, rep) for q in qs for rep in range(2)]

    def run_one(spec):
        q, rep = spec
        tag = f"diagnostic:oracle-hydration:{q['queryId']}:r{rep}"
        hyd = r.hydration_text(atlas, q["caseId"], q["requestedRoles"])
        row = {
            "queryId": q["queryId"],
            "replicate": rep,
            "oracleCaseId": q["caseId"],
            "oracleRequestedRoles": q["requestedRoles"],
            "hydration": {
                "selectedCaseId": q["caseId"],
                "selectedRoles": q["requestedRoles"],
                "utf8Bytes": len(hyd.encode()),
                "wordCount": len(hyd.split()),
            },
        }
        try:
            ans = r.run_structured(
                prompt=r.answer_prompt(hyd, q, selected_roles=q["requestedRoles"], progressive=True),
                schema=r.ANSWER_SCHEMA,
                result_kind="ofr5-oracle-hydration-diagnostic-answer",
                model=contract["livePlan"]["generationModel"],
                secret=r.slot_for(tag + ":answer"),
                tag=tag + ":answer",
                max_tokens=2200,
            )
            row["answer"] = ans
            row["answerRealized"] = bool(ans.get("valid") and isinstance(ans.get("result"), dict))
            if not row["answerRealized"]:
                row["semanticAccepted"] = False
                row["judge"] = None
                return row
            g = r.gold(cases[q["caseId"]], q)
            judged = r.run_structured(
                prompt=r.judge_prompt(q, g, ans["result"]),
                schema=r.JUDGE_SCHEMA,
                result_kind="ofr5-oracle-hydration-diagnostic-judge",
                model=contract["livePlan"]["judgeModel"],
                secret=r.slot_for(tag + ":judge"),
                tag=tag + ":judge",
                max_tokens=1100,
            )
            row["judge"] = judged
            row["semanticAccepted"] = bool(judged.get("valid") and isinstance(judged.get("result"), dict))
            return row
        except Exception as e:
            row["answerRealized"] = False
            row["semanticAccepted"] = False
            row["error"] = {"type": type(e).__name__, "message": str(e)[:800]}
            return row

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        rows = list(ex.map(run_one, specs))

    semantic = [x for x in rows if x.get("semanticAccepted")]
    scores = []
    ep = []
    unsupported = []
    over = []
    case = []
    for x in semantic:
        j = x["judge"]["result"]
        case.append(1.0 if j["caseIdentificationGrade"] == "PASS" else 0.0)
        ep.append(r.GRADE_VALUES[j["epistemicBoundaryGrade"]])
        unsupported.append(j["unsupportedInference"])
        over.append(j["overgeneralized"])
        for role in x["oracleRequestedRoles"]:
            scores.append(r.GRADE_VALUES[j[f"{role}Grade"]])
    total_prompt = sum(r.provider_prompt_tokens(x.get("answer")) for x in rows)
    total_tokens = sum(r.provider_total_tokens(x.get("answer")) for x in rows)
    realized = sum(bool(x.get("answerRealized")) for x in rows)
    analysis = {
        "physicalTrials": len(rows),
        "answerRealized": realized,
        "physicalAcceptanceRate": round(realized / len(rows), 4),
        "semanticAccepted": len(semantic),
        "caseLocalizationAccuracy": round(sum(case) / len(case), 4) if case else None,
        "requestedRoleMean": round(sum(scores) / len(scores), 4) if scores else None,
        "epistemicBoundaryMean": round(sum(ep) / len(ep), 4) if ep else None,
        "unsupportedInferenceRate": round(sum(unsupported) / len(unsupported), 4) if unsupported else None,
        "overgeneralizationRate": round(sum(over) / len(over), 4) if over else None,
        "meanHydrationWords": round(sum(x["hydration"]["wordCount"] for x in rows) / len(rows), 1),
        "meanHydrationBytes": round(sum(x["hydration"]["utf8Bytes"] for x in rows) / len(rows), 1),
        "totalProviderPromptTokens": total_prompt,
        "promptTokensPerPhysicalTrial": round(total_prompt / len(rows), 1),
        "promptTokensPerAcceptedAnswer": round(total_prompt / realized, 1) if realized else None,
        "totalTokensPerAcceptedAnswer": round(total_tokens / realized, 1) if realized else None,
    }
    out = {
        "schemaVersion": 1,
        "kind": "ordivon.ofr5-post-holdout-oracle-hydration-diagnostic.v1",
        "promotionEligible": False,
        "reason": "Post-holdout mechanism isolation only. Oracle case/roles remove navigation and over-hydration; results cannot repair or rescore the frozen OFR5 promotion decision.",
        "frozenSemanticArtifacts": json.loads((ROOT / "freeze-v1.json").read_text())["files"],
        "analysis": analysis,
        "trials": rows,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
