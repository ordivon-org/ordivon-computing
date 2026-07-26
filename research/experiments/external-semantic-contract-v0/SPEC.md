# External Semantic Contract v0 specification

## Public records

```text
EffectEnvelope   — stable backend-neutral semantic intent
ToolContract     — one normalized executable interface revision
EffectBinding    — immutable exact request binding
BindingAdmission — minimal signed projection accepted by the Kernel
```

`EffectEnvelope` never contains Provider operation names. `ToolContract` may contain `workspace.exec` or `simulator.job.launch`. `EffectBinding` binds the Effect digest, contract digest, encoder identity and exact canonical request arguments. Kernel state stores only `BindingAdmission` and the exact Binding reference on `DispatchRecord`.

## Canonical encoding

`anc-canonical-json-v1` uses UTF-8, sorted object keys, compact separators, preserved array order, integer-only numbers, explicit null, and SHA-256 over exact canonical bytes. Duplicate keys, floats, NaN, Infinity, unsupported values and unpaired Unicode surrogates fail closed. This encoding is independent of the Kernel Journal codec.

## Effect profiles

v0 freezes only:

```text
anc.object.read.v1
anc.object.replace-if-version.v1
anc.execution.launch.v1
```

Execution and completion are orthogonal. Public delivery requirements expose `none` and `natural`; concrete Tool contracts may provide stronger keyed correlation. Preconditions, Task lineage, Provider selection and scheduling remain outside v0.

## Authority and storage

Effect Authority signs the complete Effect digest. Binding Authority verifies that signature, the selected ToolContract identity/revision, action compatibility and canonical arguments before signing the Binding. The complete signed Binding is stored by `bindingDigest` outside Kernel state.

A Kernel admission is valid only if the stored Binding can be resolved and re-verified. At delivery time:

```text
actual Adapter request digest
=
canonical digest of resolved Binding arguments
```

Otherwise Dispatch admission fails before crossing the Tool boundary.

## Contract compatibility

The conservative classifier returns:

```text
IDENTICAL
COMPATIBLE_EXTENSION
CALLER_ADAPTATION
SEMANTIC_BREAK
CAPABILITY_CHANGE
COMPLETION_CHANGE
UNKNOWN
```

Unsupported JSON Schema keywords and unproven equivalence produce `UNKNOWN`. Current live MCP schemas are captured through `tools/list`; presentation metadata is excluded from contract identity, while execution-relevant schema and task-support changes alter the catalog revision.

## Binding decisions

```text
PROPOSED/PREPARED + caller adaptation  → REBIND
PROPOSED/PREPARED + semantic break     → NEW_EFFECT
PROPOSED/PREPARED + capability change  → REAUTHORIZE
DISPATCHED/RUNNING/UNKNOWN/RECONCILING → OBSERVE_ORIGINAL
SUCCEEDED/FAILED/CANCELLED              → KEEP
unknown compatibility                   → FAIL_CLOSED
```

Binding revision is not Dispatch retry. An active or uncertain Dispatch retains its original complete Binding. Alternative Backend candidates are not represented until a real selector workload requires them.
