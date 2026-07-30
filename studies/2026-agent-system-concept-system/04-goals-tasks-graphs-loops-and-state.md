# Goals, Tasks, Graphs, Loops, and State

## 1. Work-object chain

The canonical chain is:

```text
Goal
└── Task
    └── Assignment
        └── Task Attempt
            └── Harness Run
                └── Turn
                    └── Step
                        └── Tool Call / ActionProposal
                            └── Effect and Dispatch where commitment is required
                                └── Runtime Job or provider receipt
                                    └── Runtime Attempt / process where applicable
                                        └── Observation / Artifact / Evidence
```

Each level has a different identity and failure boundary.

## 2. Goal

A Goal expresses a desired world condition, not a complete execution program.

```text
Goal
= origin or accepting participant
+ desired condition
+ constraints and non-goals
+ consequence and resource relationships
+ completion evidence
```

A Goal survives many Tasks, Plans, Models, Harnesses, and Runtime nodes.

## 3. Plan

A Plan is the current cognitive hypothesis for reaching a Goal.

It may be:

- incomplete;
- probabilistic;
- locally inconsistent;
- revised after new evidence;
- discarded without altering durable history.

A Plan remains Harness-local until a part requires stable identity, independent assignment, waiting, retry, acceptance, or evidence. At that point the Harness proposes a Task.

```text
Plan node becomes operationally independent
→ TaskProposal
→ Host admission
→ durable Task
```

## 4. Task

A Task is a durable semantic work contract. It should minimally identify:

```text
task_id
goal_id
revision
purpose and expected outcome
acceptance criteria
inputs and source revisions
dependencies
current state
priority and budget
evidence requirements
supersession and cancellation relationships
```

Task is not synonymous with:

- a chat Session;
- a model invocation;
- a Runtime Job;
- a Kubernetes Job;
- a Temporal Workflow;
- a Tool call;
- a process.

Those objects may execute or support one part of a Task.

## 5. Assignment and Task Attempt

### Assignment

An Assignment is time-bounded delegation:

```text
Task
+ Harness and Model selection
+ Skill and Tool capability set
+ Runtime / World binding
+ lease and fencing generation
+ time, token, money, and consequence budget
```

### Task Attempt

A Task Attempt is one semantic exploration or execution path through a Task. Failed Task Attempts remain useful evidence and must not erase the Task.

```text
Task T
├── Task Attempt A: provider unavailable
├── Task Attempt B: wrong hypothesis, useful failure evidence
└── Task Attempt C: accepted completion
```

## 6. Run, Turn, Step, and Item

These are Harness-level objects and may differ by provider.

- **Run** — one Harness execution under an Assignment.
- **Turn** — bounded work initiated by input and ending in output, wait, limit, or interruption.
- **Step** — one model, Tool, state, or control transition.
- **Item** — typed stream object for message, Tool execution, approval, Diff, or other UI-visible unit.

Host should not require every Harness to use identical internal step types. It needs stable high-level events and evidence references.

## 7. Task decomposition

Goal-to-Task decomposition is a split responsibility:

```text
Harness proposes
Host commits
```

Harness may submit:

```text
CreateTaskProposal
SplitTaskProposal
MergeTaskProposal
AddDependencyProposal
SupersedeTaskProposal
CancelTaskProposal
```

Host validates:

- current Goal and Task revisions;
- duplicate or equivalent work;
- dependency cycles and impossible constraints;
- capability and budget;
- conflicting ownership or mutation;
- whether a local Plan node actually needs durable Task identity.

A temporary model Todo list is not automatically the Task Graph.

## 8. Graph families

Graph is a data structure, not a controller. Different semantics require different graphs.

| Graph | Nodes | Edges / meaning | Owner |
|---|---|---|---|
| Goal Graph | Goals | supports, conflicts, refines, supersedes | Host/domain |
| Task Graph | Tasks | depends_on, blocks, produces, validates, replaces | Host |
| Workflow Graph | step templates | declared control and conditions | Host/workflow backend |
| Planning Graph | hypotheses/actions | local search and contingencies | Harness |
| Agent Graph | Agents | handoff, delegation, communication | Harness or Host by lifetime |
| Assignment Graph | Tasks and workers | current delegation and lease | Host |
| Tool Graph | capabilities/contracts | requires, implements, routes_to | Harness/Broker |
| Execution Graph | Jobs/processes | spawn, wait, dependency | Runtime |
| Artifact Graph | Artifacts | derived_from, contains, supersedes | Runtime/Artifact store |
| Provenance Graph | semantic and physical objects | caused_by, produced_by, verified_by | cross-layer |
| Knowledge Graph | entities/claims | domain relations and evidence | knowledge layer |
| Communication Graph | participants/messages | sender, receiver, reply, causal link | Host/domain |

One generic graph database may store several of these, but it must not erase their distinct invariants.

## 9. Ready Frontier

Ready Frontier is the subset of durable Tasks that are currently admissible for assignment.

Readiness may depend on:

- predecessor completion;
- evidence availability;
- participant or resource commitment;
- current world and Tool revisions;
- lease and worker capacity;
- budget and deadlines;
- conflict or mutual exclusion;
- consequence policy;
- explicit waits and external triggers.

There is usually no unique “next Task.” The Frontier may contain zero, one, or many Tasks.

## 10. Loop families

Loop is the controller that advances a state structure.

| Loop | Core cycle | Owner |
|---|---|---|
| Model inference loop | token state → next token | Model Runtime |
| Agent loop | Context → Model → Tool/answer → observation → Context | Harness |
| Local planning loop | hypothesis → test → evidence → revise | Harness |
| Scheduling loop | ready work → select worker → Assignment | Host |
| Task orchestration loop | observe Assignments → complete/retry/replan | Host |
| Execution loop | admit request → start Job → observe → finish | Runtime |
| Reconciliation loop | unknown delivery → inspect world → bind result | Host/Runtime/World |
| Approval loop | DecisionRequest → authority decision → resume | Host |
| Evaluation loop | trajectory → score/diagnosis → comparison | Eval/Computing |
| Improvement loop | failures/evals → Skill/Harness/Tool proposal → canary | cross-layer |
| Memory consolidation loop | trajectories → candidate knowledge → verification | Harness/Eval/Knowledge |

## 11. Parallel graph patterns

Host may need a small set of explicit graph combinators:

```text
Fan-out          create independent branches
Join / Fan-in    wait for declared inputs and integrate
Barrier          all required participants reach a point
Race             first valid result advances
Cancel remainder stop losing speculative branches
Quorum           require independent evidence conditions
```

These are control semantics, not proof that a general workflow DSL is required.

## 12. Local subagent versus Host worker

A Harness-local subagent:

- is short lived;
- serves one parent Run;
- has no independent durable Task;
- can be regenerated by the parent;
- returns a bounded result or summary.

A Host-managed worker:

- owns an Assignment to a durable Task;
- may outlive the parent Session;
- has an independent Workspace or World binding;
- can be retried or moved to another Harness;
- requires lease, budget, evidence, and completion state.

Promotion rule:

```text
needs independent identity + scheduling + recovery
→ Host Task and worker
otherwise
→ Harness-local subagent
```

## 13. Handoff, delegation, routing, and escalation

- **Handoff** transfers current cognitive or conversational control.
- **Delegation** assigns a bounded subproblem while the parent retains responsibility.
- **Routing** selects an executor before or during work.
- **Escalation** directs unresolved responsibility to a more capable or authorized participant.

Harness may perform local handoffs. Host owns persistent delegation and Assignment routing.

## 14. State families

### Durable Host state

```text
Goal, Task, Task Graph, Assignment, Task Attempt
waits, blockers, decisions, budgets, completion
```

### Harness state

```text
Session, Context, working memory, local Plan
Turn, Step, Skill loading, Tool exposure
```

### Runtime state

```text
Workspace, Job, process, output, Artifact
resource use, cancellation, physical receipt
```

### Domain World state

```text
Game World, Security environment, external provider object
rules, authoritative transition, domain outcome
```

### Knowledge state

```text
verified reusable facts, Skills, playbooks, studies, evaluations
```

## 15. Memory categories

```text
Working memory   current Harness Run
Episodic memory  prior trajectories
Semantic memory  reusable facts and explanations
Procedural memory Skills and Workflows
Authoritative state Host/Runtime/World databases, not “memory” merely because a Model can retrieve it
```

Context is a compiled working set, not the authoritative store.

## 16. Completion and reopening

A Task may be:

```text
proposed
ready
assigned
running
waiting
blocked
completion_proposed
completed
failed
cancelled
superseded
reopened
```

The exact state set should remain small. Additional labels must prevent a concrete failure. `UNKNOWN` usually belongs to an Effect, Dispatch, or external outcome rather than becoming a vague Task state.

Completion can be reopened when:

- evidence is invalidated;
- the world or source revision changes;
- acceptance was based on a stale Assignment;
- a stronger verifier rejects the result;
- the Goal itself changes.
