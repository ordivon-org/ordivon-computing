# SECURITY-CHARTER-001 — Agent-Native Strategic Adversarial Systems

Status: strategic reorientation — active research charter

## Mission

Ordivon Security is the strategic adversarial-systems branch of Ordivon. It
studies intelligent actors that pursue conflicting objectives in long-horizon,
partially observed, dynamically changing digital environments containing other
adaptive actors.

The project is not primarily an Agent-safety, guardrail, compliance, containment,
or enterprise-protection layer. Its central question is:

> What changes when the environment contains another intelligent subject that
> actively shapes an Agent's observations, beliefs, actions, organization, and
> learning?

Cyber operations are the first experimental domain because they are digital,
tool-rich, replayable, measurable, and compatible with owned isolated ranges.
They are not the final theoretical boundary.

## Core research object

The core object is the **adversarial relationship** rather than the vulnerability,
permission, alert, isolated action, or safety incident.

A serious research setting contains:

- multiple goal-bearing actors;
- conflicting or partially conflicting objectives;
- asymmetric and potentially manipulated information;
- scarce resources and constrained opportunities;
- a contested World whose state can change;
- adaptation and counter-adaptation;
- strategic victory, failure, withdrawal, and exit conditions;
- consequences that unfold across many Tasks, Attempts, and observations.

## Candidate vocabulary

The current leading vocabulary is:

```text
Actor
  goal + knowledge + beliefs + resources + capabilities + organization

Contest
  actors + conflict structure + world + information + rules + outcomes

Campaign
  one actor or coalition's long-horizon organized effort within a Contest

Mission / Operation / Action
  progressively narrower units below a Campaign
```

Additional candidate concepts include opponent model, belief state, information
position, initiative, tempo, capability exposure, reserve, option value,
adaptation history, and strategic outcome.

These are research hypotheses. They are not authorized as a new ontology,
Protocol, database, or production control plane until comparative experiments
show that mature alternatives and simpler records cannot express the required
distinctions.

## Research domains

- autonomous Campaign synthesis and revision from strategic objectives;
- opponent modelling and belief revision under partial observability;
- intelligence collection, denial, deception, signalling, and counter-deception;
- initiative, tempo, escalation, withdrawal, and strategic resource allocation;
- adaptive offensive and defensive behavior under active counterplay;
- multi-Agent organization, command, delegation, compartmentalization, trust,
  collusion, and reorganization;
- long-horizon continuity across model, Host, process, body, and world changes;
- attack-defense coevolution and transfer across opponents and environments;
- adversarial evaluation where monitors, judges, traces, and scoring rules may
  themselves be studied or manipulated by evaluated actors.

## Relationship to classical and existing systems

Ordivon should reuse:

- MITRE ATT&CK, D3FEND, Engage, threat intelligence, and deception knowledge;
- scanners, fuzzers, program analysis, patch systems, identity systems,
  sandboxes, networks, EDR/SIEM, forensics, and incident-response mechanisms;
- DARPA-style cyber reasoning systems;
- CybORG/CAGE, CyberBattleSim, Inspect, Inspect Cyber, ControlArena, and other
  mature evaluation or simulation substrates;
- POSG, extensive-form-game, opponent-modelling, MARL, and social-generalization
  research.

The Agent-native research gap is not the existence of attack or defense actions.
It is how an intelligent actor selects, composes, conceals, revises, allocates,
and evaluates those actions against another adaptive actor.

## Ordivon composition

```text
Host      cognition, Goal, Task, Context, memory, Agent continuity
Runtime   Effects, Workspace, Job, Attempt, process and terminal facts
Link      communication relationships and path evidence
Edge      external execution bodies and provider lifecycle
Game      general World mechanics, simulation, replay, interaction substrates
Security  adversarial relationship, Campaign research, opponent models,
          information position, strategic outcome, adversarial evaluation
Computing cross-project theory, comparisons, falsifiers, and responsibility map
```

Security must not copy component-native truth.

## Current implementation disposition

The existing `ordivon-security` Campaign Manifest, lifecycle ledger, bindings,
reconciliation, residual accounting, replay, and Link/Edge/Runtime composition
are retained as an **experimental-support substrate**.

They prove bounded world admission, lifecycle closure, exact identity binding,
and evidence integrity. They do not prove strategic adversarial agency,
Campaign synthesis, opponent modelling, deception, dynamic Red/Blue behavior,
multi-Agent command, or coevolution.

The substrate is frozen by default. Expansion requires a concrete adversarial
experiment that cannot be represented through mature external tooling, current
minimal records, or the natural owner component.

## Research decomposition

- `ANC-SECURITY-001` — umbrella strategic adversarial-systems question;
- `ANC-SECURITY-002` — completed supporting comparison of World, Body,
  evidence, evaluation, and mature substrates;
- `ANC-SECURITY-003` — strategic adversarial agency and Campaign synthesis;
- `ANC-SECURITY-004` — opponent modelling, deception, and information state;
- `ANC-SECURITY-005` — multi-Agent adversarial organization and collusion;
- `ANC-SECURITY-006` — coevolution, adversarial evaluation, and transfer.

## Governing principles

1. Opposition is intelligent, not a static fault.
2. Strategy is not a workflow.
3. Information and belief state are part of the contested state.
4. Attack and defense are symmetric research objects.
5. Capability is relational to opponent, information, resources, environment,
   time, and organization.
6. The evaluator is a potential attack surface and strategic actor.
7. Research precedes ontology and implementation.
8. Dynamic-opponent experiments may use mature simulated substrates before
   custom Link/Edge fidelity is complete.
9. Every abstraction requires a simpler baseline and deletion criterion.
10. Owned ranges may permit high internal autonomy; uncontrolled third-party
    effects remain outside the research authority.

## Success condition

The program succeeds when Ordivon can make intelligent opposition a first-class,
reproducible research object; distinguish tactical success from operational and
strategic advantage; explain how actors model and manipulate one another; and
demonstrate adaptive attack-defense behavior that cannot be reduced to scripted
tools, fixed policies, ordinary workflows, or static benchmarks.
