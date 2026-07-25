# Ordivon Versioned I/O Adapter

## Objective

Extend the semantic kernel from asynchronous process execution to versioned file observation, atomic mutation, independent verification, and Fact admission.

```text
current file state
→ versioned read Observation
→ compare-and-swap mutation
→ mutation receipt
→ independent reread Effect
→ Verification
→ Fact
```

## World identity

A file is addressed as a semantic world object:

```text
world_object:ordivon-file:<workspace-id>:<normalized-relative-path>
```

The adapter validates this identity before every Tool call. Workspace and relative path are therefore not merely transport arguments; they must agree with the Effect target.

## Versioned read

`workspace.read` produces structured content and a digest. The adapter independently hashes the UTF-8 content and rejects a malformed receipt whose reported digest differs.

```text
Effect prepared
→ Dispatch started
→ workspace.read
→ synchronous receipt admitted
→ Observation(target.version = file digest)
→ Effect succeeded
```

When the Effect requests an expected target version and the observed digest differs, the read Dispatch remains admitted and the Observation is preserved, but the Effect fails with `VERSION_MISMATCH`. World drift is evidence, not a missing result.

## Atomic mutation

The first mutation slice owns exactly one existing file and requires `expectedDigest`:

```text
workspace.mutate
mode = WRITE | APPEND | REPLACE_EXACT
expectedDigest = current version
```

This creates compare-and-swap semantics. A stale digest returns structured `INVALID_REQUEST`; the Dispatch is rejected and the Effect fails without changing the file. Transport or protocol uncertainty remains Dispatch=`unknown`, Effect=`unknown`, because the mutation may have crossed the world boundary.

## Synchronous receipt identity

Synchronous Tools do not return a durable Job ID. Their successful structured result becomes an admitted receipt:

```text
ordivon-receipt:<tool>:<dispatch-id>:<response-digest>
```

Dispatch identity is included so two identical reads remain distinct observations rather than colliding on response content.

## Independent verification

A mutation receipt proves that Ordivon accepted an atomic write. It does not by itself create a Fact about current world state.

The verification chain is therefore:

```text
Mutation Effect succeeded
→ Claim(file digest = afterDigest)
→ separate Read Effect
→ Observation(file digest)
→ Verification accepted or rejected
→ Fact only when accepted
```

The kernel permits Verification to reference an Observation produced by a different succeeded Effect, provided the world object, version, evidence kind, and time ordering satisfy the originating Effect's verification plan.

## Live evidence

Target: disposable Workspace `anc-semantic-io-target-20260726`, file `semantic-io-dogfood.txt`.

```text
Before digest: sha256:38165db00100bc3ea312f531375560543c391bfbcad75b722e06c6e2c8ad16a7
After digest:  sha256:08947d27245828547c51608be7c55bc831848ea23ed2af9ed62c5637e27437a6
Mutation receipt: ordivon-receipt:workspace.mutate:ordivon-io:e6cc74cf8c0cdf54:r2:5d1216c03fac5d0c0c08fa6d5ef972870f520026a6db3faf71b4777469424679
Reread Observation: observation:ordivon-io:6b4444516ac392d6:r2:240dd6b40470738a875c7ba8
Verification: verification:digest:dc1e3da00335d720fb901ef0
Fact: fact:digest:dc1e3da00335d720fb901ef0
Stale guard: failed / INVALID_REQUEST
```

## Remaining limits

- new-file creation is outside this slice because it lacks a prior file digest;
- multi-file mutation semantics are not yet generalized;
- unknown mutation reconciliation still needs a durable receipt or world-state comparison rule;
- file encoding is UTF-8 because current `workspace.read` is text-oriented;
- Tool contract identity and schema diff remain future work.
