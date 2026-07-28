# Task, Context, Authority, Effect, and Evidence

These five responsibilities are frequently collapsed into one prompt or Agent loop. Separating them prevents model context from becoming the hidden system of record.

## Task — what work continues

A Task is a durable semantic unit that advances a Goal. It preserves:

- current purpose and completion evidence;
- dependencies and ready frontier;
- Attempts, blockers, and waits;
- relevant world bindings;
- accepted results and unresolved uncertainty.

Generic Task durability is not new: Jobs and durable workflows already survive execution failure. The Agent-specific requirement is preserving a task whose decomposition can be revised through model cognition and new evidence.

## Context — what one model sees

Context is a bounded selected view, not the complete durable state.

```text
authoritative task and world state
→ selection, retrieval, and compression
→ one invocation context
```

A context record should preserve enough source identity and revision information to explain the proposal and detect staleness. A summary is not automatically a Fact merely because later models reuse it.

## Authority — what may be committed

Physical credentials answer whether an executor can reach an object. Semantic authority answers whether this delegated work may produce one specific Effect now.

```text
principal
+ purpose
+ target and version
+ operation
+ consequence envelope
+ budget
+ expiry or revocation
+ approving policy or decision
```

Low-risk reads may use a simple policy. Irreversible or high-consequence effects require stronger binding and possibly human approval.

## Effect — what crosses into reality

An Effect expresses the stable intended observation or change. It should declare:

- target and expected world state;
- operation semantics and input digest;
- required capability or authority reference;
- completion and verification semantics;
- idempotency behavior;
- recovery or compensation path.

Effect identity is separate from Dispatch identity. A stable ID does not make a non-idempotent operation safe to repeat.

## Evidence — what supports acceptance

A model statement, Tool response, process exit, and domain Fact have different epistemic status.

```text
Observation
  immutable external reading or receipt

Artifact
  durable content-bearing output with provenance

Claim
  proposition proposed for evaluation

Verification
  declared method and authority evaluate evidence

Fact
  Claim accepted for a bounded domain and world version
```

The relation can be shared across domains while the verification method remains local.

## Combined trajectory

```text
Task selects ready work
→ Context exposes a bounded current view
→ cognition proposes a Claim or Effect
→ Authority admits or rejects the Effect
→ Runtime dispatches it
→ Observation and Artifact evidence return
→ Verification accepts, rejects, or leaves uncertainty
→ Task state changes
```

This is the minimal semantic path between a probabilistic model and classical execution.

## Design test

A field or object belongs in a shared layer only if removing it creates a specific failure across more than one workload. Otherwise keep it inside the domain application or research experiment.
