# Assimilation Relation Deletion v0 — Analysis v1

Status: first live Flash campaign complete; apparatus corrected before cross-model holdout.

## Frozen campaign

The first campaign ran 12 real-case-derived cells under two representations (`RAW_FACTS`, `RELATION_ENVELOPE`) with one fresh DeepSeek V4 Flash Run per cell. The contract, cases and prompt were frozen before result visibility. Runtime Job: `job-01a03db6-b700-7503-8ba0-808afe58dbc5`.

### Robust endpoints

| arm | standing correct | preserve native semantics | authority overclaim | native semantic erasure |
| --- | ---: | ---: | ---: | ---: |
| RAW_FACTS | 10/12 | 12/12 | 0/12 | 0/12 |
| RELATION_ENVELOPE | 11/12 | 12/12 | 0/12 | 0/12 |

Paired standing changes:

- Knowledge / no applicability: RAW `NOT_ESTABLISHED` -> ENVELOPE `POTENTIAL` (oracle `POTENTIAL`): improvement.
- Workstation Surfpath full: RAW `POTENTIAL` -> ENVELOPE `REALIZED` (oracle `REALIZED`): improvement.
- Figma pending OAuth: RAW `POTENTIAL` -> ENVELOPE `NOT_ESTABLISHED` (oracle `POTENTIAL`): regression.
- all other standing pairs unchanged and correct.

This is positive but insufficient evidence for a representation main effect: n=12 paired cases, one model, one replicate, and the standing vocabulary itself exposed a confound.

## Apparatus diagnosis

The original result schema incorrectly mixed three distinct questions:

```text
CapabilityStanding
!= AssimilationOpportunity
!= CarrierStrategy
!= NextAction
```

`POTENTIAL` was especially overloaded. For Figma, the external capability is a real *opportunity* but the exact target read/write operation is not a *current realized capability* until OAuth authority and a real consumer round exist. For mature external knowledge whose assumptions have not been transported, the source is a real knowledge opportunity but not yet a current target-specific capability. Therefore `POTENTIAL` should not sit between `REALIZED` and `NOT_ESTABLISHED` on the same current-capability axis.

The `decision` labels were also invalid as a primary oracle. `PREFER_REMOTE_SHARED`, `LOCALIZE`, `QUALIFY_OR_BIND` and `HOLD` combine carrier choice with next action. Flash often gave a semantically correct capability judgment and explanation while selecting a different but defensible carrier/action label. Those results must not be counted as evidence for or against the relation kernel.

The v1 `falseInternalization` metric is therefore invalid whenever it infers origin bias merely from the token `LOCALIZE`; several such responses explicitly preserved external authority and rejected host-control overclaim. Keep the raw evidence, retire this metric for causal interpretation.

## Strong deletion evidence independent of representation arm

The case pairs plus current owner evidence support target-relative deletion effects:

1. **Identity/currentness** — qualified Blender vs historical Blender with current bytes/profile unknown: current target capability collapses from established to not established.
2. **Authorized access** — Figma installed/configured but OAuth consent absent: current read/write capability is not realized.
3. **Consequence evidence** — OKX submission success without order/fill/bill/portfolio reconciliation: intended financial consequence is not established.
4. **Owner-authorized operation relation** — reachable public relay without SSH/RCE grant: arbitrary host control is not a capability.
5. **Applicability** — authoritative external knowledge without target assumption transport: target-specific application is not established, though the knowledge remains a qualifiable opportunity.
6. **Provider/model identity** — unattributable model response cannot establish capability specifically from the named current model generation.

Representation itself already has stronger independent Ordivon deletion evidence from ACS0–ACS9: compact owner-derived semantic projections raised exact next-operation selection from 9/21 to 19/21 (Flash) and 2/7 to 7/7 (Pro) in the pre-implementation campaign, and from 5/24 to 22/24 (Flash) and 2/8 to 7/8 (Pro) after implementation; a targeted Workstation holdout was 0/5 raw vs 5/5 current surface. Therefore this experiment should not pretend to rediscover that `consumer-usable representation` can be deletion-essential under finite-Agent budgets.

## v2 correction

Cross-model holdout will keep the same factual cases but separate outputs:

```text
currentCapabilityStanding = ESTABLISHED | NOT_ESTABLISHED
assimilationOpportunity = ACTIVE | QUALIFIABLE | NONE_FOR_TARGET
nextAction = USE_CURRENT | QUALIFY_OR_BIND | RECONCILE_OR_VERIFY | STOP_TARGET
preserveNativeSemantics = boolean
```

No local-vs-remote carrier preference will be scored. Carrier selection is a different workload requiring cadence/cost/recovery/latency/maintenance facts.

Primary holdout endpoint: exact `currentCapabilityStanding` and authority/native-semantics safety. Secondary: `assimilationOpportunity`. `nextAction` is diagnostic only unless the case uniquely entails it.

## Current standing

The first campaign does **not** justify a global Assimilation schema or service. It does strengthen the relation-centric model and, more importantly, demonstrates why an assimilation representation must preserve orthogonal axes rather than compressing them into a maturity score or adoption decision.
