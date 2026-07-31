# Ordivon Harness v0 Entry Gate

## 1. Purpose

Ordivon Harness v0 must answer one engineering question:

> Can a thin Ordivon-owned Agent Loop use a bare model API and Ordivon Runtime to complete a bounded Tool-using Assignment, emit standard Run evidence, and leave semantic completion with Host?

It is not authorized to become a general Agent framework before that result.

## 2. Initial location

```text
ordivon-host/
  src/ordivon_host/harness/ordivon/
    model.py
    loop.py
    tools.py
    result.py
```

The exact filenames are provisional. The responsibility boundary is not.

## 3. Required v0 components

### Model Adapter

One bounded raw-model call:

```text
messages / content blocks
Tool definitions
optional response schema
cancellation
→ ModelTurn
```

`ModelTurn` should retain:

- assistant content blocks;
- Tool requests with Provider identity;
- usage;
- Provider stop reason;
- raw response digest;
- explicit Provider error or interruption.

### Loop kernel

A sequential loop:

```text
model call
→ zero or more Tool requests
→ Runtime observations
→ next model call
→ Run stop
```

### Tool Bridge

A small Assignment-scoped catalog maps Tool requests to existing Runtime operations. v0 should expose only the capabilities required by the frozen workload.

### Run-local state

Retain only:

- model messages/content blocks;
- Tool requests and bounded observations;
- turn number;
- remaining token/time/Job budget;
- stop state;
- Provider usage and event digest.

This is not Host durable Task state.

### Evidence output

Produce existing `HarnessRunReceipt` and, when justified, a `CompletionProposal` with Artifact references.

## 4. Required stop states

At minimum:

```text
candidate_completed
needs_input
budget_exhausted
context_exhausted
interrupted
provider_failed
tool_failed
invalid_output
```

`candidate_completed` means the Run supplied a completion candidate. Host still verifies and decides.

## 5. First frozen comparison

Run the same bounded repository task under:

```text
A. one-shot ModelGateway
B. Ordivon Harness + bare model API
C. mature Provider Harness direct driver
```

Bind all variants to the same:

- source revision;
- objective and acceptance;
- allowed Tool capability;
- required Artifacts;
- turn/token/time budget declaration;
- Runtime execution boundary.

## 6. Measurements

| Measure | Decision use |
|---|---|
| acceptance success | whether a multi-turn Loop solves a failure one-shot cannot |
| model calls | detect uncontrolled looping |
| Tool calls and Runtime Jobs | determine whether actions are relevant and bounded |
| token usage | compare cognitive cost |
| wall time | measure startup and iteration overhead |
| Artifact validity | verify delivery quality |
| false completion | test Host admission boundary |
| repeated reads/work | evaluate Context and Tool efficiency |
| code size and dependencies | test thin-core claim |
| Provider portability | determine whether a second bare model uses the same Loop |

## 7. Acceptance

v0 is accepted only when all are true:

- one real bare-model Provider is used without delegating the Agent Loop to Codex/Hermes/Claude Code;
- at least two model calls occur in one successful Tool-using Run;
- every physical Tool action executes through Runtime or an explicitly declared external provider;
- Tool Call, Runtime Job, Artifact, Assignment, and Harness Run identities are linked;
- required Artifact and acceptance are independently verified;
- process success and model final text cannot directly complete the Task;
- interruption and one budget stop are deterministic tests;
- one response-loss or ambiguous execution path reconciles before retry;
- no Runtime production schema change, Host Task duplication, SQL table, daemon, or network service is added;
- the implementation remains substantially smaller than the existing mature direct drivers and contains no Provider lifecycle normalization.

## 8. First-round non-goals

- persistent Provider Session;
- Context compaction;
- parallel Tool execution;
- subagents;
- Harness-internal model routing;
- Skills or Plugin platform;
- generalized approval framework;
- durable Harness database;
- workflow language;
- multi-Agent branch/join;
- standalone `ordivon-harness` repository;
- replacement of mature external Harnesses.

## 9. Stop/delete conditions

Stop or delete the v0 direction if:

- the one-shot path completes the same workload with equal correctness and materially lower cost;
- the implementation must copy Host Task or Runtime process state to function;
- a Provider API cannot expose stable Tool/usage semantics without Provider-specific code larger than the Loop;
- the common Model Adapter collapses to unreliable text parsing;
- independent verification cannot distinguish candidate completion from Task completion;
- no second bare-model Provider or consuming workload appears after the first proof;
- maintenance cost exceeds the strategic value of bare-model independence.

## 10. Repository promotion gate

A standalone `ordivon-harness` repository becomes eligible only after:

- a working first-party Loop exists;
- at least two bare-model adapters pass the same frozen Loop contract;
- at least two independent consumers use the package;
- the package does not import Host storage or mutate Task state;
- the package does not own Runtime Workspace or process internals;
- extraction produces measurable net deletion and independent test/release value;
- Provider-specific extensions remain explicit rather than forced into one lifecycle.

Until then, the project name is **Ordivon Harness**, while the implementation remains Host-local.
