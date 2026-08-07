# Agent-first Cross-cutting Infrastructure A1 Audit

Status: first bounded Content Identity acceptance complete; production promotion deferred.

Baseline revisions inspected:

| Owner | Revision |
| --- | --- |
| Computing | `70ec939e35f70b6847143d3216b03ca479550b90` |
| Runtime | `4bc563e6da83af50679149002d31507cbd703305` |
| Finance | `16fef54297ff137e793448b7612fe77e2fdb6fa7` |
| Security | `d3a9faf11f990ec2549fc178121dee6b9e99dac9` |
| Studio | `c881ccaaee3af7b4adce80a17d55fcfba8e5aa8b` |
| World | `f3ba26de70d8024df86dd5a0d2c215a66cd75fcd` |

A1 applies the infrastructure-promotion rule to the most repeated low-level cross-project candidate: exact byte identity and content-addressed mechanics.

## Executive decision

A shared **byte identity vocabulary** is supported by five materially different owners, but a shared Artifact object, content store, CAS authority, or repository is not.

The surviving candidate is only:

```text
ContentIdentity
  digest      sha256:<64 lowercase hex>
  byteLength  non-negative integer
```

Disposition:

| Candidate | Evidence | A1 decision |
| --- | --- | --- |
| exact-byte digest identity | Runtime, Finance, Security, Studio, World all bind SHA-256 content | retain candidate |
| exact byte length | all five current shapes retain exact bytes/size; useful independent transfer-integrity check | retain candidate |
| media type | same A1 bytes received different media-type descriptions across owners | delete from shared identity |
| owner object ID | Artifact/Sample/Asset/Evidence/provider identities encode different semantics | owner-local |
| storage locator/key | local CAS path, R2 key, Runtime Attempt bundle and provider key have different lifecycle | owner-local |
| ETag | provider transport/storage metadata only | World/provider-local |
| provenance/lineage/sighting | semantic evidence and transformation facts | owner/domain-local |
| rights/privacy/retention | policy, not byte identity | owner/domain-local |
| truncation/dropped bytes | Runtime capture semantics | Runtime-local |
| generic CAS writer | only Finance/Security substantially overlap and still have different safety/lifecycle obligations | not earned |
| central Artifact service | no independent state/lifecycle responsibility demonstrated | reject |
| independent repository | no release/deployment/security boundary demonstrated | reject |

## Real owner evidence

### Runtime

Runtime's current `CapturedOutput` records:

```text
artifact_id
file_name
digest
retained_bytes
dropped_bytes
truncated
```

The active production Runtime was used as the A1 probe executor. `/usr/bin/printf` emitted one 31-byte payload. The retained stdout Artifact had:

```text
digest        sha256:38d4c73aefebd392091298b44e3066f316e9e005420ae2ea6843b824e75e4f37
retainedBytes 31
```

Artifact ID, Attempt/Job binding, dropped bytes and truncation remain physical-execution semantics and are not common byte identity.

### Finance

`kernel/data_plane.py` uses SHA-256 content-addressed Evidence bytes with exact byte length and media type. The owner implementation additionally owns:

- `evidence://sha256/...` identity;
- source sightings;
- SQLite registration;
- storage class;
- immutable dataset fragments and lineage.

A current `DataPlane.put_evidence` call on the same A1 payload returned the same hash and length. Finance currently serializes the hash as bare lowercase hex plus `algorithm=sha256`; A1 normalizes this to the existing Ordivon `sha256:<hex>` digest form without changing Finance state.

### Security

`SampleIdentity` binds SHA-256, byte length, media type and optional original name. `SampleVault` additionally owns streaming import, private staging, `fsync`, atomic rename, `O_NOFOLLOW`, quotas, recovery and purge receipts.

`SampleVault.import_bytes` on the same payload returned the same hash and length. These stronger Vault obligations are a reason **not** to treat its storage implementation as a generic shared CAS.

### Studio

Studio already has the cleanest semantic split:

```text
BlobInfo = digest + sizeBytes + mediaType
Asset    = production role + provenance + rights + Blob selection
```

`hash_file` on the same bytes produced the same hash and length, but inferred `application/octet-stream` rather than the explicit media type used by Finance and Security. This is the decisive A1 falsifier against including media type in byte identity.

Studio's content-addressed R2 key convention is useful local policy, not proof of a shared object-store lifecycle.

### World

Cloudflare's current provider Artifact contract contains:

```text
key
sha256
bytes
media_type
etag?
```

The current `edge-receipt` JSON Schema accepted the A1 record with the same bare SHA-256 and length. The schema itself is bound in retained evidence by digest.

World requires provider request identity, Receipt reconciliation, generation/lease facts, R2 key and ETag semantics. Those cannot move into a shared Content identity without importing external-effect lifecycle.

## Cross-owner live result

Retained evidence:

`research/experiments/content-identity-v0/evidence/a1-content-identity-acceptance.json`

The five projections all produce:

```json
{
  "schemaVersion": 1,
  "kind": "ordivon.content-identity",
  "digest": "sha256:38d4c73aefebd392091298b44e3066f316e9e005420ae2ea6843b824e75e4f37",
  "byteLength": 31
}
```

The cross-cutting evidence contains no payload bytes and creates no writable state owner.

## Why the common object is smaller than the field intersection

A naive schema intersection would likely choose:

```text
digest
byteLength
mediaType
```

A1 rejects that method. Shared semantics must survive adversarial deletion, not merely appear in several structs.

Media type failed because the exact same bytes legitimately carried different owner descriptions. Likewise, a locator or object ID can change while bytes remain identical. Therefore shared equality is based only on exact content commitment and byte count.

This distinction matters for future Agents. An Agent may conclude:

> these two records refer to the same exact bytes

It may **not** conclude:

> they are the same Artifact, have the same meaning, are equally safe, have equivalent rights, or may be substituted in the current workflow.

Those stronger claims require owner/domain semantics.

## Storage-mechanics decision

A1 also tested whether repeated content addressing already justifies a shared `atomic_put`/CAS layer.

It does not.

- Finance couples Evidence storage to transactional Evidence registration and sightings.
- Security owns a substantially stronger private Sample Vault lifecycle.
- Studio does not currently own a generic persistent CAS implementation; it hashes Blobs and defines local/R2 layout policy.
- World stores provider-owned external Artifacts in R2 under request/lease lifecycle.
- Runtime stores execution-owned bounded Artifacts under Attempt lifecycle.

Only some filesystem mechanics overlap. Mature filesystem/R2/rclone mechanisms already own the physical operations. Extracting a shared storage authority would erase meaningful failure domains and increase coupling.

## Implementation result

A1 added only a Computing experiment:

```text
research/experiments/content-identity-v0/
├── content_identity.py
├── README.md
├── evidence/
└── tests/
```

`content_identity.py` is a read-only normalization experiment. It performs no writes and owns no bytes.

Current deterministic gate: **13 tests**.

The tests explicitly delete owner-only fields from equality and fail closed on digest/length disagreement, invalid algorithms, uppercase/malformed hashes, negative lengths and schema expansion.

## Promotion decision

The semantic candidate has strong multi-owner evidence, but production promotion into `packages/ordivon-protocol` is intentionally deferred.

Why:

1. Every current owner already has working byte identity.
2. The experiment has shown semantic convergence, but not yet recurring cross-repository consumer cost from maintaining separate normalizers.
3. Promoting a package would create a version dependency across product repositories; that cost must protect a demonstrated failure or repeated mechanical burden.
4. No owner needs to migrate its durable state merely to share this projection.

Promotion gate:

> At least two real cross-repository consumers use the common identity to remove repeated normalization or prevent a demonstrated integrity/correlation failure while preserving owner-local lifecycle semantics.

If that gate passes, promote only the strict wire/value primitive and conformance vectors into `ordivon-protocol`; keep storage and semantic objects in their owners.

## Repository decision

No new repository.

Even protocol promotion would remain inside the existing Computing `ordivon-protocol` package until independent versioning/release/deployment/security evidence makes extraction cheaper.

Explicitly rejected now:

```text
ordivon-artifact
ordivon-content-store
Artifact daemon
shared CAS database
global object locator
global retention authority
```

## Next A1 gate

A1 should reopen only for one narrow consumer test:

1. identify two real cross-repository call sites that currently normalize digest + length manually;
2. replace that repeated normalization through the candidate primitive or equivalent generated contract;
3. measure whether dependency and migration cost are lower than the repeated local code;
4. retain only if a real integrity/correlation failure or recurring maintenance cost disappears.

Until then the first A1 closeout is sufficient: **shared bytes, separate meaning, separate lifecycle.**

# A1.2 addendum — production consumer gate

A1.2 applied the promotion gate to two actual cross-repository consumers after the first semantic convergence result.

## Security / Runtime failure found

Security's P0-C Runtime-backed Harness path consumed Runtime Artifact descriptors containing `digest` and `retainedBytes`, then read the Artifact through Runtime `artifact.read`.

Before A1.2, Security compared the returned Runtime digest but accepted `eof=true` at any `nextOffset`. The following boundary state was reproduced and accepted:

```text
descriptor digest         = D
descriptor retainedBytes  = 31
artifact.read digest      = D
artifact.read nextOffset  = 10
artifact.read eof         = true
→ old Security consumer accepted
```

Runtime's current contract defines `nextOffset` as a byte offset and derives EOF from the authoritative Artifact byte length. Security therefore had enough facts to check the complete content identity without any Runtime change.

Security revision `ae6c3a3300946e73e065eea0b4fa5bf5b2538049` now requires exact EOF byte count equality. It adds no dependency and changes no Runtime authority. Early EOF and overshoot regressions are retained; the full 145-test unit suite passes.

## World / Cloudflare comparison consumer

World already had the desired behavior at its Browser boundary. It independently checks:

```text
Host ArtifactRef digest == Receipt sha256
retrieved content length == Receipt bytes
```

and separately verifies media type, provider key/generation, downloaded-body digest, PNG/UTF-8 structure and Manifest semantics.

World revision `d1f827030467ed6a06076fa0f4a3d12b621e4b50` adds a regression that mutates Receipt digest and byte count independently. Both are rejected by the existing production implementation. The full 28-test World suite passes; no production code changed.

## Promotion decision after two consumers

This is intentionally a **negative package-promotion result**.

The content-identity invariant is useful enough to expose a real cross-boundary bug, but the current reusable code surface is too small to justify a new production dependency:

- Security would move from zero declared production dependencies to a Computing protocol pin for a two-field value object;
- World would need a direct protocol dependency instead of relying on its existing Host dependency transitively;
- neither owner could delete domain/authority/lifecycle checks;
- the actual Security fix is four owner-local production lines;
- World needed only an additional regression test.

Therefore:

```text
shared semantic invariant   YES
shared production package   NOT YET
shared storage authority    NO
new repository              NO
```

The promotion gate is now stricter and more empirical: reopen only when at least two consumers exchange/persist the same strict serialized `ContentIdentity`, or repeated local normalization causes another material incompatibility/correctness failure. Mere repetition of `(digest, length)` comparisons is insufficient.

Retained A1.2 evidence lives at `research/experiments/content-identity-v0/evidence/a1-consumer-adoption-acceptance.json`.
