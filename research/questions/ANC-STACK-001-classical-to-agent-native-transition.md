# ANC-STACK-001 — Classical Substrate and Agent-Native Responsibilities

## Question

Which responsibilities are already provided by classical deterministic computing, which are merely amplified by Agent workloads, and which become structurally new when a probabilistic model can select and revise actions inside a persistent world-changing loop?

## Why this question exists

A project can mistake three different events for the same architectural change:

1. an Agent uses an existing operating-system, database, workflow, or protocol mechanism;
2. Agent scale makes an old mechanism more important;
3. probabilistic cognition invalidates an old assumption and creates a responsibility that no lower layer owns.

Only the third case justifies a new Agent-native layer. The second may justify better composition or operations. The first is ordinary reuse.

Without this distinction, Ordivon can drift toward renaming Linux processes, database transactions, durable workflows, RPC, or role-based access control as new Agent primitives. The opposite error is also possible: treating model output as an ordinary deterministic function result and leaving intent, authority, uncertainty, and evidence to application convention.

## Working hypotheses

### H1 — The classical substrate remains authoritative for physical execution

Operating systems, databases, version-control systems, networks, container or VM boundaries, and durable workflow engines retain responsibility for bytes, processes, transactions, transport, isolation, and replay of already-defined workflows.

### H2 — The changed boundary is semantic, not physical

The primary new responsibility appears where an underspecified human goal and bounded context produce a probabilistic proposal that may cause a durable external effect.

### H3 — Model output is a candidate

A model response is not automatically durable task state, authorized action, observation, verification, or accepted fact. Those roles require separate system objects and authorities.

### H4 — Generic durability is not Agent-native

Kubernetes Jobs and durable workflow systems already persist and recover predeclared work. The Agent-native continuity problem is narrower: preserving and revising the meaning of a goal, task frontier, uncertainty, evidence, and next admissible action across replaceable model episodes.

### H5 — New layers require non-bypassable responsibility

A concept becomes a layer only when it has a stable contract, can fail independently, cannot safely be left to probabilistic context, and creates leverage across at least two materially different workloads.

## Evidence plan

- official classical specifications and implementation documentation;
- official engineering reports from frontier-model laboratories and Agent platform providers;
- executable Ordivon contracts, deterministic tests, live receipts, and cross-backend evidence;
- counterexamples from mature workflow, database, security, and protocol systems;
- falsification attempts against every proposed Agent-native responsibility.

The derivation is preserved in [`../../studies/2026-classical-to-agent-native-computing/`](../../studies/2026-classical-to-agent-native-computing/).

## Admission criteria for a Core change

A result may enter `core/` only when:

1. the classical responsibility has been checked against a primary source;
2. the proposed Agent difference is semantic rather than a naming change;
3. at least one realistic failure trace requires the distinction;
4. the distinction survives comparison with durable workflows and existing security mechanisms;
5. the formulation does not freeze a temporary limitation of current models;
6. the result remains compact enough to generate decisions across projects.

## Falsifiers

The central thesis weakens if any of the following are demonstrated:

- a conventional durable workflow can preserve and safely revise open-ended goal semantics without an external task, context, authority, or evidence layer;
- raw model-session history is as reliable and economical as versioned task state across model, process, and provider replacement;
- model outputs can be admitted as facts or durable effects without independent verification or authority and without increasing failure risk;
- the proposed Agent-native objects do not improve recovery, transfer, safety, or evaluation in real workloads;
- the same responsibilities are already fully and explicitly owned by a mature lower-layer standard.

## Non-goals

- claiming that all computation becomes probabilistic;
- replacing Linux, SQLite, Git, Kubernetes, Temporal, TLS, QUIC, compilers, or model-serving runtimes;
- creating a repository for every conceptual layer;
- promoting current Ordivon implementation details into universal architecture;
- treating research interest as an implementation obligation.
