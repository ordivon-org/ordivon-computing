# Live Ordivon Conformance Report

## Scope

This report records the first real execution of Semantic Core v0 through the local Ordivon public MCP endpoint on July 26, 2026.

It proves one asynchronous execution path. It does not prove the complete M1 adapter surface.

## Environment boundary

```text
MCP endpoint: local loopback /mcp
Authentication: Bearer token loaded inside WSL and never printed
Source repository: agent-native-computing
Source revision: 5d6c7125e854ff41679bac937a71192a32423315
Temporary Workspace: isolated and closed after the run
```

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

## Sanitized receipt

```json
{
  "attemptId": "attempt-019f9a2f-0378-7a61-8cd5-b49e06284c2c",
  "correlatedJobCount": 1,
  "duplicateDispatchBlocked": true,
  "factCommitted": true,
  "initialState": "running",
  "jobId": "job-019f9a2f-0378-7a61-8cd5-b48a6d70d6b5",
  "semanticArtifactCount": 3,
  "sourceRevision": "5d6c7125e854ff41679bac937a71192a32423315",
  "stdoutDigest": "sha256:f1c4ddb78f847a90b287e55013dbac94ad5d4475b380a188f0edb0e991d8a5b7",
  "stdoutMarkersVerified": true,
  "terminalState": "succeeded",
  "workspaceId": "anc-live-semantic-1784998200000"
}
```

## What this supports

- the same semantic Effect can own a real Ordivon Job and Attempt without adopting those backend identities as universal semantics;
- `running` and `succeeded` can be projected through public Tool results;
- terminal Artifacts retain Effect and Dispatch provenance;
- exactly one Job was correlated through the stable request identity;
- a terminal Effect was not redispatched;
- stdout content was independently read before Fact admission;
- the temporary Workspace was closed by the reproducible harness.

## What this does not support

- that every Ordivon operation conforms to the semantic core;
- that response-loss recovery works live;
- that semantic state survives adapter or process restart;
- that zero exit code alone proves higher-level Goal completion;
- that the current state algebra is final;
- that this experiment is production-ready.
