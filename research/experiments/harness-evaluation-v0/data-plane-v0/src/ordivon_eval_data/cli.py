from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .backup import create_backup, restore_check
from .mlflow_mirror import EXPERIMENT_NAME, check_server_health, mirror
from .projection import project, validate_projection
from .status import inspect_status


def _path(value: str) -> Path:
    return Path(value).expanduser()


def _emit(value: dict[str, Any]) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ordivon-eval-data",
        description="Build and operate the rebuildable Ordivon local evaluation data plane.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    project_parser = subparsers.add_parser(
        "project", help="Build an atomic Parquet and DuckDB projection."
    )
    project_parser.add_argument("--source-root", type=_path, required=True)
    project_parser.add_argument("--output-root", type=_path, required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="Validate the current analytical projection."
    )
    validate_parser.add_argument("--output-root", type=_path, required=True)

    health_parser = subparsers.add_parser(
        "mlflow-health", help="Check the loopback MLflow health endpoint."
    )
    health_parser.add_argument("--tracking-uri", required=True)

    mirror_parser = subparsers.add_parser(
        "mirror", help="Mirror projected Trials into MLflow idempotently."
    )
    mirror_parser.add_argument("--output-root", type=_path, required=True)
    mirror_parser.add_argument("--tracking-uri", required=True)
    mirror_parser.add_argument("--experiment-name", default=EXPERIMENT_NAME)
    mirror_parser.add_argument("--artifact-location")
    mirror_parser.add_argument("--check-health", action="store_true")

    backup_parser = subparsers.add_parser("backup", help="Create and verify one restic snapshot.")
    backup_parser.add_argument("--evaluation-root", type=_path, required=True)
    backup_parser.add_argument("--mlflow-database", type=_path, required=True)
    backup_parser.add_argument("--mlflow-artifacts", type=_path, required=True)
    backup_parser.add_argument("--staging-root", type=_path, required=True)
    backup_parser.add_argument("--repository", type=_path, required=True)
    backup_parser.add_argument("--password-file", type=_path, required=True)
    backup_parser.add_argument("--restic", type=_path, default=Path("/usr/bin/restic"))

    restore_parser = subparsers.add_parser(
        "restore-check",
        help="Restore the latest data-plane snapshot into a temporary directory and validate it.",
    )
    restore_parser.add_argument("--repository", type=_path, required=True)
    restore_parser.add_argument("--password-file", type=_path, required=True)
    restore_parser.add_argument("--restic", type=_path, default=Path("/usr/bin/restic"))

    status_parser = subparsers.add_parser(
        "status",
        help="Validate the installed projection, MLflow mirror, and backup inventory.",
    )
    status_parser.add_argument("--evaluation-root", type=_path, required=True)
    status_parser.add_argument("--tracking-uri", required=True)
    status_parser.add_argument("--mlflow-database", type=_path, required=True)
    status_parser.add_argument("--experiment-name", default=EXPERIMENT_NAME)
    status_parser.add_argument("--repository", type=_path)
    status_parser.add_argument("--password-file", type=_path)
    status_parser.add_argument("--restic", type=_path, default=Path("/usr/bin/restic"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "project":
        _emit(project(args.source_root, args.output_root))
    elif args.command == "validate":
        _emit(validate_projection(args.output_root))
    elif args.command == "mlflow-health":
        check_server_health(args.tracking_uri)
        _emit({"status": "healthy", "trackingUri": args.tracking_uri})
    elif args.command == "mirror":
        if args.check_health:
            check_server_health(args.tracking_uri)
        _emit(
            mirror(
                args.output_root,
                args.tracking_uri,
                experiment_name=args.experiment_name,
                artifact_location=args.artifact_location,
            )
        )
    elif args.command == "backup":
        _emit(
            create_backup(
                evaluation_root=args.evaluation_root,
                mlflow_database=args.mlflow_database,
                mlflow_artifacts=args.mlflow_artifacts,
                staging_root=args.staging_root,
                repository=args.repository,
                password_file=args.password_file,
                restic=args.restic,
            )
        )
    elif args.command == "restore-check":
        _emit(
            restore_check(
                repository=args.repository,
                password_file=args.password_file,
                restic=args.restic,
            )
        )
    elif args.command == "status":
        if (args.repository is None) != (args.password_file is None):
            raise ValueError("--repository and --password-file must be supplied together")
        _emit(
            inspect_status(
                evaluation_root=args.evaluation_root,
                tracking_uri=args.tracking_uri,
                mlflow_database=args.mlflow_database,
                restic_repository=args.repository,
                restic_password_file=args.password_file,
                restic=args.restic,
                experiment_name=args.experiment_name,
            )
        )
    else:
        raise AssertionError(f"unsupported command: {args.command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
