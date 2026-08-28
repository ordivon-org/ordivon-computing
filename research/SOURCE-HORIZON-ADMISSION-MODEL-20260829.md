# Source Horizon Admission Model — 2026-08-29

Status: reusable Computer/Research-method synthesis over owner-local currentness failures. This document is **not** a Git policy, global currentness registry, Runtime state machine, owner truth source, or source resolver.

## Question

When a finite Agent opens an exact repository revision and needs to make a present-tense claim or plan a present-tense action, what must be true before exact source bytes can be treated as the relevant current owner surface?

The observed failure is not simply stale Git. Exact historical source can remain correct, reproducible, cryptographically self-consistent, and useful while being the wrong horizon for the operation now.

Preserve:

```text
ExactSource != PresentSourceHorizon
PresentSourceHorizon != OwnerSemanticTruth
OwnerSemanticTruth != DeploymentTruth
RefDrift != SemanticStaleness
ValidCurrentPointer != PresentCurrentPointer
HistoricalCapabilityExistence != PresentAffordance
```

## Minimal model

Let:

- `O` = the current operation or claim;
- `R` = the owner-native rule that says which source relation is authoritative for `O`;
- `H_observed` = the exact source horizon actually opened/consumed;
- `H_expected(O)` = the exact present source horizon resolved by `R` for `O`;
- `L(O)` = the load-bearing carrier(s) whose change can alter the operation's correct result;
- `C` = the source-bound consumer/evaluator.

The safe sequence is:

```text
observe coordinates
→ resolve H_expected(O) from the owner-native operation contract
→ bind C to exact source bytes
→ compare H_observed with H_expected(O)
→ if they differ, test L(O) rather than using ref distance as the verdict
→ classify the operation-specific consequence
```

Two questions must remain separate:

```text
Q1: Is this the present source-integration horizon?
Q2: Does this exact historical source still support the same operation-specific conclusion?
```

For Q1, equality with the owner-resolved horizon is required. For Q2, a different historical source may still be usable when the load-bearing carrier is proven equivalent or the claim is explicitly historical/current-to-source. Such reuse is revalidation, not permission to relabel the old checkout as the present repository.

## Diagnostic outcomes

These are research diagnostics, **not** a required shared enum or new Runtime schema.

### A. Authority-carrier absence

A stale horizon lacks a current authority carrier that exists at the present horizon.

Natural witness — Harness:

```text
local main 240c841144982d6e525ce27b7b41f474af8e9b8d
→ research/authority/CURRENT.json absent

observed upstream main 97708bc0b6a6eea556ca580dab5c0417e6df108d
→ CURRENT.json present
→ immutable owner publication present
→ publication digest matches AuthorityVersionRef
```

Consequence: an Agent starting from the stale horizon can falsely conclude that no owner-current publication surface exists.

### B. Capability-surface absence

A stale horizon lacks a present Agent/consumer operation entirely.

Natural witness — Atlas:

```text
local main 71b1613060f9dafe3f56361b29ea55eacba7504a
→ `ordivon-atlas check-owner Harness` is not a valid command

upstream main ecf8dad2f51d50e744a942a5cbf08eadd7b50c7d
→ the same operation returns Harness CURRENT_TO_SOURCE
```

Consequence: stale source changes the reachable currentness capability, not merely prose or revision metadata.

### C. Self-consistent but superseded current pointer

A stale horizon contains a fully valid currentness pointer, but a later source horizon has republished a successor pointer.

Natural witness — SCD:

```text
local main 3ae660ebbd267097309d1c11a233194c6bdb8bd7
CURRENT → sha256:f98fef8a...
publication digest = sha256:f98fef8a...

upstream main b4b349a352f05d1ac4885658a9d8c087e0e13ad0
CURRENT → sha256:8564c1fa...
previousAuthorityVersionRef = sha256:f98fef8a...
```

The old pointer is not corrupt. It remains correct **for that historical source horizon**. The error occurs only if a consumer promotes that historically-current pointer into present owner currentness without first resolving the source horizon.

This is the strongest warning against treating cryptographic validity or a filename such as `CURRENT.json` as timeless currentness.

### D. Phantom capability

A stale horizon still exposes an implementation that the current owner deliberately retired.

Natural witness — World:

```text
historical World source
→ resource_wire.py and message_wire.py exist

current integrated World source
→ both unused Python adapters are deleted
→ trajectory semantics / packaged JSON contracts remain, but the Python affordances do not
```

Consequence: an Agent may plan against an implementation that is historically real yet no longer part of the present callable owner surface.

This is the inverse of Atlas's missing-capability failure.

## Required negative control: ref drift with no changed consequence

The model would be wrong if every source mismatch became a blocker.

Observed negative controls include:

- Game: local/upstream ref drift did not change the load-bearing owner projection for the tested consumer;
- Finance executor: running release source revision differed materially from current Finance source, while all 24 load-bearing release-closure files were byte-identical and current bindings remained correct.

Therefore:

```text
H_observed != H_expected
AND L(O) equivalent
→ historical/exact-source result may remain valid after revalidation
→ do not infer stale semantic/deployment standing from ref drift alone
```

The present repository horizon is still different; the point is that not every operation needs the entire repository horizon to be identical once the relevant carrier is independently proved equivalent.

## Admission law

For a present-tense operation, source use is justified only after both **selection** and **binding** have occurred:

```text
SourceSelection(O)
= owner-native resolution of H_expected(O)

SourceBinding(C)
= proof of the exact bytes/revision C actually consumed

SourceSelection != SourceBinding
```

A useful operational decision tree is:

```text
Need present-tense claim/action?
  no  → exact historical source may be sufficient; label the horizon
  yes → owner-operation source rule recoverable?
          no  → SOURCE_AUTHORITY_UNRESOLVED / owner-equivalent UNKNOWN
          yes → bind expected horizon and consumer
                 |
                 +-- exact horizon match → continue with owner semantic/currentness checks
                 |
                 +-- horizon mismatch → does L(O) change?
                       |
                       +-- no / proven equivalent → revalidate scoped result; do not relabel old repo as present
                       |
                       +-- yes / unknown → block present claim or reopen on current source
```

The source-horizon gate does not itself decide semantic truth. It only prevents a consumer from entering semantic/currentness evaluation through the wrong source relation.

## Why there should be no generic resolver yet

The four positive failures share a shape but not an owner truth rule:

- Harness uses repository source integration to reach its owner-research publication surface;
- Atlas uses repository source integration to determine its own current Agent interface, while `check-owner` evaluates foreign owner publications;
- SCD requires source-horizon resolution before interpreting its own `CURRENT.json`, whose immutable publication has an independent internal `sourceRevision` fence;
- World uses source integration to determine present callable implementation surface, while provider/live Reality currentness remains elsewhere.

A universal service would need to encode these owner-operation distinctions or silently recreate shadow authority. The current evidence supports a shared **method** and owner-local contracts, not a shared resolver.

## Falsifiers / reopen conditions

Reopen this model if any of the following occurs:

1. two or more independent owners require the same machine-readable resolution semantics and cannot safely compose them from owner-local contracts plus mechanical observation;
2. a real consumer needs source authority resolved before it can even identify the relevant owner/operation contract, and Atlas/owner recovery cannot close the loop;
3. owner-local rules produce contradictory expected identities for the same operation without an explicit higher-order authority relation;
4. a generic resolver beats owner-local composition under deletion/classical-baseline testing while preserving all owner boundaries;
5. the four failure classes fail to explain a new changed-consequence source-horizon error.

Until then, prefer:

```text
shared mechanical observation
+ owner-operation source contract
+ exact source-bound consumer
+ load-bearing consequence test
```

over a central resolver, global currentness score, or repository-wide `latest == truth` heuristic.

## Current evidence boundary

This model is grounded in bounded Ordivon source/currentness dogfood observed on 2026-08-29. It does not claim that Git is the universal carrier of currentness, that every repository uses remote `main`, or that source integration alone proves owner semantic truth, deployment truth, external Reality, safety, or action authority.
