# Host, Harness, and Runtime Boundaries

## 1. Three different control planes

The three components operate at different semantic levels.

```text
Ordivon Host        durable semantic work control
Ordivon Harness     bounded probabilistic cognition control
Ordivon Runtime     physical execution and evidence control
```

They may run in one process during early development. Logical ownership must remain separate even when deployment is monolithic.

## 2. Host responsibility

Ordivon Host owns state that must survive Model, Harness Session, provider, process, UI, and Runtime replacement:

- Goal identity, constraints, commitments, and completion criteria;
- Task identity, revision, dependency graph, Ready Frontier, and supersession;
- Assignment, lease, budget, worker identity, and fencing generation;
- Task Attempt identity and high-level outcome;
- waits, blockers, DecisionRequests, Signals, and participant intervention;
- Task-level completion proposal, verification, acceptance, rejection, or reopening;
- cross-session and cross-Harness continuation;
- semantic references to Context, Effect, Dispatch, Evidence, and Artifact;
- scheduling, retry, re-assignment, and recovery policy.

Host does not own Linux process truth, provider hidden state, raw model reasoning, Tool implementation, or domain-world transition rules.

## 3. Harness responsibility

Harness owns one cognitive episode and its model-specific control loop:

- Model adapter and invocation parameters;
- Context compilation and model-visible working set;
- reasoning-state retention when the provider supports it;
- compaction and working-memory management;
- Skill discovery, selection, and loading;
- Tool schema exposure and Tool-call/result normalization;
- local plan, Agent loop, stopping policy, retry policy, and handoffs;
- short-lived subagents and local critics;
- Session, Thread, Turn, Item, and Step events as required by the Harness;
- Harness checkpoint or resume data that cannot be reconstructed from Host state;
- model-specific capabilities that should not be flattened into a lowest common denominator.

Harness proposes changes to durable work. It does not directly rewrite Task truth.

## 4. Runtime responsibility

Runtime owns physical execution facts:

- Workspace creation, revision binding, mutation, Diff, and closeout;
- Job and Runtime Attempt admission, process creation, stdout/stderr, exit, timeout, and cancellation;
- Artifact persistence and execution-result identity;
- resource use, environment, credentials, and local capability boundaries;
- correlation after response loss;
- Job observation, recovery, and no-blind-redispatch semantics;
- physical idempotency, compensation hooks, and provider receipts where available.

Runtime does not decide whether a Goal is complete, which Task should run next, which Model should be used, or whether an outcome satisfies domain meaning.

## 5. End-to-end lifecycle

```text
Participant proposes Goal
→ Host commits Goal and Tasks
→ Host computes Ready Frontier
→ Host creates Assignment with lease and budget
→ Harness starts a Run for that Assignment
→ Harness compiles Context and loads relevant Skills/Tools
→ Model produces Claim, ActionProposal, Tool call, or local plan revision
→ Harness requests Tool execution
→ Runtime or provider creates Job, Runtime Attempt, or receipt
→ Runtime emits Observation and Artifact references
→ Harness interprets result and chooses next step
→ Harness submits progress, blocker, Task split, or CompletionProposal
→ Host validates current revision, evidence, lease generation, and acceptance criteria
→ Host commits Task state and updates the Task Graph
```

## 6. Object ownership matrix

| Object | Creates/proposes | Authoritative owner | Executes/consumes |
|---|---|---|---|
| Goal | participant or Harness proposal | Host | Host/Harness |
| Plan | Harness | Harness working state | Harness |
| TaskProposal | Harness/participant | not authoritative until admitted | Host |
| Task | Host | Host | Harness worker |
| Assignment | Host | Host | Harness/worker |
| Task Attempt | Host creates; Harness advances | Host summary + linked evidence | Harness/Runtime |
| Runtime Attempt | Runtime creates under one Job | Runtime | process/backend |
| Session/Thread | Harness/interaction Host | Harness product | client/Harness |
| Context | Harness compiler | Harness receipt; sources authoritative elsewhere | Model |
| Skill selection | Harness | Harness receipt | Harness/Model |
| Tool Contract | provider/normalizer | protocol/catalog owner | Harness/Runtime |
| Tool Call | Model/Harness | Harness trace | Tool provider |
| Effect | Harness/domain proposal, authority admission | semantic commitment layer | Dispatch adapter |
| Dispatch | Host/commitment layer | Host/semantic journal | Runtime/provider |
| Job | Runtime/provider | Runtime/provider | process/backend |
| Artifact | Runtime/provider | Artifact store | Harness/Host/Eval |
| CompletionProposal | Harness | proposal only | Host validator |
| TaskCompleted | Host | Host | projections/UI |

## 7. Completion boundary

A model or Harness must not directly set `Task.status = completed`.

It submits:

```text
CompletionProposal {
  task_id
  task_revision
  assignment_generation
  summary
  acceptance_results
  evidence_refs
  artifact_refs
  unresolved_risks
  cost_and_usage
  confidence
}
```

Host then applies deterministic and domain-specific checks:

- current Task revision and lease generation;
- required Evidence and Artifact existence;
- acceptance-criterion coverage;
- no unresolved external outcome marked `UNKNOWN`;
- optional Judge, verifier, participant, or domain acceptance;
- conflict with newer work or superseding Task.

Only then is `TaskCompleted` committed.

## 8. Thin Ordivon Harness hypothesis

Because Host and Runtime already own durable work and execution, a native Ordivon Harness can remain small:

```text
HarnessInput {
  assignment_ref
  task_context_sources
  model_config
  skill_manifest
  tool_manifest
  budget
}

HarnessOutput stream {
  run_started
  context_compiled
  model_invocation
  tool_request
  tool_result
  progress
  task_proposal
  completion_proposal
  interrupt_request
  run_finished
}
```

Minimum interface candidates:

```text
start_assignment
resume_run
send_signal
provide_input
interrupt
stream_events
checkpoint
finish
```

Capabilities are negotiated rather than assumed:

```text
supports_resume
supports_fork
supports_reasoning_retention
supports_compaction
supports_subagents
supports_native_tools
supports_structured_output
supports_remote_execution
```

## 9. Adapter strategy

The first boundary should support:

- `CodexHarnessAdapter` through Codex App Server or another stable surface;
- `ClaudeHarnessAdapter` through Claude Agent SDK/CLI hosting where useful;
- `HermesHarnessAdapter` for the existing provider path;
- `NativeHarness` only for experiments, fallback, and features not available elsewhere.

The adapter must preserve provider-specific capability metadata. A shared interface should not force all providers into the smallest common feature set.

## 10. Repository decision

Do not create `ordivon-harness` merely because the concept exists.

Retain it inside Host or Computing until:

1. two real adapters execute the same Host Task contract;
2. Harness replacement occurs during one Task without false continuity;
3. shared Context/Skill/Tool-loop code is substantial enough to reduce duplication;
4. a standalone test and release boundary is useful;
5. no Host or Runtime authority leaks into the package.

If those conditions fail, Harness remains an interface and local adapters, not a repository or product.

## 11. Naming correction

`Runtime` is overloaded across the industry:

```text
Model Runtime      runs model inference
Agent Runtime      runs Harness/Session state
Task Runtime       runs durable declared work
Execution Runtime  runs physical Jobs and Workspaces
```

Ordivon should use explicit qualifiers. `ordivon-runtime` means **Execution Runtime**. A Codex Core “runtime” is primarily an **Agent Runtime**. Similar wording does not imply the same authority.
