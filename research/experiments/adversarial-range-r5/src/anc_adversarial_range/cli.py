from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reporting import render_markdown
from .runner import run_range


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Ordivon R5 minimal adversarial range")
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run_range(args.source_revision).to_dict()
    encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_markdown(payload), encoding="utf-8")
    if args.output is None:
        print(encoded, end="")


if __name__ == "__main__":
    main()
