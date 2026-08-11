from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
from collections import Counter

import relation_trial as base

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "relation2-corpus-v1.json").read_text(encoding="utf-8"))
ACTOR_RELATIONS = {
    "DECIDES_SEMANTICS",
    "OWNS_STATE_SEMANTICS",
    "PERSISTS_VIA",
    "PROVES_NATIVE_FACT",
    "PROVES_LOCAL_EXECUTION",
    "MAPS_OR_DERIVES",
    "RECONCILES_IDENTITY",
    "ADMITS_CONSEQUENCE",
    "VERIFIES_ACCEPTANCE",
    "TIME_COORDINATE",
    "DELEGATES_MECHANICS_TO",
}
TARGET_DOMAIN = {
    **{relation: "actors" for relation in ACTOR_RELATIONS},
    "SEMANTIC_HOME": "scope",
    "SHARED_PROMOTION": "sharedPromotion",
    "DOES_NOT_IMPLY": "negativeInference",
}
base.CORPUS = CORPUS
base.TARGET_DOMAIN = TARGET_DOMAIN


def digest(value):
    return base.digest(value)


def analyze(trials):
    critical = set(CORPUS["metrics"]["criticalNativeFactCases"])
    carrier = set(CORPUS["metrics"]["ownerCarrierCases"])
    promotion = set(CORPUS["metrics"]["sharedPromotionCases"])
    negative = set(CORPUS["metrics"]["negativeInferenceCases"])
    out = {}
    for treatment in CORPUS["treatments"]:
        selected = [t for t in trials if t["treatment"] == treatment]
        rows = [row for t in selected for row in t["result"]]
        query_correct = sum(1 for row in rows if row["correct"])
        case_pairs = [(t, cid) for t in selected for cid in t["caseOrder"]]
        case_exact = sum(1 for t, cid in case_pairs if all(row["correct"] for row in t["result"] if row["caseId"] == cid))
        crit_rows = [row for row in rows if row["caseId"] in critical and row["relation"] == "PROVES_NATIVE_FACT"]
        carrier_pairs = [(t, cid) for t in selected for cid in carrier]
        promo_rows = [row for row in rows if row["caseId"] in promotion and row["relation"] == "SHARED_PROMOTION"]
        neg_rows = [row for row in rows if row["caseId"] in negative and row["relation"] == "DOES_NOT_IMPLY"]
        per_relation = {}
        for relation in CORPUS["relationTypes"]:
            rr = [row for row in rows if row["relation"] == relation]
            if rr:
                correct = sum(1 for row in rr if row["correct"])
                per_relation[relation] = {"correct": correct, "total": len(rr), "accuracy": correct / len(rr)}
        out[treatment] = {
            "queryCorrect": query_correct,
            "queryTotal": len(rows),
            "queryExact": query_correct / len(rows),
            "caseExactCorrect": case_exact,
            "caseTotal": len(case_pairs),
            "caseExact": case_exact / len(case_pairs),
            "criticalNativeFact": sum(1 for row in crit_rows if row["correct"]) / len(crit_rows),
            "ownerCarrier": sum(1 for t, cid in carrier_pairs if all(row["correct"] for row in t["result"] if row["caseId"] == cid)) / len(carrier_pairs),
            "sharedPromotion": sum(1 for row in promo_rows if row["correct"]) / len(promo_rows),
            "negativeInference": sum(1 for row in neg_rows if row["correct"]) / len(neg_rows),
            "perRelation": per_relation,
            "totalTokens": sum(t["usage"]["totalTokens"] for t in selected),
            "providerCalls": sum(t["usage"]["providerCalls"] for t in selected),
        }
    a = out["compact_responsibility"]
    b = out["typed_relations_v2"]
    supported = (
        b["queryExact"] >= a["queryExact"] + 0.03
        and b["caseExact"] >= 0.92
        and b["criticalNativeFact"] >= 0.98
        and b["ownerCarrier"] >= 0.98
        and b["sharedPromotion"] >= 0.95
        and b["negativeInference"] >= 0.95
    )
    safe = (
        b["queryExact"] >= 0.96
        and b["queryExact"] >= a["queryExact"] - 0.01
        and b["criticalNativeFact"] == 1.0
        and b["ownerCarrier"] >= a["ownerCarrier"]
        and b["sharedPromotion"] >= a["sharedPromotion"]
        and b["negativeInference"] >= 0.98
    )
    errors = {}
    for treatment in CORPUS["treatments"]:
        counter = Counter()
        for t in trials:
            if t["treatment"] != treatment:
                continue
            for row in t["result"]:
                if not row["correct"]:
                    counter[(row["queryId"], row["relation"], row["oracle"], row["observed"])] += 1
        errors[treatment] = [
            {"queryId": qid, "relation": relation, "oracle": oracle, "observed": observed, "count": count}
            for (qid, relation, oracle, observed), count in counter.most_common()
        ]
    return {
        "treatments": out,
        "classification": "RELATION_V2_SUPPORTED" if supported else ("SAFE_NONINFERIOR" if safe else "REJECT_OR_REVISE"),
        "pairedReplicates": [
            {
                "replicate": rep,
                "compactQueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_responsibility")["queryCorrect"],
                "relationV2QueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "typed_relations_v2")["queryCorrect"],
                "compactCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_responsibility")["caseExact"],
                "relationV2CaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "typed_relations_v2")["caseExact"],
            }
            for rep in range(1, int(CORPUS["replicates"]) + 1)
        ],
        "errorProfile": errors,
    }


def persist(path, trials, complete):
    doc = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-relation-v2-live-evidence",
        "complete": complete,
        "corpusDigest": digest(CORPUS),
        "authorityFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "authority-freeze-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
    }
    if complete:
        doc["analysis"] = analyze(trials)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "relation2-live-v1.json")
    args = parser.parse_args()
    trials = []
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if existing.get("corpusDigest") != digest(CORPUS):
            raise RuntimeError("existing evidence corpus differs")
        trials = list(existing.get("trials", []))
    done = {(int(t["replicate"]), str(t["treatment"])) for t in trials}
    secrets = base.secret_paths()
    for replicate in range(1, int(CORPUS["replicates"]) + 1):
        secret_path = secrets[(replicate - 1) % len(secrets)]
        secret = json.loads(secret_path.read_text(encoding="utf-8"))
        order = ["compact_responsibility", "typed_relations_v2"] if replicate % 2 else ["typed_relations_v2", "compact_responsibility"]
        for treatment in order:
            if (replicate, treatment) in done:
                continue
            cases = list(CORPUS["cases"])
            random.Random(f"ex2-rel2:{replicate}:{treatment}").shuffle(cases)
            result, usage = base.call_provider(secret, treatment, cases)
            trial = base.score_trial(treatment, replicate, cases, result, usage, secret_path.name)
            trials.append(trial)
            persist(args.output, trials, complete=False)
            print(json.dumps({
                "replicate": replicate,
                "treatment": treatment,
                "queryCorrect": trial["queryCorrect"],
                "queryTotal": trial["queryTotal"],
                "caseExact": trial["caseExact"],
                "caseTotal": trial["caseTotal"],
                "tokens": usage["totalTokens"],
                "calls": usage["providerCalls"],
                "checkpointedTrials": len(trials),
            }, sort_keys=True), flush=True)
    expected = int(CORPUS["replicates"]) * len(CORPUS["treatments"])
    if len(trials) != expected:
        persist(args.output, trials, complete=False)
        raise RuntimeError(f"incomplete evidence: {len(trials)} != {expected}")
    persist(args.output, trials, complete=True)
    final = json.loads(args.output.read_text(encoding="utf-8"))
    print(json.dumps(final["analysis"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
