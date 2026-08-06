# Method and Claim Boundary

## 1. Research question

What is the smallest persistent cognitive-state and mutation model that allows an Ordivon Harness to branch, join, delegate, recover, compile bounded Context, and improve from evidence better than a transcript-centered sequential loop, without creating a universal graph platform, duplicating Host or Runtime authority, or storing private chain of thought?

## 2. Evidence classes

This study separates five evidence classes.

### E1 — first-principles derivation

Claims derived from unavoidable constraints:

- a model invocation receives a bounded materialized view;
- a Task can outlive one invocation, Session, process, or model;
- external effects require stable identity and reconciliation;
- open work can contain simultaneous alternatives and unresolved relations;
- recovery requires committed state outside hidden model state.

E1 establishes necessary responsibilities, not the best implementation.

### E2 — current Ordivon source evidence

Pinned local repositories and exact files show what the current system actually owns and excludes. The source ledger is [`evidence/source-audit-20260806.json`](evidence/source-audit-20260806.json).

E2 can establish a current capability gap. It cannot establish that the proposed replacement will improve outcomes.

### E3 — primary research papers

Peer-reviewed or preprint papers establish observed behavior under their reported tasks and models. They are used for:

- long-context degradation;
- search and graph-structured reasoning;
- external memory and recursive context processing;
- recursive/full-Harness delegation;
- multi-Agent failure modes;
- online Harness adaptation.

Paper results are not transferred to Ordivon without a local ablation.

### E4 — official laboratory and company engineering reports

OpenAI, Anthropic, Google, Microsoft, and Prime Intellect reports establish real architecture choices, production incidents, and measured internal results within their systems. They are first-party sources and may be selective.

### E5 — Ordivon experiment evidence

Only E5 can decide implementation retention. The proposed `TCG-P0` through `TCG-P4` experiments compare current and candidate paths under the same Task, model, Tool contracts, Runtime, and verifier.

## 3. Terminology

### Linear transcript

An append-oriented sequence of messages, Tool requests, observations, and summaries used as the principal cognitive state supplied to later model invocations.

Linear does not mean that the Transformer itself is an RNN. It means that persistent Agent state is primarily serialized as one ordered conversation.

### Global attention

The model's ability to route information among positions inside one materialized context. It does not imply access to omitted state, persistent world facts, other Sessions, or future observations.

### Cognitive graph

A typed relation structure over externalized operational objects such as objective, work item, claim, unknown, evidence, conflict, delegation, Effect proposal, and verification result.

It is not a dump of hidden reasoning and does not claim neurological fidelity.

### Temporal Cognitive Graph

A versioned Cognitive Graph projected from append-only causal events. Time, causality, and authority remain explicit rather than being overwritten by the latest graph state.

### Working Set

The bounded local subgraph and referenced content materialized for one model invocation or Child Run.

### CognitiveMutation

A typed proposal to create, relate, supersede, resolve, activate, or release cognitive objects under an expected graph revision. A model may propose it; Harness admission decides whether it becomes Run state.

### Effect proposal

A proposed observation or external change. It is not a CognitiveMutation merely because a model expressed it. It must cross ToolGrant, authority, Effect, Dispatch, Runtime, Observation, and verification boundaries.

### Run Actor

A durable Harness Run with a Contract, mailbox, revision, budget, Engine Session binding, wakeup conditions, Child Runs, and recovery state. “Actor” describes lifecycle and message ownership, not a general distributed Actor framework requirement.

## 4. The two-dimensional metaphor and its limit

“One-dimensional to two-dimensional cognition” is a useful diagnosis:

- one dimension is ordered time and causal continuation;
- the second is simultaneous semantic relation and branching.

The complete system has additional dimensions:

- Actor ownership;
- authority and consequence;
- physical execution;
- world version and verification.

The implementation should therefore use typed temporal relations, not a literal matrix and not one undifferentiated graph.

## 5. Authority boundary

The candidate must preserve:

```text
Model / Engine
  proposes cognitive and action changes

Harness
  owns Run-local cognitive state, Engine Sessions, Child Runs, and proposal admission

Host
  owns durable Task commitments, responsibility, consequence admission, verification, and Outcome

Runtime
  owns physical Workspaces, Jobs, Attempts, Workers, process trees, Artifacts, and reconciliation

Domain / verifier
  owns authoritative world truth and semantic sufficiency
```

No graph relation transfers authority merely by referencing an object owned elsewhere.

## 6. State authority rule

The authoritative order is:

```text
append-only events and immutable referenced objects
        ↓
validated projection
        ↓
query index and materialized Working Set
        ↓
model-visible representation
```

A graph database, vector index, cache, Python kernel, KV cache, or prompt is never the sole source of truth.

## 7. Privacy and reasoning boundary

The system should externalize only state that another executor, verifier, operator, or recovery process needs:

- objective and constraints;
- proposed and accepted work decomposition;
- claims, assumptions, unknowns, and conflicts;
- evidence references and provenance;
- decisions and status;
- delegated scopes and returned results;
- effects, observations, and verification.

It should not require raw hidden chain of thought, token activations, or unverifiable introspective narratives. Natural-language rationale may be retained when it changes an admission, handoff, or audit decision, but it is not authority.

## 8. Admission test for every new object

A candidate node, edge, event, state, API, index, daemon, Worker, or schema is admitted only if it names:

1. the current failure it prevents;
2. the owner of its truth;
3. the independent transition or recovery decision it enables;
4. its reader and writer;
5. its invalidation rule;
6. its recurring storage, token, coordination, and maintenance cost;
7. the narrower alternative;
8. the experiment that can delete it.

## 9. Non-claims

This study does not claim:

- that graph-shaped state is universally better than transcripts;
- that Graph of Thoughts is a production state model;
- that multi-Agent systems are always superior;
- that long context is useless;
- that all model reasoning should be explicit;
- that a graph database is required;
- that Host should become a general workflow engine;
- that Runtime should become a scheduler;
- that Prime Agent, RLM, or any external Harness should replace Ordivon;
- that the current study has earned Protocol promotion;
- that self-improvement is safe without independent evaluation and rollback.

## 10. Closure rule

The architecture study is complete when it provides a coherent derivation, source audit, external evidence comparison, candidate model, experiment contract, and reversible migration. The implementation question remains open until local trials establish net benefit.
