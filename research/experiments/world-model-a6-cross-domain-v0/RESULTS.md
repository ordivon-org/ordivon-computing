---
schema_version: 1
id: computing.research.world-model-a6-cross-domain-results
title: World Model A6 Cross-Domain Results
type: reference
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-09
summary: Finance cross-domain re-test of Agent-owned model-visible source selection, including calibration, scaling, and campaign recovery evidence.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-finance
  - ordivon-harness
related:
  - computing.research.world-model-loop
  - computing.foundations
---
# World Model A6 Cross-Domain Results

Machine acceptance: [`../../evidence/wml-a6-finance-cross-domain-acceptance-e74ef72fb5a8.json`](../../evidence/wml-a6-finance-cross-domain-acceptance-e74ef72fb5a8.json). Raw receipts: [`../../evidence/wml-a6-finance-selection-r0-44a2c762c8b4.json`](../../evidence/wml-a6-finance-selection-r0-44a2c762c8b4.json) and [`../../evidence/wml-a6-finance-scale-r1-a6f3c3f1ec63.json`](../../evidence/wml-a6-finance-scale-r1-a6f3c3f1ec63.json).

## Result

The experiment supports the cross-domain part of Core A6:

```text
owner-native source state
!=
model-visible selected view
!=
authority to choose that view
```

It does **not** promote the experiment's two-stage `select -> answer` Model-call pattern into architecture. Selection authority is the durable distinction; the selection mechanism remains an optimization and cognition-design question.

## R0 — task relevance defeats one static caller rule

The fixed Finance source pool contained six exact owner-native units. FULL exposed all six, LATEST exposed only the most recent Q2 source, and AGENT first saw a value-free catalog then selected at most two exact sources.

- FULL: 6/6 correct.
- LATEST: 3/6 correct.
- AGENT: 6/6 correct and 6/6 predeclared required sources selected.
- AGENT read 7,657 bytes of Finance source content versus FULL's 33,288 bytes, but used 20,428 total Provider tokens versus FULL's 17,025 because selection required another Model Call.

The LATEST failures were not random numerical errors. The static recency rule could not answer an older holdings-concentration fact, a July-24 ex-Alphabet figure, or the semantics of the 18.44% three-to-five-year EPS estimate. `latest` and `relevant` are different relations.

## R1 — fixed selection cost versus growing context cost

R1 kept three tasks and added the largest exact Git-bound Finance schema files as unrelated but real domain sources. This tests scaling without exposing private portfolio/account state.

| Distractors | Sources | FULL accuracy | AGENT accuracy | FULL total tokens | AGENT total tokens | AGENT token delta | Domain-source bytes saved | FULL calls | AGENT calls |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 6 | 100% | 100% | 8,539 | 10,055 | +17.75% | 77.20% | 3 | 6 |
| 2 | 8 | 100% | 100% | 21,591 | 10,608 | -50.87% | 94.06% | 3 | 6 |
| 4 | 10 | 100% | 100% | 29,392 | 11,200 | -61.89% | 95.97% | 3 | 6 |
| 8 | 14 | 100% | 100% | 43,197 | 12,523 | -71.01% | 97.41% | 3 | 6 |

At the base tier, Agent selection remained more expensive in tokens. With two large Finance schema distractors, the relation reversed: AGENT used 10,608 total Provider tokens versus FULL's 21,591 while both stayed 3/3 correct. At eight distractors, AGENT used 12,523 versus FULL's 43,197.

The observed `2`-distractor crossover is **not** a universal threshold. The durable result is the shape:

```text
Agent selection cost ~= catalog growth + selection cognition + selected source content
FULL cost            ~= complete supplied source content
```

When the available owner-native source world grows faster than the selected task-relevant slice, a fixed selection cost can become cheaper than repeatedly injecting the full world.

## R1 also falsified the original experiment apparatus

The first scale runner stored evidence only at terminal success. One transient DeepSeek disconnect occurred after 35 completed calls and therefore left no accepted R1 receipt. That apparatus was wrong even though the calls were read-only:

```text
campaign terminal success
!=
truth of every completed observation
```

The runner was changed to commit each completed selection and treatment atomically. A second real Provider disconnect then occurred after tier 0, all tier 2 records, and the tier-4 FULL prefix. Restart replayed those committed records rather than dispatching them again them, resumed at the missing phase, and completed the final receipt.

This does not make an in-flight Provider call exactly-once. It proves the narrower research-method requirement that completed experiment evidence survives campaign-process failure.

## What changes in the world model

No new Core revision is justified yet. A6 already states the relevant distinction and this experiment supplies a materially different Finance reproduction.

Two pressures now become sharper:

1. **Selection authority is not selection mechanism.** Agent ownership of relevance does not require a generic Memory service, a Finance-owned WorkingSet, or a separate selection-only Model call.
2. **Experiment evidence is not terminal script status.** Long campaigns need step-owned durable evidence and recovery semantics, especially when external Providers fail transiently.

## Return questions

### Finance

When Finance's research world grows, what owner-native catalog/query/discovery surface lets the Primary Agent select task-relevant evidence without turning `ContextCompiler` or a caller into semantic relevance authority?

### Harness

How should Agent-owned WorkingSet/source selection consume large catalogs or retrieval surfaces while retaining exact provenance, capability visibility, and response-loss recovery?

### Computing

Should incremental experiment-step evidence become a general world-model research-method rule, or does current Runtime/Harness continuity already provide the right primitive once experiments stop bypassing it with direct Adapter calls?
