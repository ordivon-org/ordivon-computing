# 11 — Inference Runtime

A model checkpoint becomes a real-time service only through a runtime that manages requests, memory, devices, scheduling, sampling, and state.

## Request lifecycle

```text
admission
→ tokenization
→ model routing
→ prefix-cache lookup
→ KV allocation
→ prefill
→ decode scheduling
→ sampling
→ streaming
→ state release or persistence
```

## Prefill and decode

Prefill processes the entire input sequence with large parallel matrix operations and creates KV state. Decode generates one new Token per active sequence and repeatedly reads model weights and historical KV state.

This creates different objectives:

- first-Token latency depends heavily on queueing and prefill;
- output cadence depends on decode scheduling and memory bandwidth;
- throughput depends on batching and device utilization;
- goodput counts work completed within service-level latency targets.

## Continuous batching

Generated sequences have different lengths. Iteration-level scheduling removes completed requests and admits new ones after each decode step.

```text
round 1: A B C D
round 2: B C D E
round 3: B D E F G
```

The scheduling unit becomes a Token iteration rather than an entire request.

## KV memory

KV cache grows with layers, context length, concurrency, KV heads, head size, and data precision. It often determines serving capacity.

Paged KV systems divide logical sequence state into fixed-size blocks mapped to non-contiguous physical memory. This reduces fragmentation, supports sharing, and enables copy-on-write for decoding branches.

## Prefix reuse

Requests often share system Prompts, Tool definitions, documents, or conversation history. Prefix caches reuse the corresponding KV blocks and compute only the new suffix. State affinity therefore influences which worker should receive a request.

## Long-Prompt scheduling

A very long prefill can delay active decode requests. Chunked prefill divides it into smaller scheduling units that can share batches with decode work. Prefill and decode can also run on separate worker pools, exchanging KV state.

## Speculative decoding

A fast Draft path proposes several Tokens. The Target Model verifies them in parallel and accepts the valid prefix. This converts cheap prediction plus authoritative verification into fewer expensive sequential steps.

## Quantization and structured decoding

Lower-bit weights, activations, or KV state reduce storage and bandwidth when kernels and hardware support the format efficiently. Structured decoding masks invalid next Tokens according to a grammar or Schema, combining model semantic choice with machine syntax.

## Inference engine as operating system

| Operating-system idea | Inference-runtime analogue |
|---|---|
| process | request or sequence |
| scheduler | continuous batcher |
| physical memory | HBM |
| virtual page | logical KV block |
| page table | block table |
| shared page | prefix cache |
| time slice | decode step or prefill chunk |
| exit | EOS, cancellation, or stop condition |

The inference runtime manages the Token world. The Agent runtime above it manages the external world.
