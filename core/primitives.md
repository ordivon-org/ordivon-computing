# Agent-Native Primitives and Responsibility Boundaries

This file distinguishes classical backend objects, executable Semantic Core primitives, Host-proven work objects, and research candidates. Similar names do not imply shared authority.

```text
Open-work and context layer
Goal / Task / Attempt / Context / Branch / Join / Decision
                         ↓ proposes
Semantic commitment layer
Authority / Effect / Binding / Dispatch / Observation / Artifact
Claim / Verification / Fact / durable replay
                         ↓ adapts to
Classical substrate
Workspace / process / Job / transaction / file / network / Tool
```

A concept belongs in a shared Agent-native layer only when external probabilistic action requires a stable, non-bypassable invariant that lower mechanisms do not already own.

## 1. Classical backend objects

These are essential but are not universal Agent-native primitives.

### Workspace

A version-bound operational address space supplied by a Host or backend. A Git worktree can isolate candidate source state from another candidate. It is not by itself a security sandbox.

### Process and Job

A process is an operating-system execution object. A backend Job is a durable execution-control object. Either may implement one part of a Task Attempt; neither owns the human Goal or open-work semantics.

### Transaction and durable workflow

Databases own atomic state updates. Durable workflow systems own replay and continuation of declared workflow logic. Agent layers may use both without claiming their mechanisms as new.

### Tool

A Tool is an executable interface. Tool availability or process credentials establish possible reach, not semantic authorization for every generated call.

## 2. Executable Semantic Core primitives

The following objects are implemented in `research/experiments/semantic-core-v0` and protected by its conformance suite.

### WorldObjectRef

A stable external object identity with an optional observed or expected version.

```text
object identity + version binding
```

Concrete repository, file, process, API, account, or simulator representations remain backend concerns.

### Effect

A stable semantic proposal to observe or change a WorldObject.

```text
identity
+ target and expected version
+ mode and operation semantics
+ preconditions
+ required authority or capability reference
+ input digest
+ declared idempotency behavior
+ completion semantics
+ verification plan
```

Effect identity makes intent recoverable. It does not make the external operation inherently idempotent.

### Dispatch

One concrete attempt to cross the external boundary for an Effect.

```text
EffectId
+ DispatchId
+ request digest
+ backend binding
+ attempt state
```

Effect identity remains stable across recovery. Dispatch identity distinguishes physical attempts. A backend Job or synchronous receipt binds to a Dispatch rather than replacing it.

### EffectEvent

One ordered, attested transition in an Effect history. The durable Journal provides a global append-only semantic command sequence.

### Observation

An immutable, attested reading of external reality, such as content and digest, process state, command output, API response, test result, or sensor value.

Interpretation may change. Recorded content and provenance do not.

### Artifact

A durable content-bearing output with stable identity, digest, and Effect or Dispatch provenance, such as a patch, log, dataset, report, binary, or execution result.

### Claim

A proposition about a WorldObject proposed for evidence-based evaluation. A model output may create a Claim; it does not automatically create a Fact.

### Verification

A recorded decision that evaluates one Claim under a declared method and one or more evidence references.

```text
Claim
+ method
+ Observation / Artifact evidence
+ decision
+ Verification authority
```

Domain policy determines what methods and evidence are sufficient.

### Fact

A Claim admitted through a recorded Verification and Fact authority for a bounded domain and world version.

```text
Claim → Verification → Fact
```

Facts may later be invalidated or superseded by world drift or stronger evidence.

### AuthorityRef

A signed role grant binding issuer, principal, role, trust domain, policy version, and key identity. Current Semantic Core roles separate Effect proposal, Dispatch execution, Observation production, Verification decision, and Fact acceptance.

A complete purpose- and consequence-bound capability system remains a research target above or beside the Core.

### Attestation

A signed binding among one Authority, an exact semantic operation or evidence object, contract version, content digest, and record time.

### Semantic Journal

The append-only, hash-linked command history from which Kernel projections and authority provenance can be authenticated and replayed after process loss. SQLite owns durable byte transactions; the Semantic Journal owns command meaning and replay invariants.

## 3. Promoted protocol objects

These objects are implemented in `packages/ordivon-protocol/` and directly consumed by Ordivon Host.

### ToolContract

A normalized description of one executable interface revision, including the shape needed to detect material contract change.

### EffectBinding

An immutable mapping from one stable Effect to one ToolContract revision and normalized request digest.

```text
Effect semantics
+ exact Tool contract revision
+ normalized request
→ immutable Binding
```

The Binding does not authorize the Effect or prove that execution occurred.

### EffectEnvelope and SourceChangeSpec

Public production-candidate representations for selected stable Effect semantics. Their existence does not require every domain project to use the same internal object model.

## 4. Host-proven open-work objects

Ordivon Host implements these objects for bounded vertical slices. They are real product objects but not yet universal shared-kernel guarantees.

### Goal

A durable desired world condition with identity, constraints, current evidence, and completion criteria.

### Task

A persistent semantic work unit that advances a Goal and carries current state, frontier, and outcome. A Task can outlive model sessions, Host processes, Runtime Jobs, and failed Attempts.

### Attempt

One exploration or execution path for a Task. It may preserve hypotheses, model invocations, Effects, errors, Observations, and reusable Artifacts.

### Context

A bounded selected view of task, policy, Tool, evidence, and world state supplied to one model invocation. Context is derived from durable state and must not become its hidden replacement.

## 5. Research candidates

These objects require further cross-domain evidence before promotion.

### Branch and Join

A Branch is an independently executable Task subgraph with explicit inputs, world bindings, authority, and expected outputs. A Join consumes multiple Artifacts, verified Facts, or predecessor Tasks under a declared integration rule.

### Checkpoint

The minimum sufficient continuation record for another model, Host, process, or machine:

```text
Goal
+ active Task frontier and Attempts
+ relevant world and contract revisions
+ explicit uncertainty and blockers
+ verified Facts and Claims still under evaluation
+ relevant Artifacts
+ next admissible work
```

The minimum schema remains an experimental question.

### ContextSelection

A reproducible or explainable binding between durable sources and one invocation context, including source revisions, selection method, omissions or compression, and invalidation conditions.

### ConsequenceEnvelope

A bounded description of the maximum allowed external consequence for delegated work. Security and Finance provide strong domain evidence, but no universal enforcement contract is yet promoted.

### DecisionRequest

A structured escalation to the human consequence owner with reason, alternatives, evidence, reversibility, cost of delay, and permitted responses. No current Ordivon product owns a complete operator decision plane.

## 6. Combined object model

```text
Goal
└── Task frontier
    ├── Attempt / Branch
    │   ├── Context → model invocation → candidate Claim or Effect
    │   └── Effect
    │       └── EffectBinding
    │           └── Dispatch
    │               ├── backend Job or synchronous receipt
    │               ├── Observation
    │               └── Artifact
    └── Join
        └── consumes Artifacts, Verifications, or Facts

Claim
└── Verification
    ├── Observation evidence
    └── Artifact evidence
        ↓
       Fact
```

The open-work layer may revise its graph. The commitment layer preserves each selected Effect path through admission, execution, evidence, and durable semantic history.

## 7. Structural rule

Use the smallest sufficient structure:

```text
physical execution             process / Job / transaction
Effect and Dispatch lifecycle  state graph
Task readiness                 partial order or dynamic DAG
Evidence provenance            typed DAG with bounded multi-input relations
cross-project research         typed directed multigraph
system evolution               feedback loop
```

One local commitment remains a bounded path:

```text
bind world
→ admit authority
→ dispatch
→ observe
→ verify
→ update work
```
