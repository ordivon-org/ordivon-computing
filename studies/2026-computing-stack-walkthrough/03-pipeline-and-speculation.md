# 03 — Pipeline, Speculation, and Out-of-Order Execution

## Pipeline

A single instruction passes through fetch, decode, execute, memory, and write-back. A pipeline overlaps different instructions across these stages.

```text
cycle 1: I1 fetch
cycle 2: I1 decode | I2 fetch
cycle 3: I1 execute | I2 decode | I3 fetch
```

Pipelining improves throughput rather than the latency of one instruction. Registers between stages preserve intermediate state.

## Hazards

A later instruction may depend on an earlier result. A true read-after-write dependency cannot be removed:

```text
I1: x1 = x2 + x3
I2: x4 = x1 + x5
```

Forwarding sends a newly produced result directly to a consumer before normal write-back. Some cases, such as an immediately consumed load result, still require a stall.

Control hazards occur because the processor does not yet know which path follows a branch. Structural hazards occur when operations compete for the same hardware resource.

## Branch prediction and speculation

The processor predicts the likely branch direction and begins executing that future. When the prediction is correct, work is saved. When it is wrong, speculative work is discarded and execution restarts from the correct path.

This establishes a fundamental distinction:

```text
operation executed
≠ result committed to architectural state
```

## Out-of-order execution

Modern CPUs inspect a window of decoded instructions and issue operations whose true operands are ready, even when earlier instructions are still waiting.

Key structures include:

- register renaming, which creates fresh physical versions and removes false name conflicts;
- reservation stations or issue queues, which wait for operands and execution units;
- load/store queues, which reason about memory dependencies;
- a reorder buffer, which records program order and retires results in order.

The visible machine behaves as if instructions completed in program order, while the physical machine exploits available parallelism underneath.

## Precise exceptions

If an instruction faults, the architectural state should correspond to a clear sequential boundary. In-order retirement allows completed later work to remain speculative until all earlier instructions are known to be valid.

## Agent correspondence

| CPU structure | Agent analogue |
|---|---|
| instruction | Task or Effect |
| operand dependency | precondition |
| execution unit | Tool or worker |
| issue queue | ready-task queue |
| speculation | candidate plan or Attempt |
| physical register version | versioned Workspace state |
| reorder buffer | ordered task/fact record |
| retirement | verified commit |
| branch recovery | replanning from observation |

The analogy has limits: Agent effects are long-lived, open-world, and sometimes irreversible. That makes explicit preparation, observation, verification, and recovery even more important.

## Anchor

High performance comes from executing independent work early while preserving a coherent committed state.
