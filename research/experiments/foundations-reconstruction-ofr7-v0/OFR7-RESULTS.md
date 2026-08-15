# OFR7 Results — Fresh-Agent Practical Transfer

## Frozen question

Does the post-OFR6 Core + Knowledge surface improve fresh-Agent decisions over a strong pre-OFR6 surface and a strong direct-facts baseline, without losing more in Context/realization cost than it gains?

## Primary holdout

The holdout contained **20 untouched cases × 2 model capacities × 4 treatments = 160 generation trials**, followed by 20 treatment-blind judge calls. Primary evidence was not replaced by retries.

| Treatment | Physical valid | Primary accuracy | Causal score | Authority confusion | Mean prompt tokens | Mean cache-miss tokens |
|---|---:|---:|---:|---:|---:|---:|
| DIRECT | 1.000 | 1.000 | 1.000 | 0.000 | 1327.8 | 179.0 |
| PRE_OFR6_FULL | 1.000 | 1.000 | 1.000 | 0.000 | 9531.8 | 623.0 |
| POST_OFR6_FULL | 1.000 | 1.000 | 1.000 | 0.000 | 10596.8 | 891.2 |
| POST_OFR6_FOCUSED | 0.975 | 0.975 | 0.9625 | 0.000 | 5400.8 | 588.0 |

### The central result

```text
POST_OFR6_FULL - PRE_OFR6_FULL
primary = 0.0000
causal  = 0.0000
paired corrections = 0
paired regressions = 0
```

The frozen marginal-support rule is therefore **not met**. This is a ceiling/non-identification result: the pre-OFR6 surface was already perfect on primary and causal decisions, so OFR7 cannot attribute additional decision value to the OFR6 wording.

More strongly, `DIRECT` also reached 1.0 primary and 1.0 causal accuracy. The immediate case facts already exposed the decisive owner/currentness/identity/option/negative-transfer distinctions. On this workload class, the shared doctrine was not needed to reconstruct the answer.

## Cost and Context pressure

`POST_OFR6_FULL` consumed **7.98×** the mean prompt footprint of `DIRECT`; even counting only provider cache-miss tokens it remained **4.98×**. Prefix caching therefore softens repeated provider cost but does not erase Context occupancy, request-token admission, or cold-path burden.

`POST_OFR6_FOCUSED` reduced prompt footprint to **51.0%** of POST_FULL. It formally passes the preregistered aggregate Focused-vs-Full qualification, but it does **not** earn default promotion because DIRECT is both smaller and stronger on this corpus.

## Focused realization failure

The one primary physical failure was:

```text
OFR7-H-M16-02
POST_OFR6_FOCUSED
deepseek-v4-flash
stopCode = no_progress
providerAttempts = 1
```

Three exact post-holdout diagnostic retries all completed and chose the correct option. This supports stochastic structured-result realization rather than deterministic semantic omission, but the original failure remains in the primary score.

## Family dispositions

- **C2 UNKNOWN** — retain Core; not falsified, but PRE/DIRECT ceiling means OFR7 adds no identifiable marginal decision benefit.
- **C4 invariant-bound identity** — same disposition.
- **C10 option value** — retain Knowledge; ceiling, no POST_FULL regression.
- **M13 negative causal history** — retain Knowledge; ceiling. POST_FULL also removed the one PRE blinded unsupported-inference flag, but that flag is secondary because the treatment-blind judge could not see which general doctrine was supplied.
- **M16 mechanical projection** — retain Knowledge; POST_FULL ceiling. Focused has one original realization failure, not a demonstrated semantic-selection failure.
- **M17 receiver-conditioned compression** — **strengthened** by the treatment economics: more doctrine was not more useful here, and smaller Context was valuable only while fidelity/reliability survived.

## Practical architecture conclusion

```text
owner-current facts sufficient
→ send owner-current facts directly

causal distinction missing / ambiguous / transfer required
→ load the smallest relevant Foundation / Knowledge / owner evidence

never:
full world-model doctrine by default merely because it exists
```

This is a Context-selection result, not a claim that Foundations have zero research or architectural value.
