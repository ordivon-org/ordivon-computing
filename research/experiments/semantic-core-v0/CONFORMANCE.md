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
| K11 | backend-independent semantic projection | deterministic | `test_same_semantic_contract_runs_against_two_backends` |
| K12 | stable Effect / Binding separation | deterministic + integration | `test_k12_effect_binding_separation_survives_journal_restart` |

A drift-guard test binds every Charter clause to the named executable evidence in this file.

## Reproduce local conformance

```bash
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
PYTHONPATH=src python3.12 -m compileall -q src tests scripts
ruff check src tests scripts
```

The suite covers atomic rollback, Journal corruption and stale writers, response loss, cancellation races, versioned I/O, cross-Effect evidence, role escalation, forged grants, changed policy identity, wrong-secret replay, official attested Adapter projections, and exact two-backend semantic equivalence.

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
- known v2 and v3 Journals migrate to schema v4 while retaining immutable legacy payloads.

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

## P2E backend portability conformance

The canonical portability suite runs one semantic scenario set through two structurally distinct adapters:

| Property | Ordivon backend | Deterministic backend |
|---|---|---|
| execution operation | `workspace.exec` | `simulator.job.launch` |
| read operation | `workspace.read` | `simulator.object.read` |
| mutation operation | `workspace.mutate` | `simulator.object.mutate` |
| running state | `working` | `ACTIVE` |
| success state | `succeeded` | `COMPLETE` |
| uncertain state | `lost` / `orphaned` | `INDETERMINATE` |
| external identity | Job / Attempt / client request | operation / correlation / receipt |

`test_same_semantic_contract_runs_against_two_backends` requires the complete normalized reports to be equal. Both backends prove:

- versioned object read and digest-bound Observation;
- guarded mutation and stale-version rejection;
- independent reread, accepted Verification, and Fact admission;
- asynchronous Job Observation and Artifact projection;
- response loss as `UNKNOWN`;
- Adapter replacement and identity-preserving reconciliation without redispatch;
- cancellation intent before terminal cancellation evidence;
- one broken execution remaining isolated while unrelated work succeeds;
- DISPATCH authority on execution Events and OBSERVATION authority on evidence;
- absence of backend implementation objects from the Kernel state snapshot.

`test_simulator_response_loss_survives_journal_reopen` additionally closes and reopens a Journal-backed Kernel, creates a new simulator Adapter, correlates the already admitted backend operation, preserves the original Dispatch, reaches `SUCCEEDED`, and confirms one backend delivery.

The simulator and shared portability driver are internal experiment modules and are not exported from the package root. They provide executable evidence, not a generic plugin framework or a second production runtime.

Exact implementation revision: `f83764b58ae27ea64b93e7f8fa22c4577cf51e84`

Deterministic receipt: [`portability-results/backend-portability-f83764b.json`](portability-results/backend-portability-f83764b.json)

The receipt records distinct Backend contracts, `reports_equal: true`, one delivery after response loss, preserved Dispatch identity, ordered cancellation events, accepted Fact admission, isolated broken/unrelated executions, and `backend_objects_leaked: false`.

Exact Ordivon live confirmation on the same revision:

```text
signed Journal restart: UNKNOWN → authenticated replay → SUCCEEDED
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

## External semantic contract and Binding-edge conformance

The active [`external-semantic-contract-v0`](../external-semantic-contract-v0/) experiment owns canonical JSON, backend-neutral `EffectEnvelope`, normalized `ToolContract`, immutable `EffectBinding`, contract drift decisions, and Backend-specific lowering. The Kernel imports none of those packages.

The only new Kernel edge is `BindingAdmission`:

```text
binding_id
effect_id
effect_digest
binding_digest
binding_revision
supersedes_binding_id
Binding Authority Attestation
```

A `DispatchRecord` may reference the exact `binding_id` and `binding_digest` used to create its request. Legacy unbound Dispatches remain valid and Journal v2/v3 histories migrate to schema v4 without rewriting command payloads.

Deterministic evidence proves:

- Effect, Binding, and Dispatch Authorities are distinct;
- Binding revisions are contiguous, immutable, and linked through `supersedes_binding_id`;
- the current Binding must match a bound Dispatch at start;
- retryable pre-admission rejection returns the Effect to `PREPARED` and permits a new Binding revision;
- `DISPATCHED`, `RUNNING`, `UNKNOWN`, `RECONCILING`, and terminal Effects reject new Binding admission;
- a bound Dispatch and complete Binding history survive Journal close/reopen and genesis replay;
- Journal v2 and v3 histories migrate to v4 while legacy unbound Dispatches retain `binding_id = None`;
- the same external Envelope lowers to different Ordivon and simulator contracts while retaining one Effect digest;
- response loss on both Backends reconciles the original bound Dispatch with one delivery;
- an independent read still admits Verification and Fact after bound mutation.

This is the executable basis for K12.

Exact implementation revision: `2f4d7ca8db6756b8add3356db52dcd237ed7a256`

Exact results:

```text
Kernel tests: 99 / 99
external contract tests: 29 / 29
System Snapshot tests: 8 / 8
Python/Rust canonical vectors: 5 / 5
200-Effect memory workload: 34.433 ms (86.084 µs/command)
100-Effect Journal workload: 39.351 ms
200-entry Journal reopen: 30.327 ms
```

Live Ordivon on the same revision preserved one delivery, the original Dispatch, Journal `UNKNOWN → SUCCEEDED` recovery, three Artifacts, mutation-to-Fact admission, and stale-write rejection. Receipts are stored in the external contract `evidence/` directory and `benchmark-results/binding-edge-2f4d7ca.json`.

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
