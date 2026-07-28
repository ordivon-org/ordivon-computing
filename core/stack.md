# Classical Substrate and Agent-Native Responsibility Overlay

Ordivon studies the complete computing world but does not treat that world as an implementation roadmap. The current architecture separates the inherited execution substrate from responsibilities that are introduced or materially rewritten when probabilistic cognition participates in persistent action.

## 1. Inherited substrate map

| Band | Subject | Authoritative responsibility |
|---|---|---|
| S0 | physical devices and compute primitives | energy, movement, storage, communication, arithmetic, acceleration |
| S1 | machine, operating system, and isolation | ISA, processes, memory, files, namespaces, devices, scheduling, containment |
| S2 | deterministic software and data systems | compilers, language runtimes, databases, version control, networks, protocols, durable workflows |
| S3 | model learning and inference | training, parameters, tokenization, batching, KV state, routing, quantization, serving |

These bands remain active research subjects. Ordivon normally composes their mature implementations rather than reimplementing them.

## 2. Agent-native responsibility overlay

| Responsibility | Subject | Central question |
|---|---|---|
| R0 | human purpose and consequence ownership | Why is the system acting, what counts as completion, and who bears the consequences? |
| R1 | operator attention and governance | Which decisions require a person, and what evidence and alternatives should be presented? |
| R2 | open-work continuity | What Goal, Task frontier, Attempts, waits, and uncertainty persist across model and process replacement? |
| R3 | context and memory compilation | Which versioned subset of durable state should influence one probabilistic cognitive episode? |
| R4 | cognition and coordination | Which model, branch, verifier, Join, stopping rule, or human escalation should be selected next? |
| R5 | authority and consequence admission | May this principal commit this Effect now against this world version within this budget and consequence envelope? |
| R6 | Effect commitment and reconciliation | How does one stable proposal bind to a concrete Dispatch, survive response loss, and reconcile with reality? |
| R7 | evidence, verification, and epistemic state | What was observed, what is claimed, how was it verified, and what can be accepted as current Fact? |

The overlay is a feedback graph, not a strict linear call stack.

## 3. Hybrid execution boundary

```text
human purpose
→ persistent open work
→ version-bound context
→ probabilistic proposal
→ deterministic authority and Effect admission
→ classical execution substrate
→ Observation and Artifact evidence
→ Verification and revised work
→ human decision when consequence or uncertainty requires it
```

The model supplies flexible search over possible next steps. Deterministic state establishes what was admitted, dispatched, observed, and accepted.

## 4. What is not new

The following mechanisms remain classical even when Agents use them:

- processes, Jobs, retries, queues, and controllers;
- database transactions, event logs, and crash recovery;
- Git objects, branches, and content identity;
- containers, VMs, sandboxes, and network policy;
- RPC, MCP, A2A, and Tool schemas;
- compilers, tests, tracing, and metrics;
- model training and inference serving;
- replay of predeclared durable workflows.

Agent scale can amplify their importance. Composition can create a valuable product. Neither fact alone creates a new layer.

## 5. Cross-cutting invariants

1. **Identity** — principals, Goals, Tasks, model invocations, Effects, Dispatches, Artifacts, authorities, and world objects retain stable identities across replacement.
2. **Version binding** — context, policies, Tools, repositories, models, and external objects bind to observable revisions.
3. **Explicit uncertainty** — unknown outcome and unsupported Claim remain distinct from failure, success, and Fact.
4. **Provenance** — durable outputs preserve their source, causal relation, and verification path.
5. **Consequence and reversibility** — reversible exploration is distinguished from durable or irreversible commitment.
6. **Recovery** — current work and effect history can be reconstructed without relying on model memory.

## 6. Promotion rule

A proposed layer must answer:

```text
Which mature lower mechanism is insufficient?
What exact invariant remains unowned?
What realistic trajectory fails if the layer is bypassed?
Which second workload demonstrates the same responsibility?
Can the mechanism remain a policy or module instead of a new repository?
```

Unanswered proposals remain in Research.

## 7. Two complementary studies

- [`../studies/2026-computing-stack-walkthrough/`](../studies/2026-computing-stack-walkthrough/) preserves the full physical-to-institutional learning route.
- [`../studies/2026-classical-to-agent-native-computing/`](../studies/2026-classical-to-agent-native-computing/) derives the substrate/overlay boundary, counterexamples, evidence, and falsifiers.
