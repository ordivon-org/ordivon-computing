# Classical Substrate and Agent-Native Overlay

## Precise distinction

Classical computing is not perfectly deterministic. It contains concurrency, failure, nondeterministic scheduling, networks, and random input. Its defining engineering advantage is narrower: software authors declare operational objects and legal transitions, then the substrate executes, persists, isolates, or reconciles them under explicit contracts.

Examples include:

- Linux processes, threads, scheduling, namespaces, and files;
- database transactions and crash recovery;
- Git content identity and revision history;
- Kubernetes Jobs and controllers;
- Temporal durable Workflows;
- compilers, test runners, network protocols, and model-serving systems.

An Agent system should inherit these mechanisms rather than rename them.

## What changes

A foundation model moves part of semantic program construction into runtime. It receives selected context and produces a statistically generated proposal whose path was not completely encoded when the surrounding application was deployed.

```text
open human goal
→ selected context
→ probabilistic proposal
→ deterministic admission
→ classical execution
→ evidence
→ revised work
```

The new responsibility lies around the proposal and its durable consequence:

- preserving open work across replaceable model episodes;
- compiling bounded context from authoritative state;
- treating model output as a candidate rather than a fact or command;
- binding authority to purpose, target, version, budget, and consequence;
- preserving Effect identity separately from physical Dispatch;
- distinguishing Observation, Claim, Verification, and Fact;
- escalating only meaningful decisions to the human consequence owner.

## Five outcomes

When examining a classical layer, classify the change precisely:

1. **unchanged** — the existing mechanism remains sufficient;
2. **amplified** — Agent scale increases its importance or load;
3. **composed** — a product combines existing mechanisms;
4. **rewritten** — an existing abstraction needs a materially different contract;
5. **new responsibility** — no lower layer owns a required invariant.

Only the last two justify an Agent-native Core abstraction.

## Durable workflows are the strongest counterexample

Kubernetes Jobs and Temporal Workflows already prove that work can survive process and machine failure. Therefore generic Job identity, retries, event history, and replay are not Agent-native inventions.

The narrower Agent problem is continuity of work whose decomposition and completion evidence change after model-generated investigation:

```text
durable workflow
  preserves declared control logic

open-work continuity
  preserves and revises Goal meaning, hypotheses,
  task frontier, uncertainty, authority, and evidence
```

If a conventional durable workflow can express a workload without losing these semantics, Ordivon should reuse it.

## Boundary rule

A new Ordivon layer or repository requires:

- a real repeated failure;
- an invariant not already owned by a mature substrate;
- a non-bypassable enforcement or evidence boundary;
- value across multiple workloads;
- greater benefit than adaptation of an existing project.

Research can remain broader. Studying chips, memory, storage, networks, or model architecture does not obligate Ordivon to implement them.

See the full derivation in [`../../studies/2026-classical-to-agent-native-computing/`](../../studies/2026-classical-to-agent-native-computing/).
