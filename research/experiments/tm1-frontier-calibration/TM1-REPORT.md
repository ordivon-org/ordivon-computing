# TM1 — Prospective Research Frontier Calibration Report

## Question

Does exposing a compact set of TM0 research-taste priors to the same Agent improve prospective research-frontier selection and bounded discovery efficiency?

TM1 is the first prospective test after the retrospective TM0 audit. The candidate frontier, actionability classes, Harness source revision, discovery budget, and hidden localization oracle were frozen before accepted live results.

## Frozen design

The exact frontier is `frontier-v1.json`. It contains seven real owner questions from Harness, Runtime, Host, Security, Finance, and Game. The predeclared Computing-campaign actionability classes were hidden from the Provider:

- class A: `H-NOTOOL`, `S-UNKNOWN` — immediate bounded reversible owner-native falsifiers;
- class B: `H-DISCOVERY`, `HOST-PKG` — useful but less direct/larger evidence paths;
- class C: `R-WITNESS` — requires materially more complex privileged physical experimentation;
- class D: `F-LIVE`, `G-HUMAN` — consequence-heavy or externally blocked for this Computing campaign.

Two treatments used the same `deepseek-v4-flash` model:

- **baseline:** ordinary bounded research-selection/discovery instruction;
- **taste:** identical instruction plus six compact TM0 priors about burden, discriminating falsifiers, closed-loop cost, reversibility, information selection, and lawful stopping.

Stage A ranked the frozen frontier. Stage B used exact Harness revision `999d7535242b14c432cd14527ec109f2c6749969` and a read-only search/read/submit surface to investigate the real `H-NOTOOL` owner pressure.

The Stage-B hidden evaluator required localization of the interaction between `ordivon/loop.py` conclusion-correction state binding and `ordivon/sqlite_agent_bridge.py` no-Tool state admission. It scored causal localization, not patch correctness.

## Apparatus correction history

Several pre-result canaries were explicitly excluded from scientific evidence. They exposed Provider-surface assumptions in the first direct runner: JSON-object output was not the current owner-native DeepSeek contract; the Provider may emit parallel Tool calls; action batches must be counted by observations rather than assumed one-call-per-turn; and exhausting an observation budget without submission is a legitimate forced-abstention outcome rather than a runner crash.

A protocol-freeze canary then completed successfully. Its result was not admitted to the main campaign because it occurred before the final predeclared three-replicate run.

The first full v1 campaign was also excluded after a `RemoteDisconnected` terminated the script before a durable campaign receipt. That failure independently reproduced an existing Computing method lesson: **experiment-step truth is not terminal script success**.

Apparatus v2 changed no frontier card, treatment prompt, evaluator, scoring rule, or observation budget. It added only:

1. atomic per-replicate progress records with exact treatment/replicate identity;
2. one identical retry for a read-only Provider transport failure.

The first v2 attempt persisted all six Stage-A ranking replicates before a later `BrokenPipeError`. The transport exception class was completed to include the same connection-failure family, and the identical `tm1-live-v2` campaign resumed from those exact durable records rather than re-dispatching them.

## Accepted evidence

Accepted receipt: `evidence/tm1-live-v2.json`.

Receipt digest:

`sha256:232385508a6b8f934911c211c0ff71129ff0bd29361393fac8af4a1b1d705c3b`

The corresponding per-replicate records are under `evidence/tm1-live-v2-progress/`.

### Stage A — frontier selection

| Measure | Baseline | Taste |
|---|---:|---:|
| Top choice is class A | 3/3 | 3/3 |
| Both class-A questions in top 3 | 2/3 | 0/3 |
| Both class-D questions explicitly deferred | 3/3 | 3/3 |
| A class-D question appears in top 2 | 0/3 | 1/3 |
| Provider tokens | 4,598 | 5,080 |

Every replicate in both treatments selected `H-NOTOOL` first. The added taste representation therefore did not improve the most important top-choice decision. It degraded secondary frontier ordering: it never placed both immediate class-A questions in the first three and once promoted the real-capital `F-LIVE` question to second place despite this Computing campaign lacking the relevant effect authority.

Stage-A taste used about 10.5% more Provider tokens.

### Stage B — Harness discovery

| Measure | Baseline | Taste |
|---|---:|---:|
| Replicates | 3 | 3 |
| Causal submissions | 2/3 | 0/3 |
| Forced budget abstentions | 1/3 | 3/3 |
| Scores | 6, 0, 4 | 0, 0, 0 |
| Mean score / 6 | 3.33 | 0.00 |
| Mean observations | 10 | 10 |
| Mean observed bytes | 43,065 | 38,943 |
| Provider tokens | 346,776 | 512,761 |

The taste condition consumed about 9.6% fewer source bytes but approximately **47.9% more Provider tokens**. Lower byte exposure therefore did not translate into better research efficiency.

Baseline replicate 1 localized both required source files and the full causal interaction, scoring 6/6. Baseline replicate 3 localized the conclusion-correction state-binding path but missed the exact no-Tool bridge file, scoring 4/6. Baseline replicate 2 exhausted the budget without a justified submission.

All three taste replicates exhausted the complete ten-observation budget without submitting a causal target. Their searches were not empty or nonsensical: they inspected conclusion correction, `MODEL_CORRECTABLE`, `conclusion_rejected`, `bind_run_state`, Tool errors, runtime lowering, and no-Tool surfaces. The failure was that the added meta-priors did not turn those observations into an earlier frontier-changing decision.

This is a stronger negative result than “the taste prompt used more tokens.” It increased deliberative/search cost while reducing causal closure.

## Interpretation

### TM0 world-model priors are not equivalent to an operational taste representation

TM1 falsifies the implementation hypothesis:

```text
compact list of good research maxims
→ better research selection
```

for this model and consumer.

It does **not** individually falsify every TM0 prior. Several remain supported by the experiment itself: strong simpler baselines matter, more observation is not automatically better, closed-loop cost matters, lawful abstention matters, and research-step durability matters.

The correct world-model update is therefore:

```text
Representation of research taste
!=
research-taste competence
```

A model can repeat or receive correct methodological statements without those statements producing the right next observation, question transformation, or stopping decision.

### Static meta-instruction can create a research-performance layer

The taste treatment appears to have added a meta-deliberation burden. It searched many relevant concepts but failed to collapse them into a causal target before budget exhaustion. This is consistent with a failure mode in which high-level research principles become another representation to reason about rather than a policy that changes the geometry of search.

TM1 therefore rejects promoting `taste-priors-v0.json` as a default Agent prompt, system instruction, global research checklist, or scheduling policy.

### Research durability is part of tractability

The invalid v1 campaign is also evidence. A research loop that loses completed trials after one Provider/network failure has a much higher effective closed-loop cost. Atomic per-trial evidence was not merely operational cleanup; it changed whether a multi-replicate campaign was practically tractable.

This supports retaining experiment-step durability as research apparatus, while still not creating a new global research service.

## Disposition

- **Reject:** static TM0-prior prompt as the operational form of research taste.
- **Retain:** TM0 priors as research-world-model hypotheses, not default instructions.
- **Retain:** per-replicate durable experiment evidence and bounded transport recovery for long live campaigns.
- **Do not build:** Tractability Engine, ResearchTasteService, universal question scorer, scheduler, or Core rewrite.
- **Next falsifier:** test whether research taste is better represented as **operator / question-transformation selection**: use the evidence shape to choose a narrow classical observation operator before open-ended model search, and compare on a materially different Security holdout as well as the Harness pressure.

TM1 therefore moves the RSI question one level down. The important capability is not “know good research sayings.” It is: **given the current uncertainty and evidence surface, select an operation that cheaply changes what can be believed or done next.**
