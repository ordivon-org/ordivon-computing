# Ordivon Insertion and Repository Boundaries

## 1. Insertion thesis

Ordivon Security should not insert between every Agent action and the classical
execution substrate as a permanent security gate.

Its candidate insertion is higher:

```text
strategic objective
→ Campaign and opponent reasoning
→ Host-owned Tasks and Agent cognition
→ Runtime / Link / Edge / Game effects
→ actor observations and authoritative world facts
→ adversarial evaluation and Campaign revision
```

Security studies the conflict relation and consumes component-native facts. It
does not become a universal mediator for ordinary work.

## 2. Responsibility matrix

| Concern | Natural owner | Security relation |
|---|---|---|
| model call, Context, reasoning loop, Goal, Task, memory | Host | consumes actor/cognition identity and may supply adversarial research context |
| Effect execution, Workspace, Job, Attempt, process tree | Runtime | consumes receipts and terminal facts |
| communication path, topology, delivery, impairment, network evidence | Link | treats network conditions as Contest variables without owning transport |
| external body, provider, Sandbox generation, placement | Edge | binds actor presence to bodies without owning provider lifecycle |
| World state, rules, hidden information, simulation, replay | Game | uses Worlds and actor-specific observations; may provide scenario adapters |
| scanners, fuzzers, exploit/patch tools, EDR, IAM, sandboxes | mature external systems | uses as tactical capabilities and sensors |
| Actor conflict, Contest, Campaign, opponent model, information position, strategic outcome | Security research | candidate ownership pending experiments |
| cross-project theory, novelty tests, falsifiers, promotion decisions | Computing | authoritative research home |

## 3. What existing Security code is

The current repository contains:

- Campaign admission;
- capability/consequence declarations;
- component-native identity bindings;
- lifecycle intent and reconciliation;
- residual closure;
- evidence export and replay;
- one infrastructure-only Link/Edge/Runtime composition.

This code is a **research substrate** for owned-world experiments. It should be
maintained because it already demonstrates useful systems properties.

It should not be interpreted as:

- a completed Campaign engine;
- the strategic Actor model;
- an adversarial organization layer;
- a production control plane;
- evidence that adaptive attack or defense exists;
- a reason to delay simulated research until a custom physical range is complete.

## 4. Freeze and promotion rules

### Freeze by default

Do not expand:

- Campaign schema;
- lifecycle verbs or coordinator;
- identity graph;
- evidence-bundle vocabulary;
- process or network wrappers;
- containment and policy machinery;

unless a concrete dynamic-opponent experiment exposes an unrepresentable fact.

### Promote only after pressure

A proposed Security responsibility may be promoted when:

1. a mature environment or thin adapter cannot express the fact;
2. the fact affects strategic performance, transfer, diagnosis, or evaluator
   validity;
3. it spans components but does not belong naturally to one component;
4. at least two workload families need it;
5. a simpler record or local policy has been tested;
6. the implementation cost and governance friction are measured;
7. a deletion path remains available.

## 5. Candidate interfaces, not commitments

Experiments may eventually need thin records such as:

```text
ActorBinding
  Security actor hypothesis
  ↔ Host Agent / Goal / Task / Attempt identity

WorldObservationBinding
  actor-specific observation
  ↔ Game / Link / Runtime / Edge authoritative fact roots

CampaignSnapshot
  strategic objective, hypotheses, resources, organization, and alternatives
  at one revision

StrategicOutcomeRecord
  tactical, operational, strategic, information, validity, and evaluator fields
```

These names are examples only. Existing evaluation logs, provenance graphs, or
scenario-local data may prove sufficient.

## 6. Security and Game

Game is the closest neighbouring project.

```text
Game
  general World, rules, actors, actions, hidden state, replay, interaction

Security
  conflicting objectives, opponent hypotheses, information conflict,
  Campaigns, strategic adaptation, and adversarial evaluation
```

Possible outcomes of research:

- Security becomes a set of adversarial scenario/evaluation packages built on
  Game;
- Game supplies shared World mechanics while Security owns compact strategic
  records;
- the projects share no new core objects and integrate only through adapters;
- some current Security responsibilities migrate into Game or Verify.

Repository separation is a hypothesis, not an axiom.

## 7. Security and Host

Host owns how one or many Agents think and continue work. Security should not
implement another Agent loop.

Potential pressure on Host may include:

- bounded strategic context above one Task;
- actor-specific observations and belief hypotheses;
- organization and delegation identities;
- exact model/scaffold/resource snapshots;
- preservation of Campaign-relevant state across replacement.

These become Host issues only after experiments prove a reusable Host need.

## 8. Security and Runtime

Runtime executes Effects and preserves physical facts. It should not infer
adversarial intention.

Security may consume:

- Attempt and process identity;
- file, process, network, and Artifact effects;
- cancellation and ambiguous-outcome facts;
- resource consumption;
- terminal and residual state.

Strategic interpretation remains outside Runtime.

## 9. Security and Link/Edge

Link and Edge are optional fidelity providers, not prerequisites for early
strategic research.

Link can make topology, delay, visibility, partition, identity, and
communication evidence causal variables. Edge can provide heterogeneous bodies
and provider failure. Neither should implement Campaign strategy.

A custom persistent Link/Edge range is justified only when mature simulation or
sandbox environments cannot answer a material question.

## 10. Security and classical tools

Classical security capabilities become:

- weapons and countermeasures;
- sensors and intelligence sources;
- terrain constraints;
- resource objects;
- deception surfaces;
- recovery capabilities.

The research target is the Agent's strategic use and interpretation of them, not
the mechanisms themselves.

## 11. Route change for existing Issues

| Existing work | Revised interpretation |
|---|---|
| Security #1 | strategic adversarial-systems program, not infrastructure program |
| Security #4 | first dynamic-opponent strategic Contest and Red/Blue experiment |
| Security #10 | one information-manipulation and deception experiment family |
| Security #11 | supporting coordinator debt; not a conceptual P0 gate |
| Security #12 | evaluation-validity support, not strategic core |
| Security #13 | repeated-evaluation foundation used by coevolution research |
| Security #14 | optional first Agent/substrate spike, subordinate to dynamic-opponent research |
| Computing #46 | umbrella cross-project strategic adversarial research program |
| Computing #57 | supporting comparison of mature World/Body/evidence substrates |
| Computing #72–#75 | main research decomposition |

## 12. Repository admission test

Work belongs in `ordivon-security` only if most answers are yes:

1. Is there an adaptive or strategically relevant opponent?
2. Are objectives, information, resources, organization, or world state in
   conflict?
3. Does the question span more than one isolated action or Task?
4. Is an opponent, deception, organization, adaptation, or strategic-outcome
   distinction required?
5. Is there a mature or scripted baseline?
6. Would deleting the Security-specific layer erase measurable adversarial
   capability or explanation?

Otherwise the work belongs in another Ordivon project, a mature external tool,
or a scenario-specific adapter.
