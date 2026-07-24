# 10 — Training and Post-Training

## Data pipeline

Raw web pages, books, code, papers, conversations, and synthetic examples require parsing, normalization, classification, deduplication, quality scoring, mixture design, tokenization, and sequence packing.

The data mixture acts as an implicit curriculum: it determines which structures and domains repeatedly shape the parameters.

## Scaling

Empirical scaling laws show that loss often improves predictably as model parameters, training Tokens, and compute increase across broad ranges. Compute-efficient training balances model size with enough high-quality data rather than maximizing one dimension alone.

## Pretraining

Causal pretraining minimizes next-Token loss over large sequences. It produces a Base Model able to continue many distributions of language, code, reasoning, and knowledge.

Training is also a systems process involving mixed precision, distributed communication, gradient clipping, learning-rate schedules, checkpoints, fault recovery, and continuous monitoring.

## Long-context adaptation

Long-context capability combines positional representation, longer training examples, long-range tasks, attention algorithms, KV management, and evaluation. It is a learned behaviour supported by the runtime.

## Supervised fine-tuning

SFT trains on instruction–response demonstrations. It organizes broad Base-Model capacity into stable interaction patterns, formats, task strategies, and Tool-call syntax.

## Preference optimization

Preference data compares candidate responses for the same Prompt. RLHF commonly learns a reward signal and optimizes the model against it. Direct preference methods optimize the relative probability of preferred and rejected responses more directly.

## Reinforcement learning and reasoning

Tasks with verifiable outcomes—mathematics, code, games, tool environments—can supply result rewards. The model can discover longer search, checking, correction, and strategy-switching behaviour beyond direct imitation.

Outcome rewards evaluate the final state. Process rewards provide denser feedback on intermediate steps. Both shape what kinds of trajectories the model learns.

## Inference-time scaling

After training, a system can allocate more computation to a difficult request through longer reasoning, multiple candidates, search, external verification, or Tool execution.

```text
task capability
= model weights
+ context
+ inference-time compute
+ tools
+ feedback
```

## Agent training

Agent trajectories contain:

```text
Goal
→ Observation
→ Tool Call
→ Tool Result
→ updated state
→ verification
→ final outcome
```

Success, failure, and recovery all carry learning value. Ordivon-like runtimes can preserve these real trajectories as future research and training artifacts.
