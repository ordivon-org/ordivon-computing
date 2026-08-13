# ACS3 — Minimal Agent Consumption Grammar

Status: derived research grammar, **not** a universal API or shared truth store.

## Thesis

Ordivon owners do not need identical methods. They need to make a small set of mechanically knowable distinctions easy for an Agent to recover **when those distinctions exist in that domain**.

The grammar is semantic, not nominal:

```text
owner-native truth / invariant
        ↓
owner-native primitive
        ↓
derived consumption projection
        ↓
Agent selects exact next operation
        ↓
owner-native result / receipt
```

A projection may compile facts already owned elsewhere. It must preserve each fact's truth role, source owner, applicability/currentness, and effect/authority boundary.

## Eight consumption questions

An Agent-facing owner surface should answer the applicable subset of these questions without requiring source-code archaeology:

| Question | Required projection semantics | Must not imply |
| --- | --- | --- |
| **Who owns this?** | owner/stable role/source authority | central Ordivon ownership |
| **What can I do?** | capability/operation families and exact addressable binding | permission or current availability merely because a capability exists |
| **Can I do it now?** | configured/available/current plus basis and observation/applicability time | durable future availability |
| **What does this operation do immediately?** | read/write/external-effect class; sync/async; admission vs dispatch when relevant | semantic completion |
| **What authority does it require?** | exact authority/grant/action boundary | automatically granted authority |
| **What truth will the result carry?** | observation/projection/receipt/semantic claim/current owner state | stronger truth than the owner actually establishes |
| **If it fails or becomes UNKNOWN, what is mechanically safe?** | failure class, effect possibility, retry/reconcile/recover disposition and addressable identity | semantic next strategy |
| **What deeper primitive/evidence can I inspect?** | escape hatch/source/evidence references | requirement that ordinary Agents always start from the lowest layer |

These are fields/concepts, not mandatory function names.

## Candidate vocabulary

A reusable projection MAY use the following concepts where native semantics support them:

```text
OwnerIdentity
CapabilityFamily
AgentOperation
Availability
Applicability
AuthorityRequirement
EffectClass
ResultTruthRole
FailureDisposition
RecoveryAction
EvidenceReference
EscapeHatch
```

No owner is required to materialize all of them as new objects. Existing structures remain preferred when they already encode the distinction.

### Operation projection

A compact operation description should normally be able to express:

```json
{
  "operationRef": "owner-native exact address",
  "purpose": "mechanically bounded role",
  "binding": "CLI/MCP/API/native binding",
  "availability": {
    "state": "available|unavailable|unknown|not-applicable",
    "basis": "owner-native currentness/projection reference"
  },
  "effectClass": "read-only|local-state-write|external-effect|mixed|unknown",
  "requiredAuthority": [],
  "resultTruthRole": "owner-state|point-in-time-observation|projection|receipt|proposal|unknown",
  "failureDisposition": {
    "effectPossible": "yes|no|unknown",
    "safeToRetry": "yes|no|unknown",
    "reconcileRequired": false
  },
  "escapeHatch": "deeper exact primitive/evidence reference"
}
```

This is illustrative grammar only. Owners should reuse their native schemas rather than copy this JSON shape blindly.

## Internal positive exemplars

### Host — exact tools are already the grammar

`task.resume` directly communicates its role, stale-read fence, truth boundary, and that Runtime/Git checkpoint fields are only navigation hints. ACS found no need for another wrapper.

Lesson: **good tool descriptions can themselves be the projection layer.**

### Finance — obligation-aware domain compilation

Finance earns a richer domain form:

```text
Goal
  ↓
Unresolved Obligation
  ↓
candidateOperationRefs
  ↓
AgentOperation
  ├─ capability refs
  ├─ binding / entrypoint
  ├─ side-effect class
  ├─ required authority
  └─ current availability + basis
```

This does not become a scheduler because candidate operations remain possibilities. The Agent still chooses the semantic path.

Lesson: **domain obligations may point to addressable options without infrastructure choosing the option.**

### Runtime — affordance projection

`runtime.describe` already expresses a different native grammar:

```text
Execution target
  ├─ configured
  ├─ available + issue
  ├─ execution profiles
  ├─ provider identity
  ├─ immutable-input support
  └─ structured-plan / continuity affordances
```

No Finance-like `obligation` object is appropriate.

Lesson: **cross-owner uniformity is in questions/distinctions, not data models.**

### Security — maturity/tier projection

`security_surface_manifest()` separates constitution, profile, integration, and research apparatus. Here the critical consumption question is not only “can I call this?” but “what epistemic/maturity role does this mechanism occupy?”

Lesson: **research-heavy owners need surface taxonomy so experimental apparatus does not masquerade as stable capability.**

### Game — perceptual projection

Mission-control/replay projections compress deep world state into actors, evidence stages, objectives, consequences and replay frames.

Lesson: **projection can be a perceptual interface rather than a command catalog.**

### Web — currentness counterexample

`agent:context` is useful but reports captured publication snapshots without labeling their applicability/currentness role. Web already has an owner-native comparison path that re-probes each owner's admitted public-document envelope; in the current audit it classified Harness and Security stale while Game remained current. This also shows that raw owner HEAD inequality is not itself a valid staleness test: Web's public projection is scoped to admitted public-source documents.

Lesson: **projection must carry source/applicability truth and its exact currentness basis, not merely copied content.**

## Mechanical resolution vs semantic sovereignty

Infrastructure should resolve facts that are mechanically forced:

```text
schema version
cursor / pagination continuation
exact digest
known addressable identity
configured availability
current owner revision when owner can prove it
retry/reconciliation mechanics
canonical encoding
exact input schema
```

The Agent/domain should retain choices such as:

```text
which objective matters
which source is relevant
which hypothesis to pursue
which candidate operation best advances an obligation
whether evidence is semantically sufficient
whether to trade / publish / intervene
what cognition to retain
```

Rule:

> **Eliminate repeated mechanical reconstruction; preserve semantic choice.**

## Progressive disclosure

A mature surface should support entry at the lowest sufficient level rather than force every Agent through implementation detail:

```text
Level 0 — identity / owner role
Level 1 — capability or perceptual families
Level 2 — exact operation / current availability / effect / authority
Level 3 — result truth + failure/recovery semantics
Level 4 — native primitive / evidence / implementation escape hatch
```

This does not require five literal endpoints. One excellent MCP schema may span Levels 1–4; a domain Context may compile Levels 1–3 while linking the native primitive.

## Currentness law

Derived projection is valid only with explicit applicability semantics. A projection that copies owner state should be able to distinguish at least:

```text
source identity
observed/projected revision or digest
projection time (when temporal)
currentness authority
whether currentness was revalidated
```

If the projection cannot prove currentness, it must say so rather than silently present historical state as current.

## Failure law

When infrastructure can mechanically know failure/recovery state, the Agent should not reconstruct it from prose or transport exceptions.

Desired semantics, where provable:

```text
failureClass
ownerTruthReached
admissionCommitted
effectPossible
safeToRetry
reconcileRequired
addressableRecoveryIdentity
mechanicallyLegalRecoveryActions
```

The projection must not invent these values if the transport layer does not know them.

## Surface graduation test

A new wrapper/projection is earned only if all hold:

1. An observed Agent burden is repeated or structurally important.
2. The underlying responsibility already has a correct owner, or the ownership gap is separately proven.
3. A strong native/simpler baseline is measured.
4. The candidate reduces discovery/mechanical burden or materially improves correct action selection.
5. It does not duplicate mutable truth or hide effect/authority semantics.
6. A wrong-wrapper case still exposes the native escape hatch rather than guessing.
7. Recovery/currentness remains at least as explicit as before.
8. Cross-model or independent-agent evidence does not show the gain is model-specific.

If the candidate fails, narrow or delete it. “Looks cleaner” is not sufficient evidence.

## ACS3 consequence

The round should **not** implement an `AgentSurfaceManifest` protocol across all owners yet. The evidence supports a lighter convergence:

> owner-native semantic projections + common conformance questions + explicit currentness/effect/authority/recovery semantics.

Only after multiple owners independently need the same invariant should Computing consider protocol promotion.
