# Construction Roadmap

## Governing rule

Each new layer must solve a failure that cannot be expressed by the layer below it. No Host, scheduler, memory platform, Tool catalog, or multi-Agent coordinator is authorized before the semantic core survives real backends.

## M0 — Semantic constitution

**Status: implemented and executable.**

Delivered:

- WorldObjectRef, Effect, DispatchRecord, Observation, Artifact, Claim, Verification, and Fact;
- separate Effect and Dispatch state machines;
- outcome algebra with explicit `unknown` and `reconciling`;
- identity, provenance, causal event sequence, and optimistic revision invariants;
- standard-library in-memory ReferenceKernel;
- reusable conformance scenarios;
- provider-neutral transport error model.

Exit evidence:

- 22 tests pass;
- semantics do not depend on conversation state, model provider, Linux process names, or MCP envelopes.

## M1 — Ordivon semantic adapter

**Status: in progress; asynchronous execution and versioned I/O vertical slices passed.**

Delivered:

```text
EffectSpec
→ WorldObject / Workspace validation
→ DispatchRecord before transport
→ deterministic clientRequestId
→ Ordivon Job / Attempt binding
→ TaskObservation and Artifact translation
→ Dispatch admission / unknown / rejection classification
→ retryable rejection returns Effect to prepared without erasing history
→ task.list / task.observe reconciliation
```

Delivered in the second slice:

1. versioned `workspace.read` with local content-digest validation;
2. one-file atomic `workspace.mutate` guarded by expected digest;
3. synchronous receipt identities;
4. independent reread Verification and Fact admission;
5. stale precondition rejection without overwrite.

Still required:

1. duplicate delivery after terminal completion;
2. real response-loss and restart cases;
3. unknown mutation reconciliation;
4. cancellation and Artifact-integrity races;
5. Tool-contract drift classification and rebinding.

M1 exits only when the shared semantic scenarios are demonstrably portable across the reference model and the real backend. One successful command is evidence for the direction, not completion of the adapter.

## M2 — Durable semantic journal

Replace the in-memory journal with an append-only durable store while preserving the SemanticKernel protocol.

Minimum records:

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

- process restart preserves every identity and event sequence;
- invariant scan reconstructs and validates projections;
- corruption is reported rather than normalized away.

## M3 — Effect IR codec

Only after two implementations agree on semantics, add a canonical serialized representation.

Required properties:

- deterministic normalization;
- stable semantic digest;
- explicit schema revision;
- unknown fields fail closed until compatibility is classified;
- Tool-specific request bodies remain below binding adapters.

## M4 — Tool contract binding

Introduce only the normalized contract required by observed operations:

```text
identity
revision
supported semantic operations
input/output shape
sync/async behavior
completion semantics
error model
observation path
```

First target: reproduce Ordivon schema tightening, classify the change, and rebind only pending Effects.

## M5 — Task runtime

Only then introduce Goal, Task, Attempt, dependencies, readiness, and completion evidence. Task completion must be derived from verified Facts, Artifacts, and Effect outcomes, never from model declaration alone.

## Deferred

- Task Capsule and Context Compiler;
- provider-neutral Agent Host;
- multi-Agent branch/join;
- organization interface;
- evaluation and post-training flywheel;
- Agent VM or hardware work.
