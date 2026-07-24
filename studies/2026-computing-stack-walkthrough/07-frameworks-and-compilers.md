# 07 — Frameworks, Automatic Differentiation, and Compilers

## From Python to device execution

A model expression such as:

```python
y = gelu(x @ weight + bias)
```

is not primarily computed by the Python interpreter. Python invokes Tensor operations. The framework dispatches them to compiled libraries or generated device kernels.

The lowering chain is:

```text
Python
→ Tensor operations
→ automatic-differentiation graph
→ captured computation graph
→ high-level IR
→ layout and algebra optimization
→ kernel generation or library selection
→ device runtime
→ GPU execution
```

## Tensor metadata

A Tensor includes storage, shape, data type, device, strides, layout, alias relationships, and gradient metadata. A transpose may change strides without moving data; a later operation may require a contiguous copy.

## Eager and captured execution

Eager execution launches operations as Python reaches them. It supports dynamic control and direct debugging. Graph capture reveals a larger region to the compiler, enabling fusion, specialization, memory reuse, and scheduling.

Guards record assumptions such as shape, type, device, or Python state. When a guard no longer holds, the system captures or compiles another region. A graph break returns control to dynamic execution and can later enter another compiled region.

## Automatic differentiation

Reverse-mode automatic differentiation records the chain of primitive operations and propagates gradients from a scalar loss backward. It computes vector–Jacobian products without constructing full Jacobian matrices.

Forward activations needed by the backward pass consume memory. Activation checkpointing stores selected boundaries and recomputes intermediate values later.

## IR and lowering

Different IR levels preserve different meanings:

```text
matmul / softmax / reduction
→ tensor loops and tiles
→ GPU blocks, warps, and memory spaces
→ device instructions
```

Progressive lowering lets high-level passes reason about algebra while low-level passes reason about locality, vectorization, registers, and synchronization.

## Fusion

Without fusion, pointwise operations may write intermediate Tensors to HBM and read them again. A fused kernel can keep values in registers and write only the final result.

Fusion is bounded by register pressure, occupancy, incompatible schedules, shared consumers, and synchronization requirements.

## Asynchronous runtime

The host enqueues kernels and memory transfers into streams. Returning from a framework call can mean that work was submitted rather than completed. Events and synchronization make completion observable.

## Agent lesson

Natural-language execution should also be progressively lowered:

```text
goal
→ task graph
→ Effect IR
→ Tool call
→ deterministic world action
```

The intermediate representation preserves semantic intent while making execution explicit, optimizable, and recoverable.
