from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb

from . import __version__
from .canonical import (
    canonical_text,
    file_digest,
    sha256_value,
    validate_integrity,
    with_integrity,
    write_json,
)

EVALUATION_RELATIVE = Path("research/experiments/harness-evaluation-v0")
DOGFOOD_RELATIVE = EVALUATION_RELATIVE / "dogfood-20260802"
BASELINE_RELATIVE = EVALUATION_RELATIVE / "baselines/p0-20260804"
SUITE_RELATIVE = EVALUATION_RELATIVE / "suite-v1.json"
SOURCE_REVISION_FILE = "ORDIVON_SOURCE_REVISION"


@dataclass(frozen=True)
class TableSpec:
    columns: tuple[str, ...]
    create_sql: str
    order_columns: tuple[str, ...]


TABLE_SPECS: dict[str, TableSpec] = {
    "tasks": TableSpec(
        columns=(
            "task_id",
            "task_version",
            "family",
            "objective",
            "verifier_id",
            "verifier_revision",
            "source_path",
            "payload_digest",
            "record_json",
        ),
        create_sql="""
            CREATE TABLE tasks (
                task_id VARCHAR NOT NULL,
                task_version INTEGER NOT NULL,
                family VARCHAR NOT NULL,
                objective VARCHAR NOT NULL,
                verifier_id VARCHAR,
                verifier_revision VARCHAR,
                source_path VARCHAR NOT NULL,
                payload_digest VARCHAR NOT NULL,
                record_json JSON NOT NULL,
                PRIMARY KEY (task_id, task_version)
            )
        """,
        order_columns=("task_id", "task_version"),
    ),
    "trials": TableSpec(
        columns=(
            "trial_id",
            "task_id",
            "task_version",
            "execution_path",
            "started_at_ms",
            "completed_at_ms",
            "provider_id",
            "model_id",
            "model_revision",
            "adapter_revision",
            "harness_id",
            "harness_revision",
            "harness_manifest_digest",
            "system_manifest_ref",
            "system_snapshot_ref",
            "source_revision",
            "tool_catalog_digest",
            "verifier_id",
            "verifier_revision",
            "configuration_group_id",
            "comparison_eligible",
            "comparison_blockers_json",
            "source_path",
            "payload_digest",
            "record_json",
        ),
        create_sql="""
            CREATE TABLE trials (
                trial_id VARCHAR PRIMARY KEY,
                task_id VARCHAR NOT NULL,
                task_version INTEGER NOT NULL,
                execution_path VARCHAR NOT NULL,
                started_at_ms BIGINT,
                completed_at_ms BIGINT,
                provider_id VARCHAR NOT NULL,
                model_id VARCHAR NOT NULL,
                model_revision VARCHAR,
                adapter_revision VARCHAR NOT NULL,
                harness_id VARCHAR NOT NULL,
                harness_revision VARCHAR NOT NULL,
                harness_manifest_digest VARCHAR,
                system_manifest_ref VARCHAR,
                system_snapshot_ref VARCHAR,
                source_revision VARCHAR NOT NULL,
                tool_catalog_digest VARCHAR,
                verifier_id VARCHAR,
                verifier_revision VARCHAR,
                configuration_group_id VARCHAR,
                comparison_eligible BOOLEAN NOT NULL,
                comparison_blockers_json JSON NOT NULL,
                source_path VARCHAR NOT NULL,
                payload_digest VARCHAR NOT NULL,
                record_json JSON NOT NULL
            )
        """,
        order_columns=("trial_id",),
    ),
    "results": TableSpec(
        columns=(
            "trial_id",
            "task_id",
            "task_version",
            "acceptance_status",
            "false_completion",
            "verifier_status",
            "verifier_id",
            "verifier_revision",
            "stop_code",
            "trace_ref",
            "trace_digest",
            "trace_event_count",
            "source_path",
            "payload_digest",
            "record_json",
        ),
        create_sql="""
            CREATE TABLE results (
                trial_id VARCHAR PRIMARY KEY,
                task_id VARCHAR NOT NULL,
                task_version INTEGER NOT NULL,
                acceptance_status VARCHAR NOT NULL,
                false_completion BOOLEAN NOT NULL,
                verifier_status VARCHAR NOT NULL,
                verifier_id VARCHAR,
                verifier_revision VARCHAR,
                stop_code VARCHAR NOT NULL,
                trace_ref VARCHAR,
                trace_digest VARCHAR,
                trace_event_count BIGINT,
                source_path VARCHAR NOT NULL,
                payload_digest VARCHAR NOT NULL,
                record_json JSON NOT NULL
            )
        """,
        order_columns=("trial_id",),
    ),
    "failures": TableSpec(
        columns=(
            "failure_id",
            "trial_id",
            "failure_class",
            "failure_code",
            "responsible_boundary",
            "recoverable",
            "recovered",
            "duplicate_effect",
            "human_intervention",
            "description",
            "minimal_correction",
            "correction_cost",
            "source_path",
            "payload_digest",
            "record_json",
        ),
        create_sql="""
            CREATE TABLE failures (
                failure_id VARCHAR PRIMARY KEY,
                trial_id VARCHAR NOT NULL,
                failure_class VARCHAR NOT NULL,
                failure_code VARCHAR NOT NULL,
                responsible_boundary VARCHAR NOT NULL,
                recoverable BOOLEAN NOT NULL,
                recovered BOOLEAN NOT NULL,
                duplicate_effect BOOLEAN NOT NULL,
                human_intervention BOOLEAN NOT NULL,
                description VARCHAR NOT NULL,
                minimal_correction VARCHAR NOT NULL,
                correction_cost VARCHAR NOT NULL,
                source_path VARCHAR NOT NULL,
                payload_digest VARCHAR NOT NULL,
                record_json JSON NOT NULL
            )
        """,
        order_columns=("failure_id",),
    ),
    "result_metrics": TableSpec(
        columns=("trial_id", "metric_name", "metric_value", "is_missing"),
        create_sql="""
            CREATE TABLE result_metrics (
                trial_id VARCHAR NOT NULL,
                metric_name VARCHAR NOT NULL,
                metric_value DOUBLE,
                is_missing BOOLEAN NOT NULL,
                PRIMARY KEY (trial_id, metric_name)
            )
        """,
        order_columns=("trial_id", "metric_name"),
    ),
    "result_artifacts": TableSpec(
        columns=("trial_id", "ordinal", "artifact_ref", "artifact_kind", "digest", "valid"),
        create_sql="""
            CREATE TABLE result_artifacts (
                trial_id VARCHAR NOT NULL,
                ordinal INTEGER NOT NULL,
                artifact_ref VARCHAR NOT NULL,
                artifact_kind VARCHAR NOT NULL,
                digest VARCHAR,
                valid BOOLEAN NOT NULL,
                PRIMARY KEY (trial_id, ordinal)
            )
        """,
        order_columns=("trial_id", "ordinal"),
    ),
    "verifier_assertions": TableSpec(
        columns=("trial_id", "ordinal", "assertion_id", "status", "evidence_refs_json"),
        create_sql="""
            CREATE TABLE verifier_assertions (
                trial_id VARCHAR NOT NULL,
                ordinal INTEGER NOT NULL,
                assertion_id VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                evidence_refs_json JSON NOT NULL,
                PRIMARY KEY (trial_id, ordinal)
            )
        """,
        order_columns=("trial_id", "ordinal"),
    ),
    "trial_source_evidence": TableSpec(
        columns=("trial_id", "ordinal", "repository_id", "path", "digest"),
        create_sql="""
            CREATE TABLE trial_source_evidence (
                trial_id VARCHAR NOT NULL,
                ordinal INTEGER NOT NULL,
                repository_id VARCHAR NOT NULL,
                path VARCHAR NOT NULL,
                digest VARCHAR NOT NULL,
                PRIMARY KEY (trial_id, ordinal)
            )
        """,
        order_columns=("trial_id", "ordinal"),
    ),
    "system_manifests": TableSpec(
        columns=(
            "manifest_id",
            "captured_at",
            "system_snapshot_path",
            "system_snapshot_digest",
            "provider_id",
            "model_id",
            "model_revision",
            "adapter_revision",
            "secrets_included",
            "raw_reasoning_required",
            "source_path",
            "payload_digest",
            "record_json",
        ),
        create_sql="""
            CREATE TABLE system_manifests (
                manifest_id VARCHAR PRIMARY KEY,
                captured_at VARCHAR NOT NULL,
                system_snapshot_path VARCHAR NOT NULL,
                system_snapshot_digest VARCHAR NOT NULL,
                provider_id VARCHAR,
                model_id VARCHAR,
                model_revision VARCHAR,
                adapter_revision VARCHAR,
                secrets_included BOOLEAN NOT NULL,
                raw_reasoning_required BOOLEAN NOT NULL,
                source_path VARCHAR NOT NULL,
                payload_digest VARCHAR NOT NULL,
                record_json JSON NOT NULL
            )
        """,
        order_columns=("manifest_id",),
    ),
    "suite_tasks": TableSpec(
        columns=(
            "suite_id",
            "suite_version",
            "family_id",
            "family_status",
            "family_priority",
            "task_id",
            "task_version",
            "repository_id",
            "path",
            "digest",
        ),
        create_sql="""
            CREATE TABLE suite_tasks (
                suite_id VARCHAR NOT NULL,
                suite_version INTEGER NOT NULL,
                family_id VARCHAR NOT NULL,
                family_status VARCHAR NOT NULL,
                family_priority VARCHAR NOT NULL,
                task_id VARCHAR NOT NULL,
                task_version INTEGER NOT NULL,
                repository_id VARCHAR NOT NULL,
                path VARCHAR NOT NULL,
                digest VARCHAR,
                PRIMARY KEY (suite_id, suite_version, family_id, task_id, task_version)
            )
        """,
        order_columns=("suite_id", "suite_version", "family_id", "task_id", "task_version"),
    ),
    "projection_records": TableSpec(
        columns=(
            "record_kind",
            "record_id",
            "collection",
            "source_path",
            "file_digest",
            "payload_digest",
        ),
        create_sql="""
            CREATE TABLE projection_records (
                record_kind VARCHAR NOT NULL,
                record_id VARCHAR NOT NULL,
                collection VARCHAR NOT NULL,
                source_path VARCHAR NOT NULL,
                file_digest VARCHAR NOT NULL,
                payload_digest VARCHAR,
                PRIMARY KEY (source_path)
            )
        """,
        order_columns=("source_path",),
    ),
}


def _json(value: Any) -> str:
    return canonical_text(value)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected an object: {path}")
    return value


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _source_revision(source_root: Path) -> str:
    marker = source_root / SOURCE_REVISION_FILE
    if marker.is_file():
        revision = marker.read_text(encoding="utf-8").strip()
    else:
        result = subprocess.run(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        revision = result.stdout.strip()
    if len(revision) != 40 or any(character not in "0123456789abcdef" for character in revision):
        raise ValueError(f"invalid source revision: {revision!r}")
    return revision


def _dogfood_paths(source_root: Path) -> list[Path]:
    root = source_root / DOGFOOD_RELATIVE
    paths: list[Path] = []
    for directory in ("tasks", "trials", "results", "failures"):
        paths.extend(sorted((root / directory).glob("*.json")))
    return paths


def _control_paths(source_root: Path) -> list[Path]:
    return [
        source_root / SUITE_RELATIVE,
        source_root / BASELINE_RELATIVE / "system-manifest.json",
        source_root / BASELINE_RELATIVE / "dogfood-summary.json",
        source_root / BASELINE_RELATIVE / "component-baseline.json",
        source_root / BASELINE_RELATIVE / "closeout.json",
    ]


def validate_source(source_root: Path) -> None:
    evaluation_root = source_root / EVALUATION_RELATIVE
    records = _dogfood_paths(source_root)
    if len(records) != 33:
        raise ValueError(f"expected 33 curated dogfood records, found {len(records)}")
    subprocess.run(
        [
            sys.executable,
            str(evaluation_root / "validate_evaluation_evidence.py"),
            *[str(path) for path in records],
        ],
        cwd=source_root,
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(evaluation_root / "validate_p0_artifacts.py"),
            "--root",
            str(source_root),
            str(source_root / SUITE_RELATIVE),
            str(source_root / BASELINE_RELATIVE),
        ],
        cwd=source_root,
        check=True,
    )


def _record_id(document: dict[str, Any]) -> str:
    kind = document.get("kind")
    if kind == "ordivon.evaluation-task":
        return f"{document['taskId']}@{document['taskVersion']}"
    if kind in {"ordivon.evaluation-trial", "ordivon.evaluation-result"}:
        return str(document["trialId"])
    if kind == "ordivon.evaluation-failure":
        return str(document["failureId"])
    for field in ("manifestId", "suiteId", "summaryId", "baselineId", "closeoutId"):
        if field in document:
            return str(document[field])
    return sha256_value(document)


def _record_collection(relative_path: str) -> str:
    if "/dogfood-20260802/" in f"/{relative_path}":
        return "dogfood-20260802"
    if relative_path.endswith("suite-v1.json"):
        return "suite-v1"
    return "p0-20260804"


def _comparison_maps(
    summary: dict[str, Any],
) -> tuple[dict[str, str], dict[tuple[str, int], tuple[bool, list[str]]]]:
    trial_groups: dict[str, str] = {}
    for group in summary["groups"]:
        for trial_id in group["trialIds"]:
            if trial_id in trial_groups:
                raise ValueError(f"trial appears in multiple summary groups: {trial_id}")
            trial_groups[trial_id] = group["groupId"]
    task_eligibility: dict[tuple[str, int], tuple[bool, list[str]]] = {}
    for candidate in summary["comparisonCandidates"]:
        task_ref = candidate["taskRef"]
        key = (task_ref["taskId"], task_ref["taskVersion"])
        task_eligibility[key] = (bool(candidate["eligible"]), list(candidate["blockers"]))
    return trial_groups, task_eligibility


def build_rows(source_root: Path) -> tuple[dict[str, list[tuple[Any, ...]]], list[dict[str, Any]]]:
    dogfood_paths = _dogfood_paths(source_root)
    documents = {path: _load(path) for path in dogfood_paths}
    tasks = {
        document["taskId"]: (path, document)
        for path, document in documents.items()
        if document["kind"] == "ordivon.evaluation-task"
    }
    trials = {
        document["trialId"]: (path, document)
        for path, document in documents.items()
        if document["kind"] == "ordivon.evaluation-trial"
    }
    results = {
        document["trialId"]: (path, document)
        for path, document in documents.items()
        if document["kind"] == "ordivon.evaluation-result"
    }
    failures: dict[str, list[tuple[Path, dict[str, Any]]]] = {}
    for path, document in documents.items():
        if document["kind"] == "ordivon.evaluation-failure":
            failures.setdefault(document["trialId"], []).append((path, document))

    if set(trials) != set(results):
        raise ValueError("dogfood Trial and Result identities differ")

    summary_path = source_root / BASELINE_RELATIVE / "dogfood-summary.json"
    summary = _load(summary_path)
    trial_groups, task_eligibility = _comparison_maps(summary)
    suite_path = source_root / SUITE_RELATIVE
    suite = _load(suite_path)
    manifest_path = source_root / BASELINE_RELATIVE / "system-manifest.json"
    system_manifest = _load(manifest_path)

    rows: dict[str, list[tuple[Any, ...]]] = {name: [] for name in TABLE_SPECS}

    for task_id, (path, document) in sorted(tasks.items()):
        contract = document["acceptanceContract"]
        rows["tasks"].append(
            (
                task_id,
                document["taskVersion"],
                document["family"],
                document["objective"],
                contract["verifierId"],
                contract["verifierRevision"],
                _relative(path, source_root),
                document["integrity"]["payloadDigest"],
                _json(document),
            )
        )

    for trial_id, (path, document) in sorted(trials.items()):
        result = results[trial_id][1]
        verifier = result["acceptance"]["verifier"]
        task_ref = document["taskRef"]
        eligible, blockers = task_eligibility[task_ref["taskId"], task_ref["taskVersion"]]
        rows["trials"].append(
            (
                trial_id,
                task_ref["taskId"],
                task_ref["taskVersion"],
                document["executionPath"],
                document["startedAtMs"],
                document["completedAtMs"],
                document["model"]["providerId"],
                document["model"]["modelId"],
                document["model"]["modelRevision"],
                document["model"]["adapterRevision"],
                document["harness"]["harnessId"],
                document["harness"]["harnessRevision"],
                document["harness"]["manifestDigest"],
                document["bindings"].get("systemManifestRef"),
                document["bindings"].get("systemSnapshotRef"),
                document["bindings"]["sourceRevision"],
                document["bindings"]["toolCatalogDigest"],
                verifier["verifierId"],
                verifier["verifierRevision"],
                trial_groups[trial_id],
                eligible,
                _json(blockers),
                _relative(path, source_root),
                document["integrity"]["payloadDigest"],
                _json(document),
            )
        )
        for ordinal, evidence in enumerate(document["sourceEvidenceRefs"]):
            rows["trial_source_evidence"].append(
                (
                    trial_id,
                    ordinal,
                    evidence["repositoryId"],
                    evidence["path"],
                    evidence["digest"],
                )
            )

    for trial_id, (path, document) in sorted(results.items()):
        acceptance = document["acceptance"]
        verifier = acceptance["verifier"]
        trace = document["trace"]
        task_ref = document["taskRef"]
        rows["results"].append(
            (
                trial_id,
                task_ref["taskId"],
                task_ref["taskVersion"],
                acceptance["status"],
                acceptance["falseCompletion"],
                verifier["status"],
                verifier["verifierId"],
                verifier["verifierRevision"],
                document["stopCode"],
                trace["ref"] if trace is not None else None,
                trace["digest"] if trace is not None else None,
                trace["eventCount"] if trace is not None else None,
                _relative(path, source_root),
                document["integrity"]["payloadDigest"],
                _json(document),
            )
        )
        for metric_name, metric_value in sorted(document["metrics"].items()):
            rows["result_metrics"].append(
                (
                    trial_id,
                    metric_name,
                    None if metric_value is None else float(metric_value),
                    metric_value is None,
                )
            )
        for ordinal, artifact in enumerate(document["artifacts"]):
            rows["result_artifacts"].append(
                (
                    trial_id,
                    ordinal,
                    artifact["ref"],
                    artifact["kind"],
                    artifact["digest"],
                    artifact["valid"],
                )
            )
        for ordinal, assertion in enumerate(verifier["assertions"]):
            rows["verifier_assertions"].append(
                (
                    trial_id,
                    ordinal,
                    assertion["assertionId"],
                    assertion["status"],
                    _json(assertion["evidenceRefs"]),
                )
            )

    for trial_id in sorted(failures):
        for path, document in sorted(failures[trial_id], key=lambda item: item[1]["failureId"]):
            rows["failures"].append(
                (
                    document["failureId"],
                    trial_id,
                    document["failureClass"],
                    document["failureCode"],
                    document["responsibleBoundary"],
                    document["recoverable"],
                    document["recovered"],
                    document["duplicateEffect"],
                    document["humanIntervention"],
                    document["description"],
                    document["minimalCorrection"],
                    document["correctionCost"],
                    _relative(path, source_root),
                    document["integrity"]["payloadDigest"],
                    _json(document),
                )
            )

    provider = system_manifest["configuration"]["provider"]
    privacy = system_manifest["privacy"]
    rows["system_manifests"].append(
        (
            system_manifest["manifestId"],
            system_manifest["capturedAt"],
            system_manifest["systemSnapshot"]["path"],
            system_manifest["systemSnapshot"]["digest"],
            provider["providerId"],
            provider["modelId"],
            provider["modelRevision"],
            provider["adapterRevision"],
            privacy["secretsIncluded"],
            privacy["rawReasoningRequired"],
            _relative(manifest_path, source_root),
            system_manifest["integrity"]["payloadDigest"],
            _json(system_manifest),
        )
    )

    for family in suite["workloadFamilies"]:
        for task_ref in family["taskRefs"]:
            rows["suite_tasks"].append(
                (
                    suite["suiteId"],
                    suite["suiteVersion"],
                    family["familyId"],
                    family["status"],
                    family["priority"],
                    task_ref["taskId"],
                    task_ref["taskVersion"],
                    task_ref["repositoryId"],
                    task_ref["path"],
                    task_ref["digest"],
                )
            )

    source_records: list[dict[str, Any]] = []
    for path in [*dogfood_paths, *_control_paths(source_root)]:
        document = _load(path)
        relative_path = _relative(path, source_root)
        payload_digest = document.get("integrity", {}).get("payloadDigest")
        record = {
            "recordKind": document.get("kind", "unknown"),
            "recordId": _record_id(document),
            "collection": _record_collection(relative_path),
            "sourcePath": relative_path,
            "fileDigest": file_digest(path),
            "payloadDigest": payload_digest,
        }
        source_records.append(record)
        rows["projection_records"].append(
            (
                record["recordKind"],
                record["recordId"],
                record["collection"],
                record["sourcePath"],
                record["fileDigest"],
                record["payloadDigest"],
            )
        )

    for table_name, spec in TABLE_SPECS.items():
        indexes = [spec.columns.index(column) for column in spec.order_columns]
        rows[table_name].sort(key=lambda row: tuple(row[index] for index in indexes))
    source_records.sort(key=lambda record: record["sourcePath"])
    return rows, source_records


def _table_logical_digest(spec: TableSpec, rows: Iterable[tuple[Any, ...]]) -> str:
    values = [dict(zip(spec.columns, row, strict=True)) for row in rows]
    return sha256_value(values)


def _sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


def _write_generation(
    generation_root: Path,
    rows: dict[str, list[tuple[Any, ...]]],
    source_records: list[dict[str, Any]],
    source_revision: str,
) -> dict[str, Any]:
    parquet_root = generation_root / "parquet"
    parquet_root.mkdir(parents=True)
    database_path = generation_root / "evaluation.duckdb"
    connection = duckdb.connect(str(database_path))
    table_manifest: dict[str, dict[str, Any]] = {}
    try:
        for table_name, spec in TABLE_SPECS.items():
            connection.execute(spec.create_sql)
            values = rows[table_name]
            if values:
                placeholders = ", ".join("?" for _ in spec.columns)
                connection.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})",
                    values,
                )
            parquet_path = parquet_root / f"{table_name}.parquet"
            connection.execute(
                f"COPY {table_name} TO '{_sql_path(parquet_path)}' "
                "(FORMAT PARQUET, COMPRESSION ZSTD)"
            )
            table_manifest[table_name] = {
                "path": parquet_path.relative_to(generation_root).as_posix(),
                "rowCount": len(values),
                "logicalDigest": _table_logical_digest(spec, values),
                "fileDigest": file_digest(parquet_path),
            }
        connection.execute("CHECKPOINT")
    finally:
        connection.close()

    source_record_set_digest = sha256_value(source_records)
    identity = {
        "projectionSchemaVersion": 1,
        "projectorVersion": __version__,
        "sourceRevision": source_revision,
        "sourceRecordSetDigest": source_record_set_digest,
        "tableLogicalDigests": {
            name: value["logicalDigest"] for name, value in sorted(table_manifest.items())
        },
    }
    generation_id = sha256_value(identity)
    manifest = with_integrity(
        {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-data-projection",
            "generationId": generation_id,
            "projector": {
                "name": "ordivon-eval-data",
                "version": __version__,
            },
            "source": {
                "repositoryId": "ordivon-computing",
                "revision": source_revision,
                "recordSetDigest": source_record_set_digest,
                "records": source_records,
            },
            "inventory": {
                "tasks": len(rows["tasks"]),
                "trials": len(rows["trials"]),
                "results": len(rows["results"]),
                "failures": len(rows["failures"]),
            },
            "database": {
                "path": database_path.relative_to(generation_root).as_posix(),
                "engine": "duckdb",
            },
            "tables": table_manifest,
        }
    )
    write_json(generation_root / "projection-manifest.json", manifest)
    return manifest


def _current_generation(output_root: Path) -> Path:
    current = output_root / "current"
    if not current.exists():
        raise ValueError(f"projection current generation is missing: {current}")
    resolved = current.resolve(strict=True)
    generations = (output_root / "generations").resolve(strict=True)
    try:
        resolved.relative_to(generations)
    except ValueError as error:
        raise ValueError("projection current link escapes the generations directory") from error
    return resolved


def validate_projection(output_root: Path) -> dict[str, Any]:
    generation_root = _current_generation(output_root)
    manifest_path = generation_root / "projection-manifest.json"
    manifest = _load(manifest_path)
    validate_integrity(manifest)
    if manifest.get("kind") != "ordivon.evaluation-data-projection":
        raise ValueError("unsupported projection manifest kind")
    database_path = generation_root / manifest["database"]["path"]
    if not database_path.is_file():
        raise ValueError("projection DuckDB database is missing")
    for table_name, table in manifest["tables"].items():
        if table_name not in TABLE_SPECS:
            raise ValueError(f"unexpected projected table: {table_name}")
        parquet_path = generation_root / table["path"]
        if file_digest(parquet_path) != table["fileDigest"]:
            raise ValueError(f"Parquet digest differs: {table_name}")

    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        for table_name, table in manifest["tables"].items():
            count = connection.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
            if count != table["rowCount"]:
                raise ValueError(
                    f"DuckDB row count differs for {table_name}; "
                    f"expected={table['rowCount']}, observed={count}"
                )
        checks = {
            "trial_task_refs": """
                SELECT count(*) FROM trials t
                LEFT JOIN tasks k ON (t.task_id, t.task_version) = (k.task_id, k.task_version)
                WHERE k.task_id IS NULL
            """,
            "result_trial_refs": """
                SELECT count(*) FROM results r
                LEFT JOIN trials t USING (trial_id)
                WHERE t.trial_id IS NULL
            """,
            "failure_trial_refs": """
                SELECT count(*) FROM failures f
                LEFT JOIN trials t USING (trial_id)
                WHERE t.trial_id IS NULL
            """,
            "metric_result_refs": """
                SELECT count(*) FROM result_metrics m
                LEFT JOIN results r USING (trial_id)
                WHERE r.trial_id IS NULL
            """,
            "artifact_result_refs": """
                SELECT count(*) FROM result_artifacts a
                LEFT JOIN results r USING (trial_id)
                WHERE r.trial_id IS NULL
            """,
            "assertion_result_refs": """
                SELECT count(*) FROM verifier_assertions a
                LEFT JOIN results r USING (trial_id)
                WHERE r.trial_id IS NULL
            """,
        }
        for label, query in checks.items():
            missing = connection.execute(query).fetchone()[0]
            if missing != 0:
                raise ValueError(f"projection relational check failed: {label}={missing}")
        inventory = manifest["inventory"]
        expected_inventory = {"tasks": 7, "trials": 10, "results": 10, "failures": 6}
        if inventory != expected_inventory:
            raise ValueError(
                "projection dogfood inventory differs; "
                f"expected={expected_inventory}, observed={inventory}"
            )
    finally:
        connection.close()
    return manifest


def project(source_root: Path, output_root: Path) -> dict[str, Any]:
    source_root = source_root.resolve(strict=True)
    output_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(output_root, 0o700)
    generations = output_root / "generations"
    generations.mkdir(mode=0o700, exist_ok=True)

    validate_source(source_root)
    rows, source_records = build_rows(source_root)
    source_revision = _source_revision(source_root)
    temporary = generations / f".tmp-{uuid.uuid4().hex}"
    temporary.mkdir(mode=0o700)
    try:
        manifest = _write_generation(temporary, rows, source_records, source_revision)
        generation_name = manifest["generationId"].removeprefix("sha256:")
        target = generations / generation_name
        if target.exists():
            existing_manifest = _load(target / "projection-manifest.json")
            if existing_manifest != manifest:
                raise ValueError(f"existing projection generation conflicts: {target}")
            shutil.rmtree(temporary)
        else:
            temporary.rename(target)
        current_new = output_root / f".current-{uuid.uuid4().hex}"
        current_new.symlink_to(Path("generations") / generation_name)
        os.replace(current_new, output_root / "current")
        validated = validate_projection(output_root)
        if validated != manifest:
            raise ValueError("projection manifest changed after publication")
        return manifest
    except Exception:
        if temporary.exists():
            shutil.rmtree(temporary)
        raise
