# ANC-IR-001 — Minimum Useful Agent Effect IR

## Question

What is the smallest representation that can lower an open Goal into external Effects across models, runtimes, and Tool providers while preserving enough semantics for execution and continuation?

## Current hypothesis

A useful minimal Effect contains:

```text
identity
+ parent Task and Attempt
+ target identity
+ preconditions / guards
+ required capability
+ payload
+ idempotent identity
+ result semantics
+ verification path
```

The wider lowering chain is:

```text
Intent
→ Goal
→ Task Graph
→ Effect IR
→ Tool binding
→ Observation
→ Fact / Artifact
```

## Construction order

The serialized IR is not the first artifact. State, identity, causality, evidence, unknown outcomes, and forbidden transitions must first survive an independent reference implementation and a real backend. Otherwise the wire format merely freezes accidental Tool or runtime assumptions.

```text
semantic constitution
→ reference kernel
→ real backend adapter
→ conformance evidence
→ canonical Effect IR codec
```

## First executable artifact

[`../experiments/semantic-core-v0/`](../experiments/semantic-core-v0/) currently provides:

- an executable Agent semantic constitution;
- an in-memory ReferenceKernel;
- independent Effect and Dispatch records;
- reusable conformance scenarios;
- a provider-neutral Tool boundary;
- a live Ordivon `workspace.exec` adapter slice;
- versioned `workspace.read` and compare-and-swap `workspace.mutate`;
- synchronous receipt identities;
- independent reread Verification and Fact admission;
- structured rejection and unknown-delivery separation.

The first heterogeneous slice now includes:

- versioned Workspace file reads;
- atomic mutation against expected text and digest;
- asynchronous command dispatch and observation;
- independent cross-Effect verification and Fact admission.

Failure continuity now includes deliberately lost live responses, adapter-instance restart correlation, and cancellation races. Remaining evidence is concentrated in durable process restart and pending/running Tool-contract drift.

## Current evidence

- synchronous reference execution and asynchronous Ordivon execution share the same semantic state model;
- `unknown` cannot be blindly redispatched and can reconcile by stable request identity;
- retryable and non-retryable pre-admission rejection are distinct from uncertain delivery;
- Effect and Dispatch maintain separate lifecycles;
- `Lost` and `Orphaned` remain unresolved rather than becoming invented failure;
- Effect WorldObject identity is checked against the actual backend Workspace;
- a live Ordivon Job and Attempt produced a semantic Observation and three Artifacts;
- versioned read and `REPLACE_EXACT` mutation were independently verified into two Facts;
- stale digest preconditions failed without corrupting final state;
- two concurrent Semantic Core implementations were integrated, preserving the stronger Dispatch admission/rejection algebra and the stronger cross-Effect evidence semantics;
- the concrete MCP transport remains below the provider-neutral semantic adapter.

This evidence supports the direction but does not yet close ANC-IR-001. Failure injection, contract drift, durable continuation, and canonical serialization remain open.

## Evidence required for closure

- successful representation of several heterogeneous Effects;
- clear handling of synchronous, asynchronous, failed, cancelled, and unknown outcomes;
- continuation after a Tool contract or world-state change;
- comparison with direct ad hoc Tool calls;
- deterministic normalization and stable semantic digest after semantics stabilize.

## Related material

- [`../../core/primitives.md`](../../core/primitives.md)
- [`../../knowledge/agents/goal-task-effect.md`](../../knowledge/agents/goal-task-effect.md)
- [`../../studies/2026-computing-stack-walkthrough/12-agent-language.md`](../../studies/2026-computing-stack-walkthrough/12-agent-language.md)
- [`../experiments/semantic-core-v0/`](../experiments/semantic-core-v0/)
- Ordivon
