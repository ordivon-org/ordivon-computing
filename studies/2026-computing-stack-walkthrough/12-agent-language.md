# 12 — Agent Language and Effect IR

Natural language expresses open meaning well. Machines require explicit objects, dependencies, targets, and execution contracts. Agent Language connects the two through progressive representation.

## Representation chain

```text
Intent
→ Goal
→ Plan
→ Task Graph
→ Effect IR
→ Tool Call
→ Observation
→ Fact
```

### Intent

The human direction or preference, such as “make long tasks more recoverable.”

### Goal

A durable desired state with identity, subject, context, current status, and completion evidence.

### Plan

A revisable cognitive strategy explaining how the Goal might be advanced.

### Task Graph

Stable work units and their true dependencies. It supports scheduling, parallel execution, waiting, retry, and dynamic expansion after new observations.

### Effect IR

A concrete proposed observation or world change carrying stable identity, target, preconditions, capability, payload, declared idempotency and retry semantics, result semantics, and verification. Stable identity supports reconciliation but does not make the external operation inherently idempotent.

### Fact

A statement about current task or world state supported by observations and artifacts.

## Task and Effect

A Task expresses a semantic objective such as “validate the implementation.” Its Effects may include reading configuration, starting tests, observing a process, reading log artifacts, and recording the exact result.

Pure computation transforms values and is easy to repeat. Effects access files, services, databases, people, or devices and therefore require state and recovery semantics.

## Guards

An Effect may be compiled under assumptions:

```text
repository revision
file digest
Tool catalog revision
Workspace state
available capability
```

When a guard changes, the Runtime re-observes the world and recompiles the pending path. This is an open-world counterpart to JIT guard failure.

## Capability

A capability binds a holder, action, object scope, and lifetime. It informs planning before an Effect is generated and execution when the Effect is dispatched.

## Minimal verbs

A candidate Agent instruction set includes:

```text
OBSERVE  READ  PROPOSE  PREPARE  EXECUTE  VERIFY
COMMIT   CHECKPOINT  SPAWN  JOIN  CANCEL  EMIT
```

The exact set remains a research question. The important property is that cognition, execution, observation, and commitment become distinguishable state transitions.

## Task Capsule

A portable continuation capsule can contain the Goal, Task Graph, world bindings, capabilities, artifacts, facts, and next ready work. Another model or machine can continue without reconstructing the entire chat history.
