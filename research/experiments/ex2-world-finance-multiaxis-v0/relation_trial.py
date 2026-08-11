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
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "relation-corpus-v1.json").read_text(encoding="utf-8"))
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
    "PROMOTION_STATUS": "promotion",
    "DOES_NOT_IMPLY": "negativeInference",
}


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def secret_paths() -> list[pathlib.Path]:
    out = []
    for path in sorted(pathlib.Path("/root/.config/ordivon/secrets").glob("deepseek*.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if all(isinstance(value.get(k), str) and value[k] for k in ("apiKey", "baseUrl", "model")):
            out.append(path)
    if not out:
        raise RuntimeError("no usable DeepSeek secret")
    return out


def query_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for case in cases:
        for query in case["queries"]:
            rows.append({
                "queryId": f"{case['id']}.{query['q']}",
                "caseId": case["id"],
                "relation": query["relation"],
                "oracle": query["answer"],
            })
    return rows


def allowed_targets(relation: str) -> set[str]:
    return set(CORPUS["labels"][TARGET_DOMAIN[relation]])


def call_provider(secret: dict[str, Any], treatment: str, cases: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = query_rows(cases)
    ids = [row["queryId"] for row in rows]
    row_by_id = {row["queryId"]: row for row in rows}
    relation_guide = "\n".join(f"- {name}: {description}" for name, description in CORPUS["relationTypes"].items())
    visible_cases = []
    for case in cases:
        visible_cases.append({
            "caseId": case["id"],
            "scenario": case["scenario"],
            "queries": [
                {
                    "queryId": f"{case['id']}.{query['q']}",
                    "relation": query["relation"],
                    "question": CORPUS["relationTypes"][query["relation"]],
                }
                for query in case["queries"]
            ],
        })
    system = (
        "You are a fresh evaluator learning an unfamiliar Agent infrastructure. Learn only from the explanation. "
        "Answer each explicitly listed relation query and ONLY that relation. Do not fill latent ownership fields that were not asked. "
        "A state-contract owner can differ from its persistence carrier; native occurrence can differ from local process proof and from mapped/derived facts; semantic home, mechanical delegation, and promotion status are distinct. Return only the required tool call.\n\n"
        "RELATION DEFINITIONS:\n" + relation_guide + "\n\nEXPLANATION:\n" + CORPUS["treatments"][treatment]
    )
    answer_properties = {}
    for row in rows:
        relation = row["relation"]
        answer_properties[row["queryId"]] = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "target": {"type": "string", "enum": sorted(allowed_targets(relation))},
                "reason": {"type": "string", "minLength": 1, "maxLength": 600},
            },
            "required": ["target", "reason"],
        }
    tool = {
        "type": "function",
        "function": {
            "name": "submit_relations",
            "description": "Return exactly one typed target for every explicitly listed relation query.",
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "answers": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": answer_properties,
                        "required": ids,
                    }
                },
                "required": ["answers"],
            },
        },
    }
    body = {
        "model": secret["model"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(visible_cases, ensure_ascii=False, separators=(",", ":"))},
        ],
        "tools": [tool],
        "tool_choice": {"type": "function", "function": {"name": "submit_relations"}},
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": 14000,
        "stream": False,
    }
    data = canonical(body)
    corrections = []
    started = time.time_ns()
    for attempt in range(1, 4):
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + secret["apiKey"],
                "Content-Type": "application/json",
                "User-Agent": "ordivon-ex2-relations/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                payload = json.loads(response.read(12_000_000))
        except (urllib.error.URLError, TimeoutError, OSError, http.client.IncompleteRead) as exc:
            corrections.append({"attempt": attempt, "kind": "transport", "error": type(exc).__name__})
            if attempt == 3:
                raise
            time.sleep(0.5 * attempt)
            continue
        try:
            calls = payload["choices"][0]["message"].get("tool_calls") or []
            if len(calls) != 1 or calls[0].get("function", {}).get("name") != "submit_relations":
                raise ValueError("required tool call missing or multiple")
            args = json.loads(calls[0]["function"]["arguments"])
            answers = args.get("answers")
            if not isinstance(answers, dict) or set(answers) != set(ids):
                raise ValueError("query coverage differs")
            by_id = {}
            for qid, answer in answers.items():
                if not isinstance(answer, dict) or set(answer) != {"target", "reason"}:
                    raise ValueError("answer fields differ")
                if not isinstance(answer["reason"], str) or not answer["reason"]:
                    raise ValueError("answer value invalid")
                relation = row_by_id[qid]["relation"]
                if answer["target"] not in allowed_targets(relation):
                    raise ValueError(f"target invalid for relation {relation}: {answer['target']}")
                by_id[qid] = {"queryId": qid, **answer}
            usage = payload.get("usage") or {}
            return {
                "answers": [by_id[qid] for qid in ids],
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
            if attempt == 3:
                raise RuntimeError(f"wire/schema-invalid after retries: {corrections}") from exc
    raise AssertionError("unreachable")


def score_trial(treatment: str, replicate: int, cases: list[dict[str, Any]], result: dict[str, Any], usage: dict[str, Any], secret_name: str) -> dict[str, Any]:
    rows = query_rows(cases)
    by_id = {answer["queryId"]: answer for answer in result["answers"]}
    scored = []
    for row in rows:
        answer = by_id[row["queryId"]]
        scored.append({
            **row,
            "observed": answer["target"],
            "correct": answer["target"] == row["oracle"],
            "reason": answer["reason"],
        })
    case_ids = [case["id"] for case in cases]
    return {
        "treatment": treatment,
        "replicate": replicate,
        "secretSlot": secret_name,
        "caseOrder": case_ids,
        "result": scored,
        "queryCorrect": sum(1 for row in scored if row["correct"]),
        "queryTotal": len(scored),
        "caseExact": sum(1 for cid in case_ids if all(row["correct"] for row in scored if row["caseId"] == cid)),
        "caseTotal": len(case_ids),
        "usage": usage,
        "providerModel": result["providerModel"],
    }


def analyze(trials: list[dict[str, Any]]) -> dict[str, Any]:
    critical = set(CORPUS["metrics"]["criticalNativeFactCases"])
    carrier = set(CORPUS["metrics"]["ownerCarrierCases"])
    minimality = set(CORPUS["metrics"]["minimalityCases"])
    out = {}
    for treatment in CORPUS["treatments"]:
        selected = [t for t in trials if t["treatment"] == treatment]
        rows = [row for t in selected for row in t["result"]]
        q_correct = sum(1 for row in rows if row["correct"])
        case_pairs = [(t, cid) for t in selected for cid in t["caseOrder"]]
        case_exact = sum(1 for t, cid in case_pairs if all(row["correct"] for row in t["result"] if row["caseId"] == cid))
        crit = [row for row in rows if row["caseId"] in critical and row["relation"] == "PROVES_NATIVE_FACT"]
        carrier_rows = [(t, cid) for t in selected for cid in carrier]
        min_rows = [(t, cid) for t in selected for cid in minimality]
        per_relation = {}
        for relation in CORPUS["relationTypes"]:
            rr = [row for row in rows if row["relation"] == relation]
            if rr:
                per_relation[relation] = {
                    "correct": sum(1 for row in rr if row["correct"]),
                    "total": len(rr),
                    "accuracy": sum(1 for row in rr if row["correct"]) / len(rr),
                }
        out[treatment] = {
            "queryCorrect": q_correct,
            "queryTotal": len(rows),
            "queryExact": q_correct / len(rows),
            "caseExactCorrect": case_exact,
            "caseTotal": len(case_pairs),
            "caseExact": case_exact / len(case_pairs),
            "criticalNativeFact": sum(1 for row in crit if row["correct"]) / len(crit),
            "ownerCarrier": sum(1 for t, cid in carrier_rows if all(row["correct"] for row in t["result"] if row["caseId"] == cid)) / len(carrier_rows),
            "minimality": sum(1 for t, cid in min_rows if all(row["correct"] for row in t["result"] if row["caseId"] == cid)) / len(min_rows),
            "perRelation": per_relation,
            "totalTokens": sum(t["usage"]["totalTokens"] for t in selected),
            "providerCalls": sum(t["usage"]["providerCalls"] for t in selected),
        }
    a = out["compact_responsibility"]
    b = out["typed_relations"]
    supported = (
        b["queryExact"] >= a["queryExact"] + 0.05
        and b["caseExact"] >= 0.90
        and b["criticalNativeFact"] >= 0.98
        and b["ownerCarrier"] >= 0.95
        and b["minimality"] >= 0.90
    )
    safe = (
        b["queryExact"] >= 0.95
        and b["queryExact"] >= a["queryExact"] - 0.01
        and b["criticalNativeFact"] == 1.0
        and b["ownerCarrier"] >= a["ownerCarrier"]
        and b["minimality"] >= a["minimality"]
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
            {"queryId": qid, "relation": rel, "oracle": oracle, "observed": observed, "count": count}
            for (qid, rel, oracle, observed), count in counter.most_common()
        ]
    return {
        "treatments": out,
        "classification": "RELATIONS_SUPPORTED" if supported else ("SAFE_NONINFERIOR" if safe else "REJECT_OR_REVISE"),
        "pairedReplicates": [
            {
                "replicate": rep,
                "compactQueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_responsibility")["queryCorrect"],
                "relationQueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "typed_relations")["queryCorrect"],
                "compactCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_responsibility")["caseExact"],
                "relationCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "typed_relations")["caseExact"],
            }
            for rep in range(1, int(CORPUS["replicates"]) + 1)
        ],
        "errorProfile": errors,
    }


def persist(path: pathlib.Path, trials: list[dict[str, Any]], complete: bool) -> None:
    document = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-relation-live-evidence",
        "complete": complete,
        "corpusDigest": digest(CORPUS),
        "authorityFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "authority-freeze-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
    }
    if complete:
        document["analysis"] = analyze(trials)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "relation-live-v1.json")
    args = parser.parse_args()
    trials = []
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if existing.get("corpusDigest") != digest(CORPUS):
            raise RuntimeError("existing evidence corpus differs")
        trials = list(existing.get("trials", []))
    done = {(int(t["replicate"]), str(t["treatment"])) for t in trials}
    secrets = secret_paths()
    for replicate in range(1, int(CORPUS["replicates"]) + 1):
        secret_path = secrets[(replicate - 1) % len(secrets)]
        secret = json.loads(secret_path.read_text(encoding="utf-8"))
        order = ["compact_responsibility", "typed_relations"] if replicate % 2 else ["typed_relations", "compact_responsibility"]
        for treatment in order:
            if (replicate, treatment) in done:
                continue
            cases = list(CORPUS["cases"])
            random.Random(f"ex2-rel:{replicate}:{treatment}").shuffle(cases)
            result, usage = call_provider(secret, treatment, cases)
            trial = score_trial(treatment, replicate, cases, result, usage, secret_path.name)
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
