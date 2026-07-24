# Agent-Native Primitives

These are the minimum current objects for expressing persistent Agent work. Domain systems may add richer objects, but these relationships provide the shared substrate.

## Object model

```text
Goal
└── Task
    └── Attempt
        └── Effect
            ├── Observation
            ├── Artifact
            └── Fact
```

A **Workspace** binds an Attempt to a versioned operational state. A **Capability** binds an actor to possible Effects. A **Checkpoint** preserves the minimum sufficient continuation state.

## Goal

A durable desired world state. A Goal carries identity, subject, context, current state, and completion evidence.

```text
Goal = desired state + context + continuity
```

## Task

A schedulable semantic unit that advances a Goal. Tasks form a dynamically growing dependency graph and move through states such as pending, ready, running, waiting, completed, failed, and cancelled.

## Attempt

One concrete exploration or execution path for a Task. Attempts preserve hypotheses, Effects, errors, observations, and reusable results so that later Attempts begin from accumulated information.

## Effect

A proposed observation or change to an external object. An Effect minimally carries:

```text
identity
+ target
+ preconditions
+ required capability
+ payload
+ result semantics
+ verification path
```

## Observation

A structured reading of external reality: command output, file digest, process state, API response, test result, sensor value, or other environment evidence. Interpretation may change; the Observation remains the recorded input.

## Artifact

A durable content-bearing result with stable identity and provenance, such as a patch, log, dataset, report, binary, plan, task graph, or commit.

## Fact

A task-relevant statement supported by observations or artifacts and accepted into current persistent state, such as an exact repository revision or a verified test result.

## Workspace

A versioned operational address space in which an Attempt can read, compute, and create candidate state. Workspaces support isolation, comparison, branching, integration, and recovery.

## Capability

A task-bound expression of possible world effects:

```text
holder + action + object scope + lifetime
```

Capabilities are planning inputs as well as execution authority.

## Checkpoint

The minimum sufficient state for another model, process, session, or machine to continue work:

```text
Goal
+ active Tasks and Attempts
+ world bindings
+ verified Facts
+ relevant Artifacts
+ next ready work
```

## Core transitions

```text
Intent
→ Goal
→ Plan
→ Task Graph
→ Effect
→ Tool Action
→ Observation
→ Verification
→ Fact / Artifact
→ Goal update
```

Execution is progressive rather than monolithic. Stable facts persist; plans and attempts remain revisable.

## Minimal execution verbs

A compact semantic instruction set can begin with:

```text
OBSERVE  READ  PROPOSE  PREPARE  EXECUTE  VERIFY
COMMIT   CHECKPOINT  SPAWN  JOIN  CANCEL  EMIT
```

These verbs are research candidates rather than a frozen instruction set. Their purpose is to make the transition from open cognition to persistent world state explicit and composable.
