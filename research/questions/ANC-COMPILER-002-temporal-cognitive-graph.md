# ANC-COMPILER-002 — Temporal Cognitive Graph and Programmable Context

## Status

Deferred at M1. The first-principles derivation, pinned Ordivon source audit, and primary-source comparison are complete in [`../../studies/2026-linear-loop-to-temporal-cognitive-graph/`](../../studies/2026-linear-loop-to-temporal-cognitive-graph/). Construction remains blocked behind the current Harness control and evaluation lines so the research portfolio does not hide unfinished P0 work.

## Question

What is the smallest typed temporal cognitive state, Working Set, and mutation interface that lets an Ordivon Harness preserve parallel hypotheses, conflicts, evidence, Child Runs, joins, and recovery better than a sequential transcript plus compaction/retrieval, without creating a universal graph database, Agent VM, second Host, or hidden Effect path?

## Why this materially refines existing work

- `ANC-MEMORY-001` established that open work can continue from bounded semantic state without preserving a Provider Session as Task identity.
- `ANC-HARNESS-002` constructed a durable first-party sequential Loop and exposed the concrete absence of persistent Sessions, fork, compaction, and local subagents.
- `ANC-COMPILER-001` preserved the broad dynamic cognitive-control question but correctly blocked a general Agent VM before a branch/join failure.
- `ANC-MULTI-001` preserved branch, join, and Artifact coordination as a separate experiment.
- `ANC-VERIFY-001` now supplies the common trial and replay envelope needed for an ablation.

This question narrows those branches to one falsifiable state-model comparison rather than activating all of them independently.

## Hypothesis

A Harness-owned Temporal Cognitive Graph projected from append-only events, combined with bounded Working Sets and revision-fenced CognitiveMutations, will improve at least one of:

- verified completion;
- false-completion prevention;
- fresh-process/model replacement continuation;
- token and repeated-read cost;
- preservation of Unknowns, conflicts, and evidence;
- bounded Child Run integration.

The graph remains Run-local. Host owns commitment and completion, Runtime owns physical effects, and domain systems own truth.

## Minimum workload

One frozen repository-repair Task with:

- two plausible competing hypotheses;
- one stale source or Tool observation;
- one later contradictory observation;
- one interruption and fresh-process/model replacement;
- one required verified patch and test result.

Compare:

1. current sequential transcript;
2. transcript plus compaction/retrieval;
3. single-Actor Temporal Cognitive Graph and Working Set.

Only after the single-Actor comparison may one two-branch Child Run and explicit Join be added.

## First falsifier

A transcript-centered Harness with bounded compaction/retrieval, current Artifacts, and ordinary Host Task semantics matches or exceeds the Temporal Cognitive Graph on verified outcome, false completion, continuation, token cost, repeated reads, and operator review while using fewer durable objects and less maintenance.

## Additional falsifiers

- graph extraction or mutation error creates more stale or unsupported state than transcript replay;
- the graph mostly duplicates messages and does not change an admission, recovery, verification, or completion decision;
- ordinary Host Tasks and deterministic Join express the first multi-branch workload without Harness-local graph state;
- a mature Provider Harness supplies equivalent continuity and capability behind the current external execution boundary at lower permanent cost;
- graph write/query overhead or schema churn exceeds measured context and coordination savings.

## Acceptance path

1. `TCG-P0` shadow projection from current Harness events;
2. `TCG-P1` single-Actor Working Set versus strong transcript baseline;
3. `TCG-P2` bounded Child Run and Join only if P1 passes;
4. `TCG-P3` external RLM/recursive Harness Engine behind the same boundary;
5. `TCG-P4` governed HarnessRevision only after replay, holdout, canary, and rollback.

The complete metrics and fault matrix are in [`../../studies/2026-linear-loop-to-temporal-cognitive-graph/06-experiment-program-and-falsifiers.md`](../../studies/2026-linear-loop-to-temporal-cognitive-graph/06-experiment-program-and-falsifiers.md).

## Ownership hypothesis

```text
Computer
  derivation / experiment / comparison / promotion and deletion

Host
  Goal / Task commitment / consequence / verification / Outcome

Harness
  Run Actor / temporal cognitive state / Working Set / Engine / Child Run

Runtime
  Workspace / Job / Attempt / optional Worker / Artifact physical truth

Domain verifier
  authoritative semantic acceptance
```

## Deletion outcome

If falsified:

- delete graph-authoritative execution and Child Run objects;
- retain useful transcript compaction/retrieval or read-only diagnostics;
- preserve the study, labeled fixtures, and negative evidence;
- do not promote a Cognitive Graph schema, graph store, Agent VM, or Runtime Worker.

## Reopen and scheduling condition

Begin implementation only after:

- `ANC-HARNESS-002` has one frozen independent Harness baseline;
- `ANC-VERIFY-001` can compare repeated complete Trials;
- one current active portfolio line exits or this question explicitly replaces it;
- the owner accepts the minimum workload and deletion path.
