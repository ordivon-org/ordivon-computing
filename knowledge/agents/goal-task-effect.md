# Goal, Task, Task Attempt, Context, Action Proposal, and Effect

Agent systems often compress these objects into one prompt. They carry different identities, lifetimes, commitments, and authority.

## Goal

A Goal expresses a desired world condition and why it matters.

```text
Goal
= participant or requesting institution
+ desired condition
+ commitments, constraints, and non-goals
+ completion evidence
+ consequence relationships
```

A Goal can persist across models, sessions, Tasks, and days. It does not need to contain the full execution plan.

## Task

A Task is one durable semantic unit that advances a Goal. Its dependencies and ready frontier can change as evidence reveals the problem.

```text
Goal
├── inspect the current system
├── reproduce the failure
├── construct candidates
└── validate the accepted result
```

A Task is not identical to a process, Kubernetes Job, Temporal Workflow, model session, or Tool call. Those can implement parts of it.

## Task Attempt

A Task Attempt is one semantic exploration or execution path through a Task. It preserves a hypothesis, context binding, Action Proposals, Effects, observations, Artifacts, cost, and end state.

The Task survives a failed Task Attempt. Failure can add evidence rather than erase the path.

## Context

Context is the bounded selected view supplied to one model invocation.

```text
durable Task, world, capability, commitment, Tool, and evidence state
→ selection and compression
→ Context
```

It should retain source and revision bindings sufficient to detect staleness. Context is not the authoritative store merely because the model can see it.

## Action Proposal

An ActionProposal preserves open cognition before commitment. It may identify:

- intended observation or world change;
- target and expected state;
- rationale and expected benefit;
- preconditions and required capability;
- consequence, reversibility, and affected participants;
- candidate Tool or execution method;
- verification and recovery plan.

```text
Context
→ open ActionProposal
→ capability and Tool resolution
→ consequence analysis
→ Effect, negotiation, revision, or rejection
```

A model should not be permanently confined to selecting one of a small number of exact action identifiers. Exact CandidateAction menus remain useful for deterministic tests and narrow products, not as the universal Host cognition interface.

## Effect

An Effect is a stable semantic proposal selected for commitment to observe or change an external object. It minimally identifies:

- target and expected version;
- operation and input digest;
- preconditions;
- required authority or capability reference;
- declared idempotency behavior;
- completion semantics;
- verification and recovery path.

A stable Effect identifier supports correlation and reconciliation. It does not make an operation safe to repeat.

## Dispatch

A Dispatch is one concrete attempt to execute an Effect through a specific Tool or backend contract. A backend Job is an execution object owned by that backend.

```text
Effect
→ immutable Binding to Tool contract and request
→ Dispatch
→ Job or synchronous result
```

Response loss leaves the Dispatch outcome `UNKNOWN` until the world is re-observed.

## Capability and consequence

CapabilityProfile describes what a participant or workload may technically attempt under a declared environment. Consequence binding determines whether one proposed Effect may commit against a particular resource, world version, and affected set of participants.

```text
broad reversible exploration capability
≠
unlimited authority over shared or irreversible consequences
```

This separation allows stronger cognition and faster exploration without treating every local action as a public commitment.

## Progressive lowering

```text
participant purpose or request
→ Goal and commitments
→ dynamic Task frontier
→ Task Attempt and Context
→ candidate Claim or ActionProposal
→ capability and consequence resolution
→ Effect admission
→ Tool-bound Dispatch
→ Observation and Artifact
→ Verification and Task update
```

Natural language preserves openness. Task state preserves continuity. Context scopes one cognitive episode. ActionProposal preserves discovery. Effect and Dispatch identity bind selected cognition to external reality.

## Design rule

Do not promote a field, gate, or approval to a shared primitive merely because one product needs it. It must protect a specific failure across materially different workloads, remain stable across model and provider change, and create more verification, recovery, or consequence reduction than latency, friction, compatibility burden, and cognitive compression.

See [`task-context-authority-effect-evidence.md`](task-context-authority-effect-evidence.md) and [`../../core/primitives.md`](../../core/primitives.md).
