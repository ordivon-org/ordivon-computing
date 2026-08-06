# Current Ordivon Gap Audit

## 1. Audit scope

The local source audit used these exact revisions:

| Repository | Revision |
|---|---|
| `ordivon-host` | `7b17807784cc52f0be4f1786719f6dc20deb92c8` |
| `ordivon-harness` | `f39943e4bc4e5e9e0478994a68a05f69d480406f` |
| `ordivon-runtime` | `ce061a5995d7a59246a103dcc51f0539245209a6` |
| `ordivon-computing` | `ac132a5dd88d7e7b9bd42d9924bed55e2f3303e9` |

The machine-readable observations are in [`evidence/source-audit-20260806.json`](evidence/source-audit-20260806.json).

## 2. What is already correct

### 2.1 Host is a commitment kernel

`HostKernel` provides:

- exact Task revision checks;
- short lease ownership and generation fencing;
- projection equality checks;
- one transition per locked Task;
- immutable referenced objects;
- terminal irreversibility;
- monotonic revision and time.

This is the correct substrate for durable semantic commitment. It should not be replaced by a graph framework.

### 2.2 Harness has strong execution continuity

The independent Harness owns:

- caller-neutral `HarnessRunContract`;
- independent Journal/CAS path;
- Provider Call claim, dispatch, result, failure, UNKNOWN, and replay;
- Tool Step intent, fence, receipt, and reconciliation;
- Run snapshots and traces;
- budgets, pause/resume, cancellation, abandonment, and recovery;
- CompletionProposal separated from final Task completion;
- a standalone runner and optional Host adapter.

This is a stronger continuity base than most experimental reasoning graphs assume.

### 2.3 Runtime has strong physical truth

Runtime owns:

- idempotent `clientRequestId` admission;
- exact Workspace and source-state binding;
- Job, Attempt, reservation, and process-tree identity;
- bounded output and Artifacts;
- terminal supervision evidence;
- cancellation and reconciliation;
- explicit `lost`, `orphaned`, and uncertain states;
- no speculative redispatch after ambiguous delivery.

This Effect boundary should remain semantically ignorant.

### 2.4 Computer already distinguishes graph semantics

Existing Computer research separates Goal, Task, Workflow, Planning, Agent, Assignment, Tool, Execution, Artifact, Provenance, Knowledge, and Communication graphs. It also distinguishes model, Agent, scheduling, execution, reconciliation, evaluation, improvement, and memory loops.

The missing result is not graph taxonomy. It is a minimum executable state and mutation model for the Harness.

## 3. Current limitations

## 3.1 Harness cognition is still transcript-centered

`HarnessRunState` persists:

```text
messages
observations
remaining_budget
requested/effective model
seen model and Tool Call identities
usage
```

This is excellent for deterministic continuation of a sequential Tool-calling loop. It does not directly represent:

- multiple active hypotheses;
- conflicting evidence;
- independent work branches;
- explicit unknowns and blockers;
- parent/child ownership;
- branch joins;
- local Working Sets;
- reusable Context programs;
- HarnessRevision provenance.

The system can express these only inside message content or ad hoc Artifacts.

## 3.2 The current Engine is one sequential loop

`OrdivonAgentLoop` is explicitly a thin sequential loop. It advances one model response and Tool action path while Host Task and Runtime Job lifecycles remain external.

This path should remain as `SequentialEngine`, but it must stop being the only possible cognitive execution architecture.

## 3.3 Capability declarations expose the gap

The current first-party manifest reports:

```text
persistent_session = false
session_resume = false
session_fork = false
compaction = false
local_subagents = false
```

These were correct v0 exclusions. They now identify the exact capability surface that requires a new experiment rather than more branches inside the existing loop.

## 3.4 Contract references collapse into prompt state

`HarnessRunContract` already binds objective, Context, source, prior Artifact, Tool catalog, Tool grant, budget, completion contract, and system manifest by immutable reference.

The current standalone execution still reduces the active cognitive view primarily to initial messages and one Context digest. The contract is object-oriented while the cognition state remains transcript-oriented.

This mismatch is the cleanest insertion point for a Working Set compiler.

## 3.5 Host and Harness retain two cognition entry paths

Host architecture says model intelligence and Provider continuity are outside Host, but Host still contains:

- `cognition/` profiles;
- Provider invocation models and gateways;
- `CognitionTurnHost`;
- `OpenProposalHost.propose()`.

Harness independently owns Provider adapters and the Agent Loop.

This creates two places to implement Context selection, usage accounting, recovery, persistent Sessions, and future graph mutation. New cognition capabilities must converge in Harness. Host should retain proposal admission, consequence classification, decisions, verification, and Outcomes.

## 3.6 External Harness execution is lifecycle-shaped but synchronously driven

`ExternalExecutorAdapter` correctly exposes:

```text
start
observe
cancel
recover
collect_completion
```

`ExternalExecutorCoordinator` persists the request before delivery and treats foreign Run state as opaque. It never lets a foreign completion directly complete the Host Task.

However, the current Ordivon Harness adapter executes the driver to completion during `start()`. The seam is semantically asynchronous but operationally synchronous.

A persistent Run Actor requires:

```text
Host request admission
→ Harness daemon acceptance
→ immediate foreign Run binding
→ independent execution and observation
```

## 3.7 Runtime supports terminal Jobs, not interactive Workers

`RuntimeExecutionPlan` and `UniversalExecutionStep` represent one terminal execution, optionally with a bounded ordered step list. This is appropriate for commands, tests, builds, and scripts.

A persistent RLM kernel, language server, simulator, or long-lived Agent process needs a separate physical abstraction only if the Harness experiments prove that repeated terminal Jobs cannot provide the required continuity efficiently.

The candidate abstraction is a supervised Worker plus idempotent Worker Calls, not a semantic Agent inside Runtime.

## 3.8 Parallel source work lacks a first-class fork boundary

Runtime binds a Job to one Workspace source state and allows at most one active execution per Workspace. This prevents concurrent Ordivon-mediated mutation races.

Child coding Runs therefore need one of:

- independent Workspaces from the same committed revision;
- a future immutable Workspace snapshot/fork operation;
- read-only branches with Artifact outputs;
- serialized mutation.

They must not share one writable Workspace without explicit merge and verification.

## 4. Which prior decisions remain valid

| Prior decision | Current disposition |
|---|---|
| Host, Harness, Runtime, verifier remain distinct | retain |
| Provider Session is not Task identity | retain |
| Run evidence is not TaskOutcome | retain |
| Artifact-first completion | retain |
| Runtime remains semantically ignorant | retain |
| mature Provider Harness internals are not flattened | retain |
| persistent Session is Harness-local | retain |
| v0 sequential loop | retain as baseline Engine, not final architecture |
| no subagents/parallelism/compaction in v0 | reopen through controlled ablation |
| no Harness daemon in v0 | reopen because synchronous foreign execution cannot host persistent actors |
| no mandatory graph store | retain |
| minimal durable state and deletion test | retain and apply to every graph object |

## 5. Reproduced failures that justify reopening

The reopening is justified by a conjunction, not one fashionable paper:

1. **representation failure** — open branches and conflicts live only in prose;
2. **context failure** — all durable objects cannot remain in every prompt;
3. **lifecycle failure** — a synchronous Run call cannot represent a detached persistent Actor;
4. **coordination failure** — local subagents lack durable scope, result, budget, and join state;
5. **ownership duplication** — Host and Harness both contain cognition entry paths;
6. **execution-carrier failure** — terminal Jobs cannot efficiently host all persistent interactive engines;
7. **adaptation failure** — Harness self-change has no version, evaluation, activation, or rollback object.

## 6. What the audit does not prove

The audit does not prove that a Temporal Cognitive Graph will outperform:

- current messages and observations;
- transcript plus compaction;
- transcript plus retrieval;
- a mature Provider Harness;
- filesystem plans and Artifacts;
- an ordinary Host Task Graph.

That decision belongs to the experiment program.
