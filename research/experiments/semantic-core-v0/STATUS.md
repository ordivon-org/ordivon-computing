# Status

## Completed

- M0 semantic reference kernel implemented.
- 17 unit and conformance tests pass on Python 3.12.13 and 3.14.6.
- Dispatch is represented independently from Effect.
- VerificationPlan and evidence ownership are enforced.
- Scripted Ordivon adapter covers success, rejection, response loss, reconciliation, Artifact projection, uncertainty, and normal running observation.
- Live Ordivon asynchronous execution passed through the public `/mcp` endpoint.
- Live evidence was admitted through `Claim → Verification → Fact`.

## Live result

```text
Effect initial state: running
Effect terminal state: succeeded
Correlated Ordivon Jobs: 1
Semantic Artifacts: 3
Duplicate Dispatch: blocked
stdout markers: independently read and verified
Fact admission: committed
Temporary Workspace: closed
```

## Current claim boundary

The experiment now proves reference semantics plus one real asynchronous Ordivon execution path. It does not yet prove general backend conformance, persistent semantic durability, injected transport-loss recovery, Tool ABI stability, or production readiness.

## Next executable work

Continue M1 with:

1. versioned Workspace read;
2. atomic Workspace mutation and independent verification;
3. deliberate response loss after durable admission;
4. cancellation racing with natural completion;
5. adapter restart followed by Job correlation and observation.
