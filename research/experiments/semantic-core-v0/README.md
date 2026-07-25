# Semantic Core v0

An executable reference model for the first Agent-native semantic layer:

```text
Reality and Evidence
→ Identity and Causality
→ Outcome Algebra
→ Effect Semantics
```

The reference kernel uses only the Python standard library at runtime. It is intentionally independent of Linux process state, model providers, conversation history, and concrete Tool transports. Ordivon integration lives in a separate adapter prototype and does not define the core semantics.

## Run

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Implemented semantic objects

- typed `SemanticId` identities;
- versioned `WorldObjectRef` targets;
- immutable `EffectSpec` intent;
- independent `DispatchRecord` boundary attempts;
- ordered `EffectEvent` causality;
- immutable `Observation` and `Artifact` evidence;
- `Claim → Verification → Fact` admission;
- optimistic revisions and invariant scanning.

## Critical rules

- an Effect is not a Tool call;
- beginning a Dispatch does not prove acceptance or completion;
- response loss becomes `unknown`, never implicit failure;
- `unknown` must reconcile and cannot blindly redispatch;
- terminal outcomes are immutable;
- accepted Verification must satisfy the Effect's declared evidence plan;
- evidence from one Effect cannot verify a Claim owned by another Effect;
- a Fact cannot predate or bypass its accepted Verification.

## Current maturity

- **M0 semantic reference kernel:** implemented and covered by reusable conformance scenarios;
- **M1 Ordivon adapter:** scripted prototype only; live backend conformance is not yet claimed;
- **durability:** in-memory only;
- **wire format:** intentionally deferred until reference and backend semantics agree.

See [`SPEC.md`](SPEC.md), [`DECISIONS.md`](DECISIONS.md), and [`ROADMAP.md`](ROADMAP.md).
