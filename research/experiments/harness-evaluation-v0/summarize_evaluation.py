#!/usr/bin/env python3
"""Aggregate Track R records without inventing a cross-task leaderboard."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
from statistics import fmean
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
VALIDATOR_PATH = ROOT / "validate_evaluation_evidence.py"
P0_VALIDATOR_PATH = ROOT / "validate_p0_artifacts.py"


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


records_validator = _load_module("track_r_records", VALIDATOR_PATH)
p0_validator = _load_module("track_r_p0", P0_VALIDATOR_PATH)


def canonical_digest(value: Any) -> str:
    content = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(content).hexdigest()


def record_identity(document: dict[str, Any]) -> str:
    kind = document["kind"]
    if kind == "ordivon.evaluation-task":
        return f"{document['taskId']}@{document['taskVersion']}"
    if kind in {"ordivon.evaluation-trial", "ordivon.evaluation-result"}:
        return document["trialId"]
    if kind == "ordivon.evaluation-failure":
        return document["failureId"]
    raise ValueError(f"unsupported record kind: {kind}")


def record_set_digest(documents: Iterable[dict[str, Any]]) -> str:
    entries = sorted(
        (
            {
                "kind": document["kind"],
                "identity": record_identity(document),
                "payloadDigest": document["integrity"]["payloadDigest"],
            }
            for document in documents
        ),
        key=lambda item: (item["kind"], item["identity"], item["payloadDigest"]),
    )
    return canonical_digest(entries)


def metric_statistics(values: list[int | float | None]) -> dict[str, int | float | None]:
    observed = [value for value in values if value is not None]
    if not observed:
        return {
            "observedCount": 0,
            "nullCount": len(values),
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    mean = fmean(observed)
    if all(isinstance(value, int) for value in observed):
        rendered_mean: int | float = round(mean, 6)
    else:
        rendered_mean = round(mean, 9)
    return {
        "observedCount": len(observed),
        "nullCount": len(values) - len(observed),
        "minimum": min(observed),
        "maximum": max(observed),
        "mean": rendered_mean,
    }


def group_configuration(trial: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    verifier = result["acceptance"]["verifier"]
    return {
        "taskRef": trial["taskRef"],
        "executionPath": trial["executionPath"],
        "model": trial["model"],
        "harness": trial["harness"],
        "sampling": trial["sampling"],
        "budget": trial["budget"],
        "systemSnapshotRef": trial["bindings"]["systemSnapshotRef"],
        "verifier": {
            "verifierId": verifier["verifierId"],
            "verifierRevision": verifier["verifierRevision"],
        },
    }


def summarize(
    documents: list[dict[str, Any]],
    *,
    summary_id: str,
    generated_at: str,
    suite_ref: dict[str, str],
    minimum_trials: int,
) -> dict[str, Any]:
    records_validator.validate_collection(documents)
    tasks = {
        (document["taskId"], document["taskVersion"]): document
        for document in documents
        if document["kind"] == "ordivon.evaluation-task"
    }
    trials = {
        document["trialId"]: document
        for document in documents
        if document["kind"] == "ordivon.evaluation-trial"
    }
    results = {
        document["trialId"]: document
        for document in documents
        if document["kind"] == "ordivon.evaluation-result"
    }
    failures = {
        document["failureId"]: document
        for document in documents
        if document["kind"] == "ordivon.evaluation-failure"
    }

    grouped: dict[str, dict[str, Any]] = {}
    metric_values: dict[str, dict[str, list[int | float | None]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for trial_id in sorted(results):
        result = results[trial_id]
        trial = trials[trial_id]
        configuration = group_configuration(trial, result)
        group_id = canonical_digest(configuration)
        group = grouped.setdefault(
            group_id,
            {
                "groupId": group_id,
                "configuration": configuration,
                "trialIds": [],
                "trialCount": 0,
                "acceptance": {"accepted": 0, "rejected": 0, "not_adjudicated": 0},
                "falseCompletions": 0,
                "stopCodes": {},
                "failureClasses": {},
                "failureCodes": {},
                "metrics": {},
            },
        )
        group["trialIds"].append(trial_id)
        group["trialCount"] += 1
        group["acceptance"][result["acceptance"]["status"]] += 1
        group["falseCompletions"] += int(result["acceptance"]["falseCompletion"])
        stop_codes = Counter(group["stopCodes"])
        stop_codes[result["stopCode"]] += 1
        group["stopCodes"] = dict(sorted(stop_codes.items()))
        failure_classes = Counter(group["failureClasses"])
        failure_codes = Counter(group["failureCodes"])
        for failure_id in result["failureRefs"]:
            failure = failures[failure_id]
            failure_classes[failure["failureClass"]] += 1
            failure_codes[f"{failure['failureClass']}.{failure['failureCode']}"] += 1
        group["failureClasses"] = dict(sorted(failure_classes.items()))
        group["failureCodes"] = dict(sorted(failure_codes.items()))
        for metric_name, value in result["metrics"].items():
            metric_values[group_id][metric_name].append(value)

    for group_id, group in grouped.items():
        group["trialIds"] = sorted(group["trialIds"])
        group["metrics"] = {
            metric_name: metric_statistics(values)
            for metric_name, values in sorted(metric_values[group_id].items())
        }

    groups = sorted(
        grouped.values(),
        key=lambda group: (
            group["configuration"]["taskRef"]["taskId"],
            group["configuration"]["taskRef"]["taskVersion"],
            group["configuration"]["executionPath"],
            group["groupId"],
        ),
    )
    task_groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for group in groups:
        task_ref = group["configuration"]["taskRef"]
        task_groups[(task_ref["taskId"], task_ref["taskVersion"])].append(group)

    comparison_candidates: list[dict[str, Any]] = []
    for (task_id, task_version), task_group_values in sorted(task_groups.items()):
        blockers: list[str] = []
        if len(task_group_values) < 2:
            blockers.append("fewer_than_two_configurations")
        if any(group["trialCount"] < minimum_trials for group in task_group_values):
            blockers.append("insufficient_trials_per_configuration")
        if any(
            group["configuration"]["systemSnapshotRef"] is None
            for group in task_group_values
        ):
            blockers.append("missing_system_snapshot")
        verifier_identities = {
            (
                group["configuration"]["verifier"]["verifierId"],
                group["configuration"]["verifier"]["verifierRevision"],
            )
            for group in task_group_values
        }
        if len(verifier_identities) > 1:
            blockers.append("verifier_identity_differs")
        comparison_candidates.append(
            {
                "taskRef": {"taskId": task_id, "taskVersion": task_version},
                "groupIds": sorted(group["groupId"] for group in task_group_values),
                "eligible": not blockers,
                "blockers": sorted(set(blockers)),
            }
        )

    summary = {
        "schemaVersion": 1,
        "kind": "ordivon.evaluation-summary",
        "summaryId": summary_id,
        "generatedAt": generated_at,
        "suite": suite_ref,
        "source": {
            "recordCount": len(documents),
            "recordSetDigest": record_set_digest(documents),
        },
        "inventory": {
            "tasks": len(tasks),
            "trials": len(trials),
            "results": len(results),
            "failures": len(failures),
        },
        "groups": groups,
        "comparisonCandidates": comparison_candidates,
        "policy": {
            "minimumTrialsPerGroup": minimum_trials,
            "globalScoreGenerated": False,
        },
        "limitations": [
            "Groups are descriptive unless comparisonCandidates marks the same Task and verifier configuration eligible.",
            "Missing metrics remain null and are excluded from means rather than converted to zero.",
            "This summary does not normalize Provider token accounting or compare heterogeneous workload families.",
        ],
        "integrity": {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": "sha256:" + "0" * 64,
        },
    }
    summary["integrity"]["payloadDigest"] = p0_validator.payload_digest(summary)
    p0_validator.validate_summary(summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--summary-id", required=True)
    parser.add_argument("--generated-at", required=True)
    parser.add_argument("--suite-path", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--minimum-trials", type=int, default=3)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.minimum_trials < 1:
        raise ValueError("minimum trials must be positive")
    loaded = records_validator.load_documents(args.paths)
    documents = [document for _, document in loaded]
    suite_path = args.suite_path.resolve()
    root = args.root.resolve()
    relative_suite = suite_path.relative_to(root).as_posix()
    suite_ref = {
        "path": relative_suite,
        "digest": p0_validator.file_digest(suite_path),
    }
    summary = summarize(
        documents,
        summary_id=args.summary_id,
        generated_at=args.generated_at,
        suite_ref=suite_ref,
        minimum_trials=args.minimum_trials,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"{args.output}: {summary['source']['recordCount']} records {summary['integrity']['payloadDigest']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
