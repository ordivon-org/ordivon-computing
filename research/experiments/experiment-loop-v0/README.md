# Experiment Loop v0

Status: P2 bounded cross-evidence-family self-reform closeout complete.

Current plan: `CEL-R4-007` in [`plan-v7.json`](plan-v7.json). Historical `plan-v1.json` remains the original B5-era design; v2–v7 retain the evidence-backed reform sequence rather than rewriting that history.

This Track R experiment now implements the smallest file/Git-backed Agent-led loop needed to test changes to Ordivon Computing's own research policy without creating a second Host, scheduler, model router, database, deployment authority, or self-modification service.

## What changed in P1

The original plan bound readiness to historical phase names:

```text
HHO-P1 status
→ HHR-R3/B5 status
→ CEL may begin
```

P1 found that chronology had become stale authority. Current P0 already supplied the actual capabilities CEL required while historical B5 remained blocked for a different frozen Provider contract. `plan-v2.json` therefore recompiles prerequisites into exact capability evidence: rebuildable evidence selection, independent Trial validity, repeated comparable Trials, negative-result retention, and isolated reversible candidate execution.

The minimal executable loop is [`cel.py`](cel.py). It owns research Campaign records and deterministic selection only. Owner-native facts, execution, verification, product state, merge, release, deployment, and public consequence remain with their existing owners.

## First-generation self-change

Campaign [`campaigns/cel-p1-selection-001/`](campaigns/cel-p1-selection-001/) tested one variable: whether every selection-eligible Trial must have Observation-plane completeness, or whether the exact Campaign may declare the evidence claims actually required for its question.

Using 25 retained P0-family trajectories, split deterministically into 20 development and 5 holdout cases:

- `observation_always_required_v1`: 18 false exclusions on development;
- `campaign_declared_evidence_v2`: 20/20 development correct, zero false inclusions/exclusions;
- frozen holdout: 5/5 correct, including an invalid budget-preflight diagnostic that remained rejected.

The research-local policy was promoted in `plan-v3.json`. A fresh Runtime Workspace then reverted the promotion revision and passed the prior 15 CEL tests plus `git diff --check`; the rollback Workspace was removed. The exact receipt is retained beside the Campaign.

## Second-generation self-change

The improved loop then drove Campaign [`campaigns/cel-p1-prerequisite-002/`](campaigns/cel-p1-prerequisite-002/) against its own prerequisite resolver.

Baseline `named_phase_status_v1` incorrectly blocked the current capability-complete state because historical HHO/HHR plans still carry B5-blocked status. Candidate `capability_evidence_v1` was evaluated against the current positive capability sets plus a complete leave-one-capability-out negative-control set:

- development: baseline 4/5 with one false block; candidate 5/5 with zero false-ready/false-block;
- holdout: candidate 2/2, correctly accepting the complete current set and rejecting the missing-`repeated_comparable_trials` control.

The second-generation policy was promoted in `plan-v4.json`, then independently reverted in a fresh Runtime Workspace. The first-generation state's 17 CEL tests and `git diff --check` passed after rollback. `plan-v5.json` records both generations and both rollback proofs.


## Third-generation cross-evidence-family self-change

P2 moved away from the P0 Provider/Trial corpus. Campaign [`campaigns/cel-p2-frontier-freshness-003/`](campaigns/cel-p2-frontier-freshness-003/) tested Computing's own world-model observation freshness across ten owner repositories. The syntax-only baseline marked six stale development observations current; `git_relation_freshness_v2` was 7/7 development and 3/3 frozen holdout with zero false-current/false-stale decisions. An independent rollback Workspace reverted the promotion and passed the preceding 26 CEL tests and world-model checker.

The resulting method is [`../../world-model-loop-v2.json`](../../world-model-loop-v2.json): historical observation validity and currentness are distinct, and owner revision movement creates review pressure rather than automatic shared-model change. This establishes transfer to a materially different evidence family, not open-ended RSI.

## Claim boundary

P1 establishes **bounded recursive self-improvement evidence** in Computer research policy:

```text
retained evidence
→ first policy candidate
→ independent development/holdout evaluation
→ reversible promotion
→ rollback proof
→ improved loop selects a second change to itself
→ second independent holdout
→ second rollback proof
```

It does **not** establish open-ended RSI, autonomous general capability growth, unrestricted recursive mutation, or product authority. A materially different self-change or owner-native workload is required before broadening the claim.

The proposed generic World-Model return-edge driver is rejected for now. The current file/Git CEL plus owner-native Runtime/Host tools already executed the return/recompile edge end-to-end; another generic driver would duplicate orchestration without a demonstrated unowned responsibility.

## Key files

- [`plan-v1.json`](plan-v1.json) — historical B5-era design;
- [`plan-v2.json`](plan-v2.json) — capability-evidence prerequisite recompilation and minimal self-customer frontier;
- [`plan-v3.json`](plan-v3.json) — first-generation selection policy promotion;
- [`plan-v4.json`](plan-v4.json) — second-generation prerequisite-policy promotion before rollback proof;
- [`plan-v5.json`](plan-v5.json) — P1 closeout plan with both P1 rollback proofs;
- [`plan-v7.json`](plan-v7.json) — current P2 plan with third-generation cross-evidence transfer and rollback;
- [`p2-bounded-rsi-closeout.json`](p2-bounded-rsi-closeout.json) — machine-readable P2 claim boundary;
- [`recompile-receipt-v2.json`](recompile-receipt-v2.json) — exact old→new prerequisite decision;
- [`p1-bounded-rsi-closeout.json`](p1-bounded-rsi-closeout.json) — machine-readable P1 claim boundary and evidence index;
- [`cel.py`](cel.py) — minimal file-backed record, eligibility, evaluation, and deterministic selection logic;
- [`build_p0_policy_corpus.py`](build_p0_policy_corpus.py) — derives the 25-case P0 evidence corpus without copying mutable owner truth;
- [`run_selection_self_customer.py`](run_selection_self_customer.py) — first-generation self-change Campaign;
- [`run_prerequisite_self_change.py`](run_prerequisite_self_change.py) — second-generation self-change Campaign;
- [`tests/`](tests/) — historical plan guards plus P1 self-change evidence checks.

No daemon, database, scheduler, new repository, automatic merge/deploy, or World Model Round 002 was admitted by P1.
