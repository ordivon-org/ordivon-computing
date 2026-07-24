# Agent-Native Computing Stack

This stack is a research map, not a claim that every layer must be rebuilt.

| Layer | Subject | Central question |
|---|---|---|
| L0 | Physical devices | What are the energy, movement, persistence, and communication costs of agent workloads? |
| L1 | Compute primitives | Which dense, sparse, attention, state-space, reduction, and cryptographic primitives deserve direct support? |
| L2 | Memory and interconnect | How should weights, activations, KV state, working memory, durable task state, and artifacts be placed and moved? |
| L3 | Dataflow substrate | When should execution be stream-, graph-, event-, or instruction-driven? |
| L4 | ISA and machine contracts | What execution primitives should exist above or beside classical load/store instructions? |
| L5 | Host kernel and isolation | How should resources, processes, namespaces, capabilities, and faults be contained? |
| L6 | Compiler and general IR | How do model and agent programs lower into efficient deterministic execution? |
| L7 | Model runtime | How are inference, batching, routing, KV state, quantization, and distributed execution managed? |
| L8 | Foundation-model architecture | Which cognitive architectures best combine reasoning, memory, perception, and learned world models? |
| L9 | Training and update | How are models, prompts, tools, memory, policies, and runtimes versioned and changed? |
| L10 | Agent language and IR | How are goals lowered into typed, revisable, capability-aware effect plans? |
| L11 | Agent execution kernel | How are tasks, attempts, workspaces, mutations, artifacts, cancellation, and recovery made durable? |
| L12 | World and tool interface | How are external systems exposed with explicit effects, authority, schemas, and completion semantics? |
| L13 | Product and organization | How do humans and agents assign goals, approve actions, verify results, cooperate, and bear responsibility? |

## Cross-cutting planes

Five concerns cross every layer:

1. **Identity** — stable identity for principals, agents, tasks, workspaces, tools, artifacts, and runtimes.
2. **Capability** — who may perform which effect, on what object, under which conditions.
3. **State and memory** — separation of belief, context, task state, durable knowledge, and external reality.
4. **Evidence and verification** — distinction between claims, process outcomes, tests, receipts, and verified world state.
5. **Time and recovery** — ordering, interruption, retries, checkpoints, compensation, and resumption.

## Current project placement

```text
Agent-native computing
├── execution kernel
│   └── Ordivon
├── domain governance systems
│   └── FinHarness
└── long-horizon empirical research
    └── Ordinary Prosperity Research
```
