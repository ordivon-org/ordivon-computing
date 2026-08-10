"""CLI for Ordivon's narrow managed-document metadata validator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .check import check_repository, load_project_manifest


def _write_json(path: Path, document: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def command_check(args: argparse.Namespace) -> int:
    receipt = check_repository(args.root, mode=args.mode)
    if args.receipt:
        _write_json(args.receipt, receipt)
    keys = (
        "projectId",
        "mode",
        "contentState",
        "checkedDocuments",
        "managedDocuments",
        "metadataDocuments",
        "blockingFailures",
        "warnings",
        "receiptDigest",
    )
    print(json.dumps({key: receipt[key] for key in keys}, indent=2, ensure_ascii=False))
    return 1 if receipt["contentState"] == "BLOCKED" else 0


def command_project(args: argparse.Namespace) -> int:
    document = load_project_manifest(args.root.expanduser().resolve())
    print(json.dumps(document, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ordivon managed-document metadata validation")
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="validate managed document metadata")
    check.add_argument("--root", type=Path, default=Path.cwd())
    check.add_argument("--mode", choices=("advisory", "strict"))
    check.add_argument("--receipt", type=Path)
    check.set_defaults(handler=command_check)
    project = subparsers.add_parser("project", help="validate and print one project manifest")
    project.add_argument("--root", type=Path, default=Path.cwd())
    project.set_defaults(handler=command_project)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
