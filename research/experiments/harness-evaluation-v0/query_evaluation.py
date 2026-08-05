#!/usr/bin/env python3
"""Query validated Track R evaluation records without a persistent data plane."""

from __future__ import annotations

import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
DEFAULT_RECORDS = ROOT / "dogfood-20260802"
DEFAULT_SUITE = ROOT / "suite-v1.json"
VALIDATOR_PATH = ROOT / "validate_evaluation_evidence.py"
SUMMARIZER_PATH = ROOT / "summarize_evaluation.py"
P0_VALIDATOR_PATH = ROOT / "validate_p0_artifacts.py"

KIND_ALIASES = {
    "task": "ordivon.evaluation-task",
    "trial": "ordivon.evaluation-trial",
    "result": "ordivon.evaluation-result",
    "failure": "ordivon.evaluation-failure",
}


def _load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


records_validator = _load_module("track_r_query_records", VALIDATOR_PATH)
summarizer = _load_module("track_r_query_summary", SUMMARIZER_PATH)
p0_validator = _load_module("track_r_query_p0", P0_VALIDATOR_PATH)


def emit_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def record_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    paths: list[Path] = []
    for directory in ("tasks", "trials", "results", "failures"):
        candidate = root / directory
        if candidate.is_dir():
            paths.extend(sorted(candidate.glob("*.json")))
    if not paths:
        paths.extend(sorted(root.rglob("*.json")))
    if not paths:
        raise ValueError(f"no evaluation records found under {root}")
    return paths


def load_records(root: Path) -> list[dict[str, Any]]:
    loaded = records_validator.load_documents(record_paths(root))
    documents = [document for _, document in loaded]
    records_validator.validate_collection(documents)
    return documents


def identity(document: dict[str, Any]) -> str:
    return summarizer.record_identity(document)


def make_summary(
    documents: list[dict[str, Any]],
    *,
    suite_path: Path,
    minimum_trials: int,
) -> dict[str, Any]:
    suite_path = suite_path.resolve(strict=True)
    repository_root = ROOT.parents[2]
    suite_ref = {
        "path": suite_path.relative_to(repository_root).as_posix(),
        "digest": p0_validator.file_digest(suite_path),
    }
    return summarizer.summarize(
        documents,
        summary_id="ordivon-evaluation-query",
        generated_at="1970-01-01T00:00:00Z",
        suite_ref=suite_ref,
        minimum_trials=minimum_trials,
    )


def compact(document: dict[str, Any]) -> dict[str, Any]:
    kind = document["kind"]
    if kind == "ordivon.evaluation-task":
        return {
            "kind": kind,
            "identity": identity(document),
            "taskId": document["taskId"],
            "taskVersion": document["taskVersion"],
            "family": document["family"],
            "objective": document["objective"],
            "payloadDigest": document["integrity"]["payloadDigest"],
        }
    if kind == "ordivon.evaluation-trial":
        return {
            "kind": kind,
            "identity": identity(document),
            "trialId": document["trialId"],
            "taskRef": document["taskRef"],
            "executionPath": document["executionPath"],
            "providerId": document["model"]["providerId"],
            "modelId": document["model"]["modelId"],
            "harnessId": document["harness"]["harnessId"],
            "harnessRevision": document["harness"]["harnessRevision"],
            "systemManifestRef": document["bindings"].get("systemManifestRef"),
            "payloadDigest": document["integrity"]["payloadDigest"],
        }
    if kind == "ordivon.evaluation-result":
        return {
            "kind": kind,
            "identity": identity(document),
            "trialId": document["trialId"],
            "acceptance": document["acceptance"]["status"],
            "falseCompletion": document["acceptance"]["falseCompletion"],
            "stopCode": document["stopCode"],
            "failureRefs": document["failureRefs"],
            "payloadDigest": document["integrity"]["payloadDigest"],
        }
    if kind == "ordivon.evaluation-failure":
        return {
            "kind": kind,
            "identity": identity(document),
            "failureId": document["failureId"],
            "trialId": document["trialId"],
            "failureClass": document["failureClass"],
            "failureCode": document["failureCode"],
            "responsibleBoundary": document["responsibleBoundary"],
            "recovered": document["recovered"],
            "duplicateEffect": document["duplicateEffect"],
            "humanIntervention": document["humanIntervention"],
            "payloadDigest": document["integrity"]["payloadDigest"],
        }
    raise ValueError(f"unsupported evaluation record kind: {kind}")


def status(
    documents: list[dict[str, Any]],
    *,
    suite_path: Path,
    minimum_trials: int,
) -> dict[str, Any]:
    summary = make_summary(
        documents,
        suite_path=suite_path,
        minimum_trials=minimum_trials,
    )
    results = [
        document
        for document in documents
        if document["kind"] == "ordivon.evaluation-result"
    ]
    failures = [
        document
        for document in documents
        if document["kind"] == "ordivon.evaluation-failure"
    ]
    acceptance = Counter(document["acceptance"]["status"] for document in results)
    failure_classes = Counter(document["failureClass"] for document in failures)
    candidates = summary["comparisonCandidates"]
    return {
        "schemaVersion": 1,
        "kind": "ordivon.evaluation-query-status",
        "source": summary["source"],
        "inventory": summary["inventory"],
        "acceptance": dict(sorted(acceptance.items())),
        "failureClasses": dict(sorted(failure_classes.items())),
        "configurationGroups": len(summary["groups"]),
        "comparisonCandidates": len(candidates),
        "eligibleComparisons": sum(bool(item["eligible"]) for item in candidates),
        "globalScoreGenerated": summary["policy"]["globalScoreGenerated"],
    }


def list_records(
    documents: Iterable[dict[str, Any]],
    *,
    kind: str | None,
) -> list[dict[str, Any]]:
    expected = None if kind in (None, "all") else KIND_ALIASES[kind]
    selected = [
        compact(document)
        for document in documents
        if expected is None or document["kind"] == expected
    ]
    return sorted(selected, key=lambda item: (item["kind"], item["identity"]))


def show_records(
    documents: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    failure_ids: set[str] = set()
    for document in documents:
        kind = document["kind"]
        matches = identity(document) == query
        if kind == "ordivon.evaluation-task":
            matches = matches or document["taskId"] == query
        elif kind in {"ordivon.evaluation-trial", "ordivon.evaluation-result"}:
            matches = matches or document["trialId"] == query
        elif kind == "ordivon.evaluation-failure":
            matches = matches or document["trialId"] == query
        if matches:
            selected.append(document)
            if kind == "ordivon.evaluation-result":
                failure_ids.update(document["failureRefs"])
    for document in documents:
        if (
            document["kind"] == "ordivon.evaluation-failure"
            and document["failureId"] in failure_ids
            and document not in selected
        ):
            selected.append(document)
    if not selected:
        raise ValueError(f"evaluation identity not found: {query}")
    return sorted(selected, key=lambda document: (document["kind"], identity(document)))


def filter_failures(
    documents: Iterable[dict[str, Any]],
    *,
    failure_class: str | None,
    boundary: str | None,
    trial_id: str | None,
    recovered: str | None,
) -> list[dict[str, Any]]:
    expected_recovered = None if recovered is None else recovered == "true"
    selected = []
    for document in documents:
        if document["kind"] != "ordivon.evaluation-failure":
            continue
        if failure_class is not None and document["failureClass"] != failure_class:
            continue
        if boundary is not None and document["responsibleBoundary"] != boundary:
            continue
        if trial_id is not None and document["trialId"] != trial_id:
            continue
        if (
            expected_recovered is not None
            and document["recovered"] != expected_recovered
        ):
            continue
        selected.append(compact(document))
    return sorted(selected, key=lambda item: item["failureId"])


def comparison_readiness(
    documents: list[dict[str, Any]],
    *,
    suite_path: Path,
    minimum_trials: int,
) -> dict[str, Any]:
    summary = make_summary(
        documents,
        suite_path=suite_path,
        minimum_trials=minimum_trials,
    )
    candidates = summary["comparisonCandidates"]
    blocker_counts = Counter(
        blocker for candidate in candidates for blocker in candidate["blockers"]
    )
    return {
        "schemaVersion": 1,
        "kind": "ordivon.evaluation-comparison-readiness",
        "source": summary["source"],
        "minimumTrialsPerGroup": minimum_trials,
        "configurationGroups": summary["groups"],
        "candidates": candidates,
        "blockerCounts": dict(sorted(blocker_counts.items())),
        "eligibleComparisons": sum(bool(item["eligible"]) for item in candidates),
        "globalScoreGenerated": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query validated Track R records as machine-readable JSON."
    )
    parser.add_argument("--records", type=Path, default=DEFAULT_RECORDS)
    parser.add_argument("--suite", type=Path, default=DEFAULT_SUITE)
    parser.add_argument("--minimum-trials", type=int, default=3)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--kind", choices=["all", *KIND_ALIASES], default="all")

    show_parser = subparsers.add_parser("show")
    show_parser.add_argument("identity")

    failure_parser = subparsers.add_parser("failures")
    failure_parser.add_argument("--class", dest="failure_class")
    failure_parser.add_argument("--boundary")
    failure_parser.add_argument("--trial-id")
    failure_parser.add_argument("--recovered", choices=["true", "false"])

    subparsers.add_parser("comparison-readiness")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.minimum_trials < 1:
        raise ValueError("minimum trials must be positive")
    documents = load_records(args.records.resolve(strict=True))
    if args.command == "status":
        output = status(
            documents,
            suite_path=args.suite,
            minimum_trials=args.minimum_trials,
        )
    elif args.command == "list":
        output = {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-query-list",
            "records": list_records(documents, kind=args.kind),
        }
    elif args.command == "show":
        output = {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-query-show",
            "query": args.identity,
            "records": show_records(documents, args.identity),
        }
    elif args.command == "failures":
        output = {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-query-failures",
            "records": filter_failures(
                documents,
                failure_class=args.failure_class,
                boundary=args.boundary,
                trial_id=args.trial_id,
                recovered=args.recovered,
            ),
        }
    elif args.command == "comparison-readiness":
        output = comparison_readiness(
            documents,
            suite_path=args.suite,
            minimum_trials=args.minimum_trials,
        )
    else:
        raise AssertionError(f"unsupported command: {args.command}")
    emit_json(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
