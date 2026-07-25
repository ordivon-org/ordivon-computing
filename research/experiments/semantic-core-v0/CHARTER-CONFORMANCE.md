# Kernel Charter Conformance v0

## Status vocabulary

- **PROVEN-v0** — executable deterministic tests exist; live proof is noted where available.
- **OPEN-P0** — required for the Charter but not enforced by the current API.
- **DELEGATED** — intentionally inherited from a classical lower layer.
- **NON-GOAL** — explicitly outside this Kernel.

## Guarantee matrix

| ID | Guarantee | Status | Canonical executable evidence | Remaining boundary |
|---|---|---|---|---|
| K1 | stable semantic identity | PROVEN-v0 | `test_k1_identity_survives_journal_restart` | no replicated/multi-host identity service |
| K2 | Effect/Dispatch separation | PROVEN-v0 | `test_k2_dispatch_identity_cannot_cross_effects` | public Effect IR not frozen |
| K3 | unknown is not failure | PROVEN-v0 | `test_k3_transport_loss_is_unknown_not_failed` | Adapter classification remains trusted |
| K4 | reconcile before redispatch | PROVEN-v0 + live | `test_k4_reconciliation_reuses_original_dispatch` | remote history retention may expire |
| K5 | cancellation intent differs from outcome | PROVEN-v0 + live | `test_k5_cancel_request_is_not_terminal_cancellation` | compensation is not modeled |
| K6 | Observation is not Fact | PROVEN-v0 | `test_k6_observation_cannot_bypass_verification` | authority/trust-domain evidence is not enforced |
| K7 | atomic semantic mutation | PROVEN-v0 | `test_k7_failed_admission_restores_all_projections` | reference implementation is not performance-oriented |
| K8 | replayable durable history, fail closed | PROVEN-v0 + live | `test_k8_corrupt_durable_history_fails_closed` | no snapshots, migration, replication, or signed root |
| K9 | authority separated by role | **OPEN-P0** | skipped gate `test_k9_authority_roles_are_enforced` | one public Kernel object currently exposes all mutation powers |
| K10 | mechanical success is not goal completion | PROVEN-v0 | `test_k10_successful_tool_result_does_not_create_fact` | Goal Runtime is intentionally absent |

## Test command

```bash
PYTHONPATH=src python3.12 -m unittest tests.test_kernel_charter -v
```

Expected current result:

```text
10 passed
1 skipped (K9 OPEN-P0)
```

The skip is intentional evidence of an unimplemented hard boundary. It must not be removed by weakening K9; it is closed only by introducing distinct authenticated authority surfaces and adversarial bypass tests.

## Promotion rule

A guarantee may move to `PROVEN-v0` only when the canonical test fails against the pre-fix implementation and passes against the new implementation. Documentation alone is not conformance.
