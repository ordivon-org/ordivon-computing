# R5 Evidence Contract

## Deterministic range evidence

Generated file:

```text
evidence/deterministic-range.json
```

Required fields:

- exact experiment source revision;
- all 176 Trial records;
- per-variant acceptance and failure counts;
- model proposal and Host rejection observations;
- retry, duplicate, and reconciliation observations;
- front/backend interpretation observations;
- reset proof for every Trial;
- architecture disposition;
- canonical result digest.

The JSON and [`RESULTS.md`](RESULTS.md) must be regenerated from the same committed
source revision and compare byte-for-byte on repeated runs.

## Product contract observations

### Ordivon Host

Bound revision:

```text
fa313039cf2f7c9f8df445a8ccbfed8d9e06f3aa
```

Observed tests:

```text
test_context_provenance.py       4 passed
test_cognition_admission.py      7 passed
test_effect_lifecycle.py         1 passed
test_ordivon_harness_oh4.py      5 passed
```

Established relations:

- untrusted instruction remains explicitly labeled in Context provenance;
- source revision changes invalidate bound Context;
- a model-invented action outside the compiled candidate set is rejected;
- a stale World requirement is rejected;
- a completed Effect cannot be repeated;
- a new Effect is forbidden while a Dispatch is unresolved;
- response loss produces an uncertain state and fresh Host reconciliation
  observes the original Dispatch without redelivery;
- ToolGrant filters Tools, paths, execution checks, Jobs, and Artifacts;
- assignment, grant, trace, verification, and outcome survive fresh Host
  instances.

### Ordivon Game

Bound revision:

```text
7bf23579f822d412808d39197255fc4369b861c0
```

This is the local `origin/main` revision observed on 2026-08-01, tested in an
isolated detached Workspace rather than the local main branch that was 28 commits
behind.

Observed tests:

```text
world.test.ts                 3 passed
fault-injection.test.ts       2 passed
game-world-executor.test.ts   4 passed
```

Established relations:

- initial hidden World and resource ledgers satisfy invariants;
- invalid action does not mutate World;
- pre-commit fault leaves no partial Effect;
- after-commit fault is recovered by idempotent replay;
- committed Command can be observed after response loss without redelivery;
- absent Command observation is a pure lookup;
- Team Tick delivery/observation has no hidden retry;
- stale Commands produce typed rejection.

## Initial environment failure

The first Host test attempt used the system Python 3.14 and failed before running
because `anc_canonical` was not on `PYTHONPATH`. This was an environment/configuration
failure, not a contract failure.

The corrected run bound:

```text
Python 3.12.13
Host revision fa313039cf2f7c9f8df445a8ccbfed8d9e06f3aa
Ordivon Protocol source revision be5fe779267f0225dd37c570932c7d71ee5223a7
```

The machine-readable observation is
[`evidence/external-contract-observation.json`](evidence/external-contract-observation.json).

No dependencies were downloaded and no product repository was modified.

## Evidence limitations

- Host and Game tests establish contracts separately; the R5 deterministic
  simulator is not yet an end-to-end live product run.
- Agent hijacking profiles are synthetic and contain no real language model.
- The Game observation covers deterministic World and response-loss mechanics,
  not the final R5 hijacking scenario.
- No live Runtime, browser, Token, network path, or cloud provider is involved.
- A passing safety profile cannot establish universal attack absence.

These limitations define R6 rather than invalidating R5.
