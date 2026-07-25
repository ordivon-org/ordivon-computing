# Status

## Completed

- M0 semantic reference kernel implemented.
- 24 unit and conformance tests pass on Python 3.12.13 and 3.14.6.
- Effect, Dispatch, Observation content identity, and causal observation identity are distinct.
- VerificationPlan, subject/version scope, and evidence-time ordering are enforced.
- Independent read Effects can verify mutation Claims without permitting unrelated evidence.
- Live Ordivon asynchronous execution passed through the public `/mcp` endpoint.
- Live versioned read and atomic mutation passed with digest preconditions.
- Two mutation Claims were independently re-read and admitted as Facts.
- A stale-digest mutation failed and left final content and digest unchanged.

## Current live coverage

```text
workspace.open
workspace.read
workspace.mutate
workspace.exec
task.observe
task.list
artifact.read
workspace.close
```

## Current claim boundary

The experiment proves the semantic reference model and the four required operation classes against one real Ordivon backend. It does not yet prove failure recovery under deliberately lost responses, cancellation races, semantic state persistence across restart, Tool-contract evolution, or production readiness.

## Next executable work

1. deliberately lose the `workspace.exec` response after durable admission and reconcile by identity;
2. race cancellation against natural completion;
3. restart the adapter and recover bindings from public Job state;
4. reproduce pending and running Tool-contract drift.
