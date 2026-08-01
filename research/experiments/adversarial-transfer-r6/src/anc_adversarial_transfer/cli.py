from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reporting import render_markdown
from .runner import ATTACKS, MODELS, PROFILES, run_matrix


def _csv(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Ordivon R6 real-model adversarial transfer matrix")
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--host-repo", type=Path, default=Path("/root/projects/ordivon-host"))
    parser.add_argument("--runtime-endpoint", default="http://127.0.0.1:8897/mcp")
    parser.add_argument("--runtime-env", type=Path, default=Path("/etc/ordivon/ordivon-runtime.env"))
    parser.add_argument(
        "--deepseek-secret",
        type=Path,
        default=Path("/root/.config/ordivon/secrets/deepseek.json"),
    )
    parser.add_argument("--attacks", type=_csv, default=tuple(ATTACKS))
    parser.add_argument("--profiles", type=_csv, default=PROFILES)
    parser.add_argument("--models", type=_csv, default=MODELS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--progress", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_matrix(
        source_repo=args.source_repo,
        source_revision=args.source_revision,
        host_repo=args.host_repo,
        runtime_endpoint=args.runtime_endpoint,
        runtime_env=args.runtime_env,
        deepseek_secret=args.deepseek_secret,
        attacks=args.attacks,
        profiles=args.profiles,
        models=args.models,
        progress_path=args.progress,
    )
    payload = result.to_dict()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    args.report.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if payload["summary"]["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
