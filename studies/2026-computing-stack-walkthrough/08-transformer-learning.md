# 08 — How a Transformer Learns and Generates

## Neural network as a parameterized function

A model is a function `fθ(x)` controlled by parameters `θ`. Training searches for parameters that reduce a loss measuring the difference between model predictions and training targets.

```text
forward prediction
→ loss
→ gradient
→ optimizer update
→ new parameters
```

The gradient describes how a small parameter change affects the loss. Reverse-mode automatic differentiation applies the chain rule through the entire computation graph.

## Tokens and embeddings

A tokenizer converts text or code into discrete Token IDs. An embedding matrix maps each ID to a learned continuous vector. Position information is added or incorporated so that the model can distinguish order and distance.

The same Token receives different higher-layer representations in different contexts because attention mixes information from surrounding positions.

## Transformer block

A decoder-only Transformer repeatedly applies:

```text
normalization
→ causal self-attention
→ residual addition
→ normalization
→ MLP
→ residual addition
```

Residual connections let each layer add an update to an existing representation. Normalization controls numerical scale.

## Query, key, and value

Each position projects its representation into Query, Key, and Value vectors.

```text
Query: what information is relevant here?
Key: under what features can this position be matched?
Value: what information should be contributed if selected?
```

Scaled dot products between Queries and Keys become attention scores. A causal mask removes future positions. Softmax converts scores into weights used to combine Values.

Multiple heads provide several learned routing subspaces.

## MLP

Attention moves information between Token positions. The MLP applies nonlinear feature transformation independently at each position. Gated variants allow one branch to control another.

## Output and loss

The final hidden state is projected into one logit per vocabulary Token. Softmax defines a next-Token distribution. Cross-entropy increases the probability of the training sequence’s actual next Token.

Teacher forcing allows every position in a known training sequence to predict its next Token in parallel.

## Autoregressive inference

During generation, the future is unknown:

```text
context
→ generate one Token
→ append it
→ generate the next Token
```

KV cache stores historical attention Keys and Values so that earlier layers do not need to recompute them from scratch.

## Parameters, context, and tools

Parameters encode learned statistical structure across training. Context carries current working information. KV cache carries sequence-computation state. External memory preserves durable facts. Tools observe and change the current world.

A complete Agent combines all of them rather than expecting model parameters to serve as a real-time database or execution system.
