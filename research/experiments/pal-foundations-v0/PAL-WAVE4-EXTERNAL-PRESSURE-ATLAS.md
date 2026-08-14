# PAL Foundations Wave 4 — External Pressure Atlas and First-Principles Reduction

Status: **research map, not architecture**.

External papers, economic history, adaptive-control results, autonomous-science systems, and Ordivon's own experiments are treated on the same epistemic plane: each is evidence about a mechanism under a bounded environment. A paper is not promoted because it is famous; an Ordivon result is not privileged because it is ours.

The purpose of Wave 4 is to attack the remaining PAL problems one by one while keeping them inside one common state model.

## 1. One coordinate system for the remaining problems

Represent the adaptive system at time `t` as:

```text
S_t = (
  X_t,   current world/task state
  C_t,   capability portfolio
  P_t,   retained priors / learned procedures
  G_t,   mechanisms that generate and apply changes
  V_t,   evaluation / selection machinery
  L_t,   lineage, commitments, evidence and authority continuity
  M_t    mandate / viability / terminal value anchors
)
```

The external world is `W_t`. A candidate adaptive change is `Δ_t` and the transition is:

```text
(S_{t+1}, observations) = T(S_t, W_t, Δ_t)
```

The six remaining problems are not six unrelated architecture nouns. They are six places where this transition is still under-specified:

| problem | unknown in the transition |
| --- | --- |
| option value | which parts of `C_t` should survive before future `W` is revealed |
| regulation | what happens when `Δ` can alter the evidence/evaluator that selects later `Δ` |
| complementarity / credit | whether the value of one `Δ_i` depends non-additively on other retained changes |
| prior revalidation | when a retained `P_t` remains causally applicable after `W`, model or task family changes |
| identity under change | which elements of `L_t` and `M_t` must survive when mechanisms themselves change |
| pressure selection | how candidate research pressures are generated and selected relative to `M_t` and observed mismatch with `W_t` |

This reduction gives a first important hypothesis:

> **PAL is primarily a problem of controlled state-transition under uncertainty, not a problem of maximizing an intrinsic scalar called “improvement.”**

Any scalar is local to a mandate/task and cannot substitute for the state dimensions above.

## 2. Cross-cutting first-principles laws to attack

### 2.1 Value is relational, temporal, and counterfactual

A capability, prior, method, or architecture element has no context-free adaptive value. Its value depends on:

```text
future world
+ mandate
+ alternatives
+ retained complements
+ carrying cost
+ reacquisition path
+ information created by retaining/using it
```

Therefore `persistent`, `deep`, `reusable`, `general`, and `open-ended` are descriptors, not value proofs.

### 2.2 A self-evaluator cannot certify itself without an independent causal path

If a change can alter the data, metric, judge, or evidence process that selects it, the loop can become circular:

```text
change
→ action
→ evidence distribution
→ evaluator score
→ retain change
↺
```

A meaningful regulator needs at least one observation/evidence path whose truth is not fully mediated by the candidate change being judged. This may be a frozen holdout, owner-native consequence, independent sensor, counterfactual, external verifier, or rollback comparison.

This is a causal-independence requirement, not a requirement for a permanent “regulator service.”

### 2.3 Marginal credit is valid only under separability assumptions

For capability/change set `S` and outcome `Y(S)`, standalone deletion logic assumes something close to additivity. Interaction is exposed by:

```text
I(A,B | S)
= Y(S+A+B) - Y(S+A) - Y(S+B) + Y(S)
```

F12 produced `I=+1` for full durable-correction closure in all three cases. That proves the *possibility* of interactional credit. It does not justify evaluating every power-set coalition.

A more economical hypothesis is:

> Search interactions along a known composition/dependency graph first; use factorial/coalition tests only where mechanism predicts a real interaction.

### 2.4 Prior validity depends on support conditions, not wall-clock age

A prior is applicable because the mechanism/assumptions that supported it still hold, not because it is recent. Conversely an old prior can remain valid if its causal support is unchanged.

A reusable prior should therefore be viewed as:

```text
claim
+ source domain
+ mechanism
+ assumptions/support conditions
+ evidence family
+ falsifier
+ known negative-transfer boundary
```

Model version, task-family change, owner drift, or a contradictory outcome create **revalidation pressure** only insofar as they threaten those support conditions. Generic TTL expiry is therefore not a first-principles solution.

### 2.5 Identity is continuity of commitments and lineage, not byte sameness

If implementation, models, providers, schemas, and policies can change, “same system” cannot mean same bytes. A candidate operational definition is:

```text
identity continuity
= explicit lineage
+ preserved authoritative commitments
+ preserved evidence/history where still interpretable
+ explicit migration of mutable state
+ explicit invalidation where interpretation changed
```

The mutable implementation is replaceable. Silent changes to authority, unresolved obligations, semantic identifiers, or evidence interpretation are identity breaks unless an authorized migration explicitly changes them.

### 2.6 Importance cannot be generated from nothing

A system can autonomously discover pressure only relative to some value/viability anchor. `important` is undefined without a mandate, survival constraint, objective, affected participant, or environment-relative criterion.

Therefore the strongest form of autonomous pressure selection should be rejected:

```text
system creates importance without an external value anchor
```

A more coherent target is:

```text
stable/slow mandate M
+ observations of W
+ current capability/model S
→ discover mismatch, bottleneck, opportunity, contradiction or uncertainty
→ formulate candidate research pressure
→ run discriminating probe
→ allocate bounded research effort
```

This reframes C6. The open problem is not “invent values autonomously”; it is “discover the highest-leverage pressure relative to existing value anchors without a human pre-formulating the exact problem.”

## 3. Problem A — option value

### External pressure

Real-options research shows why irreversibility and information arrival make waiting/flexibility valuable, but recent R&D work adds an important reversal: uncertainty can increase experimentation when the activity itself resolves uncertainty. Value-of-information research similarly distinguishes learning useful targets from merely acquiring more information.

The combined lesson is not “uncertainty means retain more.” It is:

> **Reversibility, information production, carrying cost, reacquisition cost, and future workload determine option value jointly.**

### First-principles loss instead of a retention score

For a retained capability set `S` and realized future workload sequence `ω`, define a post-reveal loss vector:

```text
L(S, ω) = (
  carrying cost,
  reacquisition cost,
  reacquisition delay,
  missed/blocked outcome,
  maintenance/compatibility failure,
  prior/bias cost,
  lost information/experimentation opportunity
)
```

Do **not** collapse these dimensions before the relevant mandate supplies an ordering.

For a particular bounded experiment whose units are commensurable, scalar realized regret may be defined only locally:

```text
Regret(policy, ω)
= Loss(S_policy, ω) - Loss(S_oracle-after-reveal, ω)
```

This is stronger than F11's t0 classification accuracy because the future world itself settles whether a retained option mattered.

### F14 admission target

Start a prospective **shadow capability portfolio** at a frozen cutoff. Do not mutate owner equipment merely to create the experiment.

Candidate portfolio should be drawn from already-real E0/P2 decisions, for example:

- scoped egress;
- TShark;
- bounded network-surface mapper;
- conditional mitmproxy;
- StrykerJS;
- Firefox/WebKit;
- Lighthouse/Lighthouse CI;
- additional static-analysis engine;
- Hypothesis in pinned Finance Python;
- reactive notebook environment;
- host-query engine;
- continuous telemetry stack.

At `t0`, freeze:

1. exact capability identity and current disposition;
2. carrying-cost evidence available now;
3. reacquisition/materialization path and any measured friction;
4. several retention policies **before** future consumption is known;
5. a future observation window and exact consumption-event semantics.

After `t0`, only owner-native future work and external/provider changes may create demand events. A consumption event requires exact owner evidence: code/evidence/Task/command that actually needs or attempts the capability. Narrative “this could have helped” does not count.

When a deferred capability first becomes demanded, measure reacquisition friction then; do not backfill an imagined cost.

This turns option value into prospective field regret rather than hindsight labeling.

## 4. Problem B — endogenous regulation

### External pressure

Reward-tampering work formalizes when agents gain incentives to alter their own reward process. Reward-model over-optimization demonstrates proxy improvement with degrading stronger objectives. Performative prediction shows decisions can alter the future distribution against which the predictor is evaluated. Pessimistic offline RL shows uncertainty can justify conservative value estimates when evidence coverage is weak.

### First-principles discriminating condition

Regulation is not identifiable unless the unregulated loop can actually self-certify a false change.

A valid experiment requires:

```text
candidate can affect future evidence/score
AND
proxy score can diverge from independent consequence truth
AND
baseline sometimes retains a false local winner
```

Then compare a minimal independent evidence path/rollback arm. If the unregulated arm never false-reinforces, repeat F7A's conclusion: regulation remains non-identifiable.

The strongest likely Ordivon test bed is not a synthetic reward toy. It is a multi-generation research/change loop where selected changes alter the next generation's evidence or candidate distribution while a frozen owner-native holdout remains outside that path.

## 5. Problem C — cross-domain complementarity and causal credit

### External pressure

Factorial causal inference provides a clean way to estimate interactions under intervention. Shapley-style interaction methods formalize coalition effects but are computationally expensive and depend on a chosen value function. Open-ended evolution and POET emphasize non-additive composition and stepping stones whose value appears only after transfer/composition.

### First-principles contraction

Do not build a universal coalition-credit engine.

Instead:

```text
known composition graph / dependency dependency edge
→ predict a specific interaction
→ neither / A / B / A+B
→ owner-native outcome
→ only then retain interaction evidence
```

The next acceptable case must be materially different from Harness cognition mechanics. A promising natural candidate is **Workstation scoped egress × Finance proxy-aware consumer transport** under a currently route-sensitive read-only OKX workload, but it must first be re-observed. If ambient networking already makes all arms equivalent, the experiment is not identifiable and should not run.

## 6. Problem D — prior revalidation / negative transfer

### External pressure

Bayesian change-point work treats regime identity as uncertain. Distribution-shift methods partially erase prior updates after detected changes. Continual-learning work shows old knowledge can cause negative transfer and that selective reset/forgetting can improve new-task learning.

### First-principles mechanism

No generic TTL.

Revalidation trigger should be a **support-boundary change**:

```text
prior K = (claim, mechanism, support assumptions, evidence family, falsifier)
new task/model/world
→ which support assumptions are threatened?
→ if none: prior remains usable
→ if some: prior becomes hypothesis, not authority
→ compare prior-on / prior-off / revalidated on independent target outcome
```

A natural future model/task-family change is required before this becomes an experiment. F5/F6/F9 labels must not be reused as the oracle.

## 7. Problem E — identity under genuine self-change

### External pressure

Event-sourced systems separate immutable historical events from current projections and use explicit evolution tactics such as versioned events and version adaptation. Schema-evolution research shows that data shape and code must migrate together. Self-modification literature repeatedly needs some evaluation criterion to remain stable while a particular modification is judged; a recent conceptual framework makes identity-under-transformation an explicit unresolved problem.

### First-principles candidate invariant boundary

At any one migration step, separate:

```text
must-preserve unless explicitly re-authorized
  task/object identity
  authority and ownership
  unresolved commitments/obligations
  accepted evidence lineage
  effect occurrence / uncertainty history
  participant constraints

may change under migration
  model/provider
  tool implementation
  storage representation
  schema version
  planning policy
  working view
  optimization method
```

A valid PAL identity experiment needs a real migration with competing inheritance policies:

```text
inherit everything
reset everything
invariant-bound migration
```

and must measure continuation correctness, stale-state carryover, evidence interpretability, authority violations, and recovery. Until such a real migration appears, H-IDENTITY remains open rather than simulated into existence.

## 8. Problem F — pressure selection / what to improve next

### External pressure

Current external systems repeatedly solve a **bounded** version of this problem:

- CURIOUS allocates practice by learning progress inside a predefined goal space;
- POET/UED generate challenges inside predefined environment-design spaces and objectives;
- DGM explores an archive of agent variants while external coding benchmarks supply selection pressure;
- AI Co-Scientist conditions hypothesis generation on scientist-provided research objectives and prior evidence;
- AI Scientist-v2 autonomously iterates research inside a supplied scientific domain/evaluation process;
- FirstResearch makes question formation auditable by exposing assumptions, mechanism, falsifier and decisive test, but current validation is preliminary and judge-based;
- large-scale LLM ideation studies still report self-evaluation/diversity as open weaknesses.

This is highly consistent with Ordivon's C6 negative result: external systems automate exploration **relative to an already-bounded objective/search space/evaluator** much more successfully than they derive what ultimately matters from nothing.

### First-principles redefinition

Reject:

```text
choose the globally most important next problem
```

Replace with:

```text
M = current mandate / survival / participant constraints
W = observed world
S = current system

pressure certificate =
  observed mismatch or opportunity
  + affected mandate
  + causal mechanism hypothesis
  + uncertainty
  + available discriminating probe
  + expected decision change if resolved
  + cost / reversibility
  + failure update
```

Candidate pressures should come from multiple independent sources rather than one global score:

- contradiction / falsifier;
- repeated reconstruction burden;
- blocked Goal/Task frontier;
- newly reachable capability/resource;
- high-consequence uncertainty;
- external demand / participant request;
- learning progress or regression;
- cross-domain repeated residual;
- unexplained performance delta.

Then selection is a bounded research-allocation problem, not a value-generation problem.

The next C6 successor should compare generic free-form “pick the next problem” against this certificate method on future owner-generated pressure events, with downstream evidence determining which proposed questions actually changed a decision or capability.

## 9. Current Wave 4 order

The order is chosen by whether a valid discriminating environment exists now, not by conceptual prestige:

1. **Option value** — admit a prospective shadow field portfolio now; future reality supplies the oracle.
2. **Complementarity** — immediately re-observe the natural Finance × Workstation candidate; run only if four-arm outcome remains identifiable.
3. **Regulation** — locate a real endogenous self-reinforcing research/change loop; no synthetic false-positive injection by default.
4. **Pressure selection** — redesign C6 around mandate-relative pressure certificates and future owner events.
5. **Prior revalidation** — wait for a natural earned-prior × model/task shift, then freeze the test before outcomes.
6. **Identity under change** — wait for a real migration/self-change episode with genuine inheritance alternatives.

The ordering may change if external reality produces a better falsifier first.

## 10. Anti-architecture boundary

Wave 4 does not authorize:

- a PAL controller;
- a universal improvement/option score;
- a regulator service;
- a Shapley/coalition-credit infrastructure layer;
- a prior TTL/expiry daemon;
- a global identity constitution object;
- an autonomous research scheduler;
- owner mutation merely to create evidence.

The research product is a better causal model and better discriminating experiments. Architecture follows only after repeated owner-native consumption.
