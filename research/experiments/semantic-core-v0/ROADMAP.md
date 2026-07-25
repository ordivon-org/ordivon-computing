# Construction Roadmap

## Governing rule

Each layer must solve a failure that cannot be expressed below it. Mature classical mechanisms are inherited where they already solve the problem; Agent-native work is limited to missing semantic responsibility.

## M0 — Semantic constitution

**Status:** v0 complete.

Delivered identity, Effect, Dispatch, causal events, uncertainty, evidence, Verification, Fact, optimistic revisions, and reusable conformance scenarios.

## M1 — Ordivon semantic adapter

**Status:** v0 complete.

Delivered real versioned I/O, mutation guards, asynchronous execution, Observation/Artifact projection, response-loss recovery, cancellation races, and stable Job correlation through public Tool contracts.

## M1.5 — Kernel atomicity closure

**Status:** complete.

Exit gates passed:

- a failed command leaves every projection unchanged;
- multi-command semantic batches are all-or-nothing;
- Adapter result projection is transactional;
- malformed backend payloads cannot leave partial binding or evidence;
- Dispatch state must have corresponding causal Events.

## M2 — Durable semantic journal

**Status:** v0 complete.

Delivered SQLite WAL/FULL persistence, an append-only command journal, an internal schema-v1 allowlisted codec, chained entry digests, durable head metadata, deterministic reconstruction, process restart, pending-Job correlation, and stale-writer rejection through journal-head CAS.

Exit gates passed:

- process restart preserves identity and event order;
- Effect, Dispatch, Observation, Artifact, Claim, Verification, and Fact projections rebuild;
- pending Job correlation survives process restart;
- corrupt or incomplete journals fail closed;
- real Ordivon recovery does not redispatch.

Deferred production work: snapshots, compaction, replication, online schema migration, encryption policy, and performance tuning.

## M2.25 — Kernel Charter and falsification surface

**Status:** complete.

Delivered:

- a normative Kernel mission and classical-OS responsibility boundary;
- eight proven hard guarantees K1–K8;
- a positive capability contract and explicit cost budget;
- classical, distributed, and Agent-native failure taxonomy;
- canonical fault-injection tests linked to every guarantee;
- a rule that future Kernel primitives require a demonstrated failure and falsifiable invariant.

## M2.5 — Authority and attestation boundary

**Status:** next.

Required exit gates:

- separate Effect proposal, Dispatch admission, Observation attestation, Verification decision, and Fact acceptance authority surfaces;
- role-scoped handles and authenticated issuers;
- evidence records issuer, trust domain, attestation kind, and contract version;
- Fact admission carries the responsible authority and verification policy;
- journal entries bind semantic reducer and authority-policy versions;
- adversarial tests prove role isolation and authority provenance.

## M3 — Effect IR codec

**Status:** follows M2.5.

Define an external canonical representation only after M0–M2 agreement.

Required properties:

- deterministic normalization;
- stable semantic digest;
- explicit schema revision;
- unknown fields fail closed until compatibility is classified;
- Tool-specific request bodies remain below adapters;
- internal journal storage encoding remains replaceable.

## M4 — Tool contract binding

Normalize the minimum contract required by real operations and test schema drift while Effects are pending and running.

## M5 — Task runtime

Introduce Goal, Task, Attempt, dependencies, readiness, and completion evidence only after Effect IR and Tool contracts stabilize. Task completion must derive from verified Facts, Artifacts, and Effect outcomes.

## Deferred

- Task Capsule and context compiler;
- provider-neutral Agent Host;
- memory platform;
- multi-Agent branch/join;
- organization interface;
- evaluation and post-training flywheel;
- Agent VM or hardware work;
- full classical/Agent hybrid product architecture.
