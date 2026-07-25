# Agent Semantic Core v0

## Purpose

This experiment defines the minimum semantics required before an Agent Host, Task runtime, memory system, Tool ABI, or multi-Agent coordinator can be trustworthy.

The core answers six questions:

1. What external object is being observed or changed?
2. Which semantic Effect is responsible?
3. Which concrete Dispatch crossed the world boundary?
4. What evidence was actually observed or retained?
5. What outcome is known, failed, cancelled, or still unknown?
6. Which verified claims may enter durable Fact state?

## Primitive separation

```text
WorldObjectRef  address and optional version of an external object
Effect          intended observation or change
Dispatch        one concrete crossing into a Tool or external system
Observation     immutable reading bound to Effect and Dispatch identity
Artifact        durable content result with provenance
Claim           candidate proposition about a world object
Verification    evidence-bound decision about a Claim
Fact            Claim admitted only through accepted Verification
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

## Dispatch state algebra

```text
started
  ├→ admitted
  ├→ unknown
  └→ rejected
```

- `admitted` requires a stable backend operation identity;
- `unknown` never permits a new Dispatch;
- `rejected` requires proof that backend admission did not occur;
- retryable rejection returns the Effect to `prepared` while preserving the rejected Dispatch;
- non-retryable rejection terminates the Effect as `failed`;
- a Dispatch once proven admitted cannot later be called rejected.

Rules:

- `unknown` is explicit and is never converted to `failed` by absence of a response;
- `unknown` cannot be redispatched; it must enter `reconciling`;
- terminal states are immutable;
- every post-dispatch state retains the exact Dispatch identity;
- terminal and uncertainty transitions require evidence;
- optimistic revision checks prevent concurrent state loss.

## Core invariants

1. One identity cannot denote two different semantic objects.
2. One Dispatch identity belongs to exactly one Effect.
3. Event sequence for an Effect is contiguous and causally ordered.
4. A pre-dispatch Effect cannot produce Observation or Artifact evidence.
5. Observation and Artifact evidence must match the Effect's bound Dispatch.
6. A Fact must reference an accepted Verification.
7. A Verification must reference existing Observation or Artifact evidence.
8. A terminal Effect cannot acquire a contradictory terminal outcome.
9. An unknown outcome cannot trigger automatic redispatch.
10. A rejected Dispatch is never the current Dispatch of an Effect.
11. Evidence requires a Dispatch proven admitted.
12. Session loss never erases Effect, Dispatch, event, evidence, or terminal identity.

## Classical-to-Agent mapping

Ordivon remains a backend, not the semantic definition. Its runtime states initially map as follows:

| Ordivon runtime state | Semantic state | Reason |
|---|---|---|
| Accepted with validated plan | Prepared | admitted locally, not yet across the world boundary |
| Starting after dispatch intent | Dispatched | execution may already have crossed the boundary |
| Running | Running | correlated process identity exists |
| Stopping | Cancel requested | intent exists; terminal outcome is not yet known |
| Recovering | Reconciling | runtime is reconstructing external truth |
| Succeeded | Succeeded | only after terminal evidence is committed |
| Failed / Timed out | Failed | definitive process-level terminal evidence |
| Cancelled | Cancelled | cancellation terminal evidence exists |
| Lost / Orphaned | Unknown | absence of ownership is not proof of world failure |

This mapping is provisional and must be tested through an adapter and conformance suite.

## Non-goals for v0

- Goal decomposition or Task scheduling;
- model calls, prompts, context compilation, or memory retrieval;
- general policy or authorization language;
- generic retry or compensation;
- provider-neutral Tool catalogs;
- distributed consensus;
- user interface or organization workflow.
