# The Agent-Native Responsibility Overlay

## 1. Overlay, not replacement stack

The following responsibilities sit above and across the classical substrate. They are not a second operating system and do not imply that every product needs eight services.

```text
R0 Human purpose and consequence ownership
R1 Operator attention and governance
R2 Open-work continuity and task frontier
R3 Context and memory compilation
R4 Cognition and coordination
R5 Authority and consequence admission
R6 Effect commitment and reconciliation
R7 Evidence, verification, and epistemic state
                     ↓
classical processes, workflows, databases, networks, and isolation
```

The ordering is explanatory, not a strict call stack. Evidence can revise context; authority can require human governance; a world observation can create new tasks. The real structure is a feedback graph.

## 2. R0 — Human purpose and consequence ownership

### Subject

Why the system is acting, which tradeoffs matter, and who remains responsible for consequences.

### Stable objects

- Goal or desired world condition;
- preferences and constraints;
- non-goals;
- completion evidence;
- consequence owner;
- decision records for irreversible or value-laden choices.

### Why classical mechanisms do not own it

A Kubernetes `spec` can encode a desired cluster state [C07], but it does not determine which human objective deserves priority. A database can store a preference but cannot assume responsibility for its moral, economic, or social consequence.

### Agent-era change

Agents make more intermediate decisions, so human purpose cannot remain only in the operator's memory or the first prompt. It must persist in a form that later model episodes and reviewers can challenge.

### Non-goal

Ordivon does not decide human values. It preserves the declared purpose, uncertainty, and decision boundary.

## 3. R1 — Operator attention and governance

### Subject

Which situations require human attention, what evidence the operator needs, and which bounded work may continue autonomously.

### Stable objects

- decision queue;
- escalation reason;
- reversibility and consequence class;
- alternatives and evidence;
- approval, rejection, redirection, or stop decision;
- notification and attention budget.

### Why it changes

Per-action approval does not scale with Agent throughput and can create approval fatigue [A13]. OpenAI's agent-first engineering experience similarly treats human time and attention as the scarce resource [A01].

### Classical overlap

Alerting, incident management, access approval, and workflow human tasks already exist. The Agent-native gap is selecting meaningful intervention points when the action path is generated dynamically and the operator cannot inspect every model turn.

### Admission test

A separate governance layer is justified only if it reduces human intervention while preserving or improving accepted-result quality and consequence control.

## 4. R2 — Open-work continuity and task frontier

### Subject

What work remains true and actionable when models, processes, contexts, providers, and individual Attempts are replaced.

### Stable objects

- Goal binding;
- Task identity;
- Attempt and branch identity;
- dynamic dependencies;
- current ready frontier;
- waits and blockers;
- completion or abandonment criteria;
- checkpoint sufficient for continuation.

### Critical narrowing

Durable Job and Workflow identity are classical capabilities [C06][C08]. R2 exists only for work whose semantic decomposition is revised through cognition and evidence.

```text
predeclared durable workflow
  exact or bounded control logic is already program state

open-work continuity
  task meaning, hypotheses, dependencies, and next action evolve at runtime
```

### Failure if omitted

- a new model repeats completed work;
- a failed Attempt erases useful evidence;
- the latest conversation summary becomes the only source of task truth;
- process completion is mistaken for Goal completion;
- changing one hypothesis silently invalidates dependent work.

## 5. R3 — Context and memory compilation

### Subject

Which subset of durable world and task state should influence one model invocation.

### Stable objects

- source identities and revisions;
- selected facts, claims, artifacts, and task state;
- instruction and policy version;
- Tool or capability catalog version;
- omission and compression policy;
- context digest or reproducible selection record;
- invalidation conditions.

### Why storage and sessions are insufficient

Storage keeps a larger state. A model can consume only a bounded selected token state. Sessions preserve conversational history [A03], while context engineering repeatedly chooses from instructions, Tools, history, and external information [A08].

### New invariant

The system must distinguish:

```text
durable state that remains authoritative
from
context selected for one probabilistic episode
```

No critical authority or effect identity may exist only because it happened to remain inside the prompt.

### Temporary-mechanism warning

Specific summarizers, retrieval algorithms, context limits, or reset schedules remain implementation details. The stable responsibility is selection, provenance, and invalidation.

## 6. R4 — Cognition and coordination

### Subject

How the system obtains, compares, routes, and joins probabilistic proposals.

### Stable objects

- model invocation;
- candidate plan, claim, or action;
- role or capability profile;
- branch ownership;
- comparison and Join;
- cost, latency, and evaluation result;
- stopping or escalation decision.

### Agent-era change

The system must schedule information-producing cognition as well as machine resources. It may choose between another search, a new candidate, an independent verifier, a cheaper model, or a human decision.

### Multi-Agent boundary

A2A provides interoperability objects for remote Agents [P03][P04]. It does not determine whether multiple Agents are useful for a specific task. Anthropic's research system shows both breadth-first gains and significant cost and coordination limits [A10].

### Minimal coordination form

```text
shared Goal
→ independent bounded Attempt
→ Artifact / Claim / Evidence
→ explicit Join or comparison
```

Free-form Agent conversation is not required and should not become the system of record.

### Promotion threshold

A general cognitive scheduler should not be frozen until at least two domains show repeated routing, branching, or stopping failures that cannot be solved by local policy.

## 7. R5 — Authority and consequence admission

### Subject

Whether one proposed Effect may be committed now, by this principal, against this world version, within this consequence boundary.

### Stable objects

- principal and delegating authority;
- purpose or Goal binding;
- target identity and expected version;
- capability and operation class;
- consequence envelope;
- resource or financial budget;
- expiry and revocation state;
- approval or policy evidence;
- admission decision.

### Relationship to classical security

Operating-system permissions, credentials, sandboxes, and egress controls remain the physical enforcement substrate. R5 adds a semantic commit decision above them.

```text
OS permission answers:
Can this process write here?

Agent Effect admission answers:
May this delegated work produce this specific change now?
```

Anthropic's containment work shows why both are necessary: deterministic environment boundaries protect against the cases probabilistic safeguards miss [A13].

### Non-goal

Not every read or reversible local change needs a universal authorization language. Admission should be proportionate to consequence.

## 8. R6 — Effect commitment and reconciliation

### Subject

How a stable semantic proposal crosses into classical reality without losing identity under retries, transport loss, replacement, or partial failure.

### Stable objects

- Effect identity;
- target and preconditions;
- declared idempotency and completion semantics;
- Tool or backend contract revision;
- immutable Effect Binding;
- Dispatch identity;
- backend correlation identity;
- result or explicit `UNKNOWN`;
- reconciliation and compensation path;
- durable Artifact references.

### Classical overlap

Distributed systems already use idempotency keys, retries, transactions, and reconciliation. The Agent-native addition is preserving the semantic proposal across model and Tool replacement and preventing probabilistic cognition from inventing the physical history.

### Key invariants

```text
Effect ≠ Dispatch ≠ backend Job
lost response ≠ failed Effect
stable identity ≠ inherent idempotency
a new proposal ≠ retry of the old proposal
```

### Current Ordivon maturity

This is the strongest implemented Ordivon responsibility: Runtime execution and recovery, Host Effect admission and Binding, and the cross-backend Semantic Core experiment provide E4–E5 evidence for bounded slices.

## 9. R7 — Evidence, verification, and epistemic state

### Subject

What the system observed, what is merely claimed, how claims are evaluated, and what can be accepted as current fact.

### Stable objects

- Observation;
- Artifact and provenance;
- Claim and assumptions;
- inference or interpretation;
- Verification method and authority;
- decision and confidence or scope;
- admitted Fact;
- invalidation and supersession relation.

### Why ordinary observability is insufficient

Tracing can show model turns and Tool calls [A05]. It does not by itself establish that an observation supports a claim or that the verifier was independent and authorized.

### Why a universal truth engine is not implied

Different domains require different authorities and methods:

- source code may use tests, static checks, and review;
- finance may require provider lineage and account reconciliation;
- security may require independent observers and sealed evidence;
- design quality may require rubrics and human judgment.

The stable cross-domain structure is the distinction among claim, evidence, verification, and admitted fact—not one universal grader.

## 10. Cross-cutting invariants

The overlay is held together by six cross-cutting invariants:

1. **Identity** — semantic objects survive provider, process, and transport replacement.
2. **Version binding** — context, Tools, world objects, policies, and evidence have observable revisions.
3. **Explicit uncertainty** — unknown outcome or unsupported claim is not coerced into success or failure.
4. **Provenance** — durable results retain their source and causal path.
5. **Reversibility and consequence** — the system distinguishes reversible exploration from durable commitment.
6. **Recovery** — current state can be reconstructed without relying on model memory.

## 11. The closed loop

```text
R0 purpose
→ R2 work frontier
→ R3 context
→ R4 cognition
→ R5 admission
→ R6 effect commitment
→ classical execution
→ R7 evidence and verification
→ R2 revised work
→ R1 human decision when needed
```

This loop is the candidate Ordivon Computer core. Individual products may implement only the responsibilities required by their risk, duration, and domain.
