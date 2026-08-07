# Parallelism and Data Movement

## Parallelism begins with dependency

Two operations can execute independently when neither requires the other’s result and they do not conflict on shared state. The fundamental question is therefore not “how many workers exist?” but:

```text
what is truly independent,
and what communication is necessary?
```

CPU pipelines, out-of-order execution, SIMD, GPUs, and distributed training all exploit different kinds of independence.

## CPU: parallel work behind sequential semantics

A modern CPU fetches, predicts, decodes, renames, schedules, executes, and retires instructions through overlapping structures. Register renaming removes false name dependencies. Reservation stations wait for real operands. A reorder buffer allows execution to complete out of order while architectural state commits in order.

The key separation is:

```text
execution completed
≠
architectural state committed
```

This pattern later reappears in Agent systems as proposal, attempt, verification, and commit.

## GPU: regular parallelism and latency hiding

GPUs use large numbers of threads grouped into blocks and warps. They are effective when operations are regular, control flow is similar, and memory accesses are coalesced. Matrix multiplication fits because many output elements can be computed in parallel and reused through tiling, registers, shared memory, and tensor instructions.

GPU performance is shaped by both arithmetic and movement:

```text
useful operations
per byte moved
```

FlashAttention is an important example: its advantage comes from reorganizing the algorithm to reduce traffic between high-bandwidth memory and on-chip memory, not from changing the mathematical definition of attention.

## Distributed systems: communication becomes visible

Multi-GPU execution introduces collective operations such as all-reduce, all-gather, reduce-scatter, broadcast, and all-to-all. Data, tensor, pipeline, expert, and sequence parallelism partition different dimensions of work.

A training step can be approximated as:

```text
compute
+ exposed communication
+ pipeline bubbles
+ load imbalance
+ runtime overhead
```

As more devices are added, the remaining serial work, communication, and slowest participant limit strong scaling.

## Three forms of Agent parallelism

Agent systems can exploit:

1. **Numerical parallelism** — model and data computation on accelerators;
2. **Request parallelism** — many independent inference requests;
3. **Task parallelism** — independent research, coding, testing, and observation tasks.

Task parallelism benefits from versioned workspaces, explicit dependencies, artifact-based joins, and state affinity. Adding more Agents without a decomposable task graph increases coordination cost rather than useful work.

## Design consequence

Parallelism is a property of the dependency graph. Scheduling should expose true independence, place work near its state, and keep synchronization proportional to actual shared facts.
