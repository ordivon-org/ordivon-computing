# 05 — Multicore, GPU, and Matrix Computation

## Multicore CPUs

A multicore processor runs several instruction streams simultaneously. Shared memory makes communication easy, but it introduces races, coherence traffic, synchronization, and load-balancing problems.

Concurrency is correct when shared-state relationships are explicit. Performance improves when independent work remains independent in both the program and physical memory layout.

## SIMD and SIMT

SIMD applies one instruction to several data lanes. GPUs expose a related SIMT model: many logical threads execute in groups on shared hardware.

CUDA-like execution organizes work as:

```text
grid
└── blocks
    └── threads
```

Hardware groups nearby threads into warps. Threads in a warp execute together; divergent branches serialize different paths.

## Latency hiding

A GPU keeps many warps resident. When one warp waits for memory, another can issue instructions. This exchanges sophisticated single-thread latency optimization for large-scale throughput scheduling.

The memory hierarchy includes:

```text
per-thread registers
→ shared on-chip memory and caches
→ device-wide cache
→ HBM
```

Coalesced accesses combine neighbouring thread requests into efficient memory transactions.

## Matrix multiplication

For `C = A × B`, each output element is an independent reduction over one row and one column. A tiled implementation loads submatrices into faster memory, reuses them for many multiply–accumulate operations, and writes completed output tiles.

Tensor cores or matrix units accelerate small matrix multiply–accumulate patterns. Systolic designs move data through arrays of arithmetic units to maximize reuse.

## Transformer mapping

A Transformer uses large matrix operations for:

- Q, K, and V projections;
- attention score computation;
- attention output projection;
- gated MLP layers;
- vocabulary projection.

Attention also contains reductions, masking, softmax, and state movement. Efficient implementations reorganize these operations around the physical memory hierarchy.

## Training, prefill, and decode

- **Training** combines large forward and backward graphs and substantial activation memory.
- **Prefill** processes many Prompt positions in parallel and creates KV state.
- **Decode** generates one new Token per sequence and repeatedly reads weights and historical KV state.

The same model therefore creates different hardware workloads depending on its phase.

## Agent parallelism

GPU parallelism batches homogeneous numerical work. Agent task parallelism is more heterogeneous. A Runtime should batch similar Effects when useful, but retain semantic identities and dependency boundaries for long-running external actions.

## Anchor

GPUs succeed by organizing regular computation and data reuse at massive scale. Agent systems should similarly expose the shape and locality of work rather than treating every action as an opaque message.
