# Agent-Native Computing

**Toward a computing stack designed for probabilistic models as primary cognitive and software-producing units.**

中文：面向智能体原生计算栈的第一性原理研究。

## Core question

Most of today's computing stack was shaped around humans writing deterministic programs. If probabilistic foundation models become primary planners, programmers, and system operators, which abstractions remain valid, which require new contracts, and which should be rebuilt?

This repository is the **research root**, not a monolithic implementation. It maintains the smallest shared map of assumptions, layers, open questions, evidence, and independently executable projects.

## Current baseline

- The current mainstream frontier-model baseline remains the Transformer family, including dense, MoE, multimodal, and hybrid variants.
- This is a contingent engineering baseline, not a permanent architectural commitment.
- A model is treated as a probabilistic cognitive component, not as the sole owner of truth, authority, durable state, or real-world side effects.

## Research structure

The research tree currently covers:

1. model and cognitive computation;
2. agent languages and intermediate representations;
3. agent compilers;
4. execution kernels;
5. memory and state;
6. tools, capabilities, and effects;
7. multi-agent systems;
8. hardware, ISA, and dataflow;
9. verification and benchmarks;
10. organization, economics, and governance.

The working stack is defined in [`stack.md`](stack.md). Stable research principles are in [`axioms.md`](axioms.md). Machine-readable questions and projects live in [`research-map.yaml`](research-map.yaml) and [`project-registry.yaml`](project-registry.yaml).

## Initial executable questions

- What is the minimum useful Agent Effect IR?
- What durable state is required to recover a long-running task after model context loss?
- How should hosts, agents, and runtimes detect and negotiate tool-contract drift?

## Existing branches and fruits

- **Ordivon** — an execution microkernel connecting probabilistic agents to deterministic, persistent, recoverable system effects.
- **FinHarness** — a capital-governance testbed for truth, authority, decision, execution, and reconciliation under agent participation.
- **Ordinary Prosperity Research** — an empirical research testbed for reproducible, long-horizon agent-assisted inquiry.

## Status

**P0 — foundation skeleton.**

The repository currently defines the shared research surface only. Literature synthesis, experiments, prototypes, and autonomous maintenance loops will be added as independently verifiable work.
