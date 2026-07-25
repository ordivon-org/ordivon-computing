# Initial Architecture Decisions

## D1 — Start with semantics, not serialization

JSON Schema, protobuf, dataclasses, and Rust structs are encodings. State, identity, causality, evidence, and forbidden transitions are defined before an Effect IR wire format is frozen.

## D2 — Use an independent reference implementation

The reference kernel is standard-library Python. Ordivon is Rust and Linux-specific. Agreement between independent implementations is stronger evidence of a universal contract than two implementations sharing one backend's assumptions.

Python is an executable semantic oracle and falsification surface, not the selected production kernel.

## D3 — Separate Effect from Dispatch

An Effect expresses intended world observation or change. A Dispatch is one concrete boundary attempt. `DispatchRecord` has independent identity, request digest, ownership, time, and a lifecycle: `STARTED`, `ADMITTED`, `UNKNOWN`, or `REJECTED`. Starting a boundary attempt does not claim backend admission.

## D4 — Separate pre-admission rejection from uncertain delivery

A structured rejection before backend admission may be retryable or terminal. Once a Dispatch is admitted or becomes unknown, it cannot be rewritten as a pre-admission rejection. This prevents a lost response from being normalized into a safe retry.

## D5 — Treat unknown as a first-class state

No response, lost process ownership, stale local state, or disconnected Host is not proof of failure. `unknown → reconciling → observed outcome` is a core path.

## D6 — Facts require evidence-bound verification

Model text, successful transport, process exit, and Artifact existence are not Facts. A Fact is admitted only when an explicit Claim receives an accepted Verification.

## D7 — Separate Claim origin from evidence origin

A Claim records the Effect that proposed it, but independent verification often requires a different Effect. Cross-Effect evidence is allowed only when its world-object identity and version match the Claim subject, its timestamp does not follow Verification, and it satisfies the originating Effect's VerificationPlan.

## D8 — Keep retries out of v0

Blind retry is unsafe after a Dispatch may have crossed the world boundary. Later work must distinguish new delivery, rebinding, retry, compensation, and a genuinely new Effect.

## D9 — Keep transport below adapters

The semantic core defines Tool-call uncertainty classes but does not implement MCP, HTTP, CLI, or RPC transports. Transport protocol correctness belongs to Tool ABI and adapter work.

## D10 — Keep Goal and Task above the kernel

Goal, Task, scheduling, memory, and model calls consume Effect and evidence state. They do not define the lower semantics.


## D11 — Inherit classical durability mechanisms

Semantic Core does not implement a filesystem, WAL, locking protocol, or crash-safe database. M2 uses standard-library SQLite with WAL and `synchronous=FULL`. The Agent-native layer defines semantic commands, replay, identity, and corruption policy above those classical mechanisms.

## D12 — Make semantic commands and projections transactional

A Kernel command must be all-or-nothing. Related commands may be grouped through `SemanticKernel.transaction()`. Dispatch start remains committed before an external Tool call; result admission, evidence projection, and terminal state are committed as a separate atomic batch.

## D13 — Persist commands, rebuild projections

The durable source is an append-only command journal. Effects, Dispatches, Events, evidence, Claims, Verifications, and Facts are deterministic projections rebuilt by replaying the same reference semantics. Mutable snapshot tables are not the source of truth in v0.

## D14 — Keep the journal codec internal

M2 requires a storage encoding, but that encoding is not the public Effect IR. It is schema-versioned, allowlisted, and replaceable. M3 will define external normalization and compatibility only after durable replay has validated the semantics.

## D15 — Reject stale local writers rather than invent distributed consensus

SQLite orders local commits. `JournalKernel` additionally compares the replayed journal head during each write. A stale process receives `JournalConflict` and must reopen. Replication, consensus, and multi-host availability remain outside M2.


## D16 — Admit Kernel primitives only from failures

A feature does not enter the Kernel because another Agent platform calls it an operating-system primitive. Admission requires a concrete cross-framework failure, a hard invariant, an enforcement boundary, a cost analysis, and a fault test. Scheduler, memory, workflow, provider, channel, and UI capabilities remain above the Kernel unless they satisfy this rule.

## D17 — Freeze the Charter before external IR

The public Effect IR is deferred until the Kernel responsibility boundary, hard guarantees, failure model, and current proof gaps are explicit. Freezing serialization before authority and trust boundaries would convert a prototype API weakness into an ABI obligation.

## D18 — Treat current Facts as Kernel-accepted propositions

`Fact` is retained as the current model name, but its precise meaning is a Claim accepted under a recorded Verification method and evidence set. It is not a guarantee of objective truth, independent trust domains, signed evidence, or Byzantine resistance.

## D19 — Keep K9 authority separation visibly open

The current Python `SemanticKernel` surface exposes proposal, Dispatch, evidence, Verification, and Fact mutation through one object. This is acceptable for a reference reducer but not for a trusted reference monitor. Conformance therefore carries an intentional skipped K9 gate until distinct authenticated authority surfaces and bypass tests exist.
