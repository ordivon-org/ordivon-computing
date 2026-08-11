# P0–P3 — Agent-first RSI Laboratory Instruments

## Result

P0–P3 is accepted as a **thin scientific-instrument promotion**, not as a new RSI control plane. The work separates long-lived reusable mechanics from disposable experiment apparatus:

```text
owner-native truth
  → bounded export / EvidencePack
  → mechanical Matrix execution
  → rebuildable JSONL/Parquet/DuckDB analysis
  → Agent scientific judgment
  → owner/domain verification and reform
```

The retained rule is: **classical deterministic machinery should compress, execute, count, query, diff, and replay mechanical evidence; the Agent retains question selection, causal interpretation, semantic applicability, world-model revision, and reform proposals.**

## P0 — Observation Core promotion and EvidencePack

Current Runtime, Host, and Harness exporters all import `ordivon_observation_core`. Earlier contraction removed the implementation together with experiment apparatus, leaving current import failure. This was a real deletion falsifier: three materially different owner consumers still require the same contract.

The earned implementation is therefore promoted to `packages/ordivon-observation-core/`. It remains non-authoritative: owners retain state; Gateway state is rebuildable; Selection never infers Trial validity; no daemon or continuous collection policy is introduced. Historical schema builders/copies were initially restored during promotion, then deleted in the contraction audit because no current consumer used them.

Owner regression:

- Runtime exporter: 5/5 tests passed against the promoted core.
- Host exporter: the first current test exposed a real owner-local defect: it hard-coded Journal schema 4 while current Host owns schema 5. Host candidate `0b65927fef0ccfb9b494be6ddc30fb92d3cb34a0` now imports its own `journal._schema.SCHEMA_VERSION`; targeted exporter tests are 3/3.
- Harness exporter: 3/3 tests passed against the promoted core.
- Promoted core active tests: 16/16, including a current Selection regression proving an incomplete selection remains non-authoritative.
- Package distribution smoke: `ordivon-observation-core==0.1.0` built offline and installed into an isolated Python 3.14.6 environment; the wheel digest was `sha256:d48fc0ae2bc7f4b959a6b0954735ad14c72373ff5cc033b909ab0e9be593ca40`. The wheel itself is rebuildable and is not retained as repository evidence.

Three-owner dogfood froze one EvidencePack from:

- live deployed Host owner `6495822162c69179e8ad4f8a0d79cc42902ff599`, 64 events, exported by candidate `0b65927...`;
- current Harness `2083ee8587f44d757ceb3845fc322664aa0cfb53`, a disposable owner-native four-event store because no production `/var/lib/ordivon/harness` store was present;
- current Runtime `e168c496410d8bdfb9d2f1d45e0a9019b637e57a`, one exact Job selected from a Registry containing 41,313 Jobs, producing 8 events.

Combined result: 3 owner projects, 76 events, six measurement values, zero truncation. The Harness terminal event projects model calls, Tool calls, observation bytes, 58 total tokens, wall time, and Tool corrections without copying Provider per-call usage payload.

## P1 — Experiment Matrix Executor

`scripts/ordivon_lab.py matrix` expands frozen factors × replicates, gives each trial a deterministic identity, runs bounded subprocess cells in parallel, writes one terminal record per trial, and resumes already-recorded terminal trials without re-execution. It does **not** decide success in the scientific sense.

Final dogfood: 3 modes (`ok`, `fail`, `timeout`) × 2 batches × 2 replicates = 12 trials. First run executed all 12 and recorded 4 exit-zero, 4 nonzero, 4 timeout outcomes. Exact rerun replayed all 12 terminal identities and executed zero new trials.

A critical negative boundary is machine-visible: `effectRecoveryOwnedByMatrix=false`. A process can produce an external effect and crash before the Matrix terminal record exists. Effectful trial commands therefore need Runtime/domain durable effect identity and reconciliation; Matrix must not become a second Effect kernel.

## P2 — Classical analytical path

`analyze-evidence`, `analyze-matrix`, and `query` use the installed DuckDB CLI to materialize rebuildable JSONL/Parquet projections and query them. Owner/trial JSON remains evidence; Parquet is not authority.

The first real dogfood caught a derived-only bug: the analyzer guessed Privacy field `classification` while the contract uses `class`. The EvidencePack remained valid; the analytical projection was deleted/rebuilt after the fix.

Mechanical context reduction on current dogfood:

| Input / projection | Bytes |
| --- | ---: |
| three-owner EvidencePack JSON | 180,747 |
| three-owner Parquet | 26,271 |
| owner-count SQL result | 134 |
| 12 Matrix trial JSON records combined | 18,199 |
| Matrix Parquet | 5,169 |

These are transport/query mechanics, not research-quality scores. Their value is that the Agent can request a small discriminating table rather than ingesting the entire evidence corpus into model context.

## P3 — PressurePack without a selector

The old C6 owner-pressure selector is not restored. It previously failed to reliably find the frozen shared-method pressure and did not earn autonomous problem selection.

`pressure-pack` instead freezes only mechanical revision pressure: observed revision, current HEAD, Git relation, bounded changed paths, bounded commit sample, truncation, and UNKNOWN. It explicitly emits no importance score, topology, tractability, world-model change, or recommended action.

Current dogfood over the ten-project frontier found one exact owner and nine `owner_advanced` owners. Examples: Runtime +35 commits / 65 changed paths; Harness +58 / 97; Finance +18 / 158. The old freshness assessment is 3,762 bytes and says only one exact / nine advanced; the bounded PressurePack is 50,351 bytes because it carries concrete path/commit evidence. That extra data is justified only as review input; the Agent still chooses what matters.

## Contraction decision

Retain:

- `packages/ordivon-observation-core`: exact shared Observation contract/export/checkpoint/Gateway/Selection mechanics already consumed across owners;
- `scripts/ordivon_lab.py`: thin CLI for EvidencePack, Matrix, analysis/query, PressurePack;
- owner-local exporters beside their truth owners;
- DuckDB/Parquet as classical derived analysis;
- explicit limits, truncation, UNKNOWN, and no-inference boundaries.

Reject / defer:

- Observation daemon/repository/database;
- continuous collection by default;
- universal System/Usage database;
- Experiment scheduler/scorer;
- Matrix effect authority;
- pressure ranking, topology or tractability classifier;
- generic Fault Injection framework;
- closeout/cleanup service;
- schema surface with no current consumer.

Future continuous telemetry should first inherit OpenTelemetry/system tooling when a real workload proves decision value. Fault injection and closeout helpers remain future candidates only after repeated cross-project mechanical burden.
