# ANC-HARNESS-002 — Ordivon Harness

## Status

Current status, maturity, and next action are owned by [`research/portfolio.json`](../portfolio.json). This page preserves the stable Harness question, ownership hypothesis, frozen v0 scope, acceptance criteria, falsifier, and deletion outcome rather than duplicating the Ready Frontier.

## Question

What is the smallest Ordivon-owned Harness that can turn a bare model API or local inference endpoint into a verifiable Agent Run through Ordivon Runtime without copying Host Task semantics or flattening mature Provider Harness lifecycles?

## Why this is a new question

`ANC-HARNESS-001` tested the boundary among Host, mature Provider Harnesses, and Runtime. H1–H5 rejected a shared Codex/Hermes internal lifecycle while retaining Assignment, Run evidence, completion admission, and Provider-faithful direct drivers.

This question addresses the missing case:

```text
Provider supplies model intelligence
but no complete Agent Loop
```

Ordivon then requires its own Loop to compile model input, interpret Tool Calls, execute through Runtime, return observations, manage a bounded Run, and emit evidence.

## Ownership hypothesis

```text
Host
  durable Task / Attempt / Assignment / acceptance / Outcome

Ordivon Harness
  Model Adapter / Run-local Context / Agent Loop / Tool Bridge / budget / stop / Run evidence

Runtime
  Workspace / Job / Attempt / process / Artifact / physical evidence
```

## Frozen v0 scope

- one bare-model Adapter;
- one sequential multi-turn Loop;
- Assignment-scoped Tool catalog;
- Runtime-backed Tool execution;
- turn/token/time/Runtime-Job budgets;
- cancellation and explicit stop states;
- Artifact-first result;
- existing `HarnessRunReceipt` and `CompletionProposal` boundary.

## First comparison

Use one frozen repository workload under:

1. one-shot ModelGateway;
2. Ordivon Harness with a bare model API;
3. one mature Provider Harness direct driver.

## Acceptance

- at least two model calls and one Runtime Tool action occur in one successful Run;
- the Run binds model, Tool Call, Runtime Job, Artifact, Assignment, and receipt identities;
- required Artifact and acceptance are independently verified;
- Run stop does not directly complete the Task;
- interruption and budget exhaustion are deterministic;
- no Runtime semantic object, Host Task copy, SQL table, daemon, or network service is added;
- the first implementation remains thin and does not normalize Codex/Hermes/Claude internal lifecycles.

## First falsifier

The one-shot ModelGateway or mature Provider Harness completes the same bounded workloads with equal correctness, recovery, portability, and lower permanent cost, while no bare-model or local-model use case requires an Ordivon-owned Loop.

## Deletion outcome

If falsified, retain ModelGateway and external Harness paths and delete the Ordivon Harness prototype. Do not preserve a framework for strategic optionality alone.

## Reopen conditions for broader features

Compaction, persistent Session, parallel Tools, subagents, model routing, Skills, Plugins, and repository extraction require separate observed failures and ablations after v0.
