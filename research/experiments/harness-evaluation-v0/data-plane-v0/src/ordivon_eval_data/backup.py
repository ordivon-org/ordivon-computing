from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .canonical import file_digest, sha256_value, with_integrity, write_json
from .projection import _current_generation, validate_projection

BACKUP_TAG = "ordivon-evaluation-data-plane"


def _utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def _files(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): file_digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _copy_tree_stable(source: Path, destination: Path) -> dict[str, str]:
    before = _files(source)
    destination.mkdir(parents=True, exist_ok=True)
    for relative, digest in before.items():
        source_path = source / relative
        destination_path = destination / relative
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)
        if file_digest(destination_path) != digest:
            raise ValueError(f"copied file digest differs: {relative}")
    after = _files(source)
    if before != after:
        raise ValueError("source file set changed during backup capture")
    return before


def _sqlite_backup(source: Path, destination: Path) -> dict[str, Any]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_connection = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
    destination_connection = sqlite3.connect(destination)
    try:
        source_connection.backup(destination_connection)
        result = destination_connection.execute("PRAGMA integrity_check").fetchone()
        if result is None or result[0] != "ok":
            raise ValueError(f"SQLite backup integrity check failed: {result}")
        page_count = destination_connection.execute("PRAGMA page_count").fetchone()[0]
        page_size = destination_connection.execute("PRAGMA page_size").fetchone()[0]
    finally:
        destination_connection.close()
        source_connection.close()
    os.chmod(destination, 0o600)
    return {
        "path": destination.name,
        "digest": file_digest(destination),
        "pageCount": page_count,
        "pageSize": page_size,
    }


def _restic_environment(repository: Path, password_file: Path) -> dict[str, str]:
    if not password_file.is_file():
        raise ValueError(f"restic password file is missing: {password_file}")
    if password_file.stat().st_mode & 0o077:
        raise ValueError("restic password file must not grant group or other permissions")
    return {
        **os.environ,
        "RESTIC_REPOSITORY": str(repository),
        "RESTIC_PASSWORD_FILE": str(password_file),
    }


def _run_restic(
    restic: Path,
    args: list[str],
    *,
    repository: Path,
    password_file: Path,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(restic), *args],
        cwd=cwd,
        env=_restic_environment(repository, password_file),
        check=True,
        capture_output=True,
        text=True,
    )


def _parse_backup_snapshot(output: str) -> str:
    snapshot_id: str | None = None
    for line in output.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and isinstance(value.get("snapshot_id"), str):
            snapshot_id = value["snapshot_id"]
    if snapshot_id is None:
        raise ValueError("restic backup did not return a snapshot identity")
    return snapshot_id


def create_backup(
    *,
    evaluation_root: Path,
    mlflow_database: Path,
    mlflow_artifacts: Path,
    staging_root: Path,
    repository: Path,
    password_file: Path,
    restic: Path = Path("/usr/bin/restic"),
) -> dict[str, Any]:
    projection_manifest = validate_projection(evaluation_root)
    current_generation = _current_generation(evaluation_root)
    staging_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(staging_root, 0o700)
    snapshot_name = f"snapshot-{_utc_stamp()}-{projection_manifest['generationId'][-12:]}"
    snapshot_root = staging_root / snapshot_name
    if snapshot_root.exists():
        raise ValueError(f"backup staging snapshot already exists: {snapshot_root}")
    snapshot_root.mkdir(mode=0o700)
    try:
        generation_name = current_generation.name
        copied_generation = snapshot_root / "evaluation" / "generations" / generation_name
        projection_files = _copy_tree_stable(current_generation, copied_generation)
        (snapshot_root / "evaluation" / "current").symlink_to(Path("generations") / generation_name)
        sqlite_info = _sqlite_backup(
            mlflow_database,
            snapshot_root / "mlflow" / "mlflow.db",
        )
        artifact_files = _copy_tree_stable(
            mlflow_artifacts,
            snapshot_root / "mlflow" / "artifacts",
        )
        backup_manifest = with_integrity(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-data-backup",
                "capturedAt": datetime.now(UTC)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "projection": {
                    "generationId": projection_manifest["generationId"],
                    "manifestPayloadDigest": projection_manifest["integrity"]["payloadDigest"],
                    "fileSetDigest": sha256_value(projection_files),
                    "fileCount": len(projection_files),
                },
                "mlflow": {
                    "database": sqlite_info,
                    "artifactFileSetDigest": sha256_value(artifact_files),
                    "artifactFileCount": len(artifact_files),
                },
            }
        )
        write_json(snapshot_root / "backup-manifest.json", backup_manifest)
        backup_result = _run_restic(
            restic,
            ["backup", "--json", "--tag", BACKUP_TAG, snapshot_name],
            repository=repository,
            password_file=password_file,
            cwd=staging_root,
        )
        snapshot_id = _parse_backup_snapshot(backup_result.stdout)
        _run_restic(
            restic,
            ["check"],
            repository=repository,
            password_file=password_file,
        )
        return {
            "snapshotId": snapshot_id,
            "snapshotName": snapshot_name,
            "projectionGeneration": projection_manifest["generationId"],
            "backupManifestDigest": backup_manifest["integrity"]["payloadDigest"],
        }
    finally:
        if snapshot_root.exists():
            shutil.rmtree(snapshot_root)


def _latest_snapshot_id(
    restic: Path,
    *,
    repository: Path,
    password_file: Path,
) -> str:
    result = _run_restic(
        restic,
        ["snapshots", "--json", "--tag", BACKUP_TAG],
        repository=repository,
        password_file=password_file,
    )
    snapshots = json.loads(result.stdout)
    if not isinstance(snapshots, list) or not snapshots:
        raise ValueError("no evaluation data-plane restic snapshots exist")
    snapshots.sort(key=lambda snapshot: snapshot["time"])
    snapshot_id = snapshots[-1].get("id") or snapshots[-1].get("short_id")
    if not isinstance(snapshot_id, str):
        raise ValueError("latest restic snapshot has no identity")
    return snapshot_id


def restore_check(
    *,
    repository: Path,
    password_file: Path,
    restic: Path = Path("/usr/bin/restic"),
) -> dict[str, Any]:
    snapshot_id = _latest_snapshot_id(
        restic,
        repository=repository,
        password_file=password_file,
    )
    with tempfile.TemporaryDirectory(prefix="ordivon-eval-restore-") as temporary:
        restore_root = Path(temporary)
        _run_restic(
            restic,
            ["restore", snapshot_id, "--target", str(restore_root)],
            repository=repository,
            password_file=password_file,
        )
        snapshot_directories = [path for path in restore_root.iterdir() if path.is_dir()]
        if len(snapshot_directories) != 1:
            raise ValueError(
                "restored snapshot root differs; "
                f"expected one directory, observed={len(snapshot_directories)}"
            )
        snapshot_root = snapshot_directories[0]
        backup_manifest = json.loads(
            (snapshot_root / "backup-manifest.json").read_text(encoding="utf-8")
        )
        from .canonical import validate_integrity

        validate_integrity(backup_manifest)
        projection_manifest = validate_projection(snapshot_root / "evaluation")
        if projection_manifest["generationId"] != backup_manifest["projection"]["generationId"]:
            raise ValueError("restored projection generation differs from backup manifest")
        database = snapshot_root / "mlflow" / "mlflow.db"
        connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
        try:
            result = connection.execute("PRAGMA integrity_check").fetchone()
            if result is None or result[0] != "ok":
                raise ValueError(f"restored MLflow SQLite integrity check failed: {result}")
        finally:
            connection.close()
        if file_digest(database) != backup_manifest["mlflow"]["database"]["digest"]:
            raise ValueError("restored MLflow SQLite digest differs")
        artifact_files = _files(snapshot_root / "mlflow" / "artifacts")
        if sha256_value(artifact_files) != backup_manifest["mlflow"]["artifactFileSetDigest"]:
            raise ValueError("restored MLflow Artifact file-set digest differs")
        return {
            "snapshotId": snapshot_id,
            "snapshotName": snapshot_root.name,
            "projectionGeneration": projection_manifest["generationId"],
            "backupManifestDigest": backup_manifest["integrity"]["payloadDigest"],
            "sqliteIntegrity": "ok",
        }
