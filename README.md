# Ordivon Computing

**Researching and constructing the semantic control layer between probabilistic cognition and classical computing.**

中文：Ordivon 的智能体原生计算研究、协议、参考实验与跨项目验证母项目。

## What this repository is

Ordivon Computing studies the complete computing world, but it does not treat that world as an implementation roadmap. Mature operating systems, databases, networks, version-control systems, compilers, isolation mechanisms, model runtimes, and durable workflow engines remain the classical substrate.

The repository focuses construction where probabilistic model cognition creates an unowned system responsibility:

```text
human purpose
→ persistent open work
→ version-bound context
→ probabilistic proposal
→ authority and Effect admission
→ classical execution
→ Observation and Artifact evidence
→ Verification, revised work, or human decision
```

Its role is research synthesis, specification, reference experiments, protocol promotion, conformance, and evidence—not ownership of every product implementation or lower computing layer.

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

Two studies are especially important:

- [`studies/2026-computing-stack-walkthrough/`](studies/2026-computing-stack-walkthrough/) — the complete physical-to-institutional computing route;
- [`studies/2026-classical-to-agent-native-computing/`](studies/2026-classical-to-agent-native-computing/) — the strict derivation of what remains classical, what Agents merely amplify, and what responsibilities are genuinely rewritten or new.

## Core thesis

Foundation models provide useful probabilistic proposals under selected context. They do not automatically provide durable work state, current authority, external observations, verified facts, or responsibility for consequences.

Ordivon therefore studies and constructs a hybrid boundary:

```text
probabilistic cognition
inside
persistent deterministic identity, authority, commitment, and evidence
above
classical execution, storage, networking, isolation, and model serving
```

The compact Core is:

- [`core/foundations.md`](core/foundations.md) — working foundations;
- [`core/stack.md`](core/stack.md) — inherited substrate and Agent-native responsibility overlay;
- [`core/primitives.md`](core/primitives.md) — backend objects, executable semantic primitives, promoted protocol objects, Host-proven work objects, and explicit research candidates.

## Research discipline

A proposed Agent-native layer must answer:

```text
Which mature lower mechanism is insufficient?
What exact invariant remains unowned?
What realistic trajectory fails if it is bypassed?
What second workload demonstrates the same responsibility?
Why is a new shared component better than a local policy or adapter?
```

Research interest does not imply implementation. A concept moves toward Core only after primary-source comparison, executable evidence, counterexamples, and deletion tests.

## Current questions

- [`ANC-STACK-001`](research/questions/ANC-STACK-001-classical-to-agent-native-transition.md) — classical substrate versus Agent-native responsibility;
- [`ANC-IR-001`](research/questions/ANC-IR-001-agent-effect-ir.md) — minimum useful Agent Effect IR;
- [`ANC-MEMORY-001`](research/questions/ANC-MEMORY-001-task-continuity.md) — minimum durable state for open-work continuity;
- [`ANC-EFFECT-001`](research/questions/ANC-EFFECT-001-tool-contract-evolution.md) — Tool-contract change and rebinding;
- [`ANC-ORG-001`](research/questions/ANC-ORG-001-agent-native-organization.md) — human and multi-Agent coordination around persistent work;
- [`ANC-ADAPT-001`](research/questions/ANC-ADAPT-001-agent-era-capabilities.md) — evidence-governed adaptation;
- [`ANC-SECURITY-001`](research/questions/ANC-SECURITY-001-adversarial-agent-systems.md) — adversarial Agent capability under independently bounded consequence.

See [`research/map.yaml`](research/map.yaml).

## Project roles

- **Ordivon Host** — bounded durable Goal and Task control, context compilation, candidate admission, Effect coordination, verification, and recovery;
- **Ordivon Runtime** — trusted-local Workspace, Job, Attempt, Artifact, physical dispatch, cancellation, reconciliation, and recovery;
- **Ordivon Link** — local network observation, controlled egress, Network World, and reference transport slices;
- **Ordivon Edge** — Cloudflare external Fetch, Browser, Artifact, receipt, and remote-body lifecycle experiments;
- **Ordivon Finance** — capital-domain truth, authority, decision, effect, and reconciliation laboratory;
- **Ordivon Game** — deterministic world, role-local context, coordination, replay, and evaluation laboratory;
- **Ordivon Security** — Campaign, consequence-envelope, independent judge, evidence, and reconstruction contracts;
- **Ordivon Web** — public publication and project navigation.

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

It preserves identity, explicit uncertainty, evidence provenance, authority, and replay while delegating byte durability, processes, files, and transport to classical systems. [`research/experiments/external-semantic-contract-v0/`](research/experiments/external-semantic-contract-v0/) separately tests public Effect, ToolContract, and EffectBinding boundaries.

## Coordination and state

Documents preserve stable theory, contracts, sources, and reproducible evidence. GitHub Issues own changing task state and dependencies. Git commits own code revision. Immutable [`System Snapshots`](research/evidence/) bind exact historical repository and Artifact combinations without becoming a second mutable deployment registry.
