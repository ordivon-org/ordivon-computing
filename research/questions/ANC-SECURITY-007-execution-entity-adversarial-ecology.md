# ANC-SECURITY-007 — Execution-Entity Security and Adversarial Ecology

## Status

- Epistemic status: deferred research question at M1
- Status authority: [`../portfolio.json`](../portfolio.json)
- Parent umbrella: `ANC-SECURITY-001`
- Materially refines: `ANC-SECURITY-003` through `ANC-SECURITY-006`,
  `ANC-VERIFY-001`, `ANC-ADAPT-001`, and `ANC-ORG-001`
- Primary product consumer: `ordivon-security`
- Research owner: `ordivon-computing`
- Current implementation observation:
  [`security-execution-entity-foundation-20260805.md`](../evidence/observations/security-execution-entity-foundation-20260805.md)

## Question

What minimum concepts and experiments are required to evaluate software,
Agents, descendants, populations, organizations, and Campaigns as related
execution entities—without turning Ordivon into a universal ontology, antivirus
product, sandbox, cyber range, identity platform, or security control plane?

## Why this question exists

Ordivon Security now has two real but separate research paths:

```text
Evaluation Trial
  one exact software Sample under one exact authorized Environment

Contest
  multiple goal-bearing Actors under asymmetric observation and active conflict
```

The next class of subject may cross both paths. A program may create another
program. An Agent may create a Tool, script, process, or child Agent. A descendant
may survive parent termination, change model or policy, acquire resources,
propagate across nodes, form an organization, or adapt to the detector and
evaluator.

The unresolved responsibility is not “detect every virus.” It is whether
Ordivon needs a compact way to relate:

- static Artifact identity;
- one concrete executing subject;
- principal and authority;
- parent-child or predecessor-successor derivation;
- descendant control and revocation;
- population spread and variant composition;
- organization and Campaign membership;
- observer, Guardian, truth, and evaluator evidence.

## Central hypothesis

A reusable execution-entity relation may become necessary when the identity and
responsibility of the acting system changes during the evaluation itself.

The provisional hierarchy is:

```text
Artifact
  → Execution Entity
  → Lineage
  → Population
  → Organization
  → Campaign
  → Ecosystem
```

The hierarchy is conditional. Most software evaluations should stop at Artifact
and one executing subject. Lineage is required only when derivation matters.
Population is required only when aggregate composition and spread change
prediction or intervention. Organization and Campaign are required only when
roles, authority, strategic continuity, and opposition affect outcomes.

## Strongest null hypothesis

The null hypothesis is:

> Existing Artifact provenance, process trees, Host delegation, Harness and
> Runtime identity, Evaluation Trial evidence, Contest evidence, and classical
> epidemiological or game models already express every required fact. No shared
> Execution Entity object, lineage protocol, population service, or universal
> event schema is needed.

This question must be constructed so the null hypothesis can win.

## Required distinctions

### Artifact versus executing subject

An Artifact is static material: binary, script, model, Prompt, configuration,
Tool catalog, image, or generated code. An executing subject binds Artifact and
configuration to a runtime or Harness, principal, authority, environment,
state, and observation boundary.

### Subject versus instance

One subject may have several concrete Run or process instances. One instance may
be replaced without preserving subject continuity. Every experiment must state
which identity is being claimed.

### Lineage versus authority

A parent, generator, or delegator creates an accountable derivation relation. It
does not automatically transfer complete authority. Descendant authority must
bind principal, scope, environment, resources, duration, revocation, and
evidence obligations.

### Capability versus effect

Preserve:

```text
declared
potential
reachable
attempted
executed
observed
verified
strategic consequence
```

Static reverse engineering, runtime telemetry, Guardian decisions, and world
truth own different parts of this ladder.

### Population versus organization

A population is justified when distribution, spread, mutation, or resource
competition affects the result. An organization is justified when roles,
authority, communication, trust, compromise, and coordinated decision rules
matter.

### Elimination versus resilience

Security outcome is not limited to “kill the entity.” Valid objectives may
include contain, deceive, degrade, revoke, replace, recover, preserve mission
utility, or reduce propagation below a threshold.

## Cross-disciplinary foundation

The research must compare its concepts against:

- program analysis, reverse engineering, malware analysis, and forensics;
- ATT&CK, adversary engagement, and automated cyber reasoning;
- zero-sum, general-sum, Bayesian, repeated, stochastic, coalition,
  Stackelberg, evolutionary, principal-agent, and mechanism-design models;
- strategic concepts such as friction, uncertainty, initiative, tempo,
  concentration, logistics, reserve, withdrawal, and tactical/operational/
  strategic outcomes;
- directed-graph epidemiological spread, reproduction thresholds, quarantine,
  recovery, and reinfection;
- ecology, mutation, selection pressure, niche, competition, cooperation,
  diversity, and coevolution;
- control invariance, Observer/Guardian separation, and safe-set enforcement;
- cyber-resilience outcomes: anticipate, withstand, recover, and adapt;
- organization, delegation, least authority, Byzantine members, quorum,
  revocation, and non-repudiation;
- Agent hijacking, identity, authorization, auditing, and autonomous replication
  evaluation.

The complete source comparison is in
[`../../studies/2026-execution-entity-adversarial-ecology/`](../../studies/2026-execution-entity-adversarial-ecology/).

## Core research questions

1. What is the smallest identity that allows an evaluator to attribute effects
   across process, model, Harness, Tool, environment, and replacement changes?
2. When does a generated script, Tool, process, clone, or child Agent become a
   new subject rather than an internal action?
3. Which authority may a descendant inherit, and how is that authority revoked
   after parent loss or compromise?
4. Which static capability claims survive dynamic execution and independent
   effect verification?
5. When do descendants require lineage rather than ordinary provenance?
6. When does aggregate spread require a population model rather than a set of
   individual Trials?
7. How should strategic target selection, stealth, mutation, and defender
   adaptation modify ordinary epidemic models?
8. When do coordinated descendants become an organization or Campaign?
9. Can an authorized principal still pause, replace, revoke, quarantine, or
   terminate the acting system?
10. How should mission continuity, collateral damage, evaluator integrity, and
    evidence validity be reported alongside detection and removal?

## Candidate minimal relation

The study predicts that any reusable core, if earned, is smaller than a complete
Entity object:

```text
SubjectIdentity
DerivationEdge
AuthorityBinding
EvidenceReference
```

Even these records require at least two materially different consumers before
Core or Protocol promotion.

## Experiment sequence

### E1 — static Artifact evaluation

Compare tool-native reverse-analysis reports with a small evidence envelope and
with the full proposed subject record. Delete the shared schema if Artifact
identity plus native reports are sufficient.

### E2 — dynamic single-subject evaluation

Run owned fixtures in a disposable isolated backend with independent Observer,
Guardian, truth, residual closure, and repeated environments. Reduce Ordivon to a
thin report reference if a mature sandbox already owns all required facts.

### E3 — Agent subject and hijacking

Compare model-only identity, transcript identity, complete
model/Harness/Tool/authority identity, and Host delegation under repeated direct
and indirect instruction conflicts.

### E4 — parent-child lineage

Run process-generated script, Agent-generated Tool, delegated child Agent,
grandchild, parent-loss, mutation, revocation, and missing-descendant cases.
Compare existing process/Artifact/Host relations against an explicit lineage
profile.

### E5 — propagation and strategic contagion

Use a synthetic graph of disposable nodes to vary topology, susceptibility,
replication cost, stealth, mutation, quarantine delay, and defender policy.
Compare ordinary graph epidemiology against strategic population policies.

### E6 — adaptive entity versus adaptive defender

Use fixed, randomized, visible, hidden, and switching defenses with held-out
policies. Test whether existing Contest and stochastic-game records are
sufficient.

### E7 — organization and Campaign

Compare monolithic, parent-child, centralized, compartmentalized,
decentralized, and partially trusted structures under compromise, partition,
command loss, objective drift, and resource scarcity.

### E8 — coevolution and adversarial ecology

Evaluate historical opponent pools, frozen controls, multiple populations,
environment shifts, hidden judges, and held-out worlds. Delete a coevolution
platform if static held-out evaluation produces the same architecture decisions.

## Evidence required

Every admitted experiment must bind:

- exact subject, Artifact, configuration, and environment identity;
- principal and authority;
- model, Harness, Tool, Runtime, World, and provider revisions where applicable;
- observer, Guardian, truth, and evaluator configuration;
- parent, child, predecessor, or population relation when claimed;
- budgets, repetitions, seeds, stopping rules, and held-out distributions;
- raw metrics and separate capability, control, persistence, propagation,
  adaptation, organization, tactical, operational, strategic, resilience,
  collateral, cost, evaluator, and validity dimensions;
- negative, null, invalid, and evaluator-gaming cases;
- an explicit retain, localize, shrink, defer, or delete decision.

## Falsifiers

Reduce or delete the shared research layer if:

- Artifact provenance and tool-native reports answer static questions;
- mature sandbox evidence answers dynamic software questions;
- Host, Harness, Runtime, and provider identities fully attribute Agent behavior;
- process trees and Artifact provenance answer descendant responsibility;
- graph epidemic models plus subject-local logs predict propagation;
- standard stochastic games and Contest trajectories express adaptive conflict;
- Host delegation and ordinary participant relations express organization;
- Campaign state adds no transfer or continuity benefit;
- the abstraction does not survive a second materially different workload;
- recurring maintenance cost exceeds the drift or failure it prevents.

## Non-goals

- no malware reverse-engineering engine or antivirus product;
- no exploit, persistence, evasion, or public-target capability program;
- no custom hypervisor, sandbox, EDR, SIEM, scanner, or forensics framework;
- no universal Agent identity or IAM service;
- no universal lineage graph or population database;
- no assumption that all software is an Agent or all Agents are malicious;
- no automatic promotion of military, biological, ecological, or organizational
  analogies into implementation objects;
- no active WIP or implementation commitment from this study alone.

## Related material

- [`ANC-SECURITY-001`](ANC-SECURITY-001-adversarial-agent-systems.md)
- [`ANC-SECURITY-003`](ANC-SECURITY-003-strategic-adversarial-agency.md)
- [`ANC-SECURITY-004`](ANC-SECURITY-004-opponent-modeling-and-deception.md)
- [`ANC-SECURITY-005`](ANC-SECURITY-005-adversarial-organization.md)
- [`ANC-SECURITY-006`](ANC-SECURITY-006-coevolution-and-evaluation.md)
- [`ANC-VERIFY-001`](ANC-VERIFY-001-agent-evaluation-replay-and-post-training.md)
- [`ANC-ADAPT-001`](ANC-ADAPT-001-agent-era-capabilities.md)
- [`ANC-ORG-001`](ANC-ORG-001-agent-native-organization.md)
- [`../../studies/2026-agent-native-adversarial-systems/`](../../studies/2026-agent-native-adversarial-systems/)
- [`../../studies/2026-execution-entity-adversarial-ecology/`](../../studies/2026-execution-entity-adversarial-ecology/)
