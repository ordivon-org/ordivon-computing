# First-Principles Derivation

## 1. Begin with the physical fact

A foundation model does not continuously inhabit the complete Task world. At inference time it receives a finite token sequence and produces a finite continuation or structured output.

```text
materialized context C_t
→ model inference M
→ output Y_t
```

Self-attention can connect positions inside `C_t`, but it cannot attend to:

- an omitted repository object;
- a Tool result that has not been fetched;
- another Agent's private Session;
- an unmaterialized Artifact;
- a Runtime process fact outside the request;
- a future world transition;
- state lost when the process or provider Session disappears.

Therefore:

> Global attention is global only inside a selected local view.

## 2. Agent work is not one inference

An Agent Task changes an external or durable state through repeated interaction:

```text
world / source state
→ observation
→ bounded cognition
→ proposal
→ admitted effect
→ physical execution
→ new observation
→ verification
→ revised work state
```

The Task can outlive every individual model invocation. Hence the state required to continue work cannot exist solely in the current prompt or KV cache.

## 3. Why a transcript is initially sufficient

For short, mostly sequential work, the transcript provides four useful properties:

- temporal order;
- simple replay;
- direct compatibility with chat-trained models;
- low implementation cost.

A thin Tool-calling loop can therefore solve real tasks with:

```text
messages + observations + remaining budget
```

Ordivon correctly chose this as its first Harness baseline.

## 4. The transcript's structural compression

A transcript serializes several distinct things into one sequence:

- facts and unsupported claims;
- current objectives and obsolete objectives;
- open branches and closed branches;
- evidence and interpretations of evidence;
- parent and child work;
- Tool requests and physical receipts;
- plans and execution commitments;
- current state and historical explanation.

The system can recover order, but must repeatedly infer the live structure from prose.

Let `H_t` be the complete transcript after turn `t`. The next invocation behaves approximately as:

```text
Y_t = M(materialize(H_t))
H_(t+1) = append(H_t, Y_t, O_t)
```

As `H_t` grows, one of four things happens:

1. it is passed in full and consumes attention and cost;
2. it is truncated and loses state;
3. it is summarized and may erase distinctions or provenance;
4. it is retrieved in chunks and may miss dynamic relations.

None is a complete persistent work model.

## 5. Open work is partially ordered, not totally ordered

Many real tasks contain simultaneous relations:

```text
Hypothesis A supported by Evidence A1
Hypothesis A contradicted by Evidence A2
Subproblem B independent of Subproblem C
Experiment D blocked by Runtime Job E
Claim F requires Verification G
Child Run H owns one bounded investigation
```

A transcript imposes a total order on their descriptions even when the underlying work is a partial order or graph.

A total event order remains necessary for causality and recovery. But the current semantic state must preserve relations directly instead of forcing every later model to reconstruct them from the total order.

Therefore the minimum persistent form is:

```text
ordered causal history + relational current projection
```

not one or the other.

## 6. Why “just use a longer context” is insufficient

Increasing the context window reduces some truncation but does not remove:

- distractor interference;
- uneven utilization by position;
- repeated aggregation cost;
- stale facts mixed with current facts;
- inability to grant different Child Runs different views;
- lack of typed provenance;
- recovery dependence on prompt reconstruction;
- authority confusion between proposal and committed effect.

Long context is a larger working memory surface. It is not a durable Task database or cognitive-state authority.

## 7. Why “just add RAG” is insufficient

Static retrieval answers “which chunks are similar to this query?” It does not intrinsically represent:

- which claim a chunk supports or contradicts;
- whether the source revision is still current;
- whether a branch is resolved;
- which Agent owns the branch;
- whether a result has been independently verified;
- which Effect produced an Artifact;
- which unknown blocks completion.

Retrieval remains valuable as a query mechanism over objects. It is not the complete relation and lifecycle model.

## 8. Why “just add subagents” is insufficient

Subagents add parallel context windows, but without durable relation and ownership state they introduce:

- duplicated work;
- incompatible assumptions;
- lost findings;
- opaque cancellation;
- unbounded token use;
- parent-child context drift;
- “game of telephone” summaries;
- unclear completion and verification.

Parallelism scales both useful exploration and coordination failure. A Child Run must have an explicit delegation scope, budget, context grant, returned Artifact/evidence, and parent admission rule.

## 9. Why a universal workflow graph is also insufficient

A declared workflow graph assumes that the relevant steps and transitions are known before execution. Open cognition must be able to:

- discover a new hypothesis;
- abandon a branch;
- create a new investigation;
- revise a plan after evidence;
- defer an Effect;
- ask for a decision;
- create a Child Run dynamically.

Classical workflow systems remain appropriate for stable declared processes. They do not replace a revisable cognitive state model.

## 10. Deriving the minimum state split

Persistent work requires four separations.

### 10.1 Event versus projection

```text
Event: what was proposed, admitted, observed, superseded, or resolved
Projection: what is currently active and related
```

Events preserve causality. Projection accelerates current reasoning.

### 10.2 Content versus relation

```text
Content object: source text, Artifact, report, code, observation
Relation: supports, contradicts, depends_on, derived_from, delegated_to
```

Large bytes remain in CAS or Artifact storage. The graph carries bounded typed references.

### 10.3 Global Run state versus local Working Set

```text
Run graph: all retained operational cognitive objects
Working Set: bounded current view selected for one invocation
```

The model reasons densely over the view without receiving every retained object.

### 10.4 Cognitive proposal versus external effect

```text
CognitiveMutation: changes Run-local interpretation and work structure
Effect proposal: may change or observe external reality
```

Only the latter crosses authority, Tool binding, Dispatch, Runtime, and verification boundaries.

## 11. Deriving typed mutation

If a model directly rewrites a graph, stale or conflicting output can silently overwrite newer state. Therefore every change must be a proposal with an expected revision.

```text
read graph revision r
→ compile Working Set V_r
→ invoke Engine
→ receive CognitiveMutation(expected=r)
→ validate object types, references, scope, and invariants
→ reject if current revision ≠ r
→ append admitted events
→ project revision r+1
```

This is the cognitive analogue of Host revision fencing and Runtime request identity.

## 12. Deriving Run Actors

Once branches can wait, receive messages, own budgets, and survive process loss, a Run is no longer adequately represented as one synchronous function call.

It needs:

- immutable Run Contract;
- durable revision;
- mailbox;
- activation lease;
- Engine Session binding;
- wakeup conditions;
- Child Run references;
- active Effect references;
- cancellation intent;
- completion proposal;
- recovery assessment.

This is a persistent Run Actor. It remains Assignment-scoped and does not imply a universal scheduler.

## 13. Deriving multiple graph families

One graph cannot safely own all facts because different layers have different authority and lifecycle rules.

```text
Host Commitment Graph
  semantic work and consequence authority

Harness Cognitive/Run Graph
  revisable cognition and delegation

Runtime Physical Causality Graph
  physical execution and Artifact lineage

Domain truth graph or state machine
  authoritative world semantics
```

Cross-layer links are immutable references, not shared mutable ownership.

## 14. Deriving evidence-governed adaptation

If Harness behavior can change from trajectories, the changed configuration itself becomes a versioned work product.

```text
trajectory evidence
→ RefinementProposal
→ static and permission diff
→ replay / shadow evaluation
→ holdout and adversarial evaluation
→ admission
→ HarnessRevision activation
→ canary
→ rollback or promotion
```

The Agent may propose changes to prompts, skills, memory, or subagent specifications. It cannot self-authorize changes to authority, permissions, verifier, reward, audit, or immutable evidence.

## 15. Final derived architecture

The complete control loop becomes:

```text
Host Task commitment
→ Harness Run Actor
→ current Temporal Cognitive Graph
→ Context Compiler selects Working Set
→ Engine performs local dense reasoning
→ typed CognitiveMutation / ChildRun / Effect proposals
→ Harness structural admission
→ Host consequence admission where required
→ Runtime physical execution
→ Observation / Artifact
→ independent Verification
→ graph and Task updates
→ continue, branch, wait, join, complete, or stop
```

The architecture is justified only if it produces more accepted verified work per unit of time, token, operator attention, and system complexity than the current transcript-centered baseline.
