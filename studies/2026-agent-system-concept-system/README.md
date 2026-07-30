# Agent System Concept System

This study organizes the rapidly expanding vocabulary of Agent systems into a coherent set of research objects, responsibility boundaries, mature classical baselines, and falsifiable Ordivon hypotheses.

The central result is not a new universal ontology. It is a small ownership rule:

```text
Host owns durable work.
Harness owns the cognitive episode and Agent loop.
Runtime owns physical execution facts.
```

Everything else—Goals, Tasks, Skills, Tools, Hooks, Events, Graphs, Loops, Sessions, Checkpoints, Leases, Artifacts, Policies, and Evals—must be classified by what it is, who owns authoritative state, and how it fails under restart, replacement, duplication, or drift.

## Why this study exists

Modern products frequently package multiple architectural roles under one product name:

```text
Codex / Claude Code
= Surface + interaction Host + Harness + Session + execution adapters + sandbox
```

That product packaging is useful, but it obscures reusable boundaries. Ordivon already separated durable execution into `ordivon-runtime` and durable open work into `ordivon-host`. The remaining question is whether an explicit thin Harness boundary creates enough portability, evaluation power, and conceptual clarity to justify a shared module or repository.

This study therefore asks:

1. Which concepts are objects, containers, control mechanisms, records, or distribution units?
2. Which state is authoritative in Host, Harness, Runtime, a Tool provider, or a domain world?
3. Which mechanisms are inherited from operating systems, durable workflows, distributed systems, observability, and protocol design?
4. Which Agent-specific responsibilities remain after those mature mechanisms are reused?
5. What must be tested before `ordivon-harness` or any new protocol surface is promoted?

## Files

- [`00-method-and-admission.md`](00-method-and-admission.md) — methodology, maturity levels, promotion and deletion rules.
- [`01-concept-taxonomy.md`](01-concept-taxonomy.md) — the complete classification axes and concise definitions.
- [`02-host-harness-runtime-boundaries.md`](02-host-harness-runtime-boundaries.md) — component roles, object ownership, lifecycle, and thin Harness hypothesis.
- [`03-skills-tools-hooks-and-events.md`](03-skills-tools-hooks-and-events.md) — Skills, Tools, Hooks, Events, Commands, Signals, Policies, Plugins, and Connectors.
- [`04-goals-tasks-graphs-loops-and-state.md`](04-goals-tasks-graphs-loops-and-state.md) — Goal-to-Job object chain, graph families, loop families, memory and state.
- [`05-durability-coordination-and-recovery.md`](05-durability-coordination-and-recovery.md) — checkpoints, journals, leases, fencing, idempotency, compensation, queues, and recovery.
- [`06-mature-baselines-and-standards.md`](06-mature-baselines-and-standards.md) — comparison with Codex, Claude Code, Temporal, Kubernetes, MCP, OpenTelemetry, and LangGraph.
- [`07-ordivon-research-program.md`](07-ordivon-research-program.md) — prioritized experiments, repository requirements, falsifiers, and stop conditions.
- [`REFERENCES.md`](REFERENCES.md) — primary sources and mature implementation references.

## Compact map

```text
Human / participant / institution
        │ purpose, constraints, commitments
        ▼
Goal → Task graph → Ready frontier
        │ assignment
        ▼
Agent worker
= model + Harness instance + Context + Skills + Tool set + Runtime binding
        │ Tool calls / Action Proposals
        ▼
Tool / Connector / Provider
        │ execution request
        ▼
Ordivon Runtime or another execution backend
        │ Jobs / Observations / Artifacts / receipts
        ├──────────────► Harness: choose the next cognitive step
        └──────────────► Host: update durable work and completion state
```

## Main architectural decision

`ordivon-harness` is admitted as a **research boundary**, not yet as an independent repository.

The first implementation should remain a thin interface or package inside Host or Computing. Repository extraction requires all of the following:

- at least two materially different Harness backends;
- one workload that changes Harness while preserving Task identity;
- measured reduction in duplicate Host/Runtime logic;
- no loss of provider-specific capability through lowest-common-denominator abstraction;
- a stable event and checkpoint boundary that survives provider replacement;
- net benefit clearly greater than maintenance, compatibility, and cognitive cost.

Until then, Codex, Claude Agent SDK, Hermes, or a minimal native loop remain adapters behind one experimental boundary.
