from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from anc_semantic_core.backend_conformance import (  # noqa: E402
    run_backend_portability_conformance,
)
from anc_semantic_core.simulator import DeterministicBackendAdapter  # noqa: E402
from tests.test_backend_portability import (  # noqa: E402
    OrdivonPortabilityDriver,
    SimulatorPortabilityDriver,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    ordivon = run_backend_portability_conformance(OrdivonPortabilityDriver())
    simulator = run_backend_portability_conformance(SimulatorPortabilityDriver())
    if ordivon != simulator:
        raise SystemExit("backend semantic reports differ")

    result = {
        "schema_version": 1,
        "source_revision": args.source_revision,
        "reports_equal": True,
        "semantic_report": asdict(ordivon),
        "backend_contracts": {
            "ordivon": {
                "operations": [
                    "workspace.read",
                    "workspace.mutate",
                    "workspace.exec",
                    "task.list",
                    "task.observe",
                    "task.cancel",
                ],
                "status_vocabulary": [
                    "working",
                    "succeeded",
                    "failed",
                    "cancelled",
                    "orphaned",
                ],
            },
            "simulator": {
                "operations": [
                    DeterministicBackendAdapter.READ_OPERATION,
                    DeterministicBackendAdapter.MUTATION_OPERATION,
                    DeterministicBackendAdapter.JOB_OPERATION,
                    "lookup",
                    "inspect",
                    "request_cancel",
                ],
                "status_vocabulary": [
                    "ACTIVE",
                    "COMPLETE",
                    "ERROR",
                    "ABORTED",
                    "INDETERMINATE",
                ],
            },
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
