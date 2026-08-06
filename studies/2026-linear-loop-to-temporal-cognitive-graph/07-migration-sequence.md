# Migration Sequence

## 1. Migration principle

Do not replace the proven sequential production path in one rewrite. Introduce reversible seams, run shadow projections, compare against strong narrow baselines, and promote only after evidence.

```text
preserve current authority
→ expose Engine seam
→ shadow relational state
→ bounded Working Set
→ optional Child Runs
→ optional persistent Workers
→ governed adaptation
```

## 2. Phase M0 — research and contract freeze

### Computer

- record `ANC-COMPILER-002`;
- freeze terminology, falsifiers, and experiment variants;
- retain the study as research evidence, not Core;
- do not activate a third WIP line.

### Harness

- document current sequential baseline revision;
- freeze the `HarnessRunContract`, ToolGrant, budget, trace, and CompletionProposal inputs used by the first trial;
- export read-only evidence required by `ANC-VERIFY-001`.

### Exit

One reproducible B0 baseline and one frozen W1/W2 fixture.

## 3. Phase M1 — boundary convergence

### Host

- route new model execution through independent Harness external execution;
- freeze new Host cognition features;
- preserve existing cognition profiles as fixtures/compatibility;
- make external Run start operationally asynchronous.

### Harness

- complete independent Journal/CAS cutover for new Runs;
- add `HarnessExecutionEngine` with `SequentialEngine` only;
- add Supervisor acceptance/binding without graph state;
- ensure fresh-process observe/cancel/recover/collect-completion.

### Runtime

- no new abstraction.

### Exit

The same sequential Run survives detached Harness execution and Host/Harness restart without changing outcome semantics.

### Stop

If the independent service adds no lifecycle value and synchronous execution is sufficient for all admitted workloads, do not continue to Actor work.

## 4. Phase M2 — shadow graph projection

### Harness

- project minimal Objective, WorkItem, Claim, Unknown, EvidenceRef, and EffectProposal nodes from existing events;
- derive only deterministic relations first;
- store projection in the existing Journal/CAS or rebuildable local index;
- expose read-only inspect/export;
- collect labeled graph-quality evidence.

### Restrictions

- graph cannot alter Engine input;
- graph cannot dispatch Tools;
- graph cannot complete a Run;
- no graph database;
- no Child Runs.

### Exit

TCG-P0 passes.

## 5. Phase M3 — typed mutation and Working Set

### Harness

- add `CognitiveMutation` admission with expected revision;
- compile a bounded Working Set from current graph and object references;
- allow `SequentialEngine` to consume the Working Set through model-specific formatting;
- retain transcript export and fallback;
- record omissions, selection method, and materialization digest.

### Restrictions

- mutations only affect Run-local cognitive state;
- Effects continue through existing Tool Step and Runtime boundaries;
- no persistent Python kernel requirement;
- no self-refinement.

### Exit

TCG-P1 passes against B1.

### Stop

If transcript plus compaction/retrieval matches T1, delete authoritative graph execution and retain only useful diagnostics.

## 6. Phase M4 — Run Actor and mailbox

### Harness

- make Run activation lease and wakeup explicit;
- add durable mailbox and direct message receipt;
- bind replaceable Engine Session;
- rehydrate active Run from graph and mailbox after process loss;
- separate Run accepted, active, waiting, paused, completion-proposed, and terminal physical lifecycle as narrowly as evidence requires.

### Host

- observe foreign Run revisions without polling hidden Session state;
- retain Task completion authority.

### Exit

Long-running detached W2 continuation succeeds with a fresh Engine Session.

## 7. Phase M5 — bounded Child Runs

### Harness

- add delegation contract, Context grant, ToolGrant, budget, deadline, result schema, and join policy;
- isolate branch graph scopes;
- return immutable Child Artifacts and mutation proposals;
- add cancel remainder, quorum, first-verified, and compare-and-select only when required by fixtures.

### Runtime

- use independent existing Workspaces and Jobs first;
- add snapshot/fork only after repeated setup cost or source-transfer ambiguity is measured.

### Exit

TCG-P2 passes.

## 8. Phase M6 — external RLM/recursive Engine

### Harness

- implement one `PrimeRpcEngine` or equivalent adapter;
- map external Session to replaceable EngineSessionRef;
- retain external JSONL/transcripts as evidence Artifacts, not Harness authority;
- map subagents to Child Run observations only where the external Engine exposes stable identity;
- block direct external effects outside the Effect Broker;
- disable automatic refinement activation.

### Runtime

- run the external Engine in a restricted environment; never grant the current root trusted-local authority by default;
- use terminal Job supervision first;
- introduce Worker/WorkerCall only if repeated activation or interactive state requires it.

### Exit

TCG-P3 passes.

## 9. Phase M7 — physical Worker and Workspace fork, conditional

### Runtime Worker

Admit only if experiments show a persistent physical process is necessary. Provide:

- create or admit;
- observe;
- call with idempotent request identity;
- cancel/terminate;
- heartbeat;
- reconcile;
- retained Artifacts and terminal evidence.

### Workspace fork

Admit only if parallel source mutation repeatedly needs exact parent uncommitted state. Prefer exact revision Workspaces and patch Artifacts when sufficient.

### Exit

A second consumer beyond one Prime/RLM adapter or one workload demonstrates the same physical invariant.

## 10. Phase M8 — governed continual Harness

### Computer and Eval

- define frozen replay and holdout sets;
- add adversarial evaluator and reward-hacking cases;
- preserve comparison and rollback evidence.

### Harness

- add `HarnessRevision` and `RefinementProposal`;
- permit low-risk memory or retrieval candidates first;
- require stronger gates for prompt, executable Skill, subagent spec, and Context policy changes;
- never allow self-editing of permission, authority, verifier, reward, audit, or immutable evidence.

### Exit

TCG-P4 passes across at least two workload families.

## 11. Repository responsibility map

| Change | Owner |
|---|---|
| research question, experiment, comparison, promotion | Computer |
| Task commitment and final completion | Host |
| Run Actor, graph, Working Set, Child Runs, Engine adapters | Harness |
| Workspace, Job, Worker, process, Artifact physical truth | Runtime |
| world state and semantic verification | domain owner |
| user/operator view | Host/Harness product surface, not authority |

## 12. Compatibility strategy

- current sequential Run contracts remain readable;
- transcripts remain exportable;
- graph fields are additive and local until promotion;
- no dual authoritative write path;
- shadow projections can be rebuilt or deleted;
- Engine-specific Sessions are replaceable and not Task identity;
- external Harness events remain opaque unless a stable observation mapping is demonstrated;
- Protocol promotion is last, not first.

## 13. Completion definition

The reform is complete only if the retained implementation:

1. improves accepted verified work or continuation at measured net benefit;
2. preserves Host and Runtime truth boundaries;
3. supports at least one replacement Engine;
4. survives interruption and stale mutations;
5. makes unresolved work and evidence more legible;
6. deletes failed graph, Worker, or multi-Agent candidates;
7. does not require a universal graph platform or private reasoning capture.
