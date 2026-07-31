# VERIFY-CHARTER-001 — Ordivon Evaluation, Replay, and Trajectory Research

Status: active Track R charter

## Mission

Track R determines whether Ordivon Agents actually complete useful work, why they succeed or fail, when they should stop or abstain, and which part of the model-to-world system caused the observed result.

It converts real Ordivon work into reproducible Tasks, version-bound Trials, independent verification, failure attribution, and replayable evidence without becoming a second Host, Harness, Runtime, or workflow platform.

## Governing principle

```text
measure the complete system
preserve component-native truth
promote only repeated evidence
```

## Ownership

### Ordivon Computer

- research questions, competing hypotheses, task-admission criteria, comparison design, interpretation, and falsification;
- common research-only Task, Trial, Result, and Failure envelopes;
- failure taxonomy and experiment reports;
- decisions to retain, localize, shrink, defer, or delete an abstraction.

### Ordivon Host

- Goal, Task, Attempt, Assignment, Context selection, completion admission, and TaskOutcome;
- authoritative semantic state and operator handoff;
- product-owned workload fixtures when Host is the consumer.

### Ordivon Harness

- model invocation, Run-local Context, Agent Loop, Tool Calls, observations, budgets, stop, usage, and Run trace;
- no Eval-specific production lifecycle.

### Ordivon Runtime

- Workspace, Job, Attempt, process truth, physical output, Artifact retention, and uncertain-delivery evidence;
- no semantic score or Task completion claim.

### Verifier

- independent assertions over final state and required Artifacts;
- versioned tests and explicit limitations;
- no authority to rewrite the Task or hide requirements.

### Evaluation runner

- clean environment construction, execution-path selection, evidence collection, verifier invocation, and Trial aggregation;
- no ownership of Host Task state or automatic redispatch after uncertain Effects.

## Required invariants

1. The evaluated unit includes model and Harness; model-only rankings require otherwise identical system conditions.
2. Unknown measurements remain `null` or explicitly unavailable, never synthetic zeroes.
3. A model's final text cannot substitute for independent acceptance when the Task changes the world.
4. Every formal Task has a versioned initial state, verifier, oracle or human baseline, reproducibility check, and known limitations.
5. Trial evidence binds exact source, model, Adapter, Harness, Context, Tool contract, budget, and environment identities when they were retained.
6. Historical evidence may declare missing fields; the envelope must not fabricate them retroactively.
7. Provider-native lifecycle events remain Provider-native. Track R references their digests and normalized outcome fields only.
8. Raw private reasoning is not required for validity.
9. Failed hypotheses, flaky verifiers, observer failures, and false accepts remain visible.
10. No Track R record directly dispatches an Effect or completes a Host Task.

## Task admission

A Task enters a formal suite only after:

- the initial baseline fails for the intended reason;
- an oracle or reference solution passes;
- at least two known-invalid solutions are rejected;
- repeated clean rebuilds agree;
- verifier assertions test outcomes rather than one preferred method;
- the task description contains no hidden requirement required by the verifier;
- the model workspace excludes oracle, hidden verifier internals, prior answers, and leaked trial results;
- private data is removed or the Task remains private and access-bound.

## Comparison policy

- smoke: one Trial per configuration for environment and protocol validity;
- development: three Trials per configuration for fast iteration;
- architecture decision: five to ten Trials per competitive configuration when cost permits;
- all failures, false completions, and anomalous-cost successes receive trajectory review;
- confidence intervals or raw counts accompany stochastic comparisons when sample size supports them.

## Initial scope

Track R0–R2 includes:

- reopening `ANC-VERIFY-001` from H3–H5 evidence;
- an executable Evaluation Evidence Contract;
- historical Trial projections for H3, H4, and H5;
- one frozen repository-repair Task with oracle, known-invalid candidates, hidden verifier, and deterministic QA.

It does not yet include a general runner, replay engine, model router, dataset service, or post-training pipeline.

## Promotion gates

A standalone package or repository becomes eligible only when:

- at least two product repositories consume the same contract;
- at least twenty validated Tasks exist across more than one workload family;
- repeated Trials demonstrate common runner or storage duplication;
- extraction produces measurable net deletion and independent release value.

Post-training research becomes eligible only after at least one hundred privacy-reviewed, verifier-bound trajectories exist across multiple models and failure classes.

## Stop and deletion conditions

Shrink or delete Track R infrastructure if:

- three real experiment families do not retain stable common fields;
- Task QA costs exceed the decisions enabled by the suite;
- verifier instability dominates model or Harness variance;
- a mature external eval framework can consume Ordivon component evidence with less permanent code and equal semantics;
- the research records begin duplicating production authority or lifecycle state.

## First deliverable

The first acceptable result is not a benchmark score. It is one trustworthy answer to:

> Under the same frozen repository task and verifier, what does a multi-turn Ordivon Harness add over a one-shot model call, and where does it still differ from a mature Provider Harness?
