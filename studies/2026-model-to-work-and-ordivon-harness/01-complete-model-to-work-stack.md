# The Complete Model-to-Work Stack

## 1. Starting point: conditional generation

At the lowest logical level, an autoregressive language model repeatedly estimates a distribution over a next token or output unit:

```text
encoded context
→ model forward computation
→ next-token distribution
→ decoding decision
→ appended output
→ repeat until stop
```

A modern API may expose structured output, reasoning summaries, multimodal input, or Tool Calls. These are richer output protocols, not physical actions. A generated request to modify a file does not modify the file until a system outside the model interprets and executes it.

## 2. Four nested loops

A complete Agent system contains at least four nested loops with different authority.

### Token loop

Owned by the model serving system.

```text
context → token → token → token → stop
```

Question answered: what output representation comes next?

### Agent loop

Owned by a Harness.

```text
compile model input
→ invoke model
→ interpret Tool request
→ execute or delegate Tool
→ return observation
→ invoke model again
→ stop one Run
```

Question answered: how does one cognitive episode use intelligence and Tools?

### Task loop

Owned by Host.

```text
read durable Task
→ select Ready work
→ commit Assignment
→ receive Run evidence
→ verify
→ continue, replace, wait, reject, or complete
```

Question answered: what work remains true across replaceable Runs?

### Goal/world loop

Owned jointly by Host, applications, participants, and authoritative Worlds.

```text
participant purpose
→ Tasks and dependencies
→ actions and Effects
→ changed world state
→ evidence and revised judgment
→ new Ready Frontier
```

Question answered: is the real objective improving, and what should happen next?

## 3. Full logical call chain

### L0 — participant and world

Inputs originate in real preferences, constraints, repositories, services, deadlines, people, machines, budgets, and law. The world is not reconstructed from model text.

### L1 — Surface

Chat, CLI, IDE, Web, mobile, voice, or API captures input, displays progress, collects approval or clarification, and renders Artifacts. Surface is replaceable and should not own Task truth.

### L2 — interaction hosting

Authentication, conversation transport, file upload, streaming channels, client connection, and notification are hosted. A conversation Session may be useful without becoming a durable Task database.

### L3 — Goal interpretation

Natural-language intent is interpreted into a bounded Goal, constraints, preferences, risks, and success conditions. Model assistance may contribute, but admitted facts must be externalized.

### L4 — Workload Contract

The system defines:

```text
objective
inputs and source revision
allowed operations
required Artifacts
acceptance criteria
Effect boundaries
budget and deadline
dependencies
```

A Workload Contract constrains work. It does not run the Agent.

### L5 — Task graph and Ready Frontier

Complex work becomes Tasks, dependencies, branches, waits, joins, replacement points, and verification nodes. Host decides which nodes are ready and whether work remains valuable.

### L6 — Task Attempt and Assignment

Host creates one semantic Task Attempt and commits a versioned Assignment to a selected Harness. The Assignment binds exact Context, Tool catalog, source, capabilities, budget, and prior Artifacts.

Generation changes when execution authority moves to another Harness. It is a semantic fencing token, not a process lease.

### L7 — semantic Context compilation

Host selects the smallest current set of durable facts required by the Assignment:

```text
Goal and Task objective
acceptance criteria
source bindings
prior decisions and Artifacts
known failures
allowed Effects
participant constraints
```

This is selection of authoritative meaning, not Provider prompt formatting.

### L8 — Harness input compilation

The selected Harness converts semantic Context into model-specific messages, instructions, Tool schemas, output schema, and Provider options.

Host decides which facts matter. Harness decides how this model should receive them.

### L9 — Model Adapter

For Ordivon Harness, a Model Adapter serializes one inference call to OpenAI, Anthropic, Gemini, DeepSeek, OpenRouter, vLLM, or another endpoint. It returns a `ModelTurn` with content, Tool requests, usage, stop reason, extensions, and raw-response digest.

External mature Harnesses keep their own direct protocol drivers instead.

### L10 — model serving

The serving system performs authentication, scheduling, encoding, KV-cache management, model computation, decoding, streaming, and usage accounting. Some Providers also host Tools or code execution. Hosting location changes; logical responsibility remains.

### L11 — protocol interpretation

Harness interprets output as one of:

```text
message
structured final result
Tool request
need input
refusal
truncation
Provider error
```

A Tool Call is a requested action, not evidence that an action occurred.

### L12 — Agent Loop kernel

Harness decides whether to continue the Run, request a Tool, wait for input, stop for budget, interrupt, or emit a candidate result.

This is the irreducible core of Ordivon Harness.

### L13 — capability projection

Only Assignment-approved capabilities are exposed. Tool definitions consume context and influence model behavior, so the complete system catalog should not be sent by default.

### L14 — authorization and policy

A requested action is checked against semantic authority, argument schema, budget, target scope, reversibility, consequence, and approval requirements. Authority may be divided among Host, Harness, Runtime, Surface, and an application World.

### L15 — Tool Bridge

Harness translates the model request into a concrete Tool or Runtime operation and preserves Tool Call identity.

```text
Model Tool request
→ Ordivon Harness Tool Bridge
→ Runtime request / external provider call
```

### L16 — Runtime

Runtime creates or reuses the exact Workspace and Job, owns process supervision, captures stdout/stderr, enforces timeout, retains Artifacts, and records terminal evidence. It does not decide that a Task is complete.

### L17 — external world and Effects

Files, services, repositories, databases, networks, messages, deployments, and other real state change. Delivery may be ambiguous; an action may be irreversible or externally uncertain.

### L18 — observation and Artifact capture

Raw execution facts become bounded observations and content-addressed Artifacts. The original evidence remains available even when Harness sends a smaller summary back to the model.

### L19 — Run-local Context update

Harness appends or transforms the Tool result, updates token/turn/time budget, and performs another model call.

This closes the Agent Loop:

```text
model → Tool request → Runtime/world → observation → model
```

### L20 — context-window management

Harness may select recent messages, elide repeated output, externalize Artifacts, reuse Provider cache, or compact state. Compaction is a strategy, not durable Task truth.

### L21 — Harness Run stop

A Run can stop as:

```text
candidate_completed
needs_input
budget_exhausted
context_exhausted
interrupted
provider_failed
tool_failed
invalid_output
```

None of these automatically commits `TaskOutcome`.

### L22 — Harness Run evidence

Harness emits a `HarnessRunReceipt` binding Assignment, Harness identity, model/Provider, Session evidence, Context, Tool catalog, Runtime Jobs, Artifacts, usage, stop reason, and event digest.

### L23 — CompletionProposal

When appropriate, Harness proposes completion and references acceptance results and Artifacts. A proposal is evidence-bearing but untrusted until Host adjudication.

### L24 — verification

Deterministic tests, static checks, a simulator, an independent model, or a human reviewer assesses acceptance. Verification should inspect authoritative source/world state rather than merely score final prose.

### L25 — CompletionDecision and TaskOutcome

Host verifies current Task Attempt and Assignment generation, required Artifacts, unresolved Effects/UNKNOWN state, and acceptance evidence. Only an accepted decision creates `TaskOutcome`.

### L26 — graph advancement

Outcome closes or revises nodes, releases dependencies, changes the Ready Frontier, creates follow-up work, or ends a Goal.

### L27 — durable provenance and memory

Persist only facts whose loss would make continuation, attribution, reconciliation, or verification unsafe. Full token streams and hidden reasoning are not default durable state.

### L28 — participant feedback

Surface presents results, evidence, limits, and next decisions. Participant response becomes new Goal or Task input.

## 4. Ownership invariant

```text
Model owns generated representation for one call.
Harness owns one cognitive and Tool-use episode.
Host owns durable work meaning and semantic transitions.
Runtime owns physical execution facts.
World/application owns authoritative domain state.
Participant owns purpose and consequential judgment.
```

Products may colocate these responsibilities. Correctness depends on logical ownership, not process count.

## 5. Graph representation

Useful identities include:

```text
G  Goal
T  Task
A  Task Attempt
S  Assignment
H  Harness Run
M  Model Call
C  Tool Call
J  Runtime Job
E  Evidence / Artifact / Effect
P  CompletionProposal
D  CompletionDecision
O  TaskOutcome
```

Typical relations are:

```text
G → T
T → A
A → S
S → H
H → M
M → C
C → J
J → E
E → M
H → P
P → D
D → O
O → downstream T
```

The runtime behavior contains cycles, but the append-only provenance history is a directed evidence graph.
