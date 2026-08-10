# TM0 — Scientific Research Taste as a World-Model Prior

## Thesis

A useful way to describe scientific research taste is not “intuition” or a mysterious meta-cognitive faculty. It is a **revisable set of high-probability world-model claims about research dynamics**.

Examples are conditional claims such as:

- broad architecture work usually produces less discriminating evidence than a narrow falsifier when the causal bottleneck is still unknown;
- a cheap generator does not make an improvement problem tractable when verification or consequence reconciliation is expensive;
- the same semantic relation appearing in two domains does not imply that both domains should share a mechanism;
- deletion and substitution often reveal an invariant faster than adding another layer;
- once no available observation is likely to change the decision, continuing the loop is often worse research than lawful abstention.

These claims are not semantic laws like WL0 L1–L5. They can be wrong in a particular world. Their value is probabilistic: under recurring classes of problems, they improve the prior over **which question is worth asking next**.

That makes research taste directly relevant to RSI. An improving system needs not only a model of Reality and its Dynamics, but also a model of its own **research frontier**: which uncertainties are reachable, observable, discriminable, affordable, reversible, and capable of changing future decisions.

## Boundary: law, taste, and constitution

TM0 separates three different things that should not be collapsed.

### Semantic law

A law expresses a distinction whose unjustified collapse creates a structural category error. WL0 examples include representation/reality separation, applicability binding, scoped authority, and causal non-collapse.

### Research-taste prior

A taste prior expresses a conditional empirical expectation about research itself. “Prefer the smallest discriminating falsifier before a broad solution” is not universally true, but Ordivon's recent practice predicts that it will often reduce uncertainty faster and with less confounding.

### Constitution / architecture principle

A principle expresses a chosen system boundary, such as preserving owner authority or refusing to create a central implementation solely because semantics converge. It can be informed by the world model without pretending to be a descriptive law of nature.

This distinction matters because encoding taste as law would ossify research, while treating law as mere taste would allow repeated category errors.

## What the current method already does well

The existing Agent-First Research Method already contains a large fraction of good research taste, but mainly **after a burden has been selected**. Its loop starts from real Agent work, identifies the current responsibility carrier, names a strong simpler baseline, builds the smallest externalization hypothesis, runs a bounded experiment, and retains/narrows/defers/deletes from evidence.

The current method therefore already encodes several powerful priors:

```text
real work > conceptual appeal
specific responsibility > platform theme
strong simpler baseline > unchallenged novelty
bounded reversible experiment > broad irreversible reform
negative/deletion result = first-class evidence
owner-native evidence > copied research truth
```

The missing layer is earlier: given many live burdens, anomalies, possible questions, and possible observations, **which one should enter this loop first?**

That is where tractability and research taste begin.

## Evidence corpus

TM0 is retrospective. It does not claim an unbiased scientific sample. The audit deliberately uses materially different recent Ordivon trajectories that contain explicit continue/stop/delete/localize/promote decisions.

### Computer — removal-first Existence Gauntlet

`task:computing:computer-rsi-audit-20260810` revision 11 attacked 47 features. Only 2 survived unchanged; 20 were narrowed, 6 localized, 14 archived, 4 deleted, and 1 remained inconclusive.

The important result is not the exact count. It is that removal pressure repeatedly exposed a smaller responsibility than the existing abstraction suggested. The next action is contraction implementation, not another architecture-expansion phase, and a direct Agent-task ablation is required before deleting or rewriting Core.

This supports three priors:

1. **RT1 burden before abstraction** — historical existence and conceptual completeness are weak evidence of current utility;
2. **RT8 contraction as discovery** — deletion/narrowing is an experiment that reveals the invariant;
3. **RT4 strong baseline / ablation before rewrite** — even an attractive smaller world-model representation must beat the current Core in real Agent work before replacement.

### Harness P4 — autonomy without discovery efficiency

`task:harness-host:rsi-p4-20260810` revision 4 is unusually informative for research taste. The Agent selected 203 admitted repository observations across 204 rounds, read almost the complete Harness source surface, independently finalized two target hypotheses, and then falsified both. No source bytes needed to change.

The system correctly learned lawful no-change semantics. But the unresolved issue is now **discovery efficiency**: can the Agent choose a much smaller set of high-information observations and stop earlier without weakening causal admission quality?

This is a direct tractability result:

```text
more observation
!=
better research
```

The next useful problem is not another preselected bug. It is observation/question selection itself.

This supports RT2, RT10, RT12 and directly falsifies the anti-prior that more complete context or source coverage is always better.

### Runtime P3 — stronger mechanism can be the wrong experiment

`task:runtime:rsi-p3-toctou-and-third-effect-20260810` revision 6 first proved a real delayed-consumption TOCTOU gap, then strengthened continuity evidence. But a seemingly stronger default — exact executable byte materialization through sealed memfd — remained rejected because it changed legitimate target-visible pathname semantics such as shebang `__file__`, `argv[0]`, and ELF `/proc/self/exe` behavior.

This is a strong taste lesson:

> do not optimize an abstract property such as “stronger isolation” before checking whether the proposed mechanism preserves the actual semantics being studied.

A small physical falsifier had more value than a generic hardening program. It supports RT2 and rejects the anti-prior “stronger mechanism is automatically more correct.”

### World high-pressure survival — stopping is part of research quality

`task:world:high-pressure-survival-audit-20260810` revision 5 completed HP0–HP8 and explicitly says there is no further HP-series action. Future World work should reopen only when a real workload/failure changes the boundary.

The audit also moved historical studies out of current authority and improved deterministic retrieval while reducing active retrieval burden. More importantly, multiple unresolved items were left with their actual owners instead of being absorbed by World.

This supports RT1, RT7, RT8, RT10 and the broader idea that a good frontier model includes **where not to spend more search budget**.

### Studio/Web — ordinary work beats aesthetic/platform speculation

`task:studio-web:hp-agent-friction-recurrence-20260810` revision 3 tested retained priors on real ordinary work. Twenty current social assets were already task-legible at the tested size, so no gratuitous redesign was admitted. Adversarial cases exposed specific overflow and CJK limitations, while dominant remaining friction moved toward Runtime/package/browser environment rather than Production architecture.

The next actions explicitly avoid manufacturing another workload only for metrics. Real multilingual publication should trigger a new font/glyph experiment only when it actually appears.

This supports RT1, RT3, RT10 and shows that research taste includes **moving attention when the dominant bottleneck moves**, rather than defending the current project's agenda.

### Computer P0 consumer falsification — capability gain has a price

`task:computing:p0-consumer-falsification-20260810` revision 7 compared a strong one-shot baseline against the current public DomainToolLoopRunner on five valid live pairs. The simpler baseline accepted 0/5; Harness accepted 3/5 and produced verifier-passing candidate bytes 4/5, but at roughly 7.93× Provider-token cost.

The correct conclusion was scoped retain/localize rather than “Agent loops are better” or “one-shot is cheaper.” The experiment makes tractability multidimensional: better capability can be real while still carrying a large closed-loop cost.

This supports RT3 and RT4.

### Security uncertainty retention — forced certainty destroys future value

`task:security:cage-structured-uncertainty-retention-20260810` revision 2 found that Harness can retain unresolved unknowns while a Security adapter currently collapses them into an empty list. Earlier Security experiments showed that structured unknowns survive useful reasoning and temporal/provenance adjudication.

This supports RT9. A system that forces uncertainty into a terminal label may make the current record look simpler while making subsequent research less tractable because it has destroyed the distinction needed to decide what to observe next.

## The strongest candidate priors

TM0 currently finds twelve candidate priors. Ten have strong or emerging-strong support; two are deliberately marked emerging.

### RT1 — Start from observed burden, not named concept

A concept is cheap to invent. A repeatedly reconstructed responsibility, reproducible failure, or measurable decision cost is much stronger evidence that a structure deserves attention.

This transforms:

```text
Should we build Memory / Graph / World / Loop?
```

into:

```text
What recurring burden exists?
Who carries it now?
What fails when that carrier disappears?
What is the narrowest candidate that could remove it?
```

### RT2 — Prefer the smallest discriminating falsifier

When the causal model is uncertain, broad implementation adds confounders. A good research question seeks an observation or intervention whose possible outcomes eliminate materially different explanations.

The operative object is not “small change” but **smallest change that separates the live hypotheses**.

### RT3 — Tractability is closed-loop cost, not generation cost

A system can generate thousands of variants and still have an intractable improvement problem when:

- evaluation takes days;
- the metric is weakly related to the real goal;
- external effects are ambiguous;
- recovery is expensive;
- human review dominates;
- environment setup is fragile;
- repeated observations consume most of the budget.

For RSI, the scarce resource is therefore not just FLOPs or tokens. It is the total cost of obtaining **decision-changing trusted evidence**.

### RT4 — Beat the strong simpler baseline

New structure does not earn existence by being more expressive. It must create a useful capability or reduce recurring burden enough to justify its permanent complexity.

The relevant baseline can be classical infrastructure, a stronger one-shot model, direct owner-native state, a local adapter, or simply deletion.

### RT5 — Reversibility expands the practical search frontier

A reversible private experiment makes more hypotheses tractable because the Agent can fail cheaply. Recovery, exact replay, isolated workspaces, immutable inputs, and scoped effect semantics therefore matter to RSI not merely as safety devices but as **search-space enlargers**.

This prior has an important limit: some social, economic, adversarial, and irreversible phenomena cannot be learned from consequence-free simulation alone.

### RT6 — Observability precedes optimization

An optimization loop without a trustworthy observation boundary can improve the wrong representation indefinitely.

Before asking “how can we make X better?”, a high-taste transformation is often:

```text
what observation would distinguish better from merely different?
```

### RT7 — Generalize only after materially different recurrence

The same words or fields appearing in multiple projects are weak evidence. The stronger signal is independent recurrence of the same invariant under different dynamics and owners.

Even then, semantic convergence does not automatically imply mechanism convergence.

### RT8 — Contraction is a discovery operator

Deletion, narrowing, localization, and archive are not cleanup after research. They are experiments.

If removing a layer leaves the claimed invariant intact, the world model was over-factored. If removal causes a reproducible unique failure, the surviving boundary becomes clearer.

### RT9 — Preserve unknowns

Unknown, ambiguous, stale, unsupported, absent, and false are different states because they imply different next observations and interventions.

Premature certainty can reduce apparent complexity while increasing future research cost.

### RT10 — Stop when no causally justified target remains

A recursive loop that must always mutate will eventually manufacture work. Research taste therefore includes an optimal-stopping instinct: if no available observation is likely to change the decision enough to justify its cost, abstention or changing the question is progress.

The caveat is equally important: “no target under the current observation policy” is not “the system is globally correct.” New capabilities or cheaper observations can reopen the frontier.

### RT11 — Experimentability can compound more than direct capability

Runtime receipts, immutable input binding, Host continuity, Harness working-set control, owner-native observations, replay, and recovery can look like infrastructure work rather than intelligence improvement.

But when they reduce the cost or increase the fidelity of many future experiments, they improve the **improvement function itself**. This is one of the strongest connections between Ordivon's infrastructure work and RSI.

This prior is still marked emerging because meta-infrastructure can easily become self-referential overhead.

### RT12 — Good questions change the frontier

Answer volume is weak evidence of research progress. A stronger question is:

> If this experiment returns each plausible outcome, will our next admissible action actually differ?

Questions whose outcomes delete large hypothesis regions, change ownership placement, change whether a mechanism survives, or lower future experiment cost have high frontier value.

This is the closest current formulation to “scientific taste” as an RSI capability.

## Tractability is a vector, not a scalar

TM0 rejects a universal “tractability score” for now. The same question can be easy computationally and impossible experimentally, or cheap to verify but inaccessible under current authority.

A useful Agent frontier representation should at least reason over these dimensions:

| Dimension | Question |
|---|---|
| Observability | Can we see the relevant state/outcome? |
| Discriminability | Can one bounded result separate live explanations? |
| Feedback latency | How quickly does evidence affect the next decision? |
| Verification cost | How expensive is trustworthy evaluation? |
| Experiment cost | What must be built/run before evidence appears? |
| Authority/access | Is the needed observation/intervention admissible? |
| Reversibility/recovery | What happens when the experiment is wrong? |
| Search branching | How many plausible branches survive each observation? |
| Generality/recurrence | Is the result likely local or reusable? |
| Meta-leverage | Will this lower the cost of future improvement cycles? |

These dimensions are intentionally not summed into one number. Different research missions can trade them differently, and false scalar precision would hide the world-model assumptions behind the weights.

## Question-transformations: the practical form of research taste

A mature research Agent probably does not need to recite twelve priors before every action. The useful operational form is a set of **question transformations**.

### Q1 — Theme → burden

```text
Should we build X?
→
Which observed burden or non-bypassable responsibility would X remove?
```

### Q2 — Grand goal → current bottleneck

```text
How do we solve all of Y?
→
Which current bottleneck prevents the next meaningful transition?
```

### Q3 — Solution → falsifier

```text
How do we improve X?
→
What smallest experiment would prove X insufficient or unnecessary?
```

### Q4 — Feature → deletion counterfactual

```text
Does X work?
→
What fails if X is deleted, narrowed, localized, or replaced by the simpler baseline?
```

### Q5 — Similarity → recurrence

```text
This appears in two projects; should it be shared?
→
Does a materially different owner reproduce both the semantic invariant and the mechanical friction?
```

### Q6 — Generation → discrimination

```text
Can we generate better candidates?
→
Can we cheaply distinguish a genuinely better candidate from a plausible wrong one?
```

### Q7 — Continuation → stopping value

```text
What should we do next?
→
Which next observation could still change the decision, at what cost, and what makes stopping correct?
```

### Q8 — Mechanical success → consequence

```text
The operation passed; are we done?
→
Which causal stage and domain consequence were actually established?
```

### Q9 — Global world → owner boundary

```text
How do we model/control the whole world?
→
Which owner-native relation or consequence is currently unobservable or unactionable?
```

### Q10 — Search more → observe better

```text
Search more of the space.
→
Which next observation has the highest expected discrimination or frontier-changing value relative to cost?
```

Q10 is particularly important after Harness P4. The open RSI bottleneck is no longer merely whether an Agent can choose observations. It is whether it can learn **which observations are worth choosing**.

## Where current Ordivon is already this mode

Ordivon is already substantially tractability-driven, even though the concept was not named explicitly.

Its repeated pattern is:

```text
owner-native anomaly / burden
→ narrow question
→ smallest falsifier
→ reversible physical experiment
→ independent evidence
→ retain / narrow / localize / delete
→ move the frontier
→ stop when no justified next intervention exists
```

This is why recent progress often looks like expansion followed by aggressive contraction. Expansion generates candidate representations and mechanisms. Contraction learns which distinctions survive contact with Reality.

In that sense, contraction is not the opposite of RSI. It is one of the main ways RSI prevents its own search space from exploding.

## The important gap: frontier selection is still mostly implicit

The current Research Method is already good at executing a chosen bounded question. The weak point appears one level earlier.

Given:

```text
100 possible burdens
20 unresolved anomalies
10 plausible abstractions
5 available environments
finite tokens / compute / human attention
```

we do not yet have a well-tested Agent-native answer to:

> Which question should consume the next unit of research budget?

Current practice answers this through a mixture of project context, the shared world model, user direction, Agent judgment, obvious failures, and accumulated local experience. That is already “research taste,” but it is weakly externalized and poorly calibrated.

The main gaps are:

1. **No prospective calibration.** We know which past decisions look good after seeing outcomes, but we rarely freeze a predicted tractability judgment before running the experiment.
2. **Rejected alternatives are often implicit.** We record the selected question and falsifier better than the other questions we consciously declined.
3. **Information gain is not directly observed.** We measure tokens, tests, time, errors, or product effects, but seldom record how much of the live hypothesis space an experiment eliminated.
4. **Observation selection remains expensive.** Harness P4's 203 observations demonstrate authority/autonomy, not efficient research taste.
5. **The taste model has no explicit learning loop.** When a supposedly high-value direction yields little information, the system does not yet update a durable prior saying “questions of this form under these conditions tend to be poor bets.”

This is the clearest current distance between Ordivon's research method and a stronger RSI research policy.

## What should not be built

TM0 specifically rejects the obvious overreaction:

```text
TractabilityEngine
ResearchTasteService
UniversalQuestionScore
MetaReasoningRegistry
```

Those would turn an emerging probabilistic research model into architecture before it has prospective evidence.

A compact checklist or Agent-visible representation is enough for the first prospective test.

## Current world-model update

The strongest TM0 update is:

> **Scientific research taste can be modeled as a learned prior over transformations of the research frontier, not as a mysterious faculty and not primarily as domain facts.**

It predicts which reformulation is likely to turn an open-ended problem into a bounded path from current state to decision-changing evidence.

For an RSI system, this adds a second learned model beside the ordinary world model:

```text
World Model M
  predicts states / relations / dynamics

Research Frontier Model T
  predicts which unknowns and interventions are
  observable, discriminable, affordable, recoverable,
  high-leverage, and worth pursuing next
```

The recursive loop then becomes:

```text
Reality
→ Observation
→ update M
→ generate candidate questions/interventions
→ use T to choose a tractable high-value frontier
→ experiment
→ observe consequence
→ update M
→ update T from whether the research bet paid off
↺
```

The final arrow is the important RSI step. The system should learn not only **what the world is like**, but also **what kinds of questions tend to improve its model of the world efficiently**.

## TM0 verdict

Ordivon is already operating in this mode partially and implicitly. Its strongest existing research priors are burden-first inquiry, discriminating falsification, strong simpler baselines, reversible experimentation, owner-native observation, recurrence before generalization, contraction, uncertainty retention, and lawful stopping.

The next bottleneck is not another ontology layer. It is **prospective calibration of frontier selection**.

A future falsifier should freeze several real candidate questions before outcomes are known, ask an Agent to rank them using only a compact subset of the TM0 priors, compare against a strong simpler selection baseline, and then measure not only task success but information gained, total closed-loop cost, unnecessary exploration, false promotion, and correct abstention.

Until that prospective test exists, TM0 remains a research-world-model hypothesis rather than a new Ordivon law or product subsystem.
