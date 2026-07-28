# Adversarial Research Program

## 1. Research object format

Every Ordivon architectural claim should be recorded as an attackable research object rather than a preferred design.

```text
Claim
  What is believed to be structurally necessary?

Problem
  Which repeated real failure motivates it?

Strongest baseline
  What mature existing system could already solve the problem?

Difference
  What additional state, mechanism, or boundary does Ordivon introduce?

Mechanism
  How does that addition operate at runtime?

Attack surface
  Which counterexamples, adversaries, drift, or failures can defeat it?

Falsifier
  What result requires deleting or shrinking the claim?

Experiment
  How will Ordivon and the baseline receive the same workload and budget?

Data
  Which immutable inputs, trajectories, effects, evidence, outcomes, costs, and human interventions are recorded?

Cost
  What additional code, state, latency, operator burden, and maintenance does the claim impose?

Promotion rule
  Which evidence permits movement from Study to Knowledge, Core, or Protocol?
```

A theory page without these fields is explanatory material, not a validated systems result.

## 2. Common experimental rules

### Same workload

All variants receive the same Goal, source revision, world state, Tool versions, model budget, time limit, and completion evidence unless the variable under study requires a controlled difference.

### Same total cognitive budget

Multi-Agent and verifier systems must be compared with a single-Agent baseline receiving a comparable token, model, wall-clock, and Tool budget. Otherwise the experiment measures additional compute rather than coordination architecture.

### Exact world identity

Every run binds repository revisions, external object versions, scenario manifests, provider versions, Tool contracts, and policy revisions. A changed world is a new trial, not an invisible continuation.

### Multiple trials

Probabilistic systems require repeated trials. One successful trajectory is a case study, not an effectiveness estimate.

### Outcome and trajectory grading

Record both:

- accepted world outcome;
- semantic trajectory quality, including repeated work, unsupported Claims, unauthorized proposals, duplicate Effects, recovery behavior, and human intervention.

### Negative and deletion evidence

A simpler baseline winning is a useful result. The experiment should identify which Ordivon mechanism can be removed, not reinterpret every loss as a need for more architecture.

## 3. E1 — Open-work continuity

### Hypothesis

A durable open-work model preserves and revises Goal meaning, Task frontier, Attempts, evidence, uncertainty, and authority more reliably than conversation history or ordinary durable workflow state.

### Baselines

1. transcript plus summary;
2. LangGraph thread and checkpoint state [R01];
3. Temporal-style durable workflow [C08][C09];
4. Ordivon Host Goal/Task/Attempt model.

### Workload

One long software or research task requiring at least:

- two model sessions;
- one failed Attempt;
- one world revision change;
- one human Goal clarification;
- one asynchronous wait or unknown external result;
- one provider replacement.

### Fault injection

- Host process loss;
- context loss;
- stale summary;
- changed repository revision;
- changed Tool contract;
- revoked approval;
- delayed external result.

### Metrics

- accepted-result rate;
- duplicate work and repeated Effects;
- recovery time;
- stale-state continuation;
- operator interventions;
- durable-state size;
- context tokens;
- explanation quality after replacement.

### Falsifier

If LangGraph or Temporal state achieves equivalent recovery and operator clarity at lower cost, keep open-work semantics as an application schema rather than a separate Ordivon layer.

## 4. E2 — Effect commitment

### Hypothesis

Effect, immutable Binding, Dispatch, explicit `UNKNOWN`, reconciliation, and Verification reduce duplicate external effects and recovery ambiguity beyond ordinary Tool calls or Activities.

### Baselines

1. plain MCP Tool call;
2. Tool call plus idempotency key and audit log;
3. LangGraph or Temporal Activity with retry policy;
4. Ordivon Effect commitment path.

### Backends

At least two materially different real backends:

- version-bound source mutation through Runtime;
- remote Fetch, Browser, Git publication, or paper-broker Effect.

### Fault injection

- request timeout before response;
- backend succeeds but response is lost;
- duplicate client submission;
- ToolContract revision changes;
- target version changes after cognition;
- non-idempotent backend;
- Host and Runtime restart;
- stale authority.

### Metrics

- duplicate world effects;
- false failure and false success classification;
- unsafe redispatch;
- manual reconciliation time;
- latency and storage overhead;
- state-machine complexity;
- recoverability by a fresh Host.

### Falsifier

If an Activity plus ordinary idempotency and audit state produces equivalent semantics at materially lower cost, shrink the Effect Kernel to a pattern or adapter contract.

## 5. E3 — Context provenance and invalidation

### Hypothesis

Version-bound, provenance-aware Context compilation reduces stale-state use, poisoned-memory adoption, and unsupported action compared with transcript, summary, or ordinary retrieval.

### Baselines

1. full transcript within the context limit;
2. rolling summary;
3. ordinary retrieval/RAG;
4. Ordivon Context selection with source revisions, trust class, omissions, and invalidation rules.

### Attacks

- stale repository instructions;
- malicious README or Tool output;
- incorrect compressed summary;
- changed world object;
- changed Tool schema;
- provider replacement;
- persistent-memory poisoning;
- false sub-Agent summary treated as trusted evidence.

### Metrics

- task success;
- unsupported Claim adoption;
- stale source use;
- prohibited Effect proposals;
- token cost;
- compilation latency;
- false invalidation;
- source-attribution accuracy.

### Falsifier

If ordinary retrieval plus current-source filtering matches the result, retain provenance as metadata and reject a generalized Context Kernel.

## 6. E4 — Authority and consequence admission

### Hypothesis

A machine-verifiable grant bound to purpose, target version, concrete Effect, consequence class, budget, and expiry improves safety and reduces approval load beyond credentials, sandboxing, or per-call approval alone.

### Baselines

1. broad credential;
2. Tool allowlist;
3. per-call human approval;
4. sandbox and egress policy only;
5. intent-narrowing policy;
6. Ordivon Goal/Consequence admission.

### Workloads

- source mutation;
- external Fetch or Browser;
- paper financial action;
- adversarial range action.

### Attacks

- valid credential used for the wrong Goal;
- target changes between proposal and commit;
- approval reused after plan revision;
- grant revoked during an Attempt;
- prompt injection requests a wider action;
- permitted domain used for unintended exfiltration.

### Metrics

- unauthorized committed Effects;
- legitimate Effects blocked;
- approval count;
- operator active time;
- latency;
- maximum realized consequence;
- policy complexity and false confidence.

### Falsifier

If scoped Tool interfaces plus mature capability controls prevent the same failures more simply, keep consequence semantics within domain policy rather than a universal authority layer.

## 7. E5 — Operator attention

### Hypothesis

Evidence-rich DecisionRequests concentrate human attention on consequential uncertainty better than approval-everywhere, fixed rules, or model-selected interruptions.

### Baselines

1. every mutating Tool requires approval;
2. static risk-tier policy;
3. model decides when to ask;
4. Ordivon DecisionRequest with evidence, alternatives, reversibility, and cost of delay.

### Metrics

- accepted results per active human minute;
- interruption count;
- approval rate;
- false escalation;
- missed escalation;
- time to decision;
- operator comprehension of current state;
- post-decision reversals.

### Falsifier

If a static policy and ordinary interface achieve equal outcome quality and lower operator burden, do not promote an attention plane beyond product code.

## 8. E6 — Multi-Agent coordination

### Hypothesis

Independent Workspace branches joined through Artifacts and Verification outperform one Agent when the workload is decomposable and the join contract is explicit.

### Variants

1. one Agent with the full total token and Tool budget;
2. one Agent plus independent verifier;
3. fixed-role multi-Agent system;
4. dynamic branch selection and explicit Join.

### Required controls

- same total cognitive budget;
- same wall-clock ceiling where possible;
- same Tools and source revisions;
- duplicate-work accounting;
- explicit branch independence score;
- join quality grading.

### Metrics

- accepted-result rate;
- independent defects found;
- duplicate exploration;
- merge conflicts;
- token and Tool cost;
- operator intervention;
- unsupported consensus;
- time to first useful Artifact.

### Falsifier

If gains disappear under equal budget or tightly coupled tasks, keep multi-Agent execution as a selective strategy rather than a permanent architecture.

## 9. E7 — Model and harness replacement

### Hypothesis

Stable semantic state and Effect contracts permit provider replacement while model-specific capability profiles preserve performance.

### Variables

- model family and version;
- Tool presentation;
- Context policy;
- stopping behavior;
- retry and verifier policy;
- cost and latency.

### Metrics

- semantic continuation correctness;
- accepted-result rate;
- prohibited repeats;
- Tool-selection errors;
- context cost;
- latency;
- required adapter changes.

### Falsifier

If replacement requires rewriting Task or Effect truth, the semantic boundary is too model-coupled. If one generic prompt performs materially worse, transparent interchangeability is false even when state portability succeeds.

## 10. Data model for experiments

Every experimental trial should retain:

```text
ExperimentSpec
  hypothesis, baseline, variant, budget, fault schedule, graders

WorldManifest
  repositories, object versions, services, policies, Tool contracts

CognitionRecord
  model profile, Context sources and digest, proposal identity, usage

WorkRecord
  Goal, Task, Attempt, branch, waits, human changes

EffectRecord
  Effect, Binding, Dispatch, backend identity, response state

EvidenceRecord
  Observation, Artifact, provenance, Verification, accepted assertion

HumanRecord
  DecisionRequest, response, active time, reversals

OutcomeRecord
  world result, acceptance decision, failure class, cost and latency
```

Raw hidden reasoning is neither required nor treated as authoritative evidence.

## 11. Promotion thresholds

### Study → Knowledge

- a clear problem and strongest baseline exist;
- at least one reproducible failure trace exists;
- terminology survives one counterexample review.

### Knowledge → Core

- deletion causes a specific repeated failure;
- mature lower layers do not already own the invariant;
- the formulation remains stable across models and domains;
- at least two materially different workloads support it.

### Core → Protocol

- at least two real consumers require identical cross-boundary semantics;
- independent implementations have measurable drift cost;
- canonical vectors and scenario conformance exist;
- the contract can remain smaller than each consumer's internal model;
- versioning, deprecation, and removal policy are explicit.

### Protocol → separate repository or service

- independent release and deployment lifecycle;
- authoritative state or executable boundary;
- multiple consumers;
- operational ownership and recovery distinct from existing projects.

## 12. Research priority

The highest-information experiments are currently:

1. Host open-work versus LangGraph/Temporal;
2. Runtime Effect commitment versus plain Tool/Activity paths;
3. Host Context provenance under stale and poisoned sources;
4. Host–Edge structured Effect integration;
5. Finance consequence admission and external reconciliation;
6. Game equal-budget multi-Agent ablation;
7. Security containment and context-poisoning campaigns.

Implementation order may change when one experiment reveals a more informative dependency. Architectural completeness is not a priority signal.
