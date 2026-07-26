# External Semantic Contract evidence

Machine receipts are the source of truth for exact revisions, counts, digests, timings, and live outcomes. README and conformance documents describe stable boundaries only.

## Retained receipts

- [`evidence/external-contract-2f4d7ca.json`](evidence/external-contract-2f4d7ca.json) — initial Effect IR, ToolContract, Binding and drift report;
- [`evidence/live-ordivon-2f4d7ca.json`](evidence/live-ordivon-2f4d7ca.json) — compatibility-era unbound Ordivon live paths;
- [`../semantic-core-v0/benchmark-results/binding-edge-2f4d7ca.json`](../semantic-core-v0/benchmark-results/binding-edge-2f4d7ca.json) — Kernel Binding-edge performance receipt;
- [`evidence/external-contract-85ee8d5.json`](evidence/external-contract-85ee8d5.json) — post-surgery deterministic external-contract report;
- [`evidence/bound-ordivon-85ee8d5.json`](evidence/bound-ordivon-85ee8d5.json) — complete signed Binding, exact-request, process-restart and file-to-Fact live evidence;
- [`fixtures/contracts/ordivon-live-catalog.json`](fixtures/contracts/ordivon-live-catalog.json) — normalized live MCP catalog snapshot for read, mutate, exec, observe and Artifact read.

## Manual evidence commands

These are deliberately excluded from ordinary CI:

```bash
set -a
source /etc/ordivon/ordivon-mcp.env
set +a

PYTHONPATH=src:../semantic-core-v0/src:../semantic-core-v0/scripts:. \
  python3.12 scripts/live_bound_ordivon_restart.py \
  --source-revision <exact-commit>

PYTHONPATH=src:../semantic-core-v0/src:../semantic-core-v0/scripts:. \
  python3.12 scripts/live_bound_ordivon_files.py \
  --source-revision <exact-commit>

PYTHONPATH=src:../semantic-core-v0/src:../semantic-core-v0/scripts:. \
  python3.12 scripts/capture_ordivon_contracts.py \
  --output fixtures/contracts/ordivon-live-catalog.json
```

A stage closeout may add a new immutable JSON receipt. It must not overwrite an older exact-revision receipt.
