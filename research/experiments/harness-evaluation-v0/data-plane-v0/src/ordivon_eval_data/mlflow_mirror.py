from __future__ import annotations

import json
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

import duckdb

from .canonical import sha256_value, write_json
from .projection import _current_generation, validate_projection

EXPERIMENT_NAME = "ordivon-harness-evaluation-v0"


def check_server_health(tracking_uri: str, *, timeout_seconds: float = 10.0) -> None:
    uri = tracking_uri.rstrip("/") + "/health"
    request = urllib.request.Request(uri, method="GET")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
        if response.status != 200:
            raise ValueError(f"MLflow health check failed: status={response.status}")


def _parse_json(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        parsed = json.loads(value)
        if isinstance(parsed, dict):
            return parsed
    raise ValueError("expected a JSON object from the evaluation projection")


def _load_trials(output_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = validate_projection(output_root)
    generation = _current_generation(output_root)
    database_path = generation / manifest["database"]["path"]
    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        rows = connection.execute(
            """
            SELECT
                t.trial_id,
                t.task_id,
                t.task_version,
                t.execution_path,
                t.started_at_ms,
                t.completed_at_ms,
                t.provider_id,
                t.model_id,
                t.model_revision,
                t.adapter_revision,
                t.harness_id,
                t.harness_revision,
                t.harness_manifest_digest,
                t.system_manifest_ref,
                t.system_snapshot_ref,
                t.source_revision,
                t.tool_catalog_digest,
                t.verifier_id,
                t.verifier_revision,
                t.configuration_group_id,
                t.comparison_eligible,
                t.comparison_blockers_json,
                t.payload_digest AS trial_payload_digest,
                t.record_json AS trial_record_json,
                k.payload_digest AS task_payload_digest,
                k.record_json AS task_record_json,
                r.acceptance_status,
                r.false_completion,
                r.verifier_status,
                r.stop_code,
                r.payload_digest AS result_payload_digest,
                r.record_json AS result_record_json
            FROM trials t
            JOIN tasks k ON (t.task_id, t.task_version) = (k.task_id, k.task_version)
            JOIN results r USING (trial_id)
            ORDER BY t.trial_id
            """
        ).fetchall()
        columns = [description[0] for description in connection.description]
        trials: list[dict[str, Any]] = []
        for row in rows:
            value = dict(zip(columns, row, strict=True))
            trial_id = value["trial_id"]
            metric_rows = connection.execute(
                """
                SELECT metric_name, metric_value, is_missing
                FROM result_metrics
                WHERE trial_id = ?
                ORDER BY metric_name
                """,
                [trial_id],
            ).fetchall()
            failure_rows = connection.execute(
                """
                SELECT failure_id, payload_digest, record_json
                FROM failures
                WHERE trial_id = ?
                ORDER BY failure_id
                """,
                [trial_id],
            ).fetchall()
            artifact_rows = connection.execute(
                """
                SELECT artifact_ref, artifact_kind, digest, valid
                FROM result_artifacts
                WHERE trial_id = ?
                ORDER BY ordinal
                """,
                [trial_id],
            ).fetchall()
            trials.append(
                {
                    "identity": value,
                    "task": _parse_json(value["task_record_json"]),
                    "trial": _parse_json(value["trial_record_json"]),
                    "result": _parse_json(value["result_record_json"]),
                    "metrics": {
                        name: None if missing else float(metric_value)
                        for name, metric_value, missing in metric_rows
                    },
                    "failures": [
                        {
                            "failureId": failure_id,
                            "payloadDigest": payload_digest,
                            "record": _parse_json(record_json),
                        }
                        for failure_id, payload_digest, record_json in failure_rows
                    ],
                    "artifacts": [
                        {
                            "ref": artifact_ref,
                            "kind": artifact_kind,
                            "digest": digest,
                            "valid": valid,
                        }
                        for artifact_ref, artifact_kind, digest, valid in artifact_rows
                    ],
                }
            )
        return manifest, trials
    finally:
        connection.close()


def _string(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _source_set_digest(trial: dict[str, Any]) -> str:
    identity = trial["identity"]
    return sha256_value(
        {
            "task": identity["task_payload_digest"],
            "trial": identity["trial_payload_digest"],
            "result": identity["result_payload_digest"],
            "failures": [failure["payloadDigest"] for failure in trial["failures"]],
        }
    )


def _tags(trial: dict[str, Any], projection_manifest: dict[str, Any]) -> dict[str, str]:
    value = trial["identity"]
    return {
        "mlflow.runName": value["trial_id"],
        "ordivon.trial_id": value["trial_id"],
        "ordivon.task_id": value["task_id"],
        "ordivon.task_version": _string(value["task_version"]),
        "ordivon.execution_path": value["execution_path"],
        "ordivon.provider_id": value["provider_id"],
        "ordivon.model_id": value["model_id"],
        "ordivon.model_revision": _string(value["model_revision"]),
        "ordivon.adapter_revision": value["adapter_revision"],
        "ordivon.harness_id": value["harness_id"],
        "ordivon.harness_revision": value["harness_revision"],
        "ordivon.harness_manifest_digest": _string(value["harness_manifest_digest"]),
        "ordivon.system_manifest_ref": _string(value["system_manifest_ref"]),
        "ordivon.system_snapshot_ref": _string(value["system_snapshot_ref"]),
        "ordivon.source_revision": value["source_revision"],
        "ordivon.tool_catalog_digest": _string(value["tool_catalog_digest"]),
        "ordivon.verifier_id": _string(value["verifier_id"]),
        "ordivon.verifier_revision": _string(value["verifier_revision"]),
        "ordivon.acceptance_status": value["acceptance_status"],
        "ordivon.verifier_status": value["verifier_status"],
        "ordivon.stop_code": value["stop_code"],
        "ordivon.configuration_group_id": _string(value["configuration_group_id"]),
        "ordivon.comparison_eligible": _string(value["comparison_eligible"]),
        "ordivon.comparison_blockers": _string(value["comparison_blockers_json"]),
        "ordivon.source_set_digest": _source_set_digest(trial),
        "ordivon.projection_generation": projection_manifest["generationId"],
        "ordivon.mirror_authority": "downstream_projection_only",
    }


def _metric_values(trial: dict[str, Any]) -> dict[str, float]:
    identity = trial["identity"]
    failures = trial["failures"]
    metrics = {
        f"ordivon.{name}": value for name, value in trial["metrics"].items() if value is not None
    }
    metrics.update(
        {
            "ordivon.false_completion": 1.0 if identity["false_completion"] else 0.0,
            "ordivon.failure_count": float(len(failures)),
            "ordivon.duplicate_effect_count": float(
                sum(1 for failure in failures if failure["record"]["duplicateEffect"])
            ),
            "ordivon.recovered_failure_count": float(
                sum(1 for failure in failures if failure["record"]["recovered"])
            ),
            "ordivon.human_intervention_failure_count": float(
                sum(1 for failure in failures if failure["record"]["humanIntervention"])
            ),
        }
    )
    return metrics


def mirror(
    output_root: Path,
    tracking_uri: str,
    *,
    experiment_name: str = EXPERIMENT_NAME,
    artifact_location: str | None = None,
) -> dict[str, Any]:
    from mlflow import MlflowClient

    projection_manifest, trials = _load_trials(output_root)
    client = MlflowClient(tracking_uri=tracking_uri)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = client.create_experiment(
            experiment_name,
            artifact_location=artifact_location,
        )
    else:
        experiment_id = experiment.experiment_id
        if artifact_location is not None and experiment.artifact_location != artifact_location:
            raise ValueError(
                "MLflow experiment Artifact location differs; "
                f"expected={artifact_location}, observed={experiment.artifact_location}"
            )

    existing_by_trial: dict[str, list[Any]] = {}
    for run in client.search_runs([experiment_id], max_results=5000):
        trial_id = run.data.tags.get("ordivon.trial_id")
        if trial_id:
            existing_by_trial.setdefault(trial_id, []).append(run)

    created = 0
    reused = 0
    run_ids: dict[str, str] = {}
    for trial in trials:
        identity = trial["identity"]
        trial_id = identity["trial_id"]
        expected_tags = _tags(trial, projection_manifest)
        existing = existing_by_trial.get(trial_id, [])
        if len(existing) > 1:
            raise ValueError(f"multiple MLflow Runs claim one Ordivon Trial: {trial_id}")
        if existing:
            observed = existing[0].data.tags.get("ordivon.source_set_digest")
            expected = expected_tags["ordivon.source_set_digest"]
            if observed != expected:
                raise ValueError(
                    f"MLflow Trial identity conflict for {trial_id}; "
                    f"expected={expected}, observed={observed}"
                )
            run_ids[trial_id] = existing[0].info.run_id
            reused += 1
            continue

        create_kwargs: dict[str, Any] = {"tags": expected_tags}
        if identity["started_at_ms"] is not None:
            create_kwargs["start_time"] = int(identity["started_at_ms"])
        run = client.create_run(experiment_id, **create_kwargs)
        run_id = run.info.run_id
        run_ids[trial_id] = run_id
        try:
            parameters = {
                "execution_path": identity["execution_path"],
                "provider_id": identity["provider_id"],
                "model_id": identity["model_id"],
                "harness_id": identity["harness_id"],
                "harness_revision": identity["harness_revision"],
                "task_id": identity["task_id"],
                "task_version": identity["task_version"],
            }
            for key, value in parameters.items():
                client.log_param(run_id, key, _string(value))
            for key, value in _metric_values(trial).items():
                metric_kwargs: dict[str, Any] = {}
                if identity["completed_at_ms"] is not None:
                    metric_kwargs["timestamp"] = int(identity["completed_at_ms"])
                client.log_metric(run_id, key, value, **metric_kwargs)
            with tempfile.TemporaryDirectory(prefix="ordivon-mlflow-mirror-") as temporary:
                artifact_root = Path(temporary)
                write_json(artifact_root / "task.json", trial["task"])
                write_json(artifact_root / "trial.json", trial["trial"])
                write_json(artifact_root / "result.json", trial["result"])
                write_json(
                    artifact_root / "failures.json",
                    [failure["record"] for failure in trial["failures"]],
                )
                write_json(artifact_root / "artifact-references.json", trial["artifacts"])
                write_json(
                    artifact_root / "projection-reference.json",
                    {
                        "generationId": projection_manifest["generationId"],
                        "manifestPayloadDigest": projection_manifest["integrity"]["payloadDigest"],
                        "sourceRevision": projection_manifest["source"]["revision"],
                    },
                )
                for path in sorted(artifact_root.iterdir()):
                    client.log_artifact(run_id, str(path), artifact_path="ordivon")
            terminate_kwargs: dict[str, Any] = {"status": "FINISHED"}
            if identity["completed_at_ms"] is not None:
                terminate_kwargs["end_time"] = int(identity["completed_at_ms"])
            client.set_terminated(run_id, **terminate_kwargs)
            created += 1
        except Exception:
            client.set_terminated(run_id, status="FAILED")
            raise

    final_runs = client.search_runs([experiment_id], max_results=5000)
    mirrored = [run for run in final_runs if run.data.tags.get("ordivon.trial_id")]
    if len(mirrored) != len(trials):
        raise ValueError(
            f"MLflow mirrored Trial count differs; expected={len(trials)}, observed={len(mirrored)}"
        )
    return {
        "experimentId": experiment_id,
        "experimentName": experiment_name,
        "projectionGeneration": projection_manifest["generationId"],
        "trials": len(trials),
        "created": created,
        "reused": reused,
        "runIds": run_ids,
    }
