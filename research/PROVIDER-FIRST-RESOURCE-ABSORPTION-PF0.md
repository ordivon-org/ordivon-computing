# Provider-First Resource Absorption — PF0

Status: research synthesis — 2026-08-14

## Thesis

The public world is not only a source of ideas. Mature software, protocols, APIs, datasets, models, skills, engines, services, and tools are **resources** that an Agent can discover, qualify, acquire, bind, consume, compare, replace, and retire.

This extends the accepted `Agent-first Infrastructure Promotion Rule` from an engineering preference into an operational resource model:

```text
need
→ discover the public capability world
→ qualify candidate owners
→ acquire through a mature acquisition owner
→ bind the smallest semantic capability
→ dogfood against the real consumer
→ compare providers and measure residual gaps
→ delegate mature mechanism
→ delete displaced mechanism
→ innovate only on stable residual responsibility
```

The scarce resource is therefore not code. It is correct selection, authority, evidence, composition, evaluation, and learning.

## Relation to the accepted promotion rule

`projects/decisions/agent-first-infrastructure-promotion.md` already establishes that mature infrastructure and provider-native APIs come first, thin Agent-facing adapters come second, and new Ordivon semantic ownership requires repeated evidence.

PF0 adds the missing **resource lifecycle** and the explicit distinction between:

- a public capability that merely exists;
- an acquirable software artifact;
- materialized bytes or a reachable service;
- an admitted provider binding;
- a provider that actually worked for the consumer;
- a provider preferred only after comparison.

This avoids two opposite failures:

1. `build-first`: reimplementing mature mechanisms because they are technically implementable;
2. `dependency-first`: installing or adopting popular tools before proving they reduce total ownership.

## Resource lifecycle

```text
DISCOVERED
    ↓
INDEXED
    ↓
QUALIFIED
    ↓
ACQUIRABLE
    ↓
MATERIALIZED
    ↓
ADMITTED
    ↓
PROVEN
    ↓
PREFERRED
```

### DISCOVERED

The resource is known to exist. This is search knowledge, not authority.

### INDEXED

Stable candidate identity, capability claims, source owner, license/access class, and navigation are recorded. Indexing proves no availability or fitness.

### QUALIFIED

Owner-native documentation, current maintenance, interface shape, authority requirements, failure semantics, and relevant constraints have been checked closely enough to justify acquisition or a bounded live probe.

### ACQUIRABLE

A current mature acquisition path exists for the exact resource class. Examples include signed system packages, `mise` backends, `uvx`, immutable OCI images, provider-native installers, or hosted APIs.

### MATERIALIZED

Exact local bytes, environment, image digest, or service identity are present. Materialization is not consumer success.

### ADMITTED

An Ordivon owner has explicitly bound the provider to a semantic capability with exact authority/currentness/evidence rules. Provider internals are not promoted into domain semantics.

### PROVEN

A real consumer outcome succeeded through the admitted binding. Provider self-health is insufficient.

### PREFERRED

The provider is the current default only after bounded comparison against realistic alternatives on outcome, friction, evidence, failure semantics, cost, and displacement potential.

`PREFERRED` is revocable. No provider becomes architecture by popularity.

## EquipmentCandidate

Software resources should be represented above source-specific package managers:

```text
EquipmentCandidate
  candidateId
  capabilityClaims[]
  sourceOwner
  sourceClass
  sourceAuthority
  versionOrRevision
  licenseAndAccess
  acquisitionCandidates[]
  agentSurface
  isolationRequirements
  maintenanceFacts
  acquisitionCostFacts
  qualificationEvidence[]
  lifecycleState
```

`sourceClass` may be a distro package, npm package, Python package, release binary, OCI image, provider-native application, hosted API, model, dataset, skill catalog, or another explicit class.

This is discovery/evaluation state. It does not install anything.

## EquipmentBinding

A binding records one exact admitted materialization or service relation:

```text
EquipmentBinding
  bindingId
  candidateId
  capabilityId
  acquisitionProvider
  materializationIdentity
  authorityDigest
  generationOrVersion
  executionOrEndpointShape
  isolation
  evidenceDigest
  observedAt
  maxEvidenceAge
  consumerProofs[]
  providerRef
```

Domain consumers bind `capabilityId` plus exact evidence. They should not know npm store paths, container layer details, VM process IDs, Surfshark endpoints, browser cache directories, or other provider-specific mechanics unless those facts are themselves the research subject.

## Acquisition is also provider-owned

PF0 rejects a universal Ordivon installer.

Current evidence shows the better composition:

| Resource class | Preferred acquisition owner | Ordivon role |
|---|---|---|
| Arch/system package | existing signed `isolated_equipment` / pacman authority | bind package closure evidence |
| Release CLI / multi-ecosystem developer tool | dormant `mise` backend, especially aqua/GitHub where provenance is available | exact request + evidence projection |
| Ephemeral Python CLI | `uvx` | bind exact package/version and process result |
| Node CLI | `mise npm` or bounded pnpm execution | record package/version/acquisition cost |
| OCI appliance | container runtime + immutable image digest, only when a container runtime is an admitted substrate | bind image/service identity |
| Complex reproducible environment | Nix when closure reproducibility justifies its cost | bind closure/revision evidence |
| Hosted capability | provider-native API/CLI | bind endpoint/account/capability authority without copying service state machine |

Acquisition evidence and runtime capability evidence are distinct. Successful installation does not prove useful operation.

### Local `mise` proof

The current Workstation already contains `mise` in the desired dormant form:

- no active global configuration;
- no shell activation;
- no `MISE_*` / `ASDF_*` environment ownership;
- materialized tools remain inactive by default;
- explicit `mise --no-config --no-env --no-hooks x ...` successfully executed both npm and cargo-backed tools;
- the complete ambient environment digest was identical before and after execution.

Therefore `mise` is currently a strong **Software Acquisition Provider**, not an ambient environment manager.

Backend-specific supply-chain evidence remains explicit; a `mise` binding does not by itself imply signature, checksum, attestation, or provenance strength.

## Classification law

For every existing Ordivon mechanism, classify responsibility rather than code size.

### DELETE

A mature provider completely owns the mechanism and Ordivon has no residual semantic responsibility.

### DELEGATE

A mature provider owns the mechanism, while Ordivon retains only capability binding, policy, evidence, or composition semantics.

### RETAIN

The responsibility survives every plausible provider substitution and belongs to the current Ordivon owner.

### INNOVATE

The responsibility is both valuable and not adequately owned by the mature public ecosystem. This is the scarce area where custom engineering should expand.

Do not mechanically delete historical experiment apparatus. Research may establish an invariant even when its mechanism is later delegated.

## Cross-project PF0 audit

### Workstation — strongest contraction target

Observed current network/provider surface contains approximately 6.3k LOC across fifteen selected scripts and currently owns several mature specialist mechanism domains simultaneously.

**Delegate/delete mechanism:** provider-specific VPN lifecycle, low-level resolver implementation, generic CONNECT relay, route/isolation plumbing, provider-native health/restart machinery.

**Retain:** semantic egress capability, currentness/generation binding, exact authority, independent consumer proof, topology/failure-domain composition, explicit fallback, provider-neutral profiles.

**Innovate:** resource discovery and capability-universe reasoning.

The current small Clash/Mihomo adapter is the reference failure shape: provider unavailable produced exact unavailable evidence without enabling TUN/system proxy/global capture or trying to become the provider.

### Web — inherit before expanding

Web should own Web semantics and encounter evidence, not browser/crawler infrastructure.

The existing Playwright 1.62 CLI plus already-provisioned Chromium was dogfooded successfully after only provider-native configuration and the existing short-TMP compatibility binding. It produced named sessions, machine-readable session state, accessibility refs, page evaluation, network surface, screenshots, and clean session teardown.

**P0:** existing Playwright CLI as Agent Browser Equipment.

**P1 when demanded by real workloads:** dedicated browser appliance, crawl queue/retry provider, model-assisted interaction provider.

**Retain:** source/provenance binding, rendered encounter evidence, accessibility/interaction evidence, and the thin Runtime↔Chromium physical compatibility binding.

### Studio — already substantially provider-first

Studio already consumes FFmpeg/ffprobe, ImageMagick, Typst, Blender, Godot, Resolve, OBS, Figma, Remotion, and OpenTimelineIO-related capabilities rather than recreating full media engines.

**Retain/innovate:** production semantics, claims/assets provenance, technical QC and perception evidence, medium-aware creative research, review/evaluation, cross-medium production contracts.

**Delegate:** media codecs/render engines, NLE internals, live-production scene graph, generic timeline interchange, generic image/vector/3D/runtime mechanics.

Provider-first consequence: unify acquisition/binding evidence rather than adding another Studio-local equipment installer.

Candidate priorities:

- OpenTimelineIO remains the preferred timeline interchange owner;
- OBS integration should use its owner-native WebSocket protocol when machine control becomes worthwhile;
- Resolve remains an external professional NLE provider behind a narrow adapter rather than a Studio-owned editing engine.

### Security — preserve adversarial semantics, attack VM mechanism ownership

Security's charter already says it does not own hypervisor, scanner, EDR/SIEM, database, network-emulator, or vulnerability-database state machines.

The largest current mechanism pressure is the Windows KVM apparatus: QEMU lifecycle, VM/image construction, virtual networking/fabric, snapshots/recovery, and orchestration are represented by thousands of lines of current or historical provider/acceptance code.

**Retain/innovate:** adversarial authority, partial-information/epistemic semantics, contest/scenario semantics, consequence reconstruction, independent evidence, ambiguity, evaluator integrity, recovery experiments.

**Delegate candidate:** generic VM lifecycle/network/storage/snapshot mechanics to libvirt where it can satisfy the exact experiment boundary.

**Delegate candidate:** reproducible QEMU/KVM image construction to Packer QEMU builder where it displaces custom image-build procedure without weakening immutable-source/evidence requirements.

Acceptance scripts that encode past fault experiments are historical apparatus; they are not deletion targets merely because the future physical provider changes.

### Game — core product semantics stay local

Station Zero's deterministic World, simultaneous Turn authority, Faction Knowledge, action admission, replay, persistence, and domain scoring define the product/research subject. Public simulation frameworks must not become a second World authority.

**Retain/innovate:** exact Station Zero state transition, hidden knowledge, Planning/Commit semantics, simultaneous consequence resolution, replay/evidence, scenario content, product experience.

**External benchmark equipment:**

- PettingZoo for standard multi-agent environment interoperability and MARL tooling; its Parallel API is particularly relevant to simultaneous-action comparisons;
- OpenSpiel for game-theoretic/search/RL algorithm baselines and established game/evaluation suites.

Do not add either dependency merely for naming symmetry. First prove an external evaluation or learning workload that benefits from the adapter.

### Finance — governance is local; trading machinery must be attacked by mature baselines

Finance currently has a large explicit capability/evidence/governance surface. Its capital mandate, belief/thesis/decision state, proposal/admission, owner authority, reservations, external-effect identity, and reconciliation evidence are domain responsibilities and must not be outsourced to a trading framework.

The current direct OKX executor transport is relatively narrow compared with the wider Finance authority layer. Provider-first therefore should not replace it merely to use a popular exchange SDK.

The stronger challenge is to custom research/backtest/data/execution-model infrastructure.

**PF1 benchmark candidate: NautilusTrader.** Its documented architecture already owns data routing, portfolio/cache, risk, order lifecycle, execution reports, backtest/sandbox/live common-core machinery, and live reconciliation. Use it first as external research/simulation/execution-model equipment and a falsifier of Finance-specific mechanisms.

**Retain:** capital governance, effect admission, exact owner authority, financial semantic state, world/basis binding, independent reconciliation evidence and final capital consequences.

No provider-first experiment authorizes live capital effects.

### Computing — mother project for the law, not a global software controller

Computing should own the research model and cross-project falsification method:

- lifecycle semantics;
- candidate/binding definitions while experimental;
- qualification dimensions;
- cross-project responsibility audits;
- deletion/delegation evidence;
- reusable experimental fixtures where a true cross-project semantic responsibility emerges.

Computing must **not** become a package manager, tool marketplace, central runtime controller, or mutable registry of every installed binary.

Owner-local inventories and provider-native state remain authoritative. Computing records the world model and promoted contracts only when repeated evidence justifies them.

## Provider qualification vector

Every candidate should be compared on a bounded vector rather than star count:

```text
authorityFit
agentSurface
ownerNativeEvidence
currentnessObservability
failureSemantics
isolationScope
consumerProofability
acquisitionCost
steadyStateCost
supplyChainEvidence
maintenanceMaturity
licenseAccess
mechanismDisplacement
adapterThickness
providerSubstitutability
reversibility
```

A provider with more features can score worse when it adds a control plane, account dependency, global side effects, opaque state, or large acquisition cost.

## Public-resource search as a persistent loop

Provider discovery should become a normal precondition for new mechanism work:

```text
new need
→ search current public owner landscape
→ inspect primary documentation and current release state
→ compare against local installed equipment
→ prefer already-present capable equipment
→ acquire only bounded missing candidates
→ dogfood before architecture
```

This is a resource-harvesting loop, not dependency accumulation.

A mature public resource that fails qualification is still useful evidence: it narrows the residual problem that Ordivon actually needs to solve.

## PF1 queue

1. **Finance / NautilusTrader:** bounded acquisition + minimal deterministic backtest/data/reconciliation comparison; no credentials and no live effect.
2. **Security / libvirt + Packer:** audit local availability and compare current Windows KVM mechanism responsibility to provider-native lifecycle/image primitives before installing anything.
3. **Game / PettingZoo + OpenSpiel:** no dependency adoption yet; design one external benchmark question first, then materialize only the provider needed to answer it.
4. **Studio / OTIO + OBS:** keep current OTIO/Resolve path; only admit OBS WebSocket when a concrete live-production task requires it.
5. **Workstation:** resume Gluetun/sing-box displacement only after an admitted appliance acquisition substrate exists; do not build another container layer merely to test a provider.

## Stop conditions

Provider-First itself should be rejected or narrowed if repeated trials show that:

- adapter and qualification overhead exceeds the mechanism it replaces;
- external mutable state makes evidence materially weaker;
- provider churn creates more migration work than custom stable mechanism;
- provider semantics force domain authority leakage;
- custom code remains substantially smaller and better evidenced after realistic comparison.

The principle is not "always use dependencies." The principle is **make mechanism ownership earn its existence against the best public owner currently available**.
