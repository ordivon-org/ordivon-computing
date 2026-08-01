# R5 Minimal Owned Adversarial Range

Status: completed deterministic experiment and product-contract observation

## Purpose

R5 moves the R0–R4 Web/network adversarial research from standards and incident
reconstruction into one executable, owned, reversible range.

The governing question is:

> Can existing Host, Runtime, Game, provider-local World evidence, and independent
> verification express representative cross-layer failures without creating a
> permanent Security platform?

## Executable source

The implementation, experiment specification, immutable Trial evidence, external
Host/Game observations, results, and deletion decisions live in:

[`../../research/experiments/adversarial-range-r5/`](../../research/experiments/adversarial-range-r5/)

The executable range is bound to source revision:

```text
7042c38b24fba72a985101e55a281cc31d7cbb70
```

## Experiment families

```text
Agent hijacking
  4 variants × 24 seeds = 96 Trials

response loss and retry
  4 variants × 8 seeds = 32 Trials

interpretation differential
  4 variants × 12 seeds = 48 Trials

total
  176 deterministic Trials
```

All Effects are simulated, reversible, locally owned, and independently visible
to the experiment verifier. The parser case uses typed abstract values rather
than operational HTTP payloads.

## Main result

R5 retained the existing thin responsibilities:

- source provenance and trust labels;
- Host-compiled candidate admission;
- Assignment-scoped ToolGrant;
- stable Effect identity;
- explicit `UNKNOWN` and reconcile-before-redispatch;
- provider-native idempotency;
- strict ambiguity rejection or typed reserialization;
- independent World verification;
- exact reset and residual proof.

R5 did not earn:

- a universal `AttackChain` service;
- a central Agent-security policy engine;
- a generic cyber range;
- a new parser or network stack;
- a global World telemetry database.

## Safety-policy result

The synthetic safety profile reduced measured hijacking objective success from
24/24 to 19/24. This demonstrates that policy affects the configured system's
risk distribution. It does not prove lower-layer capability absence.

The Host provenance/candidate/Effect gate admitted zero unauthorized Effects in
24/24 Trials while preserving the authorized Effect in 24/24 Trials.

These are deterministic synthetic-policy results, not claims about a named real
model or Provider.

## Product contract observations

At exact external revisions:

```text
ordivon-host
  fa313039cf2f7c9f8df445a8ccbfed8d9e06f3aa
  17 relevant tests passed

ordivon-game
  7bf23579f822d412808d39197255fc4369b861c0
  9 relevant tests passed
```

These tests establish that the required provenance, admission, ToolGrant,
uncertain-delivery, reconciliation, hidden-World, idempotency, fault-injection,
and reset contracts already exist in the product repositories. They do not
constitute an end-to-end real-model security evaluation.

## R6 gate

R6 may replace synthetic policies with:

- real model and Provider profiles;
- held-out natural-language attacks;
- repeated adaptive attempts;
- deliberate Context loss;
- Host replacement;
- generated Tool availability;
- independent deterministic World verification.

R6 remains a transfer and falsification experiment. It must not begin by building
a larger Security platform.
