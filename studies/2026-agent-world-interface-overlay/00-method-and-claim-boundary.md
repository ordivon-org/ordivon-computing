# 00 — Method and Claim Boundary

## Research objective

Determine which Edge and Link responsibilities are genuinely introduced or
structurally rewritten by open, probabilistic, persistent Agent Tasks, while
leaving mature execution and network mechanisms below the boundary.

## Strong-baseline rule

No Ordivon abstraction is admitted merely because it is useful, elegant, or
present in current code. It must defeat the strongest relevant classical
baseline under a realistic trajectory.

For Edge, baselines include provider SDKs, Sandbox APIs, workflow engines,
schedulers, cloud operation polling, browser services, snapshots, provenance,
and direct Host adapters.

For Link, baselines include DNS, HTTP clients, CNI, VPNs, proxies, service
meshes, workload identity, queues, retries, observability, network simulation,
and direct Host adapters.

## Responsibility admission test

```text
Which lower mechanism is insufficient?
Which exact invariant remains unowned?
Which realistic trajectory fails when the candidate layer is bypassed?
Which second workload reproduces the failure?
Can a local adapter or Host policy solve it more cleanly?
```

## Evidence classes

1. primary specifications and maintained implementation contracts;
2. exact Ordivon code, tests, and operational receipts;
3. controlled fault-injection trajectories;
4. comparative implementations against strong baselines;
5. sustained real workload use;
6. counterexamples and deletion tests.

## Claim discipline

- Current Cloudflare execution proves one reliable provider, not a universal
  Edge model.
- Current local `unshare` execution proves a narrow body/lifecycle experiment,
  not persistent Agent embodiment.
- Current Network World proves deterministic state, events, and a loopback
  fixture, not a general Agent-native network layer.
- Current Security composition proves cross-component lifecycle/evidence
  interoperability, not Edge/Link attachment or correct long-term boundaries.
- Similar names across projects do not establish shared identity or authority.

## Research output

The study should produce:

- a classical authority map;
- minimal field inventories, not premature schemas;
- failure trajectories and falsifiers;
- two real workloads per candidate responsibility;
- measured comparison with direct integration;
- explicit promote, absorb, freeze, or delete decisions.
