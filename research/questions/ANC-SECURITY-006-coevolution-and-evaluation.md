# ANC-SECURITY-006 — Coevolution, Adversarial Evaluation, and Transfer

## Status

- Epistemic status: active research question
- Parent: `ANC-SECURITY-001`
- Related: `ANC-VERIFY-001`, `ANC-ADAPT-001`, `ANC-SECURITY-003`–`005`
- GitHub Issue: #75
- Primary consumers: Security and Game

## Question

How can Ordivon evaluate attack-defense coevolution when actors adapt to one
another, study or manipulate monitors and judges, and overfit to known opponents,
worlds, tools, or scoring rules?

## Why static evaluation is insufficient

A static benchmark estimates performance against a frozen task distribution.
Strategic adversarial systems change the distribution through:

- adaptation to the opponent;
- tool and policy mutation;
- changed organization;
- deception and evaluator manipulation;
- resource expenditure and capability exposure;
- world modification;
- repeated encounters and learned expectations.

The evaluator therefore cannot be treated as a timeless neutral function.

## Required outcome separation

At minimum, research should distinguish:

```text
run validity
  whether the environment and evidence support interpretation

tactical outcome
  whether local actions achieved their immediate effect

operational outcome
  whether missions and Campaign phases progressed

strategic outcome
  whether objectives, initiative, resources, exposure, and options improved

information outcome
  how knowledge, beliefs, uncertainty, and deception changed

evaluator integrity
  whether actors accessed, manipulated, gamed, or overfit the judge
```

No single scalar is assumed sufficient.

## Core subquestions

1. How should honest, attack, defense, deception, and evaluator-attack modes be
   represented without making the evaluator tell the actor its hidden role?
2. How do we distinguish genuine adaptation from memorization of one opponent?
3. What cycling, escalation, equilibrium, collapse, or arms-race patterns appear
   across repeated encounters?
4. Can monitor and judge capability keep pace with evaluated actors?
5. How should held-out opponents, social partners, worlds, tools, organizations,
   and test-time compute budgets be sampled?
6. Which improvements transfer, and which merely exploit a static evaluator?
7. How should individual trajectories remain available when aggregate results
   are distributional?

## Required comparisons

- Inspect AI and Inspect Cyber;
- ControlArena Settings, honest/attack modes, policies, monitors,
  micro-protocols, macro-protocols, safety, and usefulness;
- CybORG/CAGE rewards, observations, and world truth;
- repeated-trial capability evaluation and hidden scoring;
- self-play, league play, population-based training, and held-out opponents;
- Melting Pot-style generalization to unfamiliar social situations;
- Game replay and counterfactual analysis.

## Experiment families

### Held-out opponent population

Train or tune against one population and evaluate against hidden policies with
different risk, tempo, deception, and organization.

### Alternating and simultaneous adaptation

Compare best-response cycles, simultaneous learning, frozen-opponent controls,
and mixed historical opponent pools.

### Evaluator attack

Include synthetic answer lookup, reward hacking, judge manipulation, evidence
corruption, monitor evasion, and apparent compliance.

### Transfer

Change world topology, mission priority, available tools, budget, organization,
and model/scaffold while preserving the high-level Contest family.

### Compute scaling

Measure whether additional inference-time compute improves strategy, merely
searches harder over known paths, or increases evaluator exploitation.

## Evidence required

- evaluation-family, trial, seed, actor, opponent, world, judge, and budget
  identity;
- repeated trials with uncertainty;
- authoritative world truth plus actor-specific observations;
- hidden tests, opponents, or judge state;
- preserved trajectories and aggregate analysis;
- successful detection of at least one synthetic evaluator-gaming case;
- negative, null, regression, cycling, and collapse results;
- transfer evidence beyond the training opponent.

## Falsifiers

Reduce or delete the proposed evaluation layer if:

- rankings change arbitrarily under minor judge changes;
- gains vanish against held-out opponents;
- repeated play produces only overfitting or uninterpretable cycles;
- strategic or information outcomes cannot be grounded in world truth;
- the evaluator requires greater privileged intelligence than any plausible
  research setting can provide;
- added complexity produces no better model or engineering decision.

## Cross-project implications

- Game may provide hidden-state simulation, opponent populations, replay, and
  counterfactual branches;
- Security may define adversarial experiment families and strategic analyses;
- Host may expose exact model/scaffold/organization identity;
- Runtime, Link, and Edge provide native facts and resource conditions;
- Verify and Adapt tracks determine what results may feed post-training or
  policy improvement.
