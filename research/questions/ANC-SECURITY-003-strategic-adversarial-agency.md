# ANC-SECURITY-003 — Strategic Adversarial Agency and Campaign Synthesis

## Status

- Epistemic status: active research question
- Parent: `ANC-SECURITY-001`
- GitHub Issue: #72
- Primary product consumer: `ordivon-security`
- Cross-project consumers: Host, Game, Runtime, Link, and Edge

## Question

What minimum model distinguishes strategic adversarial agency from classical
attack automation, finite-state or learned Red/Blue policies, ordinary Agent
planning, and durable workflows?

The working hierarchy is:

```text
Actor → Contest → Campaign → Mission → Operation → Action
```

It is provisional. The purpose of this question is to determine whether those
distinctions are real, useful, and irreducible—not to encode them immediately.

## Why this question exists

Existing systems already provide many lower-level pieces:

- ATT&CK provides tactical goals, techniques, and procedures;
- automated cyber reasoning systems discover, prove, exploit, and patch;
- CybORG/CAGE and CyberBattleSim provide partially observed multi-step
  attack-defense environments;
- Host can maintain Goals, Tasks, Context, and plans;
- Game can represent Worlds, actors, rules, and state transitions;
- workflow engines can execute long-lived graphs.

The unresolved question is whether strategic opposition requires additional
state and control semantics above those systems.

## Candidate distinctions

### Actor

An Actor is not merely a model invocation or process. It may require:

- strategic objective and acceptable end states;
- knowledge and uncertainty;
- beliefs about the world and other actors;
- resources, capabilities, and exposed or concealed assets;
- organizational role and authority;
- risk, time, and information preferences;
- continuity across individual Attempts.

### Contest

A Contest may differ from a generic World by making explicit:

- which actors have conflicting objectives;
- asymmetric information and observation rights;
- resources that can be consumed, denied, captured, or exposed;
- strategic victory, failure, withdrawal, and termination conditions;
- which world changes alter the balance among actors.

### Campaign

A Campaign may differ from a plan or workflow because it must be revised when:

- an opponent blocks or anticipates a path;
- observations indicate deception or changed capability;
- intermediate objectives lose strategic value;
- resource consumption changes feasible options;
- action would expose a scarce capability;
- initiative changes hands;
- withdrawal, concealment, escalation, or reserve becomes preferable.

## Core subquestions

1. What persists above individual Tasks and trajectories?
2. Which events should cause Campaign revision rather than ordinary retry or
   replanning?
3. How should initiative and tempo be measured when actions have different
   latency, visibility, reversibility, and compute cost?
4. How should an actor value retained access, secrecy, unused tools, future
   options, and uncommitted Agents?
5. Can a Campaign survive model, Host, process, body, or world replacement
   without implying false continuity?
6. When are phase, mission, operation, and reserve distinctions useful, and when
   are they imported terminology without measurable value?

## Required comparisons

- MITRE ATT&CK and its tactic/technique/procedure hierarchy;
- Cyber Kill Chain and threat-informed defense;
- DARPA Cyber Grand Challenge and AIxCC;
- CybORG/CAGE and CyberBattleSim;
- Inspect/ControlArena task and trajectory structures;
- Host Goal/Task/plan and classical workflow/DAG systems;
- POSGs and extensive-form games.

## Minimal experiment family

Use a mature simulated environment with:

- at least two viable routes to a strategic objective;
- a defender or attacker that changes policy during the episode;
- scarce action, time, compute, or visibility budget;
- delayed and path-dependent consequences;
- at least one action that creates local success while reducing future options;
- held-out opponent policies.

Compare:

1. fixed script or finite-state actor;
2. learned policy;
3. ordinary LLM Agent with transcript memory;
4. LLM Agent with explicit Campaign and strategic-state support.

## Evidence required

- exact actor, opponent, world, policy, model, scaffold, Tool, and budget identity;
- authoritative world truth and actor-specific observations;
- records showing why strategy changed, not merely that action changed;
- tactical, operational, and strategic outcomes reported separately;
- cost of maintaining proposed strategic state;
- transfer to at least one held-out opponent or world variation;
- negative cases where the strategic model adds no value.

## Falsifiers

Reduce or delete the proposed layer if:

- an ordinary trajectory plus Host memory expresses all necessary distinctions;
- fixed or learned policies adapt equivalently;
- Campaign state does not improve transfer, explanation, or long-horizon
  continuity;
- initiative/resource metrics merely duplicate cumulative reward;
- imported strategic terms cannot be grounded in observable facts.

## Cross-project implications

Potential implications are hypotheses only:

- Host may need strategic-context snapshots above individual Tasks;
- Game may need Contest adapters or actor-specific observations;
- Security may need Campaign records and strategic outcome analysis;
- Runtime, Link, and Edge should expose facts, not strategic interpretations.

No implementation request should be filed until an experiment demonstrates a
specific missing responsibility.
