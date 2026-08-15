# Core Work System v1

This is the completed historical Round 1 comparison for Ordivon's core work-system claims.
The executable apparatus was intentionally removed from the active tree during the
Computer contraction round; current `main` retains the report and bound evidence only.
The source receipt binds the executable experiment to Computing revision
`0485fcf337ba002aa81a57cb166489f3ddce7709`, which remains recoverable from Git.
It is therefore **not** an executable package on current `main`.

```text
one frozen maintenance world
+ one authoritative grader
+ isolated E1/E7, E3, E2, and E5 work packages
+ one combined gauntlet after isolated faults pass
```

## Documents

- [`REPORT.md`](REPORT.md) — complete experiment report: principles, implementation, comparisons, data, engineering problems, limitations, and architectural consequences;
- [`RESULTS.md`](RESULTS.md) — compact result and disposition summary;
- [`SPEC.md`](SPEC.md) — frozen claim, workload, fairness, and hard-failure contract;
- [`DECISIONS.md`](DECISIONS.md) — retained, shrunk, localized, and deferred decisions;
- [`EVIDENCE.md`](EVIDENCE.md) — evidence and receipt contract.

## Work packages

- `continuity`: transcript/summary, LangGraph SQLite checkpoints, Temporal Workflow state, and Ordivon-style typed work state;
- `context`: full transcript, rolling summary, revision-filtered retrieval, and source-bound invalidation;
- `effect`: plain call, idempotency/audit, durable Activity, and Effect/Binding/Dispatch/UNKNOWN;
- `attention`: approval-everywhere, static risk policy, model-selected interruption, and evidence-rich DecisionRequest.

## Historical executable gate

The original executable gate belongs to the source-bound historical revision, not the
contracted active tree. To reproduce it without reviving retired dependencies on `main`,
materialize revision `0485fcf337ba002aa81a57cb166489f3ddce7709` in a detached Git
worktree and run the gate there:

```bash
git worktree add --detach /tmp/core-work-system-v1 0485fcf337ba002aa81a57cb166489f3ddce7709
cd /tmp/core-work-system-v1/research/experiments/core-work-system-v1
uv sync --frozen
uv run python -m unittest discover -s tests -v
uv run ruff check src tests scripts
uv run anc-core-work-system freeze --output fixtures/contract-rebind-maintenance-v1
uv run anc-core-work-system matrix \
  --fixture fixtures/contract-rebind-maintenance-v1 \
  --output evidence/deterministic-matrix.json
```

The retained `evidence/round1-source-receipt.json` records that this bound source passed
clean-environment recreation, compileall, Ruff, and all nine unit tests at closeout.

## Report statistics

The report's aggregate tables are derived from the bound receipts rather than
maintained manually:

```bash
uv run python scripts/report_statistics.py \
  --matrix evidence/deterministic-matrix.json \
  --live evidence/live-provider-gauntlet.json \
  --output evidence/report-statistics.json
```

## Closeout

Generate the machine-readable architectural closeout after the evidence files
exist:

```bash
uv run python scripts/report_closeout.py \
  --matrix evidence/deterministic-matrix.json \
  --live evidence/live-provider-gauntlet.json \
  --host-source-revision 394e205d165c0d891448179fbc0fdc7270a98970 \
  --host-receipt-digest sha256:8eec72773621dacbf3826b467d010bed6717e80642e1d10eb2c3fe66253bf785 \
  --output evidence/round1-closeout.json
```
