# Live Ordivon Conformance Report

## Scope

This report records live Semantic Core v0 execution through the local Ordivon public MCP endpoint on July 26, 2026.

It proves the four required operation classes against one backend: versioned read, atomic mutation, asynchronous execution/observation, and independent reread-to-Fact admission. It does not prove the remaining failure and durability cases.

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
  "attemptId": "attempt-019f9a51-02d3-73c1-a67a-347c97947848",
  "correlatedJobCount": 1,
  "duplicateDispatchBlocked": true,
  "factCommitted": true,
  "initialState": "running",
  "jobId": "job-019f9a51-02d3-73c1-a67a-346946652160",
  "semanticArtifactCount": 3,
  "sourceRevision": "1b87a76f2cbc14c788b49428cbdac7811128cf24",
  "stdoutDigest": "sha256:f1c4ddb78f847a90b287e55013dbac94ad5d4475b380a188f0edb0e991d8a5b7",
  "stdoutMarkersVerified": true,
  "terminalState": "succeeded",
  "workspaceId": "anc-live-semantic-1785000428071"
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
  "sourceRevision": "1b87a76f2cbc14c788b49428cbdac7811128cf24",
  "staleMutationErrorCode": "INVALID_REQUEST",
  "staleMutationState": "failed",
  "toolCallCounts": {
    "workspace.mutate": 3,
    "workspace.open": 1,
    "workspace.read": 3
  },
  "workspaceId": "anc-live-files-1785000429867"
}
```

# C. Integrated existing-Workspace dogfood

After merging the concurrent Semantic Core implementation, the retained targeted dogfood script ran against an already-open exact-revision Workspace through the consolidated test-only MCP caller.

```json
{
  "artifactCount": 3,
  "attemptId": "attempt-019f9a51-7ec1-7d03-b538-77f1abab4ba7",
  "errorCode": null,
  "jobId": "job-019f9a51-7ec1-7d03-b538-77ecb7701f87",
  "observationDigest": "sha256:e5d695e50cee2296fd7f8be57d5bd1d3de49dfa8be8812e62461ccaba843aea1",
  "state": "succeeded",
  "stdoutTail": "merged-semantic-core-live\n"
}
```

This run confirms that the integrated Dispatch admission model, adapter, public object identity, and consolidated transport harness remain compatible with the parallel branch's original dogfood surface. The temporary Workspace was closed after the run.

# Findings

## Supported

- one semantic Effect can own a real Ordivon Job without making Job identity universal;
- Dispatch STARTED, ADMITTED, UNKNOWN, and REJECTED remain distinct across reference and live adapter paths;
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
3. **Mechanically choosing one concurrent implementation:** the parallel `main` implementation carried stronger pre-admission rejection semantics, while this branch carried stronger independent verification and file Effects. Neither was sufficient alone; semantic integration was required.

## Not supported

- complete Ordivon conformance;
- live recovery after deliberately lost responses;
- cancellation-race semantics;
- semantic state across process restart;
- Tool-contract rebinding;
- production readiness or Goal-level correctness.

# C. Final integrated I/O regression

After integrating the dedicated `ordivon_io.py` subsystem from the latest `main`, the live path was rerun through the unified public API:

```text
beforeDigest: sha256:8bf8ee1400851e9b01f687cac287cf26681d3b7ca49a345ce0efd1123d1573dd
afterDigest:  sha256:ae422cadc74a5b2f5c4eff147494edb0b68e0f83275c0d4874da986f060e2fb4
independent Fact: committed
stale guard: failed / INVALID_REQUEST
Workspace cleanup: completed
```

The integrated suite contains 31 tests on both Python 3.12.13 and 3.14.6.
