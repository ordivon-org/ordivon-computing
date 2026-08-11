from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import random
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
TARGETS = [
    "repeated-low-information-failure",
    "information-route-bottleneck",
    "survival-spatial-pressure",
    "local-policy-choice",
    "world-mechanic-affordance",
    "mixed-or-insufficient-evidence",
]
TARGET_HELP = {
    "repeated-low-information-failure": "Repeated failure/contestation adds little new information and should be the next bounded research target.",
    "information-route-bottleneck": "Knowledge/contact/route formation is the main causal bottleneck before useful action becomes available.",
    "survival-spatial-pressure": "Health, position, capacity, or hostile pressure blocks the actor before the useful affordance becomes actionable.",
    "local-policy-choice": "The needed affordance is locally available/legible, but the Agent chooses poorly or fails to exploit it.",
    "world-mechanic-affordance": "World/content/mechanics fail to expose or realize the intended causal affordance even when the Agent reaches the relevant situation.",
    "mixed-or-insufficient-evidence": "No single bounded causal research target is justified from the available trajectory evidence.",
}


def digest_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_digest(value: Any) -> str:
    return digest_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def load_secret() -> dict[str, Any]:
    return json.loads(SECRET.read_text())


def function_tool(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
    }


def call_model(messages: list[dict[str, Any]], tools: list[dict[str, Any]], *, max_tokens: int = 1800) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    secret = load_secret()
    body = {
        "model": secret["model"],
        "messages": messages,
        "tools": tools,
        "tool_choice": "required",
        "thinking": {"type": "disabled"},
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "stream": False,
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    retries = 0
    started = time.time_ns()
    while True:
        request = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=encoded,
            headers={
                "Authorization": "Bearer " + str(secret["apiKey"]),
                "Content-Type": "application/json",
                "User-Agent": "ordivon-computing-rf1/1",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                raw = response.read(4_194_304)
            break
        except urllib.error.HTTPError as error:
            detail = error.read(4096).decode(errors="replace")
            raise RuntimeError(f"Provider HTTP {error.code}: {detail}") from error
        except (http.client.HTTPException, urllib.error.URLError, TimeoutError, OSError):
            if retries >= 1:
                raise
            retries += 1
            time.sleep(0.5)
    payload = json.loads(raw)
    message = payload["choices"][0]["message"]
    calls = message.get("tool_calls")
    if not isinstance(calls, list) or not calls:
        raise ValueError("Provider returned no tool call")
    parsed_calls: list[dict[str, Any]] = []
    for call in calls:
        fn = call.get("function") if isinstance(call, dict) else None
        if not isinstance(fn, dict):
            raise ValueError("malformed tool call")
        name = fn.get("name")
        call_id = call.get("id")
        arguments = fn.get("arguments")
        if not all(isinstance(value, str) and value for value in (name, call_id, arguments)):
            raise ValueError("malformed tool call fields")
        parsed = json.loads(arguments)
        if not isinstance(parsed, dict):
            raise ValueError("tool arguments must be object")
        parsed_calls.append({"id": call_id, "name": name, "arguments": parsed})
    usage = payload.get("usage", {})
    meta = {
        "model": payload.get("model", secret["model"]),
        "elapsedMs": (time.time_ns() - started) // 1_000_000,
        "inputTokens": int(usage.get("prompt_tokens", 0) or 0),
        "outputTokens": int(usage.get("completion_tokens", 0) or 0),
        "totalTokens": int(usage.get("total_tokens", 0) or 0),
        "transportRetries": retries,
    }
    assistant_wire = {"role": "assistant", "content": message.get("content"), "tool_calls": calls}
    return parsed_calls, meta, assistant_wire


def submit_tool(name: str = "submit_research_target") -> list[dict[str, Any]]:
    return [
        function_tool(
            name,
            "Submit one bounded causal research target from the evidence. This is not a fun score or product approval.",
            {
                "researchTarget": {"type": "string", "enum": TARGETS},
                "rationale": {"type": "string"},
                "citedTurns": {"type": "array", "items": {"type": "integer"}},
                "liveAlternatives": {"type": "array", "items": {"type": "string"}},
            },
            ["researchTarget", "rationale", "citedTurns", "liveAlternatives"],
        )
    ]


def progressive_tools() -> list[dict[str, Any]]:
    return [
        function_tool(
            "observe_turn",
            "Request one exact Turn window because it could discriminate a still-live alternative.",
            {
                "turnSequence": {"type": "integer"},
                "discriminates": {"type": "string"},
            },
            ["turnSequence", "discriminates"],
        ),
        function_tool(
            "stop_research",
            "Stop when no available unobserved Turn is expected to change the bounded causal research target. Do not stop on confidence alone.",
            {
                "researchTarget": {"type": "string", "enum": TARGETS},
                "rationale": {"type": "string"},
                "citedTurns": {"type": "array", "items": {"type": "integer"}},
                "liveAlternatives": {"type": "array", "items": {"type": "string"}},
                "noFurtherDiscriminator": {"type": "string"},
            },
            ["researchTarget", "rationale", "citedTurns", "liveAlternatives", "noFurtherDiscriminator"],
        ),
    ]


def compact_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "turn": state.get("turn"),
        "status": state.get("status"),
        "resources": state.get("resources"),
        "actors": state.get("actors"),
        "contacts": state.get("contacts"),
        "known": state.get("known"),
        "objectives": state.get("objectives"),
        "outcomes": state.get("outcomes"),
    }


def compact_turn(turn: dict[str, Any]) -> dict[str, Any]:
    return {
        "turnSequence": turn["turnSequence"],
        "highlightReasons": turn.get("highlightReasons", []),
        "before": compact_state(turn["before"]),
        "preview": {
            "commanderDirectiveId": turn["preview"].get("commanderDirectiveId"),
            "commanderAction": turn["preview"].get("commanderAction"),
            "summary": turn["preview"].get("summary"),
            "risks": turn["preview"].get("risks"),
            "actions": turn["preview"].get("actions"),
        },
        "consequence": turn["consequence"],
        "after": compact_state(turn["after"]),
        "diagnostics": turn.get("diagnostics", {}),
    }


def overview(run: dict[str, Any], variant: str) -> dict[str, Any]:
    return {
        "variant": variant,
        "profileId": run["profileId"],
        "intendedProbe": run["intendedProbe"],
        "orderProbe": run["orderProbe"],
        "turnsExecuted": run["turnsExecuted"],
        "objectiveVector": run["objectiveVector"],
        "diagnostics": run["diagnostics"],
        "finalPlayerProjected": {
            "status": run["final"].get("status"),
            "resources": run["final"].get("resources"),
            "objectives": run["final"].get("objectives"),
            "outcomes": run["final"].get("outcomes"),
        },
        "turnInventory": [
            {
                "turnSequence": turn["turnSequence"],
                "highlightReasons": turn.get("highlightReasons", []),
            }
            for turn in run["turns"]
        ],
    }


def load_cases() -> list[dict[str, Any]]:
    specs = [
        ("pre-af-loop-001", INPUTS / "baseline-269d8cf.json", "269d8cf8362730e014c79ccdfa8f748c1b3e0bff"),
        ("post-af-loop-001", INPUTS / "afloop-6bc7405.json", "6bc74051affb78b3a6f4dd6c82fd31a2b9f7f25e"),
    ]
    cases: list[dict[str, Any]] = []
    for variant, path, revision in specs:
        raw = path.read_bytes()
        packet = json.loads(raw)
        for run in packet["runs"]:
            cases.append(
                {
                    "caseId": f"{variant}:{run['profileId']}",
                    "variant": variant,
                    "gameRevision": revision,
                    "packetPath": str(path.relative_to(ROOT)),
                    "packetDigest": digest_bytes(raw),
                    "run": run,
                }
            )
    return cases


def decision_context() -> str:
    return (
        "Choose the narrowest next causal research target for this one Station Zero trajectory. "
        "Do not score fun and do not propose a broad rewrite. Target meanings: "
        + json.dumps(TARGET_HELP, ensure_ascii=False)
    )


def one_shot_decision(case: dict[str, Any], turns: list[dict[str, Any]], label: str) -> dict[str, Any]:
    body = {
        "caseId": case["caseId"],
        "evidenceMode": label,
        "overview": overview(case["run"], case["variant"]),
        "observedTurns": turns,
        "instruction": decision_context(),
    }
    prompt = json.dumps(body, ensure_ascii=False)
    calls, usage, _ = call_model(
        [
            {"role": "system", "content": "You are a Game causal auditor. Use the provided evidence only and submit exactly one bounded research target."},
            {"role": "user", "content": prompt},
        ],
        submit_tool(),
    )
    if any(call["name"] != "submit_research_target" for call in calls):
        raise ValueError("unexpected one-shot tool")
    result = dict(calls[0]["arguments"])
    result["parallelCallCount"] = len(calls)
    return {"result": result, "usage": usage, "contextBytes": len(prompt.encode())}


def progressive_decision(case: dict[str, Any]) -> dict[str, Any]:
    run = case["run"]
    by_turn = {int(turn["turnSequence"]): compact_turn(turn) for turn in run["turns"]}
    base = {
        "caseId": case["caseId"],
        "overview": overview(run, case["variant"]),
        "instruction": decision_context(),
        "stoppingRule": (
            "After each evidence batch, either request an unobserved Turn that could discriminate a still-live alternative, "
            "or STOP only if no currently available unobserved Turn is expected to change your bounded research target. "
            "Never use a confidence threshold as the stopping reason."
        ),
    }
    initial = json.dumps(base, ensure_ascii=False)
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": "You are a Game causal auditor controlling your own evidence acquisition. Use only observe_turn or stop_research."},
        {"role": "user", "content": initial},
    ]
    total_usage = {"inputTokens": 0, "outputTokens": 0, "totalTokens": 0, "elapsedMs": 0, "transportRetries": 0}
    unique_observed: list[int] = []
    observation_requests = 0
    observation_bytes = 0
    trace: list[dict[str, Any]] = []
    submission: dict[str, Any] | None = None
    forced = False
    for round_index in range(10):
        allowed_tools = progressive_tools()
        calls, usage, assistant_wire = call_model(messages, allowed_tools)
        for key in total_usage:
            total_usage[key] += int(usage.get(key, 0) or 0)
        if any(call["name"] not in {"observe_turn", "stop_research"} for call in calls):
            raise ValueError("unexpected progressive tool")
        trace.append({"round": round_index, "calls": calls})
        stop_calls = [call for call in calls if call["name"] == "stop_research"]
        if stop_calls:
            submission = dict(stop_calls[0]["arguments"])
            submission["parallelCallCountAtStop"] = len(calls)
            break
        messages.append(assistant_wire)
        for call in calls:
            observation_requests += 1
            turn_sequence = int(call["arguments"].get("turnSequence", -1))
            if turn_sequence not in by_turn:
                payload = {"status": "invalid-turn", "turnSequence": turn_sequence, "available": sorted(by_turn)}
            elif turn_sequence in unique_observed:
                payload = {"status": "duplicate-observation", "turn": by_turn[turn_sequence]}
            else:
                unique_observed.append(turn_sequence)
                payload = {"status": "observed", "turn": by_turn[turn_sequence]}
            rendered = json.dumps(payload, ensure_ascii=False)
            observation_bytes += len(rendered.encode())
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": rendered})
        if len(unique_observed) >= len(by_turn):
            forced = True
            break
    if submission is None:
        force_prompt = (
            "All available Turn windows have now been observed or the acquisition loop ended. "
            "You must submit the narrowest current research target; stopping is forced by evidence exhaustion, not confidence."
        )
        calls, usage, _ = call_model(
            messages + [{"role": "user", "content": force_prompt}],
            [function_tool(
                "stop_research",
                "Submit the final bounded target after evidence exhaustion.",
                {
                    "researchTarget": {"type": "string", "enum": TARGETS},
                    "rationale": {"type": "string"},
                    "citedTurns": {"type": "array", "items": {"type": "integer"}},
                    "liveAlternatives": {"type": "array", "items": {"type": "string"}},
                    "noFurtherDiscriminator": {"type": "string"},
                },
                ["researchTarget", "rationale", "citedTurns", "liveAlternatives", "noFurtherDiscriminator"],
            )],
        )
        for key in total_usage:
            total_usage[key] += int(usage.get(key, 0) or 0)
        stop_calls = [call for call in calls if call["name"] == "stop_research"]
        if not stop_calls:
            raise ValueError("forced finalization returned no stop")
        submission = dict(stop_calls[0]["arguments"])
        submission["parallelCallCountAtStop"] = len(calls)
        forced = True
    all_reasons = {reason for turn in run["turns"] for reason in turn.get("highlightReasons", [])}
    observed_reasons = {
        reason
        for turn_sequence in unique_observed
        for reason in by_turn[turn_sequence].get("highlightReasons", [])
    }
    return {
        "result": submission,
        "usage": total_usage,
        "initialContextBytes": len(initial.encode()),
        "observationBytes": observation_bytes,
        "uniqueObservedTurns": unique_observed,
        "uniqueObservedCount": len(unique_observed),
        "observationRequests": observation_requests,
        "redundantObservationRequests": max(0, observation_requests - len(unique_observed)),
        "forcedByEvidenceExhaustion": forced,
        "eventClassesAvailable": sorted(all_reasons),
        "eventClassesObserved": sorted(observed_reasons),
        "eventClassCoverage": (len(observed_reasons & all_reasons) / len(all_reasons)) if all_reasons else 1.0,
        "trace": trace,
    }


def add_usage(group: list[dict[str, Any]]) -> dict[str, int]:
    keys = ["inputTokens", "outputTokens", "totalTokens", "elapsedMs", "transportRetries"]
    return {key: sum(int(item.get("usage", {}).get(key, 0) or 0) for item in group) for key in keys}


def load_or_run(path: Path, producer: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text())
    record = producer()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    tmp.replace(path)
    return record


def run_campaign(output: Path, full_replicates: int) -> dict[str, Any]:
    cases = load_cases()
    progress = output.parent / (output.stem + "-progress")
    case_records: list[dict[str, Any]] = []
    for case in cases:
        compact_turns = [compact_turn(turn) for turn in case["run"]["turns"]]
        full_trials: list[dict[str, Any]] = []
        for replicate in range(1, full_replicates + 1):
            path = progress / f"{case['caseId'].replace(':', '__')}-full-r{replicate}.json"
            full_trials.append(load_or_run(path, lambda c=case, turns=compact_turns: one_shot_decision(c, turns, "full-trajectory")))
        targets = [trial["result"]["researchTarget"] for trial in full_trials]
        counts = Counter(targets)
        reference_target, reference_votes = counts.most_common(1)[0]
        stable_reference = reference_votes >= 2

        progressive_path = progress / f"{case['caseId'].replace(':', '__')}-progressive.json"
        progressive = load_or_run(progressive_path, lambda c=case: progressive_decision(c))
        stopped_target = progressive["result"]["researchTarget"]

        reveal_path = progress / f"{case['caseId'].replace(':', '__')}-full-reveal.json"
        reveal = load_or_run(
            reveal_path,
            lambda c=case, turns=compact_turns, stopped=stopped_target: one_shot_decision(
                c,
                turns,
                f"counterfactual-full-reveal-after-progressive-stop:{stopped}",
            ),
        )
        reveal_target = reveal["result"]["researchTarget"]
        false_early_stop = progressive["uniqueObservedCount"] < len(compact_turns) and reveal_target != stopped_target

        sample_count = progressive["uniqueObservedCount"]
        rng = random.Random("rf1-random:" + case["caseId"])
        sampled_turns = sorted(rng.sample(range(len(compact_turns)), k=sample_count)) if sample_count else []
        random_evidence = [compact_turns[index] for index in sampled_turns]
        random_path = progress / f"{case['caseId'].replace(':', '__')}-matched-random.json"
        matched_random = load_or_run(
            random_path,
            lambda c=case, turns=random_evidence: one_shot_decision(c, turns, "matched-random"),
        )
        random_target = matched_random["result"]["researchTarget"]
        random_reasons = {
            reason
            for index in sampled_turns
            for reason in compact_turns[index].get("highlightReasons", [])
        }
        all_reasons = {reason for turn in compact_turns for reason in turn.get("highlightReasons", [])}

        case_records.append(
            {
                "caseId": case["caseId"],
                "variant": case["variant"],
                "profileId": case["run"]["profileId"],
                "gameRevision": case["gameRevision"],
                "packetPath": case["packetPath"],
                "packetDigest": case["packetDigest"],
                "fullReference": {
                    "trials": full_trials,
                    "targets": targets,
                    "stable": stable_reference,
                    "referenceTarget": reference_target,
                    "referenceVotes": reference_votes,
                    "usage": add_usage(full_trials),
                },
                "progressive": progressive,
                "counterfactualFullReveal": reveal,
                "matchedRandom": {
                    **matched_random,
                    "sampledTurnIndexes": sampled_turns,
                    "eventClassesObserved": sorted(random_reasons),
                    "eventClassCoverage": (len(random_reasons & all_reasons) / len(all_reasons)) if all_reasons else 1.0,
                },
                "metrics": {
                    "progressiveAgreementWithReference": stable_reference and stopped_target == reference_target,
                    "randomAgreementWithReference": stable_reference and random_target == reference_target,
                    "progressiveStableAfterFullReveal": stopped_target == reveal_target,
                    "falseEarlyStop": false_early_stop,
                    "progressiveUniqueWindowFraction": progressive["uniqueObservedCount"] / len(compact_turns),
                    "progressiveWindowsSaved": len(compact_turns) - progressive["uniqueObservedCount"],
                },
            }
        )

    stable = [record for record in case_records if record["fullReference"]["stable"]]
    false_early = [record for record in stable if record["metrics"]["falseEarlyStop"]]
    progressive_agree = sum(bool(record["metrics"]["progressiveAgreementWithReference"]) for record in stable)
    random_agree = sum(bool(record["metrics"]["randomAgreementWithReference"]) for record in stable)
    aggregate = {
        "cases": len(case_records),
        "stableReferenceCases": len(stable),
        "ambiguousReferenceCases": len(case_records) - len(stable),
        "progressiveAgreement": progressive_agree,
        "matchedRandomAgreement": random_agree,
        "progressiveAgreementRate": progressive_agree / len(stable) if stable else None,
        "matchedRandomAgreementRate": random_agree / len(stable) if stable else None,
        "falseEarlyStops": len(false_early),
        "falseEarlyStopRate": len(false_early) / len(stable) if stable else None,
        "meanProgressiveUniqueWindowFraction": sum(record["metrics"]["progressiveUniqueWindowFraction"] for record in case_records) / len(case_records),
        "meanProgressiveEventCoverage": sum(record["progressive"]["eventClassCoverage"] for record in case_records) / len(case_records),
        "meanRandomEventCoverage": sum(record["matchedRandom"]["eventClassCoverage"] for record in case_records) / len(case_records),
        "progressiveForcedByEvidenceExhaustion": sum(bool(record["progressive"]["forcedByEvidenceExhaustion"]) for record in case_records),
        "progressiveTokens": sum(record["progressive"]["usage"]["totalTokens"] for record in case_records),
        "progressiveRevealTokens": sum(record["counterfactualFullReveal"]["usage"]["totalTokens"] for record in case_records),
        "matchedRandomTokens": sum(record["matchedRandom"]["usage"]["totalTokens"] for record in case_records),
        "fullReferenceTokens": sum(record["fullReference"]["usage"]["totalTokens"] for record in case_records),
    }
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.rf1-game-stopping-receipt",
        "provider": "deepseek",
        "model": load_secret()["model"],
        "fullReferenceReplicatesPerCase": full_replicates,
        "targetVocabulary": TARGET_HELP,
        "cases": case_records,
        "aggregate": aggregate,
    }
    receipt["receiptDigest"] = canonical_digest(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "rf1-live-v1.json")
    parser.add_argument("--full-replicates", type=int, default=3)
    args = parser.parse_args()
    receipt = run_campaign(args.output, args.full_replicates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"aggregate": receipt["aggregate"], "receiptDigest": receipt["receiptDigest"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
