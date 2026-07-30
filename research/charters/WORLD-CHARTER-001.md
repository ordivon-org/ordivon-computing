# WORLD-CHARTER-001 — Task-to-World Interaction Continuity

Status: active research charter

Supersedes the future responsibility claims in `EDGE-CHARTER-003` and
`LINK-CHARTER-003`. Those charters remain historical records of the intermediate
placement/connectivity decomposition and the evidence that led to unification.

## Mission

Ordivon World studies the boundary through which an open Task discovers,
connects to, invokes, observes, and recovers external work across services,
providers, Agents, humans, devices, and data without depending on one path,
endpoint, identity, transport, provider, body, participant, or response channel.

```text
Goal / Task / Task Attempt / Effect
              │ foreign semantic references
              ▼
      World Interaction intent
              ▼
 target / identity / path / transport / provider / capability observations
              ▼
       exact Interaction Binding
              ▼
 mature network, identity, API, Browser, Sandbox, queue, storage, Agent or device
              ▼
 delivery / provider execution / Receipt / Artifact / Observation / callback
              ▼
 reconcile / invalidate / rebind / verify / continue
```

World is not a network stack, proxy, VPN, CNI, Service Mesh, identity platform,
Browser, Sandbox, VM orchestrator, scheduler, workflow engine, queue, storage
system, or cloud control plane. Those systems remain authoritative for their
native mechanisms and physical state.

## Why Edge and Link converge

The former decomposition was useful for identifying classical boundaries, but
it is not the correct top-level Task object:

1. the intended Effect determines endpoint, path, transport, session, locality,
   identity, and provider requirements;
2. path, region, identity, and provider conditions can change the observation or
   consequence;
3. a timeout cannot be reconciled from communication or provider-operation
   state alone;
4. provider replacement usually changes endpoint, identity, path, body, and
   callback together;
5. remote-to-local callbacks and remote-to-remote Artifact movement repeatedly
   cross the former boundary;
6. separate repositories forced premature NetworkAttachment, cross-project
   identity, and continuity contracts.

The atomic research object is therefore one **World Interaction**. Connectivity
and external action remain internal analytical planes with separate revisions,
not independent project ownership.

## Candidate owned semantics

World may own the following only after cross-workload evidence:

1. **Interaction intent** — bounded external relation, capability, consequence,
   data, locality, identity, evidence, duration, callback, and continuity needs
   of one Task Attempt or Effect.
2. **Candidate Observation** — versioned, expiring facts about targets,
   participants, endpoints, paths, transports, providers, capabilities, cost,
   policy, availability, and uncertainty.
3. **Interaction Binding** — immutable correlation from Task, Task Attempt, Effect, and
   Dispatch references to exact target, identity, path, transport, provider,
   physical execution, authority, policy, and observation revisions.
4. **Delivery and execution correlation** — explicit distinction among message
   or request delivery, provider acceptance, physical execution, response, and
   semantic Effect satisfaction.
5. **Remote uncertainty** — preservation of accepted, delivered, running,
   replied, succeeded, failed, rejected, cancelled, compensated, and unknown
   states without blind retry.
6. **Conditioned provenance** — body, provider, endpoint, path, identity, region,
   method, policy, build, and time conditions under which an Artifact,
   Observation, or Claim was produced.
7. **Invalidation and reconciliation** — dependency-aware determination of which
   evidence, permissions, and pending work become stale after external change.
8. **Rebinding and continuation** — replacement of path, endpoint, transport,
   provider, body, identity, or participant while preserving the parent Task.
9. **Residual closure** — explicit evidence for remaining sessions, callbacks,
   credentials, provider objects, queued work, external Effects, and retained
   evidence after an interaction ends.

These are field inventories, not admitted protocol schemas.

## Foreign semantics

World references but does not redefine:

- Goal, Task, Task Attempt, Effect, Claim, Verification, commitment, strategy, and
  completion;
- trusted-local Workspace, Job, process, cancellation, and recovery;
- packets, routes, DNS, VPNs, proxies, meshes, transports, PKI, and workload
  identity;
- Browser, Sandbox, VM, function, queue, object store, device, and provider
  lifecycle;
- domain authorization, compliance, and final validity.

Host owns why work occurs and whether to replan. Runtime owns trusted-local
physical work. Classical systems own native mechanisms. Security or the domain
system owns consequence authority and final validity.

## Current implementation carrier

`ordivon-world` preserves the histories and working implementations of the
former prototypes:

- `providers/cloudflare/` — bounded Fetch/Browser/R2 provider, remote request
  state, Receipts, Artifacts, fencing, reconciliation, release, and operations;
- `modules/network-observation/` — network observations, sanitized history,
  private egress tools, deterministic network-condition experiments, and bounded
  reference transports.

No universal resolver, Interaction Binding schema, automatic path/provider
selector, participant registry, or production World data plane currently exists.

## Topology under study

- local → remote action or query;
- remote → local callback, stream, approval, or result;
- remote → remote Artifact transfer or provider chaining;
- one → many fan-out;
- many → one join;
- many ↔ many multi-Agent and multi-provider interaction graphs.

World should preserve semantic control and evidence without proxying all bytes.

## Research route

### W1 — first complete interaction

Run one real Host Task through a current path/target Observation and the existing
Cloudflare Fetch or Browser provider. Preserve exact semantic, communication,
provider, policy, Receipt, and Artifact identities. Inject response loss or Host
restart and reconcile the original interaction before redispatch.

### W2 — field deletion and direct-baseline comparison

Compare with direct Host provider calls and direct network inspection. Delete
candidate fields until only those preventing duplicate Effects, false recovery,
stale evidence, excess consequence, or unexplained authority remain.

### W3 — second workload

Use either asynchronous Agent/service Artifact review with participant handoff or
an external programmable Sandbox with remote-to-remote Artifact movement and
provider replacement.

### W4 — graph topology and independent rebinding

Test callback, remote-to-remote transfer, fan-out, join, and independent/joint
replacement of path, provider, transport, identity, body, and participant.

### W5 — architecture decision

Retain a thin World layer, absorb it into Host, preserve only provider and
observation modules, or delete the unproven shared abstractions.

## Falsifiers

Reduce or delete independent World semantics if:

- Host plus direct provider/network adapters preserve the same uncertainty,
  provenance, invalidation, and recovery with less permanent machinery;
- shared fields do not generalize across two materially different workloads;
- connectivity and execution correlation adds no failure prevention beyond
  ordinary traces and provider operation IDs;
- remote-to-remote and callback flows need no Task-level shared state;
- one combined object obscures independently changing path and provider
  revisions;
- operational modules remain useful but the unified control layer does not.

## Success condition

World succeeds when open Tasks can interact with multiple external objects
through replaceable paths, providers, transports, identities, bodies, and
participants; preserve exact conditioned evidence and uncertain outcomes; avoid
duplicate Effects; continue after replacement; and do so with less permanent
complexity than direct integration.
