# Architecture

## Ownership

| Package | Owns | Must not own |
|---|---|---|
| `anc_canonical` | one strict JSON encoding and SHA-256 digest | Agent semantics, Kernel state |
| `anc_effect_ir` | stable backend-neutral intent | Tool names, Dispatch, catalog selection |
| `anc_tool_contract` | executable interface identity and compatibility | Effect lifecycle, recovery |
| `anc_effect_binding` | immutable Effect-to-contract argument binding | actual delivery, Backend state |

## Dependency rules

```text
anc_canonical imports no project package
anc_effect_ir imports anc_canonical only
anc_tool_contract imports anc_canonical only
anc_effect_binding imports the three packages above
Semantic Kernel imports none of these packages
conformance may import every component
```

## Kernel edge

Only this stable projection crosses into the Kernel:

```text
binding_id
effect_id
effect_digest
binding_digest
binding_revision
Binding Authority Attestation
```

Tool schemas, encoder code, provider operation names, catalog state, and arguments remain outside Kernel state.
