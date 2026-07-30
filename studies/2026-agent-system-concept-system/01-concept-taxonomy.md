# Concept Taxonomy

Agent-system vocabulary becomes manageable when separated across orthogonal axes.

## 1. System components and containers

| Concept | Definition | Primary owner |
|---|---|---|
| Model | Probabilistic inference component that transforms Context into output | model provider / Model Runtime |
| Model Runtime | Serving infrastructure for model inference, batching, KV state, routing, and hardware | provider or local inference stack |
| Harness | Cognitive control layer that compiles Context, invokes the Model, interprets outputs, exposes Tools, and runs the Agent loop | Harness implementation |
| Interaction Host | Process or service that hosts Harness Sessions and exposes them to UI clients | product Host |
| Ordivon Host | Durable semantic control plane for Goals, Tasks, Assignments, Task Attempts, waits, decisions, completion, and recovery | `ordivon-host` |
| Execution Runtime | System that owns Workspace, Job, process, execution observation, cancellation, Artifact, and physical recovery | `ordivon-runtime` or another backend |
| Sandbox | Isolation boundary for files, process, network, credentials, and resources | execution provider |
| Workspace | Version-bound operational address space used by a Job or Runtime Attempt | Runtime/backend |
| Surface | Web, mobile, CLI, IDE, or API through which participants observe and direct work | product/UI |
| World | Domain-owned state and transition authority against which actions have meaning | Game, Security experiment, external provider, physical environment |

## 2. Durable work objects

| Object | Meaning | Authority |
|---|---|---|
| Participant | Actor, institution, resource owner, verifier, or system role with identity and scoped relationships | domain / Host |
| Goal | Desired world condition with constraints, commitments, and completion evidence | Host |
| Plan | Current hypothesis for reaching a Goal; revisable and not automatically durable truth | Harness working state |
| Task | Durable semantic work contract that advances a Goal | Host |
| Task Graph | Typed dependencies and relations among Tasks | Host |
| Ready Frontier | Tasks currently admissible for assignment | Host |
| Assignment | Lease-bound delegation of one Task to an Agent worker and execution environment | Host |
| Task Attempt | One semantic exploration or execution path through a Task | Host, with Harness/Runtime evidence |
| Runtime Attempt | One bounded physical dispatch history owned by a Runtime Job | Runtime/backend |
| Run | One concrete Harness execution under an Assignment; framework-specific term | Harness/Host binding |
| Turn | One bounded unit of Agent work initiated by input | Harness |
| Step | One model, Tool, state, or control transition inside a Turn | Harness |
| Effect | Stable semantic commitment candidate to observe or change a world object | semantic commitment layer |
| Dispatch | One concrete attempt to deliver an Effect through a bound Tool contract | Host/commitment layer |
| Job | Backend execution-control object | Runtime/backend |
| Process | Operating-system execution object | OS/Runtime |

## 3. Cognitive and knowledge objects

| Concept | Meaning | Authority |
|---|---|---|
| Context | Bounded selected view supplied to one Model invocation | Harness compiler |
| Working Memory | Active hypotheses, local plan, recent observations, and unresolved state for a Run | Harness |
| Episodic Memory | Retrieved record of prior trajectories or experiences | knowledge/memory service |
| Semantic Memory | Stable reusable facts and project knowledge | knowledge store, subject to verification |
| Procedural Memory | Reusable method such as Skill, Workflow, or playbook | Skill/Workflow registry |
| Skill | Reusable knowledge and procedure for accomplishing a class of work | Harness consumes; registry stores |
| Instruction | Normative or advisory text supplied to a Context | authoring source / Harness selection |
| Reflection | Post-trajectory analysis that may propose improved knowledge or policy | Harness/Eval |
| Consolidation | Evidence-based conversion of trajectories into durable knowledge or Skills | knowledge/evaluation pipeline |

## 4. Capabilities and extensions

| Concept | Meaning |
|---|---|
| Tool | Executable interface with declared input, output, error, and side-effect semantics |
| Tool Contract | Versioned normalized executable interface revision |
| Adapter | Translation between one semantic interface and a provider-specific interface |
| Connector | Adapter and credentials that expose an external system as Tools or resources |
| Capability Manifest | Machine-readable declaration of supported operations and properties |
| Registry | Directory of Models, Harnesses, Skills, Tools, Runtime nodes, or providers |
| Discovery | Process of finding relevant capabilities at runtime |
| Broker | Routing and compatibility layer between caller and concrete providers |
| Plugin | Distribution package containing Skills, Tools, Connectors, Hooks, UI, or configuration |

## 5. Control mechanisms

| Mechanism | Semantics |
|---|---|
| Loop | Repeated controller that observes state, chooses work, acts, and updates state |
| Graph | Typed state structure whose nodes and edges require a controller to advance |
| Workflow | Reusable declared process or graph template |
| Scheduler | Selects when and where admitted work runs |
| Router | Selects a Model, Harness, Tool, provider, or participant |
| Reducer | Combines typed updates into authoritative state |
| Hook | Lifecycle extension point that runs at a defined moment |
| Middleware | Wrapper around an invocation for retry, auth, cache, tracing, or transformation |
| Interceptor | Mechanism that inspects, modifies, replaces, or blocks a call |
| Policy | Decision function over actor, action, resource, context, and consequence |
| Guardrail | Local validation of input, output, or Tool use |
| Approval | Explicit permission from an authority before a proposed action proceeds |
| Watchdog | Detects lack of progress, unhealthy repetition, or missed deadlines |

## 6. Messages and state changes

| Concept | Meaning |
|---|---|
| Command | Request that a component perform an operation |
| Query | Read-only request for current state |
| Update | Request to change durable state and return acceptance or rejection |
| Signal | Asynchronous information delivered to a running object |
| Event | Immutable statement that something already happened |
| Trigger | Condition or schedule that creates new work |
| Interrupt | Durable suspension while awaiting external input or condition |
| Resume | Continuation from an identified checkpoint and authoritative current state |
| Handoff | Transfer of current conversational or cognitive control |
| Delegation | Parent retains responsibility while assigning a bounded subproblem |
| Escalation | Routing unresolved responsibility to a more appropriate authority or capability |

## 7. Durability and coordination

| Concept | Meaning |
|---|---|
| Checkpoint | Minimum state sufficient to continue execution after interruption |
| Snapshot | Point-in-time complete or bounded state view |
| Journal | Append-only sequence of state-changing records |
| Replay | Reconstruction or re-execution from recorded state |
| Lease | Time-bounded ownership or execution right |
| Heartbeat | Periodic evidence that a worker remains alive and making progress |
| Fencing Token | Monotonic generation that prevents a stale owner from committing |
| Idempotency Key | Stable key used to deduplicate repeated operation requests |
| Compensation | New action that counteracts an earlier external effect |
| Saga | Long transaction coordinated through steps and compensations |
| Dead-letter Queue | Quarantine for repeatedly unprocessable work or messages |
| Tombstone | Durable marker that an object was deleted, superseded, or retired |
| Backpressure | Feedback that slows producers when consumers cannot keep up |
| Circuit Breaker | Temporary refusal to call a persistently failing dependency |
| Bulkhead | Resource isolation that limits blast radius |

## 8. Evidence and observability

| Concept | Meaning |
|---|---|
| Observation | Immutable reading of external state with provenance |
| Artifact | Durable content-bearing output |
| Claim | Proposition proposed for evaluation |
| Verification | Recorded evaluation of a Claim using declared evidence and method |
| Fact | Bounded Claim admitted by an authority through Verification |
| Evidence | Material used to support or reject a Claim or completion criterion |
| Provenance | Causal and source path from work to result |
| Lineage | Transformation path among data or Artifacts |
| Trace | End-to-end causal execution record |
| Span | Timed operation within a Trace |
| Log | Diagnostic record |
| Metric | Aggregated numerical observation |
| Audit Record | Who performed what action under which identity and authority |

## 9. Evaluation objects

| Concept | Meaning |
|---|---|
| Eval | Test of one behavior, property, or capability |
| Benchmark | Stable comparable collection of Evals |
| Judge | Component that scores or classifies a result |
| Critic | Component that searches for deficiencies before completion |
| Arbiter | Component that resolves conflicting proposals or evidence |
| Canary | Small real traffic or workload exposure to a new variant |
| Shadow | Parallel execution whose output does not affect production state |
| Dry Run | Full planning or request generation without external commitment |
| Simulation | Execution in a controlled substitute world |
| Counterfactual Replay | Fork from a checkpoint under a changed model, policy, or Tool |

## 10. Cross-cutting invariants

The following are not owned by one layer, but each layer must preserve them at its boundary:

```text
identity
version binding
authority
explicit uncertainty
provenance
reversibility and consequence
recovery
schema compatibility
cost and budget
privacy and secret handling
```

## 11. One-line distinctions

```text
Goal: what world condition matters.
Plan: the current hypothesis for reaching it.
Task: a durable work contract.
Graph: relations among durable or local objects.
Loop: the controller that advances state.
Skill: reusable method and knowledge.
Tool: executable capability.
Hook: deterministic lifecycle extension point.
Event: immutable fact that something happened.
Harness: cognitive episode and Tool-use loop.
Host: durable work and assignment control.
Runtime: physical execution and execution evidence.
```
