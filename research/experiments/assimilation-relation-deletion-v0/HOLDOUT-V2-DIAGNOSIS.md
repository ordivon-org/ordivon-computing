# Assimilation Relation Deletion v0 — Cross-model Holdout v2 Diagnosis

Status: DeepSeek V4 Pro 24-cell holdout complete; result is primarily an apparatus/world-model refinement, not a clean representation winner.

Runtime Job: `job-01a03dbb-282b-7d91-8e13-f2a802c264f0`.

## Mechanical result

| arm | current-standing oracle match | boolean native-semantics match | authority overclaim |
| --- | ---: | ---: | ---: |
| RAW_FACTS | 9/12 | 9/12 | 0/12 |
| RELATION_ENVELOPE | 10/12 | 10/12 | 0/12 |

The one-cell advantage is not admissible as a general representation effect because several expected-positive cases were themselves underspecified relative to the word `current`.

## What Pro correctly exposed

### 1. Relation type is not relation value

`HARNESS-MODEL-FULL` said the Run bound an exact Provider/Adapter/requested-model identity but did not include the actual DeepSeek identity value in raw facts. Pro RAW refused to infer that the bound model was DeepSeek. The relation projection also originally used only `PROVIDER_ADAPTER_MODEL_BOUND`, not the exact value; nevertheless Pro treatment inferred the target relation from the rest of the packet. The safe conclusion is not that the envelope solved identity, but:

```text
IdentityRelationExists != TargetIdentityEstablished
```

A capability claim requires enough bound identity value/reference to entail the target claim.

### 2. Proven capability class is not a live current instance

`WORKSTATION-SURFPATH-FULL` contains real historical/current-owner evidence that exact Surfpath generations have been handshake-qualified, destination-probed and used under fresh revalidation. But the packet did not contain a live observation proving that a particular path generation was available *at the moment of the holdout*. Pro therefore refused `CURRENTLY ESTABLISHED` in both arms.

```text
CapabilityMechanismProven
!= CurrentCapabilityInstanceBound
!= CurrentAvailabilityObserved
```

Repository/experiment evidence can establish a reusable capability mechanism without establishing live instance currentness.

### 3. Domain relation is not one monolithic capability

`FINANCE-OKX-FULL` bundled observation, effect and reconciliation into one target phrase. Pro correctly noticed that provider-native venue observation, effect submission and reconciled financial consequence have different proof boundaries. The case oracle assumed the composed Finance relation was already the unit under test, while the prompt allowed a narrower reading.

```text
ObservationCapability
!= EffectSubmissionCapability
!= ConsequenceReconciliationCapability
```

A future assimilation representation should preserve operation granularity rather than name one provider as a capability bundle.

### 4. `preserveNativeSemantics` boolean is not a valid semantic-erasure oracle

Several Pro responses returned `false` while their explanations explicitly preserved the external authority boundary and rejected overclaim. The boolean prompt did not define whether `true` meant 'the response itself preserves semantics' or 'the target operation requires native semantics to be preserved'. Retire this boolean as a causal metric. The textual reasons and explicit authority overclaim checks remain evidence.

## Relation-deletion standing after v1+v2

The destructive result is stronger than the representation A/B result:

- remove target identity/current binding -> named current capability is not established;
- remove current authorization -> target action is not established;
- remove target applicability -> direct target use is not established;
- remove operation authority -> reachable resource does not become unauthorized action capability;
- remove consequence evidence -> attempted external effect does not become established consequence;
- remove live instance/currentness evidence -> validated mechanism does not become currently available instance.

Representation has independent stronger evidence from ACS0–ACS9 and Representation D2/D2A; this campaign need not recreate it.

## Revised assimilation object

The smallest surviving research representation is no longer a flat seven-field kernel. It has at least three nested relations:

```text
Capability Class / Mechanism
    what operation has been demonstrated possible through this carrier/relation?

Capability Binding / Instance
    which exact source/resource/account/model/device/generation/permission relation is admitted for the target?

Current Availability / Consequence
    is that exact relation usable now, and what current observation/effect/consequence is actually established?
```

Each level remains owner-/source-relative and operation-relative. This is an audit distinction, not a proposed schema/service.

## Representation conclusion

The compact relation projection is still promising because it reduced some finite-Agent reconstruction errors in Flash and one Pro cell, and because ACS already demonstrates large representation effects. But this experiment does **not** earn a canonical universal `AssimilationEnvelope`. Its most valuable result is that such an envelope would be harmful if it flattened class/instance/currentness or relation type/value.
