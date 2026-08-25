# S4A Closeout — Metamorphic Semantic Substrate

Status: **PASS after one substrate repair and one relation-precondition repair**.

## First run

100,000 generated random bases exposed two failures:

1. `MR6_TRANSIENT_CONTEST_CLEAR`: false positive caused by an invalid metamorphic precondition. The minimal base already contained live authority claims; the transformation's institution-wide `clear_claims` erased those pre-existing claims. The relation was therefore not semantics-preserving. Repair: apply MR6 only when the base has no existing authority claims.
2. `MR9_REPEAT_INVALIDATION_IDEMPOTENT`: genuine semantic substrate bug. Repeating `invalidate_sanction` changed a sanction from `INVALIDATED_LATER` to `INVALID`, rewriting the historical reason for invalidity. Remedy did not duplicate, so conventional state/reward checks would likely miss it.

## Semantic repair

`invalidate_sanction` now performs a state transition only when the sanction is currently `VALID`; later repeated review is a no-op for current standing and remedy, and does not reclassify historical invalidity.

## Regression before rerun

- Original S0 deterministic gates: all PASS.
- Original S0 50,000 random stress: 0 property violations; same aliasing summary (92 naive classes, 75 aliased classes, max 302 typed standings in one naive class).
- S2 deterministic cases: all PASS.
- S3 deterministic cases: all PASS.
- `cases-s2-v1.json` SHA-256 remained exactly `5c5ce762b1ed17f830032f42f00e666507a1db40c69443729dc43eabb4dff174`.
- `cases-s3-v1.json` SHA-256 remained exactly `5212f2efaa1e59be492f12b187af63818256d93d336df15c3182574a594cdb4b`.
- Therefore old S1-S3 provider/model evidence is not rescored or changed.

## Second S4A run

All 12 frozen metamorphic relations PASS.

Random-base relation checks:
- MR1 invalid-election insertion: 100,000
- MR2 redundant recovery: 79,542 applicable bases
- MR3 redundant root compromise: 24,972 applicable bases
- MR4 root-compromise order: 100,000
- MR5 claim order: 100,000
- MR6 transient contest + clear: 70,402 applicable bases
- MR11 election/control-transfer commutation: 92,496 applicable bases
- MR12 no-op physical tamper: 100,000

Fixed relation families MR7/MR8/MR9/MR10 all PASS after repair.

## Standing

S4A demonstrates why AIC cannot rely only on example-based correctness. A state machine that passed the earlier deterministic suite and 50k random stress still contained a history-standing rewrite bug detectable only through a relation such as repeated-operation idempotence.

S4A does not establish Agent robustness. It only freezes which semantic transformations are safe to use as metamorphic oracles in S4B.
