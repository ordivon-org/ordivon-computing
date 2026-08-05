from __future__ import annotations

import json
import os
import sqlite3
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from mlflow import MlflowClient

from .backup import BACKUP_TAG
from .mlflow_mirror import EXPERIMENT_NAME, check_server_health
from .projection import validate_projection


def _restic_snapshots(
    restic: Path,
    repository: Path,
    password_file: Path,
) -> list[dict[str, Any]]:
    if not repository.exists() or not password_file.is_file():
        return []
    result = subprocess.run(
        [str(restic), "snapshots", "--json", "--tag", BACKUP_TAG],
        env={
            **os.environ,
            "RESTIC_REPOSITORY": str(repository),
            "RESTIC_PASSWORD_FILE": str(password_file),
        },
        check=True,
        capture_output=True,
        text=True,
    )
    value = json.loads(result.stdout)
    if not isinstance(value, list):
        raise ValueError("restic snapshots output must be a list")
    return value


def inspect_status(
    *,
    evaluation_root: Path,
    tracking_uri: str,
    mlflow_database: Path,
    restic_repository: Path | None = None,
    restic_password_file: Path | None = None,
    restic: Path = Path("/usr/bin/restic"),
    experiment_name: str = EXPERIMENT_NAME,
) -> dict[str, Any]:
    projection = validate_projection(evaluation_root)
    if tracking_uri.startswith(("http://", "https://")):
        check_server_health(tracking_uri)

    connection = sqlite3.connect(f"file:{mlflow_database}?mode=ro", uri=True)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()
        if integrity is None or integrity[0] != "ok":
            raise ValueError(f"MLflow SQLite integrity check failed: {integrity}")
    finally:
        connection.close()

    client = MlflowClient(tracking_uri=tracking_uri)
    experiment = client.get_experiment_by_name(experiment_name)
    runs = (
        []
        if experiment is None
        else client.search_runs([experiment.experiment_id], max_results=5000)
    )
    trial_ids = [run.data.tags.get("ordivon.trial_id") for run in runs]
    missing_identity = sum(trial_id is None for trial_id in trial_ids)
    identified = [trial_id for trial_id in trial_ids if trial_id is not None]
    duplicates = sorted(trial_id for trial_id, count in Counter(identified).items() if count > 1)
    if missing_identity or duplicates:
        raise ValueError(
            "MLflow Ordivon Run identity invariant failed; "
            f"missing={missing_identity}, duplicates={duplicates}"
        )

    snapshots: list[dict[str, Any]] = []
    if restic_repository is not None and restic_password_file is not None:
        snapshots = _restic_snapshots(
            restic,
            restic_repository,
            restic_password_file,
        )
        snapshots.sort(key=lambda snapshot: snapshot["time"])

    return {
        "status": "healthy",
        "projection": {
            "generationId": projection["generationId"],
            "sourceRevision": projection["source"]["revision"],
            "inventory": projection["inventory"],
            "manifestPayloadDigest": projection["integrity"]["payloadDigest"],
        },
        "mlflow": {
            "trackingUri": tracking_uri,
            "experimentName": experiment_name,
            "experimentId": None if experiment is None else experiment.experiment_id,
            "runCount": len(runs),
            "sqliteIntegrity": "ok",
            "duplicateTrialIds": duplicates,
        },
        "restic": {
            "snapshotCount": len(snapshots),
            "latestSnapshotId": None
            if not snapshots
            else snapshots[-1].get("id", snapshots[-1].get("short_id")),
            "latestSnapshotTime": None if not snapshots else snapshots[-1]["time"],
        },
    }
