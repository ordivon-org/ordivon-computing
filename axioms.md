# Research Axioms

These are working axioms: compact decision rules grounded in current systems and open to revision when evidence changes.

## A0 — Current model reality is a baseline, not a destiny

The current mainstream foundation-model stack is Transformer-family dominated. Research may assume this operationally without assuming it is the final cognitive architecture.

## A1 — The model is not the system of record

A model may infer, plan, generate, and revise. It must not be the sole owner of durable truth, authority, committed side effects, or completion facts.

## A2 — Natural language expresses intent, not sufficient execution contracts

Open goals may begin in natural language. Real effects require explicit identities, capabilities, preconditions, effect semantics, and commit conditions.

## A3 — Context is not durable memory

Model parameters, KV cache, conversation context, working memory, task state, long-term knowledge, and world state are different classes of state and must not be collapsed into one prompt.

## A4 — Effects are first-class

An external action should be representable by its target, authority, preconditions, idempotency, reversibility, result contract, and completion evidence—not merely by a tool name and JSON arguments.

## A5 — Failure and recovery are normal execution states

Long-running agent work must assume interruption, stale state, partial progress, retries, cancellation, compensation, and resumption. Recovery is part of the primary design, not an operational afterthought.

## A6 — Own irreducible semantics; reuse mature mechanisms

A project should implement the semantics that existing layers cannot reliably express. Mature infrastructure should be reused when it does not constrain those semantics.

## A7 — Stable core, replaceable edge

Identity, state transition, authority, effect, and recovery contracts should be strict. Models, providers, transports, interfaces, and experimental policies should remain replaceable.

## A8 — Evidence outranks architectural narrative

Claims should be distinguished as fact, inference, hypothesis, or preference. Running systems, failure traces, reproducible experiments, and benchmarks are required to promote important hypotheses.

## A9 — Code generation is cheap; world-state correctness remains expensive

Agent capability reduces the cost of producing code. It does not eliminate the cost of choosing goals, preserving truth, validating outcomes, resolving conflicting objectives, or maintaining stable interfaces.
