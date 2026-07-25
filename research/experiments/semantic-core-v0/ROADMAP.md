# Construction Roadmap

## Governing rule

Each layer must solve a failure that cannot be expressed below it. No Host, scheduler, memory platform, Tool catalog, or multi-Agent coordinator is authorized before the semantic core survives real backends.

## M0 — Semantic constitution

**Status:** complete.

Delivered:

- WorldObjectRef, EffectSpec, DispatchRecord, Observation, Artifact, Claim, Verification, and Fact;
- explicit unknown-outcome algebra;
- independent Dispatch identity and admission/rejection lifecycle;
- causal events and optimistic revisions;
- evidence scope, temporal ordering, and VerificationPlan enforcement;
- invariant scanner;
- reusable conformance scenarios.

Exit gate: two independent implementations were integrated; 35 tests pass on the selected Python 3.12.13 runtime.

## M1 — Ordivon semantic adapter

**Status:** complete for the defined v0 scope.

Passed live:

```text
versioned workspace.read
atomic workspace.mutate with digest preconditions
asynchronous workspace.exec and task.observe
Artifact projection and artifact.read
independent read Effect → Verification → Fact
stale-digest rejection without state corruption
duplicate Dispatch rejection
response loss after durable admission
adapter-instance restart and identity re-correlation
cancellation applied to a running Job
natural completion winning a cancellation race
Workspace cleanup
```

M1 v0 exit gate:

- all four required operation classes run through semantic scenarios;
- response loss reconciles without redispatch;
- one stable request identity correlates to exactly one Job;
- `Lost` and `Orphaned` remain unknown;
- repeated delivery does not duplicate completed work;
- cancellation intent remains distinct from terminal cancellation;
- public Tool contracts are sufficient without private Runtime inspection.

Tool-contract drift is deferred to a focused contract-binding slice rather than expanding M1 indefinitely.

## M2 — Durable semantic journal

**Status:** next.

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

- full process restart preserves identity and event order;
- projections can be rebuilt from the journal;
- pending Job correlation survives process restart;
- corruption is reported rather than normalized away.

## M3 — Effect IR codec

Add canonical serialization only after the reference model, durable journal, and live backend agree.

Required properties:

- deterministic normalization;
- stable semantic digest;
- explicit schema revision;
- unknown fields fail closed until compatibility is classified;
- Tool-specific request bodies remain below adapters.

## M4 — Tool contract binding

Introduce the normalized contract needed by real operations and test drift while Effects are pending and running.

## M5 — Task runtime

Only then introduce Goal, Task, Attempt, dependencies, readiness, and completion evidence. Task completion must derive from verified Facts, Artifacts, and Effect outcomes, never model declaration.

## Deferred

- Task Capsule and context compiler;
- provider-neutral Agent Host;
- multi-Agent branch/join;
- organization interface;
- evaluation and post-training flywheel;
- Agent VM or hardware work.
