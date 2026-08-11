# HP0–HP2 — High-Pressure Operator Transfer and Research Stopping

## Executive result

HP0–HP2 tested the current Research Frontier Model (RFM) on two fresh owner-native pressures that were not primary workloads in TM1–TM3. The campaign deliberately used **elastic/high model budgets**: total token minimization was not an objective. The experiment asked whether additional compute was converted into owner-correct causal closure and whether an Agent could stop when another observation no longer had decision-changing value.

The main findings are:

1. **RFM1 transfers.** On a fresh localized Host packaging/dependency pressure, deterministic evidence compilation plus one semantic synthesis was 3/3 successful and more stable than open search. This is new OOD support for the localized-diagnostic/operator prior.
2. **RFM2 remains conditional.** On a fresh Runtime distributed execution/admission/materialization pressure, adaptive relation-following improved mean causal score relative to open search, and the deliberately compiled wrong operator false-stopped 3/3. But the selected adaptive policy was only 1/3 successful. Distributed relation-following is useful here; the current policy is not yet robust.
3. **The tested stopping implementation is falsified.** Requiring the Agent before every observation to name live alternatives, a current decision, a discriminator and a predicted decision change did not cause early stopping. Every accepted HP2 cell consumed the full 32/32 physical observation ceiling.
4. **Explicit marginal-value narration can improve research quality without producing stopping.** Host success improved from 2/3 to 3/3 and Runtime mean score improved slightly, but observation count did not fall at all. On Host it also consumed more Provider tokens than the high-budget open baseline.
5. **Research efficiency cannot be scalarized before semantic acceptance.** The Runtime compiled wrong-operator cell was extremely cheap and therefore looked excellent under score-per-token, yet it false-stopped 3/3 and never crossed the success threshold. Cheap wrong research is not efficient research.
6. **Available budget is capacity, not evidence obligation.** Several high-budget trials saw required-file evidence almost immediately and nevertheless continued for 22–31 more physical observations. Giving more compute does not imply that the compute should be exhausted.
7. **Research discipline semantics must be separated from wire representation.** The first verbose HP2 stopping audit repeatedly destabilized DeepSeek Tool JSON serialization. A shorter representation preserved the same semantic commitments and restored valid execution. The representation cost of a method is part of its tractability.

An independent concurrent Game RF1 campaign reached the same stopping conclusion on a materially different temporal-evidence workload: its serial progressive Agent consumed all 6/6 windows on 8/8 trajectories, agreed with unanimous full-evidence references only 6/8, and cost roughly 2.3× the Provider tokens of a one-shot full-evidence comparator. HP2 and RF1 therefore converge on the same negative result without sharing the primary workloads.

## HP0 — frozen OOD battlefield

The battlefield was frozen before accepted live HP1/HP2 results.

- Computing experiment base: `dfb75f6546f1af8d17be10a469000bb69b1c1f3f`
- Host owner revision: `6495822162c69179e8ad4f8a0d79cc42902ff599`
- Runtime owner revision: `501941a0b9cbcb9f13d8e34d8f9b53c8e86f7f41`
- Battlefield digest: `sha256:a69608172fa3d8ca61841afd92c138436fe7fd068fbf91ff394dd7b93a1ce024`

### H-PACKAGE — localized packaging/dependency topology

Real pressure: a World consumer passed the focused Host semantic boundary while installing/upgrading the Host distribution expanded the Python lock graph from 9 to 34 packages. The hidden owner oracle required localization of the unconditional `mcp==2.0.0` project dependency together with the separate `ordivon-host-mcp` server entrypoint / MCP SDK import carrier. Semantic compatibility with World was explicitly not the current failure.

RFM hypothesis:

```text
localized exact packaging evidence
→ literal identity-preserving search
→ bounded local reads
→ deterministic evidence compilation
→ one semantic synthesis
```

### R-WININPUT — distributed execution/admission/materialization topology

Real pressure: a cross-target World trajectory preserved source/effect references across `local_linux → windows_native`, while direct `workspace.execBound` Windows admission remained unavailable. The hidden owner oracle bound the public Tool path, Core input-bound admission/profile checks, immutable-input presentation semantics, Windows dispatch, and existing-Job replay ordering.

RFM hypothesis:

```text
initial exact owner anchors
→ adaptive semantic relation following
→ request binding
→ admission/profile validation
→ immutable-input presentation
→ Windows dispatch
```

The wrong control deliberately used deterministic compiled evidence for this distributed relation.

## Budget semantics

The campaign did **not** optimize minimum total tokens. Per accepted adaptive trial the Agent could consume up to 24 physical observations in HP1 and 32 in HP2, with up to 8,000 completion tokens per Provider call. The purpose was to distinguish:

```text
more available compute
from
more useful research
```

The semantic ordering used in interpretation is:

1. owner-correct / authority-safe outcome;
2. no false stop / no false action;
3. causal and frontier closure;
4. only then evidence/model cost and token utilization.

No scalar cost metric is allowed to reverse that order.

## HP1 — operator transfer

Accepted receipt: `evidence/hp1-live-v1.json`.

### H-PACKAGE

| Treatment | Success | Mean score | Obs / rep | Provider calls | Total tokens |
|---|---:|---:|---:|---:|---:|
| Open Agent | 2/3 | 3.67 / 6 | 24 | 72 | 2,139,701 |
| RFM-selected compiled | **3/3** | **5.33 / 6** | 16 | **3** | **108,832** |
| Wrong distributed/adaptive | 2/3 | 5.00 / 6 | 24 | 38 | 812,458 |

The strongest open failure consumed 24 observations, 40 Provider calls and 1,368,700 tokens, despite the first observation already surfacing both required-file paths; it still reached only a forced abstention.

The selected compiled policy was not merely cheaper. It was also the only 3/3-success treatment and had the highest mean semantic score. This is fresh OOD support for **RFM1**.

The wrong adaptive policy often recovered the answer, so the result does not imply adaptive investigation is incapable of solving a local problem. It implies that, for this evidence topology, adaptive search adds large recurring closed-loop cost without improving the accepted result over deterministic compilation.

## R-WININPUT

| Treatment | Success | Mean score | Obs / rep | Provider calls | Total tokens |
|---|---:|---:|---:|---:|---:|
| Open Agent | 1/3 | 2.33 / 7 | 24 | 97 | 3,183,045 |
| RFM-selected adaptive | 1/3 | **4.67 / 7** | 24 | 57 | 1,391,206 |
| Wrong compiled one-shot | **0/3** | 4.00 / 7 | 11 | 3 | 114,854 |

The selected adaptive policy improved relation reconstruction: its mean score was materially above open search, and one trial recovered all five causal concepts needed by the oracle. The compiled wrong operator was inexpensive but **false-stopped 3/3**.

This supports the direction of RFM2 while narrowing its confidence. The current claim is not:

```text
distributed topology → adaptive Agent succeeds
```

It is only:

```text
for this distributed owner relation,
mechanical compilation loses decision-critical relational structure,
while adaptive relation-following can recover more of it;
the current adaptive policy remains unstable.
```

A striking measurement failure appears here. The compiled wrong treatment had a much better raw score-per-token ratio than the accepted adaptive treatment, yet it never produced a semantically acceptable result. Therefore:

> **Research efficiency cannot be scalarized before semantic acceptance.**

## HP2 — marginal-value stopping

Accepted receipt: `evidence/hp2-live-v1.json`.

The candidate stopping policy required, before every new observation, an explicit compact account of:

- live alternatives;
- current causal decision;
- why this observation discriminates those alternatives;
- what result would change the decision.

Submission additionally required the remaining affordable discriminator, if any, and a stop reason.

It was explicitly told:

> Stop only when no affordable observation can be named that is expected to change the causal decision; confidence alone is not a stop rule.

### Result

| Workload | Treatment | Success | Mean score | Mean observations | Total tokens |
|---|---|---:|---:|---:|---:|
| H-PACKAGE | High-budget open | 2/3 | 4.33 / 6 | **32 / 32** | 1,474,253 |
| H-PACKAGE | Marginal-value audit | **3/3** | **5.33 / 6** | **32 / 32** | 2,216,341 |
| R-WININPUT | High-budget open | 2/3 | 5.67 / 7 | **32 / 32** | 2,404,262 |
| R-WININPUT | Marginal-value audit | 2/3 | **6.00 / 7** | **32 / 32** | 2,193,384 |

No accepted treatment cell reduced physical evidence acquisition by a single observation on average.

Required-file coverage occurred extremely early:

- H-PACKAGE: observation 1 in every HP2 replicate, followed by 31 more observations;
- R-WININPUT: observation 2 in every HP2 replicate, followed by 30 more observations.

Required-file coverage alone is not a stopping oracle, but these numbers demonstrate how much room remained for a stopping mechanism to prove value. The tested mechanism did not use that room.

### What the candidate actually did

It acted more like a **research-quality audit** than a stopping mechanism:

- Host success improved 2/3 → 3/3;
- Host mean score improved 4.33 → 5.33;
- Runtime mean score improved 5.67 → 6.00;
- Runtime success remained 2/3.

On Host, those gains cost more Provider tokens than the open baseline. Under the user-approved high-budget regime that is not itself a failure: additional compute is allowed when it buys better evidence. The failure is narrower and more important:

> the additional compute bought some quality, but **did not buy stopping**.

So HP2 falsifies this implementation hypothesis:

```text
serial per-observation marginal-value narration
→ autonomous stopping competence
```

It does not falsify the need for stopping itself.

## Apparatus failures were retained as method evidence

HP2 experienced multiple Provider-surface failures before the first valid marginal sample and later between durable replicates. None was rescored as a scientific outcome.

### Verbose structured audit destabilized Tool JSON

The original long field representation repeatedly produced malformed function arguments. Raw captured responses showed a stable pattern such as:

```text
"whyThisObservationDiscriminates": pyproject.toml is the direct declaration...
```

The value was emitted as bare text rather than a JSON string. The response was not executed.

A minimal canary proved the schema family was supported in principle. The accepted mechanical correction preserved the same semantic commitments but shortened the wire representation to fields such as `alts`, `decision`, `discriminator`, and `decisionChange`.

This adds a research-tractability law:

> **Semantic discipline is not the same thing as its wire representation.**

A methodology whose representation creates Provider serialization failure has imposed a real closed-loop cost even if its abstract rule is sensible.

### Out-of-catalog Tool output failed closed

A later Provider response named a Tool outside the exact offered `search/read/submit` catalog. The runner rejected it before execution. The adapter was then mechanically hardened to treat out-of-catalog Tool names as invalid Provider turns eligible only for bounded identical retry. It never aliased the Tool, expanded authority, or interpreted the response as a semantic action.

These failures independently support durable per-replicate progress: already accepted trials survived script/Provider failure and were not re-dispatched.

## Independent Game RF1 comparison

While HP0–HP2 ran, a separate Computing experiment used Game AF Loop trajectories and independently tested serial marginal-evidence stopping.

Canonical closeout after that campaign: `a6caa06936910847cdd3f594e1956396ab56551f`.

Its main result was materially consistent with HP2:

- 8/8 progressive trials consumed all 6/6 temporal windows;
- progressive agreed with unanimous 3× full-evidence references only 6/8;
- matched full one-shot evidence agreed 8/8;
- progressive used 406,388 Provider tokens versus 176,333 for matched one-shot, about 2.3×;
- equivalent eventual evidence sets could still yield different semantic decisions depending on acquisition/dialogue path.

RF1 therefore adds a second materially different negative result:

> repeatedly asking the same Agent whether another observation matters is not, by itself, stopping competence.

It also introduces **semantic path dependence** as a tractability variable.

## World-model update

### Retain / strengthen

**RFM1 — localized exact diagnostic/packaging topology.** Fresh Host OOD evidence supports deterministic identity-preserving retrieval, bounded compilation and one semantic synthesis when the causal neighborhood is sufficiently concentrated.

### Retain but narrow

**RFM2 — distributed representation/dataflow/execution topology.** Adaptive relation-following can recover causal relations that frequency-ranked compilation loses. However, fresh Runtime success was only 1/3. Treat RFM2 as an operator prior, not a reliable policy.

### Reject as stopping mechanism

**Serial per-observation Agent self-audit of marginal evidence value.** HP2 did not stop on either OOD workload; independent Game RF1 also did not stop on 8/8 finite trajectories.

### Do not reject as quality diagnostic

Explicit alternatives/discriminator accounting may still improve causal quality. It has not earned default use because it adds Provider/wire/context cost and did not prove stopping value.

### New stopping frontier

The next stopping hypothesis, if a natural workload earns it, should be materially different:

```text
large / expensive evidence universe
→ batched or non-serial marginal-value estimate
→ compare against strong full-inspection / compiled baseline
→ select / stop without paying one full Provider decision round per observation
```

Do **not** manufacture a large evidence universe merely to continue the experiment sequence.

### Budget law

```text
available budget != evidence obligation
```

A high token budget gives the Agent headroom to integrate difficult evidence. It is not a target that should be exhausted.

### Measurement law

Interpret research performance lexicographically:

```text
owner correctness / authority safety
→ false-stop / false-action control
→ causal and frontier closure
→ recurring evidence/model cost
```

A scalar score-per-token before semantic acceptance is invalid.

## Disposition

- **Retain:** HP1/HP2 final receipts and this bounded report as evidence.
- **Retain:** the exact frozen battlefield/experiment contract only while referenced by the current RFM calibration claim.
- **Archive in Git:** runner, per-replicate progress, malformed raw Provider payloads, correction scaffolding and transport diagnostics.
- **Reject:** ResearchStoppingService, ResearchTasteService, universal topology classifier, scheduler, query planner, default serial STOP loop, or global token-efficiency scalar.
- **No owner mutation:** Host and Runtime product fixes remain with their owners. HP0–HP2 produced only research evidence and next falsifiers.
- **Do not automatically start HP3:** first close and assimilate HP0–HP2 into current Computing reality; later topology-deception testing remains a separate frontier.
