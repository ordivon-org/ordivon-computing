# Content Identity v0

Status: A1 first bounded acceptance passed. The experiment retains only a candidate cross-owner byte identity; no shared store, service, repository, or production protocol promotion is admitted yet.

## Question

Runtime, Finance, Security, Studio, and World all need to bind exact bytes, but each owner attaches different semantics and lifecycle. A1 asks what remains after those semantics are deleted.

The current candidate is deliberately small:

```text
ContentIdentity
├── digest      sha256:<64 lowercase hex>
└── byteLength  non-negative integer
```

`ContentIdentity` means only: **these records claim the same exact byte sequence**. It does not mean the bytes are truthful, safe, authorized, retained, public, executable, evidentiary, or semantically equivalent.

## Owner comparison

| Owner | Native object | Byte fields used by A1 | Fields deliberately left owner-local |
| --- | --- | --- | --- |
| Runtime | captured/result Artifact | `digest`, `retainedBytes` | Artifact ID, Job/Attempt, dropped bytes, truncation, terminal semantics |
| Finance | `EvidenceArtifact` | `algorithm=sha256`, `digest`, `byteLength` | evidence ref, sighting, source, storage class, analytical lineage |
| Security | `SampleIdentity` / `SampleVault` | `sha256`, `byteLength` | Sample ID, original name, authority, quarantine, Vault quotas/purge |
| Studio | `BlobInfo` / Asset Blob | `digest`, `sizeBytes` | Asset role, provenance, rights, alternatives, production meaning |
| World | provider Artifact reference | `sha256`, `bytes` | provider key, ETag, Receipt, lease generation, request identity |

The representations are intentionally not rewritten in owner repositories. `content_identity.py` contains read-only projections from each current shape into the candidate common identity.

## A1 dogfood

One 31-byte payload was passed through five current owner paths/contracts without copying the payload into retained cross-cutting evidence.

- **Runtime**: the active production Runtime executed `/usr/bin/printf`; its real stdout Artifact retained 31 bytes with digest `sha256:38d4c73a...e75e4f37`.
- **Finance**: current `DataPlane.put_evidence` wrote the payload through the owner-native SQLite/content-addressed Evidence path and returned the same digest and length.
- **Security**: current `SampleVault.import_bytes` streamed the payload into its private Vault and produced the same `SampleIdentity` digest and length.
- **Studio**: current `hash_file` produced the same digest and length.
- **World**: the current `edge-receipt` Artifact JSON Schema accepted the same bare SHA-256 and byte count with provider-local key, media type, and ETag.

The retained acceptance is [`evidence/a1-content-identity-acceptance.json`](evidence/a1-content-identity-acceptance.json). It binds the inspected owner revisions and the current World Artifact Schema digest.

### Media type falsifier

The same bytes were not described with one media type:

```text
Finance   application/x-ordivon-a1
Security  application/x-ordivon-a1
Studio    application/octet-stream
World     application/x-ordivon-a1
Runtime   no media-type field in the captured Artifact shape
```

Therefore media type is not admitted into byte identity. It remains useful owner-native descriptor metadata.

The same deletion rule excludes storage location/key, ETag, Artifact/Sample/Asset identity, source/sighting, rights, truncation, policy, retention, and lifecycle state.

## Why byte length remains

A SHA-256 digest is the cryptographic content identifier. `byteLength` is retained as a cheap independent transfer/integrity bound because every accepted consumer already records the exact retained byte count or equivalent size and because a digest/length disagreement should fail closed as corrupt metadata rather than normalize silently.

The shared representation embeds the algorithm in the digest string (`sha256:...`). Finance and World currently use bare SHA-256 fields plus owner-local algorithm/schema context; the A1 projection normalizes those forms without changing owner storage.

## What did not survive deletion

A1 does **not** retain a common:

- `Artifact` object;
- media-type authority;
- storage locator or object key;
- provenance or lineage record;
- retention/privacy class;
- evidence meaning;
- Asset/Sample semantics;
- CAS database;
- generic object-store writer;
- R2/filesystem abstraction;
- backup or garbage-collection lifecycle.

The local storage implementations are materially different. Finance performs atomic local Evidence registration coupled to its control plane. Security's Vault additionally owns streaming import, no-follow safety, quotas, manifests, recovery and purge receipts. Studio primarily hashes and derives content-addressed R2 keys. World binds remote provider Artifacts to Receipts. Runtime creates bounded execution Artifacts inside Attempt lifecycle. Field similarity does not justify central storage authority.

## Acceptance

Run:

```bash
/usr/bin/python3 -m unittest discover \
  -s research/experiments/content-identity-v0/tests \
  -p 'test_*.py' -v
```

The current suite has thirteen deterministic tests. It checks the five owner projections, retained live/contract evidence, digest-format normalization, fail-closed digest/length mismatches, and deletion tests proving that media type and owner lifecycle fields are not part of the candidate identity.

## Disposition

Retain **as a Computing experiment**:

```text
ordivon.content-identity
{ digest, byteLength }
```

Do not promote it into `ordivon-protocol` yet. Existing owner records already work, and A1 has so far proven semantic convergence, not enough recurring cross-repository consumer cost to justify a production package migration.

Promotion gate:

> At least two real cross-repository consumers must use the common identity to remove repeated digest/length normalization or prevent a demonstrated integrity/correlation failure, without importing owner lifecycle semantics.

Even after protocol promotion, repository extraction is a separate decision. No `ordivon-artifact`, shared Artifact daemon, central CAS, or new object-storage authority is justified by A1.

## A1.2 — consumer adoption / promotion test

A1.2 tested whether the semantic candidate already justifies a production package dependency.

Two real cross-repository consumers were used.

### Security ← Runtime

`ordivon-security` consumes Runtime terminal Artifact descriptors and retrieves their content through `artifact.read`.

The pre-fix consumer verified the descriptor/read digest on every chunk but accepted `eof=true` without proving that the final Runtime byte offset equaled descriptor `retainedBytes`. A deterministic reproduction declared a 31-byte Artifact, returned the same digest, stopped at byte offset 10 and reported EOF. The old Security consumer accepted the partial read.

Security fixed this owner-local boundary: EOF now requires `nextOffset == retainedBytes`. Early EOF and overshoot both fail closed. The complete Security unit suite passed 145 tests after the change.

This is a concrete example of why A1 retained both digest and byte length: digest metadata equality alone did not prove complete byte consumption.

### World ← Host / Cloudflare

`ordivon-world` already performs the equivalent pair of checks while reconstructing Browser bundles: Host Artifact digest must match the Cloudflare Receipt, and downloaded Artifact byte count must match the Receipt byte count. A new regression test mutates each field independently and proves both mismatches fail closed. The complete World suite passed 28 tests.

World also retains media type, provider key, Receipt and browser semantics as separate checks. A1 therefore did not replace this boundary with a generic Artifact object.

Retained evidence: [`evidence/a1-consumer-adoption-acceptance.json`](evidence/a1-consumer-adoption-acceptance.json).

### Promotion result

The semantic candidate survives, but package promotion does not.

- Security currently declares zero production dependencies. Importing a generic `ContentIdentity` from `ordivon-protocol` would add a cross-repository production/version dependency to replace a four-line owner-local correctness check.
- World receives `ordivon-protocol` only transitively through Host. A correct direct import would require another explicit protocol dependency/pin even though World production code already enforces the invariant.
- Neither consumer would delete its owner lifecycle, Receipt, media-type, truncation, authorization or storage checks.
- The observed Security bug was removed without any new shared state or production dependency.

Therefore A1.2 rejects promotion into `ordivon-protocol` for now. The shared semantic vocabulary remains a Computing experiment. Reopen only when at least two production consumers need the same **serialized** content-identity object across a wire/stored contract, or another incompatible local normalization produces a demonstrated cross-project failure.
