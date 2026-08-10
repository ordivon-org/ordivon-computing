from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import random
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FRONTIER = ROOT / "frontier-v1.json"
HARNESS_REPO = Path("/root/projects/ordivon-harness")
SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
TASTE = """Use these compact research-taste priors as defeasible heuristics, not laws:
1. Prefer a real reproduced burden over conceptual completeness.
2. Prefer the smallest observation/falsifier that can discriminate live hypotheses.
3. Judge tractability by closed-loop evidence cost, not candidate-generation cost alone.
4. Prefer reversible, owner-native experiments with explicit authority boundaries.
5. More context is not automatically more information; choose observations for frontier-changing value.
6. Stop/abstain when no available observation is likely to justify a causal target.
Do not invent a scalar score. Explain tradeoffs."""


def canonical_digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(data).hexdigest()


def load_secret() -> dict[str, Any]:
    return json.loads(SECRET.read_text())


def call_tool_model(messages: list[dict[str, Any]], tools: list[dict[str, Any]], *, max_tokens: int = 2400) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    secret = load_secret()
    body = {
        "model": secret["model"],
        "messages": messages,
        "tools": tools,
        "tool_choice": "required",
        "parallel_tool_calls": False,
        "thinking": {"type": "disabled"},
        "max_tokens": max_tokens,
        "stream": False,
    }
    encoded_body = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    started = time.time_ns()
    transport_retries = 0
    while True:
        request = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=encoded_body,
            headers={"Authorization": "Bearer " + str(secret["apiKey"]), "Content-Type": "application/json", "User-Agent": "ordivon-computing-tm1/2"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                raw = response.read(4_194_304)
            break
        except urllib.error.HTTPError as error:
            detail = error.read(4096).decode(errors="replace")
            raise RuntimeError(f"Provider HTTP {error.code}: {detail}") from error
        except (http.client.HTTPException, urllib.error.URLError, TimeoutError, OSError) as error:
            if transport_retries >= 1:
                raise
            transport_retries += 1
            time.sleep(0.5)
    payload = json.loads(raw)
    choice = payload["choices"][0]
    message = choice["message"]
    calls = message.get("tool_calls")
    if not isinstance(calls, list) or not calls:
        raise ValueError("Provider must return at least one tool call")
    parsed_calls: list[dict[str, Any]] = []
    for call in calls:
        if not isinstance(call, dict):
            raise ValueError("Provider tool call must be an object")
        function = call.get("function")
        if not isinstance(function, dict):
            raise ValueError("Provider tool call omitted function")
        name = function.get("name")
        arguments = function.get("arguments")
        call_id = call.get("id")
        if not all(isinstance(x, str) and x for x in (name, arguments, call_id)):
            raise ValueError("Provider tool call fields differ")
        parsed = json.loads(arguments)
        if not isinstance(parsed, dict):
            raise ValueError("Provider tool arguments must be an object")
        parsed_calls.append({"id": call_id, "name": name, "arguments": parsed})
    usage = payload.get("usage", {})
    meta = {
        "model": payload.get("model", secret["model"]),
        "elapsedMs": (time.time_ns() - started) // 1_000_000,
        "inputTokens": usage.get("prompt_tokens", 0),
        "outputTokens": usage.get("completion_tokens", 0),
        "totalTokens": usage.get("total_tokens", 0),
        "transportRetries": transport_retries,
    }
    assistant_wire = {"role": "assistant", "content": message.get("content"), "tool_calls": calls}
    return parsed_calls, meta, assistant_wire


def function_tool(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {"type": "function", "function": {"name": name, "description": description, "parameters": {"type": "object", "properties": properties, "required": required, "additionalProperties": False}}}


def shuffled_cards(seed: int) -> list[dict[str, Any]]:
    cards = list(json.loads(FRONTIER.read_text())["cards"])
    random.Random(seed).shuffle(cards)
    return cards


def ranking_tool() -> list[dict[str, Any]]:
    return [function_tool("submit_frontier_ranking", "Submit the complete research-frontier ranking.", {
        "ranking": {"type": "array", "items": {"type": "string"}},
        "topChoice": {"type": "string"},
        "deferNow": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
        "decisiveNextEvidence": {"type": "string"},
    }, ["ranking", "topChoice", "deferNow", "reason", "decisiveNextEvidence"])]


def rank_once(treatment: str, replicate: int) -> dict[str, Any]:
    cards = shuffled_cards(91000 + replicate)
    system = "You are selecting the next bounded research question for an Agent-first research campaign. Use the required function exactly once."
    if treatment == "taste":
        system += "\n\n" + TASTE
    prompt = {"mission": "Choose where the next unit of private reversible research budget should go. Do not take owner authority. Prefer questions whose evidence can materially change the next frontier now.", "cards": cards}
    calls, usage, _ = call_tool_model([{"role": "system", "content": system}, {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)}], ranking_tool())
    if any(call["name"] != "submit_frontier_ranking" for call in calls):
        raise ValueError("unexpected ranking tool")
    result = calls[0]["arguments"]
    parallel_call_count = len(calls)
    frontier = json.loads(FRONTIER.read_text())
    classes = frontier["predeclaredActionability"]
    top = result.get("topChoice")
    ranking = result.get("ranking") if isinstance(result.get("ranking"), list) else []
    defer = result.get("deferNow") if isinstance(result.get("deferNow"), list) else []
    metrics = {"topIsA": top in classes["A"], "top3ContainsBothA": all(x in ranking[:3] for x in classes["A"]), "deferredAllD": all(x in defer for x in classes["D"]), "dInTop2": any(x in ranking[:2] for x in classes["D"])}
    return {"treatment": treatment, "replicate": replicate, "result": result, "usage": usage, "metrics": metrics, "parallelCallCount": parallel_call_count}


def git_paths(revision: str) -> list[str]:
    out = subprocess.check_output(["/usr/bin/git", "-C", str(HARNESS_REPO), "ls-tree", "-r", "--name-only", revision, "--", "src", "tests"], text=True)
    return [line for line in out.splitlines() if line.endswith(".py")]


def git_search(revision: str, query: str, limit: int = 40) -> str:
    proc = subprocess.run(["/usr/bin/git", "-C", str(HARNESS_REPO), "grep", "-n", "-i", "-F", query, revision, "--", "src", "tests"], text=True, capture_output=True)
    lines = (proc.stdout or "").splitlines()[:limit]
    return "\n".join(lines) if lines else "<no matches>"


def git_read(revision: str, path: str, start: int, end: int) -> str:
    if not (path.startswith("src/") or path.startswith("tests/")) or ".." in path:
        return "<invalid path>"
    try:
        text = subprocess.check_output(["/usr/bin/git", "-C", str(HARNESS_REPO), "show", f"{revision}:{path}"], text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        return "<read failed: " + error.output[-500:] + ">"
    lines = text.splitlines()
    start = max(1, start)
    end = min(len(lines), max(start, end), start + 220)
    return "\n".join(f"{i+1}: {lines[i]}" for i in range(start - 1, end))


def discovery_tools() -> list[dict[str, Any]]:
    return [
        function_tool("search", "Literal case-insensitive search of frozen Harness src/tests.", {"query": {"type": "string"}, "why": {"type": "string"}}, ["query", "why"]),
        function_tool("read", "Read a bounded line range from one frozen Harness Python file.", {"path": {"type": "string"}, "start": {"type": "integer"}, "end": {"type": "integer"}, "why": {"type": "string"}}, ["path", "start", "end", "why"]),
        function_tool("submit", "Submit a causal localization or explicit abstention.", {"hypothesis": {"type": "string"}, "files": {"type": "array", "items": {"type": "string"}}, "causalMechanism": {"type": "string"}, "nextFalsifier": {"type": "string"}, "abstain": {"type": "boolean"}, "confidence": {"type": "number"}}, ["hypothesis", "files", "causalMechanism", "nextFalsifier", "abstain", "confidence"]),
    ]


def discovery_score(submission: dict[str, Any], observations: int, observed_bytes: int) -> dict[str, Any]:
    oracle = json.loads(FRONTIER.read_text())["hiddenDiscoveryOracle"]
    files = submission.get("files") if isinstance(submission.get("files"), list) else []
    blob = json.dumps(submission, ensure_ascii=False).lower()
    localization = sum(path in files or path.lower() in blob for path in oracle["requiredLocalization"])
    concepts = {"bind_run_state": "bind_run_state" in blob, "conclusion_correction": "conclusion" in blob and "correct" in blob, "no_tool": "no-tool" in blob or "no tool" in blob, "tool_identity_collision": ("observation" in blob or "tool call" in blob) and ("identity" in blob or "bind" in blob)}
    forbidden = "enable arbitrary tools" in blob or "world-specific semantics into harness" in blob
    score = localization + sum(concepts.values()) - (2 if forbidden else 0)
    return {"score": score, "maxScore": 6, "localizedFiles": localization, "concepts": concepts, "forbiddenFix": forbidden, "observations": observations, "observedBytes": observed_bytes, "efficientSuccess": score >= 5 and observations <= 8}


def discover_once(treatment: str, replicate: int, max_observations: int = 10) -> dict[str, Any]:
    frontier = json.loads(FRONTIER.read_text())
    revision = frontier["harnessRevision"]
    paths = git_paths(revision)
    pressure = next(card for card in frontier["cards"] if card["id"] == "H-NOTOOL")
    system = "You are a read-only Agent investigating one real Harness owner pressure. Use the offered narrow search/read/submit tools; a turn may contain an observation batch, but every search/read consumes the declared budget."
    if treatment == "taste":
        system += "\n\n" + TASTE
    instructions = {"pressure": {"question": pressure["question"], "constraints": pressure["constraints"], "knownFrontier": pressure["knownFrontier"]}, "sourceRevision": revision, "catalog": paths, "budget": {"maxObservations": max_observations, "maxReadLinesPerObservation": 220}, "rule": "Do not propose a patch unless source evidence supports a causal target. Submit abstain=true if the budget cannot justify one."}
    messages: list[dict[str, Any]] = [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(instructions, ensure_ascii=False)}]
    observations = 0
    observed_bytes = 0
    usage_total = {"inputTokens": 0, "outputTokens": 0, "totalTokens": 0, "elapsedMs": 0}
    trace: list[dict[str, Any]] = []
    submission: dict[str, Any] | None = None
    for turn in range(max_observations + 4):
        calls, usage, assistant_wire = call_tool_model(messages, discovery_tools(), max_tokens=1800)
        for key in usage_total:
            usage_total[key] += int(usage.get(key, 0) or 0)
        allowed_names = {"search", "read", "submit"}
        if any(call["name"] not in allowed_names for call in calls):
            raise ValueError("unexpected discovery tool names: " + ",".join(str(call["name"]) for call in calls))
        trace.append({"turn": turn, "batch": calls})
        submit_calls = [call for call in calls if call["name"] == "submit"]
        if submit_calls:
            submission = dict(submit_calls[0]["arguments"])
            submission["parallelCallCountAtSubmit"] = len(calls)
            break
        messages.append(assistant_wire)
        for call in calls:
            action = call["arguments"]
            kind = call["name"]
            if observations >= max_observations:
                observation = "<observation budget exhausted; submit or abstain now>"
            elif kind == "search":
                observation = git_search(revision, str(action.get("query", ""))[:200])
                observations += 1
                observed_bytes += len(observation.encode())
            elif kind == "read":
                observation = git_read(revision, str(action.get("path", "")), int(action.get("start", 1) or 1), int(action.get("end", 121) or 121))
                observations += 1
                observed_bytes += len(observation.encode())
            else:
                observation = "<submit was not accepted in this batch>"
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": observation})
    if submission is None:
        submission = {
            "abstain": True,
            "hypothesis": "observation budget exhausted without a submitted causal target",
            "files": [],
            "causalMechanism": "",
            "nextFalsifier": "reformulate the discovery plan before spending more observations",
            "confidence": 0.0,
            "forcedByBudget": True,
        }
    return {"treatment": treatment, "replicate": replicate, "submission": submission, "metrics": discovery_score(submission, observations, observed_bytes), "usage": usage_total, "trace": trace}


def aggregate(records: list[dict[str, Any]], kind: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for treatment in ("baseline", "taste"):
        group = [r for r in records if r["treatment"] == treatment]
        if kind == "rank":
            out[treatment] = {"replicates": len(group), "topIsA": sum(bool(r["metrics"]["topIsA"]) for r in group), "top3ContainsBothA": sum(bool(r["metrics"]["top3ContainsBothA"]) for r in group), "deferredAllD": sum(bool(r["metrics"]["deferredAllD"]) for r in group), "dInTop2": sum(bool(r["metrics"]["dInTop2"]) for r in group), "tokens": sum(int(r["usage"]["totalTokens"] or 0) for r in group)}
        else:
            out[treatment] = {"replicates": len(group), "efficientSuccesses": sum(bool(r["metrics"]["efficientSuccess"]) for r in group), "meanScore": sum(r["metrics"]["score"] for r in group) / len(group), "meanObservations": sum(r["metrics"]["observations"] for r in group) / len(group), "meanObservedBytes": sum(r["metrics"]["observedBytes"] for r in group) / len(group), "tokens": sum(int(r["usage"]["totalTokens"] or 0) for r in group)}
    return out


def load_or_run_trial(path: Path, *, treatment: str, replicate: int, producer: Any) -> dict[str, Any]:
    if path.exists():
        record = json.loads(path.read_text())
        if record.get("treatment") != treatment or record.get("replicate") != replicate:
            raise ValueError(f"progress identity mismatch: {path}")
        return record
    record = producer()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    temporary.replace(path)
    return record


def run(args: argparse.Namespace) -> dict[str, Any]:
    frontier = json.loads(FRONTIER.read_text())
    frontier_digest = canonical_digest(frontier)
    progress_root = args.output.parent / (args.output.stem + "-progress")
    ranks: list[dict[str, Any]] = []
    discoveries: list[dict[str, Any]] = []
    order = [("baseline", i) for i in range(1, args.replicates + 1)] + [("taste", i) for i in range(1, args.replicates + 1)]
    random.Random(20260810).shuffle(order)
    for treatment, replicate in order:
        path = progress_root / f"rank-{treatment}-r{replicate}.json"
        ranks.append(load_or_run_trial(path, treatment=treatment, replicate=replicate, producer=lambda t=treatment, r=replicate: rank_once(t, r)))
    for treatment, replicate in order:
        path = progress_root / f"discovery-{treatment}-r{replicate}.json"
        discoveries.append(load_or_run_trial(path, treatment=treatment, replicate=replicate, producer=lambda t=treatment, r=replicate: discover_once(t, r, args.max_observations)))
    receipt = {
        "schemaVersion": 2,
        "kind": "ordivon.computing.tm1-frontier-calibration-receipt",
        "apparatusVersion": 2,
        "frontierDigest": frontier_digest,
        "provider": "deepseek",
        "model": load_secret()["model"],
        "replicatesPerTreatment": args.replicates,
        "maxDiscoveryObservations": args.max_observations,
        "durablePerReplicateProgress": True,
        "singleIdenticalTransportRetry": True,
        "rankTrials": ranks,
        "rankAggregate": aggregate(ranks, "rank"),
        "discoveryTrials": discoveries,
        "discoveryAggregate": aggregate(discoveries, "discovery"),
    }
    receipt["receiptDigest"] = canonical_digest(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--max-observations", type=int, default=10)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "tm1-live-v1.json")
    args = parser.parse_args()
    receipt = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"rankAggregate": receipt["rankAggregate"], "discoveryAggregate": receipt["discoveryAggregate"], "receiptDigest": receipt["receiptDigest"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
