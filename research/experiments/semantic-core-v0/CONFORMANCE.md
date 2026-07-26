# Semantic Kernel v0 conformance

## Evidence classes

- **deterministic** — a local test exercises one invariant;
- **integration** — multiple semantic layers execute together without a real external service;
- **live** — a sanitized real Ordivon trajectory exercises the boundary;
- **exact-revision** — an immutable receipt records the implementation commit.

## Kernel Charter matrix

| ID | Guarantee | Evidence | Canonical test |
|---|---|---|---|
| K1 | stable semantic identity | deterministic | `test_k1_identity_survives_journal_restart` |
| K2 | Effect / Dispatch separation | deterministic | `test_k2_dispatch_identity_cannot_cross_effects` |
| K3 | explicit uncertainty preservation | deterministic | `test_k3_transport_loss_is_unknown_not_failed` |
| K4 | identity-preserving reconciliation | deterministic + live | `test_k4_reconciliation_reuses_original_dispatch` |
| K5 | evidence-derived cancellation outcome | deterministic + live | `test_k5_cancel_request_is_not_terminal_cancellation` |
| K6 | evidence-gated knowledge admission | deterministic + live | `test_k6_observation_cannot_bypass_verification` |
| K7 | atomic semantic mutation | deterministic | `test_k7_failed_admission_restores_all_projections` |
| K8 | durable deterministic replay | deterministic + live | `test_k8_corrupt_durable_history_fails_closed` |
| K9 | role-scoped semantic authority | deterministic | `test_role_specific_signer_cannot_escalate_to_another_role` |
| K10 | content-bound attestation | deterministic + live | `test_attestation_provenance_survives_journal_replay` |
| K11 | backend-independent semantic projection | deterministic | `test_same_semantic_contract_runs_against_two_backends` |
| K12 | stable Effect / Binding separation | deterministic + integration + live | `test_k12_effect_binding_separation_survives_journal_restart` |

A drift-guard test binds every Charter clause to the named executable evidence in this file.

## Deterministic reproduction

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests
python3.12 -m compileall -q src tests scripts
ruff check src tests scripts
```

The deterministic suite protects:

- legal Effect and Dispatch transitions;
- UNKNOWN without blind redelivery;
- cancellation races;
- evidence and Fact admission;
- role separation and signed content;
- atomic rollback and explicit full audit;
- Journal corruption, stale writers, v2/v3 migration and genesis replay;
- Binding revision history and exact Dispatch references;
- legacy unbound compatibility;
- structurally distinct Backend projections.

## Current external boundary

`KernelEffectProjection` is an internal projection, not a second public Effect IR. New Kernel state stores the public semantic action once through the capability projection and does not store a Provider operation. Historical Journal records with the old `EffectSpec` name and duplicated operation continue to decode through a compatibility alias.

Complete signed Bindings, Tool schemas, encoders and request arguments remain outside Kernel state. The Kernel stores only `BindingAdmission` and the exact Binding identity/digest used by a bound Dispatch. External integration additionally proves that the actual Adapter request digest equals the stored complete Binding arguments.

## Heavy evidence

Benchmarks, real Ordivon execution, process restart, live Tool catalog capture and exact receipt generation are manual T3 gates. They do not run in ordinary CI. Receipts and commands are indexed in [`EVIDENCE.md`](EVIDENCE.md) and the adjacent [`external-semantic-contract-v0/EVIDENCE.md`](../external-semantic-contract-v0/EVIDENCE.md).
