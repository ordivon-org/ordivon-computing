# State, Computation, and Memory

## Physical and logical state

Information is represented by physical states that can be distinguished and restored. Computation is a controlled transition:

```text
next state = F(current state, input, timing)
```

Registers, caches, memory, persistent storage, networks, and databases provide different latency, capacity, energy, durability, and consistency contracts.

## Classical memory hierarchy

Systems compose layers because no storage technology is best along every dimension:

```text
registers
→ caches
→ DRAM / HBM
→ SSD
→ remote storage
```

Virtual memory separates stable logical addresses from dynamic physical placement. Page tables and copy-on-write preserve useful identity while the operating system manages location and sharing.

These mechanisms remain classical substrate responsibilities.

## Model and Agent state are not one memory

| State | Typical lifetime | Authority |
|---|---|---|
| model parameters | model version | learned statistical structure |
| KV cache | active sequence | inference optimization state |
| conversation history | session | recorded interaction |
| Context | one cognitive episode | selected input, not durable truth |
| Task state | hours to months | work continuity and current frontier |
| Knowledge | long-lived | reusable explanation or model |
| Artifact | long-lived | content-bearing output and evidence |
| world state | external | authoritative reality of the connected domain |

Treating all of these as “memory” or “context” hides their different identities and failure modes.

## Context as a compiled view

A model can consume only a bounded selected representation. The larger authoritative state remains in repositories, databases, journals, Artifacts, and external systems.

```text
durable task and world state
→ select, retrieve, and compress
→ bind source and revision provenance
→ load Context
→ reason and propose
→ persist new evidence and work state
```

Context resembles a working set, but the virtual-memory analogy has limits:

- semantic relevance is not an address translation;
- summaries can lose uncertainty or provenance;
- retrieved content may be malicious or stale;
- different models use the same tokens differently;
- omission changes behavior even when durable state is correct.

The stable system responsibility is selection, provenance, and invalidation—not one retrieval algorithm.

## Three state categories

A useful Agent system separates:

### World state

Files, processes, services, accounts, game worlds, networks, and other external objects.

### Control state

Goals, Tasks, Attempts, Context bindings, Effects, Dispatches, waits, leases, and decisions.

### Epistemic state

Observations, Claims, assumptions, evidence, Verifications, and accepted Facts.

A database can atomically store all three. It does not make their meanings interchangeable.

## Context thrashing and semantic drift

Context thrashing occurs when essential state is repeatedly reconstructed or when a working set exceeds useful context. Semantic drift occurs when summaries, Tool contracts, policies, or external objects change while an old context remains active.

Mitigations include:

- stable source identities and revisions;
- task-local Artifacts;
- explicit Claims and uncertainty;
- invalidation on world or Tool drift;
- compact continuation state;
- independent verification before Fact or Effect admission.

## Design consequence

Persistent authority, physical history, and accepted facts belong in durable state. Context is a replaceable view used by probabilistic cognition.

```text
model memory may fail or be replaced
but Task identity, Effect history, and evidence remain reconstructible
```

See [`classical-substrate-and-agent-overlay.md`](classical-substrate-and-agent-overlay.md) and the [transition study](../../studies/2026-classical-to-agent-native-computing/README.md).
