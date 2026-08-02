"""Command-line interface for Ordivon content engineering."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .baseline import build_baseline, render_markdown, write_json
from .check import check_repository, load_project_manifest


def command_check(args: argparse.Namespace) -> int:
    receipt = check_repository(args.root, mode=args.mode)
    if args.receipt:
        write_json(args.receipt, receipt)
    summary = {key: receipt[key] for key in ("projectId", "mode", "contentState", "checkedDocuments", "managedDocuments", "metadataDocuments", "blockingFailures", "warnings", "receiptDigest")}
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 1 if receipt["contentState"] == "BLOCKED" else 0


def command_project(args: argparse.Namespace) -> int:
    document = load_project_manifest(args.root.expanduser().resolve())
    print(json.dumps(document, indent=2, ensure_ascii=False))
    return 0


def command_baseline(args: argparse.Namespace) -> int:
    document = build_baseline(
        args.repository_parent,
        args.pattern,
        repository_roots=args.repository_root,
    )
    if args.json_output:
        write_json(args.json_output, document)
    markdown = render_markdown(document)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(markdown, encoding="utf-8")
    if not args.json_output and not args.markdown_output:
        print(markdown)
    else:
        print(json.dumps(document["totals"], indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ordivon content contracts, checks, and baselines")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="check one repository")
    check.add_argument("--root", type=Path, default=Path.cwd())
    check.add_argument("--mode", choices=("advisory", "strict"))
    check.add_argument("--receipt", type=Path)
    check.set_defaults(handler=command_check)

    project = subparsers.add_parser("project", help="validate and print one project manifest")
    project.add_argument("--root", type=Path, default=Path.cwd())
    project.set_defaults(handler=command_project)

    baseline = subparsers.add_parser("baseline", help="generate a cross-repository advisory baseline")
    baseline.add_argument("--repository-parent", type=Path)
    baseline.add_argument("--repository-root", type=Path, action="append", default=[])
    baseline.add_argument("--pattern", default="ordivon-*")
    baseline.add_argument("--json-output", type=Path)
    baseline.add_argument("--markdown-output", type=Path)
    baseline.set_defaults(handler=command_baseline)
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
