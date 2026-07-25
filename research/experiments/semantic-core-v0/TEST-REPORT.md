# Test Report

Date: 2026-07-26

## Unit and conformance verification

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests scripts
git diff --check
```

Result:

```text
14 tests passed
Python bytecode compilation passed
Git whitespace validation passed
```

Covered semantics:

- idempotent Effect admission and conflicting identity rejection;
- independent EffectState and DispatchState machines;
- Dispatch `started → admitted / unknown / rejected`;
- retryable rejection preserves Effect=`prepared` and permits a new unique Dispatch;
- non-retryable rejection produces Effect=`failed`;
- a Dispatch proven admitted can never be reclassified as rejected;
- unknown outcome cannot be blindly redispatched;
- unknown outcome can reconcile through stable request identity;
- terminal state immutability and optimistic revision conflicts;
- Observation and Artifact provenance requires proven backend admission;
- Effect WorldObject must match the actual Ordivon Workspace;
- `Lost` and `Orphaned` remain semantic `unknown`;
- Claim → Verification → Fact admission invariants.

## Live Ordivon success

The reproducible dogfood script executed a semantic Effect through the local Streamable HTTP MCP endpoint into a different Ordivon Workspace.

```text
Semantic state: succeeded
Ordivon Job: job-019f9a37-d1db-78d3-ba63-5a8eb7b47c18
Ordivon Attempt: attempt-019f9a37-d1db-78d3-ba63-5a95d149cdfa
Artifacts: 3
Observation digest: sha256:2ddc64cffe3ec5de7dc8ee18622654bf838de08ddac2feed4560bff4593542de
stdout: semantic-core-dual-state-live-success-v2
```

Verified path:

```text
Effect prepared
→ Dispatch started
→ Ordivon Job durably admitted
→ Dispatch admitted
→ TaskObservation
→ Observation + Artifacts
→ Effect succeeded
```

## Live retryable admission rejection

A nested execution intentionally targeted the Workspace already holding the outer Job. Ordivon's per-Workspace execution limit is one.

```text
Effect state: prepared
Dispatch state: rejected
Error code: CONCURRENCY_LIMIT
Message: workspace execution concurrency limit reached (active=1, limit=1)
Correlated Job: none
```

The adapter received the structured Tool rejection, searched `task.list` by the stable `clientRequestId`, proved that no Job had been admitted, marked the concrete Dispatch rejected, and returned the durable Effect to prepared. A later execution may create a new Dispatch identity; the rejected attempt remains historical evidence.

## Semantic correction discovered by dogfood

The first implementation treated every Tool error as Effect=`unknown`; the second treated every proven rejection as Effect=`failed`. Both were too coarse. The corrected algebra is:

```text
transport/protocol uncertainty
→ Dispatch unknown + Effect unknown
→ reconcile; never blind redispatch

structured rejection + correlated Job
→ Dispatch admitted
→ observe/reconcile the existing Job

structured rejection + no Job + retryable
→ Dispatch rejected
→ Effect prepared
→ a new Dispatch may be attempted later

structured rejection + no Job + non-retryable
→ Dispatch rejected
→ Effect failed
```

## Live contract drift observed

During the experiment the MCP server identity changed from `ordivon-mcp` to `ordivon-runtime-mcp`, and the systemd unit changed to `ordivon-runtime.service`. The public Tool capability remained available. The dogfood client now recognizes the Ordivon server family instead of freezing one historical service name. This is evidence for semantic identity and contract classification above concrete deployment names.

## Not yet proven

- real response loss after durable Job admission; deterministic transport-loss coverage exists;
- restart recovery from a durable semantic journal;
- cancellation racing with natural completion;
- live versioned read and atomic mutation Effects;
- live independent Verification and Fact admission;
- Tool-contract diff and pending Effect rebinding.
