# Ordivon Adapter Design

## Boundary

The adapter translates between universal Agent semantics and Ordivon's concrete Linux execution substrate. The semantic core does not know systemd units, Git worktree paths, SQLite rows, process IDs, bearer tokens, or MCP request envelopes.

```text
SemanticKernel
    ↑
OrdivonSemanticAdapter
    ↑ ToolCaller
StreamableHttpMcpClient
    ↓
Ordivon public MCP contract
```

## World-object binding

A semantic Effect must identify the actual object it will affect. For the first slice:

```text
WorldObjectId = ordivon-workspace:<workspace-id>
```

Before starting a Dispatch, the adapter verifies that this identity matches `OrdivonExecution.workspace_id`. A mismatched target is rejected before any Tool call.

## Identity binding

| Semantic identity | Ordivon binding |
|---|---|
| EffectId | stable intent identity owned above the adapter |
| DispatchId | one concrete crossing attempt, recorded before transport |
| WorldObjectId | canonical Ordivon Workspace identity |
| clientRequestId | deterministic hash derived from EffectId for backend idempotency |
| JobId | Ordivon's durable admitted operation identity |
| AttemptId | Ordivon's concrete execution attempt identity |
| ObservationId | immutable digest-bound reading of one Tool result |
| ArtifactId | Ordivon Artifact identity namespaced by backend and Job |
| EventId | semantic state-transition event, not an MCP request ID |

`clientRequestId` is a backend correlation and idempotency key; it is not the universal Effect identity.

## Two dispatch boundaries

The implementation distinguishes:

1. **Semantic dispatch start** — the kernel records DispatchId and request digest before transport begins. In v0 this is in-memory; M2 must make it durable.
2. **Backend durable admission** — Ordivon commits Job, Attempt, execution plan, idempotency key, and capacity reservation.

A lost response between these boundaries is uncertain. The adapter must query Ordivon using the stable request identity rather than create a second Dispatch.

## Dispatch state algebra

```text
started
  ├→ admitted   backend Job identity is proven
  ├→ unknown    delivery or backend outcome is unresolved
  └→ rejected   backend admission is proven not to have occurred
```

A retryable rejected Dispatch is historical and immutable; it releases the Effect back to `prepared`. A new execution uses a new DispatchId. An unknown Dispatch never authorizes redispatch.

## Public runtime-state mapping

```text
Ordivon queued    → Semantic dispatched
Ordivon working   → Semantic running
Ordivon succeeded → Semantic succeeded
Ordivon failed    → Semantic failed
Ordivon timed_out → Semantic failed
Ordivon cancelled → Semantic cancelled
Ordivon lost      → Semantic unknown
Ordivon orphaned  → Semantic unknown
Ordivon unknown   → Semantic unknown
```

The mapping is asymmetric by design. Missing backend knowledge is represented as uncertainty, not invented failure.

## Error classification

```text
Tool transport/protocol uncertainty
→ unknown
→ reconcile by clientRequestId

Structured Tool rejection
→ search task.list for a correlated Job
    ├─ Job exists: admit and observe/reconcile that execution
    ├─ no Job + retryable: Dispatch rejected; Effect prepared
    └─ no Job + non-retryable: Dispatch rejected; Effect failed
```

This prevents unsafe blind retry while preserving the ability to create a new Dispatch after a proven retryable pre-admission rejection.

## Evidence translation for `workspace.exec`

```text
EffectSpec
→ DispatchRecord(request digest)
→ workspace.exec
→ Job / Attempt binding
→ TaskObservation payload digest
→ Observation
→ Ordivon Artifact descriptors
→ semantic outcome
```

A zero process exit is execution evidence, not sufficient proof that a higher-level Goal was achieved. Claim, Verification, and Fact remain separate layers.

## Synchronous file I/O

Versioned `workspace.read` and compare-and-swap `workspace.mutate` are implemented by a separate thin adapter. Synchronous structured responses become receipt identities rather than invented Jobs. Independent reread evidence may verify a mutation Claim and admit a Fact. See [`IO-ADAPTER.md`](IO-ADAPTER.md).

## Security boundary

The concrete MCP client reads the bearer token from its caller and sends it only in the Authorization header. The dogfood script requires `ORDIVON_BEARER_TOKEN` but never emits it. The semantic journal stores request and evidence digests, not credentials.

## Verified live cases

- successful cross-Workspace command execution with Job, Attempt, Observation, and three Artifacts;
- same-Workspace nested execution produced Dispatch=`rejected`, Effect=`prepared`, and `CONCURRENCY_LIMIT`;
- simulated response loss reconciled through `task.list` and `task.observe` without a second `workspace.exec` call;
- `orphaned` projected to semantic `unknown`.

## Remaining adapter tests

1. real response loss after durable backend admission;
2. duplicate delivery after terminal completion;
3. cancellation racing with natural completion;
4. Artifact digest mutation or identity mismatch;
5. stale Workspace revision precondition;
6. versioned read and atomic mutation;
7. Tool-schema change while an Effect is pending;
8. Tool-schema change while a Job is already running;
9. invariant scan after semantic-journal restart.
