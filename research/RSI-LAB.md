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

Later transfer experiments changed the research method without adding commands. When a plan or derivation knows which owner facts make a **new consequence** applicable, record that basis before admission and compare it to current owner truth. P10 adds a phase boundary: once the exact Effect/request identity is durably admitted, recovery should preserve that identity and use owner-native replay/dispatch/reconciliation semantics rather than repeatedly re-applying generic currentness. Exactly-once protection is identity-scoped; creating a new identity is a new consequence.

When an evidence-acquisition Agent exhibits search inertia, a **fresh synthesis context** after decision-relevant dependency coverage remains a supported research operator. P11 narrows the earlier order hypothesis: before blaming Context or evidence order, freeze an unambiguous semantic question and oracle. On the clarified Finance workload, raw order was already 44/48 strict and stable list/map canonicalization did not improve it. Canonical bytes are mechanical convenience, not evidence of better semantic tractability.

Neither policy authorizes an `ApplicabilityService`, `EffectPhaseService`, `CriticService`, `StoppingService`, `EvidenceNormalizer`, `OrderService`, `ContextCompiler`, economic-intent global deduper, automatic rebase rule, materiality classifier, evidence-order authority, or global observation-count threshold.

## Data-plane rule

Prefer mature deterministic equipment—Git, SQLite, DuckDB/Parquet, `jq`, `hyperfine`, system/OTel telemetry, owner-native receipts—over model context for counting, filtering, storage, diffing, replay bookkeeping, and aggregation. Add a new Ordivon mechanism only when repeated current consumers prove that classical composition cannot preserve the needed semantics.

## Evidence

P0–P3 instrument promotion is recorded in [`experiments/rsi-lab-p0-p3-v0/`](experiments/rsi-lab-p0-p3-v0/). The strict P4–P9 existence tests are recorded in [`experiments/rsi-lab-p4-p9-v0/`](experiments/rsi-lab-p4-p9-v0/), their Security/Finance cross-domain transfer in [`experiments/p8-p9-cross-domain-transfer-v0/`](experiments/p8-p9-cross-domain-transfer-v0/), and the Effect-phase/order falsification in [`experiments/p10-p11-effect-phase-order-v0/`](experiments/p10-p11-effect-phase-order-v0/).
