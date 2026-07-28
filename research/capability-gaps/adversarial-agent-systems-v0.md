# Minimum Capability Gaps for Link, Edge, and Security

Status: initial gap register

This register names the minimum missing capabilities implied by the current Charters. It is not a commitment to implement every advanced feature. P0 means the research claim cannot be made credibly without it.

## Ordivon Link

### P0 — range experiments are not yet valid

1. **Network world manifest** — typed nodes, links, subnets, trust zones, identity domains, routes, and external boundaries.
2. **Deterministic lifecycle** — create, inspect, freeze, reset, and destroy one named network world.
3. **Programmable fault plane** — latency, jitter, loss, bandwidth, partition, DNS, route, and service-reachability mutation.
4. **Independent observer** — append-only connection and topology events outside evaluated-Agent control.
5. **Explicit egress proof surface** — declared allowed exits plus measured evidence; no assumption that missing routes imply isolation.
6. **Control API** — versioned topology and mutation commands consumable by Security and Game.
7. **Synthetic identity lifecycle** — range-only node and communication identity creation, rotation, revocation, and reset.

### P1 — full-spectrum network behavior

- dynamic topology and moving trust boundaries;
- Agent-to-Agent communication graph and message provenance;
- deception nodes, sinkholes, mirrors, and service identity emulation;
- repeatable traffic capture and network replay;
- production adapters for mature TCP, QUIC, VPN, proxy, and mediation implementations;
- multi-host range federation and partial-controller failure recovery.

### P2 — frontier research

- large distributed ranges;
- mobile, intermittent, and heterogeneous physical links;
- adaptive network policies competing with adaptive Agents;
- hardware-backed observation and high-fidelity impairment.

## Ordivon Edge

### P0 — Edge is still one Cloudflare product slice

1. **Edge Node contract** — identity, class, provider, image or source, capabilities, policy, resources, and lifecycle state.
2. **Provider-neutral lifecycle** — provision, admit, start, freeze, snapshot, restore, retire, and destroy.
3. **Execution profiles** — production, research, and adversarial range profiles with separate credentials and authority.
4. **Disposable substrate adapter** — at least one container or VM implementation beyond Cloudflare Worker.
5. **Management-plane separation** — evaluated nodes cannot reach lifecycle authority or authoritative evidence storage.
6. **Evidence export contract** — one-way, identity-bound Artifact and event export from disposable worlds.
7. **Node lease and reconciliation** — uncertain provision, execution, loss, and destruction outcomes become explicit.
8. **Reconstruction receipt** — prove which declared inputs recreate a destroyed node.

### P1 — distributed presence

- browser, container, VM, service-emulator, sensor, and decoy node classes;
- campaign membership and multi-node coordination identity;
- checkpoint and restore plus partial-world recovery;
- controlled dependency and tool installation inside research profiles;
- heterogeneous cloud and user-owned provider adapters;
- remote resource accounting and failure-domain placement.

### P2 — frontier research

- multi-region and cross-provider placement;
- accelerator and specialized hardware bodies;
- long-lived migratable Agent bodies;
- high-fidelity physical or IoT interfaces in isolated facilities.

## Ordivon Security

### P0 — no executable laboratory exists yet

1. **Campaign manifest** — world, actors, objectives, authority, capability envelope, consequence envelope, time, resources, and stop conditions.
2. **Range authority registry** — every target and service binds to owned or explicitly authorized experiment state.
3. **Maximum-elicitation profile** — exact model, Host, tools, memory, time, compute, and collaboration configuration.
4. **Actor contracts** — Red, Blue, neutral, user, service, observer, and judge identities with independent authority.
5. **Independent judge and event root** — evaluated Agents cannot rewrite score, topology truth, or containment evidence.
6. **Replay bundle** — exact revisions, prompts and context inputs, Tool contracts, events, Artifacts, budgets, and world snapshots.
7. **Containment and kill circuit** — out-of-band freeze and destruction path plus evidence that it remains independent.
8. **Deterministic reset** — recreate one baseline world and prove residual state was removed or accounted for.
9. **Seed benchmark family** — at least one adaptive Red or Blue scenario, not only a fixed vulnerable target.
10. **Outcome taxonomy** — distinguish objective success, partial progress, defense success, escape, observer loss, invalid experiment, and inconclusive evidence.

### P1 — full-spectrum adversarial research

- dynamic multi-stage system and Web campaigns;
- adaptive Blue Agents, deception, and service restoration;
- prompt, context, memory, Tool, Artifact, identity, delegation, and supply-chain attacks;
- multi-Agent teams with ownership, communication, betrayal, and coordination failures;
- tool generation and controlled persistence inside the range;
- long-horizon campaigns with environment mutation and model or Host replacement;
- causal comparison of model, Harness, Tool, budget, and topology contributions.

### P2 — frontier research

- attack-defense coevolution across repeated campaigns;
- evidence-governed policy or Skill learning;
- organizational Agent structures and resource economies;
- days-long campaigns and cross-range transfer studies;
- post-training datasets and evaluation feedback derived from verified trajectories.

## Shared P0 gaps

Across all three projects, the stack still lacks:

- one stable World or Range identity shared by Host, Runtime, Link, Edge, Game, and Security;
- one actor and node provenance chain across cognition, network, execution, and evidence;
- one external-consequence ledger distinct from internal capability;
- independent observer integrity and loss reporting;
- whole-world freeze, export, reset, and destruction receipts;
- a cross-project conformance test proving the same campaign identities survive every boundary.
