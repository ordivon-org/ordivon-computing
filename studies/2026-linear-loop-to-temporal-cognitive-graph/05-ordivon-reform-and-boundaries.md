# Ordivon Reform and Boundaries

## 1. Reform statement

The reform is not “add graphs” or “add more Agents.” It is:

> Change the Harness's principal cognitive state from a serialized transcript to a versioned temporal relation state, while retaining the transcript as evidence and interface and retaining Host/Runtime authority boundaries.

The principal computation changes from:

```text
next turn over message history
```

into:

```text
select local view
→ reason
→ propose typed state transformation, delegation, or Effect
→ admit and verify
```

## 2. Host reform

### 2.1 Preserve the kernel

Retain:

- Task Journal/CAS;
- exact revision and lease fencing;
- immutable descriptors and references;
- consequence and Effect commitment;
- DecisionRequest;
- VerificationReceipt;
- conservative recovery;
- terminal TaskOutcome.

### 2.2 End cognition duplication

No new production Provider or model loop should be added to Host. Existing closed-choice and open-proposal cognition paths become:

- compatibility and deterministic fixtures;
- schema/admission references;
- migration sources.

New model execution enters through the independent Harness boundary.

### 2.3 Promote External Executor from seam to production lifecycle

The Host should:

```text
admit immutable ExternalExecutionRequest
→ submit to Harness service
→ bind foreign Run quickly
→ observe revisions
→ request cancellation
→ recover after either side restarts
→ collect CompletionProposal
→ verify and decide Outcome
```

It should not execute the complete foreign Run inside `start()`.

### 2.4 Keep cognitive branches out of Host by default

A Harness-local branch becomes a Host Task only when it introduces independent commitment, authority, scheduling, responsible ownership, verification, or lifetime.

This prevents the Host Task graph from becoming a dump of transient model thoughts.

### 2.5 Revisit Frontier only after Actor evidence

Host's current `ready_frontier` is workload-local and does not make Host a graph scheduler. Do not redesign TaskProjection first. After Harness Actor experiments, determine whether coarse Commitment Graph dependencies need a separate Host projection or can remain extension-local.

## 3. Harness reform

### 3.1 One production persistence owner

The independent Harness Journal/CAS becomes the only writer for new Run cognition and lifecycle state. The Host-backed path becomes read/migrate/recover compatibility and receives no new cognitive features.

### 3.2 Introduce `HarnessExecutionEngine`

```python
class HarnessExecutionEngine(Protocol):
    def create_session(...): ...
    def activate(...): ...
    def observe(...): ...
    def send_message(...): ...
    def request_cancel(...): ...
    def recover(...): ...
    def collect_completion(...): ...
```

Implementations:

- `SequentialEngine` wraps current `OrdivonAgentLoop`;
- `PrimeRpcEngine` or another external Engine provides experimental RLM/recursive behavior;
- `NativeCognitiveGraphEngine` is built only after TCG ablations justify it.

### 3.3 Make Run a durable Actor

Add a Supervisor and Run Actor projection with activation lease, mailbox, wakeup, Engine Session binding, Child Runs, budgets, and recovery. A daemon is justified here because a synchronous call cannot represent detached persistent execution.

### 3.4 Add graph state in shadow mode first

The first TCG path derives candidate nodes and relations from existing messages, Tool Steps, observations, and Artifacts without changing Engine input or production behavior.

This tests whether the projection is stable and useful before it becomes authoritative cognitive state.

### 3.5 Move to explicit Working Sets

After shadow validation, compile model context from graph/object references. Messages remain available as one source and UI view, but no longer define the complete current state.

### 3.6 Add Child Runs after single-Actor graph value

Do not use multi-Agent parallelism to hide a weak state model. First show that one Actor with explicit Claims, Unknowns, Evidence, and Working Sets improves continuation or cost. Then add bounded Child Runs and joins.

### 3.7 Add governed HarnessRevision

Represent:

```text
HarnessRevision
  base revision
  prompt bundle refs
  Engine and subagent specs
  Skill refs
  memory refs
  Context policy ref
  Tool catalog compatibility
  evaluation and activation receipts
```

A refinement is a proposal, never an in-place mutation of the active Harness.

## 4. Runtime reform

### 4.1 Retain Job/Attempt truth

Do not move model, Task, Run, or completion semantics into Runtime.

### 4.2 Add immutable input materialization if needed

Large Context objects should enter an execution environment through digest-bound read-only inputs, not argv, environment variables, or oversized MCP requests.

Candidate local objects:

```text
InputArtifactRef
InputMaterialization
InputMountReceipt
```

### 4.3 Add Workspace snapshot/fork if parallel mutation proves necessary

A Child Run should receive an independent source state:

```text
parent sourceStateDigest
→ immutable snapshot or exact revision
→ child Workspace
→ patch/Artifact/result
→ explicit merge and verification
```

Do not permit multiple Child Runs to mutate one Workspace concurrently.

### 4.4 Add Worker only after terminal-Job ablation

A persistent Worker is justified for IPython kernels, language servers, simulators, or Agent daemons only when repeated terminal Jobs produce material overhead or lose necessary continuity.

Runtime Worker owns physical lifecycle only:

```text
worker_id
Workspace and source binding
execution profile
process identity
endpoint
resource budget
heartbeat
state and reconciliation
```

Each interaction remains an idempotent WorkerCall with request identity and result/UNKNOWN semantics.

### 4.5 Keep queueing outside Runtime

Runtime should continue immediate capacity admission. Harness Supervisor owns pending Run/branch scheduling and may react to holder identities.

## 5. Verifier and domain reform

### 5.1 Verify end state, not cognitive style

The candidate graph should improve accepted outcomes and evidence. A verifier should not reward the mere presence of more nodes, branches, or explanations.

### 5.2 Add process diagnostics separately

Evaluation may measure:

- unsupported Claim rate;
- stale Evidence use;
- unresolved Unknowns at completion;
- duplicate branch work;
- conflict-resolution quality;
- recovery fidelity;
- Effect-policy violations.

These diagnose the Harness but do not replace end-state acceptance.

### 5.3 Protect the evaluator boundary

Harness refinement cannot edit:

- held-out tasks;
- verifier code or configuration;
- reward calculation;
- authority policy;
- evidence retention;
- canary and rollback criteria.

## 6. Computer reform

Computer should own:

- the derivation and falsifiers;
- the question and relation map;
- experiment contracts and evidence comparison;
- promotion/deletion decisions;
- shared terminology only after proof.

Computer should not own:

- the production graph database;
- Run scheduling;
- live Harness configuration;
- Runtime Worker management;
- a central research or architecture control plane.

## 7. Product-level benefits

If validated, the reform provides:

### Better effective context

The model receives the smallest relevant subgraph instead of repeated full transcript materialization.

### Explicit open work

Unknowns, conflicts, branches, blockers, and evidence remain visible across compaction and model replacement.

### Safe parallelism

Child Runs have scoped Context, Tools, budgets, Artifacts, and join rules.

### Stronger recovery

A fresh Engine can continue from committed graph state rather than reconstructing intent from a transcript summary or hidden Session.

### Better attribution

Evaluation can distinguish model, Engine, Context compiler, graph mutation, Tool, Runtime, and verifier contributions.

### Safer adaptation

Harness changes become versioned evaluated candidates instead of self-modifying ambient state.

### Lower repeated work

Pinned evidence and explicit relations can reduce repeated repository reads, duplicate searches, and “game of telephone” summaries.

### Multiple cognitive Engines

Sequential, RLM, recursive Harness, or future model-native Engines can share Run/Effect/verification boundaries without flattening their internals.

## 8. Costs and risks

### Formalism tax

More objects may cost more than repeated reading. The experiment must measure graph write/read overhead and operator comprehension.

### Schema churn

Premature node/edge types can fossilize one reasoning style. Start minimal and local.

### Extraction error

A model may create incorrect Claims or relations. Graph structure does not make content true.

### Staleness

A relation may outlive its source revision. Every EvidenceRef requires version and invalidation semantics.

### Coordination overhead

Child Runs can consume far more tokens and create integration work.

### Shared-state contention

Parallel Actors can race graph revisions. Use branch scopes, immutable results, and explicit joins rather than unrestricted shared writes.

### Reward hacking

A self-improving Harness may optimize graph metrics, evaluator quirks, or environment exploits. Use external held-out verification.

### Over-centralization

A universal graph can erase authority boundaries. Keep graph families and ownership distinct.

## 9. Net-acceleration condition

The reform is retained only when:

```text
verified outcome gain
+ recovery gain
+ operator-attention reduction
+ reusable trajectory value
>
model/token cost
+ graph maintenance
+ coordination overhead
+ schema and migration cost
+ new failure surface
```

No qualitative appeal to “global cognition” overrides this condition.
