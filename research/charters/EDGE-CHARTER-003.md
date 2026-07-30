# EDGE-CHARTER-003 — Task-to-External-Execution Continuity Overlay


> **Historical intermediate charter:** superseded by [`WORLD-CHARTER-001`](WORLD-CHARTER-001.md) after external placement and connectivity were unified as one Task-to-World Interaction responsibility.
Status: historical intermediate charter — superseded by WORLD-CHARTER-001

Supersedes the long-term responsibility claim in
[`EDGE-CHARTER-002`](EDGE-CHARTER-002.md). Charter 002 remains a historical
record of the Phase 0 body/lifecycle hypothesis and its evidence.

## Mission

Ordivon Edge studies and supplies the semantic boundary through which an open
Task obtains external execution capability from mature providers without making
the Task depend on any one browser, Sandbox, container, virtual machine,
serverless isolate, device, machine, region, or cloud.

Edge is not a replacement Sandbox, container runtime, VM orchestrator,
scheduler, browser implementation, cloud control plane, or device platform.
Those systems remain authoritative for their physical resources and native
lifecycle. Edge adds the Task-level placement, binding, reconciliation,
provenance, and continuation semantics that those substrates do not own.

```text
Goal / Task / Task Attempt / Effect
              │ foreign semantic references
              ▼
      placement requirement
              ▼
 provider capability observations and candidates
              ▼
        placement binding
              ▼
 mature browser / Sandbox / VM / function / device provider
              ▼
 provider execution identity, Receipt, Artifact, residual evidence
              ▼
       Host continues the Task
```

## Central distinction

```text
Provider body lifecycle
  creates, runs, suspends, snapshots, and destroys physical execution objects

Edge continuity semantics
  explain why a Task uses one of those objects, bind one Effect to one physical
  execution, reconcile uncertain outcomes, export durable results, and continue
  after the object or provider is replaced
```

A remote body is not automatically an Agent-native abstraction. The durable
candidate responsibility is the relation between open work and replaceable
external bodies.

## Candidate owned semantics

Edge may own the following semantics when experiments demonstrate that they are
shared and non-bypassable:

1. **Placement Requirement** — a bounded description of the execution
   capabilities, data, locality, credential domain, duration, resource class,
   reversibility, evidence, and consequence requirements of one Task Attempt or
   Effect.
2. **Provider Capability Observation** — versioned, time-bounded facts about
   what a provider currently offers, under which policy, cost class, quota,
   region, and evidence freshness.
3. **Placement Candidate** — one provider-native way to satisfy a Placement
   Requirement, with explicit strengths, limitations, uncertainty, and binding
   inputs.
4. **Placement Binding** — an immutable relation from Task, Task Attempt, and Effect
   references to the exact provider, body or Sandbox generation, capability and
   policy revision, and provider execution identity used by a Dispatch.
5. **External execution reconciliation** — preservation of `accepted`,
   `running`, `known_success`, `known_failure`, and `unknown` without treating a
   transport failure as world failure or blindly redispatching an Effect.
6. **Artifact and Observation provenance** — durable export of results from a
   temporary body, including content identity, originating Effect and Dispatch,
   execution environment, provider revision, and verification status.
7. **Semantic reconstruction** — declaration of the minimum sufficient inputs
   needed to continue work on another body instead of defaulting to whole-VM
   cloning.
8. **Residual closure** — explicit evidence about provider objects, background
   work, credentials, and external effects that remain after a body is retired
   or destroyed.

These objects are research candidates. Their exact schemas do not belong in
Core or Protocol until two materially different workloads prove them.

## Foreign semantics

Edge references but does not redefine:

- Goal, Task, Task Attempt, Effect, Dispatch, Claim, Verification, and Fact identities;
- human or organizational authority and consequence ownership;
- local Workspace, Job, process, and recovery lifecycle;
- network path, communication identity, route, and connectivity evidence;
- provider-native Sandbox, VM, browser, function, device, image, snapshot,
  scheduler, and resource objects.

Host or the semantic Kernel remains authoritative for open-work state and Effect
history. Runtime remains authoritative for trusted-local execution. Link remains
authoritative for Task-conditioned connectivity. Providers remain authoritative
for physical execution objects.

## Current repository interpretation

The current `ordivon-edge` repository contains three distinct evidence classes:

1. **Real production provider** — Cloudflare Fetch, Browser Run, private R2
   Artifacts, transactional request state, release, rollback, and operations.
2. **Remote-effect reliability evidence** — stable Request IDs, pending and
   committed states, generation fencing, ambiguous-write reread, Receipt replay,
   Artifact cleanup, and policy/version binding.
3. **Body/lifecycle research substrate** — provider-neutral Node contracts,
   deterministic lifecycle, local `unshare` reference body, Security control
   session, reconstruction, and residual evidence.

The third class is not promoted to a permanent Agent-native Node core by this
charter. It remains a useful hypothesis and conformance substrate. Current code
does not implement a Placement Requirement, candidate comparison, Host-level
Placement Binding, automatic router, cross-provider body replacement, or
Task-continuation benchmark.

## Research route

### E0 — Preserve operational truth

Keep the Cloudflare provider reliable and production-usable. Do not destabilize
its existing Fetch, Browser, Receipt, Artifact, release, and reconciliation
surfaces while the higher semantic model is researched.

### E1 — Prove one Host-consumable external Effect backend

Bind one real Host Effect to the existing Cloudflare provider with exact Effect,
Dispatch, provider execution, Receipt, Artifact, policy, and version identities.
Inject response loss and prove reconciliation without duplicate work.

### E2 — Derive Placement Requirement from two real workloads

Use at least two materially different workloads, such as dynamic Web research
and disposable software execution. Record which requirement fields are truly
needed and which are provider-specific noise. Do not build an automatic router.

### E3 — Prove body and provider replacement

Continue one Task across two different external execution substrates using only
minimum sufficient reconstruction inputs. Measure lost work, duplicated work,
state volume, explanation quality, and residual state.

### E4 — Test multi-body branch and join

Run parallel Attempts on heterogeneous bodies, preserve separate provenance,
and join their Artifacts into one Task without inventing a permanent Agent body.

### E5 — Revisit persistent presence only under evidence

Introduce a durable Agent-presence identity only if real asynchronous or
long-lived workloads fail without it and the responsibility cannot remain a
Task role, service identity, Provider object, or Host participant binding.

## Admission tests

A proposed Edge abstraction must answer:

1. Which mature provider, scheduler, workflow, or Sandbox mechanism is
   insufficient?
2. Which exact Task-level invariant remains unowned?
3. What realistic failure occurs if the abstraction is deleted?
4. Which second workload demonstrates the same invariant?
5. Can the result remain a Host policy, provider adapter, or external Binding
   rather than a new resident service?

## Falsifiers

Reduce or delete the independent Edge semantic layer if:

- Host plus direct provider APIs preserve the same Task, Effect, uncertainty,
  Artifact, and replacement semantics without duplicated application logic;
- provider replacement requires complete provider-native snapshots and no
  stable cross-provider semantic state exists;
- Placement Requirement fields do not generalize beyond one workload;
- a persistent Agent Node identity creates misleading continuity or merely
  renames Task, service, or Sandbox identity;
- residual evidence adds no recovery, safety, cost, or explanatory value.

## Success condition

Edge succeeds when one open Task can choose and bind an external execution
substrate, survive ambiguous remote outcomes, export sufficient evidence and
Artifacts, replace or parallelize bodies, close residual state, and continue
without rewriting the Task or reimplementing the underlying execution platform.
