# Agent Semantic Core v0

## Purpose

This experiment defines the minimum semantics required before an Agent Host, Task runtime, memory system, Tool ABI, or multi-Agent coordinator can be trustworthy.

The normative responsibility boundary and hard guarantees are defined in [`KERNEL-CHARTER.md`](KERNEL-CHARTER.md). Failure classes are defined in [`FAILURE-MODEL.md`](FAILURE-MODEL.md). Executable evidence for every current guarantee is indexed in [`CONFORMANCE.md`](CONFORMANCE.md).

The core answers seven questions:

1. What external object is being observed or changed?
2. Which semantic Effect owns the intent?
3. Which concrete Dispatch attempted to cross the world boundary?
4. What evidence was actually observed or retained?
5. What outcome is known, failed, cancelled, or still unknown?
6. Which Claim is being evaluated, and which Effect owns it?
7. Which evidence-bound Verification may admit that Claim as a Fact?
8. Which Authority signed each semantic mutation and evidence record?

## Primitive separation

```text
AuthorityRef   signed role grant with issuer, principal, trust domain, and policy version
Attestation    signed binding between Authority, exact semantic content, contract, and time
WorldObjectRef  external object identity and optional version
EffectSpec      intended observation or change
DispatchRecord  one concrete boundary attempt with request identity and admission state
EffectEvent     ordered causal transition
Observation     immutable reading bound to Effect and Dispatch
Artifact        durable content result with provenance
Claim           candidate proposition owned by one Effect
Verification    evidence-bound decision about a Claim
Fact            Claim admitted through accepted Verification
```

A Tool response is not automatically an Effect outcome. A process exit is not automatically Goal completion. An Artifact is not automatically a Fact.

## Authority and attestation

The public runtime exposes scoped Kernel Views:

```text
effects       EFFECT role
execution     DISPATCH + OBSERVATION roles
verification  VERIFICATION role
facts         FACT role
read          no mutation role
```

Every reducer mutation requires an Attestation. The reducer verifies the signed Authority grant, required role, Attestation kind, contract version, record time, and digest of the exact command or evidence object. Stored events and evidence are revalidated by explicit full invariant audit and Journal replay. Command admission validates only the affected semantic neighborhood.

Ordivon Adapters use the execution View. Claim evaluation and Fact acceptance use separate Verification and Fact Views. See [`AUTHORITY.md`](AUTHORITY.md).

## Public Views and raw reducers

The public mutation boundary is expressed through precise role protocols:

```text
KernelReadView
EffectView
ExecutionView
VerificationView
FactView
```

`AuthorizedKernel` implements these Views according to its issued grants. `ReferenceReducer` and `JournalReducer` are raw reduction mechanisms below that boundary. The historical `ReferenceKernel` and `JournalKernel` names remain compatibility aliases for experiments and tests, not package-root public capabilities.

Ordivon Adapters accept only `ExecutionView`. Knowledge admission accepts separate `VerificationView` and `FactView` handles.

## Effect state algebra

```text
proposed
  → prepared
  → dispatched
  → running ───────────────┐
  → cancel_requested ──────┤
  → unknown → reconciling ─┤
                           ├→ succeeded
                           ├→ failed
                           └→ cancelled
```

`dispatched` means a boundary attempt with stable identity has begun. It does not assert that the external system accepted the operation.

## Dispatch state algebra

```text
STARTED
├── ADMITTED
├── UNKNOWN
└── REJECTED

ADMITTED
└── UNKNOWN

UNKNOWN
├── ADMITTED
└── REJECTED

REJECTED
└── terminal
```

`ADMITTED → UNKNOWN` preserves the proven backend identity while the later outcome becomes uncertain. `UNKNOWN → ADMITTED` represents identity-preserving reconciliation. `UNKNOWN → REJECTED` is valid only when reconciliation proves the original attempt never crossed the backend admission boundary. A Dispatch carrying a backend operation identity cannot be reclassified as rejected.

## Synchronous receipt semantics

A synchronous Tool result that has no durable backend Job is admitted through a receipt identity:

```text
Tool + DispatchId + normalized response digest
```

The receipt proves that the backend returned the structured result. It does not by itself prove a later world state.

## Cross-Effect verification

A Claim may be verified by an Observation from a different succeeded Effect when:

- both address the same WorldObject;
- the evidence kind is permitted by the verification plan;
- accepted version claims match the observed version;
- Observation time does not follow Verification time;
- Fact acceptance does not predate Verification.

This allows a change Effect to be verified by an independent reread Effect rather than self-attestation.

## Core invariants

1. One identity cannot denote two different semantic objects.
2. One Dispatch identity belongs to exactly one Effect.
3. Effect events are contiguous, causally ordered, and non-regressing in time.
4. A STARTED Dispatch does not prove backend admission.
5. Observation and Artifact evidence require an ADMITTED Dispatch.
6. Retryable rejection returns the Effect to prepared with the rejected Dispatch retained as history; non-retryable rejection fails the Effect.
7. An ADMITTED or UNKNOWN Dispatch cannot be reclassified as REJECTED.
8. Observation and Artifact evidence must match the Effect's bound Dispatch.
9. A Claim identifies its originating Effect and a specific world-object subject.
10. Verification evidence may come from independent Effects only when it targets the same subject and compatible version.
11. Evidence must exist no later than the Verification that evaluates it.
12. Accepted Verification must satisfy the originating Effect's declared method and evidence kinds.
13. A Fact must reference an accepted Verification and cannot predate it.
14. Terminal Effect outcomes are immutable.
15. An unknown outcome cannot trigger automatic redispatch.
16. Observation identity includes causal Effect/Dispatch provenance; equal content does not collapse distinct observations.
17. Session or process loss never erases committed Effect, Dispatch, event, evidence, or terminal identity.
18. A failed semantic command leaves every projection unchanged.
19. A semantic transaction commits all commands or none.
20. Durable genesis replay into a fresh Kernel reproduces the committed projection.
21. A stale journal writer cannot append against a changed head.
22. Journal corruption is reported rather than normalized.
23. Every semantic Event and evidence object carries a valid Authority Attestation.
24. An Attestation role must match the mutation role admitted by the reducer.
25. Attested content, contract version, and record time are immutable under verification.
26. Verification and Fact acceptance retain distinct Authority identities.

## Atomicity and durability

Semantic mutation is authorized and transactional:

```text
verify Authority and exact-content Attestation
→ validate candidate state
→ append one or more signed commands in one SQLite transaction
→ commit durable head
→ publish projection
```

A failure before commit leaves every semantic projection unchanged. Result projection may include Dispatch admission, Observation, Artifacts, and terminal state in one transaction. Dispatch start remains a prior durable command because it precedes the external world boundary.

The durable journal is replayed into a fresh Kernel. Replay must reproduce all object identities, revisions, event order, evidence relations, and terminal outcomes. Unsupported schemas, malformed commands, broken hash chains, missing durable head metadata, sequence gaps, tail truncation, semantic replay failures, and stale writer heads fail closed.

The internal journal encoding is not an external Effect IR contract.

## Backend projection mappings

Backend status vocabularies are Adapter inputs, not Kernel enums or public protocol values. Two independent mappings currently satisfy the same semantic contract:

| Semantic state | Ordivon Adapter input | Deterministic Adapter input |
|---|---|---|
| `DISPATCHED` | `queued` | `ACCEPTED` |
| `RUNNING` | `working` | `ACTIVE` |
| `SUCCEEDED` | `succeeded` | `COMPLETE` |
| `FAILED` | `failed` / `timed_out` | `ERROR` |
| `CANCELLED` | `cancelled` | `ABORTED` |
| `UNKNOWN` | `lost` / `orphaned` | `INDETERMINATE` |

The backend operation identity is stored only as the opaque `DispatchRecord.backend_operation_id`. Job IDs, Attempt IDs, simulator operation IDs, correlation keys, receipt structures, transport envelopes, and status terms remain Adapter-local.

Shared conformance compares the resulting semantic projection rather than requiring either backend to adopt the other's contract. This is the executable basis for K11.

## Mutation and audit complexity

A semantic command owns a local undo savepoint and validates the identities, revisions, state transitions, evidence, and Attestations it touches. Unrelated Effects are not copied or rescanned.

```text
command path: local admission + local undo
audit path:   complete cross-projection invariant scan
replay path:  verified command sequence + complete final audit
```

This separation preserves atomicity and corruption detection without making command latency proportional to all historical state.

## Derived read projections

The Kernel exposes canonical records and deterministic read-only projections:

```text
ExecutionTraceView   Effect + Dispatch + ordered Events + evidence
RecoveryView         current state + stable Dispatch identity + required next action
FactProvenanceView   Fact → Verification → Claim → Evidence → producing execution
AuthorityTraceView   ordered Authority and Attestation provenance
```

These Views do not persist new state. They are reconstructed from the same canonical projections and therefore cannot become an independent truth source.

## Layer placement

The following capabilities compose above this Kernel:

- Goal decomposition or Task scheduling;
- LLM/resource scheduling, model routing, token budgeting, or provider selection;
- model calls, prompts, context compilation, or memory retrieval;
- process, filesystem, network, device, or sandbox implementation;
- general policy or authorization language beyond the future minimal authority boundary;
- generic retry or compensation;
- provider-neutral Tool catalogs;
- distributed consensus;
- production transport clients;
- user interface or organization workflow.
