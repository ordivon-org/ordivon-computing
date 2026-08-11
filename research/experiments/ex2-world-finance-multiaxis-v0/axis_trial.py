from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import time
import urllib.error
import urllib.request
from collections import Counter
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
CORPUS = json.loads((ROOT / "axis-corpus-v1.json").read_text(encoding="utf-8"))
AXES = list(CORPUS["axes"])


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


def axis_schema(axis: str) -> dict[str, Any]:
    values = CORPUS["axes"][axis]
    return {
        "type": "array",
        "minItems": 1,
        "maxItems": len(values),
        "uniqueItems": True,
        "items": {"type": "string", "enum": values},
    }


def tool(case_ids: list[str]) -> dict[str, Any]:
    axes_props = {axis: axis_schema(axis) for axis in AXES}
    return {
        "type": "function",
        "function": {
            "name": "submit_multiaxis",
            "description": "For every case return the exact set of labels for all five independent authority axes. Multiple labels may be simultaneously true. Do not collapse the axes into a primary owner.",
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
                                "axes": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "properties": axes_props,
                                    "required": AXES,
                                },
                                "note": {"type": "string", "minLength": 1, "maxLength": 600},
                            },
                            "required": ["caseId", "axes", "note"],
                        },
                    }
                },
                "required": ["answers"],
            },
        },
    }


def validate_axes(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict) or set(value) != set(AXES):
        raise ValueError("axis fields differ")
    result: dict[str, list[str]] = {}
    for axis in AXES:
        items = value[axis]
        allowed = set(CORPUS["axes"][axis])
        if not isinstance(items, list) or not items or len(items) != len(set(items)) or any(item not in allowed for item in items):
            raise ValueError(f"invalid axis set: {axis}")
        result[axis] = sorted(items)
    return result


def call_provider(secret: dict[str, Any], treatment: str, cases: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    ids = [c["id"] for c in cases]
    definitions = "\n".join(f"- {axis}: {CORPUS['axisDefinitions'][axis]}" for axis in AXES)
    system = (
        "You are a fresh evaluator learning an unfamiliar Agent infrastructure. Learn only from the supplied explanation. "
        "For each scenario answer all five independent axes as exact SETS. Multiple labels can be true simultaneously. "
        "Do not infer a stronger authority from mere storage, execution, mapping, or proximity. Return only the required tool call.\n\n"
        "AXIS DEFINITIONS:\n" + definitions + "\n\nEXPLANATION:\n" + CORPUS["treatments"][treatment]
    )
    visible = [{"caseId": c["id"], "scenario": c["scenario"]} for c in cases]
    body = {
        "model": secret["model"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(visible, ensure_ascii=False, separators=(",", ":"))},
        ],
        "tools": [tool(ids)],
        "tool_choice": {"type": "function", "function": {"name": "submit_multiaxis"}},
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": 14000,
        "stream": False,
    }
    data = canonical(body)
    corrections: list[dict[str, Any]] = []
    started = time.time_ns()
    for attempt in range(1, 4):
        req = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=data,
            headers={
                "Authorization": "Bearer " + str(secret["apiKey"]),
                "Content-Type": "application/json",
                "User-Agent": "ordivon-ex2-multiaxis/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                payload = json.loads(response.read(12_000_000))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            corrections.append({"attempt": attempt, "kind": "transport", "error": type(exc).__name__})
            if attempt == 3:
                raise
            time.sleep(0.5 * attempt)
            continue
        try:
            calls = payload["choices"][0]["message"].get("tool_calls") or []
            if len(calls) != 1 or calls[0].get("function", {}).get("name") != "submit_multiaxis":
                raise ValueError("required tool call missing or multiple")
            args = json.loads(calls[0]["function"]["arguments"])
            answers = args.get("answers")
            if not isinstance(answers, list) or len(answers) != len(ids):
                raise ValueError("answer cardinality differs")
            by_id: dict[str, dict[str, Any]] = {}
            for answer in answers:
                if not isinstance(answer, dict) or set(answer) != {"caseId", "axes", "note"}:
                    raise ValueError("answer fields differ")
                cid = answer["caseId"]
                if cid not in ids or cid in by_id or not isinstance(answer["note"], str) or not answer["note"]:
                    raise ValueError("answer value invalid")
                by_id[cid] = {"caseId": cid, "axes": validate_axes(answer["axes"]), "note": answer["note"]}
            if set(by_id) != set(ids):
                raise ValueError("case coverage differs")
            usage = payload.get("usage") or {}
            return {
                "answers": [by_id[cid] for cid in ids],
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
    case_map = {c["id"]: c for c in cases}
    rows = []
    for answer in result["answers"]:
        case = case_map[answer["caseId"]]
        axis_results = {}
        all_correct = True
        for axis in AXES:
            oracle = sorted(case["oracle"][axis])
            observed = sorted(answer["axes"][axis])
            correct = observed == oracle
            all_correct = all_correct and correct
            axis_results[axis] = {"oracle": oracle, "observed": observed, "correct": correct}
        rows.append({
            "caseId": case["id"],
            "subset": case["subset"],
            "axes": axis_results,
            "caseExact": all_correct,
            "note": answer["note"],
        })
    return {
        "treatment": treatment,
        "replicate": replicate,
        "secretSlot": secret_name,
        "caseOrder": [c["id"] for c in cases],
        "result": rows,
        "axisCorrect": sum(1 for r in rows for a in AXES if r["axes"][a]["correct"]),
        "axisTotal": len(rows) * len(AXES),
        "caseExact": sum(1 for r in rows if r["caseExact"]),
        "caseTotal": len(rows),
        "usage": usage,
        "providerModel": result["providerModel"],
    }


def analyze(trials: list[dict[str, Any]]) -> dict[str, Any]:
    critical = set(CORPUS["metrics"]["criticalExternalEffectCases"])
    carrier = set(CORPUS["metrics"]["worldHostCarrierCases"])
    minimality = set(CORPUS["metrics"]["minimalityCases"])
    out: dict[str, Any] = {}
    for treatment in CORPUS["treatments"]:
        selected = [t for t in trials if t["treatment"] == treatment]
        rows = [r for t in selected for r in t["result"]]
        axis_correct = sum(1 for r in rows for a in AXES if r["axes"][a]["correct"])
        axis_total = len(rows) * len(AXES)
        case_exact = sum(1 for r in rows if r["caseExact"])
        per_axis = {}
        for axis in AXES:
            per_axis[axis] = {
                "correct": sum(1 for r in rows if r["axes"][axis]["correct"]),
                "total": len(rows),
            }
            per_axis[axis]["accuracy"] = per_axis[axis]["correct"] / per_axis[axis]["total"]
        crit_rows = [r for r in rows if r["caseId"] in critical]
        carrier_rows = [r for r in rows if r["caseId"] in carrier]
        min_rows = [r for r in rows if r["caseId"] in minimality]
        out[treatment] = {
            "axisCorrect": axis_correct,
            "axisTotal": axis_total,
            "axisExact": axis_correct / axis_total,
            "caseExactCorrect": case_exact,
            "caseTotal": len(rows),
            "caseExact": case_exact / len(rows),
            "perAxis": per_axis,
            "criticalExternalEffectExact": sum(1 for r in crit_rows if r["axes"]["externalEffectTruth"]["correct"]) / len(crit_rows),
            "worldHostCarrierDurableExact": sum(1 for r in carrier_rows if r["axes"]["durableStructuralState"]["correct"]) / len(carrier_rows),
            "minimalitySharingExact": sum(1 for r in min_rows if r["axes"]["sharingDisposition"]["correct"]) / len(min_rows),
            "totalTokens": sum(t["usage"]["totalTokens"] for t in selected),
            "providerCalls": sum(t["usage"]["providerCalls"] for t in selected),
        }
    a = out["compact_responsibility"]
    b = out["explicit_five_axis"]
    supported = (
        b["axisExact"] >= a["axisExact"] + 0.05
        and b["caseExact"] >= a["caseExact"] + 0.05
        and b["criticalExternalEffectExact"] >= 0.98
        and b["minimalitySharingExact"] >= 0.90
    )
    safe = (
        b["axisExact"] >= 0.97
        and b["axisExact"] >= a["axisExact"] - 0.01
        and b["criticalExternalEffectExact"] == 1.0
        and b["minimalitySharingExact"] >= a["minimalitySharingExact"]
    )
    classification = "MULTIAXIS_SUPPORTED" if supported else ("SAFE_NONINFERIOR" if safe else "REJECT_OR_REVISE")
    errors: dict[str, Any] = {}
    for treatment in CORPUS["treatments"]:
        counter = Counter()
        for t in trials:
            if t["treatment"] != treatment:
                continue
            for row in t["result"]:
                for axis in AXES:
                    if not row["axes"][axis]["correct"]:
                        counter[(row["caseId"], axis)] += 1
        errors[treatment] = [
            {"caseId": cid, "axis": axis, "count": count}
            for (cid, axis), count in counter.most_common()
        ]
    return {
        "treatments": out,
        "classification": classification,
        "pairedReplicates": [
            {
                "replicate": rep,
                "compactAxisCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_responsibility")["axisCorrect"],
                "fiveAxisCorrect": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "explicit_five_axis")["axisCorrect"],
                "compactCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "compact_responsibility")["caseExact"],
                "fiveAxisCaseExact": next(t for t in trials if t["replicate"] == rep and t["treatment"] == "explicit_five_axis")["caseExact"],
            }
            for rep in range(1, int(CORPUS["replicates"]) + 1)
        ],
        "errorProfile": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "axis-live-v1.json")
    args = parser.parse_args()
    secrets = secret_paths()
    trials = []
    for replicate in range(1, int(CORPUS["replicates"]) + 1):
        secret_path = secrets[(replicate - 1) % len(secrets)]
        secret = json.loads(secret_path.read_text(encoding="utf-8"))
        order = ["compact_responsibility", "explicit_five_axis"] if replicate % 2 else ["explicit_five_axis", "compact_responsibility"]
        for treatment in order:
            cases = list(CORPUS["cases"])
            random.Random(f"ex2-axis:{replicate}:{treatment}").shuffle(cases)
            result, usage = call_provider(secret, treatment, cases)
            trial = score_trial(treatment, replicate, cases, result, usage, secret_path.name)
            trials.append(trial)
            print(json.dumps({
                "replicate": replicate,
                "treatment": treatment,
                "axisCorrect": trial["axisCorrect"],
                "axisTotal": trial["axisTotal"],
                "caseExact": trial["caseExact"],
                "caseTotal": trial["caseTotal"],
                "tokens": usage["totalTokens"],
                "calls": usage["providerCalls"],
            }, sort_keys=True), flush=True)
    evidence = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-five-axis-live-evidence",
        "corpusDigest": digest(CORPUS),
        "authorityFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "authority-freeze-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
        "analysis": analyze(trials),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(evidence["analysis"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
