# Mature Baselines and Standards

This document identifies what Ordivon should reuse, what it should adapt, and where a distinct research responsibility may remain.

## 1. Codex

OpenAI describes the Codex Harness as the Agent loop and supporting logic shared across Codex surfaces. Codex Core contains the loop, Thread lifecycle and persistence, configuration and authentication, Tool execution, sandbox integration, MCP, and Skills. Codex App Server is a long-lived bidirectional process and protocol that hosts Core Threads for TUI, IDE, desktop, web, and remote clients.

```text
Codex product
├── Surface: TUI / IDE / app / web
├── App Server: interaction Host and stable event protocol
├── Codex Core: Harness + Agent Session runtime
└── sandbox / shell / file / cloud compute: execution layer
```

### Ordivon lesson

- product packaging may combine roles without erasing logical ownership;
- a stable client protocol should expose lifecycle and events, not internal implementation objects;
- Thread is not the same as durable Goal or Task;
- Codex-specific richness should be preserved behind an adapter;
- Ordivon should not reimplement the complete Codex Harness merely to gain a common interface.

## 2. Claude Code and Claude Agent SDK

Claude Code exposes an integrated local Agent product with Sessions, Tools, Skills, MCP, subagents, teams, hooks, permissions, and execution. Claude Code Hooks run at defined lifecycle events and can call commands, HTTP endpoints, MCP Tools, prompts, or subagents. Skills provide reusable knowledge and workflows; plugins package extensions.

### Ordivon lesson

- Hook events need explicit input/output, scope, timeout, matcher, ordering, and blocking semantics;
- Skills, Hooks, subagents, MCP, and plugins are separate extension forms;
- a local CLI process can simultaneously act as Surface, interaction Host, Harness, and execution adapter;
- Host-managed durable workers must remain distinct from Harness-local subagents or teams;
- provider-specific session and hook features should remain visible through capability manifests.

## 3. OpenAI Agents SDK

The Agents SDK provides a model/tool loop, Agent and Run hooks, handoffs, guardrails, Sessions, and tracing. It is a strong baseline for an embedded Harness library.

### Ordivon lesson

- Harness lifecycle callbacks are not Host Task events;
- Handoff is commonly represented inside the model-visible Agent loop;
- tracing should bind model calls, Tool calls, handoffs, guardrails, and custom events;
- Ordivon should reuse an SDK where the workload fits rather than create another general Agent framework.

## 4. Temporal and durable workflows

Temporal provides durable Workflow execution, Activities, retries, timers, Task Queues, Signals, Queries, Updates, and replay-based recovery.

### Ordivon lesson

Temporal is the baseline for:

- long waits and timers;
- crash recovery;
- durable declared control flow;
- asynchronous Signals;
- read-only Queries;
- accepted/rejected Updates;
- Activity retry and timeout;
- worker and queue separation.

Ordivon must not claim these mechanisms as Agent-native. The distinct problem is open work whose decomposition and next action can be revised by probabilistic cognition and new evidence rather than fully encoded in a deterministic Workflow definition.

A future Host implementation may use Temporal or another mature workflow engine if the deployment cost is justified. Host semantics should not depend on one engine.

## 5. Kubernetes controllers and Leases

Kubernetes demonstrates reconciliation loops, desired versus observed state, controller ownership, Work Queues, resource versions, status projections, Lease objects, node heartbeats, and leader election.

### Ordivon lesson

- Host scheduling should resemble a controller over durable Task state rather than a conversational script;
- Assignment ownership requires lease and stale-writer protection;
- readiness and current status are projections, not mutable narration;
- domain controllers should own narrow resources rather than one global controller owning every object;
- Kubernetes does not supply Agent cognition, Context compilation, or semantic Goal completion.

## 6. Model Context Protocol

MCP defines a client-server lifecycle with initialization, version negotiation, capability negotiation, operation, and shutdown. It standardizes Tool/resource/prompt integration but does not define durable Goal, Task, Assignment, completion, or world-effect semantics.

### Ordivon lesson

- capability negotiation should happen before ordinary operation;
- Tool discovery and Tool execution are different from Harness hosting;
- MCP Tool schemas are part of the executable boundary but require normalized contract identity and drift classification for long-lived work;
- Ordivon Protocol should compose with MCP rather than replace it;
- a Harness protocol may need richer bidirectional Session events than MCP Tools alone provide.

## 7. OpenTelemetry

OpenTelemetry defines common semantics for traces, spans, metrics, logs, resources, and events. Generative-AI semantic conventions are evolving and should be reused where applicable.

### Ordivon lesson

- do not invent a proprietary trace format for every layer;
- bind Goal, Task, Assignment, Run, Tool Call, Dispatch, Job, and Artifact IDs as attributes or links;
- keep business Events distinct from diagnostic Logs;
- preserve sensitive-data controls for prompts, Tool arguments, and outputs;
- add Ordivon-specific semantic attributes only where no standard term exists and a real query requires them.

## 8. LangGraph

LangGraph provides graph execution, state reducers, checkpoints, Threads, interrupts, resume, time travel, replay, and fault-tolerant super-step execution.

### Ordivon lesson

- checkpoints and interrupts are powerful but tied to graph-node and Thread semantics;
- replay may re-execute model and external calls, so exact replay must be distinguished from semantic replay;
- side effects before an interrupt must be idempotent or reconciled;
- reducers should combine typed updates rather than overwrite shared state;
- Task Graph and Harness Planning Graph should not automatically become one LangGraph graph.

## 9. Databases and event-driven systems

Relational databases, append-only logs, transactional outbox patterns, event buses, materialized views, and change-data capture remain the baseline for durable state and projection.

### Ordivon lesson

- Host should use ordinary transactions for atomic state changes;
- an Event is not automatically an event-sourcing mandate;
- materialized projections are appropriate for Ready Frontier, Task summaries, Agent health, and portfolio reports;
- full event sourcing is deferred until replay and audit benefits exceed complexity;
- domain facts and model claims require explicit epistemic status, not just database durability.

## 10. Baseline comparison matrix

| Need | Strong baseline | Ordivon-specific remaining question |
|---|---|---|
| Model/tool loop | Codex, Claude Agent SDK, OpenAI Agents SDK | Can one thin adapter boundary preserve Task identity and provider-specific capability? |
| Session hosting | Codex App Server, Claude CLI hosting | Which Session state must survive and which belongs only to a Harness? |
| Durable workflow | Temporal | How does open probabilistic replanning alter durable Task semantics? |
| Reconciliation | Kubernetes controllers | How are semantic Effects, evidence, and Task completion reconciled? |
| Tool integration | MCP | How are Tool revisions bound to long-lived work and world effects? |
| Graph checkpoints | LangGraph | Which state is Harness-local versus durable Host work? |
| Observability | OpenTelemetry | Which cross-layer IDs and evidence links are required? |
| Physical execution | OS, containers, CI, cloud sandboxes | What stable Execution Runtime contract reduces Host/Harness coupling? |
| Authorization | IAM, capability systems, provider policy | How are purpose, consequence, and participant commitments represented without duplicating IAM? |
| Evaluation | established benchmark/eval frameworks | How are real Task outcomes, recovery, and evidence compared across Harnesses? |

## 11. Reuse policy

For every mechanism:

```text
reuse mature implementation by default
wrap it with a narrow adapter where semantics differ
measure before introducing a shared Ordivon object
promote only after a second workload
retain provider-specific capability instead of flattening it
```

## 12. Deliberate non-standards

The following should not become Ordivon standards without much stronger evidence:

- one universal Agent protocol covering every provider feature;
- one universal graph representation for cognition, work, execution, and provenance;
- one universal memory database;
- one global Hook engine;
- one scalar risk or autonomy score;
- one general-purpose multi-Agent organization schema;
- one plugin marketplace;
- one replacement for MCP, OpenTelemetry, Temporal, Kubernetes, or provider Harnesses.
