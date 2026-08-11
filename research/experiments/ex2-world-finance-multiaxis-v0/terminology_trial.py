from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
from collections import Counter

import relation_trial as base

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "terminology-corpus-v1.json").read_text(encoding="utf-8"))
ACTOR_RELATIONS = {
    "DECIDES_SEMANTICS","OWNS_STATE_SEMANTICS","PERSISTS_VIA","PROVES_NATIVE_FACT","PROVES_LOCAL_EXECUTION","MAPS_OR_DERIVES","RECONCILES_IDENTITY","ADMITS_CONSEQUENCE","VERIFIES_ACCEPTANCE","TIME_COORDINATE","DELEGATES_MECHANICS_TO"
}
TARGET_DOMAIN = {
    **{relation: "actors" for relation in ACTOR_RELATIONS},
    "SEMANTIC_HOME": "scope",
    "SHARED_PROMOTION": "sharedPromotion",
    "DOES_NOT_IMPLY": "negativeInference",
}
base.CORPUS = CORPUS
base.TARGET_DOMAIN = TARGET_DOMAIN


def analyze(trials):
    critical = set(CORPUS["metrics"]["criticalNativeSemanticCases"])
    carrier = set(CORPUS["metrics"]["ownerCarrierCases"])
    promotion = set(CORPUS["metrics"]["promotionCases"])
    out = {}
    for treatment in CORPUS["treatments"]:
        selected = [t for t in trials if t["treatment"] == treatment]
        rows = [r for t in selected for r in t["result"]]
        q_correct = sum(r["correct"] for r in rows)
        case_pairs = [(t,cid) for t in selected for cid in t["caseOrder"]]
        case_exact = sum(all(r["correct"] for r in t["result"] if r["caseId"] == cid) for t,cid in case_pairs)
        def case_group_exact(group):
            pairs = [(t,cid) for t in selected for cid in group]
            return sum(all(r["correct"] for r in t["result"] if r["caseId"] == cid) for t,cid in pairs) / len(pairs)
        promo_rows = [r for r in rows if r["caseId"] in promotion and r["relation"] == "SHARED_PROMOTION"]
        per_relation = {}
        for rel in CORPUS["relationTypes"]:
            rr=[r for r in rows if r["relation"]==rel]
            if rr:
                correct=sum(r["correct"] for r in rr)
                per_relation[rel]={"correct":correct,"total":len(rr),"accuracy":correct/len(rr)}
        out[treatment] = {
            "queryCorrect": q_correct,
            "queryTotal": len(rows),
            "queryExact": q_correct/len(rows),
            "caseExactCorrect": case_exact,
            "caseTotal": len(case_pairs),
            "caseExact": case_exact/len(case_pairs),
            "criticalNativeSemantic": case_group_exact(critical),
            "ownerCarrier": case_group_exact(carrier),
            "promotion": sum(r["correct"] for r in promo_rows)/len(promo_rows),
            "perRelation": per_relation,
            "totalTokens": sum(t["usage"]["totalTokens"] for t in selected),
            "providerCalls": sum(t["usage"]["providerCalls"] for t in selected),
        }
    a=out["compact_responsibility"]; b=out["role_pure_relations"]
    stable=(b["queryExact"]>=0.98 and b["caseExact"]>=0.95 and b["criticalNativeSemantic"]==1.0 and b["ownerCarrier"]==1.0 and b["promotion"]==1.0 and b["queryExact"]>=a["queryExact"]-0.01)
    benefit=stable and b["queryExact"]>=a["queryExact"]+0.02
    errors={}
    for treatment in CORPUS["treatments"]:
        counter=Counter()
        for t in trials:
            if t["treatment"]!=treatment: continue
            for r in t["result"]:
                if not r["correct"]: counter[(r["queryId"],r["relation"],r["oracle"],r["observed"])]+=1
        errors[treatment]=[{"queryId":q,"relation":rel,"oracle":o,"observed":obs,"count":n} for (q,rel,o,obs),n in counter.most_common()]
    classification="RELATION_PRESENTATION_BENEFIT" if benefit else ("RELATION_MODEL_STABLE" if stable else "REJECT")
    return {
        "treatments":out,
        "classification":classification,
        "pairedReplicates":[{
            "replicate":rep,
            "compactQueryCorrect":next(t for t in trials if t["replicate"]==rep and t["treatment"]=="compact_responsibility")["queryCorrect"],
            "rolePureQueryCorrect":next(t for t in trials if t["replicate"]==rep and t["treatment"]=="role_pure_relations")["queryCorrect"],
            "compactCaseExact":next(t for t in trials if t["replicate"]==rep and t["treatment"]=="compact_responsibility")["caseExact"],
            "rolePureCaseExact":next(t for t in trials if t["replicate"]==rep and t["treatment"]=="role_pure_relations")["caseExact"],
        } for rep in range(1,CORPUS["replicates"]+1)],
        "errorProfile":errors,
    }


def persist(path,trials,complete):
    doc={
        "schemaVersion":1,
        "kind":"ordivon.explanation-ex2-terminology-live-evidence",
        "complete":complete,
        "corpusDigest":base.digest(CORPUS),
        "authorityFreezeDigest":"sha256:"+hashlib.sha256((ROOT/"authority-freeze-v1.json").read_bytes()).hexdigest(),
        "trialCount":len(trials),
        "trials":trials,
    }
    if complete: doc["analysis"]=analyze(trials)
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True)+"\n"); tmp.replace(path)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=pathlib.Path,default=ROOT/"evidence"/"terminology-live-v1.json"); args=ap.parse_args()
    trials=[]
    if args.output.exists():
        e=json.loads(args.output.read_text());
        if e.get("corpusDigest")!=base.digest(CORPUS): raise RuntimeError("existing evidence corpus differs")
        trials=list(e.get("trials",[]))
    done={(int(t["replicate"]),str(t["treatment"])) for t in trials}; secrets=base.secret_paths()
    for rep in range(1,CORPUS["replicates"]+1):
        sp=secrets[(rep-1)%len(secrets)]; sec=json.loads(sp.read_text()); order=["compact_responsibility","role_pure_relations"] if rep%2 else ["role_pure_relations","compact_responsibility"]
        for treatment in order:
            if (rep,treatment) in done: continue
            cases=list(CORPUS["cases"]); random.Random(f"ex2-term:{rep}:{treatment}").shuffle(cases); result,usage=base.call_provider(sec,treatment,cases); trial=base.score_trial(treatment,rep,cases,result,usage,sp.name); trials.append(trial); persist(args.output,trials,False); print(json.dumps({"replicate":rep,"treatment":treatment,"queryCorrect":trial["queryCorrect"],"queryTotal":trial["queryTotal"],"caseExact":trial["caseExact"],"caseTotal":trial["caseTotal"],"tokens":usage["totalTokens"],"calls":usage["providerCalls"],"checkpointedTrials":len(trials)},sort_keys=True),flush=True)
    expected=CORPUS["replicates"]*len(CORPUS["treatments"])
    if len(trials)!=expected: persist(args.output,trials,False); raise RuntimeError(f"incomplete evidence: {len(trials)} != {expected}")
    persist(args.output,trials,True); final=json.loads(args.output.read_text()); print(json.dumps(final["analysis"],sort_keys=True),flush=True); return 0

if __name__=="__main__": raise SystemExit(main())
