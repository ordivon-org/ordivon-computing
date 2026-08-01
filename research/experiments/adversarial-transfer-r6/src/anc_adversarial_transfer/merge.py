from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from .model import MatrixResult, TrialResult, TrialSpec
from .reporting import render_markdown
from .runner import _decisions, _summary


def _trial(value: Mapping[str, Any]) -> TrialResult:
    spec = TrialSpec(
        trial_id=str(value["trialId"]),
        model=str(value["model"]),
        profile=str(value["profile"]),
        attack_id=str(value["attackId"]),
        attack_path=str(value["attackPath"]),
        output_path=str(value["outputPath"]),
    )
    return TrialResult(
        spec=spec,
        status=str(value["status"]),
        source_revision=str(value["sourceRevision"]),
        host_revision=str(value["hostRevision"]),
        runtime_catalog_digest=value.get("runtimeCatalogDigest"),
        tool_definition_digest=value.get("toolDefinitionDigest"),
        committed_tool_catalog_digest=value.get("committedToolCatalogDigest"),
        context_digest=value.get("contextDigest"),
        omitted_context_blocks=tuple(value["omittedContextBlocks"]),
        stop_code=value.get("stopCode"),
        stop_detail=value.get("stopDetail"),
        model_calls=int(value["modelCalls"]),
        tool_calls=int(value["toolCalls"]),
        usage=value["usage"],
        proposed_calls=tuple(value["proposedCalls"]),
        observations=tuple(value["observations"]),
        authorized_utility=bool(value["authorizedUtility"]),
        attack_objective_success=bool(value["attackObjectiveSuccess"]),
        secret_read_attempted=bool(value["secretReadAttempted"]),
        secret_read_observed=bool(value["secretReadObserved"]),
        secret_leaked=bool(value["secretLeaked"]),
        outbox_changed=bool(value["outboxChanged"]),
        registry_changed=bool(value["registryChanged"]),
        memory_changed=bool(value["memoryChanged"]),
        unauthorized_mutation_observed=bool(value["unauthorizedMutationObserved"]),
        opaque_exec_attempted=bool(value["opaqueExecAttempted"]),
        opaque_exec_observed=bool(value["opaqueExecObserved"]),
        false_completion=bool(value["falseCompletion"]),
        host_verifier_accepted=bool(value["hostVerifierAccepted"]),
        completion_reason_code=value.get("completionReasonCode"),
        final_task_state=value.get("finalTaskState"),
        candidate_summary=value.get("candidateSummary"),
        output_digest=value.get("outputDigest"),
        diff_digest=value.get("diffDigest"),
        hard_failures=tuple(value["hardFailures"]),
        error=value.get("error"),
    )


def merge_parts(paths: tuple[Path, ...], *, expected_trials: int) -> MatrixResult:
    if not paths:
        raise ValueError("no R6 result parts supplied")
    source_revision: str | None = None
    host_revision: str | None = None
    runtime_endpoint: str | None = None
    retained: dict[str, TrialResult] = {}
    for path in sorted(paths):
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("kind") != "anc.adversarial-transfer-result":
            raise ValueError(f"not an R6 result part: {path}")
        current = (
            str(value["sourceRevision"]),
            str(value["hostRevision"]),
            str(value["runtimeEndpoint"]),
        )
        if source_revision is None:
            source_revision, host_revision, runtime_endpoint = current
        elif current != (source_revision, host_revision, runtime_endpoint):
            raise ValueError(f"result identity drift in {path}: {current}")
        for raw in value["trials"]:
            trial = _trial(raw)
            existing = retained.get(trial.spec.trial_id)
            if existing is not None and existing.to_dict() != trial.to_dict():
                raise ValueError(f"conflicting duplicate Trial: {trial.spec.trial_id}")
            retained[trial.spec.trial_id] = trial
    if len(retained) != expected_trials:
        raise ValueError(
            f"merged Trial count differs: expected {expected_trials}, got {len(retained)}"
        )
    assert source_revision is not None
    assert host_revision is not None
    assert runtime_endpoint is not None
    trials = tuple(retained[key] for key in sorted(retained))
    return MatrixResult(
        source_revision=source_revision,
        host_revision=host_revision,
        runtime_endpoint=runtime_endpoint,
        trials=trials,
        summary=_summary(trials),
        decisions=_decisions(trials),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge independently executed R6 result parts")
    parser.add_argument("--parts", type=Path, required=True)
    parser.add_argument("--expected-trials", type=int, default=28)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = tuple(args.parts.glob("*.json"))
    result = merge_parts(paths, expected_trials=args.expected_trials)
    payload = result.to_dict()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.report.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
