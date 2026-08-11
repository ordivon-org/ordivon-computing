from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import pathlib
import random
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "family2-corpus-v1.json").read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def secret_paths() -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for path in sorted(pathlib.Path("/root/.config/ordivon/secrets").glob("deepseek*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if all(isinstance(value.get(k), str) and value[k] for k in ("apiKey", "baseUrl", "model")):
            out.append(path)
    if not out:
        raise RuntimeError("no usable DeepSeek secret")
    return out


def query_specs() -> list[dict[str, Any]]:
    out = []
    for case in CORPUS["cases"]:
        for query in case["queries"]:
            out.append({
                "queryId": f"{case['id']}.{query['q']}",
                "caseId": case["id"],
                "scenario": case["scenario"],
                "relation": query["relation"],
                "oracle": query["answer"],
            })
    return out


def call_one(secret: dict[str, Any], treatment: str, spec: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    relation = spec["relation"]
    allowed = CORPUS["targetDomains"][relation]
    system = (
        "You are a fresh evaluator learning an unfamiliar multi-project Agent system. Learn only from the explanation. "
        "Answer exactly ONE responsibility relation. Project names are valid only when the relation asks for a project-owned contract/derivation. "
        "SEMANTIC_JUDGE means the person/Agent/domain evaluator responsible for meaning; OWNER_NATIVE_SOURCE means an Ordivon project's own authoritative source/state; NATIVE_EXTERNAL_SYSTEM means an independently authoritative provider/physical/domain system. "
        "Return only the required tool call.\n\n"
        f"RELATION: {relation}: {CORPUS['relationTypes'][relation]}\n\n"
        "EXPLANATION:\n" + CORPUS["treatments"][treatment]
    )
    user = {
        "queryId": spec["queryId"],
        "scenario": spec["scenario"],
        "relation": relation,
        "question": CORPUS["relationTypes"][relation],
    }
    tool = {
        "type": "function",
        "function": {
            "name": "submit_one_relation",
            "description": "Submit the target for this one responsibility relation.",
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "target": {"type": "string", "enum": allowed},
                    "reason": {"type": "string", "minLength": 1, "maxLength": 400},
                },
                "required": ["target", "reason"],
            },
        },
    }
    body = {
        "model": secret["model"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False, separators=(",", ":"))},
        ],
        "tools": [tool],
        "tool_choice": {"type": "function", "function": {"name": "submit_one_relation"}},
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": 700,
        "stream": False,
    }
    data = canonical(body)
    corrections: list[dict[str, Any]] = []
    started = time.time_ns()
    for attempt in range(1, 6):
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + secret["apiKey"],
                "Content-Type": "application/json",
                "User-Agent": "ordivon-ex2-family2-single/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                payload = json.loads(response.read(2_000_000))
        except (urllib.error.URLError, TimeoutError, OSError, http.client.IncompleteRead) as exc:
            corrections.append({"attempt": attempt, "kind": "transport", "error": type(exc).__name__})
            if attempt == 5:
                raise
            time.sleep(0.7 * attempt)
            continue
        try:
            calls = payload["choices"][0]["message"].get("tool_calls") or []
            if len(calls) != 1 or calls[0].get("function", {}).get("name") != "submit_one_relation":
                raise ValueError("required tool call missing or multiple")
            args = json.loads(calls[0]["function"]["arguments"])
            if not isinstance(args, dict) or set(args) != {"target", "reason"}:
                raise ValueError("answer fields differ")
            if args["target"] not in allowed:
                raise ValueError(f"target invalid for {relation}: {args['target']}")
            if not isinstance(args["reason"], str) or not args["reason"]:
                raise ValueError("reason invalid")
            usage = payload.get("usage") or {}
            return {
                "queryId": spec["queryId"],
                "caseId": spec["caseId"],
                "relation": relation,
                "oracle": spec["oracle"],
                "observed": args["target"],
                "correct": args["target"] == spec["oracle"],
                "reason": args["reason"],
                "providerModel": payload.get("model", secret["model"]),
            }, {
                "promptTokens": int(usage.get("prompt_tokens", 0) or 0),
                "completionTokens": int(usage.get("completion_tokens", 0) or 0),
                "totalTokens": int(usage.get("total_tokens", 0) or 0),
                "providerCalls": attempt,
                "wireCorrections": corrections,
                "elapsedMs": (time.time_ns() - started) // 1_000_000,
                "requestDigest": digest(body),
            }
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            corrections.append({"attempt": attempt, "kind": "schema", "error": str(exc)[:300]})
            if attempt == 5:
                raise RuntimeError(f"single-query schema-invalid after retries: {spec['queryId']} {corrections}") from exc
            time.sleep(0.35 * attempt)
    raise AssertionError("unreachable")


def run_trial(secret: dict[str, Any], secret_name: str, treatment: str, replicate: int) -> dict[str, Any]:
    specs = query_specs()
    random.Random(f"ex2-family2-single:{replicate}:{treatment}").shuffle(specs)
    results_by_id: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(call_one, secret, treatment, spec): spec for spec in specs}
        for future in as_completed(futures):
            spec = futures[future]
            result, usage = future.result()
            results_by_id[spec["queryId"]] = (result, usage)
    scored = []
    usage_total = {
        "promptTokens": 0,
        "completionTokens": 0,
        "totalTokens": 0,
        "providerCalls": 0,
        "elapsedMsSum": 0,
        "wireCorrections": [],
        "requestDigests": [],
    }
    models = []
    for spec in specs:
        result, usage = results_by_id[spec["queryId"]]
        models.append(result.pop("providerModel"))
        scored.append(result)
        for key in ("promptTokens", "completionTokens", "totalTokens", "providerCalls"):
            usage_total[key] += int(usage[key])
        usage_total["elapsedMsSum"] += int(usage["elapsedMs"])
        if usage["wireCorrections"]:
            usage_total["wireCorrections"].append({"queryId": spec["queryId"], "corrections": usage["wireCorrections"]})
        usage_total["requestDigests"].append({"queryId": spec["queryId"], "digest": usage["requestDigest"]})
    if len(set(models)) != 1:
        raise RuntimeError(f"provider model drift: {set(models)}")
    case_order = [case["id"] for case in CORPUS["cases"]]
    return {
        "treatment": treatment,
        "replicate": replicate,
        "secretSlot": secret_name,
        "result": scored,
        "queryCorrect": sum(1 for row in scored if row["correct"]),
        "queryTotal": len(scored),
        "caseExact": sum(1 for cid in case_order if all(row["correct"] for row in scored if row["caseId"] == cid)),
        "caseTotal": len(case_order),
        "usage": usage_total,
        "providerModel": models[0],
        "subcallCount": len(specs),
    }


def group_case_exact(selected: list[dict[str, Any]], group: set[str]) -> float:
    pairs = [(t, cid) for t in selected for cid in group]
    return sum(all(r["correct"] for r in t["result"] if r["caseId"] == cid) for t, cid in pairs) / len(pairs)


def analyze(trials: list[dict[str, Any]]) -> dict[str, Any]:
    infra = set(CORPUS["metrics"]["infrastructureCases"])
    domain = set(CORPUS["metrics"]["domainCases"])
    negative = set(CORPUS["metrics"]["negativeCases"])
    promotion = set(CORPUS["metrics"]["promotionCases"])
    out = {}
    for treatment in CORPUS["treatments"]:
        selected = [t for t in trials if t["treatment"] == treatment]
        rows = [r for t in selected for r in t["result"]]
        qc = sum(r["correct"] for r in rows)
        case_pairs = [(t, cid) for t in selected for cid in [case["id"] for case in CORPUS["cases"]]]
        ce = sum(all(r["correct"] for r in t["result"] if r["caseId"] == cid) for t, cid in case_pairs)
        neg_rows = [r for r in rows if r["caseId"] in negative and r["relation"] == "DOES_NOT_IMPLY"]
        promo_rows = [r for r in rows if r["caseId"] in promotion and r["relation"] == "SHARED_PROMOTION"]
        per_relation = {}
        for relation in CORPUS["relationTypes"]:
            rr = [r for r in rows if r["relation"] == relation]
            if rr:
                correct = sum(r["correct"] for r in rr)
                per_relation[relation] = {"correct": correct, "total": len(rr), "accuracy": correct / len(rr)}
        out[treatment] = {
            "queryCorrect": qc,
            "queryTotal": len(rows),
            "queryExact": qc / len(rows),
            "caseExactCorrect": ce,
            "caseTotal": len(case_pairs),
            "caseExact": ce / len(case_pairs),
            "infrastructure": group_case_exact(selected, infra),
            "domain": group_case_exact(selected, domain),
            "negative": sum(r["correct"] for r in neg_rows) / len(neg_rows),
            "promotion": sum(r["correct"] for r in promo_rows) / len(promo_rows),
            "perRelation": per_relation,
            "totalTokens": sum(t["usage"]["totalTokens"] for t in selected),
            "providerCalls": sum(t["usage"]["providerCalls"] for t in selected),
        }
    a = out["compact_family"]
    b = out["role_pure_family_relations"]
    stable = (
        b["queryExact"] >= 0.97
        and b["caseExact"] >= 0.92
        and b["infrastructure"] >= 0.97
        and b["domain"] >= 0.97
        and b["negative"] >= 0.98
        and b["promotion"] == 1.0
        and b["queryExact"] >= a["queryExact"] - 0.01
    )
    benefit = stable and b["queryExact"] >= a["queryExact"] + 0.02
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
        "classification": "FAMILY_PRESENTATION_BENEFIT" if benefit else ("FAMILY_RELATIONS_STABLE" if stable else "REJECT"),
        "pairedReplicates": [
            {
                "replicate": rep,
                "compactQueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_family")["queryCorrect"],
                "rolePureQueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "role_pure_family_relations")["queryCorrect"],
                "compactCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_family")["caseExact"],
                "rolePureCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "role_pure_family_relations")["caseExact"],
            }
            for rep in range(1, CORPUS["replicates"] + 1)
        ],
        "errorProfile": errors,
    }


def persist(path: pathlib.Path, trials: list[dict[str, Any]], complete: bool) -> None:
    doc = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-family2-live-evidence",
        "apparatusVersion": 2,
        "complete": complete,
        "corpusDigest": digest(CORPUS),
        "familyFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "family-authority-freeze-v1.json").read_bytes()).hexdigest(),
        "familyRelationsDigest": "sha256:" + hashlib.sha256((ROOT / "family-relations-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
    }
    if complete:
        doc["analysis"] = analyze(trials)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "family2-live-v2.json")
    args = parser.parse_args()
    trials: list[dict[str, Any]] = []
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if existing.get("corpusDigest") != digest(CORPUS):
            raise RuntimeError("existing evidence corpus differs")
        trials = list(existing.get("trials", []))
    done = {(int(t["replicate"]), str(t["treatment"])) for t in trials}
    secrets = secret_paths()
    for rep in range(1, CORPUS["replicates"] + 1):
        secret_path = secrets[(rep - 1) % len(secrets)]
        secret = json.loads(secret_path.read_text(encoding="utf-8"))
        order = ["compact_family", "role_pure_family_relations"] if rep % 2 else ["role_pure_family_relations", "compact_family"]
        for treatment in order:
            if (rep, treatment) in done:
                continue
            trial = run_trial(secret, secret_path.name, treatment, rep)
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
