from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
BATTLEFIELD = ROOT / "battlefield-v2.json"
SECRETS = sorted(Path("/root/.config/ordivon/secrets").glob("deepseek*.json"))
DECISIONS = [
    "ACT_UNBOUND",
    "ACT_WITH_PLANNING_BINDING",
    "HOLD",
    "REOBSERVE_THEN_DECIDE",
    "REBASE_AND_ACT",
    "REPLAY_EXACT",
]
DISPOSITIONS = [
    "would_commit",
    "would_conflict_not_committed",
    "would_replay_existing",
    "would_hold",
    "requires_reobservation",
    "uncertain",
]
_PRINT_LOCK = threading.Lock()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def submit_tool() -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": "submit",
            "description": "Submit one consequence decision. This ends the trial.",
            "parameters": {
                "type": "object",
                "properties": {
                    "decision": {"type": "string", "enum": DECISIONS},
                    "bindingBasis": {"type": "string"},
                    "predictedOwnerDisposition": {"type": "string", "enum": DISPOSITIONS},
                    "wouldCreateNewConsequence": {"type": "boolean"},
                    "rationale": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": [
                    "decision",
                    "bindingBasis",
                    "predictedOwnerDisposition",
                    "wouldCreateNewConsequence",
                    "rationale",
                    "confidence",
                ],
                "additionalProperties": False,
            },
        },
    }


def load_secret(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def call_model(messages: list[dict[str, str]], secret_path: Path, *, max_tokens: int = 5000) -> tuple[dict[str, Any], dict[str, int]]:
    secret = load_secret(secret_path)
    body = {
        "model": secret["model"],
        "messages": messages,
        "tools": [submit_tool()],
        "tool_choice": "required",
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": max_tokens,
        "stream": False,
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    protocol_retries = 0
    transport_retries = 0
    input_tokens = output_tokens = total_tokens = elapsed_ms = 0
    while True:
        started = time.time_ns()
        request = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=encoded,
            headers={
                "Authorization": "Bearer " + str(secret["apiKey"]),
                "Content-Type": "application/json",
                "User-Agent": "ordivon-computing-hp4/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                raw = response.read(4_194_304)
        except (urllib.error.URLError, TimeoutError, OSError):
            transport_retries += 1
            if transport_retries > 2:
                raise
            time.sleep(0.5 * transport_retries)
            continue
        elapsed_ms += (time.time_ns() - started) // 1_000_000
        payload = json.loads(raw)
        usage = payload.get("usage") or {}
        input_tokens += int(usage.get("prompt_tokens", 0) or 0)
        output_tokens += int(usage.get("completion_tokens", 0) or 0)
        total_tokens += int(usage.get("total_tokens", 0) or 0)
        try:
            message = payload["choices"][0]["message"]
            calls = message.get("tool_calls")
            if not isinstance(calls, list) or len(calls) != 1:
                raise ValueError("expected exactly one submit Tool call")
            function = calls[0].get("function")
            if not isinstance(function, dict) or function.get("name") != "submit":
                raise ValueError("expected submit Tool call")
            arguments = json.loads(str(function.get("arguments", "")))
            if not isinstance(arguments, dict):
                raise ValueError("submit arguments must be object")
            if arguments.get("decision") not in DECISIONS:
                raise ValueError("invalid decision")
            if arguments.get("predictedOwnerDisposition") not in DISPOSITIONS:
                raise ValueError("invalid predicted disposition")
            return arguments, {
                "inputTokens": input_tokens,
                "outputTokens": output_tokens,
                "totalTokens": total_tokens,
                "elapsedMs": elapsed_ms,
                "transportRetries": transport_retries,
                "providerProtocolRetries": protocol_retries,
                "providerCalls": protocol_retries + 1,
            }
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            protocol_retries += 1
            diag = ROOT / "diagnostics" / "provider-protocol.jsonl"
            diag.parent.mkdir(parents=True, exist_ok=True)
            with _PRINT_LOCK, diag.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "error": str(error),
                    "secret": secret_path.name,
                    "messagesDigest": canonical_digest(messages),
                    "raw": payload.get("choices"),
                }, ensure_ascii=False) + "\n")
            if protocol_retries > 2:
                raise


def visible_scenario(scenario: dict[str, Any], treatment: str) -> dict[str, Any]:
    result = {
        "scenarioId": scenario["id"],
        "owner": scenario["owner"],
        "planningEvidence": scenario["planningEvidence"],
        "intendedConsequence": scenario["intendedConsequence"],
        "ownerActionContract": scenario["ownerActionContract"],
        "decisionCatalog": DECISIONS,
    }
    if treatment == "generic_change":
        result["consequenceBoundaryEvidence"] = scenario["genericSignal"]
    elif treatment == "owner_native":
        result["consequenceBoundaryEvidence"] = scenario["ownerNativeEvidence"]
    elif treatment != "stale_evidence":
        raise ValueError(treatment)
    return result


def expected_disposition(scenario: dict[str, Any], decision: str) -> str | None:
    cls = scenario["hiddenOracle"]["class"]
    if decision == "HOLD":
        return "would_hold"
    if decision == "REOBSERVE_THEN_DECIDE":
        return "requires_reobservation"
    if decision == "ACT_WITH_PLANNING_BINDING":
        if "replay" in cls:
            return "would_replay_existing"
        return "would_conflict_not_committed"
    if decision == "REPLAY_EXACT":
        if "replay" in cls:
            return "would_replay_existing"
        return None
    if decision == "REBASE_AND_ACT":
        return "would_commit"
    if decision == "ACT_UNBOUND":
        if scenario["owner"].startswith("Runtime"):
            return "would_commit"
        return None
    return None


def score(scenario: dict[str, Any], treatment: str, submission: dict[str, Any]) -> dict[str, Any]:
    decision = str(submission["decision"])
    oracle = scenario["hiddenOracle"]
    false_consequence = decision in oracle["falseConsequenceDecisions"]
    unnecessary_hold = decision in oracle["unnecessaryHoldDecisions"]
    progress_correct = decision in oracle["progressDecisions"]
    safe_conflict = decision in oracle["safeButConflictDecisions"]
    exact_replay_correct = bool(oracle["exactReplayRequired"] and decision == "REPLAY_EXACT")
    authority_safe = not false_consequence and decision != "ACT_UNBOUND"
    binding_used = decision in {
        "ACT_WITH_PLANNING_BINDING",
        "REOBSERVE_THEN_DECIDE",
        "REBASE_AND_ACT",
        "REPLAY_EXACT",
    }
    predicted = expected_disposition(scenario, decision)
    disposition_correct = predicted is None or submission["predictedOwnerDisposition"] == predicted
    semantic_accepted = bool(progress_correct and authority_safe and disposition_correct)
    return {
        "semanticAccepted": semantic_accepted,
        "falseConsequence": false_consequence,
        "duplicateOrOverwriteRisk": bool(false_consequence and oracle["exactReplayRequired"]),
        "unnecessaryHold": unnecessary_hold,
        "progressCorrect": progress_correct,
        "safeConflictOnly": safe_conflict,
        "exactReplayCorrect": exact_replay_correct,
        "authoritySafe": authority_safe,
        "ownerBindingUsed": binding_used,
        "predictedDispositionCorrect": disposition_correct,
        "treatment": treatment,
    }


def trial_messages(scenario: dict[str, Any], treatment: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You are deciding one consequence at an owner authority boundary. The owner action contract and evidence in the user payload are exact for this trial. "
                "Optimize lexicographically: first prevent a false, duplicate, or overwrite consequence; second preserve useful progress rather than holding forever; third minimize extra coordination. "
                "Do not infer semantic change from a revision number alone, and do not infer applicability merely because planning-time evidence was once correct. "
                "Do not invent an API not listed by the owner contract. Choose exactly one decision from decisionCatalog and submit it."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(visible_scenario(scenario, treatment), ensure_ascii=False),
        },
    ]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def run_one(scenario: dict[str, Any], treatment: str, replicate: int, secret_path: Path) -> dict[str, Any]:
    progress = ROOT / "evidence" / "progress" / f"{scenario['id'].lower()}-{treatment}-r{replicate}.json"
    if progress.exists():
        return json.loads(progress.read_text())
    messages = trial_messages(scenario, treatment)
    submission, usage = call_model(messages, secret_path)
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.hp4-binding-concurrency-trial",
        "scenario": scenario["id"],
        "owner": scenario["owner"],
        "treatment": treatment,
        "replicate": replicate,
        "submission": submission,
        "metrics": score(scenario, treatment, submission),
        "usage": usage,
        "visibleContextDigest": canonical_digest(visible_scenario(scenario, treatment)),
        "secretSlot": secret_path.name,
    }
    write_json(progress, result)
    with _PRINT_LOCK:
        print(json.dumps({
            "scenario": scenario["id"],
            "treatment": treatment,
            "replicate": replicate,
            "decision": submission["decision"],
            "accepted": result["metrics"]["semanticAccepted"],
            "tokens": usage["totalTokens"],
        }, ensure_ascii=False), flush=True)
    return result


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for treatment in ["stale_evidence", "generic_change", "owner_native"]:
        group = [r for r in records if r["treatment"] == treatment]
        result[treatment] = {
            "trials": len(group),
            "semanticAccepted": sum(bool(r["metrics"]["semanticAccepted"]) for r in group),
            "falseConsequences": sum(bool(r["metrics"]["falseConsequence"]) for r in group),
            "duplicateOrOverwriteRisk": sum(bool(r["metrics"]["duplicateOrOverwriteRisk"]) for r in group),
            "unnecessaryHolds": sum(bool(r["metrics"]["unnecessaryHold"]) for r in group),
            "progressCorrect": sum(bool(r["metrics"]["progressCorrect"]) for r in group),
            "safeConflictOnly": sum(bool(r["metrics"]["safeConflictOnly"]) for r in group),
            "exactReplayCorrect": sum(bool(r["metrics"]["exactReplayCorrect"]) for r in group),
            "authoritySafe": sum(bool(r["metrics"]["authoritySafe"]) for r in group),
            "ownerBindingUsed": sum(bool(r["metrics"]["ownerBindingUsed"]) for r in group),
            "predictedDispositionCorrect": sum(bool(r["metrics"]["predictedDispositionCorrect"]) for r in group),
            "providerTokens": sum(int(r["usage"]["totalTokens"]) for r in group),
            "providerCalls": sum(int(r["usage"]["providerCalls"]) for r in group),
            "meanTokens": sum(int(r["usage"]["totalTokens"]) for r in group) / len(group),
        }
    by_scenario: dict[str, Any] = {}
    for scenario in sorted({r["scenario"] for r in records}):
        by_scenario[scenario] = {}
        for treatment in ["stale_evidence", "generic_change", "owner_native"]:
            group = [r for r in records if r["scenario"] == scenario and r["treatment"] == treatment]
            by_scenario[scenario][treatment] = {
                "accepted": sum(bool(r["metrics"]["semanticAccepted"]) for r in group),
                "falseConsequences": sum(bool(r["metrics"]["falseConsequence"]) for r in group),
                "unnecessaryHolds": sum(bool(r["metrics"]["unnecessaryHold"]) for r in group),
                "decisions": [r["submission"]["decision"] for r in group],
            }
    result["byScenario"] = by_scenario
    return result


def deterministic_baselines(battlefield: dict[str, Any]) -> dict[str, Any]:
    baselines: dict[str, Any] = {}
    policies = {
        "always_unbound_act": lambda s: "ACT_UNBOUND",
        "always_hold": lambda s: "HOLD",
        "owner_oracle": lambda s: s["hiddenOracle"]["progressDecisions"][0],
    }
    for name, policy in policies.items():
        rows = []
        for scenario in battlefield["scenarios"]:
            decision = policy(scenario)
            submission = {
                "decision": decision,
                "predictedOwnerDisposition": expected_disposition(scenario, decision) or "uncertain",
            }
            rows.append(score(scenario, "deterministic", submission))
        baselines[name] = {
            "semanticAccepted": sum(r["semanticAccepted"] for r in rows),
            "falseConsequences": sum(r["falseConsequence"] for r in rows),
            "unnecessaryHolds": sum(r["unnecessaryHold"] for r in rows),
            "progressCorrect": sum(r["progressCorrect"] for r in rows),
            "authoritySafe": sum(r["authoritySafe"] for r in rows),
            "scenarios": len(rows),
        }
    return baselines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["validate", "canary", "run"], required=True)
    parser.add_argument("--replicates", type=int, default=4)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    battlefield = json.loads(BATTLEFIELD.read_text())
    if len(SECRETS) < 1:
        raise RuntimeError("no DeepSeek secret configured")
    if args.phase == "validate":
        print(json.dumps({
            "ok": True,
            "battlefieldDigest": canonical_digest(battlefield),
            "physicalProbeDigest": "sha256:" + hashlib.sha256((ROOT / "physical-owner-probe-v1.json").read_bytes()).hexdigest(),
            "scenarios": [s["id"] for s in battlefield["scenarios"]],
            "secrets": [p.name for p in SECRETS],
            "baselines": deterministic_baselines(battlefield),
        }, ensure_ascii=False, indent=2))
        return 0
    if args.phase == "canary":
        results = []
        messages = [
            {"role": "system", "content": "Transport canary. Submit HOLD exactly once."},
            {"role": "user", "content": "Use the submit Tool with decision HOLD, predictedOwnerDisposition would_hold, wouldCreateNewConsequence false, and concise placeholders."},
        ]
        for path in SECRETS:
            submission, usage = call_model(messages, path, max_tokens=800)
            results.append({"secret": path.name, "decision": submission["decision"], "usage": usage})
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    treatments = ["stale_evidence", "generic_change", "owner_native"]
    jobs: list[tuple[dict[str, Any], str, int, Path]] = []
    index = 0
    for scenario in battlefield["scenarios"]:
        for treatment in treatments:
            for replicate in range(1, args.replicates + 1):
                jobs.append((scenario, treatment, replicate, SECRETS[index % len(SECRETS)]))
                index += 1
    records: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(run_one, *job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            records.append(future.result())
    records.sort(key=lambda r: (r["scenario"], r["treatment"], r["replicate"]))
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.hp4-binding-concurrency-receipt",
        "battlefieldDigest": canonical_digest(battlefield),
        "physicalProbeDigest": "sha256:" + hashlib.sha256((ROOT / "physical-owner-probe-v1.json").read_bytes()).hexdigest(),
        "replicatesPerScenarioTreatment": args.replicates,
        "deterministicBaselines": deterministic_baselines(battlefield),
        "aggregate": aggregate(records),
        "records": records,
    }
    receipt["payloadDigest"] = canonical_digest(receipt)
    write_json(ROOT / "evidence" / "hp4-live-v2.json", receipt)
    print(json.dumps({
        "payloadDigest": receipt["payloadDigest"],
        "deterministicBaselines": receipt["deterministicBaselines"],
        "aggregate": receipt["aggregate"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
