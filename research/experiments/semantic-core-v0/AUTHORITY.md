# Authority and Attestation Boundary v0

## Purpose

M2.5 turns the Semantic Core from one shared mutation surface into a role-scoped admission system.

```text
Effect proposer          → EFFECT Authority
Execution Adapter        → DISPATCH + OBSERVATION Authorities
Verifier                 → VERIFICATION Authority
Fact acceptor            → FACT Authority
Readers                  → read-only Kernel View
```

Every accepted mutation is signed before it reaches the reducer. The reducer verifies the role, grant, exact semantic content, record time, and contract version before changing state.

## Authority Grant

An `AuthorityRef` records:

```text
authority_id
issuer_id
principal_id
role
trust_domain
policy_version
key_id
issuer_signature
```

The root `AuthorityPolicy` signs the grant. A grant establishes which principal may exercise one semantic role inside one trust domain under one policy version.

## Per-authority signer

The root policy derives a distinct HMAC key for every issued Authority. A role-scoped Kernel View receives only the signer derived for its own Authority.

This produces two enforced properties:

1. an EFFECT signer produces valid EFFECT attestations;
2. the same signer cannot produce a valid DISPATCH, OBSERVATION, VERIFICATION, or FACT authority chain.

The root policy remains in the trusted bootstrap. Runtime consumers receive scoped signers rather than the root signing capability.

## Attestation

An `Attestation` binds:

```text
AuthorityRef
AttestationKind
contract_version
subject_digest
issued_at_ms
signature
```

The subject digest is computed over the exact semantic operation, positional arguments, and keyword arguments. Changing an Effect, Dispatch identity, backend operation identity, evidence digest, Observation payload, Verification decision, Fact reference, or timestamp changes the subject digest and invalidates the attestation.

## Role matrix

| Role | Authorized mutations |
|---|---|
| EFFECT | admit and prepare Effect |
| DISPATCH | begin/admit/reject Dispatch, preserve UNKNOWN, advance execution state |
| OBSERVATION | record Observation and Artifact |
| VERIFICATION | admit Claim and record Verification |
| FACT | accept Fact |

The standard bootstrap returns five scoped views:

```text
views.effects
views.execution      # DISPATCH + OBSERVATION
views.verification
views.facts
views.read
```

There is no public full-authority convenience view.

## Adapter boundary

Ordivon Adapters receive only `views.execution`.

They can:

- begin and reconcile Dispatches;
- bind backend Job or receipt identity;
- preserve uncertain outcomes;
- record attested Observations and Artifacts;
- advance execution state from observed backend evidence.

They do not receive Effect proposal, Verification, or Fact authority.

## Knowledge admission boundary

Digest verification receives two separate handles:

```text
verify_digest_fact(
    views.verification,
    views.facts,
    ...
)
```

The Verification and Fact records therefore carry distinct Authority identities even when one deterministic helper coordinates the transaction.

## Durable replay

Journal schema v2 stores Authority grants and Attestations with every semantic command and evidence object. Journal metadata binds:

```text
journal_schema_version
semantic_model_version
reducer_version
authority_policy_fingerprint
```

Replay performs the same checks as live admission:

```text
decode command
→ verify grant signature
→ verify required role
→ recompute semantic subject digest
→ verify attestation signature and time
→ apply reducer transition
→ validate complete projection
```

A journal opened with a changed policy identity is rejected before replay. A journal opened with the wrong secret fails signature verification during replay.

## Key custody

The root authority secret is supplied by runtime configuration and is not stored in the Journal. Process-restart recovery supplies the same secret to the new Kernel process, allowing the complete authority chain to be re-authenticated.

## Executable evidence

The M2.5 conformance suite proves:

- `AuthorizedKernel` can only be issued by `AuthorityRoot`;
- public bootstrap exposes only scoped Views;
- one role cannot call another role's mutations;
- a role-specific signer cannot escalate into another role;
- forged grants are rejected;
- altered semantic content invalidates its Attestation;
- caller-supplied evidence attestations are replaced by trusted issuance;
- attestation provenance survives Journal replay;
- changed policy identity and wrong secrets are rejected;
- Verification and Fact acceptance retain distinct Authority identities;
- Ordivon projections return the official attested records stored by the Kernel.
