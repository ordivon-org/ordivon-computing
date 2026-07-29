# 01 — Classical Execution Stack and the Edge Seam

## Classical layers

```text
physical compute and devices
→ operating-system process, filesystem, namespace, cgroup, and permission
→ container, VM, browser, serverless isolate, device runtime
→ provider control plane and native lifecycle
→ scheduler and declared workflow
→ application or Agent Task semantics
```

The lower layers already own creation, placement, resource limits, process
execution, health, snapshot, restore, retry, and destruction. Edge must not
rebuild them.

## Structural gap candidate

Classical systems normally receive a declared workload. An open Task may
discover during execution that it needs JavaScript rendering, a writable
Sandbox, a GPU, a user-authenticated browser, a region-specific endpoint, or a
physical device. The requirement is generated dynamically from Task state and
must remain attributable after provider replacement.

## Semantic separations

```text
Task ≠ Attempt ≠ Effect ≠ Dispatch ≠ Provider Execution
Task ≠ body ≠ Sandbox generation ≠ process
physical capability ≠ authorized capability ≠ allowed consequence
body deletion ≠ reversal of external effects
snapshot ≠ sufficient Task continuation state
```

## Candidate Edge seam

The narrow seam is not body implementation. It is:

- deriving a placement requirement from current work;
- observing and comparing provider capability;
- binding one semantic Effect/Dispatch to one exact provider execution;
- reconciling ambiguous remote outcomes;
- exporting durable Artifact and Observation provenance;
- reconstructing minimum sufficient work state elsewhere;
- classifying residual state after body retirement.

## Current evidence

The Cloudflare provider already demonstrates strong remote-effect mechanics:
transactional request identity, pending/committed state, generation fencing,
ambiguous-write reread, Receipt replay, private Artifacts, policy fingerprints,
and release rollback.

The local Node experiment demonstrates deterministic lifecycle, lease fencing,
one-way evidence export, reconstruction, and residual classification under a
narrow reference body.

The missing evidence is Task-level placement and cross-provider continuity.
