#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve()
EXPERIMENT = SCRIPT.parents[1]
EXPERIMENTS = EXPERIMENT.parent
for path in (
    EXPERIMENT / "src",
    EXPERIMENTS / "external-semantic-contract-v0" / "src",
    EXPERIMENTS / "external-semantic-contract-v0",
    EXPERIMENTS / "semantic-core-v0" / "src",
):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anc_continuation.evaluation import continuation_evaluation_report  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a semantic continuation evaluation report from one evidence receipt"
    )
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text())
    if not isinstance(evidence, dict):
        raise SystemExit("continuation evidence must be a JSON object")
    report = continuation_evaluation_report(evidence)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
