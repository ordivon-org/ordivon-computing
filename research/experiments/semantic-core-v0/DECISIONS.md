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

A Kernel command must be all-or-nothing. Related commands may be grouped through a role-scoped View transaction. Dispatch start remains committed before an external Tool call; result admission, evidence projection, and terminal state are committed as a separate atomic batch.

## D13 — Persist commands, rebuild projections

The durable source is an append-only command journal. Effects, Dispatches, Events, evidence, Claims, Verifications, and Facts are deterministic projections rebuilt by replaying the same reference semantics. Mutable snapshot tables are not the source of truth in v0.

## D14 — Keep the journal codec internal

M2 requires a storage encoding, but that encoding is not the public Effect IR. It is schema-versioned, allowlisted, and replaceable. M3 will define external normalization and compatibility only after durable replay has validated the semantics.

## D15 — Reject stale local writers rather than invent distributed consensus

SQLite orders local commits. `JournalReducer` additionally compares the replayed journal head during each write. A stale process receives `JournalConflict` and must reopen. Replication, consensus, and multi-host availability remain outside M2.


## D16 — Admit Kernel primitives only from failures

A feature does not enter the Kernel because another Agent platform calls it an operating-system primitive. Admission requires a concrete cross-framework failure, a hard invariant, an enforcement boundary, a cost analysis, and a fault test. Scheduler, memory, workflow, provider, channel, and UI capabilities remain above the Kernel unless they satisfy this rule.

## D17 — Freeze the Charter before external IR

The public Effect IR is deferred until the Kernel responsibility boundary, hard guarantees, failure model, and current proof gaps are explicit. Freezing serialization before authority and trust boundaries would convert a prototype API weakness into an ABI obligation.

## D18 — Define Fact through positive admission semantics

A `Fact` is a Claim admitted through a recorded accepted Verification bound to the required evidence plan. The Kernel preserves the complete Claim, evidence, method, decision, and acceptance history.

## D19 — Build role-scoped authority before external IR

M2.5 introduces distinct proposal, Dispatch, Observation, Verification, and Fact authority surfaces before the public Effect IR is frozen. This keeps authority semantics inside the design rather than retrofitting them after serialization.


## D20 — Separate Authority roles

Effect proposal, Dispatch execution, Observation production, Verification decision, and Fact acceptance are distinct signed roles. The standard runtime bootstrap returns scoped Views and exposes no full-authority convenience View.

## D21 — Derive one signing key per Authority

The root HMAC policy signs Authority grants and derives a separate attestation key for every issued Authority. Runtime Views receive only their own derived signer, so possession of one role signer cannot produce a valid attestation for another role.

## D22 — Bind Attestation to exact semantic content

Every mutation and evidence object is digested from its operation name, positional arguments, keyword arguments, contract version, and record time. Reducer admission, invariant scanning, and replay recompute and verify this binding.

## D23 — Bind durable history to semantic and authority versions

Journal schema v2 stores signed grants and Attestations. Metadata binds the semantic model version, reducer version, and authority-policy fingerprint before replay.

## D24 — Return official attested projections

Adapters and verification helpers return the records retrieved from the Kernel after admission, rather than unsigned draft objects created before admission.


## D25 — Separate public Views from raw reducers

Role-scoped public protocols live in `interfaces.py`. `AuthorizedKernel` implements those protocols with signed Authority grants. `ReferenceReducer` and `JournalReducer` are raw mechanisms below the Authority boundary. Historical Kernel names remain compatibility aliases only.

## D26 — Give Effect and Dispatch separate explicit state graphs

Effect lifecycle and Dispatch admission lifecycle answer different questions. Both transition predicates are now explicit in `state.py`; reducer methods must pass the relevant graph before changing state.

## D27 — Divide invariant validation by semantic responsibility

The complete invariant scan remains one public operation but delegates to five domains: Effect history, Dispatch binding, evidence provenance, knowledge admission, and Attestation validity. This improves fault localization without creating a plugin framework or weakening full-state validation.

## D28 — Derive projections instead of storing explanation state

Execution, recovery, Authority, and Fact-provenance Views are reconstructed from canonical records. Human and Agent explanations therefore gain focused projections without a second mutable truth source.


## D29 — Use local undo savepoints on the command path

Each reducer command records undo actions only for touched keys and list suffixes. Command admission validates its affected semantic neighborhood. Full cross-projection invariant scanning remains an explicit audit and replay operation rather than a per-command tax.

## D30 — Append Journal commands inside the live reducer transaction

`JournalReducer` no longer clones the complete reducer or compares full snapshots. The live reducer mutation remains rollback-capable until SQLite append succeeds. Append failure and stale-writer conflict therefore undo the in-memory change without duplicating all state.

## D31 — Quarantine unimplemented model fields

Free-text Preconditions, Task/Attempt parent IDs, keyed idempotency keys, and capability expiry remain decode-only Journal-v2 compatibility fields. New Effects reject them until a real Task Runtime, Effect Binding, or policy enforcement mechanism exists.

## D32 — Migrate known Journal histories without rewriting commands

Migration is allowed only from the exact known v2 or v3 semantic-model and reducer versions under the same Authority-policy fingerprint. Historical command payloads remain immutable; new tail entries use the current schema.

## D33 — Reject the first checkpoint design after measurement

The exact prototype at `23353fdd550badf090c404861755131a70b7807b` duplicated state, enlarged the database, and reopened more slowly than optimized genesis verification. The runtime feature was removed. Future checkpoint work requires a new representation and positive benchmark evidence.


## D34 — Prove portability with a structurally distinct backend

A second backend must differ in operation names, status vocabulary, correlation identity, receipt shape, and implementation objects. Replaying Ordivon payloads through a mock would test only the Ordivon Adapter. The deterministic simulator therefore defines its own object, Job, mutation, status, and failure contracts.

## D35 — Compare semantic projections, not backend payloads

Portable conformance compares Effect states, Dispatch preservation, Event kinds, evidence, Fact admission, Authority roles, delivery count, and fault isolation. Backend Job IDs, operation IDs, status words, and receipt envelopes remain opaque Adapter bindings and are intentionally absent from the normalized report.

## D36 — Keep the portability oracle internal

The deterministic backend and `BackendPortabilityDriver` are experiment and conformance mechanisms. They are not package-root exports, a generic Backend interface, or a production plugin framework. A future public execution ABI must be justified separately by the Effect IR and Tool-contract work.


## D37 — Keep public contracts outside the Kernel

The Kernel does not import canonical JSON, `EffectEnvelope`, `ToolContract`, encoder, or contract-diff packages. It receives only a signed `BindingAdmission` projection and persists the exact Binding edge used by a Dispatch.

## D38 — Separate Effect, Binding, and Dispatch authority

Effect Authority admits stable intent, Binding Authority attests the selected contract and argument digest, and Dispatch Authority records one actual boundary attempt. No one role implicitly grants the other two.

## D39 — Rebinding is not retry

A new immutable Binding revision is allowed only while an Effect is pre-dispatch or after a retryable rejection proven to occur before Backend admission. Active, uncertain, reconciling, and terminal Effects retain the original Binding and cannot use catalog refresh to create another delivery.

## D40 — Journal schema v4 preserves legacy unbound Dispatches

Binding support is optional on `DispatchRecord`. Exact v2/v3 histories replay as unbound legacy Dispatches, while v4 commands may carry a signed Binding edge. Migration updates metadata only and never rewrites historical command payloads.
