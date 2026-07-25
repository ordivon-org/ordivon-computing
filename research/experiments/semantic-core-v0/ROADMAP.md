# Construction Roadmap

## Governing rule

Each layer must solve a failure that cannot be expressed below it. No Host, scheduler, memory platform, Tool catalog, or multi-Agent coordinator is authorized before the semantic core survives a real backend.

## M0 — Semantic constitution

**Status:** reference implementation complete.

Delivered:

- WorldObjectRef, EffectSpec, DispatchRecord, Observation, Artifact, Claim, Verification, and Fact;
- explicit unknown-outcome algebra;
- independent Dispatch identity;
- causal events and optimistic revisions;
- evidence ownership and VerificationPlan enforcement;
- invariant scanner;
- reusable conformance scenarios.

Exit gate:

- reference tests pass on Python 3.12 and 3.14;
- no semantic transition depends on conversation state, provider identity, Linux names, or protocol schemas.

## M1 — Ordivon semantic adapter

**Status:** scripted prototype; live validation pending.

First operations:

1. versioned Workspace read;
2. atomic Workspace mutation;
3. asynchronous command execution and observation;
4. output Verification into Fact and Artifact state.

Exit gate:

- reusable scenarios run through a live Ordivon backend;
- response loss reconciles without redispatch;
- `Lost` and `Orphaned` remain unknown;
- repeated delivery does not duplicate completed work;
- public Tool contracts are sufficient without private Runtime inspection.

## M2 — Durable semantic journal

Replace in-memory dictionaries with an append-only store while preserving the same protocol:

```text
effects
dispatches
effect_events
observations
artifacts
claims
verifications
facts
```

Exit gate:

- process restart preserves identity and event order;
- projections can be rebuilt from the journal;
- corruption is reported rather than normalized away.

## M3 — Effect IR codec

Add canonical serialization only after the reference model and live backend agree.

Required properties:

- deterministic normalization;
- stable semantic digest;
- explicit schema revision;
- unknown fields fail closed until compatibility is classified;
- Tool-specific request bodies remain below adapters.

## M4 — Tool contract binding

Introduce only the normalized contract needed by the four real operations:

```text
identity
revision
supported semantic operations
input/output shape
sync/async behaviour
completion semantics
error model
observation path
```

## M5 — Task runtime

Only then introduce Goal, Task, Attempt, dependencies, readiness, and completion evidence. Task completion must derive from verified Facts, Artifacts, and Effect outcomes, never model declaration.

## Deferred

- Task Capsule and context compiler;
- provider-neutral Agent Host;
- multi-Agent branch/join;
- organization interface;
- evaluation and post-training flywheel;
- Agent VM or hardware work.
