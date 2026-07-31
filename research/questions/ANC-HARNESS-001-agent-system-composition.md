# ANC-HARNESS-001 — Harness, Host, Runtime, and Agent-System Composition

> **Status:** completed at M5 on 2026-07-31. H1–H5 retained a Host-local durable boundary with provider-specific direct drivers and rejected extracting those drivers into a shared cross-Provider lifecycle or repository.
>
> **Scope clarification:** this decision does not reject a first-party **Ordivon Harness** for bare model APIs. That distinct construction question is [`ANC-HARNESS-002`](ANC-HARNESS-002-ordivon-harness.md).
>
> **Evidence index:** [`../evidence/snapshots/harness-boundary-h5-20260731t031134z.json`](../evidence/snapshots/harness-boundary-h5-20260731t031134z.json)

## Question

Can a thin, capability-preserving Harness boundary allow Ordivon Host Tasks to run and continue across materially different Agent Harnesses while keeping durable work in Host, physical execution in Runtime, and provider-specific cognition features intact?

## Resolution

Yes, at the durable Host-object boundary; no, at a shared Provider lifecycle boundary. Codex and Hermes both continued one Task through Host-owned Task Attempt, Assignment generation, fresh Context, explicit Artifacts, Runtime identities, and Host completion admission. Their Session, event, Tool, terminal, and final-response semantics remained materially different.

The accepted cross-Provider boundary remains inside `ordivon-host`. Direct drivers preserve Provider capability, while a shared `HarnessAdapter`, provider-independent Session model, common event runtime, and repository extracted from those drivers were deleted from the route because their cost exceeded demonstrated duplicate-code reduction.

A separate first-party Agent Loop is now admitted for the case where a Provider supplies model inference but no mature Harness. It is named **Ordivon Harness**, begins as a Host-local construction, and must not normalize Codex/Hermes/Claude internal lifecycles.

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
## H5 closeout

The completed experiment ran both live replacement orders:

```text
Codex diagnosis → Assignment g2 → Hermes repair
Hermes diagnosis → Assignment g2 → Codex repair
```

Both trajectories preserved one Task Attempt, compiled fresh Context, transferred diagnosis through an explicit Artifact, started a new Provider Session, passed independent Runtime verification, and allowed Host alone to commit `TaskOutcome`.

The three first-fault families produced decisive results:

- stale generation-1 completion was rejected as `stale_assignment`;
- process success without the required completion Artifact was rejected as `missing_artifact`;
- a dropped Runtime response recovered exactly one admitted Job without redispatch.

Provider final text was not portable completion evidence: Codex returned usable structured text, while Hermes completed valid Artifacts and tests with no ACP assistant text. Verified Artifacts, source digest, Runtime evidence, and Host adjudication became authoritative.

Final disposition:

- **retain:** immutable Task Attempt role, Assignment generation, `HarnessRunReceipt`, `CompletionProposal` and `CompletionDecision`, Host Runtime references, provider-specific direct drivers, and one-shot baselines;
- **localize or shrink:** Provider modes and approvals, optional final text, and the immutable Task-Attempt descriptor;
- **delete or do not create:** shared `HarnessAdapter`, common Session or Provider lifecycle, synthesized universal Tool events, shared event runtime, Runtime Task state, new Harness SQL tables, global Hook framework, and `ordivon-harness`.

The question reopens only if a second independent consumer demonstrates a stable shared lifecycle with measurable net deletion and no material Provider-capability loss.
