# Architecture

## Ownership

| Component | Owns | Must not own |
|---|---|---|
| `anc_canonical` | strict public JSON bytes and SHA-256 digest | Agent semantics, Kernel state |
| `anc_effect_ir` | signed backend-neutral `EffectEnvelope` | Tool names, Dispatch, catalog selection |
| `anc_tool_contract` | normalized executable interface identity | Effect lifecycle, recovery |
| `anc_effect_binding` | immutable Effect-to-contract arguments and external storage | actual delivery, Backend state |
| integration | Authority chain, Kernel projection and Adapter request enforcement | canonical Kernel state |

## Dependency direction

```text
anc_canonical imports no project package
anc_effect_ir imports anc_canonical only
anc_tool_contract imports anc_canonical only
anc_effect_binding imports the three packages above
Semantic Kernel source imports none of these packages
integration may import external packages and Kernel protocols
```

## One Effect truth

```text
EffectEnvelope
    ↓ one-way projection
KernelEffectProjection
```

`EffectEnvelope` is the public semantic record. `KernelEffectProjection` is an internal Kernel v0 projection and is not reversible into the complete public record. New Kernel state stores the semantic action once through its capability projection; Provider operations remain in `ToolContract` and `EffectBinding`. Historical `EffectSpec` Journal records remain decodable through a non-exported compatibility alias.

## Binding trust chain

```text
signed EffectEnvelope
        ↓ Effect Authority verification
normalized ToolContract
        ↓ identity and revision verification
exact EffectBinding arguments
        ↓ Binding Authority signature
content-addressed signed Binding artifact
        ↓ minimal projection
BindingAdmission
━━━━━━━━ Semantic Kernel boundary ━━━━━━━━
Dispatch(binding_id, binding_digest)
```

Complete Tool schemas, encoder identity and request arguments stay outside Kernel state. The Binding digest is both the immutable Kernel reference and the content-addressed lookup key. Resolution re-verifies Authority, Effect identity, revision and supersedes edges. Missing, corrupt or forged artifacts fail closed.

Before a real Adapter calls `begin_dispatch`, `BoundExecutionView` requires the actual request digest to equal the canonical digest of the resolved Binding arguments. A Binding reference without request equality is insufficient.

## Catalog scope

The current implementation captures selected Ordivon MCP contracts from `tools/list` and retains a normalized snapshot. It is not a resident catalog service or automatic Provider selector. Binding alternatives remain deferred; one selected Binding lineage crosses the Kernel edge.
