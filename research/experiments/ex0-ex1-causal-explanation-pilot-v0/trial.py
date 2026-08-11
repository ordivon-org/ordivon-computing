from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import time
import urllib.error
import urllib.request
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "pilot-corpus-v1.json").read_text(encoding="utf-8"))
OWNERS = ["HOST", "HARNESS", "RUNTIME", "CALLER_OR_DOMAIN"]


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def secret_paths() -> list[pathlib.Path]:
    paths = sorted(pathlib.Path("/root/.config/ordivon/secrets").glob("deepseek*.json"))
    usable = []
    for path in paths:
        value = json.loads(path.read_text(encoding="utf-8"))
        if all(isinstance(value.get(k), str) and value.get(k) for k in ("apiKey", "baseUrl", "model")):
            usable.append(path)
    if not usable:
        raise RuntimeError("no usable DeepSeek secrets")
    return usable


def submit_tool(case_ids: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "submit_comprehension",
            "description": "Submit exactly one primary authority owner for every supplied case. Choose the owner that owns the uncertain fact or final judgment asked by the scenario, not merely a component that participates nearby.",
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "answers": {
                        "type": "array",
                        "minItems": len(case_ids),
                        "maxItems": len(case_ids),
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "caseId": {"type": "string", "enum": case_ids},
                                "owner": {"type": "string", "enum": OWNERS},
                                "reason": {"type": "string", "minLength": 1, "maxLength": 700}
                            },
                            "required": ["caseId", "owner", "reason"]
                        }
                    }
                },
                "required": ["answers"]
            }
        }
    }


def call_provider(secret: dict[str, Any], treatment: str, cases: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    ids = [str(c["id"]) for c in cases]
    explanation = str(CORPUS["treatments"][treatment])
    system = (
        "You are a fresh evaluator learning an unfamiliar infrastructure from the explanation below. "
        "Do not rely on any previous Ordivon knowledge. For each scenario choose exactly one primary authority: "
        "HOST, HARNESS, RUNTIME, or CALLER_OR_DOMAIN. The question is ownership of the fact/judgment that resolves "
        "the stated uncertainty, not which components may be adjacent. Return only the required tool call.\n\n"
        "EXPLANATION:\n" + explanation
    )
    visible = [{"caseId": c["id"], "scenario": c["scenario"]} for c in cases]
    body = {
        "model": secret["model"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(visible, ensure_ascii=False, separators=(",", ":"))}
        ],
        "tools": [submit_tool(ids)],
        "tool_choice": {"type": "function", "function": {"name": "submit_comprehension"}},
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": 9000,
        "stream": False
    }
    data = canonical(body)
    attempts = []
    started = time.time_ns()
    for wire_attempt in range(1, 4):
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + str(secret["apiKey"]),
                "Content-Type": "application/json",
                "User-Agent": "ordivon-ex1-causal-explanation/1"
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                payload = json.loads(response.read(8_388_608))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            attempts.append({"attempt": wire_attempt, "kind": "transport", "error": type(exc).__name__})
            if wire_attempt == 3:
                raise
            time.sleep(0.5 * wire_attempt)
            continue
        try:
            message = payload["choices"][0]["message"]
            calls = message.get("tool_calls") or []
            if len(calls) != 1 or calls[0].get("function", {}).get("name") != "submit_comprehension":
                raise ValueError("required tool call missing or multiple")
            args = json.loads(calls[0]["function"]["arguments"])
            answers = args.get("answers")
            if not isinstance(answers, list) or len(answers) != len(ids):
                raise ValueError("answer cardinality differs")
            by_id: dict[str, dict[str, Any]] = {}
            for answer in answers:
                if not isinstance(answer, dict) or set(answer) != {"caseId", "owner", "reason"}:
                    raise ValueError("answer fields differ")
                cid = answer["caseId"]
                if cid not in ids or cid in by_id or answer["owner"] not in OWNERS or not isinstance(answer["reason"], str) or not answer["reason"]:
                    raise ValueError("answer value invalid")
                by_id[cid] = answer
            if set(by_id) != set(ids):
                raise ValueError("case coverage differs")
            usage = payload.get("usage") or {}
            return {
                "answers": [by_id[cid] for cid in ids],
                "providerModel": payload.get("model", secret["model"])
            }, {
                "promptTokens": int(usage.get("prompt_tokens", 0) or 0),
                "completionTokens": int(usage.get("completion_tokens", 0) or 0),
                "totalTokens": int(usage.get("total_tokens", 0) or 0),
                "providerCalls": wire_attempt,
                "wireCorrections": attempts,
                "elapsedMs": (time.time_ns() - started) // 1_000_000,
                "requestDigest": digest(body)
            }
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            attempts.append({"attempt": wire_attempt, "kind": "schema", "error": str(exc)[:300]})
            if wire_attempt == 3:
                raise RuntimeError(f"wire/schema-invalid after retries: {attempts}") from exc
    raise AssertionError("unreachable")


def score_trial(treatment: str, replicate: int, cases: list[dict[str, Any]], result: dict[str, Any], usage: dict[str, Any], secret_name: str) -> dict[str, Any]:
    case_map = {c["id"]: c for c in cases}
    rows = []
    for answer in result["answers"]:
        case = case_map[answer["caseId"]]
        correct = answer["owner"] == case["oracle"]
        rows.append({
            "caseId": answer["caseId"],
            "subset": case["subset"],
            "oracle": case["oracle"],
            "owner": answer["owner"],
            "temptingWrong": case["temptingWrong"],
            "correct": correct,
            "reason": answer["reason"]
        })
    return {
        "treatment": treatment,
        "replicate": replicate,
        "secretSlot": secret_name,
        "caseOrder": [c["id"] for c in cases],
        "result": rows,
        "strictCorrect": sum(1 for r in rows if r["correct"]),
        "strictTotal": len(rows),
        "usage": usage,
        "providerModel": result["providerModel"]
    }


def analyze(trials: list[dict[str, Any]]) -> dict[str, Any]:
    cases = {c["id"]: c for c in CORPUS["cases"]}
    out: dict[str, Any] = {}
    for treatment in CORPUS["treatments"]:
        selected = [t for t in trials if t["treatment"] == treatment]
        rows = [r for t in selected for r in t["result"]]
        strict = sum(1 for r in rows if r["correct"])
        total = len(rows)
        domain = [r for r in rows if r["subset"] == "semantic-overreach"]
        transfer = [r for r in rows if r["subset"] == "transfer"]
        boundary = [r for r in rows if r["subset"] == "boundary"]
        out[treatment] = {
            "strictCorrect": strict,
            "strictTotal": total,
            "accuracy": strict / total,
            "boundaryAccuracy": sum(1 for r in boundary if r["correct"]) / len(boundary),
            "domainOverreachCount": sum(1 for r in domain if r["owner"] != "CALLER_OR_DOMAIN"),
            "domainOverreachTotal": len(domain),
            "domainOverreachRate": sum(1 for r in domain if r["owner"] != "CALLER_OR_DOMAIN") / len(domain),
            "transferCorrect": sum(1 for r in transfer if r["correct"]),
            "transferTotal": len(transfer),
            "transferAccuracy": sum(1 for r in transfer if r["correct"]) / len(transfer),
            "totalTokens": sum(int(t["usage"]["totalTokens"]) for t in selected),
            "providerCalls": sum(int(t["usage"]["providerCalls"]) for t in selected)
        }
    a = out["repository_first"]
    b = out["causal_first"]
    superior = b["accuracy"] >= a["accuracy"] + 0.08 and b["domainOverreachRate"] <= a["domainOverreachRate"] and b["transferAccuracy"] >= 0.90
    ceiling = a["accuracy"] >= 0.95 and b["accuracy"] >= 0.95 and b["accuracy"] >= a["accuracy"] and b["domainOverreachRate"] <= a["domainOverreachRate"] and b["transferAccuracy"] >= 0.90
    classification = "SUPERIOR" if superior else ("CEILING_EQUIVALENT" if ceiling else "MIXED_OR_FAILED")
    paired = []
    for rep in range(1, int(CORPUS["replicates"]) + 1):
        ra = next(t for t in trials if t["replicate"] == rep and t["treatment"] == "repository_first")
        rb = next(t for t in trials if t["replicate"] == rep and t["treatment"] == "causal_first")
        paired.append({"replicate": rep, "repositoryCorrect": ra["strictCorrect"], "causalCorrect": rb["strictCorrect"], "delta": rb["strictCorrect"] - ra["strictCorrect"]})
    return {
        "treatments": out,
        "pairedReplicates": paired,
        "classification": classification,
        "caseCount": len(cases)
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "live-v1.json")
    args = parser.parse_args()
    secrets = secret_paths()
    trials = []
    for replicate in range(1, int(CORPUS["replicates"]) + 1):
        secret_path = secrets[(replicate - 1) % len(secrets)]
        secret = json.loads(secret_path.read_text(encoding="utf-8"))
        treatments = ["repository_first", "causal_first"] if replicate % 2 else ["causal_first", "repository_first"]
        for treatment in treatments:
            cases = list(CORPUS["cases"])
            random.Random(f"ex1:{replicate}:{treatment}").shuffle(cases)
            result, usage = call_provider(secret, treatment, cases)
            trials.append(score_trial(treatment, replicate, cases, result, usage, secret_path.name))
            print(json.dumps({"replicate": replicate, "treatment": treatment, "correct": trials[-1]["strictCorrect"], "total": trials[-1]["strictTotal"], "tokens": usage["totalTokens"], "calls": usage["providerCalls"]}, sort_keys=True), flush=True)
    evidence = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-comprehension-live-evidence",
        "corpusDigest": digest(CORPUS),
        "authorityFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "authority-freeze-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
        "analysis": analyze(trials)
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evidence["analysis"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
