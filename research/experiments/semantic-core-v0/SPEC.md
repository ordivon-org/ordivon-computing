# Agent Semantic Core v0

## Purpose

This experiment defines the minimum semantics required before an Agent Host, Task runtime, memory system, Tool ABI, or multi-Agent coordinator can be trustworthy.

The normative responsibility boundary and hard guarantees are defined in [`KERNEL-CHARTER.md`](KERNEL-CHARTER.md). Failure classes and trust assumptions are defined in [`FAILURE-MODEL.md`](FAILURE-MODEL.md). The current implementation must not claim guarantees beyond [`CHARTER-CONFORMANCE.md`](CHARTER-CONFORMANCE.md).

The core answers seven questions:

1. What external object is being observed or changed?
2. Which semantic Effect owns the intent?
3. Which concrete Dispatch attempted to cross the world boundary?
4. What evidence was actually observed or retained?
5. What outcome is known, failed, cancelled, or still unknown?
6. Which Claim is being evaluated, and which Effect owns it?
7. Which evidence-bound Verification may admit that Claim as a Fact?

## Primitive separation

```text
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
20. Durable replay into a fresh Kernel reproduces the committed projection.
21. A stale journal writer cannot append against a changed head.
22. Journal corruption is reported rather than normalized.

## Atomicity and durability

Semantic mutation is transactional:

```text
validate candidate state
→ append one or more commands in one SQLite transaction
→ commit durable head
→ publish projection
```

A failure before commit leaves every semantic projection unchanged. Result projection may include Dispatch admission, Observation, Artifacts, and terminal state in one transaction. Dispatch start remains a prior durable command because it precedes the external world boundary.

The durable journal is replayed into a fresh Kernel. Replay must reproduce all object identities, revisions, event order, evidence relations, and terminal outcomes. Unsupported schemas, malformed commands, broken hash chains, missing durable head metadata, sequence gaps, tail truncation, semantic replay failures, and stale writer heads fail closed.

The internal journal encoding is not an external Effect IR contract.

## Ordivon mapping hypothesis

| Ordivon runtime state | Semantic state | Reason |
|---|---|---|
| Accepted with validated plan | Prepared | admitted locally, not yet externally running |
| Starting after dispatch intent | Dispatched | a correlated execution attempt exists |
| Running | Running | process identity is observed |
| Stopping | Cancel requested | cancellation intent is not terminal evidence |
| Recovering | Reconciling | runtime is reconstructing external truth |
| Succeeded | Succeeded | terminal process evidence is committed |
| Failed / Timed out | Failed | definitive process-level terminal evidence |
| Cancelled | Cancelled | cancellation terminal evidence exists |
| Lost / Orphaned | Unknown | loss of ownership is not proof of world failure |

This mapping remains provisional until live adapter conformance is run.

## Non-goals for v0

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
