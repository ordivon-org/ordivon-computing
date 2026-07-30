# Harness Boundary v0 — Stage 1 and Stage 2 Design

Status: frozen design for the first `R-A-HARNESS-CONTROL` vertical slice  
Research owners: `ANC-HARNESS-001`, `ANC-VERIFY-002`  
Implementation owners: `ordivon-host#14`, `ordivon-runtime#64`  
Design date: 2026-07-30

## 1. Decision to test

The experiment asks whether one durable Host Task can continue across two materially different Agent Harnesses while:

- Host retains Task, Task Attempt, Assignment, completion, and recovery authority;
- each Harness retains its Session, local context, tool loop, compaction, and provider-specific behavior;
- Runtime retains Workspace, Job, Runtime Attempt, process, Artifact, and physical execution truth;
- a fresh Harness can continue from Host state without hidden-reasoning transfer;
- stale Harness work cannot commit semantic completion or duplicate an external Effect.

The experiment does not begin by creating an `ordivon-harness` repository. The first boundary remains Host-local and earns extraction only through live replacement, a second consumer, stable capability semantics, and measurable duplicate-code reduction.

## 2. Existing foundations reused

### Host already provides

- durable Goal and Task streams;
- revisioned `TaskProjection` and a Task lease;
- compiled Context with source bindings;
- `ModelInvocationIntent`, observations, and receipts;
- `ActionProposal`, `DecisionRequest`, and `TaskOutcome`;
- content-addressed objects and event history;
- operator handoff state;
- fresh-Host continuation and Codex/Hermes one-shot baselines.

### Runtime already provides

- immutable Workspace identity and source commitment;
- `clientRequestId`, Job, and Runtime Attempt identity;
- at-most-once physical dispatch;
- bounded observation, cancellation, Artifacts, and terminal evidence;
- explicit lost/orphaned outcomes and reconciliation;
- up to sixteen immutable `foreignReferences` bound into request identity and terminal evidence.

### Provider Harnesses available locally

| Harness | Native protocol | Relevant capabilities |
|---|---|---|
| Codex CLI 0.145 App Server | JSON-RPC over stdio/Unix/WebSocket | thread start/resume/fork, turn start/interrupt, tool and approval events, persistent Session |
| Hermes Agent 0.18 ACP | Agent Client Protocol over stdio | session new/load/resume/fork, prompt/cancel, MCP tools, tool-call updates, usage, persistent Session and checkpoints |

The existing `CodexCliModelGateway` and `HermesCliModelGateway` remain one-shot direct baselines. They are not renamed as Harnesses.

## 3. Smallest admitted Host objects

Stage 1 admits four experimental object types. They live in Host's content-addressed object store and Task event stream. No new database table or service is introduced.

### 3.1 `TaskAttemptDescriptor`

One semantic path through a Task. Harness replacement inside the same intended path keeps this identity.

```text
schemaVersion
kind = ordivon.task-attempt-descriptor
taskAttemptId
taskId
startedAtTaskRevision
objectiveDigest
acceptanceCriteriaDigest
createdAtMs
```

The descriptor is immutable. Task state remains in the Task stream; v0 does not add a second Task-Attempt state machine.

### 3.2 `HarnessAssignment`

One durable Host commitment that authorizes a specific Harness to work on the current Task Attempt.

```text
schemaVersion
kind = ordivon.harness-assignment
assignmentId
taskId
taskRevision
taskAttemptId
generation
targetHarnessId
harnessManifestDigest
contextObjectDigest
acceptanceCriteriaDigest
toolCatalogDigest
workspace / source references
prior Artifact and evidence references
budget and deadline
requiredCapabilities
createdAtMs
```

Rules:

- `generation` is a durable monotonically increasing integer within one Task Attempt;
- replacement creates a new Assignment generation;
- the Assignment binds one exact Harness manifest and one exact compiled Context;
- provider Session identity is absent from the Assignment;
- a changed generation or digest requires a new Runtime operation identity.

### 3.3 `HarnessRunReceipt`

Evidence for one concrete Harness process/session execution.

```text
schemaVersion
kind = ordivon.harness-run-receipt
harnessRunId
assignmentId
assignmentGeneration
harnessId
harnessRevision
manifestDigest
sessionRef
startedAtMs
finishedAtMs
stopReason
eventDigest
contextDigest
toolCatalogDigest
Runtime Job and Artifact references
usage
```

`sessionRef` is Harness-local evidence. It never becomes Task or Task-Attempt identity and is not required by a replacement Harness.

### 3.4 `CompletionProposal`

A Harness proposal that the current Task or Task Attempt satisfies declared acceptance criteria.

```text
schemaVersion
kind = ordivon.completion-proposal
completionProposalId
taskId
taskRevision
taskAttemptId
assignmentId
assignmentGeneration
harnessRunId
summary
acceptanceResults
evidenceRefs
artifactRefs
unresolvedEffectRefs
unresolvedUnknowns
usage
createdAtMs
```

Host accepts or rejects the proposal against current durable state. A process exit, provider final message, or Runtime Job success cannot commit Task completion by itself.

## 4. Host-local adapter boundary

The common interface stays smaller than either provider protocol:

```python
class HarnessAdapter(Protocol):
    harness_id: str

    def manifest(self) -> HarnessCapabilityManifest: ...
    def start_assignment(
        self,
        assignment: HarnessAssignment,
        event_sink: HarnessEventSink,
    ) -> HarnessRunHandle: ...
    def wait(self, run: HarnessRunHandle) -> HarnessRunResult: ...
    def interrupt(self, run: HarnessRunHandle, reason: str) -> None: ...
    def close(self, run: HarnessRunHandle) -> None: ...
```

The interface deliberately omits:

- a provider-independent hidden-reasoning format;
- a universal Session snapshot;
- Host Task mutation methods;
- Runtime process control;
- global Skills, Plugins, Hooks, or subagents;
- a common planner or memory implementation.

Provider capabilities remain explicit through a manifest. V0 observes but does not normalize optional capabilities such as session resume, fork, compaction, checkpoint, approval modes, images, local subagents, and provider-specific commands.

### Codex mapping

```text
start_assignment  → initialize + thread/start + turn/start
Harness events    → thread/turn/item notifications
interrupt         → turn/interrupt
provider resume   → thread/resume (observed capability, not Task continuity)
```

### Hermes mapping

```text
start_assignment  → initialize + session/new + session/prompt
Harness events    → session/update, including tool_call and tool_call_update
interrupt         → session/cancel
provider resume   → session/load or session/resume (observed capability)
```

## 5. Durable identity map

```text
Goal
└── Task
    └── Task Attempt                         Host semantic path
        ├── Assignment generation 1          Host commitment
        │   └── Harness Run A                 Codex or Hermes Session/process
        │       └── Runtime Job
        │           └── Runtime Attempt       physical execution
        └── Assignment generation 2          replacement commitment
            └── Harness Run B
                └── Runtime Job(s)
                    └── Runtime Attempt(s)
```

Replacement preserves Goal, Task, and Task Attempt. It changes Assignment generation, Harness Run, provider Session, and any new Runtime Jobs.

The current Task lease protects a short Host transition. It is not used as a durable fencing generation because released lease rows can disappear. Assignment generation provides the persistent stale-worker fence.

## 6. Minimum Task events

Four explicit event kinds are sufficient for v0:

```text
HARNESS_ASSIGNMENT_COMMITTED
HARNESS_RUN_RECORDED
COMPLETION_PROPOSED
COMPLETION_DECIDED
```

Each event references immutable objects. Host keeps Task state in the existing projection and avoids a parallel Harness or Assignment database.

A rejected stale proposal remains stored and inspectable. Rejection advances no Task completion state and dispatches no new Effect.

## 7. Frozen workload

Workload identity: `harness-replacement-repository-repair-v1`.

A small frozen Git repository contains:

- a versioned specification;
- a deterministic code defect;
- acceptance tests;
- an empty `artifacts/` directory.

The Goal requires two deliverables:

1. `artifacts/diagnosis.json` describing the defect, affected revision, proposed correction, and evidence;
2. a verified code correction plus `artifacts/completion.json` referencing the diagnosis digest, final source revision, test result, and changed paths.

### Replacement trajectory

```text
Assignment g1 → Codex App Server
→ inspect repository
→ create diagnosis Artifact
→ deliberate Session/process termination

Host records Run A evidence
→ recompiles current Context
→ commits Assignment g2

Assignment g2 → Hermes ACP
→ re-read current repository
→ consume diagnosis as evidence, not hidden state
→ correct code and run tests through Runtime
→ submit CompletionProposal
→ Host verifies and commits TaskOutcome
```

The reverse order, Hermes then Codex, is run as a second live trial. Direct one-Harness and one-shot paths use the same repository, acceptance criteria, budget, and grader.

## 8. Initial fault matrix

Only three faults enter the first live slice.

### F1 — stale Assignment completion

Run A submits a CompletionProposal after generation 2 has been committed.

Expected result:

- proposal and evidence remain inspectable;
- Host rejects semantic completion;
- no new Effect is dispatched;
- Run B continues.

### F2 — process success without required Artifact

The Harness or Runtime Job exits successfully but `diagnosis.json` or `completion.json` is absent, mismatched, or references the wrong digest.

Expected result:

- Runtime success remains physical evidence;
- CompletionProposal is rejected or remains incomplete;
- Task stays continuable.

### F3 — ambiguous Runtime result

The code-changing Runtime request may have committed, but the response is lost.

Expected result:

- Host resolves the original Job by `clientRequestId`;
- exact foreign references and terminal evidence are checked;
- no blind redispatch occurs;
- CompletionProposal waits for reconciled evidence.

Context drift, Hook recursion, compaction loss, adversarial stopping, and broader non-action pairs remain later slices.

## 9. Stage 2 Runtime correlation contract

Stage 2 uses Runtime's existing `foreignReferences`; it does not add Registry columns or rename `task.*` Tools.

Canonical Host references use namespace `ordivon.host`:

| type | id | generation | digest |
|---|---|---|---|
| `task` | Host Task ID | Task revision | current Task event/projection digest |
| `task_attempt` | Task Attempt ID | omitted | descriptor digest |
| `assignment` | Assignment ID | Assignment generation | Assignment digest |
| `harness_run` | Harness Run ID | omitted | run-intent or receipt digest |
| `effect` | Effect ID when present | omitted | Effect digest |
| `dispatch` | Dispatch ID when present | omitted | Dispatch/request digest |

A Runtime request from a Harness path carries at least Task, Task Attempt, Assignment, and Harness Run references. Effect and Dispatch references are added when the operation crosses an Effect commitment boundary.

Because foreign references participate in Runtime request identity:

- replaying the same `clientRequestId` and same references resolves the original Job;
- changing Assignment generation or digest under the same `clientRequestId` is a conflict;
- replacement creates a new `clientRequestId` for new work;
- terminal evidence preserves the cross-layer identity chain.

## 10. Stage 2 conformance vector

One vector must prove:

```text
Task task:T at revision 7
Task Attempt task-attempt:T:1
Assignment assignment:T:1:g1
Harness Run harness-run:codex:1
→ Runtime Job job:J
→ Runtime Attempt attempt:A
```

Assertions:

1. all four Host references are admitted into the Execution Plan;
2. exact replay returns `job:J` and does not create another Runtime Attempt;
3. changing Assignment generation under the same `clientRequestId` is rejected;
4. terminal evidence contains the exact Host references plus Job and Runtime Attempt identity;
5. fresh Host code can locate `job:J`, read terminal evidence, and reconstruct the identity map;
6. Job success remains insufficient for semantic Task completion.

If existing fields and documentation satisfy this vector, Stage 2 closes without a Runtime schema migration or API rename.

## 11. Measurements

### Correctness

- stale CompletionProposal acceptance count;
- false Task completion count;
- duplicate Runtime dispatch or external Effect count;
- missing/mismatched Artifact detection;
- first correct action after replacement;
- accepted final repository state.

### Continuity

- retained Goal, Task, Task Attempt, Effect, and Artifact identities;
- repeated reads, Tool calls, and edits;
- unsupported assumption carried across replacement;
- operator interventions;
- time from replacement to useful action.

### Cost

- adapter-specific and shared code size;
- provider capabilities lost through the boundary;
- model calls, tokens, Context bytes, Tool calls, wall time, and provider cost;
- Runtime/Host persistent object count and bytes;
- maintenance required by provider evolution.

## 12. Baselines

The shared boundary competes against:

1. existing one-shot `CodexCliModelGateway` plus Host continuation state;
2. existing one-shot `HermesCliModelGateway` plus Host continuation state;
3. provider-specific direct Codex App Server driver;
4. provider-specific direct Hermes ACP driver;
5. shared Host-local `HarnessAdapter` boundary.

The common boundary earns retention only when it prevents a demonstrated cross-provider failure or removes meaningful duplicate lifecycle code without losing provider capability.

## 13. Decisions after the slice

Every candidate receives one disposition.

| Candidate | Retain when | Delete/localize when |
|---|---|---|
| Task Attempt descriptor | replacement needs one semantic path identity | Task + Assignment already express the path |
| Assignment generation | stale work is otherwise accepted or ambiguous | Task revision alone fences every tested case |
| Harness Run receipt | provider/session evidence improves recovery or diagnosis | existing invocation/Runtime receipts are sufficient |
| CompletionProposal | it prevents false completion or preserves unresolved work | current TaskOutcome/verification already catches every case |
| shared HarnessAdapter | two adapters share stable useful lifecycle code | direct drivers remain simpler or preserve more capability |
| Runtime foreign-reference convention | fresh Host recovery needs the identity chain | `clientRequestId` and Host records already reconstruct it |

No result automatically promotes a Protocol object or creates `ordivon-harness`.

## 14. Implementation sequence

```text
S1.0 Host contracts and deterministic stale-generation tests
S2.0 Runtime foreign-reference convention and conformance vector
S2.1 Host Runtime-reference builder used by the experiment path
S1.1 Codex App Server direct driver and thin adapter
S1.2 Hermes ACP direct driver and thin adapter
S1.3 live replacement in both directions
S1.4 three-fault matrix and equal-budget comparison
S1.5 retain / localize / shrink / delete report
```

S1.0 and S2.0 may proceed in parallel. Live Stage 1 execution begins only after the Runtime correlation vector passes.
