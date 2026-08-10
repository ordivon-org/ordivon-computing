from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FRONTIER = ROOT / "frontier-v1.json"
TM1_RUNNER = ROOT.parent / "tm1-frontier-calibration" / "run_tm1.py"


def load_tm1() -> Any:
    spec = importlib.util.spec_from_file_location("ordivon_tm1_runner", TM1_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load TM1 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TM1 = load_tm1()


def canonical_digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(data).hexdigest()


def git_paths(repo: str, revision: str) -> list[str]:
    out = subprocess.check_output(
        ["/usr/bin/git", "-C", repo, "ls-tree", "-r", "--name-only", revision, "--", "src", "tests"],
        text=True,
    )
    return [line for line in out.splitlines() if line.endswith(".py")]


def git_search(repo: str, revision: str, query: str, limit: int = 50) -> str:
    proc = subprocess.run(
        ["/usr/bin/git", "-C", repo, "grep", "-n", "-i", "-F", query, revision, "--", "src", "tests"],
        text=True,
        capture_output=True,
    )
    lines = (proc.stdout or "").splitlines()[:limit]
    return "\n".join(lines) if lines else "<no matches>"


def git_read(repo: str, revision: str, path: str, start: int, end: int) -> str:
    if not (path.startswith("src/") or path.startswith("tests/")) or ".." in path:
        return "<invalid path>"
    try:
        text = subprocess.check_output(
            ["/usr/bin/git", "-C", repo, "show", f"{revision}:{path}"],
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as error:
        return "<read failed: " + error.output[-500:] + ">"
    lines = text.splitlines()
    start = max(1, start)
    end = min(len(lines), max(start, end), start + 220)
    return "\n".join(f"{index + 1}: {lines[index]}" for index in range(start - 1, end))


def tools() -> list[dict[str, Any]]:
    return [
        TM1.function_tool(
            "search",
            "Literal case-insensitive search of the frozen owner src/tests tree.",
            {"query": {"type": "string"}, "why": {"type": "string"}},
            ["query", "why"],
        ),
        TM1.function_tool(
            "read",
            "Read a bounded line range from one frozen owner Python file.",
            {
                "path": {"type": "string"},
                "start": {"type": "integer"},
                "end": {"type": "integer"},
                "why": {"type": "string"},
            },
            ["path", "start", "end", "why"],
        ),
        TM1.function_tool(
            "submit",
            "Submit a causal localization or explicit abstention.",
            {
                "hypothesis": {"type": "string"},
                "files": {"type": "array", "items": {"type": "string"}},
                "causalMechanism": {"type": "string"},
                "nextFalsifier": {"type": "string"},
                "abstain": {"type": "boolean"},
                "confidence": {"type": "number"},
            },
            ["hypothesis", "files", "causalMechanism", "nextFalsifier", "abstain", "confidence"],
        ),
    ]


def concept_flags(consumer_id: str, blob: str) -> dict[str, bool]:
    if consumer_id == "H-NOTOOL":
        return {
            "state_binding": "bind_run_state" in blob,
            "conclusion_correction": "conclusion" in blob and "correct" in blob,
            "no_tool_boundary": ("no-tool" in blob or "no tool" in blob) and ("observation" in blob or "tool call" in blob),
            "bounded_falsifier": ("reproduc" in blob or "falsif" in blob) and ("bind" in blob or "state" in blob),
        }
    if consumer_id == "S-UNKNOWN":
        return {
            "evidence_carrier_gap": "agentturnevidence" in blob and "unresolved" in blob,
            "prompt_forces_empty": "prompt" in blob and "unresolved" in blob and "empty" in blob,
            "driver_drops_unknown": ("rationale" in blob or "conclusion.summary" in blob or "result.conclusion" in blob) and "unresolved" in blob,
            "lifecycle_hardcodes_empty": ("record" in blob or "lifecycle" in blob) and "unresolved" in blob and "empty" in blob,
        }
    raise ValueError(consumer_id)


def score_submission(consumer: dict[str, Any], submission: dict[str, Any], observations: int, observed_bytes: int, seed_coverage: int) -> dict[str, Any]:
    oracle = consumer["hiddenOracle"]
    files = submission.get("files") if isinstance(submission.get("files"), list) else []
    blob = json.dumps(submission, ensure_ascii=False).lower()
    localization = sum(path in files or path.lower() in blob for path in oracle["requiredFiles"])
    concepts = concept_flags(consumer["id"], blob)
    forbidden = any(fragment.lower() in blob for fragment in oracle["forbidden"])
    score = localization + sum(concepts.values()) - (2 if forbidden else 0)
    return {
        "score": score,
        "maxScore": 6,
        "success": score >= 5,
        "localizedFiles": localization,
        "concepts": concepts,
        "forbiddenBoundary": forbidden,
        "observations": observations,
        "observedBytes": observed_bytes,
        "seedRequiredFileCoverage": seed_coverage,
    }


def seed_evidence(consumer: dict[str, Any]) -> tuple[list[dict[str, Any]], int, int]:
    records: list[dict[str, Any]] = []
    total_bytes = 0
    combined = ""
    for anchor in consumer["anchors"]:
        output = git_search(consumer["repo"], consumer["revision"], anchor)
        encoded = output.encode()
        total_bytes += len(encoded)
        combined += "\n" + output
        records.append(
            {
                "operator": "literal_git_search",
                "anchor": anchor,
                "bytes": len(encoded),
                "outputDigest": "sha256:" + hashlib.sha256(encoded).hexdigest(),
                "output": output,
            }
        )
    coverage = sum(path in combined for path in consumer["hiddenOracle"]["requiredFiles"])
    return records, total_bytes, coverage


def discover_once(consumer: dict[str, Any], treatment: str, replicate: int, max_observations: int) -> dict[str, Any]:
    catalog = git_paths(consumer["repo"], consumer["revision"])
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "You are a read-only Agent localizing one real owner pressure. Use only the offered search/read/submit tools. "
                "A turn may contain an observation batch; every search/read counts against the total budget. Submit only when source evidence supports a causal localization, otherwise abstain."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "consumer": consumer["id"],
                    "pressure": consumer["pressure"],
                    "sourceRevision": consumer["revision"],
                    "catalog": catalog,
                    "budget": {"totalObservations": max_observations, "maxReadLines": 220},
                },
                ensure_ascii=False,
            ),
        },
    ]
    observations = 0
    observed_bytes = 0
    seed_coverage = 0
    trace: list[dict[str, Any]] = []
    if treatment == "evidence_first":
        seeded, seed_bytes, seed_coverage = seed_evidence(consumer)
        observations = len(seeded)
        observed_bytes = seed_bytes
        trace.append(
            {
                "turn": "seed",
                "observations": [
                    {key: value for key, value in item.items() if key != "output"} for item in seeded
                ],
            }
        )
        messages.append(
            {
                "role": "user",
                "content": "PRECOMPUTED OWNER-EVIDENCE OBSERVATIONS (already counted against the same budget):\n"
                + "\n\n".join(
                    f"ANCHOR {item['anchor']}\n{item['output']}" for item in seeded
                ),
            }
        )
    usage_total = {
        "inputTokens": 0,
        "outputTokens": 0,
        "totalTokens": 0,
        "elapsedMs": 0,
        "transportRetries": 0,
    }
    submission: dict[str, Any] | None = None
    for turn in range(max_observations + 4):
        calls, usage, assistant_wire = TM1.call_tool_model(messages, tools(), max_tokens=1800)
        for key in usage_total:
            usage_total[key] += int(usage.get(key, 0) or 0)
        allowed = {"search", "read", "submit"}
        if any(call["name"] not in allowed for call in calls):
            raise ValueError("unexpected tool name")
        trace.append({"turn": turn, "batch": calls})
        submits = [call for call in calls if call["name"] == "submit"]
        if submits:
            submission = dict(submits[0]["arguments"])
            submission["parallelCallCountAtSubmit"] = len(calls)
            break
        messages.append(assistant_wire)
        for call in calls:
            action = call["arguments"]
            if observations >= max_observations:
                output = "<observation budget exhausted; submit or abstain now>"
            elif call["name"] == "search":
                output = git_search(
                    consumer["repo"], consumer["revision"], str(action.get("query", ""))[:200]
                )
                observations += 1
                observed_bytes += len(output.encode())
            elif call["name"] == "read":
                output = git_read(
                    consumer["repo"],
                    consumer["revision"],
                    str(action.get("path", "")),
                    int(action.get("start", 1) or 1),
                    int(action.get("end", 121) or 121),
                )
                observations += 1
                observed_bytes += len(output.encode())
            else:
                output = "<submit not accepted as an observation>"
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": output})
    if submission is None:
        submission = {
            "abstain": True,
            "hypothesis": "observation budget exhausted without a submitted causal target",
            "files": [],
            "causalMechanism": "",
            "nextFalsifier": "reformulate the observation plan before spending more evidence budget",
            "confidence": 0.0,
            "forcedByBudget": True,
        }
    return {
        "consumer": consumer["id"],
        "treatment": treatment,
        "replicate": replicate,
        "submission": submission,
        "metrics": score_submission(consumer, submission, observations, observed_bytes, seed_coverage),
        "usage": usage_total,
        "trace": trace,
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for consumer_id in sorted({record["consumer"] for record in records}):
        result[consumer_id] = {}
        for treatment in ("open", "evidence_first"):
            group = [
                record
                for record in records
                if record["consumer"] == consumer_id and record["treatment"] == treatment
            ]
            result[consumer_id][treatment] = {
                "replicates": len(group),
                "successes": sum(bool(record["metrics"]["success"]) for record in group),
                "causalSubmissions": sum(not bool(record["submission"].get("abstain")) for record in group),
                "forcedAbstentions": sum(bool(record["submission"].get("forcedByBudget", False)) for record in group),
                "meanScore": sum(record["metrics"]["score"] for record in group) / len(group),
                "meanObservations": sum(record["metrics"]["observations"] for record in group) / len(group),
                "meanObservedBytes": sum(record["metrics"]["observedBytes"] for record in group) / len(group),
                "meanSeedCoverage": sum(record["metrics"]["seedRequiredFileCoverage"] for record in group) / len(group),
                "tokens": sum(int(record["usage"]["totalTokens"] or 0) for record in group),
                "transportRetries": sum(int(record["usage"]["transportRetries"] or 0) for record in group),
            }
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    frontier = json.loads(FRONTIER.read_text())
    progress_root = args.output.parent / (args.output.stem + "-progress")
    records: list[dict[str, Any]] = []
    planned = [
        (consumer, treatment, replicate)
        for consumer in frontier["consumers"]
        for treatment in ("open", "evidence_first")
        for replicate in range(1, args.replicates + 1)
    ]
    random.Random(20260810).shuffle(planned)
    for consumer, treatment, replicate in planned:
        path = progress_root / f"{consumer['id'].lower()}-{treatment}-r{replicate}.json"
        record = TM1.load_or_run_trial(
            path,
            treatment=treatment,
            replicate=replicate,
            producer=lambda c=consumer, t=treatment, r=replicate: discover_once(
                c, t, r, args.max_observations
            ),
        )
        if record.get("consumer") != consumer["id"]:
            raise ValueError("progress consumer identity mismatch")
        records.append(record)
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.tm2-operator-selection-receipt",
        "frontierDigest": canonical_digest(frontier),
        "provider": "deepseek",
        "model": TM1.load_secret()["model"],
        "replicatesPerConsumerTreatment": args.replicates,
        "totalObservationBudget": args.max_observations,
        "trials": records,
        "aggregate": aggregate(records),
    }
    receipt["receiptDigest"] = canonical_digest(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--max-observations", type=int, default=8)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "tm2-live-v1.json")
    args = parser.parse_args()
    receipt = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {"aggregate": receipt["aggregate"], "receiptDigest": receipt["receiptDigest"]},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
