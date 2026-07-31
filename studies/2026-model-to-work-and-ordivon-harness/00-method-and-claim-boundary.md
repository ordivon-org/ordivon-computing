# Method and Claim Boundary

## 1. Research question

The study asks:

> Starting from a model that maps an input context to generated tokens or structured output, which additional logical responsibilities are necessary before a real Task can be acted on, recovered, verified, and completed?

It then asks a narrower architecture question:

> Which of those responsibilities should Ordivon own, which should remain in mature Provider Harnesses, and which should remain in classical execution systems?

## 2. Method

The study combines four evidence classes.

### E1 — first-principles necessity

A responsibility is logically necessary when removing it leaves an unanswered transition, such as:

- who executes a Tool Call;
- who remembers that a Task remains open after a model process ends;
- who determines whether a response-lost action already happened;
- who verifies that a claimed result satisfies acceptance;
- who prevents a replaced worker from committing stale completion.

First-principles necessity identifies that a responsibility exists. It does not determine which repository or product must own it.

### E2 — mature-system comparison

Official architecture material from OpenAI, Anthropic, Microsoft, and Google is used to test whether a responsibility is already implemented and where mature systems place it.

Industry architecture is treated as a baseline, not an authority. Product packaging often combines Surface, interaction Host, Harness, Session, Tool execution, sandbox, memory, and observability under one name.

### E3 — Ordivon executable evidence

The decisive Ordivon evidence comes from:

- `task-continuation-v0`;
- `core-work-system-v1`;
- Host Harness H1–H5;
- Runtime request identity and foreign-reference recovery;
- immutable receipts and tamper tests.

These experiments are used to retain or delete proposed Ordivon responsibilities.

### E4 — negative evidence

Absence of a demonstrated benefit is not proof that a mechanism is universally useless. It is sufficient to refuse permanent architecture when the proposed mechanism would add continuing cost.

The default decision rule is:

```text
No reproduced failure
+ no second consumer
+ no measured net deletion
= no shared layer or repository
```

## 3. Terminology

### Model

A learned conditional generator. It consumes an encoded context and produces tokens, structured output, Tool requests, or another representation. It does not by itself execute the requested action or retain authoritative long-term Task state.

### Model call

One bounded inference request and response. Streaming does not change the logical unit.

### Ordivon Harness

Ordivon's first-party Agent execution layer for bare model APIs or local inference. It owns one Run's model loop, Tool interpretation, Run-local context, budgets, interruption, and evidence emission.

### External Provider Harness

A mature Agent implementation such as Codex App Server, Hermes ACP, or Claude Code/Agent SDK. It retains its own Session and lifecycle semantics.

### Harness Run

One bounded cognitive and Tool-use episode under one Assignment. A Run may stop because work completed, input is needed, budget ended, the Provider failed, or the Harness was interrupted. Run termination is not Task completion.

### Host

The authority for durable Goal and Task meaning, Task Attempt, Assignment generation, compiled semantic Context, acceptance, replacement, recovery, completion admission, and TaskOutcome.

### Runtime

The authority for Workspace, Job, Runtime Attempt, process tree, output, cancellation, Artifacts, physical execution disposition, and request reconciliation.

### Workload Contract

The Task-specific objective, source binding, allowed operations, required Artifacts, acceptance criteria, budget, and Effect boundaries. It defines what must be achieved but does not run the model loop.

### Verifier

A deterministic test, rule, model evaluator, simulator, or human review that produces evidence about acceptance. The verifier does not own the final Host transition.

## 4. Claims classified by confidence

### Strongly supported within tested boundaries

- a model call alone is not an Agent Run;
- Provider Session identity is not durable Task identity;
- a successful physical process is not semantic Task completion;
- Provider final text is not a portable completion contract;
- explicit Host state and Artifacts can carry a bounded Task across Codex/Hermes replacement;
- Assignment generation prevents a real stale-worker completion failure;
- Runtime request identity and opaque references can recover a response-lost Job without Runtime understanding Host semantics;
- Codex and Hermes lifecycle normalization would discard or invent material events in the observed versions.

### Supported as an architecture decision

- Ordivon should own a thin Harness for bare model APIs;
- mature Provider Harnesses should remain direct, provider-faithful backends;
- the common boundary should be Assignment input and Run evidence output, not an internal universal lifecycle;
- Ordivon Harness v0 should begin inside Host and earn repository extraction later.

### Open

- the minimum useful Tool vocabulary for Ordivon Harness;
- whether persistent Harness-local Sessions materially improve cost or behavior;
- when compaction becomes necessary;
- whether parallel Tool Calls or subagents provide net benefit;
- whether a second independent consumer justifies a standalone repository;
- how the retained boundary performs under adversarial or multi-Agent workloads.

## 5. Closure criteria

A research topic is closed when:

1. ownership is explicit;
2. at least one real trajectory crosses the boundary;
3. a competing mature baseline is admitted where available;
4. at least one failure or deletion test changes the decision;
5. unsupported generalizations and validity limits are recorded;
6. the next action is implementation or a narrower empirical question.

The model-to-work stack and cross-Provider Harness boundary meet these criteria. Ordivon Harness v0 now moves to construction.
