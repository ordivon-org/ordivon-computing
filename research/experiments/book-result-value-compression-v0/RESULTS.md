# Book Result / Achievement / Value Compression Falsifier — Results

Status: completed bounded experiment. **No Media Book mutation is admitted by these results.**

## 1. Question

The Book v0.5 integration audit found a specific asymmetry:

```text
fresh consumers can infer Result / Achievement / Improvement / Value / Consumption / RealizedBenefit decisions
!=
the Book explicitly presents the full compact Result/Value map
```

This experiment asked whether making that map explicit materially improves a fresh Agent beyond the exact current five-chapter Book.

The confirmatory decision was frozen before semantic runs:

> A correctness-motivated Book integration is earned only if the treatment produces a stable non-trivial improvement on difficult decisions where baseline repeatedly fails, without introducing conservative underclaim. A ceiling-level baseline is evidence against editing the Book for correctness.

## 2. Exact frozen inputs

Primary inputs:

- five-chapter Book SHA-256: `10ed267c4b4eb9d90bf8b45c65c73482d40aae2d91e7359cbeedaeac37bf782c`
- compact map SHA-256: `b3da56b021c973f4a6f1b49d19eb6c3d4039670894e11ff29416a600eb7304c2`
- primary cases SHA-256: `473d37460e55d52953e7f91233f6d1835c8b3b983ff50f02830bfe51c269655d`
- primary spec SHA-256: `5b94b8f9e81607a3ea246cb6b83b44c62b7d929c13584ed2ba8427631c1126a4`

Arms:

```text
BASELINE
= exact five-chapter Book -> frozen cases

TREATMENT_PREBOOK
= compact Result/Value map -> exact five-chapter Book -> identical frozen cases
```

The treatment map was deliberately placed before the long Book rather than next to the cases. Provider/model/settings, cases, completion schema, budgets and zero-Tool surface were otherwise matched.

## 3. Primary confirmatory result — no decision delta

The primary battery contained:

- 12 classification cases testing the strongest justified Result/Value standing;
- 10 transfer/action cases asking what to claim or do without relying only on taxonomy labels.

Accepted semantic Runs:

### Baseline

- `harness-run:book-resultvalue-v3-baseline-1-1787594298026`
- `harness-run:book-resultvalue-v3-baseline-2-1787594305050`
- `harness-run:book-resultvalue-v3-baseline-3-1787594311957`
- `harness-run:book-resultvalue-v3-baseline-4-1787594318583`
- `harness-run:book-resultvalue-v3-baseline-5-1787594325508`

### Treatment

- `harness-run:book-resultvalue-v3-treatment_prebook-1-1787594333287`
- `harness-run:book-resultvalue-v3-treatment_prebook-2-1787594340955`
- `harness-run:book-resultvalue-v3-treatment_prebook-3-1787594348656`
- `harness-run:book-resultvalue-v3-treatment_prebook-4-1787594356244`
- `harness-run:book-resultvalue-v4-treatment-replacement5-1787594408964`

Every accepted Run used one model call and zero Tools.

| Arm | Accepted Runs | Classification | Transfer/action | Total |
| --- | ---: | ---: | ---: | ---: |
| Book only | 5 | 60 / 60 | 50 / 50 | **110 / 110** |
| Map + Book | 5 | 60 / 60 | 50 / 50 | **110 / 110** |

Therefore:

```text
PrimaryAccuracyDelta = 0
```

This is not a conservative-denial ceiling. The Book-only arm correctly admitted positive claims including:

- `ObjectiveAchievement` without downstream use when the declared objective was genuinely closed;
- `DiscoveryAchievement` when an original objective failed but an independently supported consequential discovery emerged;
- bounded `Improvement` without global optimality;
- bounded `Optimality` inside a fully declared finite envelope;
- bounded `RealizedBenefit` for a named beneficiary/horizon with adequate attribution;
- `ProspectiveValue` without consumption;
- a successful decision objective whose correct disposition is `NO_OP`;
- successful epistemic apparatus while the investigated hypothesis remains unknown.

All ten accepted Runs also recovered all six requested meta-distinctions:

```text
Completion != Achievement != Consumption
Consumption != Benefit
PositiveAchievementWithoutDownstreamUse = allowed when supported
BoundedImprovementWithoutOptimality = allowed
BoundedOptimalityWithoutGlobalOptimality = allowed
MaterializeToLearn != DeployConclusion
```

### Context cost

Baseline prompt tokens were exactly `24,054` per accepted run. Treatment prompt tokens were `24,830` per accepted run:

```text
TreatmentPromptOverhead = +776 tokens/run
```

Mean total tokens:

- baseline: `24,794.8`
- treatment: `25,568.2`

approximately `+3.12%` treatment total-token overhead with zero accuracy gain.

### Weak-case signal

Self-reported weak-case flags:

- baseline: `9`
- treatment: `12`

This signal is not calibrated enough to claim the treatment is worse, but it supplies no evidence that the explicit map reduced uncertainty.

## 4. Carrier failures excluded from semantic statistics

Three carrier episodes must not be collapsed into model correctness:

1. the initial runner attempted to read a nonexistent `AgentLoopResult.conclusion_corrections` attribute after the first provider return and crashed before recording an accepted result;
2. the next attempt correctly failed closed because a new Harness Run ID reused an already-bound `caller_run_ref`;
3. primary treatment replicate 5, `harness-run:book-resultvalue-v3-treatment_prebook-5-1787594363995`, ended `budget_exhausted` after one structured-conclusion correction and produced no decodable semantic conclusion.

The third episode was replaced with the same frozen semantic inputs by `harness-run:book-resultvalue-v4-treatment-replacement5-1787594408964`, which scored 22/22. The excluded run is carrier evidence only; it is neither a semantic success nor semantic failure.

## 5. Confirmatory admission decision

The predeclared rule resolves the core question:

```text
ExplicitMapAbsent
!=
FreshAgentDecisionCapabilityAbsent
```

and:

```text
BookImplicitCompressionDebt
!=
BookCorrectnessDebt
```

For fresh `deepseek-v4-flash` consumers under this workload, the five-chapter Book already generates the relevant decision boundaries. The explicit taxonomy therefore **does not earn a Book edit as an Agent-correctness repair**.

Current disposition:

```text
Five-chapter Book core                 = NO_CHANGE
Result/Value correctness repair        = NOT_ADMITTED
Chapter 6: Result / Value              = NOT_ADMITTED
Compact map as research reference      = RETAIN
Human readability/retention claim      = UNTESTED
```

## 6. Post-primary exploratory ceiling challenge

After the primary baseline reached 22/22 in all five replicates, a legitimate alternative explanation remained:

> Perhaps single-answer cases make correct decisions easy while hiding difficulty reconstructing the complete orthogonal Result relation.

A multi-label follow-up was therefore designed **after** the confirmatory result. Its exploratory status was frozen before its own runs and cannot retroactively change the primary admission rule.

Follow-up frozen inputs:

- composite cases SHA-256: `2b2eeb5f27b637e0e36d9c84983185b04ada98000c653f4c0a697edd851b7671`
- follow-up spec SHA-256: `f2a93f732f31a7f99d424862161f4869a65f3bdc39dd4c0f148329be779802d6`

Each of eight cases required the complete set of justified labels from:

```text
COMPLETED
OUTPUT
OBJECTIVE_ACHIEVEMENT
DISCOVERY_ACHIEVEMENT
BOUNDED_IMPROVEMENT
BOUNDED_OPTIMALITY
PROSPECTIVE_VALUE
CONSUMPTION
REALIZED_BENEFIT
```

Overclaim and underclaim both counted as errors.

Accepted Runs:

### Baseline

- `harness-run:book-resultvalue-followup-baseline-1-1787619782696`
- `harness-run:book-resultvalue-followup-baseline-2-1787619792830`
- `harness-run:book-resultvalue-followup-baseline-3-1787619801480`

### Treatment

- `harness-run:book-resultvalue-followup-treatment_prebook-1-1787619808488`
- `harness-run:book-resultvalue-followup-treatment_prebook-2-1787619816701`
- `harness-run:book-resultvalue-followup-treatment_prebook-3-1787619823576`

Results:

| Arm | Exact composite cases | Label errors |
| --- | ---: | ---: |
| Book only | 10 / 24 | **28** |
| Map + Book | 12 / 24 | **14** |

The treatment therefore halved total label errors in this exploratory reconstruction workload.

Baseline error breakdown:

- extra `COMPLETED`: 12
- extra `OBJECTIVE_ACHIEVEMENT`: 7
- extra `BOUNDED_OPTIMALITY`: 2
- extra `PROSPECTIVE_VALUE`: 2
- missing `BOUNDED_IMPROVEMENT`: 4
- missing `CONSUMPTION`: 1

Treatment error breakdown:

- extra `COMPLETED`: 12
- extra `OBJECTIVE_ACHIEVEMENT`: 2

The explicit map eliminated the observed missing `BOUNDED_IMPROVEMENT` and `CONSUMPTION` errors and the extra `BOUNDED_OPTIMALITY` / `PROSPECTIVE_VALUE` errors in these three treatment runs, while reducing extra `OBJECTIVE_ACHIEVEMENT` from seven to two. It did **not** solve the repeated tendency to infer `COMPLETED` from an existing/produced artifact when lifecycle completion was not explicitly stated.

The exact-case gain (`10/24 -> 12/24`) is modest because the shared `COMPLETED` over-inference prevents several otherwise-correct treatment sets from becoming exact matches. The label-error reduction is the stronger exploratory signal.

Mean total tokens:

- baseline: `22,811.3`
- treatment: `23,575.0`

Again the treatment carries context cost.

## 7. Joint interpretation

The confirmatory and exploratory results are compatible:

```text
Immediate strongest-justified decision
    Book only = already at ceiling

Complete explicit relation reconstruction
    Map + Book = fewer composition errors in exploratory test
```

So the mature standing is not either extreme:

```text
"The map must enter Book because it is explicit"        // rejected
"The map has no representational value because accuracy tied" // rejected
```

Instead:

```text
Decision repair value:                NOT_DEMONSTRATED / primary negative
Explicit reconstruction value:        DEMONSTRATED in bounded exploratory Agent workload
Human pedagogical/retention value:     UNKNOWN
Ordinary-path environmentalization:    NOT_EARNED
```

## 8. Representation destination

The narrowest truthful destination is **Computing research evidence plus Atlas/Computing recovery**, not a Media core mutation.

Why not Chapter 3/5 now?

- primary action/decision transfer has no deficit to repair;
- explicit treatment adds recurring context cost;
- exploratory reconstruction improvement does not establish that every Book consumer needs the taxonomy by default;
- no Human continuous-reading, retention or delayed-transfer evidence exists;
- the full map remains a derived cross-cutting compression over principles the Book already generates.

Why retain it visibly?

- it materially improves complete relation reconstruction in the exploratory workload;
- it reduces future rediscovery risk for result audits and portfolio/value investigations;
- it gives a bounded reusable reference when the operation explicitly requires classifying many simultaneous Result relations.

Therefore:

```text
Book core default context                 = NO_CHANGE
Computing experiment / first-look recovery = ADMIT
Atlas historical synthesis                = RETAIN
Operation-specific Result audit reference  = JUSTIFIED
Universal default injection                = NOT_EARNED
Chapter 6                                  = NOT_ADMITTED
```

A future Media representation should reopen only if a named consumer demonstrates one of:

- Human comprehension/retention/transfer improvement from the explicit map;
- a lower-capability or long-delay Agent repeatedly loses these relations without it;
- a natural Result/value audit workload shows consequential reconstruction errors that the compact map prevents;
- an operation-specific Book companion can expose the map only when relevant without charging every consumer its context cost.

## 9. Bottom line

The experiment changes the Book-v0.5 audit's previous frontier in a precise way.

Before:

```text
Result/Value compact integration = strongest targeted Book revision candidate
```

After confirmatory + exploratory pressure:

```text
Result/Value core Book integration
    = not admitted as Agent correctness repair

Result/Value compact representation
    = retained as an operation-specific reconstruction aid
      with bounded exploratory evidence

Next Book pressure
    = not "which concept is missing?"
      but "which representation materially improves the target consumer over time?"
```

This is a successful negative admission result: the research became persistent and discoverable without making the Book larger merely because a richer taxonomy exists.
