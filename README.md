# Ordivon Computing

**Toward a computing stack designed for probabilistic cognition, persistent execution, and human–agent collaboration.**

中文：Ordivon 的智能体原生计算体系、结构化研究、协议与验证母项目。

## What this repository is

Ordivon Computing is the system-level research, specification, and construction root for an agent-native computing stack in which foundation models participate directly in reasoning, programming, system operation, research, and coordination.

The repository is organized as a knowledge-generation system rather than a flat collection of documents:

```text
real workloads, learning, errors, and observations
                    ↓
                 Studies
                    ↓ distill
                Knowledge
                    ↓ compress
                   Core
                    ↓ generate questions
                 Research
                    ↓ construct and test
                 Projects
                    └────────→ new observations
```

## Repository map

| Area | Role | Entry point |
|---|---|---|
| **Core** | Minimal, high-generativity foundations that define the current theory | [`core/`](core/) |
| **Knowledge** | Reusable explanations, models, comparisons, and cases | [`knowledge/`](knowledge/) |
| **Studies** | Learning paths and preserved derivations | [`studies/2026-computing-stack-walkthrough/`](studies/2026-computing-stack-walkthrough/) |
| **Research** | Open questions, hypotheses, executable experiments, and immutable evidence snapshots | [`research/`](research/) |
| **Projects** | The real systems through which ideas are constructed and tested | [`projects/`](projects/) |

## Core thesis

Foundation models provide probabilistic cognition: interpretation, inference, planning, generation, comparison, and revision. A wider computing stack turns that cognition into persistent work through structured effects, durable state, world interfaces, verification, recovery, and human direction.

The current core is intentionally compact:

- [`core/foundations.md`](core/foundations.md) — the working foundations;
- [`core/stack.md`](core/stack.md) — the fourteen-layer stack and five cross-cutting planes;
- [`core/primitives.md`](core/primitives.md) — executable Kernel primitives, backend objects, and future Task-Runtime candidates with explicit boundaries.

## How the research advances

```text
observe a real workload
→ form a question
→ build the smallest useful artifact
→ run it in practice
→ treat errors and friction as information
→ revise the idea and implementation
→ preserve the result as reusable knowledge or a project branch
```

Knowledge moves toward the core only after repeated use shows that it is stable, generative, and shared across projects. The Git history preserves replaced formulations; the repository foregrounds the current best structure.

## Initial executable questions

- What is the minimum useful Agent Effect IR?
- What durable state allows a long-running task to continue across model and session boundaries?
- How should hosts, agents, and runtimes detect and adopt tool-contract changes?
- How should people and multiple Agents coordinate around persistent goals and artifacts?
- How can an Agent system learn across tasks, compile capabilities, regulate cognition, and evolve itself through evidence-governed change?

See [`research/map.yaml`](research/map.yaml) and [`research/questions/`](research/questions/).

## Active project branches

- **Ordivon Runtime** — durable trusted-local execution, Workspace, Job, Artifact, and recovery plane.
- **FinHarness** — capital-domain Agent system for truth, authority, decision, execution, and reconciliation.
- **Ordivon Web** — public interface and project navigation.

See [`projects/registry.yaml`](projects/registry.yaml).

## Executable Semantic Core

The repository contains a completed executable reference Kernel at [`research/experiments/semantic-core-v0/`](research/experiments/semantic-core-v0/) and a separate active external contract experiment at [`research/experiments/external-semantic-contract-v0/`](research/experiments/external-semantic-contract-v0/). It occupies the semantic boundary between probabilistic cognition and classical execution substrates:

```text
Probabilistic cognition
        ↓ proposes an Effect
Role-scoped Semantic Core
        ↓ admits a Dispatch
Ordivon / Linux / external systems
        ↓ produce Observation and Artifact evidence
Verification
        ↓
Fact admission
```

The Kernel preserves stable internal intent, concrete boundary attempts, explicit uncertainty, evidence provenance, signed authority, and authenticated replay. The external contract experiment separately owns backend-neutral EffectEnvelope, ToolContract, and immutable EffectBinding representations. Linux, SQLite, Git, and Ordivon continue to provide the classical execution and durability mechanisms beneath them.

Start with:

- [`KERNEL-CHARTER.md`](research/experiments/semantic-core-v0/KERNEL-CHARTER.md) — mission and hard guarantees;
- [`SPEC.md`](research/experiments/semantic-core-v0/SPEC.md) — objects, state algebra, evidence, and invariants;
- [`CONFORMANCE.md`](research/experiments/semantic-core-v0/CONFORMANCE.md) — executable and live evidence;
- [Program #1](https://github.com/zycxfyh/ordivon-computing/issues/1) — dynamic dependency clusters and Ready Frontier.

## Coordination and state

Repository documents describe stable theory, contracts, decisions, and reproducible evidence. GitHub Issues own changing task state, dependencies, discussion, and readiness; Git commits own code revision. Cross-repository experiments use immutable [`System Snapshots`](research/evidence/) to bind exact revisions and evidence digests. The repository does not maintain a second textual “current phase” or mutable deployment manifest.
