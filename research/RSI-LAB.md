---
title: RSI Laboratory Instruments
type: guide
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - agent
  - researcher
  - builder
summary: Thin non-authoritative scientific instruments for cross-owner evidence packing, experiment matrices, DuckDB analysis, and revision pressure.
evidence_status: verified
readiness: READY
applies_to:
  - ordivon-computing
---
# RSI Laboratory Instruments

`python scripts/ordivon_lab.py` is a deterministic scientific-instrument surface, not an RSI controller. It reduces mechanical evidence plumbing while leaving research judgment and product authority with the Agent and fact owners.

## Boundary

```text
owner-native truth
  → owner exporter / exact receipts
  → EvidencePack or Matrix records
  → JSONL / Parquet / DuckDB query
  → Agent interpretation
  → owner/domain verification and consequence
```

The lab never decides research priority, topology, tractability, semantic completion, or scientific success. It does not own external-effect reconciliation. Analytical files are rebuildable projections.

## P0 — freeze owner evidence

Owner exporters remain beside Host, Harness, Runtime, World, or another fact owner. The shared Observation contract lives in `packages/ordivon-observation-core`. After producing bounded export bundles:

```bash
python scripts/ordivon_lab.py evidence-pack \
  --pack-id evidence-pack:example \
  --bundle /path/host-bundle.json \
  --bundle /path/harness-bundle.json \
  --bundle /path/runtime-bundle.json \
  --output /tmp/evidence-pack.json
```

`--max-events` is an explicit ceiling. The command fails instead of silently truncating. `completeForSuppliedBundles=true` means only that every event in the supplied bundles was preserved; it does not mean the owners exported their whole history or that a Trial is valid.

## P1 — mechanical experiment matrix

A matrix spec freezes factors, replicate count, executable, arguments, cwd, timeout, output retention, and concurrency. The runner expands cells and records each terminal mechanical result independently:

```bash
python scripts/ordivon_lab.py matrix \
  --spec /path/matrix.json \
  --output-dir /tmp/matrix-run
```

An exact rerun skips terminal trial records that bind the same spec/trial identity. This is **not** general Effect replay. If a command can change external reality, that command must itself use an owner-native durable Effect/request identity and reconciliation path. Matrix exposes `effectRecoveryOwnedByMatrix=false` because a crash can occur after an external effect but before the local terminal record is written.

Mechanical success (`exitCode == 0`) is not scientific success. Timeout and nonzero exit are data, not automatic experiment invalidity.

## P2 — classical analytical projection

Use DuckDB and Parquet to keep bulk deterministic analysis outside model context:

```bash
python scripts/ordivon_lab.py analyze-evidence \
  --pack /tmp/evidence-pack.json \
  --output-dir /tmp/evidence-analysis

python scripts/ordivon_lab.py analyze-matrix \
  --run-dir /tmp/matrix-run \
  --output-dir /tmp/matrix-analysis

python scripts/ordivon_lab.py query \
  --parquet /tmp/matrix-analysis/trials.parquet \
  --json \
  --sql 'SELECT factor_mode, count(*) AS n FROM {table} GROUP BY factor_mode'
```

The `{table}` placeholder is replaced only with the selected Parquet relation. SQL remains Agent-authored. Parquet/JSONL can be deleted and rebuilt from retained evidence.

## P3 — pressure without a problem selector

```bash
python scripts/ordivon_lab.py pressure-pack \
  --output /tmp/pressure-pack.json
```

The default input is `research/world-model-frontier.json`. The pack records exact observed/current Git revisions, relation, bounded changed paths, bounded commit samples, truncation, and UNKNOWN. It deliberately produces no importance score, priority, topology class, tractability score, recommended action, or world-model change.

The Agent decides whether a delta is churn, owner-local debt, a shared-model contradiction, or not worth pursuing.

## P5 — verify an Agent-declared contraction

`contraction-verify` exists because exact Git recoverability, current absence, gate binding, and executable census were repeatedly reimplemented across experiment closeouts. It verifies a scope that the Agent has already chosen; it never chooses or performs deletion.

```bash
python scripts/ordivon_lab.py contraction-verify \
  --repository /root/projects/ordivon-computing \
  --snapshot-revision <full-apparatus-commit> \
  --retired-path research/experiments/<experiment>/apparatus \
  --gate-receipt /tmp/current-conformance.json \
  --executable-root research/experiments \
  --output /tmp/contraction-receipt.json
```

A valid receipt proves only the declared mechanical facts. Semantic retention, deletion scope, mutation, and publication remain outside the command.

## Research policies that are deliberately not Lab services

Two later experiments changed the research method without adding commands. First, when a plan already knows which owner facts make a consequence applicable, record that applicability basis **before** concurrency; after a safe binding conflict, compare only those predeclared facts to current owner evidence and let the Agent/domain decide materiality. Second, when an evidence-acquisition Agent exhibits search inertia on an expensive universe, a **fresh synthesis context** after a bounded high-information batch is a candidate stopping operator. Its cadence is workload/operator-relative: one high-density search can contain dozens of discriminating matches, while additional searches can introduce path-dependent errors.

Neither policy authorizes an `ApplicabilityService`, `CriticService`, automatic rebase rule, materiality classifier, or global observation-count threshold.

## Data-plane rule

Prefer mature deterministic equipment—Git, SQLite, DuckDB/Parquet, `jq`, `hyperfine`, system/OTel telemetry, owner-native receipts—over model context for counting, filtering, storage, diffing, replay bookkeeping, and aggregation. Add a new Ordivon mechanism only when repeated current consumers prove that classical composition cannot preserve the needed semantics.

## Evidence

P0–P3 instrument promotion is recorded in [`experiments/rsi-lab-p0-p3-v0/`](experiments/rsi-lab-p0-p3-v0/). The strict P4–P9 existence tests and later method updates are recorded in [`experiments/rsi-lab-p4-p9-v0/`](experiments/rsi-lab-p4-p9-v0/).
