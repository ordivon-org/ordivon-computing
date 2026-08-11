# P4–P9 — Strict Existence Tests for the RSI Laboratory

## Verdict

This round asked six candidates to justify active existence. Only one new long-lived mechanical command survives (`contraction-verify`), while two research laws survive without becoming services: planning-time applicability bases for concurrent consequence decisions, and fresh synthesis boundaries for stopping expensive search.

| Phase | Verdict | Surviving form |
| --- | --- | --- |
| P4 Fault Injection Kit | Reject | Matrix + OS/tool primitives + owner-local semantic faults |
| P5 Closeout / contraction | Retain narrowly | `contraction-verify` only; verifier never selects/deletes/publishes |
| P6 Continuous telemetry | Reject/defer | systemd/journal/strace/hyperfine + owner receipts; inherit OTel if a real trace workload appears |
| P7 Observation packaging | No new layer | exact Git-pinned isolated research tool environment |
| P8 Semantic applicability | Support/narrow | planning declares applicability basis; tools compare before/after; Agent/domain decides |
| P9 Expensive stopping | Support/narrow | bounded high-information acquisition -> fresh synthesis; no critic service or universal count |

## P4 — shared fault vocabulary does not justify a shared fault system

Current Host/Runtime/Security/World/Game code contains many SIGKILL, delay, response-loss, and phase faults. A 651-byte Matrix spec reproduced none/exit7/SIGKILL/timeout across 12 cells and distinguished signal termination from timeout without a Fault DSL. The semantically interesting faults are already owner-specific: Host response-loss wrappers, Security migration fault points, World transport faults, Game phase faults. Their common denominator is too small to own.

**Delete the crosscut Fault Kit hypothesis.** Host may still consolidate its duplicated live-script setup as an owner-local testing utility.

## P5 — verification repeats; deletion judgment does not

The recurring crosscut burden is mechanical: prove a full apparatus snapshot remains Git-recoverable, prove Agent-declared retired paths are absent now, bind a current conformance receipt, and count current executable experiment source. `contraction-verify` does exactly this and nothing more.

A real HP4 contraction from snapshot `0570a2cf...` to current `090b7cf...` verified three retired apparatus paths, exact Git objects, the exact current gate, and zero executable-like source. The verifier explicitly records that it did not choose scope, delete files, publish, or make semantic retention judgments.

## P6 — continuous telemetry still has no consumer

The current machine already exposes systemd/journal resource summaries and mature process tools; Runtime/Host receipts and Matrix records already capture exact lifecycle/mechanical evidence. No current cross-service trace/latency experiment requires a continuously running collector. Do not build an Ordivon telemetry plane. If that workload appears, mature OpenTelemetry/system tooling is the baseline to inherit before any Ordivon-specific collector or database.

## P7 — package friction is solved by an explicit tool environment

An isolated `uv pip install --target` from the exact Computing Git revision installed `ordivon-observation-core` without sibling-source authority or owner production changes. Runtime 5/5, Host 3/3, Harness 3/3 exporter tests passed. The installed tool target was about 470 KB / 27 files.

No wrapper was added: wrapping one exact `uv` command creates no new semantics. Mandatory production dependencies remain rejected until owner correctness or frequent operations prove they are needed.

## P8 — externalize applicability basis before concurrency

Four fresh owner scenarios were frozen: Runtime identity-only drift, Runtime material input drift, Host evidence-only revision movement, and Host frontier/material movement. In every case the stale consequence binding safely failed `not_committed`.

P8-v1 was invalidated wholesale because its derived packet labeled changes as decision-relevant/material, leaking the intended classification. P8-v2 instead allowed only fields explicitly named by the plan before concurrency and emitted literal before/after/equality. Across 72 trials:

- changed-only: 9/24 accepted, 4 false consequences, 11 unnecessary holds/retries;
- raw current owner evidence: 16/24, 1 false consequence, 7 unnecessary;
- **predeclared binding-field delta: 21/24, 0 false consequences, 3 unnecessary.**

The surviving law is not `field changed -> invalid`. It is:

```text
planning evidence
  -> explicit applicability basis
  -> safe current owner comparison
  -> Agent/domain semantic applicability decision
  -> current consequence binding
```

## P9 — stopping depends on information density and a fresh synthesis boundary

The natural Runtime `hostDependencies` workload spans 21 files and 192 literal matches across request identity, admission, persistence, dispatch, Runner witness, replay, MCP, tests and docs.

The first high-budget campaign falsified self-stopping again: open and critic-at-primary-submit each ran 6 replicates; **all 12 consumed 28/28 observations, Primary produced zero draft attempts, and the critic hook was never reached**, consuming about 6.35M Provider tokens.

A checkpointed fresh synthesis + critic reached 6/6 strict closure after 8 observations, but the critic requested zero extra observations. The critic therefore did not earn existence. A synthesis-only ablation then found:

- 0 observations: 0/6 strict;
- 1 high-density search observation: **6/6 strict**;
- 2 observations: **6/6**;
- 4 observations: **6/6** after replacing one transport-invalid trial that produced no semantic output;
- 8 observations: 5/6; one extra-search path incorrectly claimed replay revalidates current dependency bytes;
- 12 observations: 6/6.

The number `1` is workload-specific: one search observation can contain up to 60 current matches and included high-density tool/source descriptions. The general update is that **more observations are not monotonically better; operator information density and a fresh synthesis boundary matter more than serial marginal-value narration or a universal observation count.**

P9 also caught a Provider-wire failure: DeepSeek frequently emitted JSON Schema booleans as strings. Wire-invalid campaigns were excluded; the accepted v3+ runs use bounded fail-closed schema retry and record every correction.

## Final world-model update

1. Generic mechanical commonality is insufficient reason for a crosscut framework; shared semantics must also be exact.
2. Repeated closeout verification is a legitimate mechanical instrument; deletion judgment is not.
3. Applicability can be partly externalized at planning time, but not inferred post hoc by a global classifier.
4. A search Agent's failure to stop is not fixed by more self-reflection or by a critic that waits for a stop proposal that never arrives.
5. Fresh synthesis contexts can break search inertia; calibrate their cadence against operator information density and false-stop risk.
6. More evidence can worsen the resulting model through path dependence; available budget remains capacity, not evidence obligation.
