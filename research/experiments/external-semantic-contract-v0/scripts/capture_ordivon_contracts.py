#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_ROOT = ROOT.parent / "semantic-core-v0"
for path in (ROOT, ROOT / "src", CORE_ROOT / "src", CORE_ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from integration import contract_snapshot, discover_ordivon_contracts  # noqa: E402
from live_support import LocalMcpToolCaller  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Capture normalized execution-relevant Ordivon Tool contracts"
    )
    parser.add_argument(
        "--endpoint",
        default=os.environ.get("ORDIVON_MCP_ENDPOINT", "http://127.0.0.1:8897/mcp"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    token = os.environ.get("ORDIVON_BEARER_TOKEN")
    if not token:
        raise SystemExit("ORDIVON_BEARER_TOKEN is required")
    client = LocalMcpToolCaller(args.endpoint, token)
    initialized = client.initialize()
    snapshot = contract_snapshot(discover_ordivon_contracts(client))
    snapshot["mcpProtocolVersion"] = initialized.get("protocolVersion")
    rendered = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
