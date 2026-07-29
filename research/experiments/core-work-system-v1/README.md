# Core Work System v1

This is the executable Round 1 comparison for Ordivon's core work-system claims.
It deliberately gives LangGraph and Temporal the same application state that the
Ordivon variant receives. The experiment asks whether separate Host semantics add
measurable value, not whether mature workflow systems can be made to look weak.

```text
one frozen maintenance world
+ one authoritative grader
+ isolated E1/E7, E3, E2, and E5 work packages
+ one combined gauntlet after isolated faults pass
```

## Work packages

- `continuity`: transcript/summary, LangGraph SQLite checkpoints, Temporal Workflow state, and Ordivon-style typed work state;
- `context`: full transcript, rolling summary, revision-filtered retrieval, and source-bound invalidation;
- `effect`: plain call, idempotency/audit, durable Activity, and Effect/Binding/Dispatch/UNKNOWN;
- `attention`: approval-everywhere, static risk policy, model-selected interruption, and evidence-rich DecisionRequest.

## Deterministic gate

```bash
uv sync
uv run python -m unittest discover -s tests
uv run anc-core-work-system freeze --output fixtures/contract-rebind-maintenance-v1
uv run anc-core-work-system matrix \
  --fixture fixtures/contract-rebind-maintenance-v1 \
  --output evidence/deterministic-matrix.json
```

Live model trials are a later command over the same frozen fixture and do not
change scoring, fault schedules, or hard-failure definitions.

## Closeout

The deterministic and live evidence is summarized in [`RESULTS.md`](RESULTS.md).
Generate the machine-readable closeout after the evidence files exist:

```bash
uv run python scripts/report_closeout.py \
  --matrix evidence/deterministic-matrix.json \
  --live evidence/live-provider-gauntlet.json \
  --host-source-revision 394e205d165c0d891448179fbc0fdc7270a98970 \
  --host-receipt-digest sha256:8eec72773621dacbf3826b467d010bed6717e80642e1d10eb2c3fe66253bf785 \
  --output evidence/round1-closeout.json
```
