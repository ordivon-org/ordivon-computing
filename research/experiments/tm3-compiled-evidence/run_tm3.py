from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
FRONTIER = ROOT / "frontier-v1.json"
TM2_RUNNER = ROOT.parent / "tm2-operator-selection" / "run_tm2.py"
TM2_FRONTIER = ROOT.parent / "tm2-operator-selection" / "frontier-v1.json"


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


TM2 = load_module(TM2_RUNNER, "ordivon_tm2_runner")
TM1 = TM2.TM1


def canonical_digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return "sha256:" + hashlib.sha256(data).hexdigest()


def raw_search(repo: str, revision: str, query: str, limit: int = 80) -> str:
    proc = subprocess.run(
        ["/usr/bin/git", "-C", repo, "grep", "-n", "-i", "-F", query, revision, "--", "src", "tests"],
        text=True,
        capture_output=True,
    )
    lines = (proc.stdout or "").splitlines()[:limit]
    return "\n".join(lines) if lines else "<no matches>"


def parse_matches(output: str, anchor_index: int) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    if output == "<no matches>":
        return matches
    for line in output.splitlines():
        parts = line.split(":", 3)
        if len(parts) < 3:
            continue
        if re.fullmatch(r"[0-9a-f]{40}", parts[0]):
            if len(parts) < 4:
                continue
            path = parts[1]
            line_text = parts[2]
        else:
            path = parts[0]
            line_text = parts[1]
        try:
            line_no = int(line_text)
        except ValueError:
            continue
        if path.startswith("src/") or path.startswith("tests/"):
            matches.append({"path": path, "line": line_no, "anchorIndex": anchor_index})
    return matches


def read_window(repo: str, revision: str, path: str, center: int) -> str:
    start = max(1, center - 45)
    end = center + 45
    return TM2.git_read(repo, revision, path, start, end)


def compile_evidence(consumer: dict[str, Any], max_observations: int) -> dict[str, Any]:
    search_outputs: list[dict[str, Any]] = []
    matches: list[dict[str, Any]] = []
    observed_bytes = 0
    observations = 0
    for index, anchor in enumerate(consumer["anchors"]):
        output = raw_search(consumer["repo"], consumer["revision"], anchor)
        encoded = output.encode()
        observed_bytes += len(encoded)
        observations += 1
        search_outputs.append(
            {
                "anchor": anchor,
                "output": output,
                "bytes": len(encoded),
                "digest": "sha256:" + hashlib.sha256(encoded).hexdigest(),
            }
        )
        matches.extend(parse_matches(output, index))

    stats: dict[str, dict[str, Any]] = {}
    for match in matches:
        entry = stats.setdefault(
            match["path"],
            {"path": match["path"], "anchorIndexes": set(), "hits": 0, "firstLine": match["line"]},
        )
        entry["anchorIndexes"].add(match["anchorIndex"])
        entry["hits"] += 1
        entry["firstLine"] = min(entry["firstLine"], match["line"])
    ranked = sorted(
        stats.values(),
        key=lambda item: (-len(item["anchorIndexes"]), -item["hits"], item["path"]),
    )

    windows: list[dict[str, Any]] = []
    remaining = max(0, max_observations - observations)
    for item in ranked[:remaining]:
        output = read_window(consumer["repo"], consumer["revision"], item["path"], item["firstLine"])
        encoded = output.encode()
        observed_bytes += len(encoded)
        observations += 1
        windows.append(
            {
                "path": item["path"],
                "centerLine": item["firstLine"],
                "anchorMatchCount": len(item["anchorIndexes"]),
                "hitCount": item["hits"],
                "output": output,
                "bytes": len(encoded),
                "digest": "sha256:" + hashlib.sha256(encoded).hexdigest(),
            }
        )

    required = consumer["requiredFiles"]
    search_blob = "\n".join(item["output"] for item in search_outputs)
    read_paths = {item["path"] for item in windows}
    return {
        "searchOutputs": search_outputs,
        "windows": windows,
        "observations": observations,
        "observedBytes": observed_bytes,
        "searchRequiredFileCoverage": sum(path in search_blob for path in required),
        "readRequiredFileCoverage": sum(path in read_paths for path in required),
    }


def submit_tool() -> list[dict[str, Any]]:
    return [
        TM1.function_tool(
            "submit",
            "Submit the causal localization from the compiled owner evidence, or explicitly abstain.",
            {
                "hypothesis": {"type": "string"},
                "files": {"type": "array", "items": {"type": "string"}},
                "causalMechanism": {"type": "string"},
                "nextFalsifier": {"type": "string"},
                "abstain": {"type": "boolean"},
                "confidence": {"type": "number"},
            },
            ["hypothesis", "files", "causalMechanism", "nextFalsifier", "abstain", "confidence"],
        )
    ]


def run_trial(consumer: dict[str, Any], replicate: int, max_observations: int) -> dict[str, Any]:
    evidence = compile_evidence(consumer, max_observations)
    rendered = {
        "pressure": consumer["pressure"],
        "sourceRevision": consumer["revision"],
        "evidenceCompilation": {
            "literalSearches": [
                {"anchor": item["anchor"], "output": item["output"]}
                for item in evidence["searchOutputs"]
            ],
            "boundedReadWindows": [
                {"path": item["path"], "centerLine": item["centerLine"], "output": item["output"]}
                for item in evidence["windows"]
            ],
        },
        "instruction": "Use only this compiled evidence. Do not request more research. Submit a causal localization only if justified; otherwise abstain. Preserve the owner boundary stated in the pressure.",
    }
    calls, usage, _ = TM1.call_tool_model(
        [
            {
                "role": "system",
                "content": "You are the semantic-synthesis step after deterministic owner-evidence compilation. Use submit exactly once; no search/read tools exist in this phase.",
            },
            {"role": "user", "content": json.dumps(rendered, ensure_ascii=False)},
        ],
        submit_tool(),
        max_tokens=2200,
    )
    if any(call["name"] != "submit" for call in calls):
        raise ValueError("unexpected synthesis tool")
    submission = dict(calls[0]["arguments"])
    submission["parallelCallCountAtSubmit"] = len(calls)
    tm2_consumers = {item["id"]: item for item in json.loads(TM2_FRONTIER.read_text())["consumers"]}
    score = TM2.score_submission(
        tm2_consumers[consumer["id"]],
        submission,
        evidence["observations"],
        evidence["observedBytes"],
        evidence["searchRequiredFileCoverage"],
    )
    score["compiledReadRequiredFileCoverage"] = evidence["readRequiredFileCoverage"]
    return {
        "consumer": consumer["id"],
        "treatment": "compiled_one_shot",
        "replicate": replicate,
        "submission": submission,
        "metrics": score,
        "usage": usage,
        "evidencePlan": {
            "observations": evidence["observations"],
            "observedBytes": evidence["observedBytes"],
            "searchRequiredFileCoverage": evidence["searchRequiredFileCoverage"],
            "readRequiredFileCoverage": evidence["readRequiredFileCoverage"],
            "rankedReadPaths": [item["path"] for item in evidence["windows"]],
            "searchDigests": [item["digest"] for item in evidence["searchOutputs"]],
            "readDigests": [item["digest"] for item in evidence["windows"]],
        },
    }


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for consumer_id in sorted({record["consumer"] for record in records}):
        group = [record for record in records if record["consumer"] == consumer_id]
        result[consumer_id] = {
            "replicates": len(group),
            "successes": sum(bool(record["metrics"]["success"]) for record in group),
            "causalSubmissions": sum(not bool(record["submission"].get("abstain")) for record in group),
            "meanScore": sum(record["metrics"]["score"] for record in group) / len(group),
            "meanObservations": sum(record["metrics"]["observations"] for record in group) / len(group),
            "meanObservedBytes": sum(record["metrics"]["observedBytes"] for record in group) / len(group),
            "meanSearchRequiredFileCoverage": sum(record["metrics"]["seedRequiredFileCoverage"] for record in group) / len(group),
            "meanReadRequiredFileCoverage": sum(record["metrics"]["compiledReadRequiredFileCoverage"] for record in group) / len(group),
            "tokens": sum(int(record["usage"].get("totalTokens", 0) or 0) for record in group),
            "transportRetries": sum(int(record["usage"].get("transportRetries", 0) or 0) for record in group),
            "providerCalls": len(group),
        }
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    frontier = json.loads(FRONTIER.read_text())
    progress_root = args.output.parent / (args.output.stem + "-progress")
    records: list[dict[str, Any]] = []
    for consumer in frontier["consumers"]:
        for replicate in range(1, args.replicates + 1):
            path = progress_root / f"{consumer['id'].lower()}-compiled-r{replicate}.json"
            record = TM1.load_or_run_trial(
                path,
                treatment="compiled_one_shot",
                replicate=replicate,
                producer=lambda c=consumer, r=replicate: run_trial(c, r, args.max_observations),
            )
            if record.get("consumer") != consumer["id"]:
                raise ValueError("progress consumer identity mismatch")
            records.append(record)
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.tm3-compiled-evidence-receipt",
        "frontierDigest": canonical_digest(frontier),
        "provider": "deepseek",
        "model": TM1.load_secret()["model"],
        "replicatesPerConsumer": args.replicates,
        "maximumEvidenceObservations": args.max_observations,
        "trials": records,
        "aggregate": aggregate(records),
    }
    receipt["receiptDigest"] = canonical_digest(receipt)
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=3)
    parser.add_argument("--max-observations", type=int, default=8)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "tm3-live-v1.json")
    args = parser.parse_args()
    receipt = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"aggregate": receipt["aggregate"], "receiptDigest": receipt["receiptDigest"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
