# Ordivon Against Current Agent-System Paradigms

## 1. Purpose

This chapter compares Ordivon's current hypotheses with the strongest available protocol, workflow, harness, memory, security, evaluation, and multi-Agent baselines.

The goal is not to prove historical priority. Most mature Ordivon formulations were committed after the MCP `2026-07-28` release candidate became public on 2026-05-21 [P05]. The relevant independence claim is narrower:

> Ordivon reached several similar conclusions through first-principles reasoning and production failures before this repository inspected the new MCP design.

Independent convergence increases confidence that a constraint is real. It does not establish originality.

## 2. Classification rule

Each Ordivon claim receives one of four statuses:

- **convergent** — independently reached and strongly aligned with mature external systems;
- **parallel hypothesis** — differs from the mainstream and deserves a fair experiment;
- **corrected** — an earlier formulation was too broad or structurally wrong;
- **unresolved** — evidence is insufficient even to choose between the hypothesis and its strongest baseline.

A claim is not promoted because it sounds coherent. It must identify the failure it prevents, the strongest existing alternative, the additional mechanism it introduces, and the evidence that would justify its cost.

## 3. Convergent claims

### 3.1 Explicit durable identity instead of protocol-session truth

Ordivon uses explicit Workspace, Job, Attempt, Effect, Dispatch, Artifact, Goal, and Task identities. The new MCP core removes protocol sessions and recommends explicit application handles for cross-call state [P05]. LangGraph similarly requires stable thread identity to retrieve checkpoints and resume execution [R01].

The stable conclusion is:

```text
connection state ≠ work state
protocol session ≠ semantic continuity
```

This is highly likely to remain correct. It is not an Ordivon invention.

### 3.2 Cognition and execution are separate replaceable planes

Ordivon Host owns open work, context, model invocation, candidate admission, and verification. Runtime owns physical execution, process identity, durable output, and recovery.

OpenAI separates the model-native harness from sandbox compute [A06]. Anthropic separately describes a brain–hands boundary and warns that harness assumptions should remain replaceable as models improve [A12]. OpenHands also treats sandboxed execution, lifecycle control, models, and user interfaces as composable concerns [R03][R05].

The corrected conclusion is:

```text
cognition plane and execution plane are separable
```

not:

```text
all execution must remain local
```

Local Runtime, remote sandbox, Edge capability, and managed compute are valid implementations when identity, authority, containment, and evidence remain explicit.

### 3.3 Model output is a candidate, not system authority

Ordivon separates Candidate, Authority admission, Effect, Dispatch, Observation, Verification, and accepted Fact. OpenAI Agents SDK similarly separates configured model behavior from Runner, Tool calls, guardrails, sessions, and execution [A02][A04].

This distinction is load-bearing:

```text
plausible model output
≠ authorized action
≠ physical event
≠ verified world claim
≠ completed Goal
```

### 3.4 Context is a compiled view

Anthropic defines context engineering as selecting a finite token state from changing instructions, tools, history, and external data [A08]. MemGPT earlier modeled virtual context management across memory tiers [R04]. Ordivon independently converged on the stronger system boundary:

```text
authoritative durable state
→ selection / retrieval / compression
→ one invocation Context
```

The additional Ordivon emphasis—source revision, Tool-contract revision, trust, omission, invalidation, and authority separation—remains worth testing. The general memory/context problem is not new.

### 3.5 Long work requires explicit artifacts and checkpoints

Anthropic's long-running harness work found that compaction alone was insufficient and used incremental progress plus explicit artifacts across sessions [A09]. OpenAI's agent-first engineering makes repository state, tests, feedback loops, and isolated workspaces central [A01]. LangGraph checkpoints graph state and supports fault tolerance, replay, time travel, and human interruption [R01].

Ordivon's Workspace → Attempt → Artifact → Verification path is therefore strongly supported. Its novelty cannot rest on using Git, checkpoints, or artifacts.

### 3.6 Human attention is scarce

OpenAI treats human time and attention as the scarce resource in high-throughput Agent engineering [A01]. Anthropic observed approval fatigue and shifted toward containment plus lower-friction approval policies [A13]. LangGraph provides durable tool-call interrupts and approval/edit/reject decisions [R02].

Ordivon's useful extension is to measure attention and structure DecisionRequests around consequence, evidence, alternatives, reversibility, and cost of delay. That extension is not yet proven as a shared layer.

### 3.7 Deterministic containment remains necessary

Anthropic reports that model-layer defenses have non-zero miss rates and that sandbox, VM, filesystem, credential, and egress boundaries cap blast radius [A13]. OpenAI and OpenHands also integrate controlled execution environments [A06][R03].

Ordivon correctly separates:

```text
physical containment
from
semantic Effect authority
```

Trusted-local root is a valid single-user profile, not a universal Agent-security architecture.

### 3.8 Agent evaluation must include environment and trajectory

Anthropic's Agent eval guidance evaluates multi-turn systems that call Tools and modify environments, using graders matched to trajectory and outcome complexity [A11]. OpenHands evaluates real software and browsing environments [R03].

Ordivon's receipts, replay, fault injection, domain worlds, and accepted-result metrics align with this direction. A successful process exit or fluent final message cannot establish Goal completion.

## 4. Parallel hypotheses

### 4.1 Agent Effect Commitment Kernel

The strongest mainstream baseline is a Tool call or durable Activity combined with an idempotency key, audit log, retry policy, and guardrail.

Ordivon proposes a stronger path:

```text
Candidate
→ Authority admission
→ Effect
→ immutable EffectBinding
→ Dispatch
→ backend Job or synchronous operation
→ Observation / Artifact
→ reconciliation
→ Verification
```

The candidate novelty is not any individual object. It is the unified semantic commitment boundary for probabilistically generated external actions.

Strongest falsifier:

> A plain MCP Tool or Temporal/LangGraph Activity with ordinary idempotency and audit state provides equal recovery, duplicate-effect prevention, Tool-drift handling, and operator clarity at lower cost.

Status: **high-value parallel hypothesis; requires a second real backend and direct baseline comparison.**

### 4.2 Open-work continuity

Kubernetes, Temporal, and LangGraph already provide durable Job, Workflow, thread, checkpoint, interrupt, and replay semantics [C06][C08][R01]. Generic task durability is not Agent-native.

Ordivon's narrower claim is that a long-lived Goal may span multiple workflow executions while its interpretation, hypotheses, Task frontier, completion evidence, and authority are revised through cognition.

Strongest falsifier:

> The same workload is equally understandable, transferable, and recoverable when these fields are ordinary LangGraph or Temporal workflow state.

Status: **unresolved parallel hypothesis; do not create a separate runtime until the baseline loses.**

### 4.3 Goal- and consequence-bound admission

Classical identity, RBAC, ABAC, capability systems, OAuth scopes, Tool allowlists, sandboxes, and per-call approval already constrain action. Ordivon proposes binding one admitted Effect to delegated purpose, target version, consequence envelope, budget, expiry, and revocation state.

The safe formulation is:

```text
human Goal
→ machine-verifiable narrowing grant
→ commit-time revalidation
```

Natural language cannot directly expand authority.

Status: **credible emerging research direction; first prove value in Finance and Security.**

### 4.4 Epistemic control plane

Ordivon separates Observation, Claim, Evidence, Verification, and domain-admitted Fact. Existing systems already provide logs, traces, provenance, tests, model graders, databases, and knowledge graphs.

The possible cross-domain invariant is the relation among these objects, not one universal truth engine.

Strongest falsifier:

> Domain systems cannot share a useful minimal relation without losing essential local meaning, or ordinary provenance plus evaluation records provide the same benefit.

Status: **medium-potential hypothesis with high over-abstraction risk. Keep domain verification local.**

### 4.5 Operator attention plane

Existing HITL systems can pause a workflow, present Tool calls, and accept approve/edit/reject decisions [R02]. Ordivon proposes a richer DecisionRequest and attention budget.

Strongest falsifier:

> A local product policy and ordinary notification queue achieve equal accepted-result quality and lower human interruption without a shared abstraction.

Status: **high product value, low current justification for Protocol or Kernel promotion.**

### 4.6 Responsibility overlay rather than Agent OS

MemGPT and later Agent systems use operating-system analogies for memory and control [R04]. Ordivon's revised thesis is intentionally narrower: study the complete stack but construct only responsibilities left unowned when probabilistic proposals enter persistent world-changing loops.

This is better treated as a research discipline than a technical invention.

## 5. Corrected or rejected formulations

### 5.1 “Classical computing is deterministic; Agent computing is probabilistic”

Rejected as a binary distinction. Classical systems include concurrency, randomization, distributed races, partial failure, and external uncertainty.

Use instead:

```text
predeclared operational contract
vs
runtime proposal generation by a learned statistical policy
```

### 5.2 Fourteen-layer Agent Computer as an implementation roadmap

Rejected. The full physical-to-institutional map remains a learning route. Mature operating systems, databases, workflow engines, networks, isolation, model runtimes, and compilers remain inherited unless a measured workload proves an unowned invariant.

### 5.3 One monolithic Agent Execution Kernel

Rejected. Open-work control, context compilation, cognition, authority, Effect commitment, physical execution, and epistemic state have different authorities, lifetimes, and failure modes.

### 5.4 Stable identity implies idempotency

Rejected. Stable identity enables correlation. Safe repetition additionally requires declared backend semantics, Dispatch identity, correlation, and reconciliation.

### 5.5 Protocol Task equals internal work truth

Rejected. MCP Tasks and A2A Tasks are interoperability objects [P02][P04][P05]. LangGraph threads are checkpoint namespaces [R01]. None automatically owns the human Goal, Ordivon open-work Task, or Runtime Job.

### 5.6 Models are transparently interchangeable

Rejected. Stable semantic state can survive model replacement, but models require capability profiles, model-specific context and Tool adaptation, and cross-model evaluation. Interface compatibility is not behavioral equivalence [A12].

### 5.7 DAG is the universal execution representation

Rejected. A dynamic DAG is useful for readiness and dependency projection, while loops, state machines, ordinary functions, event histories, and graphs remain valid execution or analysis structures. LangGraph itself offers both graph and functional APIs [R06].

### 5.8 Trusted-local root is the general security route

Rejected. It remains an explicit personal-developer profile. Contained local and remote disposable profiles are required for untrusted code, external content, and higher-consequence work [A13].

### 5.9 Every domain should maintain a complete Host and Runtime

Rejected as a long-term architecture. Independent domain implementations are useful experiments. They should either remain local or become conformance baselines; shared code and Protocol promotion require a second consumer and demonstrated drift cost.

## 6. Novelty statement

Ordivon's individual primitives mostly have clear precedents:

- durable workflow and checkpointing;
- memory tiers and context selection;
- Tool calls and protocol tasks;
- sandboxed execution;
- provenance and evaluation;
- multi-Agent tasks and artifacts;
- identity, authorization, transactions, and idempotency.

The potentially novel research object is the integrated personal work-control loop:

```text
Goal
→ version-bound Context
→ probabilistic Candidate
→ purpose- and consequence-bound admission
→ recoverable Effect commitment
→ classical execution
→ evidence and domain Verification
→ revised open work or human Decision
```

This is a hypothesis about responsibility composition. It must be evaluated against mature workflow engines, Agent runtimes, protocol objects, and simpler product policies before being claimed as a new computing layer.

## 7. Research consequence

The next phase should not add more architecture by default. It should force each candidate Ordivon responsibility to compete with its strongest existing baseline under identical workloads, fault injection, budgets, and acceptance criteria.

See [`09-adversarial-research-program.md`](09-adversarial-research-program.md).
