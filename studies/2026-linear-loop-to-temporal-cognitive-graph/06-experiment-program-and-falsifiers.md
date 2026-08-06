# Experiment Program and Falsifiers

## 1. Objective

Determine whether a minimal Temporal Cognitive Graph improves verified long-horizon work over transcript-centered alternatives under controlled model, Tool, Runtime, verifier, and budget conditions.

The program is owned by `ANC-COMPILER-002`. It does not become an active portfolio line until current Harness control and evaluation lines free capacity.

## 2. Baselines and variants

### B0 — current sequential transcript

- current `SequentialEngine`;
- messages and observations as cognitive state;
- current Run recovery;
- no graph;
- no Child Runs.

### B1 — transcript plus compaction/retrieval

- same Engine and Run boundary;
- explicit summary/compaction;
- semantic or keyword retrieval over retained messages/Artifacts;
- no typed cognitive graph.

This is the strongest narrow alternative and must not be omitted.

### T0 — shadow graph

- B0 behavior unchanged;
- derive nodes/edges from existing events and Artifacts;
- graph is read-only diagnostic projection;
- compare stability, extraction error, and operator usefulness.

### T1 — single-Actor TCG

- Context compiled from explicit Working Set;
- typed Claims, Unknowns, EvidenceRefs, WorkItems, and mutations;
- no Child Runs;
- all Effects still use current Tool/Runtime path.

### T2 — TCG with bounded Child Runs

- branch/delegation contracts;
- isolated Context and budgets;
- immutable returned Artifacts and graph mutations;
- explicit join policy.

### T3 — external recursive/RLM Engine

- same Run Contract, Effect Broker, Runtime, verifier, and TCG projection;
- Prime RPC or another external Engine;
- no self-refinement activation.

### T4 — governed HarnessRevision

- offline or shadow RefinementProposal;
- replay and holdout evaluation;
- canary and rollback;
- no permission, verifier, reward, or authority self-change.

## 3. Minimum workloads

## W1 — conflicting repository diagnosis

A repository contains:

- two plausible root causes;
- evidence supporting each;
- one stale source snapshot;
- one Tool result that contradicts an earlier assumption;
- a required patch and tests.

Purpose: test Claim/Evidence/conflict state and stale invalidation.

## W2 — interruption and model replacement

Interrupt after:

- multiple hypotheses exist;
- one Runtime Job is terminal;
- one branch is blocked;
- one required evidence object has not been read.

Resume with a fresh process and a different model or Engine Session.

Purpose: test whether graph state outperforms transcript summary for continuation.

## W3 — breadth-first evidence synthesis

Several independent sources must be inspected, but the final answer requires exact provenance and resolution of conflicting evidence.

Purpose: test bounded parallelism, compression, and join without relying on coding-specific mutation.

## W4 — branch/join code change

Two independent read or analysis branches produce Artifacts. A deterministic or model-assisted join must produce one verified source change.

Purpose: test Child Run scope, Artifact-first integration, and Workspace isolation.

## W5 — reward-hacking trap

A shortcut improves a visible metric but violates a hidden or held-out constraint.

Purpose: test verifier separation and HarnessRevision governance.

## 4. Frozen controls

For each comparison freeze:

- TaskDescriptor and acceptance criteria;
- source revision and fixture;
- model family and model version where possible;
- Tool catalog and ToolGrant;
- Runtime revision and execution profile;
- token, turn, wall-time, Job, and money budgets;
- verifier and held-out checks;
- retry and cancellation policy;
- number of trials and seed policy;
- evidence export schema.

## 5. Primary metrics

### Outcome

- accepted verified completion rate;
- false completion rate;
- failed/blocked/cancelled disposition;
- held-out verifier pass rate;
- semantic quality where deterministic verification is impossible.

### Efficiency

- total input/output tokens;
- provider calls;
- Tool calls and Runtime Jobs;
- wall time;
- repeated source reads;
- duplicate branch work;
- Context materialization bytes/tokens;
- graph event/object/query overhead;
- operator interventions and review time.

### Continuity

- successful fresh-process resume;
- model/Engine replacement success;
- lost state count;
- stale Evidence or revision errors;
- time and tokens to regain useful state;
- duplicate physical Effect rate;
- unresolved uncertainty preservation.

### Cognitive-state quality

- unsupported Claims;
- evidence coverage for accepted Claims;
- conflicts detected and resolved;
- Unknowns silently dropped;
- branch completion and join fidelity;
- graph extraction precision/recall in T0;
- mutation rejection and stale-write rate.

### Safety and authority

- unauthorized Effect attempts;
- ToolGrant violations;
- direct kernel-to-world bypass attempts;
- verifier or reward manipulation;
- permission-diff changes;
- recovery from ambiguous Runtime delivery.

## 6. Fault injection

Inject at least:

- response loss after Provider dispatch;
- response loss after Runtime admission;
- Harness process death after graph event object write but before projection commit;
- stale CognitiveMutation after another branch advances the graph;
- Child Run crash before result admission;
- conflicting Child Run Claims;
- Context object corruption or missing CAS object;
- Runtime concurrency rejection;
- Workspace source drift;
- cancellation during Provider, Worker, or Runtime execution;
- HarnessRevision candidate that improves visible score by exploiting the environment.

## 7. TCG-P0 — shadow projection gate

### Acceptance

- deterministic rebuild from existing Harness events;
- no production behavior change;
- at least 95% precision on the small hand-labeled operational node/edge set;
- operator can identify active objective, Unknowns, evidence, and active Effect without replaying the full transcript;
- projection rebuild and query cost remains bounded;
- no raw chain of thought is required.

### Falsifier

The projection is unstable, mostly duplicates message content, cannot distinguish current from historical state, or costs more to maintain than it saves in diagnosis.

### Deletion

Delete TCG projection code; retain the study and labeled dataset.

## 8. TCG-P1 — single-Actor Working Set gate

### Acceptance

Across W1 and W2, T1 must show at least one material gain:

- higher verified completion;
- lower false completion;
- lower resume cost;
- fewer repeated reads;
- lower token use at equal quality;
- better preservation of Unknowns/conflicts.

The gain must exceed graph maintenance cost and survive repeated trials.

### Falsifier

B1 transcript plus compaction/retrieval matches or exceeds T1 across outcome, recovery, and cost.

### Deletion

Keep B1 improvements and remove graph-authoritative execution.

## 9. TCG-P2 — Child Run gate

### Acceptance

On W3 and W4, T2 must improve breadth, wall time, or evidence quality without unacceptable token multiplication, duplicate work, or integration failure.

Every Child Run must have bounded scope, budget, Context grant, returned Artifact/evidence, cancellation, and join disposition.

### Falsifier

A single Actor plus independent verifier matches quality and cost, or ordinary Host Tasks with deterministic join are sufficient.

### Deletion

Retain single-Actor TCG if P1 passed; delete Child Run coordination objects.

## 10. TCG-P3 — external Engine gate

### Acceptance

An external recursive/RLM Engine must fit the same Run, Effect, Runtime, and verifier boundaries without hiding authority or requiring Host to understand provider-specific internal events.

Compare it with `SequentialEngine` under the same Task and budget.

### Falsifier

The Engine cannot expose stable observation/recovery/completion semantics, bypasses Runtime effects, or adds no outcome/cost benefit.

### Deletion

Remove the adapter; retain `HarnessExecutionEngine` only if another implementation consumes it.

## 11. TCG-P4 — continual Harness gate

### Acceptance

A proposed HarnessRevision must improve held-out verified outcomes across repeated tasks, pass permission and boundary diffs, survive adversarial cases, and roll back cleanly.

### Falsifier

Improvement does not transfer, exploits evaluator/environment artifacts, degrades another workload, or requires self-editing protected authority.

### Deletion

Delete automatic activation. Retain trajectory review and human-reviewed proposals if they create net value.

## 12. Promotion conditions

A TCG object enters reusable Knowledge only after one successful experiment. It enters Core or Protocol only after:

- two materially different workloads or Engines;
- stable ownership and recovery invariants;
- measured net benefit;
- cross-repository consumers;
- deletion of unnecessary node/edge/event types;
- compatibility and migration evidence.

## 13. Stop rule

Stop expanding the model when the next object or relation does not change an admission, recovery, scheduling, verification, or completion decision. Richer diagrams are not evidence of a better system.
