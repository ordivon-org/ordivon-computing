---
schema_version: 1
id: computing.start
title: Ordivon Computing
type: start
profile: organization
lifecycle: active
source_role: canonical
visibility: public
owners:
  - ordivon-computing
audience:
  - builder
  - researcher
  - agent
updated: 2026-08-12
summary: "Canonical entry to Ordivon Computing: cross-project research, shared world-model revision, promoted contracts, conformance, and owner-preserving responsibility placement."
evidence_status: not_applicable
readiness: READY
applies_to:
  - ordivon-project-family
related:
  - computing.authority
---
# Ordivon Computing

A capable Agent is working on a real objective. Its model session disappears; one local command exits successfully; an external provider response is lost; a later Agent must continue; and the domain still has to decide what actually happened.

No transcript, process exit code, database, or Agent framework can truthfully own all of those facts.

**Ordivon Computing studies which responsibilities remain after strong models and mature classical systems are composed, then places each responsibility in the lowest owner that can actually prove and preserve it.** It owns cross-project research and the shared Ordivon world model. It does not own every project's current state or define an eternal Host → Harness → Runtime → World stack.

## Purpose

The question is not “what infrastructure can we put around a model?” It is:

> Which facts, commitments, and recovery boundaries must survive model, Provider, process, and interface replacement — and who can legitimately own each one?

A representative trajectory is:

```text
purpose / unresolved work
→ current owner-native evidence and Context
→ replaceable cognition proposes
→ consequence / execution authority where needed
→ classical execution or provider/domain action
→ owner-native Observation / Artifact / Receipt
→ reconciliation and verification
→ revised durable work or accepted outcome
```

A workload composes only the responsibilities it needs.

## One work item across current owners

- **Host** preserves durable semantic Task/work continuity when objective, frontier, commitments, uncertainty, or verification must survive Agent/session replacement. Persistence does not make Host the owner of Git, Runtime, or domain truth.
- **Harness** can preserve one bounded Agent Run's Provider/Tool/cognition structure when that structure is not already supplied sufficiently elsewhere. Harness Run completion is not Task completion.
- **Runtime** owns exact local Workspace/Job/Attempt/process/Artifact facts. Local execution success does not prove an uncontrolled external effect occurred.
- **World** provides narrow external bindings, cross-owner trajectories, and reconciliation when a residual responsibility remains between Host work and independently authoritative providers/domains. Native owners keep occurrence/current-state truth.
- **Finance, Security, Game, Human, and other domains** keep their own meaning and acceptance rules.
- **Computing** synthesizes only when the same residual responsibility survives materially different owners and simpler baselines.

Current repository boundaries are packaging that has survived today's evidence, not mandatory layers in every request.

## Current boundary

Computing owns:

- the compressed shared world model in [`core/`](core/);
- cross-project research questions, evidence, and portfolio state in [`research/`](research/);
- reusable explanations in [`knowledge/`](knowledge/);
- project-family identity/ownership navigation in [`projects/`](projects/);
- promoted cross-project protocol contracts and conformance evidence.

It does **not** own current owner implementation truth, live deployment state, a global database of project facts, or a universal Agent runtime/Memory/World/organization layer merely because those abstractions can be named.

When Computing prose and an exact current owner source disagree, **the owner wins**. Computing revises its synthesis.

## Why this is not one monolithic Agent framework

Several things that look like “Agent state” are different authorities:

```text
semantic work continuity       ≠ Provider/session continuation
Provider/session continuation  ≠ physical process truth
physical process truth         ≠ external occurrence truth
external occurrence truth      ≠ domain meaning
persistence                    ≠ ownership
capability                     ≠ authority
completion in one scope        ≠ completion in another
```

Collapsing them encourages predictable errors: transcript → Task truth, exit code → remote success, delivery receipt → knowledge, or derived projection → owner truth.

Ordivon therefore preserves **responsibilities rather than subsystem names**. Packages may merge, split, disappear, or be replaced when a stronger model or mature lower system carries the same invariant more cheaply.

## Three conceptual bands

1. **Flexible cognition and product policy** — models, Provider-native Agents, Skills, search, planning, retrieval, specialists, and domain judgment. This layer should change quickly.
2. **Thin durable responsibility boundaries** — only residual invariants that remain unowned: durable open-work identity when required, exact source/Context binding, consequence authority, effect uncertainty/reconciliation, evidence/verification, Tool-contract identity, and owner-native observation projection.
3. **Classical substrate and native domains** — operating systems, databases, Git, networks, durable workflows, hypervisors, model serving, cloud APIs, exchanges, browsers, sensors, and domain backends retain their native authority.

[`core/stack.md`](core/stack.md) owns the exact current formulation and deletion test.

## Operating objective

```text
verified improvement per unit time
while minimizing unrecoverable loss,
unnecessary interruption,
and permanent concentration of capability
```

A persistent constraint must create more recoverability, verification, understanding, or consequence reduction than the latency, friction, compatibility, cognitive compression, and control concentration it adds. Existing implementations receive no historical presumption of retention.

## World-model loop

```text
owner repositories / external worlds
→ observations, failures, counterexamples
→ Research
→ scoped reusable Knowledge
→ compact Core
→ new project experiments
└──────────────────────────────↺
```

Owner facts do not move into Computing as copied authority. Cross-project conclusions may revise the shared model, which then creates new falsifiable questions. See [`research/WORLD-MODEL-LOOP.md`](research/WORLD-MODEL-LOOP.md).

A proposed shared layer should survive four questions: **what recurring pressure exists; who owns it today; which simpler baseline fails; what second materially different workload needs the same invariant?** If deletion leaves nothing important unowned, keep it deleted or local.

## Current project family

Use [`projects/README.md`](projects/README.md) for Computing's bounded project-family packaging/history navigation, not as an exhaustive current semantic-owner registry. Resolve current owner identity, current display name, authority and currentness from the owner-native authority surface; use Atlas generated owner/current-recovery projections where covered. Historical packaging names such as Studio remain recoverable without overriding the current Media owner. Projects compose around responsibility boundaries rather than forming one compulsory stack.

## Start here

| Need | Read |
| --- | --- |
| compact shared world model | [`core/README.md`](core/README.md) |
| responsibility placement and deletion test | [`core/stack.md`](core/stack.md) |
| owner/proof/meaning distinctions | [`knowledge/agents/causal-responsibility-explanation.md`](knowledge/agents/causal-responsibility-explanation.md) |
| current Computing research state | [`research/PORTFOLIO.md`](research/PORTFOLIO.md) |
| research/world-model revision method | [`research/README.md`](research/README.md) and [`research/WORLD-MODEL-LOOP.md`](research/WORLD-MODEL-LOOP.md) |
| project owner / truth hierarchy | [`projects/README.md`](projects/README.md) |
| Computing document authority | [`docs/authority.md`](docs/authority.md) |

## Content engineering

[`docs/content-engineering/README.md`](docs/content-engineering/README.md) owns the shared document contract Computing actually promotes. Strict checks apply only to paths admitted by `.ordivon/project.yaml`; another repository's style/lint configuration is not automatically its semantic authority.

## Protocol and conformance

[`packages/ordivon-protocol/`](packages/ordivon-protocol/) contains selected promoted contracts with real consumers, not a universal ontology. The deterministic gate is:

```bash
python scripts/run_conformance_gate.py \
  --receipt /tmp/ordivon-conformance-receipt.json
```

The launcher owns the gate environment: it uses the repository-pinned Python 3.12.13 and `requirements-conformance.txt` instead of inheriting an ambient Python or dependency set.

Exact revisions and historical System Snapshots prove what was compared then; they never become floating declarations of current owner state.

## Coordination and state

Owner repositories/live systems own implementation and physical facts. Git owns revision/history. `research/portfolio.json` owns mutable Computing research-line state. Computing documents own only the stable theory, explanation, decision, or generated view assigned by [`docs/authority.md`](docs/authority.md).

When a conclusion stabilizes, the active tree should contract: compact explanation remains; exact derivation stays recoverable from Git/evidence; obsolete apparatus leaves the default path.
