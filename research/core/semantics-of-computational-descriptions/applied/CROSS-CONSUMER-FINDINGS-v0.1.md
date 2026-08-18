# Cross-Consumer Findings v0.1

Status: **derived applied findings / law candidates**, not Foundation claims.

## 1. Operational state is orthogonal to semantic currentness

Observed in A1/A2/A6:

```text
READY       != SemanticCurrent
COMPLETED   != SemanticCurrent
Installed   != CurrentlyExecutable
PreviouslyAdmitted != CurrentlyExecutable
```

The common pattern is not one universal state machine. A current semantic claim requires the owner/scope/version/dependency support appropriate to that claim.

## 2. No Silent Carry-Forward — applied obligation

If an unqualified semantic claim depends on a current authority/version/interface and that support changes, preserving some historical/operational fact does not preserve the stronger semantic claim automatically.

This is currently an obligation schema, not a novel theorem. TMS/ATMS, provenance/versioning and capability systems provide important precedent.

## 3. Preservation has multiple regimes

Round 1 distinguishes at least:

### Historical preservation

Old claim/result remains addressable and valid as history while losing current authority.

### Referential/recoverable preservation

A bounded handoff need not duplicate full semantic content if it retains an exact authoritative reference that can reconstruct the required current semantic state before action.

### Abstract/claim-selective preservation

A summary may preserve one observation/claim class while discarding support needed for stronger claims.

### Projection fidelity

An Agent-visible view can preserve exact selected/current cognition only through current provenance/digest/interface correspondence, not text similarity.

### Capability currentness

A capability claim can stand only at the exact admission layer and current turn/scope that supports it.

These regimes must not be flattened into one `preserved=true` flag.

## 4. Exact bytes are neither necessary nor sufficient for semantic preservation

Round 1 reinforces:

- content duplication is not necessary when authoritative exact recovery exists;
- byte/text similarity is not sufficient for current WorkingView or semantic-currentness claims.

## 5. Current cognition is not history

Harness dogfood provides a concrete multi-layer distinction:

```text
canonical history
materialized source
selected durable cognition
interaction-local cognition
attempt-local Tool cognition
current model-visible view
```

These are related but non-identical truth roles.

## 6. G1 — Multi-framework semantic-obligation coordination remains live

A5 combines cognition selection, projection, privacy, caller ingress, Tool evidence and current action authority. Existing owner frameworks supply local rules, while SCD may have a useful role in coordinating the claim/correspondence/dependency obligations across them.

No universal semantics is justified.

## 7. G2 — Owner-typed dependency currentness gained real pressure

A1/A2 show external semantic owner authority changing while Host continuity facts remain unchanged. A6 shows turn-local action authority changing while an installed mechanism remains unchanged.

The candidate gap is not dependency revision itself; it is the disciplined coordination of semantic claim standing across owner-typed/versioned authority references without copying or minting authority.

Targeted comparison with truth-maintenance, provenance, capability and versioned-specification systems is required before novelty is claimed.

## 8. G4 — correspondence composition gained real pressure

A3 requires a chain resembling:

```text
bounded handoff reference
  -> authoritative Host resolution
  -> exact checkpoint recovery
  -> safe continuation claims
```

A5 similarly composes source identity, WorkingSet projection, model-view binding and independent Continuity validation.

The open question is when heterogeneous correspondences can compose into a valid standing transport and what obligations block composition. Existing simulation/morphism/institution/refinement composition theory must be checked first.

## 9. No Foundation-level result

Round 1 does not change current SCD Foundation standing or closure. Consumer success/failure remains evidence and falsification pressure only.
