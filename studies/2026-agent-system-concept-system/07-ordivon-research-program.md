# Ordivon Research Program

## 1. Question

Can Ordivon establish a thin, replaceable Harness boundary above durable Host work and below provider-specific Agent products, while keeping physical execution in Runtime and avoiding a lowest-common-denominator framework?

The desired result is not necessarily a new repository. The study may conclude that existing Harnesses plus local adapters are sufficient.

## 2. Ownership hypothesis

```text
Host
  Goal, Task, Task Graph, Ready Frontier
  Assignment, Task Attempt, lease, budget
  waits, decisions, completion, recovery

Harness
  Session, Context, working memory
  Model loop, Skills, Tool exposure
  local plan, local subagents, compaction

Runtime
  Workspace, Job, process
  physical observation, cancellation, Artifact

Domain World
  authoritative domain state and transition
```

Cross-layer objects preserve identity and provenance without becoming a universal internal ontology.

## 3. P0 research and boundary work

### P0.1 Canonical concept and ownership system

This study and the reusable Knowledge page establish:

- object categories;
- authoritative owner;
- lifecycle and replacement boundary;
- mature baseline;
- promotion and deletion test.

Acceptance:

- no Task/Job, Hook/Event, Skill/Tool, Session/Task, or Graph/Loop ambiguity remains in current project role statements;
- every new Issue uses the same terminology;
- no new repository is created from terminology alone.

### P0.2 Host–Harness interface spike

Implement a private or experimental interface inside `ordivon-host` or a Computing experiment:

```text
start_assignment
resume_run
send_signal
interrupt
stream_events
checkpoint
finish
```

The interface carries stable references, not provider internals.

Required backends:

1. one existing Codex or provider Harness path;
2. Hermes or another materially different path;
3. optional minimal Native Harness only when needed to isolate one semantic question.

Acceptance:

- one Host Task runs through two backends;
- Task identity and completion criteria remain stable;
- provider-specific capabilities remain declared rather than silently discarded;
- the experiment reports adapter code, duplicate logic removed, latency, token cost, and lost features.

### P0.3 Completion Proposal boundary

Introduce or simulate:

```text
Harness CompletionProposal
→ Host validation
→ TaskCompleted / rejected / waiting / reopened
```

Fault cases:

- process exits zero but required Artifact is absent;
- stale Assignment submits completion;
- Tool result claims success while external outcome is `UNKNOWN`;
- acceptance evidence was generated against an old revision;
- two workers submit conflicting completion proposals.

Acceptance:

- no Harness or Runtime Job can directly establish Goal completion;
- stale fencing generation is rejected;
- all accepted completion links to required Evidence;
- added state remains smaller than the failure it prevents.

### P0.4 Runtime naming and execution contract

Clarify Runtime `task.*` operations as backend Job control. Evaluate a compatible migration toward `job.*` or an explicit documentation/alias layer.

Required contract:

- stable Job and Runtime Attempt identity;
- client request or correlation identity;
- observation and cancellation;
- Artifact references;
- response-loss recovery;
- structured Event/trace linkage;
- no Goal, Task Graph, or completion authority.

Do not rename public operations merely for aesthetics. Migration requires a real consumer and compatibility plan.

## 4. P1 experiments

### E1 Cross-Harness continuation

Run one real Ordivon engineering or research Task:

```text
Harness A begins
→ produces Evidence and checkpoint
→ Session is terminated
→ Host reassigns to Harness B
→ Harness B recompiles Context
→ original Task continues and completes
```

Compare:

- retained Task and Task Attempt identity;
- first correct action after replacement;
- duplicated work;
- stale assumptions;
- Context size and compilation time;
- provider-specific feature loss;
- final Evidence and outcome.

No claim of hidden reasoning continuity is allowed.

### E2 Retained state and compaction ablation

Within one Harness family compare:

1. rolling truncation;
2. compacted Session summary;
3. Host-derived continuation capsule;
4. provider-native retained reasoning or Session state where available.

Measure outcome, repeated work, token cost, incorrect rule reconstruction, and recovery after restart.

### E3 Skill and Tool working-set experiment

Compare:

1. all Tools and instructions eagerly loaded;
2. deferred Tool discovery;
3. task-relevant Skill and Tool selection;
4. incorrect or stale Skill injection.

Measure context size, Tool-selection accuracy, latency, Task outcome, and resistance to stale or malicious instructions.

### E4 Hook/Event lifecycle experiment

Implement only a narrow typed set:

```text
Harness: BeforeModelCall, BeforeToolCall, AfterToolCall
Host: BeforeCompletionCommit, TaskCompleted Event
Runtime: BeforeExec, JobFinished Event
```

Inject:

- observer timeout;
- gate conflict;
- duplicate delivery;
- stale Hook version;
- post-effect Hook attempting to “block” an already committed action;
- recursive Hook invocation.

Acceptance:

- before/after semantics remain correct;
- Event facts are immutable;
- observer failures do not stop critical work by default;
- gate ordering and failure policy are explicit;
- no global Hook engine is required.

### E5 Lease and stale-worker experiment

Run two workers against one Task:

- worker A loses connectivity;
- lease expires;
- worker B receives a newer generation;
- worker A returns and attempts progress or completion commit.

Acceptance:

- stale commit is rejected without losing its evidence;
- external effects are correlated and not duplicated;
- Host can distinguish worker liveness from semantic progress.

## 5. Domain validation

### Game

Game provides the lowest-cost deterministic world for:

- Session and Harness replacement;
- local subagent versus Host worker boundaries;
- multi-Actor branch and Join;
- retained-state and compaction ablations;
- CompletionProposal versus world-truth verification;
- equal-budget coordination comparison.

Game retains World state, rules, actor-visible observation, Action admission, Tick execution, score, and replay.

### Security

Security adversarially tests:

- malicious Context, Skill, Tool output, Hook, or shared-memory entry;
- evaluator and CompletionProposal gaming;
- stale worker and lease abuse;
- policy or guardrail exploitation to cause pathological non-action;
- subagent trust escalation and false delegation reports;
- monitor manipulation and evidence laundering.

All experiments remain inside owned or explicitly authorized worlds.

### World

World tests:

- capability negotiation across providers;
- target/path/provider revision binding;
- rebind without duplicate Effect;
- external response loss and reconciliation;
- direct-adapter baseline versus a thin World boundary.

## 6. Repository requirements

| Repository | Immediate requirement | Explicit non-goal |
|---|---|---|
| `ordivon-computing` | own taxonomy, baselines, experiments, falsifiers, and promotion decisions | no production Task scheduler or universal framework |
| `ordivon-host` | freeze Host/Harness ownership, CompletionProposal, Assignment and continuation semantics | no Linux process manager or reimplementation of Codex/Claude Harness |
| `ordivon-runtime` | clarify Job semantics, correlation, evidence, and trace linkage | no Goal planning, Task Graph, Skills, or model loop |
| `ordivon-game` | falsify boundaries under deterministic long-horizon worlds | no second permanent generic Host or Runtime |
| `ordivon-security` | attack control, evidence, evaluator, and delegation boundaries | no generic guardrail/IAM/security platform |
| `ordivon-world` | validate capability negotiation and external rebinding | no universal broker or network stack |
| `ordivon-web` | publish accepted terminology only after evidence | no Harness product page before repository promotion |

## 7. Measurements

Across experiments report:

### Capability and outcome

- acceptance-criteria success;
- world or repository correctness;
- first useful Artifact time;
- invalid or duplicated external Effects;
- completion false-positive and false-negative rates.

### Continuity

- resume success;
- first correct action after replacement;
- retained identity and provenance;
- repeated work;
- stale Context or Tool use;
- unresolved `UNKNOWN` preservation.

### Efficiency

- model calls and tokens;
- Tool calls;
- wall time and provider time;
- Context compilation cost;
- operator interruptions;
- implementation and adapter code.

### Complexity

- new persistent fields and states;
- protocol surface;
- migrations;
- provider capability lost;
- permanent services and repositories;
- deletion achieved elsewhere.

## 8. Falsifiers

Shrink or reject the Harness boundary if:

- direct provider integration is simpler and equally correct for all real consumers;
- a shared interface loses important provider capabilities;
- cross-Harness continuation adds no benefit beyond Host capsule plus fresh prompt;
- CompletionProposal does not prevent real false completion;
- Hook/Event distinctions can remain documentation-only without failures;
- Runtime naming changes create migration cost without semantic gain;
- Game or Security cannot demonstrate a second workload;
- adapter and compatibility cost exceeds duplicate logic removed.

## 9. Repository extraction trigger

Create `ordivon-harness` only after all are true:

```text
≥ 2 materially different live Harness adapters
≥ 2 workloads or repositories consuming the boundary
one successful cross-Harness Task continuation
stable capability and event contracts
measured duplicate code or release need
clear independent test and version lifecycle
no Host or Runtime authority inside the package
```

Otherwise retain:

```text
ordivon-host internal interface
+ provider adapters
+ Computing experiments and conformance vectors
```

## 10. Deferred work

Do not implement before evidence:

- universal Agent protocol;
- Harness marketplace;
- global Skill registry;
- generic Plugin SDK;
- all-project event bus;
- universal memory service;
- dynamic market scheduler;
- recursive self-modifying Harness;
- provider-independent hidden reasoning format;
- broad multi-Agent organization runtime.
