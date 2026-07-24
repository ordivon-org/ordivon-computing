# 2026 Computing-Stack Walkthrough

This study preserves the learning path through which the repository’s current stack, primitives, and research questions were derived.

It is intentionally more explanatory than the core. The chapters keep examples, analogies, historical transitions, and cross-layer connections that are useful for learning but too detailed for the minimal theory.

## Route

```text
physical reality
→ digital state
→ CPU and memory
→ parallel and distributed machines
→ model frameworks and compilers
→ Transformer learning and serving
→ Agent language and execution
→ world interfaces
→ products and institutions
```

## Chapters

1. [Physical reality](00-physical-reality.md)
2. [Transistors and memory](01-transistors-and-memory.md)
3. [CPU and ISA](02-cpu-and-isa.md)
4. [Pipeline, speculation, and out-of-order execution](03-pipeline-and-speculation.md)
5. [Cache and virtual memory](04-cache-and-virtual-memory.md)
6. [Multicore, GPU, and matrix computation](05-multicore-and-gpu.md)
7. [Distributed AI computing](06-distributed-ai-computing.md)
8. [Frameworks, automatic differentiation, and compilers](07-frameworks-and-compilers.md)
9. [How a Transformer learns and generates](08-transformer-learning.md)
10. [Modern Transformer architecture](09-modern-model-architecture.md)
11. [Training and post-training](10-training-and-post-training.md)
12. [Inference runtime](11-inference-runtime.md)
13. [Agent language and Effect IR](12-agent-language.md)
14. [Agent execution kernel](13-agent-kernel.md)
15. [World interfaces and Tool contracts](14-world-interfaces.md)
16. [Products, collaboration, and institutions](15-products-and-institutions.md)

## Reading principle

The sequence is a spiral rather than a strict prerequisite graph. Later layers reveal why earlier mechanisms matter; earlier layers constrain what later abstractions can actually do.

The condensed current theory is in [`../../core/`](../../core/). Reusable cross-topic models are in [`../../knowledge/`](../../knowledge/).
