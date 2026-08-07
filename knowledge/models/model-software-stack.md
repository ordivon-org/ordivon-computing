# Model Software Stack

A high-level model expression becomes hardware execution through progressive lowering:

```text
Python model code
→ Tensor operations
→ automatic differentiation
→ captured graph
→ intermediate representations
→ graph and layout optimization
→ kernel selection or generation
→ device runtime
→ GPU instructions
```

## Tensor as the central object

A Tensor combines data with interpretation:

```text
storage + shape + dtype + strides + layout + device + gradient metadata
```

Views can change shape or strides without copying storage. Layout and contiguity strongly influence whether operations can use vectorized loads, fused kernels, or optimized libraries.

## Eager execution and graph execution

Eager frameworks execute operations as Python reaches them. This provides direct control and dynamic behaviour. Graph capture gives the compiler visibility across operations, enabling fusion, memory reuse, layout propagation, specialization, and global scheduling.

Dynamic programs often form mixed execution:

```text
compiled region
→ dynamic graph break
→ Python or runtime decision
→ new compiled region
```

## Automatic differentiation

Reverse-mode automatic differentiation records enough forward structure to propagate vector–Jacobian products from a scalar loss back to many parameters. It avoids materializing full Jacobians and turns a composed forward program into a generated backward program.

Saved activations consume substantial memory. Activation checkpointing stores selected boundaries and recomputes intermediate activations during backward execution, exchanging compute for memory.

## Intermediate representations

One IR cannot effectively express every abstraction level. Model compilers commonly lower through several representations:

```text
semantic graph operations
→ Tensor algebra and reductions
→ loops, tiles, and layouts
→ GPU blocks, warps, and memory spaces
→ low-level device code
```

High-level IR preserves meanings such as matrix multiplication or reduction. Lower-level IR exposes scheduling, vectorization, shared memory, registers, and instruction selection.

## Fusion and scheduling

For:

```text
y = gelu(x @ W + b)
```

a compiler may call an optimized GEMM implementation, fuse bias and activation into an epilogue, reuse buffers, and enqueue operations on an asynchronous device stream.

Fusion reduces intermediate memory traffic and launch overhead, while excessive fusion may increase register pressure or combine operations with incompatible schedules. Optimization is a locality and resource-allocation problem rather than a universal preference for larger kernels.

## Runtime semantics

Device work is usually asynchronous:

```text
host submitted work
≠ device started work
≠ device completed work
≠ host observed result
```

Streams order work, events express dependencies, and synchronization occurs when the host or another stream requires completed data.

## Agent analogy

A useful Agent lowering chain is structurally similar:

```text
natural-language goal
→ semantic task graph
→ effect graph
→ tool-specific calls
→ deterministic execution
→ observations and artifacts
→ persistent state update
```

Freedom of expression remains at the top; explicit IR connects it to deterministic execution below.
