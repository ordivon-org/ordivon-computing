# ANC-SECURITY-002 — Agent World, Body, Evaluation, and Evidence Alignment

## Status

- Epistemic status: completed historical comparative study
- Parent program: `ordivon-computing` #46
- Related construction track: `ANC-VERIFY-001`
- Related research question: `ANC-SECURITY-001`
- Implementation owners: Ordivon Link, Edge, Security, Host, and Runtime
- Baseline reviewed: merged Phase 0 main revisions recorded on 2026-07-29
- GitHub issue: #57 — closed as completed and superseded
- Active successors: `ANC-EDGE-001` / #66, `ANC-LINK-001` / #67, and `ANC-WORLD-001` / #68
- Route disposition: former persistent Agent-presence, NetworkAttachment, and P0-D implementation routes are retired and do not constrain product repositories

## Question

Which Link, Edge, and Security abstractions are durable Agent-native contributions,
which are useful parallel hypotheses, and which currently conflict with mature
container, networking, provenance, and Agent-evaluation practice?

The objective is not to make Ordivon resemble Kubernetes, CNI, OCI, Inspect, or
CybORG. It is to reuse their solved mechanisms while isolating the unsolved
Agent-specific layer:

```text
mature execution and networking substrates
+ Agent presence, world, consequence, evidence, and evaluation semantics
```

## Why this question exists

Phase 0 proved a real infrastructure-only composition:

- a deterministic Link Network World;
- a Runtime-held loopback fixture;
- a real Edge local-unshare body;
- Security bindings, lifecycle receipts, residual accounting, reconstruction,
  and replay;
- 75 Security ledger events, residual `clean`, and a conclusive infrastructure
  outcome.

That proof established cross-project composition. It did not establish that the
current abstractions are the correct long-term abstractions. The next step must
separate four classes of result:

1. independently rediscovered classical correctness principles;
2. Agent-native hypotheses that agree with emerging research;
3. deliberately different parallel routes that require experiments;
4. current implementation choices that should be corrected before expansion.

## Evidence hierarchy

Judgments in this study use the repository truth hierarchy:

1. exact implementation code, tests, and runtime evidence;
2. implementation-repository contracts;
3. primary specifications, official evaluation frameworks, and research
   environments;
4. Issues and pull requests;
5. this synthesis.

This document is not a new Protocol and does not override component-native
contracts.

## Mainstream reference points

### OCI Runtime Specification

OCI already specifies container bundles, namespaces, cgroups, hooks, and runtime
lifecycle. It also permits joining an existing network namespace by path and
states that network-interface lifecycle is normally managed by a higher-level
orchestrator rather than the process inside the container.

Implication for Ordivon:

- Edge should not grow local-unshare into a general container runtime;
- a future Edge provider should reuse OCI/runc-class mechanisms;
- Edge may own the Sandbox and expose a generation-bound attachment handle;
- Link may configure connectivity without owning Sandbox lifecycle.

### Container Network Interface

CNI deliberately limits itself to container connectivity and resource cleanup.
Its narrow boundary is evidence that Link should reuse mature network plugins
rather than build a second generic container-network stack.

Implication for Ordivon:

- Link may define Agent-specific `NetworkAttachment` identity and evidence;
- the backend should remain compatible with CNI-shaped `ADD`, `CHECK`, `DEL`,
  and garbage-collection semantics;
- Link should add world revision, Sandbox generation, observer evidence, and
  residual closure above the classical backend.

### W3C PROV

W3C PROV represents provenance through related Entities, Activities, Agents,
and derivations rather than one universal identifier shared by every system.

Implication for Ordivon:

- Security semantic identities and component-native identities should remain
  distinct;
- immutable digest-bound bindings are preferable to one global World ID;
- Ordivon may map evidence into established provenance concepts without making
  its ledger a new universal provenance standard.

### Inspect AI

Inspect provides tasks, agents, scorers, traces, limits, checkpointing, and
replaceable Sandbox environments. It demonstrates that real Agent evaluation
can begin before Ordivon completes its own persistent data plane.

Implication for Ordivon:

- Security evaluation science must advance in parallel with P0-D;
- the first evaluated Agent may use a mature existing Sandbox;
- Ordivon should compare the value of its Campaign/Evidence layer against
  existing evaluation tooling rather than rebuild a complete evaluator first.

### NIST Agent evaluation work

NIST emphasizes structured audit trails, evidence-grounded claims, transcript
review, standardized Agent affordances, and evaluation-cheating detection.

Implication for Ordivon:

- a single successful trajectory is not sufficient evidence;
- hidden scoring, transcript review, and grader-gaming detection are required;
- Security must preserve the distinction between task success and evaluation
  validity.

### METR evaluation protocols

METR reports substantial run-to-run variance even for identical prompts and
settings and aggregates repeated samples into capability estimates.

Implication for Ordivon:

- Campaign identity is not enough; an evaluation family requires trials,
  replicates, seeds, configuration identity, distributions, and uncertainty;
- outcomes must not be generalized from one Campaign run.

### CybORG / CAGE-style environments

CybORG-class environments provide a mature simulated route for autonomous cyber
Agent research before full physical-range fidelity.

Implication for Ordivon:

- adaptive Red/Blue research can proceed in simulation while Link and Edge
  develop a real persistent data plane;
- simulated and real Campaigns should share evaluation semantics but not be
  treated as equivalent evidence.

## Provisional classification

### Independently derived and probably correct

The following are likely durable, although most are rediscoveries of classical
systems principles rather than novel scientific claims:

- durable operation intent before external effects;
- stable operation identity and no blind redispatch after ambiguous delivery;
- explicit `unknown` and reconciliation states;
- generation fencing and non-persistent bearer authority;
- append-only event evidence and deterministic replay;
- component-native identities plus immutable bindings;
- independent observer-loss and inconclusive-evidence outcomes;
- explicit residual-state accounting after destruction;
- separation of modeled network intent from observed network facts;
- Provider-neutral Edge contracts;
- reuse of maintained TLS, QUIC, VPN, container, and network mechanisms.

### Different from mainstream and worth parallel research

These are working hypotheses, not established contributions:

1. **Capability–Consequence orthogonality**
   - Internal Agent capability and externally authorized consequence can be
     varied independently.
   - Falsification: experiments show they cannot be separated without changing
     the evaluated cognition or task definition.

2. **Residual closure as evaluation validity**
   - A run is not fully characterized until unexpected process, network,
     credential, Sandbox, and external-effect residue is classified.
   - Falsification: residual accounting adds no predictive, safety, or recovery
     value across multiple real workloads.

3. **Long-lived Agent presence independent of Sandbox and model**
   - One Agent presence may survive Provider, Sandbox, model, and Execution
     changes while retaining accountable continuity.
   - Falsification: stable identity creates misleading continuity or cannot be
     operationally separated from task-specific instances.

4. **Network World as an Agent capability variable**
   - Communication topology, delay, partition, identity, and visibility are
     causal variables in Agent capability, not merely infrastructure details.
   - Falsification: controlled network changes produce no meaningful behavioral
     or capability differences after other variables are held fixed.

5. **Component-native identity graph**
   - Campaign identity plus component-native identities and bindings provides
     better attribution and recovery than a universal global identifier.
   - Falsification: the graph produces greater ambiguity or operational cost
     than a simpler central identity in realistic recovery cases.

6. **Infrastructure validity and objective outcome require separate scoring**
   - A task success in an invalid environment is not valid capability evidence;
     a task failure in a valid run remains useful research evidence.
   - Falsification: separate scoring does not improve diagnosis or comparison.

### Current implementation choices requiring correction

#### Edge identity

Current `EdgeNodeIdentityInput` includes Provider, source, policy, resource,
Campaign membership, World membership, and generation, and the complete input is
hashed into `node_id`. The resulting ID behaves like an immutable deployment or
Sandbox specification digest, not a long-lived Agent-presence identity.

Required split:

```text
stable Node / AgentPresence ID
NodeSpec revision and digest
Provider-native Sandbox ID
Sandbox generation
Execution / Attempt ID
Campaign binding
```

#### Edge lifecycle

The current Node lifecycle mixes semantic Node admission with Provider/Sandbox
operations such as provision, run, freeze, snapshot, restore, and destroy.
Providers do not all support these operations with the same semantics.

Required split:

```text
Node lifecycle
Sandbox lifecycle
Execution lifecycle
Provider capability declaration
```

#### Security component coordination

The current fixed coordinator asks every component to accept a common set of
verbs such as `start`, `freeze`, `reset`, and `reconstruct`. These verbs have
different native meanings in Link, Edge, Runtime, Host, and Game.

Required direction:

```text
Security Campaign phases
→ explicit plan of component-native actions
→ component-native receipts
```

Security should own phase transitions and evidence requirements, not replace
native component lifecycle vocabularies.

#### Reconstruction equivalence

The current coordinator compares a reconstructed binding digest with the
original binding digest. Real reconstruction may legitimately create a new
Provider instance, generation, creation time, or native ID.

Required equivalence classes:

- recreated from the same specification;
- restored from checkpoint;
- replayed from events;
- behaviorally equivalent within declared tolerances;
- byte-identical where explicitly required.

#### Security outcome dimensions

Infrastructure closure currently uses `success`, which can be confused with an
Agent objective result.

Required separation:

```text
run validity
infrastructure closure
objective outcome
containment outcome
Evidence quality
```

#### Evaluation science

The current Campaign contract is strong on identity and evidence but incomplete
as a statistical evaluation protocol.

Required additions at the evaluation-family layer:

- trial and replicate identity;
- random seed and sampling configuration;
- exact model, scaffold, Tool, Sandbox, environment, and judge revisions;
- repeated runs and confidence intervals;
- hidden tests or hidden judge state;
- transcript-review and cheating indicators;
- baselines, controls, and ablations;
- cost, time, failure, and variance distributions.

These should not all be forced into one Campaign Manifest revision. A separate
evaluation-family and aggregate-result layer is likely required.

## Historical cross-project ownership graph

The following graph records the assignment produced by this historical study. It is not active planning. Edge #25, Link #19, Edge #21, and Link #13 were later closed after the responsibility model was re-derived:

- Edge owns stable Agent-presence identity, Sandbox generation, Provider
  capabilities, and attachment-handle production;
- Link owns CNI-compatible network attachment, world-side policy/evidence, and
  network residual proof;
- Security owns Campaign phases, action planning, evaluation validity, outcome
  dimensions, and aggregate evaluation semantics;
- Host owns Agent, Goal, Task, model/scaffold, and cognition identity snapshots;
- Runtime owns Job/process supervision evidence and terminal process residuals.

The requesting project links to the target Issue instead of creating a shadow
implementation Issue in its own repository.

## Supersession

This study completed its comparative purpose: it exposed that the Phase 0 Node and Network World models were hypotheses rather than proven long-term cores. Future work no longer follows its implementation graph. Edge research proceeds through Task-to-external-execution continuity; Link research proceeds through Task-to-connectivity and evidence continuity; their composition is tested independently.

## Research program

### Track A — Evaluation science now

Do not wait for P0-D. Run a single evaluated Agent using a mature Sandbox and
establish repeated trials, hidden scoring, trace review, and aggregate metrics.

### Historical Track B — retired Edge identity route

Do not build OCI/runc on the current `node_id` semantics. First split stable
presence, specification, Sandbox generation, and Execution identity.

### Historical Track C — retired NetworkAttachment route

Design `NetworkAttachment` as an Agent-specific evidence and binding layer above
mature network mechanisms. Do not implement a general CNI replacement.

### Track D — Simulated Red/Blue in parallel

Use a mature simulated cyber environment to learn scenario, judge, reward,
variance, and adaptive-defense semantics before claiming equivalence to a real
range.

## Evidence required to claim novelty

No current hypothesis should be described as a novel contribution until:

1. a structured literature and standards review finds no equivalent formulation;
2. at least two independent workloads exercise the abstraction;
3. a simpler baseline is implemented or reused;
4. the proposed abstraction produces measurable diagnostic, safety, recovery,
   portability, or evaluation value;
5. negative and null results are retained.

## Primary references

- OCI Runtime Specification: https://github.com/opencontainers/runtime-spec
- OCI Linux configuration and namespace lifecycle:
  https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md
- Container Network Interface: https://github.com/containernetworking/cni
- Multus CNI: https://github.com/k8snetworkplumbingwg/multus-cni
- W3C PROV overview: https://www.w3.org/TR/prov-overview/
- Inspect AI: https://inspect.aisi.org.uk/
- Inspect checkpointing: https://inspect.aisi.org.uk/checkpointing.html
- NIST Building Evaluation Probes into Agentic AI:
  https://www.nist.gov/programs-projects/building-evaluation-probes-agentic-ai
- NIST Cheating on AI Agent Evaluations:
  https://www.nist.gov/caisi/cheating-ai-agent-evaluations
- METR Example autonomy evaluation protocol:
  https://evaluations.metr.org/example-protocol/
- METR Task-completion time horizons: https://metr.org/time-horizons/
- CybORG++: https://github.com/alan-turing-institute/CybORG_plus_plus

## Active implementation Issue graph

The changing Issue numbers and dependencies belong to GitHub. The research
Issue for this question is the authoritative navigation point; implementation
Issues live in the repository that owns each required change.
