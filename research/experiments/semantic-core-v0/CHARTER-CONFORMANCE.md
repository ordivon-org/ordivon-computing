# Kernel Charter Conformance v0

## Status vocabulary

- **PROVEN-v0** — executable deterministic tests exist.
- **PROVEN-v0 + live** — deterministic tests and real Ordivon execution evidence exist.

## Guarantee matrix

| ID | Guarantee | Status | Canonical executable evidence |
|---|---|---|---|
| K1 | stable semantic identity | PROVEN-v0 | `test_k1_identity_survives_journal_restart` |
| K2 | Effect/Dispatch separation | PROVEN-v0 | `test_k2_dispatch_identity_cannot_cross_effects` |
| K3 | explicit uncertainty preservation | PROVEN-v0 | `test_k3_transport_loss_is_unknown_not_failed` |
| K4 | identity-preserving reconciliation | PROVEN-v0 + live | `test_k4_reconciliation_reuses_original_dispatch` |
| K5 | evidence-derived cancellation outcome | PROVEN-v0 + live | `test_k5_cancel_request_is_not_terminal_cancellation` |
| K6 | evidence-gated knowledge admission | PROVEN-v0 | `test_k6_observation_cannot_bypass_verification` |
| K7 | atomic semantic mutation | PROVEN-v0 | `test_k7_failed_admission_restores_all_projections` |
| K8 | durable deterministic replay | PROVEN-v0 + live | `test_k8_corrupt_durable_history_fails_closed` |

## Test command

```bash
PYTHONPATH=src python3.12 -m unittest tests.test_kernel_charter -v
```

Expected current result:

```text
9 passed
```

Eight canonical tests prove K1–K8. One drift-guard test binds every Charter clause to its named executable evidence.

## Promotion rule

A guarantee enters the Charter only when its canonical test fails against the pre-fix implementation and passes against the new implementation. Documentation records proven capability; executable conformance establishes it.
