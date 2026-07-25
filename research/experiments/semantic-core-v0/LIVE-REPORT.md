# Live Ordivon Conformance Report

## Scope

This report records live Semantic Core v0 execution through the local Ordivon public MCP endpoint on July 26, 2026.

It proves the four required operation classes against one backend: versioned read, atomic mutation, asynchronous execution/observation, and evidence-to-Fact admission. It does not prove the remaining failure and durability cases.

## Environment boundary

```text
MCP endpoint: local loopback /mcp
Authentication: Bearer token loaded inside WSL and never printed
Source repository: agent-native-computing
Source revision: 5d6c7125e854ff41679bac937a71192a32423315
Temporary Workspaces: isolated and closed after every run
```

# A. Asynchronous execution

## Executed path

```text
workspace.open
→ admit and prepare Effect
→ begin Dispatch
→ workspace.exec
→ initial running Observation
→ task.observe
→ succeeded terminal Observation
→ project three Artifacts
→ task.list correlation
→ reject duplicate Dispatch
→ artifact.read stdout
→ verify two expected markers
→ Claim → accepted Verification → Fact
→ invariant scan
→ workspace.close
```

## Latest sanitized receipt

```json
{
  "attemptId": "attempt-019f9a40-0a28-74f3-824e-9b19c8f0d69c",
  "correlatedJobCount": 1,
  "duplicateDispatchBlocked": true,
  "factCommitted": true,
  "initialState": "running",
  "jobId": "job-019f9a40-0a28-74f3-824e-9b0529fefd3f",
  "semanticArtifactCount": 3,
  "sourceRevision": "5d6c7125e854ff41679bac937a71192a32423315",
  "stdoutDigest": "sha256:f1c4ddb78f847a90b287e55013dbac94ad5d4475b380a188f0edb0e991d8a5b7",
  "stdoutMarkersVerified": true,
  "terminalState": "succeeded",
  "workspaceId": "anc-live-semantic-1784999315863"
}
```

# B. Versioned read and atomic mutation

## Executed path

```text
workspace.open
→ mutation Effect: WRITE initial content
→ independent read Effect
→ same-object/same-version Verification
→ Fact 1
→ mutation Effect: REPLACE_EXACT with expected digest
→ independent read Effect
→ same-object/same-version Verification
→ Fact 2
→ stale mutation with old digest
→ failed terminal state
→ final independent read
→ content and digest unchanged
→ invariant scan
→ forced cleanup of dirty temporary Workspace
```

## Latest sanitized receipt

```json
{
  "afterDigest": "sha256:7b9a72466d3960eb2aacccfc848939453490db0678bd4725def3f789b891c919",
  "beforeDigest": "sha256:9160d4be34c8695bd172a76c7c7966587ea5a4d991ad22c87b2b91af54aa9ebb",
  "finalContentStable": true,
  "finalDigestStable": true,
  "mutationFactsCommitted": 2,
  "sourceRevision": "5d6c7125e854ff41679bac937a71192a32423315",
  "staleMutationErrorCode": "INVALID_REQUEST",
  "staleMutationState": "failed",
  "toolCallCounts": {
    "workspace.mutate": 3,
    "workspace.open": 1,
    "workspace.read": 3
  },
  "workspaceId": "anc-live-files-1784999317610"
}
```

# Findings

## Supported

- one semantic Effect can own a real Ordivon Job without making Job identity universal;
- normal observation and unknown-outcome reconciliation are distinct paths;
- exactly one Job correlates to the asynchronous Dispatch;
- terminal Artifacts retain Effect and Dispatch provenance;
- independent read Effects can verify mutation Claims when object identity and version match;
- stale digest preconditions prevent mutation and preserve final state;
- equal file content across separate reads must retain distinct Observation identities because causal provenance differs;
- Fact admission can remain stricter than backend success.

## Falsified assumptions

1. **Overly strict evidence ownership:** Verification cannot be limited to evidence from the Claim-originating Effect; independent verification requires cross-Effect evidence.
2. **Content-derived Observation identity:** identical payload digests cannot identify an observation event; Effect and Dispatch causality must participate in ObservationId.

## Not supported

- complete Ordivon conformance;
- live recovery after deliberately lost responses;
- cancellation-race semantics;
- semantic state across process restart;
- Tool-contract rebinding;
- production readiness or Goal-level correctness.
