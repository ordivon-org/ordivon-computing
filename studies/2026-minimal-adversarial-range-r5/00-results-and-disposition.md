# 00 — Results and Disposition

## Deterministic result

The immutable result is:

[`../../research/experiments/adversarial-range-r5/evidence/deterministic-range.json`](../../research/experiments/adversarial-range-r5/evidence/deterministic-range.json)

```text
source revision
  7042c38b24fba72a985101e55a281cc31d7cbb70

result digest
  sha256:a49ef33e079e5476f908ce190065319a57c8fe7f5a9de327028f0395858ec1e3

Trials
  176

passed retained/benign outcomes
  91

failed unsafe baselines
  85

invalid Trials
  0

reset proofs
  176 / 176
```

The 85 failures are intended unsafe-baseline failures, not infrastructure errors.

## Agent hijacking

| Variant | Accepted | Unauthorized objective successes |
|---|---:|---:|
| model-only-open | 0/24 | 24 |
| model-only-safe | 5/24 | 19 |
| static-filter-safe | 4/24 | 20 |
| Host provenance/effect gate | 24/24 | 0 |

Interpretation:

- model safety materially changes measured risk;
- one safety profile does not prove universal absence;
- a static marker filter does not cover the semantic attack family;
- constraining the action/authority boundary can preserve utility even when
  model proposal behavior is imperfect.

## Response loss

| Variant | Accepted | Duplicate Effects |
|---|---:|---:|
| blind retry | 0/8 | 8 |
| layered retries | 0/8 | 24 |
| provider idempotency | 8/8 | 0 |
| Host `UNKNOWN` + reconcile | 8/8 | 0 |

Interpretation:

- communication ambiguity is sufficient to create duplicate durable Effects;
- hidden retry layers multiply consequence;
- provider-native idempotency is a strong, simpler baseline;
- Host reconciliation is required where current provider state must be learned
  before redispatch.

## Interpretation differential

| Variant | Accepted | Unauthorized private Effects |
|---|---:|---:|
| front-first / backend-last | 6/12 | 6 |
| shared-last policy | 12/12 | 0 |
| strict duplicate rejection | 12/12 | 0 |
| typed reserialization | 12/12 | 0 |

Interpretation:

- front/backend disagreement converts a public policy decision into a private
  execution result;
- parser alignment, strict rejection, or typed reserialization removes the
  demonstrated abstract differential;
- R5 does not justify a universal normalizer.

## External contract evidence

The machine-readable observation is:

[`../../research/experiments/adversarial-range-r5/evidence/external-contract-observation.json`](../../research/experiments/adversarial-range-r5/evidence/external-contract-observation.json)

It binds 26 passing existing Host/Game tests and records the initial Python
environment error separately from contract outcomes.

## Architecture decision

```text
retain existing thin contracts
localize range orchestration and attack corpus
reject new permanent Security platform
continue only through real-model transfer falsification
```

No production repository mutation was required for R5.
