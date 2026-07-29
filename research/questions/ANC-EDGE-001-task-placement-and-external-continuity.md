# ANC-EDGE-001 — Task Placement and External Execution Continuity

## Status

- Epistemic status: active foundational research question
- GitHub issue: #66
- Parent program: Agent-Native Responsibility Overlay
- Implementation owner: `ordivon-edge`
- Semantic consumers: `ordivon-host`, semantic Kernel, `ordivon-runtime`
- Related questions: `ANC-MEMORY-001`, `ANC-IR-001`, `ANC-EFFECT-001`,
  `ANC-WORLD-001`, `ANC-SECURITY-002`

## Question

Which semantics are required for an open Task to obtain, bind, replace,
parallelize, and release external execution bodies while preserving Effect
identity, uncertainty, Artifact provenance, residual evidence, and Task
continuity across heterogeneous mature providers?

## Why this is not ordinary scheduling

Classical schedulers and provider control planes already own resource
allocation, placement constraints, images, processes, Sandboxes, VMs,
serverless isolates, browsers, snapshots, quotas, health, and lifecycle.

The unresolved candidate responsibility begins above those mechanisms:

```text
Task discovers an execution need during work
→ need is translated into a provider-independent requirement
→ one exact provider execution is selected and bound to one Effect/Dispatch
→ result may be success, failure, running, accepted, or unknown
→ durable Artifacts and evidence leave the temporary body
→ the body may disappear or be replaced
→ the parent Task continues without invented history or full restart
```

## Objects under investigation

- Placement Requirement;
- Provider Capability Observation;
- Placement Candidate;
- Placement Binding;
- Provider Execution reference;
- external execution Receipt;
- Artifact/Observation provenance;
- semantic Reconstruction Set;
- residual and destruction evidence;
- optional persistent presence identity.

Each object is provisional. The research must find the minimum sufficient set,
not ratify all names.

## Classical baselines to defeat

1. Direct Host calls to provider SDKs and Tool APIs.
2. Durable workflow engines with activity retries and idempotency keys.
3. Kubernetes/Nomad/Slurm-style scheduling and reconciliation.
4. Sandbox products with session, snapshot, file, and process APIs.
5. Browser automation services with persistent sessions and Artifacts.
6. Cloud resource managers with client tokens and operation polling.
7. W3C-PROV/OpenTelemetry-style provenance and traces.

The Edge layer is not justified unless realistic trajectories remain difficult,
ambiguous, or repeatedly reimplemented above these baselines.

## Required failure trajectories

### F1 — capability discovery after Task start

A research Task begins with HTTP Fetch, discovers JavaScript rendering, then
requires a full browser and later a programmable Sandbox. The Task must preserve
why each escalation occurred and which evidence each body produced.

### F2 — response loss after remote completion

The provider commits Artifacts but the caller loses the response. Recovery must
query the original identity and avoid duplicate work or contradictory evidence.

### F3 — body death before evidence export

A temporary body disappears after local progress but before Task-visible
Artifact export. The experiment must classify what was durable, what was lost,
and whether the reconstruction contract was sufficient.

### F4 — cross-provider replacement

The same Task continues from provider A to provider B without loading the full
original transcript or cloning a complete machine. Minimum sufficient inputs
must be explicit and digest-bound.

### F5 — parallel bodies and join

Two heterogeneous bodies advance different Attempts. Their outputs must retain
separate provenance and join without being mistaken for one physical Agent
execution.

### F6 — body destruction with external residue

The Sandbox is gone but external resources, background jobs, credentials, or
writes may remain. Task closure must not equate body deletion with consequence
reversal.

## Research tasks

1. Map classical execution, scheduling, Sandbox, browser, and cloud operation
   lifecycles and mark their authority boundaries.
2. Audit every current `ordivon-edge` type against Task, Attempt, Effect,
   Dispatch, Provider, body, Sandbox generation, and execution identity.
3. Determine whether `EdgeNodeIdentityInput` describes presence, deployment
   specification, Sandbox generation, or an overloaded mixture.
4. Define a schema-free field inventory for Placement Requirement and test it
   against two real workloads.
5. Bind one Host Effect to the current Cloudflare provider and inject response
   loss, stale executor, policy change, and Artifact commit ambiguity.
6. Compare direct provider integration against an Edge Binding layer for code
   volume, duplicated logic, recovery clarity, and evidence quality.
7. Run one cross-provider continuation experiment using minimum sufficient
   reconstruction inputs.
8. Measure whether residual closure predicts operational failures or materially
   improves recovery.
9. Attempt to delete persistent Node identity from the model; reintroduce it
   only when a real workload fails.

## Evidence requirements

- exact source revisions and provider versions;
- Task, Attempt, Effect, Dispatch, Binding, and Provider Execution identities;
- injected failure point and observed world result;
- content digests for exported Artifacts;
- reconstruction input set and byte size;
- duplicated and lost work measurements;
- residual-state inventory;
- comparison against the strongest direct-provider baseline;
- at least two materially different workloads.

## Decision outcomes

- **Promote:** a compact cross-workload placement/continuity responsibility is
  proven and cannot be owned by Host or provider adapters alone.
- **Keep in Research:** useful concepts exist but identity, routing, or
  reconstruction fields remain workload-specific.
- **Absorb:** Host plus provider adapters own the responsibility more cleanly.
- **Delete:** the current Node/presence abstraction adds no value beyond mature
  provider lifecycle.
