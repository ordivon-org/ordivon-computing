# ANC-HARNESS-001 — Harness, Host, Runtime, and Agent-System Composition

## Question

Can a thin, capability-preserving Harness boundary allow Ordivon Host Tasks to run and continue across materially different Agent Harnesses while keeping durable work in Host, physical execution in Runtime, and provider-specific cognition features intact?

## Why this is unresolved

Codex, Claude Code, and other Agent products vertically integrate Surface, interaction Host, Harness, Session, Tools, sandbox, and execution adapters. Ordivon has separately proven durable Host and Runtime responsibilities, but has not yet demonstrated that an explicit shared Harness interface produces more value than direct provider adapters.

The conceptual boundary is useful. A new repository or protocol is not yet justified.

## Ownership hypothesis

```text
Ordivon Host
  Goal / Task / Task Graph / Ready Frontier
  Assignment / Task Attempt / lease / budget
  DecisionRequest / Completion commit / recovery

Harness
  Session / Context / working memory
  Model loop / Skills / Tool exposure
  local plan / local subagents / compaction

Ordivon Runtime
  Workspace / Job / process / Artifact
  physical observation / cancellation / recovery

Domain World
  authoritative domain state, transition, and outcome
```

Harness may propose Task decomposition and completion. Host alone commits durable Task state. Runtime Job success alone does not prove Task or Goal completion.

## Strong baselines

1. direct Codex App Server integration;
2. direct Claude Agent SDK or CLI hosting;
3. current provider-specific Ordivon Host adapters;
4. one-shot model invocation with Host continuation capsule;
5. minimal native Agent loop;
6. a shared thin Harness adapter interface.

The shared interface must compete against direct integration on correctness, capability retention, latency, code size, and maintenance.

## Research objects

### Harness capability manifest

```text
resume
fork
retained reasoning
compaction
subagents
native Tools
structured output
remote execution
Session persistence
```

### Harness lifecycle

```text
start Assignment
compile Context
invoke Model
request Tool
observe result
emit progress / proposal / interrupt
checkpoint
finish or replace
```

### Completion Proposal

Harness submits evidence-bound completion for Host validation. It does not directly change Task status.

### Cross-layer event identity

Goal, Task, Assignment, Task Attempt, Harness Run, Tool Call, Effect, Dispatch, Runtime Job, Runtime Attempt, Artifact, and Trace identities remain linkable without requiring one universal internal object model.

## First experiment

Run one real Ordivon Task under two materially different Harness backends.

Required trajectory:

```text
Host creates one Task and Assignment
→ Harness A performs useful work and checkpoints
→ Harness A Session/process is terminated
→ Host retains authoritative Task and execution evidence
→ Harness B receives a new Assignment generation
→ Harness B recompiles Context and continues
→ CompletionProposal is validated by Host
```

At least one Tool request must execute through Ordivon Runtime. At least one outcome must require evidence beyond process exit.

## Controlled variants

1. direct provider integration;
2. thin Harness adapter;
3. fresh prompt from full transcript;
4. Host-derived continuation capsule;
5. provider-native retained Session where available;
6. replacement after deliberate Context or Tool revision drift.

## Failure injection

- Harness process loss;
- provider Session loss;
- rolling truncation or compaction;
- stale Assignment completion;
- response loss after Runtime Job admission;
- missing required Artifact;
- Tool Contract drift;
- conflicting Task decomposition proposals;
- Hook timeout or conflicting gate;
- stale worker returning after lease expiry.

## Measurements

### Correctness

- Task acceptance success;
- false completion and false failure;
- duplicated external Effects;
- stale revisions used;
- unresolved `UNKNOWN` preserved or guessed.

### Continuity

- first correct action after replacement;
- retained Task, Task Attempt, Effect, and Artifact identity;
- repeated work;
- lost or fabricated assumptions;
- successful recovery without hidden reasoning export.

### Efficiency

- model calls and tokens;
- Context size and compilation time;
- Tool calls;
- wall and provider time;
- operator interruptions;
- adapter and shared code size.

### Capability retention

- provider features available directly versus through the interface;
- lowest-common-denominator losses;
- unsupported capability handling;
- explicit negotiation and fallback behavior.

## Evidence required

- exact repository and service revisions;
- interface and capability-manifest versions;
- complete Task/Assignment/Run/Tool/Job/Artifact identity map;
- full non-sensitive traces and usage receipts;
- final verification against authoritative repository or World state;
- equal or declared budgets;
- retained failures and negative results;
- code and protocol cost comparison;
- explicit retain, localize, shrink, or delete decision.

## Falsifiers

- direct provider integration remains simpler and equally correct;
- shared abstraction removes important Harness capabilities;
- Host capsule plus fresh provider Session matches cross-Harness continuation;
- no second workload needs a shared interface;
- CompletionProposal does not prevent a real failure;
- capability negotiation and event mapping cost more than adapter duplication;
- a stable interface cannot survive normal provider evolution;
- Harness logic repeatedly leaks Host scheduling or Runtime execution authority.

## Promotion rule

A standalone `ordivon-harness` repository requires:

- at least two live adapters;
- at least two consuming workloads or repositories;
- one successful mid-Task Harness replacement;
- stable lifecycle and capability contracts;
- independent release/test value;
- measurable duplicate-code reduction;
- no Host or Runtime authority in the package.

Before that point, retain the boundary as Host-local interfaces, adapters, and Computing experiments.

## Non-goals

- no universal Agent protocol;
- no reimplementation of Codex or Claude Code;
- no provider-independent hidden reasoning format;
- no global memory, Skill, Plugin, or Hook platform;
- no Task scheduler inside Harness;
- no Workspace or process ownership inside Harness;
- no immediate `ordivon-harness` repository;
- no claim that one Session equals one Task;
- no requirement that all providers expose identical features.

## Consumers

- `ordivon-host` — Harness adapter, Assignment, completion, and continuation boundaries;
- `ordivon-runtime` — stable execution and evidence boundary;
- `ordivon-game` — deterministic continuation and lifecycle ablations;
- `ordivon-security` — adversarial control and evaluator-boundary tests;
- `ordivon-world` — capability negotiation and external rebinding;
- `ordivon-web` — publication only after accepted evidence.

The source-grounded concept system and complete experiment program live in [`../../studies/2026-agent-system-concept-system/`](../../studies/2026-agent-system-concept-system/).
