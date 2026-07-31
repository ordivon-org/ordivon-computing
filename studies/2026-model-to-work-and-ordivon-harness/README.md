# From Model Tokens to Durable Work

Status: completed architecture study  
Date: 2026-07-31  
Durable questions: `ANC-HARNESS-001`, `ANC-HARNESS-002`

This study closes Ordivon's broad research into the complete path from a model invocation to a verified real-world Task outcome.

Its main conclusion is:

```text
A model generates representations.
A Harness turns repeated model and Tool interaction into one Agent Run.
A Host turns replaceable Runs into durable work.
A Runtime turns admitted actions into physical execution and evidence.
A verifier and Host decision turn evidence into semantic completion.
```

The study distinguishes two decisions that had previously been compressed into one word:

1. **H1–H5 decision:** do not flatten Codex App Server, Hermes ACP, Claude Code, or other mature Provider Harnesses into one shared internal lifecycle.
2. **Ordivon Harness decision:** build a thin first-party Agent Loop for bare model APIs and local inference systems that do not already provide a mature Harness.

These decisions are compatible. Ordivon reuses mature Harnesses where they are stronger and owns an Agent Loop where only model intelligence is supplied.

## Route

1. [`00-method-and-claim-boundary.md`](00-method-and-claim-boundary.md) — evidence classes, terminology, and closure rules.
2. [`01-complete-model-to-work-stack.md`](01-complete-model-to-work-stack.md) — the full logical call chain and nested loops.
3. [`02-industry-reference-map.md`](02-industry-reference-map.md) — OpenAI, Anthropic, Microsoft, and Google comparison.
4. [`03-ordivon-experiment-ledger.md`](03-ordivon-experiment-ledger.md) — Continuation, Core Work System, and H1–H5 data.
5. [`experiment-ledger.json`](experiment-ledger.json) — machine-readable claims and measurements.
6. [`04-architecture-decisions.md`](04-architecture-decisions.md) — retain, localize, reject, and reopen decisions.
7. [`05-ordivon-harness-v0-gate.md`](05-ordivon-harness-v0-gate.md) — admitted first implementation and stop conditions.
8. [`REFERENCES.md`](REFERENCES.md) — official primary sources and evidence locations.

## Closed research

The following questions are sufficiently answered within their tested scope:

- which layer owns model generation, Agent Run state, durable Task state, physical execution, and semantic completion;
- whether Provider Session identity is durable Task identity;
- whether process success or Provider final text establishes Task completion;
- whether Codex and Hermes internal lifecycles should be normalized into one shared Provider Harness;
- whether Runtime needs Host Task, Assignment, or completion semantics;
- whether explicit Artifacts and fresh Context can carry work across Provider replacement;
- whether stale Assignment, missing Artifact, and response-loss faults require retained Host objects.

## New engineering question

The remaining bounded question is not another taxonomy exercise:

> What is the smallest Ordivon Harness that can turn a bare model API into a verifiable Agent Run through Ordivon Runtime while preserving the H1–H5 Host boundary?

That question is recorded as [`ANC-HARNESS-002`](../../research/questions/ANC-HARNESS-002-ordivon-harness.md). It is ready for construction, not active literature research.

## Non-claims

This study does not claim:

- that one Agent stack decomposition is the only valid product packaging;
- that Codex, Hermes, Claude, Gemini, or any model are interchangeable;
- that H1–H5 measured general model quality;
- that token counts from different Provider protocols are normalized benchmarks;
- that a first-party Ordivon Harness should replace mature Provider Harnesses;
- that compaction, subagents, parallel Tools, persistent Sessions, or model routing belong in v0;
- that the current boundary has survived adversarial Game, Security, World, or large-scale multi-Agent workloads.

## Final closure rule

Broad Harness architecture research remains closed. Reopen it only when a concrete workload demonstrates one of the following:

- an authoritative fact has no owner;
- a required capability cannot be expressed by the current Assignment/Run/Runtime boundary;
- two independent consumers require the same stable lifecycle semantics;
- substantial duplicate implementation can be removed without flattening Provider behavior;
- the first-party Ordivon Harness cannot remain thin while solving a reproduced failure.
