# EDGE-CHARTER-002 — Distributed External Presence and Execution Fabric

Status: working charter

## Mission

Ordivon Edge is the distributed external presence and execution fabric for deploying observable, disposable, and policy-scoped Agent bodies across heterogeneous environments.

A Cloudflare Worker is one Edge profile, not the definition of Edge. An Edge body may be a browser, container, virtual machine, service emulator, remote sensor, decoy, user-controlled server, or another execution substrate outside the trusted-local Runtime.

## Owned semantics

Edge owns:

- Edge Node identity, class, capability descriptor, provider, image, source, and policy revision;
- provision, admit, start, pause, freeze, snapshot, restore, retire, and destroy lifecycle;
- capability-scoped remote execution and resource leases;
- remote execution receipts, Artifacts, observations, and provenance;
- heterogeneous provider adapters behind stable node and capability contracts;
- separation between management plane, experiment plane, and evidence export;
- disposable and reconstructable remote bodies;
- multi-node campaign membership and node-level failure and recovery facts.

## Profiles

- **Production profile** — narrow capabilities, strict policy, persistent service, bounded budgets, and conservative release.
- **Research profile** — broader tools, writable state, longer execution, temporary identity, and complete capture.
- **Adversarial range profile** — high-autonomy disposable nodes, multi-stage work, Agent-created tools, controlled persistence, and whole-environment destruction.

The current `ordivon-edge` repository implements only the Cloudflare production profile: bounded Fetch, Browser Run, private R2 Artifacts, receipts, leases, release, and rollback.

## Boundaries

Edge supplies where and through which body an Agent acts. It does not decide the campaign objective, network topology, Agent cognition, or global verdict. Security owns adversarial scenarios and evaluation; Link owns connectivity; Host owns goals and tasks; Runtime owns trusted-local execution.

## Required invariants

1. Every remote action binds Node, capability, policy, Agent or Task, source, and attempt identity.
2. Node capability and consequence scope are explicit and versioned.
3. Node creation and destruction are receipted operations.
4. Evidence export cannot silently become a bidirectional management path.
5. Disposable profiles are reconstructable from declared inputs.
6. The evaluated Agent cannot rewrite the authoritative observer or lifecycle record.
7. Unknown remote outcomes reconcile before redispatch.
8. Production and adversarial profiles do not share credentials or implicit authority.

## Success condition

Edge is successful when a campaign can place Agents into heterogeneous remote bodies, allow broad internal action under a declared profile, preserve authoritative evidence, survive or explain node loss, and destroy the environment without leaving undeclared external state.
