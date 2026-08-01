# G7 — Governance and Dependency Graphs

Status: completed as a research-local projection of G3-G6 evidence

Machine graphs:

- `research/data/ai-capability-governance/graphs/governance-graph.json`
- `research/data/ai-capability-governance/graphs/dependency-graph.json`

Supporting indexes:

- `research/data/ai-capability-governance/provider-cases/index.json`
- `research/data/ai-capability-governance/institutions/index.json`

## Why two graphs are required

A single graph would collapse two different questions.

### Governance graph

```text
Who can decide what about whom, under which rule and review?
```

It records normative, observational, enforcement, adjudicative,
infrastructural, and epistemic relations.

### Dependency graph

```text
Who cannot continue without which resource, and at what switching cost?
```

It records account, inference, cloud, hardware, identity, weights, Task-state,
Tool-authority, and Provider-trust dependencies.

A Provider can have strong dependency power without frequently refusing requests.
A regulator can have formal authority but weak implementation visibility. A
self-hosted deployer can possess weights while remaining dependent on hardware,
cloud, licensing, and upstream updates.

## Governance graph result

```text
Nodes  23
Edges  35
```

The graph includes:

- seven Provider or upstream-model actors;
- four jurisdictional governance actors;
- the cloud/compute layer;
- hosted users, local deployers, and Ordivon Host;
- inference, weights, accounts, data, eligibility, Tool authority, appeal, and
  durable Task-state resources.

### Strongly evidenced patterns

#### Hosted Providers combine multiple powers

For each hosted Provider, current public evidence supports some combination of:

```text
defines hosted capability
observes or processes request/account data
restricts account or service access
operates first-instance support or appeal
```

The exact thresholds and implementation detail vary and remain Provider-specific.

#### Open weights redistribute rather than erase authority

Meta licenses Llama 4 weights under private terms while the local deployer gains
runtime and Tool control. Normative power remains upstream; execution power moves
downstream.

#### Public law adds counter-power and administrative power simultaneously

EU, US, China, and Canada nodes regulate capability through materially different
combinations of documentation, filing, procurement, infrastructure, content,
privacy, national-security, and review mechanisms.

#### Ordivon separates cognition supply from Effect authority

G6/R6 evidence supports two narrow Ordivon relations:

```text
Ordivon Host owns durable caller/Task state
Ordivon Host constrains Tool and external Effect authority
```

This is not a claim that Ordivon owns or controls Provider cognition.

## Dependency graph result

```text
Nodes  14
Edges  13
```

### Hosted path

```text
user / Host
→ Provider account and access tier
→ hosted inference
→ cloud and accelerator capacity
→ identity, billing, sanctions and region eligibility
```

Switching Providers can lose model quality, account trust, approved access,
billing relationships, cached state, Tool semantics, and product integration.

### Ordivon path

```text
Provider supplies current cognition
Host retains Task, Context compilation, Tool contract, trace and completion state
Runtime / World evidence remains outside Provider conclusion text
```

G6's DeepSeek compatibility pilot shows that caller-owned history can preserve a
small benign two-turn Task across API serialization surfaces. It does not prove
cross-Provider semantic or capability equivalence.

### Licensed open-weight path

```text
local deployer
→ upstream weights and license
→ local/cloud compute
→ accelerator and memory supply
→ local Host and Tool authority
```

Inference continuity improves after lawful download, but compute and supply-chain
dependence remains capability-dependent.

## No scalar index

G7 deliberately does not calculate:

```text
Provider Power Score
Freedom Score
Censorship Score
Safety Score
User Risk Score
```

Such scores would require contested weights, comparable denominators, and behavior
evidence that G3-G6 do not possess. They would hide whether the relevant power is
request filtering, account sanction, retention, geography, compute, license,
Tool authority, or switching cost.

## Evidence confidence

### High confidence

- published policy and license relations;
- publicly disclosed monitoring/retention mechanisms;
- public-law duties and administrative systems;
- R6 Host/Runtime/World/Verifier relations;
- G6 DeepSeek surface portability in the tested configuration.

### Medium confidence

- practical strength of appeal and review;
- switching cost categories;
- relative importance of each dependency for different users;
- how policy text maps to undisclosed technical classifiers.

### Not established

- Provider-wide false-positive rates;
- comparative refusal or misuse-prevention effectiveness;
- universal cross-Provider portability;
- intent, capture, or political motivation;
- optimal constitutional or regulatory system.

## G7 disposition

Retain the graphs as **research-local evidence projections**. They may support the
later full review, identify missing observations, and prevent category collapse.
They do not justify G8 architecture changes.

Specifically:

- no graph service;
- no graph database requirement;
- no Protocol object;
- no Provider reputation subsystem;
- no Runtime dependency on governance metadata;
- no automatic policy or access decision.

Regenerate or delete the graphs if future cases make the current vocabulary
misleading. Markdown and JSON remain sufficient for the present study.

## End of execution sequence

The requested execution sequence ends here:

```text
G0-G2  scope, evidence, theory and grammar
G3     OpenAI / Anthropic deep cases
G4     comparative Provider ecology
G5     state, regulatory, compute and cloud interaction
G6     controlled empirical audit
G7     governance and dependency graphs
G8     intentionally omitted
```

The next activity is a complete review of findings, contradictions, evidence
quality, overreach, omissions, and whether the study should remain active,
completed, frozen, split, or partially deleted.
