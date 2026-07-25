# Agent Semantic Core v0

## Purpose

This experiment defines the minimum semantics required before an Agent Host, Task runtime, memory system, Tool ABI, or multi-Agent coordinator can be trustworthy.

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
DispatchRecord  one concrete boundary attempt with request identity
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

## Core invariants

1. One identity cannot denote two different semantic objects.
2. One Dispatch identity belongs to exactly one Effect.
3. Effect events are contiguous, causally ordered, and non-regressing in time.
4. A pre-dispatch Effect cannot produce Observation or Artifact evidence.
5. Observation and Artifact evidence must match the Effect's bound Dispatch.
6. A Claim must identify its owning Effect and target the same world object.
7. Verification evidence must belong to the Claim's owning Effect.
8. Accepted Verification must satisfy the Effect's declared method and evidence kinds.
9. A Fact must reference an accepted Verification and cannot predate it.
10. Terminal Effect outcomes are immutable.
11. An unknown outcome cannot trigger automatic redispatch.
12. Session loss never erases Effect, Dispatch, event, evidence, or terminal identity.

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
- model calls, prompts, context compilation, or memory retrieval;
- general policy or authorization language;
- generic retry or compensation;
- provider-neutral Tool catalogs;
- distributed consensus;
- production transport clients;
- user interface or organization workflow.
