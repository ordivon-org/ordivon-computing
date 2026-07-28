# Ordivon Project Evidence Map

## 1. Audit boundary

This map records inspected local repository revisions on 2026-07-29. It assigns only responsibilities supported by runnable code, tests, or live evidence. Repository names and future charters are not treated as proof.

| Repository | Audited revision |
|---|---|
| `ordivon-computing` | `480c9f989d505e2d3bbdaf3000f0721d552d7c29` |
| `ordivon-runtime` | `fb4a2b34e4312210443297fca7f3323d58dc1cd2` |
| `ordivon-host` | `332f30c84f50ca755f7f41ac827da5bc46b67b6c` |
| `ordivon-link` | `4cd9d2d2f4208c9799a522619ca7173befc31755` |
| `ordivon-edge` | `01e98385d0e4cdc59dd264633af143b5b71e0ebc` |
| `ordivon-finance` | `998f4b7ca611b11c478dba1508db7924b8828f25` |
| `ordivon-game` | `b1edae453c27c87939c899d9aa64731c567e414f` |
| `ordivon-security` | `4ca7ca16880a06f40032ca4dd93994482979ae34` |
| `ordivon-web` | `b94b23cfc109b774a0b5c644e5f5cc722e815139` |

The revisions are historical evidence for this study, not a mutable deployment manifest.

## 2. Responsibility matrix

| Responsibility | Current evidence | Level | Strict conclusion |
|---|---|---:|---|
| R0 purpose and consequence ownership | Host Goal/Task plans; Finance decisions; Security Campaign objectives | E2–E3 | represented in domains, no unified human-purpose authority |
| R1 operator attention and governance | CLI inspection, reports, GitHub review, external ChatGPT UI | E1–E2 | no Ordivon-owned decision queue or attention plane |
| R2 open-work continuity | Host durable Goal, Task, event projection, recovery across fresh processes and Runtime restart | E4 | bounded code-change and cognition slices proven; not a general dynamic work runtime |
| R3 context and memory compilation | task-continuation experiment; Host bounded cognition contexts; Game actor-local contexts | E4 | context compilation proven for bounded workloads; long-term memory, invalidation, and cross-task governance remain open |
| R4 cognition and coordination | Host multi-candidate admission; Game Team coordinator and provider paths | E3–E4 | local patterns exist; no general cognitive scheduler or cross-project coordination kernel |
| R5 authority and consequence admission | Semantic Core role authority; Host capability decisions; Finance authority; Security consequence envelopes; Edge policy | E3–E5 | strong shared evidence for separation, but no unified production authority model |
| R6 Effect commitment and reconciliation | Runtime Job/Attempt/recovery; Host Effect/Binding/Dispatch; Protocol; Semantic Core two-backend conformance | E4–E5 | strongest Ordivon layer; universal claims still bounded by current adapters and workloads |
| R7 evidence, verification, epistemic state | Runtime receipts; Host verification; Finance lineage; Game replay; Security ledger; Semantic Core Claim/Verification/Fact | E3–E5 | recurring cross-domain structure exists; domain verification policy remains intentionally separate |

## 3. `ordivon-runtime`

### Proven responsibility

Runtime explicitly owns the deterministic commitment boundary between Agent decisions and local reality:

- version-bound Git Workspaces;
- stable operation, Job, and Attempt identity;
- at-most-once physical dispatch admission;
- process-tree ownership;
- bounded stdout, stderr, result, progress, and Artifact evidence;
- cancellation;
- orphan and unknown-state reconciliation;
- startup repair and recovery;
- authenticated MCP entrypoint.

### Evidence

- Rust core and MCP service;
- SQLite migrations for runtime, orphan recovery, terminal repair, and reclaim;
- deterministic test suites and release-acceptance workflows;
- long-running dogfood and restart evidence in repository history.

### Does not count as

- operating-system kernel;
- model runtime;
- untrusted-code sandbox;
- Task planning or memory platform.

Runtime itself states that it grants trusted-local service-user authority and is not a sandbox.

## 4. `ordivon-host`

### Proven responsibility

Host owns durable goals, tasks, events, projections, bounded cognition contexts, candidate admission, Effect proposals, Runtime Dispatch correlation, verification receipts, and recovery assessments.

Proven slices include:

- repository read with independent digest verification;
- persistent multi-candidate cognition;
- guarded mutation;
- SourceChange Effect lowering and Binding;
- structured two-file code change and checks;
- conservative `UNKNOWN` recovery without blind redispatch;
- fresh Host and Runtime-restart recovery;
- backup, restore, Doctor, and measured event history.

### Evidence level

E4 for the bounded implemented slices.

### Does not count as

- general workflow engine;
- production multi-Agent scheduler;
- complete personal operator product;
- universal memory or coordination layer.

The repository states these limitations directly.

## 5. `ordivon-computing` and `ordivon-protocol`

### Proven responsibility

Computing owns research synthesis, reference experiments, protocol source, canonical vectors, conformance tests, and immutable evidence snapshots.

The Semantic Core experiment provides cross-backend evidence for:

- stable Effect and Dispatch identity;
- explicit unknown outcome;
- reconciliation;
- Observation, Claim, Verification, and Fact separation;
- role-scoped authority and content-bound attestation;
- durable replay;
- backend-independent semantic projection.

Host directly consumes the promoted Protocol package at an exact Computing revision.

### Evidence level

E5 for the specific Semantic Core invariants tested against Ordivon and a structurally different deterministic backend.

### Does not count as

- a shared executable kernel imported by every repository;
- proof that every sibling project conforms mechanically;
- a complete Agent Computer distribution.

## 6. `ordivon-link`

### Proven responsibility

Link implements a narrow network responsibility:

- local route, DNS, interface, VPN, WARP, and service observations;
- sanitized SQLite history and loopback console;
- controlled root-only WireGuard network namespace for selected commands;
- real egress measurement;
- Baseline wire contract and QUIC/mTLS reference transport;
- deterministic local Network World lifecycle and evidence.

### Evidence level

E4 for local observation, controlled egress, and reference transport slices.

### Does not count as

- new TCP/IP, TLS, QUIC, or cryptography;
- global overlay network;
- general multi-Agent communication fabric at production scale.

## 7. `ordivon-edge`

### Proven responsibility

Edge implements its Cloudflare production profile:

- authenticated Worker operations;
- external Fetch and Browser Rendering policy;
- R2 Artifact storage;
- request identity and idempotency state;
- budgets, rate limits, receipts, release identity, and cleanup;
- provider-neutral Node contracts and a rootless local disposable-node adapter.

### Evidence level

E4 for the Cloudflare external-capability profile; E3 for the provider-neutral Node lifecycle and local adapter.

### Does not count as

- general cluster scheduler;
- production VM or container fleet manager;
- proof of multi-provider remote body portability.

## 8. `ordivon-finance`

### Proven responsibility

Finance is a real domain system with:

- observable capital state and imports;
- valuation, exposure, data quality, and explicit unknowns;
- authority, decision basis, effect acceptance, reconciliation, and recovery;
- deterministic core, local runtime, provider paths, and extensive tests.

### Contribution to the overlay

Finance supplies strong domain evidence that:

```text
evidence ≠ authority
provider output ≠ domain truth
receipt ≠ accepted account state
unknown outcome requires reconciliation
```

### Does not count as

A generic Host, Runtime, or universal epistemic engine.

## 9. `ordivon-game`

### Proven responsibility

Game implements a deterministic world plus Host-conformant domain coordination:

- persistent World and Host journals;
- actor-local Contexts;
- Goal and Task projections;
- provider proposals;
- attribute-based authority;
- Team rounds, plans, messages, Effects, Dispatches, Observations, replay, and evaluation evidence.

### Evidence level

E3–E4 for its M3 world and team slices, including deterministic and live-provider evaluation paths.

### Contribution to the overlay

Game is the strongest current laboratory for R3/R4 coordination, role-local context, replay, and explicit world authority.

### Does not count as

Mechanical conformance to the promoted cross-repository Protocol or a general Host replacement.

## 10. `ordivon-security`

### Proven responsibility

Security contains executable boundaries for:

- Campaign manifest admission;
- append-only authority ledger;
- immutable component bindings;
- prepare/start/freeze/reset/destroy coordination;
- unknown-result reconciliation;
- residual-state classification;
- reconstruction identity;
- sealed evidence-bundle replay;
- independent judge and consequence-envelope contracts.

### Evidence level

E3 for Campaign and lifecycle contracts and fault cases.

### Does not count as

- Red or Blue Agent implementation;
- exploit execution;
- endpoint detection or prevention;
- production containment enforcement.

The repository explicitly states that no executable attack implementation exists.

## 11. `ordivon-web`

### Proven responsibility

Web is a small public publication surface with maintained routes, canonical metadata, sitemap, feed, link checks, responsive browser tests, and deployment workflows.

### Does not count as

- private operator console;
- Task control plane;
- Host or Runtime interface.

## 12. Current unowned or weakly owned responsibilities

### Operator attention

No repository owns a unified queue of decisions, escalations, consequences, alternatives, and evidence across the series.

### Context invalidation and durable memory governance

Host and experiments compile bounded context, but no system owns long-term source invalidation, memory promotion, poisoning resistance, or cross-task reuse.

### Cognitive scheduling

No system consistently chooses among model, branch, verifier, stopping, and human escalation based on measured information value and consequence.

### Unified authority semantics

Several strong local models exist, but principal, Goal binding, world version, consequence, budget, expiry, and revocation are not one mechanically consumed cross-project contract.

### Cross-domain verification relations

Claim, evidence, verification, and fact recur across projects. A stable minimal relation is plausible, but no shared production package or second direct consumer yet proves the exact boundary.

## 13. Overall conclusion

The Ordivon series has not built a full alternative computer stack. It has built meaningful vertical evidence around the point where probabilistic proposals meet durable effects and world evidence.

The strongest center is:

```text
Host semantic work and admission
→ Runtime deterministic commitment
→ Observation and Artifact evidence
→ recovery and verification
```

The next research frontier lies above and around that center, not below Linux or inside a replacement database.
