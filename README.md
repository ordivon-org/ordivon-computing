# Agent-Native Computing

**Toward a computing stack designed for probabilistic models as primary cognitive and software-producing units.**

中文：面向智能体原生计算栈的第一性原理研究。

## What we are building

Agent-Native Computing studies and constructs a computing stack for a world in which foundation models participate directly in reasoning, programming, system operation, research, and coordination.

The project connects ideas across model architecture, memory, language, compilers, execution kernels, tools, hardware, verification, and human–agent organization. Its shared research map gives independent projects a common foundation while allowing each result to grow into its own implementation, experiment, benchmark, or product.

## Current starting point

- Transformer-family models, including dense, MoE, multimodal, and hybrid systems, form the current operational starting point.
- The research map evolves with new architectures, papers, experiments, and observed workloads.
- Models provide probabilistic cognition: interpretation, inference, planning, generation, and revision.
- The surrounding stack provides durable state, executable effects, coordination, verification, and recovery.

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
10. organization, economics, and coordination.

The working stack is defined in [`stack.md`](stack.md). Working foundations are in [`axioms.md`](axioms.md). Machine-readable questions and projects live in [`research-map.yaml`](research-map.yaml) and [`project-registry.yaml`](project-registry.yaml).

## How the research advances

```text
observe a real workload
→ form a question
→ build the smallest useful artifact
→ run it in practice
→ treat errors and friction as information
→ revise the idea and implementation
→ preserve the result as a reusable branch or project
```

Papers expand the possibility space. Working systems reveal hidden constraints. Dogfood turns mistakes into precise research questions. Each cycle updates both the theory and the implementation.

## Initial executable questions

- What is the minimum useful Agent Effect IR?
- What durable state allows a long-running task to continue across model and session boundaries?
- How should hosts, agents, and runtimes detect and negotiate tool-contract changes?

## Existing branches and fruits

- **Ordivon** — an execution microkernel connecting probabilistic cognition to persistent, recoverable system action.
- **FinHarness** — a capital-governance system exploring truth, authority, decision, execution, and reconciliation with agents in the loop.
- **Ordinary Prosperity Research** — a long-horizon empirical research project exploring reproducible agent-assisted inquiry.

## Current phase

**P0 establishes the common foundation:** working principles, a layered computing-stack map, initial research questions, and relationships among active projects.

The next cycles will add current literature, executable experiments, prototypes, benchmarks, and multi-agent maintenance through the same build–observe–revise process.
