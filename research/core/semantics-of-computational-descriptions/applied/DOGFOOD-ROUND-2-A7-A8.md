# Applied SCD Dogfood Round 2 — A7/A8 Runtime Boundary

Status: **consumer falsification evidence**, not Foundation truth.

Exact Runtime source fence inspected read-only:

`7af1b0d51f678d8662ac85bb91ec4d363141c483`

Round 2 tests the description-semantics ↔ physical-realization boundary in both directions.

## A7 — Semantic validity does not imply current Runtime realizability

Runtime commits the exact execution provider contract/digest on first admission. Before physical dispatch it re-observes the configured Runner/Windows launcher provider. If the committed provider no longer matches, Runtime fails closed with:

```text
EXECUTION_PROVIDER_PRECONDITION_DRIFT
```

before a systemd unit or Windows child is created.

SCD interpretation:

```text
S = (ρ ⊢ D @ Σ)
φ = semantic claim about D
```

The abstract description and its semantic relation/property may remain valid under `Σ`. What fails is the separate Runtime-owned claim that a particular concrete realization remains currently admissible under the committed provider/policy/resource/authority contract.

Therefore:

```text
SemanticValid(D, Σ)
    !=>
RuntimeRealizableNow(D, provider, policy, resources)
```

and conversely:

```text
RuntimeAdmissionRejected
    !=>
SemanticInvalid(D, Σ)
```

K0.2 treatment:

- semantic claim `φ` remains SCD-scoped;
- Runtime provider/admission facts remain external owner-native support references in `Δ`;
- provider drift may invalidate a realization-dependent claim without invalidating unrelated semantic claims.

Result: **PASS / owner-firewall strengthened**.

## A8 — Runtime success does not imply semantic correctness or intended dependency consumption

Runtime's canonical Effect Kernel explicitly states:

```text
process exit = execution evidence
```

but not automatically:

```text
external-effect receipt
semantic Task completion
Goal satisfaction
```

The strongest hostile case is Runtime P4's physical same-authority-view experiment.

### P4 physical fixture

A trusted-local Runtime Job:

1. committed V1 of a declared Host Dependency;
2. passed Runtime's host-side prerequisite/path checks;
3. created a private mount namespace inside the target;
4. bind-mounted an unchanged alternate V2 file over the same pathname only in the target view;
5. read V2;
6. exited zero.

Meanwhile Runtime's host pathname remained V1 and no host-namespace inotify drift was observed.

Runtime therefore correctly scopes its evidence as:

```text
runtime_host_namespace_path_witness
```

which means only that no relevant path/topology drift was observed in Runtime's host namespace. It does **not** mean:

```text
target namespace isolated
committed bytes immutable
actual target consumed V1
semantic dependency was preserved
external effect was correct
Goal/Task completed
```

Thus:

```text
RuntimeSuccess
    !=>
SemanticCorrectness
```

and more specifically:

```text
RuntimeSuccess
+ host-path continuity evidence
    !=>
TargetConsumedCommittedMeaning
```

K0.2 treatment:

- Job/Attempt/evidence facts enter `Δ` as Runtime-owner references;
- any SCD claim must stay within the exact support scope;
- there is no valid correspondence that upgrades `host namespace path remained stable` into `target consumed semantically intended bytes`.

Result: **PASS / evidence-scope firewall strengthened**.

# Round-2 joint result

A7 and A8 prove a two-direction non-equivalence at the applied boundary:

```text
SemanticValidity != RuntimeRealizability
RuntimeSuccess     != SemanticCorrectness
```

The two systems can diverge without contradiction because they own different truth roles.

This directly supports the existing Runtime/SCD reconciliation:

- abstract compatibility/equivalence/refinement/transport → SCD responsibilities;
- admitted Operation binding, physical realization, Attempt/evidence/resource/authority truth → Runtime responsibilities.

No K0.3, RuntimeRealization primitive, SCDF reopen or new Foundation is justified.
