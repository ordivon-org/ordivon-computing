# Agent-Native Primitives

These are the current stable objects used to express persistent Agent work. The repository distinguishes **implemented Semantic Core primitives** from **future Task Runtime research objects**.

## Semantic Core primitives (implemented boundary)

```text
Effect
├── Dispatch
│   ├── Observation
│   └── Artifact
│
└── Claim
    └── Verification
        └── Fact
```

These objects define the durable semantic boundary between cognition and external world execution.

## Effect

A proposed observation or change to an external object.

```text
identity
+ target
+ preconditions
+ required capability
+ payload
+ result semantics
+ verification path
```

## Dispatch

One concrete attempt to cross the external execution boundary for an Effect. Dispatch records execution identity, backend binding, lifecycle state, and uncertainty when the external result is not immediately known.

## Observation

A structured record of external reality: command output, file digest, process state, API response, test result, sensor value, or other evidence.

The interpretation may change; the recorded Observation remains the historical input.

## Artifact

A durable content-bearing result with stable identity and provenance, such as a patch, log, dataset, report, binary, or commit.

## Claim

A statement proposed for acceptance based on observations or artifacts.

## Verification

The process and evidence relationship that evaluates whether a Claim can be accepted under current Kernel rules.

## Fact

A Claim accepted into current persistent state through a recorded Verification.

A Fact means:

```text
Claim + Verification + Evidence accepted by Kernel rules
```

It is not an unqualified assertion outside the system boundary.

## Cross-cutting primitives

These apply across Semantic Core objects:

### Identity

Stable identity for Effects, Dispatches, observations, artifacts, claims, facts, authorities, and world objects.

### Capability

```text
holder + action + object scope + lifetime
```

Capabilities describe possible world effects and execution authority.

### Workspace

A versioned operational address space where execution can read, compute, and create candidate state.

### Authority and Attestation

Authority defines who may perform a semantic operation. Attestation binds accepted mutations and evidence to identity, contract version, time, and exact content.

## Future Task Runtime objects (research)

These objects are intentionally above the current Semantic Core boundary.

```text
Goal
└── Task DAG
    └── Attempt
        └── Effect
```

Future Task Runtime research includes:

- Goal;
- Task;
- dependency graph;
- ready / blocked scheduling;
- Branch and Join;
- Checkpoint;
- multi-Agent coordination.

These objects submit Effects into Semantic Core rather than becoming part of the Kernel state machine.

## Core transition direction

```text
Goal / Task Runtime
        ↓
Effect
        ↓
Dispatch
        ↓
Observation / Artifact
        ↓
Claim
        ↓
Verification
        ↓
Fact
```

The Kernel protects the semantic boundary. Planning structures remain revisable above it.
