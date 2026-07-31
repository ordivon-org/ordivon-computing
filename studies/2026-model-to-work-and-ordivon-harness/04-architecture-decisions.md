# Architecture Decisions

## D1 — Keep the complete logical stack; avoid one monolithic product ontology

Retain the logical distinction among Model, Harness, Host, Runtime, Workload Contract, World, Verifier, Surface, and participant authority.

This does not require one service or repository per layer. It prevents replacement, recovery, and completion facts from becoming implicit.

## D2 — Build Ordivon Harness for bare models

Ordivon requires a first-party Agent Loop when a Provider supplies model inference but no mature Harness.

Ordivon Harness will own:

- Model Adapter calls;
- model-specific input compilation from Host Context;
- sequential Agent Loop;
- Tool request interpretation;
- Runtime Tool Bridge;
- Run-local messages and observations;
- turn/token/time/Job budgets;
- cancellation and stop classification;
- Run evidence and `HarnessRunReceipt` production.

It will not own Goal, durable Task state, Workspace/process truth, or semantic completion.

## D3 — Do not use Ordivon Harness to wrap and normalize mature Provider Harness internals

Codex App Server, Hermes ACP, Claude Code/Agent SDK, and similar systems should remain provider-faithful direct backends.

The common Host boundary is:

```text
HarnessAssignment in
HarnessRunReceipt / CompletionProposal out
```

Their internal Session and event models remain distinct.

## D4 — Clarify the H5 repository rejection

H5 rejected a standalone repository extracted from the Codex/Hermes shared-lifecycle hypothesis because:

- observed lifecycle overlap was low and mostly mechanical;
- no second independent consumer existed;
- direct drivers still depended on Host objects;
- provider-specific semantics would be lost;
- independent release value was not demonstrated.

H5 did not decide that Ordivon can never own a first-party Harness. The first-party Harness is a different implementation question: it creates an Agent Loop where no mature loop is supplied.

## D5 — Keep Task Attempt and Assignment generation

A Task Attempt is one durable semantic path. Multiple Harness Runs and Provider Sessions may occur within it.

Assignment generation is retained as the stale-worker fence because F1 demonstrated a completion claim that Task revision alone did not describe as clearly.

No mutable Attempt state machine or table is admitted.

## D6 — Keep Run evidence separate from TaskOutcome

`HarnessRunReceipt` records what one Harness Run did. `CompletionProposal` records a claim. `CompletionDecision` records Host adjudication. `TaskOutcome` records accepted terminal Task truth.

F2 demonstrated that collapsing these objects would admit false completion after a successful process with no required Artifact.

## D7 — Artifact-first, not prose-first

Provider final text is optional observation.

Completion authority is based on:

- required Artifact existence and digest;
- source/world state;
- independent acceptance evidence;
- current Assignment generation;
- resolved or explicitly retained uncertainty;
- Host decision.

This rule applies to external mature Harnesses and the future Ordivon Harness.

## D8 — Runtime remains semantically ignorant

Runtime receives opaque references and request identity, owns physical execution, and returns evidence. It does not store Host Tasks, Harness Assignments, or semantic completion.

F3 demonstrated that response-loss recovery can work through current request identity and references without a Runtime query platform.

## D9 — Workload Contract remains an arrangement, not a new core object

Current Task, Context, Assignment, Artifact, acceptance, Effect, and source-binding objects can express the first Ordivon Harness workload.

Do not add `WorkloadCapsule` or a Workload Harness platform until two materially different workloads repeatedly need the same missing envelope.

## D10 — Persistent Session is Harness-local

Host issue language that proposes a persistent Host model Session is superseded in ownership.

A persistent Provider/model Session may later be tested inside Ordivon Harness or an external Harness, but:

- it is not Task identity;
- replacement must not claim hidden-state continuity;
- exact per-turn Context and usage evidence must remain visible;
- a fresh Session path remains a recovery baseline.

## D11 — Defer compaction, parallelism, subagents, routing, and Plugins

These are legitimate Harness capabilities, not v0 requirements.

They are admitted only after a real v0 trajectory exposes a concrete limitation and an ablation shows net benefit.

## D12 — Initial implementation remains inside Host

The first implementation should live under the existing Host Harness package because:

- Assignment, Context, Runtime references, and Run receipts already exist there;
- no network service or independent deployment is required;
- no second consumer has yet demonstrated independent release value;
- extraction before stable behavior would create versioning and ownership overhead.

A future `ordivon-harness` repository is allowed only after the new first-party implementation—not the rejected cross-provider adapter hypothesis—passes its own promotion gate.

## Closed and open matrix

| Question | Decision |
|---|---|
| Who owns one model/Tool loop? | Harness |
| Who owns durable Task truth? | Host |
| Who owns process truth? | Runtime |
| Is Provider Session Task identity? | No |
| Does exit zero complete a Task? | No |
| Is final assistant text required completion evidence? | No |
| Should mature Provider lifecycles be normalized? | No |
| Does Ordivon need an Agent Loop for bare models? | Yes |
| Must that implementation be a repository now? | No |
| Does v0 need compaction/subagents/parallel Tools? | No evidence yet |
| Does v0 need a database or service? | No |
