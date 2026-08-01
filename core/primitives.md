# Agent-Native Primitives and Responsibility Boundaries

This file distinguishes classical backend objects, executable Semantic Core primitives, Host-proven work objects, and research candidates. Similar names do not imply shared authority or permanent hierarchy.

```text
Participation and open-work layer
Participant / Goal / Task / Task Attempt / Context / Branch / Join / DecisionRequest
                                  ↓ proposes or negotiates
Proposal and semantic commitment layer
ActionProposal / CapabilityProfile / Authority / Effect / Binding / Dispatch
Observation / Artifact / Claim / Verification / Fact / durable replay
                                  ↓ adapts to
Classical substrate
Workspace / process / Job / transaction / file / network / Tool
```

A concept belongs in a shared Agent-native layer only when persistent probabilistic action requires a stable, non-bypassable invariant that lower mechanisms do not already own and the abstraction produces net acceleration after its costs are counted.

## 1. Classical backend objects

These are essential but are not universal Agent-native primitives.

### Workspace

A version-bound operational address space supplied by a Host or backend. A Git worktree can isolate candidate source state from another candidate. It is not by itself a security sandbox.

### Process and Job

A process is an operating-system execution object. A backend Job is a durable execution-control object. Either may implement one part of a Task Attempt; neither owns the originating participant, Goal, commitment, or open-work semantics.

### Transaction and durable workflow

Databases own atomic state updates. Durable workflow systems own replay and continuation of declared workflow logic. Agent layers may use both without claiming their mechanisms as new.

### Tool

A Tool is an executable interface. Tool availability or process credentials establish possible physical reach, not the right to use another participant’s resources or commit every generated action.

## 2. Executable Semantic Core primitives

The following objects are implemented in `research/experiments/semantic-core-v0` and protected by its conformance suite. The experiment is closed reference evidence. Its historical migration and compatibility paths are not automatically permanent product obligations.

### WorldObjectRef

A stable external object identity with an optional observed or expected version.

```text
object identity + version binding
```

Concrete repository, file, process, API, account, or simulator representations remain backend concerns.

### Effect

A stable semantic proposal selected for commitment to observe or change a WorldObject.

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

An Effect is downstream of open cognition: a model may first produce an ActionProposal that Host or domain code resolves into an executable Effect. Effect identity makes selected intent recoverable. It does not make the external operation inherently idempotent.

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

One ordered, attested transition in an Effect history. The durable Journal provides a global append-only semantic command sequence for the reference experiment.

### Observation

An immutable, attested reading of external reality, such as content and digest, process state, command output, API response, test result, or sensor value.

Interpretation may change. Recorded content and provenance do not.

### Artifact

A durable content-bearing output with stable identity, digest, and Effect or Dispatch provenance, such as a patch, log, dataset, report, binary, or execution result.

### Claim

A proposition about a WorldObject proposed for evidence-based evaluation. A model output, human statement, or institutional assertion may create a Claim; none automatically creates a Fact.

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

A signed role grant binding issuer, principal or participant, role, trust domain, policy version, and key identity. Current Semantic Core roles separate Effect proposal, Dispatch execution, Observation production, Verification decision, and Fact acceptance.

Authority is relational and scoped. It is not proof of moral superiority, consciousness, or permanent ownership.

### Attestation

A signed binding among one Authority, an exact semantic operation or evidence object, contract version, content digest, and record time.

### Semantic Journal

The append-only, hash-linked command history from which Kernel projections and authority provenance can be authenticated and replayed after process loss. SQLite owns durable byte transactions; the Semantic Journal owns command meaning and replay invariants for the reference experiment.

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

A durable desired world condition with identity, originating or accepting participants, constraints, current evidence, and completion criteria.

### Task

A persistent semantic work unit that advances a Goal and carries current state, frontier, and outcome. A Task can outlive model sessions, Host processes, Runtime Jobs, and failed Task Attempts.

### Task Attempt

One semantic exploration or execution path for a Task. It may preserve hypotheses, model invocations, Effects, errors, Observations, and reusable Artifacts.

### Context

A bounded selected view of task, capability, policy, Tool, evidence, commitment, and world state supplied to one model invocation. Context is derived from durable state and must not become its hidden replacement.

### Bounded CandidateAction admission

The current Host can compile two to eight exact CandidateActions and require a model to select one. This proves context identity, stale-world rejection, provider replacement, and deterministic admission for narrow vertical slices.

It is not the universal cognition contract. A permanent Host must also support open ActionProposal lowering so stronger cognition can discover new actions, decompositions, Tools, subgoals, and verification paths without being confined to a pre-enumerated menu.

## 5. Research candidates

These objects require further cross-domain evidence before promotion.

### ParticipantRef and Commitment

A ParticipantRef identifies an actor in a domain without asserting consciousness or legal personhood. A Commitment binds one or more participants to a Goal, resource, promise, responsibility, refusal, or exit condition under a domain contract.

Current products should use the smallest local representation until at least two materially different domains demonstrate shared semantics.

### ActionProposal

An open cognitive proposal that may describe a target, intended change or observation, rationale, preconditions, expected consequence, reversibility, required capability, candidate Tool or method, and verification plan.

```text
Context
→ ActionProposal
→ Tool and capability resolution
→ consequence analysis
→ Effect compilation, negotiation, revision, or rejection
```

An ActionProposal is not authorized merely because a model produced it. Its purpose is to preserve open cognition before deterministic commitment, rather than forcing cognition to choose only from exact prebuilt action identifiers.

### CapabilityProfile

A declared capability mode for a participant or workload. It may distinguish broad owner-trusted private exploration from public, multi-tenant, hostile, or high-consequence execution. CapabilityProfile should reduce repeated per-action friction without erasing resource ownership or consequence boundaries.

### Branch and Join

A Branch is an independently executable Task subgraph with explicit inputs, world bindings, capability, and expected outputs. A Join consumes multiple Artifacts, verified Facts, or predecessor Tasks under a declared integration rule.

### Checkpoint

The minimum sufficient continuation record for another model, Host, process, or machine:

```text
Goal and commitments
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

A bounded description of the maximum allowed external consequence for delegated or autonomous work. Security and Game provide strong domain evidence, but no universal enforcement contract is yet promoted.

### DecisionRequest

A structured request to the participant or institution responsible for a missing commitment, resource, consequence, or unresolved conflict. It should carry reason, alternatives, evidence, reversibility, cost of delay, and permitted responses.

The receiver may be a person, organization, resource owner, verifier, team role, another Agent, or future artificial participant. Escalation is routing to the correct responsibility owner, not a universal synonym for asking a human.

### Refusal and Exit

A participant may need to refuse a proposed commitment, revoke delegation, leave a collaboration, or terminate a relationship under declared consequences. No universal protocol is promoted, but architecture must not assume permanent obedience or ownership as the only coordination model.

## 6. Combined object model

```text
Participant / institution / resource owner
└── Goal and Commitments
    └── Task frontier
        ├── Task Attempt / Branch
        │   ├── Context → model invocation → Claim or ActionProposal
        │   └── ActionProposal
        │       └── Effect compilation or DecisionRequest
        │           └── Effect
        │               └── EffectBinding
        │                   └── Dispatch
        │                       ├── backend Job or synchronous receipt
        │                       ├── Observation
        │                       └── Artifact
        └── Join
            └── consumes Artifacts, Verifications, or Facts

Claim
└── Verification
    ├── Observation evidence
    └── Artifact evidence
        ↓
       Fact
```

The open-work layer may revise its graph and negotiate commitments. The commitment layer preserves each selected Effect path through admission, execution, evidence, and durable semantic history.

## 7. Structural rule

Use the smallest sufficient structure:

```text
physical execution             process / Job / transaction
reversible exploration         Workspace / Branch / disposable environment
open cognition                 ActionProposal / Claim
Effect and Dispatch lifecycle  state graph
Task readiness                 partial order or dynamic DAG
Evidence provenance            typed DAG with bounded multi-input relations
participant commitments        domain-scoped relation or state machine
cross-project research         typed directed multigraph
system evolution               feedback loop
```

One local commitment remains a bounded path:

```text
propose
→ bind world, capability, and consequence
→ admit or negotiate commitment
→ dispatch
→ observe
→ verify
→ update work and participant state
```

## 8. Constraint admission rule

A persistent field, state, approval, compatibility layer, policy, test gate, evidence process, or shared object is not justified by caution or prior existence. At admission and re-audit it begins in the active-removal candidate set. Retention must identify its current consumer, protected capability or failure, evidence, operating cost, narrower alternatives, and review trigger. The disposition is `retain`, `localize`, `archive`, or `delete`; uncertainty favors reversible removal or archive. Historical proof may remain in Git, receipts, or a closed experiment without remaining executable in every active path.
