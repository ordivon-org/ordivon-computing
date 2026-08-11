from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random

import family_transfer_trial as family
import relation_trial as base

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = family.CORPUS
base.CORPUS = CORPUS
base.TARGET_DOMAIN = family.TARGET_DOMAIN


def merged_trial(treatment, replicate, cases, secret, secret_name):
    shuffled = list(cases)
    random.Random(f"ex2-family-v3:{replicate}:{treatment}").shuffle(shuffled)
    chunks = [shuffled[index:index + 6] for index in range(0, len(shuffled), 6)]
    scored_rows = []
    usage_total = {
        "promptTokens": 0,
        "completionTokens": 0,
        "totalTokens": 0,
        "providerCalls": 0,
        "wireCorrections": [],
        "elapsedMs": 0,
        "requestDigests": [],
    }
    provider_models = []
    case_order = []
    for chunk_index, chunk in enumerate(chunks):
        result, usage = base.call_provider(secret, treatment, chunk)
        part = base.score_trial(treatment, replicate, chunk, result, usage, secret_name)
        scored_rows.extend(part["result"])
        case_order.extend(part["caseOrder"])
        provider_models.append(part["providerModel"])
        for key in ("promptTokens", "completionTokens", "totalTokens", "providerCalls", "elapsedMs"):
            usage_total[key] += int(usage[key])
        usage_total["wireCorrections"].append({"chunk": chunk_index, "corrections": usage["wireCorrections"]})
        usage_total["requestDigests"].append(usage["requestDigest"])
    if len(set(provider_models)) != 1:
        raise RuntimeError(f"provider model drift across chunks: {provider_models}")
    return {
        "treatment": treatment,
        "replicate": replicate,
        "secretSlot": secret_name,
        "caseOrder": case_order,
        "result": scored_rows,
        "queryCorrect": sum(1 for row in scored_rows if row["correct"]),
        "queryTotal": len(scored_rows),
        "caseExact": sum(1 for cid in case_order if all(row["correct"] for row in scored_rows if row["caseId"] == cid)),
        "caseTotal": len(case_order),
        "usage": usage_total,
        "providerModel": provider_models[0],
        "chunkCount": len(chunks),
    }


def persist(path, trials, complete):
    doc = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-family-transfer-evidence",
        "apparatusVersion": 3,
        "complete": complete,
        "corpusDigest": base.digest(CORPUS),
        "familyFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "family-authority-freeze-v1.json").read_bytes()).hexdigest(),
        "familyRelationsDigest": "sha256:" + hashlib.sha256((ROOT / "family-relations-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
    }
    if complete:
        doc["analysis"] = family.analyze(trials)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "family-transfer-live-v3.json")
    args = ap.parse_args()
    trials = []
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if existing.get("corpusDigest") != base.digest(CORPUS):
            raise RuntimeError("existing evidence corpus differs")
        trials = list(existing.get("trials", []))
    done = {(int(t["replicate"]), str(t["treatment"])) for t in trials}
    secrets = base.secret_paths()
    for rep in range(1, CORPUS["replicates"] + 1):
        sp = secrets[(rep - 1) % len(secrets)]
        secret = json.loads(sp.read_text(encoding="utf-8"))
        order = ["compact_family", "role_pure_family_relations"] if rep % 2 else ["role_pure_family_relations", "compact_family"]
        for treatment in order:
            if (rep, treatment) in done:
                continue
            trial = merged_trial(treatment, rep, CORPUS["cases"], secret, sp.name)
            trials.append(trial)
            persist(args.output, trials, False)
            print(json.dumps({
                "replicate": rep,
                "treatment": treatment,
                "queryCorrect": trial["queryCorrect"],
                "queryTotal": trial["queryTotal"],
                "caseExact": trial["caseExact"],
                "caseTotal": trial["caseTotal"],
                "tokens": trial["usage"]["totalTokens"],
                "calls": trial["usage"]["providerCalls"],
                "checkpointedTrials": len(trials),
            }, sort_keys=True), flush=True)
    expected = CORPUS["replicates"] * len(CORPUS["treatments"])
    if len(trials) != expected:
        persist(args.output, trials, False)
        raise RuntimeError(f"incomplete evidence: {len(trials)} != {expected}")
    persist(args.output, trials, True)
    final = json.loads(args.output.read_text(encoding="utf-8"))
    print(json.dumps(final["analysis"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
