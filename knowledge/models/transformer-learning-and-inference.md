# Transformer Learning and Inference

## Foundation-model computation

A Transformer maps a Token sequence into contextual representations and next-Token logits. A decoder block repeatedly combines:

```text
normalization
→ causal attention
→ residual update
→ normalization
→ gated MLP or sparse experts
→ residual update
```

Attention dynamically routes information across sequence positions. The MLP transforms the representation at each position. Residual streams allow many layers to contribute incremental updates.

## Training

Training minimizes next-Token prediction loss:

```text
text
→ Token sequences
→ forward pass
→ cross-entropy loss
→ reverse-mode gradients
→ distributed optimizer update
→ new model version
```

Pretraining creates broad statistical and representational capacity. Supervised fine-tuning organizes that capacity into instruction-following behaviour. Preference optimization changes relative response tendencies. Reinforcement learning on verifiable outcomes can develop longer search, correction, and reasoning strategies.

Model capability depends jointly on architecture, data quality and mixture, parameter count, training Tokens, optimization, post-training, and inference-time compute.

## Modern architectural evolution

The current Transformer family includes combinations such as:

- Pre-Norm and RMSNorm for stable deep residual computation;
- RoPE and long-context adaptation for positional structure;
- MQA, GQA, or latent KV compression for inference-state efficiency;
- SwiGLU and related gated MLPs;
- mixture-of-experts routing for high total parameter capacity with sparse per-Token activation;
- local–global attention mixtures for scalable context communication.

These changes mainly reorganize state, routing, numerical stability, and hardware cost while preserving the core loop of contextual routing and nonlinear representation updates.

## Inference runtime

A model service divides requests into:

- **Prefill** — parallel processing of the input Prompt and creation of KV state;
- **Decode** — sequential generation of new Tokens while reusing historical KV state.

The runtime manages continuous batching, KV allocation, prefix reuse, quantization, model parallelism, scheduling, sampling, cancellation, and streaming.

Paged KV management provides logical continuity over physically non-contiguous blocks. Prefix caches reuse shared Prompt state. Chunked prefill prevents long Prompts from monopolizing scheduling. Speculative decoding uses a cheaper proposal path and a higher-authority verification path to advance multiple Tokens per expensive model step.

## From model to Agent

A model request performs a Token-level state transition. An Agent task performs a world-level state transition:

```text
model:
context → next-token distribution

Agent:
world state → observation → cognition → effect → new world state
```

The model is the probabilistic cognitive component. Task state, tools, execution, artifacts, and recovery belong to the surrounding runtime.

See [Transformer learning](../../studies/2026-computing-stack-walkthrough/08-transformer-learning.md), [modern model architecture](../../studies/2026-computing-stack-walkthrough/09-modern-model-architecture.md), [training and post-training](../../studies/2026-computing-stack-walkthrough/10-training-and-post-training.md), and [inference runtime](../../studies/2026-computing-stack-walkthrough/11-inference-runtime.md).
