# Temporal Cognitive Graph Model

## 1. Candidate abstraction

A Temporal Cognitive Graph (TCG) is a Harness-owned, Run-scoped, versioned projection over typed cognitive events and immutable content references.

```text
TCG = (N, E, R, A, B)

N  typed cognitive nodes
E  typed directed edges
R  monotonic graph revision
A  actor and ownership bindings
B  active budget and boundary bindings
```

The authoritative history is not the mutable graph itself:

```text
CausalEventLog + immutable objects
→ deterministic validated projection
→ query indexes
→ Working Sets
```

## 2. Minimum node families

The first experiment should use the smallest node set that can express its failure trajectories.

### Objective

A bounded desired condition or subgoal inherited from the Run Contract or created as a local decomposition.

Required fields:

```text
node_id
objective_ref or bounded statement
status
parent objective
acceptance reference
provenance
```

### WorkItem

One active, waiting, blocked, resolved, or abandoned cognitive operation.

Examples:

- inspect module;
- compare two hypotheses;
- run experiment;
- await Child Run;
- integrate Artifacts;
- request verification.

A WorkItem is not automatically a Host Task.

### Claim

A proposition currently under consideration. It must distinguish:

- proposed;
- supported;
- contradicted;
- accepted for local planning;
- superseded;
- rejected.

A Harness-local accepted Claim is not a domain Fact.

### Unknown

An explicit missing fact, ambiguity, unresolved conflict, or blocked decision that affects current work or completion.

Unknowns are important because transcript systems often erase them during summarization.

### EvidenceRef

A bounded reference to an Observation, Artifact, source object, Tool receipt, Child Run result, or verification record. Large content remains outside the graph.

### Decision

A retained local selection or resolution with alternatives, evidence references, and scope. Consequence-bearing decisions still require Host or domain admission.

### ActorRun

A reference to the current Run, Child Run, verifier, or other participant relevant to delegation and result ownership.

### EffectProposal

A pointer to a proposed external observation or change. It is kept distinct so graph manipulation cannot commit physical effects.

### VerificationResult

A reference to an independent or domain-specific verification decision.

## 3. Minimum edge families

The first experiment should begin with:

```text
refines
part_of
depends_on
blocks
supports
contradicts
derived_from
assigned_to
produced_by
requires_verification
supersedes
satisfies
```

Every edge must define:

- source and target node types;
- owner;
- creation event;
- optional evidence references;
- invalidation or supersession behavior;
- whether it participates in readiness or completion.

Edges are not free-form tags in the admitted core path.

## 4. Event families

Candidate append-only events:

```text
cognitive.node-created
cognitive.edge-created
cognitive.status-changed
cognitive.node-superseded
cognitive.working-set-pinned
cognitive.working-set-released
cognitive.branch-created
cognitive.child-run-requested
cognitive.child-run-bound
cognitive.child-result-admitted
cognitive.effect-proposed
cognitive.evidence-attached
cognitive.conflict-recorded
cognitive.join-resolved
cognitive.completion-proposed
```

The first implementation should use fewer events if several changes can be one atomic `CognitiveMutation` event without losing independent recovery decisions.

## 5. CognitiveMutation

A mutation proposal has:

```text
mutation_id
harness_run_id
expected_graph_revision
engine_session_ref
working_set_digest
creates
relates
status_updates
supersessions
activations
releases
child_run_requests
effect_proposal_refs
rationale_ref optional
created_at
```

Admission checks:

1. the Run Contract and Assignment generation remain current;
2. `expected_graph_revision` equals the current revision;
3. all referenced nodes and objects exist and match digests;
4. the Engine may write only within its granted Run or branch scope;
5. relation source/target types are valid;
6. no completed or immutable object is silently rewritten;
7. status transitions are legal;
8. budget and graph-size limits are respected;
9. Effect proposals do not masquerade as admitted effects;
10. completion proposals reference the required evidence and unresolved Unknowns.

## 6. Working Set

A Working Set is a reproducible materialization specification, not merely the generated prompt.

```text
WorkingSet
  run_id
  graph_revision
  objective_nodes
  active WorkItems
  selected Claims and Unknowns
  EvidenceRefs
  Child Run results
  Tool and capability view
  source and world revisions
  omission summary
  token/materialization budget
  selection method and version
  digest
```

The compiler may use:

- graph traversal;
- recency;
- readiness;
- evidence dependency;
- semantic retrieval;
- explicit pinning;
- branch ownership;
- source locality;
- model-specific formatting.

The compiler must report omissions or bounded selection metadata sufficiently for evaluation and recovery.

## 7. Context program

A model-facing programmable Context environment may expose:

```python
ctx.search(query, scope=None)
ctx.read(ref, range=None)
ctx.neighbors(node_id, relation=None)
ctx.path(source, target, max_depth=None)
ctx.compare(refs)
ctx.pin(refs)
ctx.materialize(refs, budget)
ctx.delegate(objective, context_grant, budget, tool_grant)
```

These operations query immutable or versioned state. They do not grant external effect authority.

A Python or other REPL may implement the interface, but the kernel state is replaceable. Required state transitions must be emitted as typed mutations or Artifacts.

## 8. Run Actor model

```text
RunActor
├── immutable HarnessRunContract
├── current graph revision
├── mailbox head
├── activation lease
├── HarnessRevision ref
├── EngineSession binding
├── WorkingSet refs
├── ChildRun refs
├── active Effect refs
├── remaining budgets
├── wakeup conditions
├── cancellation intent
└── CompletionProposal ref
```

A Supervisor may activate zero or more ready Run Actors under capacity. The Supervisor owns scheduling policy; Host owns Task Assignment; Runtime owns physical admission.

## 9. Child Run model

A Child Run is created through a bounded delegation contract:

```text
parent_run_ref
delegation_id
objective_ref
context_grant
ToolGrant
budget
deadline
expected result schema
evidence requirements
join policy
```

The Child receives only its granted Working Set and capabilities. It returns bounded Artifacts, Claims, Unknowns, and a ChildCompletionProposal. The parent admits or rejects these into its graph.

Promotion to a Host Task occurs only when the branch needs independent:

- commitment or responsible participant;
- authority or consequence scope;
- scheduling and recovery outside the parent Run;
- verification and Outcome;
- lifetime beyond the parent Assignment.

## 10. Branch and join

A branch creates independent WorkItems or Child Runs from one graph revision. A join is an explicit integration decision, not concatenation of summaries.

Join policies may be:

```text
all_required
first_verified
quorum
compare_and_select
merge_non_conflicting
manual_or_responsible_decision
```

A join records:

- required branch results;
- missing or cancelled branches;
- conflicts;
- evidence used;
- selected and rejected claims;
- resulting graph changes.

## 11. Effect Broker

A cognition Engine may freely inspect and transform Run-local state within its grant. External observations and changes must use an Effect Broker:

```text
EffectProposal
→ ToolGrant and capability check
→ current source/world binding
→ Host consequence admission when required
→ Effect and Dispatch identity
→ Runtime or domain adapter
→ Observation / Artifact / UNKNOWN
→ verification
→ graph update
```

This boundary prevents an RLM or Python kernel from turning arbitrary code execution into hidden authority.

## 12. Graph-family separation

### Host Commitment Graph

Nodes: Goal, Task, Task Attempt, Assignment, DecisionRequest, Verification, Outcome.  
Edges: depends_on, assigned_to, blocked_by, requires_decision, verified_by, satisfies, supersedes.

### Harness Cognitive/Run Graph

Nodes: Objective, WorkItem, Claim, Unknown, EvidenceRef, Decision, ActorRun, EffectProposal.  
Edges: refines, supports, contradicts, blocks, assigned_to, derived_from, requires_verification.

### Runtime Physical Causality Graph

Nodes: Workspace, SourceSnapshot, Job, Attempt, Worker, WorkerCall, Artifact, process identity.  
Edges: forked_from, admitted_as, attempted_by, produced, cancelled_by, reconciled_by.

### Cross-layer provenance

Cross-layer links use immutable references and digests. A graph projection can display the combined path, but no combined mutable database owns all facts.

## 13. Core invariants

1. **event authority** — no projected relation exists without an admitted event and referenced object;
2. **revision fencing** — stale mutations cannot commit;
3. **scope confinement** — an Engine writes only within its Run/branch grant;
4. **effect separation** — graph mutation cannot establish physical execution;
5. **evidence distinction** — Claim, Observation, Verification, and Fact remain distinct;
6. **terminal monotonicity** — completed or abandoned branches are not silently reopened;
7. **explicit conflict** — contradictory claims may coexist until a declared resolution;
8. **bounded materialization** — every model-visible view has a digest and budget;
9. **replaceable Session** — Engine Session loss does not erase committed graph state;
10. **deletion readiness** — unused node/edge types can be removed without rewriting authoritative history.

## 14. Storage choice

The logical model can initially use the existing Harness Journal and CAS:

- events in SQLite;
- immutable node payloads and large content references in CAS;
- a materialized adjacency/index projection for queries;
- no independent graph service;
- no cross-repository database.

Only measured query or concurrency pressure may justify another storage engine.
