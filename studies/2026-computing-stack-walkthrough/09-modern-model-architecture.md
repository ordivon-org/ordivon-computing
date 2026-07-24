# 09 — Modern Transformer Architecture

Modern foundation models retain the Transformer family’s central loop while reorganizing normalization, position, attention state, MLPs, and parameter routing.

## Decoder-only and Pre-Norm

General autoregressive models often use a stack of causal decoder blocks. Pre-Norm applies normalization before the attention or MLP sublayer and adds the result back to the residual stream:

```text
x + Attention(Norm(x))
x' + MLP(Norm(x'))
```

This preserves a direct residual path through deep networks.

## RMSNorm

RMSNorm scales a vector by its root-mean-square magnitude rather than explicitly centring it by the mean. It provides a compact way to control activation scale.

## RoPE and context position

Rotary position embeddings rotate Query and Key components according to position. Their dot product then naturally contains relative-position information.

Long-context capability also depends on long-sequence training, attention design, numerical adaptation, data, and KV-runtime support. A larger configured position range alone does not create reliable long-range use.

## MHA, MQA, GQA, and latent KV compression

Full multi-head attention stores separate Key and Value heads for every Query head. Multi-query attention shares one KV set. Grouped-query attention shares KV across groups of Query heads.

Reducing KV heads lowers cache capacity and decode bandwidth. Latent attention methods compress KV information into smaller hidden state and reconstruct the required representations during attention.

## Local and global attention

Not every layer needs complete history access. Sliding-window attention limits most communication to nearby Tokens. Periodic global layers can integrate long-range information. This exchanges unrestricted communication for controlled state and compute cost.

## SwiGLU and gated MLPs

A gated MLP produces a content branch and a gate branch, applies a nonlinear function to the gate, multiplies them, and projects back to the residual dimension. This adds learned feature selection to the feed-forward block.

## Mixture of experts

MoE layers contain many expert MLPs while routing each Token to a small subset. Total parameter capacity can grow faster than per-Token compute.

The system must manage expert placement, all-to-all communication, router quality, and load balance. Sparse model architecture is therefore simultaneously a learning problem and a distributed-systems problem.

## Architectural direction

The main changes optimize:

```text
training stability
position and context
KV state
parameter activation
communication
hardware locality
```

The enduring Transformer core remains dynamic information routing through attention plus nonlinear feature transformation through MLP or expert layers.
