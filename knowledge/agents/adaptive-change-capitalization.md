# Adaptive Change: Capitalization, Bias, Burden, and Optionality

## Scope

This page records reusable conclusions from the Computing-local PAL Foundations experiments. It is **not** a PAL architecture, controller, improvement score, retention service, or owner policy. It explains several distinctions that survived repeated falsification strongly enough to reuse in later research and design.

The derivation remains in `research/experiments/pal-foundations-v0/`. Open hypotheses stay there rather than being promoted here.

## 1. Persistence is not adaptive value

A change must remain available before it can be reused, but availability does not show that later work benefits from it.

```text
persistent state / code / capability / prior
            !=
independent future value
```

The distinction appears across several materially different cases:

- reconstructable Host state can be persisted without improving continuation;
- a scoped network path can exist without expanding the current useful-work frontier;
- a behavior-changing prior can persist while failing its objective;
- historical implementation can remain available in Git while active retention would only add maintenance.

The useful question is therefore not *did the change survive?* but *what later consumer cashes the change, on what owner-native outcome, at what recurring cost?*

## 2. Recursive depth is descriptive, not a value ordering

It is useful to distinguish state, capability, policy, knowledge, method, and meta-selection changes. It is not justified to assume that a change is more valuable merely because it sounds more recursively powerful.

A method or meta-selection rule can become stale, model-specific, over-conservative, or simply redundant. A shallow deterministic projection can transfer strongly when it removes a real repeated burden.

```text
change depth
    !=
compounding rank
```

Prefer mechanism evidence: owner fit, future-model robustness, observed burden, causal distance, independent consumption, maintenance cost, and held-out outcome.

## 3. Retained priors are interventions, not neutral capital

A retained rule, example, prompt prior, or research heuristic changes the input distribution seen by future cognition. Its historical success does not grant permanent authority.

PAL Foundations repeatedly observed sign-changing or boundary-shifting effects:

- one infrastructure-promotion prior helped a weaker model while pushing a stronger model toward under-promotion;
- a generic calibrated checklist added cost without stable cross-model superiority;
- historical examples shifted predictions toward capitalizing changes, including false promotion of negative cases;
- an option-aware lens helped some cases/models and harmed or missed others.

The stable conclusion is:

```text
retained learning
→ future decision-boundary intervention
→ may help, do nothing, or harm
```

Therefore reusable cognition should preserve provenance, scope, falsifiers, and reopen conditions. No generic expiry or revalidation algorithm has yet been earned; when model or task family changes materially, old priors should lose presumptive authority rather than silently becoming current truth.

## 4. Safe responsibility placement is not sufficient reason to externalize

A responsibility may clearly belong outside model cognition—because it requires exact identity, persistence, authority, reconciliation, or deterministic precision—without every possible projection of that responsibility being useful.

Externalization becomes valuable when there is an **observed reconstruction burden** that the smaller external mechanism actually removes.

```text
stable responsibility
+ correct owner / authority
+ repeated mechanical reconstruction error or cost
+ smaller reliable projection
→ candidate externalization value
```

In F10A, compiled reduction helped only the cases with duplicate-aware quorum/arithmetic burden; simple deterministic and reconciliation cases were already model-ceiling. Security P4 and the earlier Agent-consumption work show the same direction on natural workloads.

Do not manufacture larger raw packets to justify a projection. Observe the burden first.

## 5. More explicit variation is not a default improvement mechanism

Generating more alternatives can help only if candidate generation is actually the bottleneck.

Across both closed-menu and open-ended diagnosis experiments, explicit multi-candidate generation produced no stable final-diagnosis or oracle-candidate-coverage gain over a strong direct model. In some runs it reduced structured validity, and some rows already contained the right candidate but selected the wrong final answer.

```text
more candidates
    can become
more selection burden
```

Reopen explicit branching, multi-Agent variation, or variant factories only when natural repeated evidence shows that a strong direct model fails to generate the required causal family. Do not infer a search substrate from the abstract desirability of diversity.

## 6. Current use and future option value are different dimensions

A capability can fail its declared objective or expand no current workload frontier and still later reduce the cost of entering an adjacent problem.

Historical Computing dogfood repeatedly found this pattern, and PAL P2 supplies a direct Ordivon example: scoped egress expanded no tested current useful-work frontier at the P2 decision point, yet later Finance/Workstation work consumed and hardened that capability.

So:

```text
zero current use
    !=
zero future option value
```

But the inverse error is equally important:

```text
possible future value
    !=
retain everything
```

F11 failed to establish a generic option-aware retention rule. Both greedy and option-aware treatments rejected the negative controls well; the difficult problem was identifying *which* dormant positive would later matter. Option value is therefore a real outcome dimension whose prospective valuation remains uncertain.

Useful future experiments should measure carrying cost, reacquisition cost, hidden future workload probability, realized regret, and portfolio diversity rather than treating `retain/delete` as certain at time zero.

## What remains research-only

These questions are important but are not stable knowledge claims yet:

- whether local causal-credit proximity is a general transfer mechanism;
- whether explicit independent regulation is necessary to prevent endogenous self-reinforcement;
- whether selection rather than generation is the dominant current recursive-improvement bottleneck;
- how broad complementarity/coalition credit behaves outside the scoped Harness durable-correction case;
- how identity and inherited commitments should behave across genuine self-change;
- how a system reliably discovers the next important improvement pressure;
- how prior expiry/revalidation should work after a natural model/task-family change.

A negative or unidentifiable result remains evidence. These questions should reopen only when a materially better discriminating experiment exists.

## Evidence

Primary current research artifacts:

- `research/experiments/pal-foundations-v0/hypothesis-map-v2.json`
- `research/experiments/pal-foundations-v0/knowledge-promotion-audit-v0.json`
- `research/experiments/pal-foundations-v0/f1-results-v0.json` through `f12-results-v0.json`
- `research/experiments/pal-foundations-v0/f13-disposition-v0.json`

The page should be revised or narrowed when later prospective evidence contradicts any scoped conclusion. It does not authorize changes in Runtime, Host, Harness, World, Workstation, or domain owners.
