# ANC-VERIFY-001 — Agent Evaluation, Replay, and Trajectory Flywheel

## Status

Active at M3 for Track R. Status and next action remain owned by `research/portfolio.json`. The earlier deferral condition has been discharged by three live Host/Harness experiments: Codex App Server H3, Hermes ACP H4, and bidirectional Harness replacement H5 now expose stable repeated identities for Task, Assignment, Harness Run, model, Tool catalog, Runtime Job, Artifact, usage, stop, verification, and recovery evidence.

## Question

What is the smallest evaluation, replay, and trajectory structure that can distinguish the contributions of model, Harness, Context, Tool contract, budget, verifier, and environment to an Agent's work without creating a second production control plane?

## Why this is now actionable

The question was previously deferred until at least three real experiments shared enough evidence fields to justify a common envelope. That threshold is now met:

- H3 retained a Codex Thread/Turn lifecycle, one Tool action, usage, Runtime evidence, and a Host Run receipt without claiming semantic completion;
- H4 retained a materially different Hermes ACP Session/Prompt lifecycle, thought-event counts without thought text, Tool observation, usage, Runtime evidence, and the same Host Run boundary;
- H5 retained two replacement orders, Assignment generation, verified Artifacts, stale-completion rejection, response-loss reconciliation, independent acceptance, and one final TaskOutcome.

The common structure is not a shared Provider lifecycle. It is an experiment envelope around existing component-native evidence.

## Working hypothesis

A thin, append-only evaluation envelope can support fair comparisons, failure attribution, regression detection, and later counterfactual replay when it binds:

```text
Task definition and version
+ exact model and Harness identity
+ Context and Tool-contract identity
+ declared budgets and sampling
+ component-native traces and Artifacts
+ independent verifier result
+ explicit unknown and missing measurements
```

No evaluation database, workflow engine, Agent Loop, or universal Provider event model is required for the first useful result.

## Unit of evaluation

The primary evaluated system is:

```text
Task
× model
× Harness
× Context strategy
× Tool contract
× budget
× environment
```

A model-only ranking is not admitted when Harness, tools, Context, or verifier differ materially.

## Research objects

Track R initially defines four research-only records:

- **Task Definition** — immutable objective, initial state, capabilities, budget profile, acceptance contract, oracle, reproducibility requirements, and limitations;
- **Trial Manifest** — exact configuration and evidence bindings for one stochastic or deterministic run;
- **Trial Result** — observed outcome, verifier assertions, cost, action counts, Artifacts, trace reference, and limitations;
- **Failure Record** — first observable failure, responsible boundary, recovery, duplicate-Effect status, intervention, and evidence.

These records aggregate existing evidence. They do not replace Host Task, Harness Run, Runtime Job, Artifact, CompletionDecision, or System Snapshot.

## First research program

1. Validate the envelope against H3, H4, and one H5 trajectory.
2. Freeze `HARNESS-REPO-REPAIR-001` from the existing H5 repository-repair fixture.
3. Require oracle-pass, baseline-fail, known-invalid rejection, and repeated rebuild agreement.
4. Run the same task under one-shot, Ordivon Harness, and a mature Provider Harness.
5. Read all failed and anomalous trajectories before adding fields or mechanisms.

## Evidence requirements

A capability or architecture claim requires:

- exact source and environment revision or an explicit declaration that the historical evidence did not retain one;
- model, Provider, Adapter, Harness, Context, Tool catalog, and budget identity;
- at least one independent outcome assertion;
- explicit unknown measurements rather than invented zeroes;
- repeated trials for stochastic comparisons;
- component-native evidence references and content digests;
- disclosed task and verifier limitations.

Single trials may establish an existence, boundary, or failure case. They may not establish a general model ranking.

## Replay model

Track R distinguishes:

- **observation replay** — hold Task, Context, and Tool observations fixed while replacing model, prompt, or stop policy;
- **world replay** — reconstruct the initial environment and execute physical actions again.

Observation replay is unsuitable for claims about real side effects. World replay is unsuitable for isolating cognition when the world is nondeterministic. Both remain deferred until the first frozen workload and Trial envelope are stable.

## Privacy and reasoning boundary

Raw private Chain-of-Thought is not a required research asset. Track R retains externally observable cognition and action evidence: selected Context, Tool Calls, observations, Artifacts, verifier assertions, stop, usage, and component-native digests. Provider reasoning counts or digests may be retained when available, but the system must remain valid without reasoning text.

## Falsifiers

Shrink or delete the common envelope if any of these hold:

- H3, H4, and H5 cannot be represented without copying their Provider-specific lifecycle into the common schema;
- the frozen workload cannot distinguish one-shot, Ordivon Harness, and mature Harness outcomes with one verifier;
- Task QA reveals that verifier or environment variance dominates the measured model/Harness difference;
- the common records duplicate Host, Runtime, or Harness production state rather than referencing it;
- local receipts and a small comparison script provide equal explanatory value with materially less permanent structure.

## Non-goals

- a public model leaderboard;
- a general LLM observability service;
- a new `ordivon-evals` repository;
- a Harness database or durable scheduler;
- automatic model routing;
- post-training before sufficient validated trajectories exist;
- one composite intelligence score;
- evaluation based on hidden reasoning text.

## Current disposition

Retain the question and localize implementation to versioned files, standard-library validation, product-owned fixtures, and immutable evidence references. Promotion beyond Track R requires repeated consumers and measurable net deletion elsewhere.
