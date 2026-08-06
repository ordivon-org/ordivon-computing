# From Linear Agent Loops to Temporal Cognitive Graphs

Status: completed first-principles architecture study; implementation remains gated by experiment  
Date: 2026-08-06  
Durable question: `ANC-COMPILER-002`

## Thesis

A Transformer can route information globally inside one materialized token sequence, but a long-running Agent system still advances through a sequence of bounded invocations, tool observations, process events, and world changes. Global attention inside one prompt is therefore not persistent global cognition.

Current Agent Harnesses usually compress durable work into a one-dimensional transcript:

```text
messages
→ model call
→ tool call
→ observation
→ append messages
→ repeat
```

That representation is useful for conversation and replay, but insufficient as the primary state of open work when the system must preserve several simultaneous hypotheses, unresolved conflicts, independent branches, child Agents, evidence provenance, waits, effects, and recovery across model replacement.

The minimum next abstraction is not a universal graph database or a stored chain of thought. It is a **Temporal Cognitive Graph**:

```text
append-only causal events
        ↓ checked projection
versioned typed cognitive graph
        ↓ context compiler
bounded local Working Set
        ↓ Transformer / Agent Engine
CognitiveMutation and Effect proposals
        ↓ structural, authority, and evidence admission
new events and graph revision
```

The graph represents operationally useful external state: objectives, claims, unknowns, evidence, work items, delegations, effects, and verification. It does not preserve hidden reasoning or claim that every internal model activation is inspectable.

## Main conclusion

Ordivon's Host–Harness–Runtime separation remains valid. The reform is a change in the principal computation unit:

```text
old:
Task → one sequential Run → one message history → terminal Jobs

candidate:
Task commitment → persistent Run Actor graph
                → programmable context views
                → bounded Child Runs and Effect proposals
                → Runtime Jobs or Workers
                → independent verification
```

The corresponding ownership remains distinct:

- **Host Commitment Graph** — durable Goals, Tasks, responsibility, consequence, decisions, verification, and Outcomes;
- **Harness Cognitive/Run Graph** — Run-local objectives, hypotheses, evidence, open work, Child Runs, Working Sets, and completion proposals;
- **Runtime Physical Causality Graph** — Workspaces, snapshots, Jobs, Attempts, Workers, process trees, and Artifacts;
- **Domain truth** — authoritative world state and semantic verification.

These are logical graph families with different invariants. They must not be flattened into one universal ontology, authority store, or mandatory graph database.

## Why this study exists now

Earlier Ordivon research deliberately deferred persistent Sessions, parallel Tools, subagents, dynamic cognitive control, and self-improving Harnesses until a thin first-party Harness exposed concrete limitations. That condition is now met:

1. the independent Harness exists and preserves Run, Provider Call, Tool Step, Snapshot, Trace, recovery, and completion-proposal state;
2. its cognitive execution remains a sequential message-and-observation loop;
3. its declared capabilities still exclude persistent Session, fork, compaction, and local subagents;
4. Host and Harness retain two cognition entry paths;
5. Host's external executor seam is lifecycle-correct but the current Harness adapter remains synchronously executed;
6. Runtime owns strong terminal Job/Attempt facts but no persistent interactive Worker abstraction;
7. RLM, recursive Harness, multi-Agent, context-engineering, and continual-Harness results now provide materially different external evidence.

The old v0 freeze was an experiment boundary, not a permanent claim that linear transcripts are the final cognitive state model.

## Route

1. [`00-method-and-claim-boundary.md`](00-method-and-claim-boundary.md) — evidence classes, terminology, non-claims, and admission rules.
2. [`01-first-principles-derivation.md`](01-first-principles-derivation.md) — step-by-step derivation from model inference to persistent open work.
3. [`02-current-ordivon-gap-audit.md`](02-current-ordivon-gap-audit.md) — source-bound Host, Harness, Runtime, and Computer findings.
4. [`03-frontier-and-industry-evidence.md`](03-frontier-and-industry-evidence.md) — papers and production lessons from frontier laboratories and companies.
5. [`04-temporal-cognitive-graph-model.md`](04-temporal-cognitive-graph-model.md) — candidate state model, invariants, graph families, and interfaces.
6. [`05-ordivon-reform-and-boundaries.md`](05-ordivon-reform-and-boundaries.md) — concrete Host, Harness, Runtime, verifier, and Computer reforms.
7. [`06-experiment-program-and-falsifiers.md`](06-experiment-program-and-falsifiers.md) — ablations, metrics, failure injection, acceptance, and deletion conditions.
8. [`07-migration-sequence.md`](07-migration-sequence.md) — reversible implementation order and stop gates.
9. [`REFERENCES.md`](REFERENCES.md) — primary papers, official engineering sources, and source limitations.
10. [`evidence/source-audit-20260806.json`](evidence/source-audit-20260806.json) — machine-readable local source observations used by this study.

## Decisions

### Retain

- Host revision, lease, Journal/CAS, commitment, DecisionRequest, verification, and terminal Outcome boundaries;
- Harness-independent Run persistence, Tool-step fences, Provider-call uncertainty, recovery, and CompletionProposal separation;
- Runtime request idempotency, Job/Attempt ownership, source-state commitment, terminal evidence, cancellation, and reconciliation;
- distinct graph semantics and existing anti-formalism/deletion rules.

### Reopen

- `ANC-COMPILER-001`'s dynamic cognitive-control question through the narrower `ANC-COMPILER-002` experiment;
- persistent Harness Run actors;
- programmable Context and Working Sets;
- Harness-local Child Runs and branch/join;
- asynchronous external Harness execution;
- Runtime Worker and Workspace fork only if the experiment requires them;
- evidence-governed Harness refinement only after replay, holdout evaluation, canary, and rollback exist.

### Reject for now

- one universal graph database;
- storing private chain of thought;
- making every hypothesis a Host Task;
- moving scheduling or semantic completion into Runtime;
- allowing a cognition kernel to bypass Runtime for external effects;
- automatic self-modification of permissions, verifier, reward, authority, or audit policy;
- replacing current production paths before a shadow projection and controlled ablation demonstrate net benefit.

## Promotion rule

Temporal Cognitive Graph concepts remain research candidates. Promotion requires:

1. a frozen workload where transcript plus retrieval/compaction fails or costs materially more;
2. a typed graph variant that improves verified outcomes, continuation, or cost;
3. recovery and stale-revision faults that the graph handles without hidden Session state;
4. a second materially different workload;
5. a narrower alternative comparison;
6. a deletion test showing which graph objects and relations are actually necessary.

Until then, this study changes the research model and migration hypothesis, not the shared Protocol or production default.
