# Agent-Native Primitives

This file separates the primitives already enforced by the executable Semantic Core from higher-level objects that remain research candidates for a future Task Runtime.

The boundary matters:

```text
Future Task Runtime
Goal / Task / Attempt / Branch / Join / Checkpoint
                    ↓ submits Effects
Executable Semantic Core
Effect / Dispatch / Evidence / Verification / Authority / Replay
                    ↓ binds through Adapters
Classical substrates and external systems
Workspace / Job / Tool contract / process / file / network
```

A concept belongs in the Semantic Core only when external Agent action requires a stable, non-bypassable invariant that lower layers do not already provide.

## Executable Kernel primitives

These objects are implemented in `research/experiments/semantic-core-v0` and covered by K1–K10 conformance.

### WorldObjectRef

A stable external object identity with an optional observed or expected version.

```text
object identity + version binding
```

It may refer to a repository, Workspace, file, process, Artifact, API object, or another externally observable target. The concrete backend representation remains below the Kernel.

### Effect

A stable semantic proposal to observe or change a WorldObject.

```text
identity
+ target
+ mode
+ operation semantics
+ preconditions
+ required capability
+ input digest
+ idempotency semantics
+ completion semantics
+ verification plan
```

An Effect describes why and what should happen. It is not one concrete Tool call.

### Dispatch

One concrete attempt to cross the external world boundary for an Effect.

```text
EffectId
+ DispatchId
+ request digest
+ backend binding
+ attempt state
```

Effect identity remains stable across recovery. Dispatch identity distinguishes separate attempts. A backend Job or synchronous receipt binds to a Dispatch rather than replacing it.

### EffectEvent

One ordered, attested transition in an Effect history. Each Effect has a local event sequence; the durable Journal supplies a global append-only command sequence.

### Observation

An immutable, attested reading of external reality, such as file content and digest, process state, command output, API response, test result, or sensor value.

Interpretation may change. The recorded Observation and its provenance do not.

### Artifact

A durable content-bearing result with stable identity, digest, Effect and Dispatch provenance, such as a patch, log, dataset, report, binary, or execution result.

### Claim

A proposition about a WorldObject proposed for evidence-based evaluation.

### Verification

A recorded decision that evaluates one Claim under a declared method and one or more Evidence references.

```text
Claim
+ method
+ Observation / Artifact evidence
+ decision
+ Verification authority
```

A multi-evidence Verification is the current limited hyperedge: several evidence objects jointly support one decision without requiring a general Hypergraph runtime.

### Fact

A Claim accepted through a recorded Verification and Fact authority.

```text
Claim → Verification → Fact
```

Tool success, process exit, Observation, Artifact, or model assertion does not bypass this chain.

### AuthorityRef

A signed role grant binding issuer, principal, role, trust domain, policy version, and key identity.

Current roles separate Effect proposal, Dispatch execution, Observation production, Verification decision, and Fact acceptance.

### Attestation

A signed binding between one Authority, an exact semantic operation or evidence object, its contract version, content digest, and record time.

### Semantic Journal

The append-only, hash-linked command history from which the complete Kernel projection and Authority provenance can be authenticated and replayed after process loss.

## Backend and host objects

These objects are essential to real execution but are not universal Semantic Core primitives.

### Workspace

A versioned operational address space supplied by a host or backend. Ordivon Workspaces provide isolation, exact repository binding, mutation, comparison, and recovery.

### Job and Attempt

A backend Job is a concrete runtime execution entity. A broader Task Attempt may contain multiple Effects and Dispatches. Neither is identical to an Effect.

### ToolContract and EffectBinding

A ToolContract describes one executable interface revision. An EffectBinding maps a stable Effect to one ToolContract revision and normalized request digest. These are the joint research target of ANC-IR-001 and ANC-EFFECT-001, not frozen Kernel objects yet.

### Capability

Capability spans planning and enforcement:

```text
holder + action + object scope + lifetime
```

The current Kernel enforces semantic Authority roles and records a capability reference on Effects. A complete delegated capability system remains above or beside the Kernel.

## Future Task Runtime candidates

The following objects belong to the future coordination layer that submits Effects to the Semantic Core. They are not implemented Kernel guarantees.

### Goal

A durable desired world state carrying identity, context, current evidence, and completion criteria.

### Task

A schedulable semantic unit that advances a Goal. Tasks form a dynamically growing partial order with states such as pending, ready, running, waiting, completed, failed, and cancelled.

### Attempt

One exploration or execution path for a Task. An Attempt may preserve hypotheses, Effects, errors, observations, and reusable results across interruption.

### Branch

An independently executable Task subgraph with explicit inputs, world bindings, capabilities, and expected outputs.

### Join

A node that consumes multiple Artifacts, verified Facts, or completed predecessor Tasks before producing an integrated result. Join semantics may later use limited hyperedges or Petri-Net analysis when real concurrency requires them.

### Checkpoint

The minimum sufficient continuation Artifact for another model, process, session, or machine:

```text
Goal
+ active Task partial order
+ Attempts
+ world bindings
+ verified Facts
+ relevant Artifacts
+ repository and contract revision set
+ next ready work
```

## Layered object model

```text
Goal
└── Task partial order
    ├── Attempt / Branch
    │   └── Effect
    │       └── Dispatch
    │           ├── Observation
    │           └── Artifact
    └── Join
        └── consumes Artifacts and verified Facts

Claim
└── Verification
    ├── Observation evidence
    └── Artifact evidence
        ↓
       Fact
```

The Task layer may grow and revise its graph. The Semantic Core preserves each selected Effect path through linear admission, external execution, evidence, Verification, and durable commit.

## Structural rule

Use the smallest sufficient structure for each problem:

```text
fact history             append-only sequence
Effect / Dispatch life   state graph
Task readiness           DAG / partial order
Evidence provenance      typed DAG with limited multi-input edges
cross-project research   typed directed multigraph
system evolution         feedback loop
```

Global planning is a graph. One selected local execution remains a bounded path:

```text
observe → decide → mutate → verify → commit
```
