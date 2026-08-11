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


def call_provider(secret: dict[str, Any], treatment: str, cases: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = query_rows(cases)
    ids = [row["queryId"] for row in rows]
    row_by_id = {row["queryId"]: row for row in rows}
    visible = []
    for case in cases:
        visible.append({
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
    answer_properties = {}
    for row in rows:
        allowed = CORPUS["targetDomains"][row["relation"]]
        answer_properties[row["queryId"]] = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "target": {"type": "string", "enum": allowed},
                "reason": {"type": "string", "minLength": 1, "maxLength": 500},
            },
            "required": ["target", "reason"],
        }
    tool = {
        "type": "function",
        "function": {
            "name": "submit_family_relations",
            "description": "Answer exactly the named responsibility relation queries. Project labels name project-owned contracts/derivations only; SEMANTIC_JUDGE and native-fact labels are role-pure.",
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
    relation_guide = "\n".join(f"- {name}: {desc}" for name, desc in CORPUS["relationTypes"].items())
    system = (
        "You are a fresh evaluator learning an unfamiliar multi-project Agent system. Learn only from the explanation below. "
        "Answer ONLY the explicitly named relation queries. Never replace a project contract owner with a generic human/native role, or a generic human/native role with a project merely because the project studies that domain. "
        "Return only the required tool call.\n\nRELATIONS:\n" + relation_guide + "\n\nEXPLANATION:\n" + CORPUS["treatments"][treatment]
    )
    body = {
        "model": secret["model"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(visible, ensure_ascii=False, separators=(",", ":"))},
        ],
        "tools": [tool],
        "tool_choice": {"type": "function", "function": {"name": "submit_family_relations"}},
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": 5000,
        "stream": False,
    }
    data = canonical(body)
    corrections: list[dict[str, Any]] = []
    started = time.time_ns()
    for attempt in range(1, 5):
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + secret["apiKey"],
                "Content-Type": "application/json",
                "User-Agent": "ordivon-ex2-family2/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                payload = json.loads(response.read(8_000_000))
        except (urllib.error.URLError, TimeoutError, OSError, http.client.IncompleteRead) as exc:
            corrections.append({"attempt": attempt, "kind": "transport", "error": type(exc).__name__})
            if attempt == 4:
                raise
            time.sleep(0.6 * attempt)
            continue
        try:
            calls = payload["choices"][0]["message"].get("tool_calls") or []
            if len(calls) != 1 or calls[0].get("function", {}).get("name") != "submit_family_relations":
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
                    raise ValueError("answer reason invalid")
                row = row_by_id[qid]
                if answer["target"] not in CORPUS["targetDomains"][row["relation"]]:
                    raise ValueError(f"target invalid for relation {row['relation']}: {answer['target']}")
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
            if attempt == 4:
                raise RuntimeError(f"wire/schema-invalid after retries: {corrections}") from exc
            time.sleep(0.3 * attempt)
    raise AssertionError("unreachable")


def score_chunk(cases: list[dict[str, Any]], result: dict[str, Any]) -> list[dict[str, Any]]:
    rows = query_rows(cases)
    by_id = {answer["queryId"]: answer for answer in result["answers"]}
    return [
        {
            **row,
            "observed": by_id[row["queryId"]]["target"],
            "correct": by_id[row["queryId"]]["target"] == row["oracle"],
            "reason": by_id[row["queryId"]]["reason"],
        }
        for row in rows
    ]


def run_trial(secret: dict[str, Any], secret_name: str, treatment: str, replicate: int) -> dict[str, Any]:
    cases = list(CORPUS["cases"])
    random.Random(f"ex2-family2:{replicate}:{treatment}").shuffle(cases)
    chunks = [cases[i:i + 2] for i in range(0, len(cases), 2)]
    results_by_index: dict[int, tuple[list[dict[str, Any]], dict[str, Any], str, list[str]]] = {}
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(call_provider, secret, treatment, chunk): (index, chunk)
            for index, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            index, chunk = futures[future]
            result, usage = future.result()
            results_by_index[index] = (score_chunk(chunk, result), usage, result["providerModel"], [c["id"] for c in chunk])
    scored_rows: list[dict[str, Any]] = []
    case_order: list[str] = []
    models = []
    usage_total = {
        "promptTokens": 0,
        "completionTokens": 0,
        "totalTokens": 0,
        "providerCalls": 0,
        "elapsedMs": 0,
        "wireCorrections": [],
        "requestDigests": [],
    }
    for index in range(len(chunks)):
        rows, usage, model, ids = results_by_index[index]
        scored_rows.extend(rows)
        case_order.extend(ids)
        models.append(model)
        for key in ("promptTokens", "completionTokens", "totalTokens", "providerCalls", "elapsedMs"):
            usage_total[key] += int(usage[key])
        usage_total["wireCorrections"].append({"chunk": index, "corrections": usage["wireCorrections"]})
        usage_total["requestDigests"].append(usage["requestDigest"])
    if len(set(models)) != 1:
        raise RuntimeError(f"provider model drift across chunks: {models}")
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
        "providerModel": models[0],
        "chunkCount": len(chunks),
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
        query_correct = sum(r["correct"] for r in rows)
        case_pairs = [(t, cid) for t in selected for cid in t["caseOrder"]]
        case_exact = sum(all(r["correct"] for r in t["result"] if r["caseId"] == cid) for t, cid in case_pairs)
        neg_rows = [r for r in rows if r["caseId"] in negative and r["relation"] == "DOES_NOT_IMPLY"]
        promo_rows = [r for r in rows if r["caseId"] in promotion and r["relation"] == "SHARED_PROMOTION"]
        per_relation = {}
        for relation in CORPUS["relationTypes"]:
            rr = [r for r in rows if r["relation"] == relation]
            if rr:
                correct = sum(r["correct"] for r in rr)
                per_relation[relation] = {"correct": correct, "total": len(rr), "accuracy": correct / len(rr)}
        out[treatment] = {
            "queryCorrect": query_correct,
            "queryTotal": len(rows),
            "queryExact": query_correct / len(rows),
            "caseExactCorrect": case_exact,
            "caseTotal": len(case_pairs),
            "caseExact": case_exact / len(case_pairs),
            "infrastructure": group_case_exact(selected, infra),
            "domain": group_case_exact(selected, domain),
            "negative": sum(r["correct"] for r in neg_rows) / len(neg_rows),
            "promotion": sum(r["correct"] for r in promo_rows) / len(promo_rows),
            "perRelation": per_relation,
            "totalTokens": sum(t["usage"]["totalTokens"] for t in selected),
            "providerCalls": sum(t["usage"]["providerCalls"] for t in selected),
        }
    a = out["compact_family"]
    b = out["role_pure_family"]
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
                "rolePureQueryCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "role_pure_family")["queryCorrect"],
                "compactCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_family")["caseExact"],
                "rolePureCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "role_pure_family")["caseExact"],
            }
            for rep in range(1, CORPUS["replicates"] + 1)
        ],
        "errorProfile": errors,
    }


def persist(path: pathlib.Path, trials: list[dict[str, Any]], complete: bool) -> None:
    document = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-family2-live-evidence",
        "complete": complete,
        "corpusDigest": digest(CORPUS),
        "familyFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "family-authority-freeze-v1.json").read_bytes()).hexdigest(),
        "familyRelationsDigest": "sha256:" + hashlib.sha256((ROOT / "family-relations-v1.json").read_bytes()).hexdigest(),
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
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "family2-live-v1.json")
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
        order = ["compact_family", "role_pure_family"] if rep % 2 else ["role_pure_family", "compact_family"]
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
