# Semantic Core v0

An executable reference kernel for the first Agent-native semantic layer:

```text
Reality and Evidence
→ Identity and Causality
→ Outcome Algebra
→ Effect Semantics
→ Backend Binding
```

The semantic core is independent of Ordivon, Linux process state, MCP, model providers, and conversation history. The experiment also includes a thin Ordivon adapter and a separate standard-library Streamable HTTP MCP client so the same semantics can be exercised against a real execution backend without importing MCP into the core.

## Layering

```text
ReferenceKernel
    ↑ SemanticKernel protocol
OrdivonSemanticAdapter
    ↑ provider-neutral ToolCaller protocol
StreamableHttpMcpClient
    ↓
Ordivon MCP → Ordivon Runtime → Linux
```

## Execution form

This v0 is intentionally source-run rather than packaged. It has no runtime dependency and does not require a Python build backend. Packaging is deferred until a second consumer needs an installable artifact.

## Run unit and conformance tests

From this directory:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
```

Current result: **14 tests pass**.

## Run live Ordivon dogfood

Load the local Ordivon environment without printing its bearer token, then run:

```bash
set -a
. /etc/ordivon/ordivon-mcp.env
set +a

PYTHONPATH=src python3 scripts/live_ordivon_dogfood.py \
  --target-workspace <workspace-id> \
  --effect-name <unique-name> \
  --message semantic-core-live \
  --expect-state succeeded
```

The script emits a bounded JSON summary containing semantic state, Job and Attempt identities, Artifact count, stdout tail, and Observation digest. It never prints the bearer token.

## Implemented semantics

- typed semantic identities;
- idempotent Effect admission with identity-conflict detection;
- optimistic revisions and ordered Effect events;
- independent Effect and Dispatch records with separate state machines;
- explicit `unknown → reconciling` without blind redispatch;
- immutable terminal outcomes;
- Observation and Artifact provenance bound to one Dispatch;
- Claim → Verification → Fact admission;
- WorldObject-to-Workspace binding before dispatch;
- retryable Dispatch rejection preserves a prepared Effect;
- non-retryable Dispatch rejection fails the Effect;
- uncertain delivery remains non-redispatchable;
- Ordivon Job correlation through stable `clientRequestId`;
- an invariant scanner and reusable conformance scenarios.

## Current backend slice

The first real operation is asynchronous `workspace.exec`:

```text
EffectSpec
→ validate WorldObject / Workspace binding
→ begin Dispatch before transport
→ workspace.exec
→ Job / Attempt correlation
→ TaskObservation
→ semantic Observation and Artifacts
→ succeeded / failed / cancelled / unknown
```

A live successful run and a live pre-admission concurrency rejection are recorded in [`TEST-REPORT.md`](TEST-REPORT.md).

## Next slice

1. versioned `workspace.read`;
2. atomic `workspace.mutate` with digest/revision preconditions;
3. live Claim → Verification → Fact from independently re-observed output;
4. durable semantic journal;
5. canonical Effect IR only after the two implementations continue to agree.
