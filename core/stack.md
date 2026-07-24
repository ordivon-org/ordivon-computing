# Agent-Native Computing Stack

This stack maps the layers through which physical state becomes computation, probabilistic cognition, persistent action, and human–agent organization.

| Layer | Subject | Central question |
|---|---|---|
| L0 | Physical devices | What are the energy, movement, persistence, and communication costs of the workload? |
| L1 | Compute primitives | Which dense, sparse, attention, state-space, reduction, and cryptographic primitives deserve direct support? |
| L2 | Memory and interconnect | How should weights, activations, KV state, task state, knowledge, and artifacts be placed and moved? |
| L3 | Dataflow substrate | When should execution be stream-, graph-, event-, or instruction-driven? |
| L4 | ISA and machine contracts | What machine operations and execution contracts expose the substrate effectively? |
| L5 | Host kernel and isolation | How are processes, resources, namespaces, capabilities, faults, and persistence managed? |
| L6 | Compiler and general IR | How do high-level programs lower into efficient deterministic execution? |
| L7 | Model runtime | How are inference, batching, routing, KV state, quantization, and distributed execution managed? |
| L8 | Foundation-model architecture | Which learned architectures best combine reasoning, memory, perception, generation, and world modelling? |
| L9 | Training and update | How are models, data, preferences, tools, memory, and runtime behaviour learned and versioned? |
| L10 | Agent language and IR | How are open goals lowered into typed, revisable, capability-aware effect plans? |
| L11 | Agent execution kernel | How are goals, tasks, attempts, workspaces, effects, artifacts, cancellation, and recovery made durable? |
| L12 | World and tool interface | How are external systems exposed through identities, contracts, schemas, capabilities, and completion semantics? |
| L13 | Product and organization | How do humans and Agents assign goals, create, verify, cooperate, learn, and bear consequences? |

## Five cross-cutting planes

These concerns connect every layer:

1. **Identity** — stable identity for principals, models, tasks, attempts, workspaces, tools, artifacts, runtimes, and world objects.
2. **Capability** — which actor can perform which effect on which object under which conditions.
3. **State and memory** — how physical state, model state, context, task state, knowledge, and external reality relate across time.
4. **Evidence and verification** — how observations, tests, artifacts, receipts, and world facts support claims.
5. **Time and recovery** — ordering, waiting, retries, checkpoints, compensation, continuation, and learning.

## Two directions through the stack

Bottom-up:

```text
physical state
→ machine computation
→ model cognition
→ Agent execution
→ world change
→ organizational value
```

Top-down:

```text
human goal
→ task and effect semantics
→ runtime and tools
→ model and machine programs
→ physical state transition
```

The complete system closes the loop:

```text
goal
→ computation
→ world change
→ observation
→ revised goal
```

Detailed learning material is preserved in [`../studies/2026-computing-stack-walkthrough/`](../studies/2026-computing-stack-walkthrough/).
