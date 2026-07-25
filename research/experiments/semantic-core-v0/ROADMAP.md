# Construction Roadmap

## Governing rule

Each layer must solve a failure that cannot be expressed below it. No Host, scheduler, memory platform, Tool catalog, or multi-Agent coordinator is authorized before the semantic core survives real backends.

## M0 — Semantic constitution

**Status:** reference implementation complete.

Delivered:

- WorldObjectRef, EffectSpec, DispatchRecord, Observation, Artifact, Claim, Verification, and Fact;
- explicit unknown-outcome algebra;
- independent Dispatch identity and admission/rejection lifecycle;
- causal events and optimistic revisions;
- evidence scope, temporal ordering, and VerificationPlan enforcement;
- invariant scanner;
- reusable conformance scenarios.

Exit gate: two independent implementations were integrated; 27 tests pass on Python 3.12.13 and 3.14.6.

## M1 — Ordivon semantic adapter

**Status:** active; four-operation live vertical slice passed.

Passed live:

```text
versioned workspace.read
atomic workspace.mutate with digest preconditions
asynchronous workspace.exec and task.observe
Artifact projection and artifact.read
independent read Effect → Verification → Fact
stale-digest rejection without state corruption
duplicate Dispatch rejection
Workspace cleanup
```

Remaining failure cases:

1. response loss after durable admission;
2. cancellation and natural completion race;
3. adapter restart and identity re-correlation;
4. Tool-contract drift while pending and running.

M1 exit gate:

- all four required operations run through reusable semantic scenarios;
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
