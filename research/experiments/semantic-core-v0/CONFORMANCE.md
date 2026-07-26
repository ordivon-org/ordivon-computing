# Semantic Core v0 Conformance

## Evidence classes

- **deterministic** — an executable local test exercises the invariant;
- **live** — a sanitized real Ordivon trajectory exercises the boundary;
- **exact-revision** — the evidence records the implementation commit used by the trajectory.

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

A drift-guard test binds every Charter clause to the named executable evidence in this file.

## Reproduce local conformance

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 -m compileall -q src tests scripts
ruff check src tests scripts
```

The suite covers atomic rollback, Journal corruption and stale writers, response loss, cancellation races, versioned I/O, cross-Effect evidence, role escalation, forged grants, changed policy identity, wrong-secret replay, and official attested Adapter projections.

## P1 structural conformance

The boundary suite additionally proves:

- Ordivon Adapters are typed against `ExecutionView`;
- Verification and Fact admission use separate role protocols;
- raw reducer names retain compatibility aliases while the implementation boundary is explicit;
- the Dispatch transition graph contains only the six admitted transitions;
- execution, recovery, Fact provenance, and Authority projections reconstruct canonical records without mutation;
- UNKNOWN recovery projections preserve the original Dispatch identity and return `RECONCILE` as the next action.

Exact implementation revision: `aec6269b065b36ce9277bdbd072b1bd51e2ab5c5`

Live confirmation on that revision:

```text
signed Journal restart: UNKNOWN → authenticated replay → SUCCEEDED
workspace.exec deliveries: 1
correlated Jobs: 1
Dispatch identity preserved: true
Journal entries: 4 → 11

versioned mutation: succeeded
independent reread: matched resulting digest
Fact committed: 1
stale mutation: failed / INVALID_REQUEST
final content and digest: stable
```

## P2 performance and compatibility conformance

Deterministic tests prove:

- new Effects reject inactive precondition, Task lineage, keyed-idempotency, and expiry fields;
- the command hot path does not call complete-state `_snapshot()`;
- the Journal hot path does not clone `ReferenceReducer`;
- SQLite append failure rolls back the in-memory projection;
- explicit full audit still detects cross-projection corruption;
- a known v2 Journal migrates to v3 and accepts a v3 tail.

Exact baseline revision `bf60668aa7eac1defb4181fcdbeeb8123c7030af` measured 200 Effects / 400 in-memory commands at 3,693.445 ms and 100 Effects / 200 Journal commands at 963.434 ms. Exact optimized implementation revision `dd4730ef6767eac1a3f3d6f9c73d6dc639ca894a` measured the same workloads at 37.033 ms and 38.131 ms respectively. The 200-Effect in-memory path improved by about 99.7×, the 100-Effect Journal write path by about 25.3×, and 200-entry reopen by about 34.2× (`1,014.054 ms → 29.639 ms`). Per-command memory cost remained approximately flat at 0.09–0.11 ms across 10–200 Effects.

Receipts:

- `benchmark-results/baseline-bf60668.json`;
- `benchmark-results/optimized-dd4730e.json`;
- `benchmark-results/prototype-23353fd.json` for the rejected checkpoint design.

Exact live confirmation on `dd4730ef6767eac1a3f3d6f9c73d6dc639ca894a`:

```text
signed restart: UNKNOWN → authenticated replay → SUCCEEDED
workspace.exec deliveries: 1
correlated Jobs: 1
Dispatch identity preserved: true
Journal entries: 4 → 11
semantic Artifacts: 3

versioned mutation: succeeded
independent reread: matched resulting digest
Fact committed: 1
stale mutation: failed / INVALID_REQUEST
final content and digest: stable
```

## Live evidence summary

### Signed process-restart recovery

Implementation revision: `88678a3c06f406c41eadb0ded484d09aa656ae43`

```text
real workspace.exec delivered once
→ successful response deliberately discarded
→ signed Dispatch and Effect become UNKNOWN
→ first Python process exits
→ second process authenticates the versioned Journal schema
→ original Job correlated by stable clientRequestId
→ original Dispatch admitted
→ signed Observation and three Artifacts recorded
→ Effect succeeds
→ third open independently replays terminal projection
```

Sanitized result:

```text
initial state: unknown
terminal state: succeeded
workspace.exec deliveries: 1
correlated Jobs: 1
Dispatch identity preserved: true
Journal entries: 4 → 11
semantic Artifacts: 3
```

### Scoped versioned mutation to Fact

Implementation revision: `88678a3c06f406c41eadb0ded484d09aa656ae43`

```text
views.effects admits read and mutation Effects
→ views.execution performs guarded mutation and independent reread
→ views.verification records Claim and accepted Verification
→ views.facts accepts Fact
→ stale mutation using the old digest fails / INVALID_REQUEST
→ final content and digest remain stable
```

Observed digests:

```text
before: sha256:9160d4be34c8695bd172a76c7c7966587ea5a4d991ad22c87b2b91af54aa9ebb
after:  sha256:7b9a72466d3960eb2aacccfc848939453490db0678bd4725def3f789b891c919
```

### Cancellation race

Implementation revision: `d45ba1b1165e0fa863810c2e23f0086d0fedb3d6`

Two real Jobs established both legal outcomes:

```text
CANCEL_REQUESTED → task.cancel applied → CANCELLED
CANCEL_REQUESTED → natural completion observed first → SUCCEEDED
```

Both outcomes retained the original Job and Dispatch identity and created no duplicate execution.

## Promotion rule

A hard guarantee enters the Charter only after a canonical test demonstrates the pre-fix failure and passes against the implementation. Live evidence strengthens backend claims but does not replace deterministic conformance.

New live receipts should replace older equivalent receipts rather than create another status or report file. Git history preserves superseded evidence.
