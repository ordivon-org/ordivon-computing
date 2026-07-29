# Ordivon Computing

**Researching and constructing the persistent coordination and world-participation substrate for plural intelligence.**

中文：Ordivon 的智能体原生计算研究、协议、参考实验与跨项目验证母项目。

## What this repository is

Ordivon Computing studies the complete computing world, but it does not treat that world as an implementation roadmap. Mature operating systems, databases, networks, version-control systems, compilers, isolation mechanisms, model runtimes, and durable workflow engines remain the classical substrate.

The repository focuses construction where probabilistic cognition creates an unowned persistent responsibility:

```text
participant purpose and commitments
→ persistent open work
→ version-bound context
→ open cognitive proposal
→ capability and consequence binding
→ classical execution
→ Observation and Artifact evidence
→ Verification, revised work, negotiation, or responsible decision
```

A participant is a system role with an identity, commitments, resource relationships, and consequence exposure. The term does not assume consciousness or legal personhood. In current deployments, people and organizations usually remain the legal and physical owners of credentials, machines, money, and external commitments. Ordivon records that operational reality without turning it into a permanent axiom that every future artificial intelligence must remain property or lack independent purpose.

Its role is research synthesis, specification, reference experiments, protocol promotion, conformance, and evidence—not ownership of every product implementation or lower computing layer.

## Operating objective

Ordivon optimizes for:

```text
verified improvement per unit time
while minimizing unrecoverable loss,
unnecessary interruption,
and permanent concentration of capability
```

Capability and consequence are separate dimensions. Reversible, isolated, and privately owned exploration should be cheap and broadly available. Shared, durable, or irreversible world changes require explicit commitment, authority, evidence, and responsibility appropriate to their consequences.

A constraint earns a permanent place only when the recoverability, verification, or consequence reduction it creates is greater than its latency, operating friction, cognitive compression, compatibility cost, and concentration of control.

## Knowledge-generation system

```text
real workloads, primary sources, failures, and observations
                    ↓
                 Studies
                    ↓ distill
                Knowledge
                    ↓ compress
                   Core
                    ↓ generate falsifiable questions
                 Research
                    ↓ construct and test
                 Projects
                    └────────→ new evidence
```

| Area | Role | Entry point |
|---|---|---|
| **Core** | Minimal current theory and responsibility boundaries | [`core/`](core/) |
| **Knowledge** | Reusable explanations, comparisons, and cases | [`knowledge/`](knowledge/) |
| **Studies** | Preserved derivations and source-grounded learning paths | [`studies/`](studies/) |
| **Research** | Questions, competing hypotheses, experiments, and immutable evidence | [`research/`](research/) |
| **Projects** | Real systems through which ideas are constructed and tested | [`projects/`](projects/) |

Three studies are especially important:

- [`studies/2026-computing-stack-walkthrough/`](studies/2026-computing-stack-walkthrough/) — the complete physical-to-institutional computing route;
- [`studies/2026-classical-to-agent-native-computing/`](studies/2026-classical-to-agent-native-computing/) — the strict derivation of what remains classical, what Agents merely amplify, and what responsibilities are genuinely rewritten or new;
- [`studies/2026-adaptive-acceleration/`](studies/2026-adaptive-acceleration/) — the historical and cross-disciplinary argument for accelerating capability together with adoption, verification, defense, recovery, distribution, and cooperative intelligence rather than relying on a global frontier slowdown.

## Core thesis

Foundation models provide useful probabilistic proposals under selected context. They do not automatically provide durable work state, current capability, external observations, verified facts, accepted commitments, or responsibility for consequences.

Ordivon therefore studies and constructs a hybrid participation boundary:

```text
replaceable probabilistic cognition
inside
persistent identity, work, commitment, evidence, and recovery
above
classical execution, storage, networking, isolation, and model serving
```

The compact Core is:

- [`core/foundations.md`](core/foundations.md) — working foundations;
- [`core/stack.md`](core/stack.md) — inherited substrate and Agent-native responsibility overlay;
- [`core/primitives.md`](core/primitives.md) — backend objects, executable semantic primitives, promoted protocol objects, Host-proven work objects, and explicit research candidates.

## Research discipline

A proposed Agent-native layer or persistent constraint must answer:

```text
Which mature lower mechanism is insufficient?
What exact invariant remains unowned?
What realistic trajectory fails if it is bypassed?
What second workload demonstrates the same responsibility?
Why is a new shared component better than a local policy or adapter?
Does the mechanism increase verified improvement or reduce unrecoverable loss
by more than it adds latency, friction, cognitive compression, and control concentration?
```

Research interest does not imply implementation. A concept moves toward Core only after primary-source comparison, executable evidence, counterexamples, cost measurement, and deletion tests.

## Current questions

- [`ANC-STACK-001`](research/questions/ANC-STACK-001-classical-to-agent-native-transition.md) — classical substrate versus Agent-native responsibility;
- [`ANC-IR-001`](research/questions/ANC-IR-001-agent-effect-ir.md) — minimum useful Agent Effect IR;
- [`ANC-MEMORY-001`](research/questions/ANC-MEMORY-001-task-continuity.md) — minimum durable state for open-work continuity;
- [`ANC-EFFECT-001`](research/questions/ANC-EFFECT-001-tool-contract-evolution.md) — Tool-contract change and rebinding;
- [`ANC-ORG-001`](research/questions/ANC-ORG-001-agent-native-organization.md) — plural participants coordinating around persistent work and commitments;
- [`ANC-ADAPT-001`](research/questions/ANC-ADAPT-001-agent-era-capabilities.md) — evidence-driven adaptation and self-improvement;
- [`ANC-SECURITY-001`](research/questions/ANC-SECURITY-001-adversarial-agent-systems.md) — maximum internal Agent capability under independently bounded external consequence;
- [`ANC-EDGE-001`](research/questions/ANC-EDGE-001-task-placement-and-external-continuity.md) — Task placement and external execution continuity;
- [`ANC-LINK-001`](research/questions/ANC-LINK-001-task-connectivity-and-evidence-continuity.md) — Task connectivity and path-conditioned evidence continuity;
- [`ANC-WORLD-001`](research/questions/ANC-WORLD-001-edge-link-world-interface-composition.md) — Edge/Link World-Interface composition.

See [`research/map.yaml`](research/map.yaml).

## Project roles

- **Ordivon Host** — persistent Goal and Task continuity, context compilation, open proposal lowering, cognition coordination, participant decision routing, Effect coordination, verification, and recovery;
- **Ordivon Runtime** — trusted-local Workspace, Job, Attempt, Artifact, physical dispatch, cancellation, reconciliation, and recovery;
- **Ordivon Link** — Task-to-connectivity research overlay above mature networking, with path observations, controlled egress, evidence continuity, and Network World experiments;
- **Ordivon Edge** — Task-to-external-execution research overlay above mature providers, with Cloudflare Fetch/Browser, receipts, Artifacts, and body-continuity experiments;
- **Ordivon Game** — deterministic world, multi-participant coordination, replay, evaluation, and interaction laboratory;
- **Ordivon Security** — maximum-capability Campaigns with independently bounded consequence, observation, judging, evidence, and reconstruction;
- **Ordivon Web** — public memory, publication, project navigation, and current evidence surfaces.

The exact stable declarations live in [`projects/registry.yaml`](projects/registry.yaml). Product maturity remains in each product repository.

## Protocol and conformance

[`packages/ordivon-protocol/`](packages/ordivon-protocol/) is the production-candidate source for selected cross-boundary contracts. It is not a universal internal ontology. Direct consumption and conformance must be demonstrated mechanically rather than inferred from similar terminology.

The deterministic gate is:

```bash
python3.12 scripts/ordivon_conformance.py gate \
  --receipt /tmp/ordivon-conformance-receipt.json
```

It validates protocol, experiments, evidence, project identity, cross-language canonical vectors, and foundational-document integrity.

## Executable Semantic Core

[`research/experiments/semantic-core-v0/`](research/experiments/semantic-core-v0/) is a closed reference experiment at the semantic commitment boundary:

```text
probabilistic proposal
→ role-scoped Effect admission
→ concrete Dispatch through a backend
→ Observation and Artifact evidence
→ Verification
→ bounded Fact admission
```

It preserves identity, explicit uncertainty, evidence provenance, authority, and replay while delegating byte durability, processes, files, and transport to classical systems. It is retained as reference evidence, not as a mandate that every historical experimental compatibility path remain active forever. [`research/experiments/external-semantic-contract-v0/`](research/experiments/external-semantic-contract-v0/) separately tests public Effect, ToolContract, and EffectBinding boundaries.

## Coordination and state

Documents preserve stable theory, contracts, sources, and reproducible evidence. GitHub Issues own changing task state and dependencies. Git commits own code revision and historical recovery. Immutable [`System Snapshots`](research/evidence/) bind exact historical repository and Artifact combinations without becoming a second mutable deployment registry.
