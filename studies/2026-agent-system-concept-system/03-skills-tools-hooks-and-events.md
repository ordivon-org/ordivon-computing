# Skills, Tools, Hooks, and Events

These concepts are frequently grouped as “Agent extensions,” but they have different semantics and failure modes.

## 1. Tool and Skill

```text
Tool  = executable capability
Skill = reusable procedure and knowledge
```

A Tool answers **what can be invoked**. A Skill answers **how a class of work should be approached**.

Examples:

```text
Tool: cloudflare.deploy
Skill: deploy and verify a Cloudflare Worker with rollback evidence

Tool: workspace.exec
Skill: diagnose a failing repository test suite and preserve the failure proof
```

### Tool contract

A useful Tool contract contains more than JSON Schema:

- stable identity and revision;
- input and output schema;
- synchronous or asynchronous execution semantics;
- error taxonomy;
- correlation and idempotency support;
- cancellation and observation support;
- side-effect and consequence classification;
- required credentials or capability;
- Artifact and receipt semantics;
- compatibility and deprecation metadata.

### Skill package

A Skill may contain:

- discovery metadata;
- instructions and method;
- examples and counterexamples;
- required Tools and capabilities;
- templates or reference resources;
- optional scripts;
- evaluation cases;
- version and provenance.

The Harness selects and loads Skills. Host may index Skill metadata for Assignment routing. Runtime may execute a Skill script but does not interpret the Skill’s method.

```text
Harness understands Skill
Host indexes capability metadata
Runtime executes requested script or Tool
```

## 2. Workflow versus Skill

A Skill is adaptive procedural knowledge. A Workflow is a durable or reusable control structure.

```text
Skill:
  investigate why a deployment failed
  choose evidence and Tools according to the situation

Workflow:
  build → test → preview deploy → acceptance → publish
```

A Skill may propose or operate within a Workflow. Once steps require persistent dependencies, waiting, parallelism, retry, or external triggers, Host or a mature workflow backend should own the control state.

## 3. Hook

A Hook is a lifecycle extension point. It runs because a defined point was reached, not because the Model remembered to invoke it.

Useful Harness Hooks include:

```text
OnRunStart
BeforeContextCompile
AfterContextCompile
BeforeModelCall
AfterModelCall
BeforeToolExpose
BeforeToolCall
AfterToolCall
BeforeCompaction
AfterCompaction
BeforeHandoff
AfterHandoff
OnRunEnd
```

Useful Host Hooks include:

```text
BeforeGoalCommit
BeforeTaskCommit
BeforeTaskTransition
BeforeAssignment
BeforeCompletionCommit
AfterLeaseExpired
```

Useful Runtime Hooks include:

```text
BeforeWorkspaceOpen
BeforeMutation
BeforeExec
AfterProcessStart
OnOutputChunk
AfterProcessExit
BeforeArtifactCommit
```

### Hook modes

| Mode | Purpose | May block? | May mutate? |
|---|---|---:|---:|
| Observer | trace, metric, audit, notification | no | no authoritative state |
| Mutator | transform Context, Tool input, or visible result | sometimes | bounded payload only |
| Gate | allow, deny, rewrite, or require approval | yes | decision output only |

A mutator or gate must be explicit. A generic callback with arbitrary access creates hidden control flow and cannot be reliably replayed.

## 4. Event

An Event is an immutable record that something already happened.

```text
BeforeToolCall  → Hook or Policy may stop the call
ToolCallStarted → Event; the start already happened
ToolCallEnded   → Event; the effect must be reconciled, not blocked retroactively
```

Recommended envelope:

```text
Event {
  event_id
  event_type
  schema_version
  occurred_at
  producer
  subject_type
  subject_id
  causation_id
  correlation_id
  trace_id
  payload
}
```

The identifiers serve different purposes:

- `event_id` identifies this record;
- `subject_id` identifies the object described;
- `causation_id` identifies the immediate cause;
- `correlation_id` groups the complete Goal/Task/Effect path;
- `trace_id` groups the observable execution chain.

## 5. Command, Query, Update, Signal, Trigger, and Interrupt

These must not collapse into a generic message bus.

| Message | Meaning | Response |
|---|---|---|
| Command | request an operation | accepted, rejected, or result |
| Query | read state without mutation | current projection |
| Update | request a durable state change and await decision | accepted/rejected state result |
| Signal | asynchronous information to a running object | delivery acknowledgment, not business result |
| Trigger | condition or schedule creates work | new Task/Run identity |
| Interrupt | durably suspend at a defined boundary | checkpoint plus waiting reason |
| Resume | continue from current authoritative state | new or continued Run |

Examples:

```text
CancelAssignment     Command
GetTask              Query
AddEvidence          Update
DependencyCompleted  Signal
ScheduleElapsed      Trigger
NeedApproval          Interrupt / DecisionRequest
```

## 6. Hook, Middleware, Interceptor, Policy, and Guardrail

### Middleware

Middleware wraps an invocation:

```text
before
→ model / Tool / Runtime call
→ after
```

It is suitable for authentication, tracing, caching, retry, timeout, error translation, and rate limiting.

### Interceptor

An Interceptor emphasizes inspection or replacement of a call. It may rewrite arguments, substitute a provider, or block execution.

### Policy

Policy evaluates an actor, action, resource, context, authority, and consequence:

```text
allow
deny
require_approval
limit
rewrite
```

Policy should decide. It should not silently perform unrelated side effects.

### Guardrail

A Guardrail performs bounded validation of input, output, or Tool use. It is narrower than a general Policy engine.

### Approval

Approval is a stateful decision by the authority responsible for a missing commitment or consequence. It is not merely a Hook exit code.

## 7. Layered Hook rule

Ordivon should not build a global `on_everything` system.

Each layer exposes only lifecycle points that correspond to state it owns:

```text
Harness Hooks cannot commit Host Task state.
Host Hooks cannot rewrite provider hidden Session state.
Runtime Hooks cannot decide Goal completion.
After-events cannot erase physical side effects.
```

Shared infrastructure may provide common envelopes, ordering, timeout, trace, and error handling without merging ownership.

## 8. Ordering and failure semantics

Every Hook family must specify:

- deterministic or explicitly unordered execution;
- parallel or sequential handlers;
- timeout;
- failure policy: fail-open, fail-closed, record-only, or retry;
- deduplication and idempotency;
- reentrancy and recursion rules;
- whether output is visible to Model, operator, or only telemetry;
- version and provenance;
- maximum payload and Context injection.

Gate Hooks should be few. Observer Hooks should never stall the critical path by default.

## 9. Connector, Adapter, Broker, Registry, and Plugin

```text
Adapter   translates one interface into another
Connector binds an external system, identity, and Tools
Broker    routes calls among providers
Registry  indexes available capabilities
Plugin    packages and distributes extensions
```

A Plugin can contain Skills, Tools, Connectors, Hooks, UI resources, and configuration. It is not a runtime layer or authority model.

Registries and Brokers are deferred until a real number of providers makes static configuration inadequate. Capability negotiation should precede automatic routing.

## 10. Capability negotiation

A connected component should declare what it supports rather than relying on product names:

```text
HarnessCapabilities {
  resume
  fork
  compaction
  retained_reasoning
  subagents
  native_tools
  structured_output
}

ToolCapabilities {
  execution_kind
  observation
  cancellation
  idempotency
  compensation
  dry_run
  approval_requirement
}

RuntimeCapabilities {
  workspaces
  long_jobs
  artifact_store
  remote_nodes
  network
  resource_limits
}
```

Negotiation is not provider selection. It establishes the current compatible surface and its revision.

## 11. Extension admission rules

Prefer:

- Tool for one executable operation;
- Skill for adaptive reusable method;
- Workflow for persistent declared control;
- Hook for deterministic lifecycle intervention;
- Event for immutable fact;
- Policy for allow/deny/limit decisions;
- Plugin only as packaging when multiple components need distribution together.

Reject or defer:

- a Tool that hides an entire autonomous Agent without declaring Session semantics;
- a Skill that becomes a second authoritative Task database;
- a Hook that performs untracked external commitments;
- an Event listener that changes the event it is consuming;
- a global Plugin API before two independent plugins exist;
- automatic Skill self-modification without Eval, versioning, and rollback evidence.
