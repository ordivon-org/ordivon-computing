# External Semantic Contract v0 Specification

## Boundary

The experiment defines three public records and one canonical encoding:

```text
EffectEnvelope  — stable backend-neutral semantic intent
ToolContract    — one normalized executable interface revision
EffectBinding   — immutable intent-to-contract argument binding
BindingAdmission — minimal signed projection accepted by the Kernel
```

`EffectEnvelope` never contains provider operation names. `ToolContract` may contain `workspace.exec` or `simulator.job.launch`. `EffectBinding` references both digests and exact canonical arguments. The Kernel imports none of these packages and stores only `BindingAdmission` plus the Binding reference on `DispatchRecord`.

## Canonical encoding

`anc-canonical-json-v1` uses UTF-8, sorted object keys, compact separators, preserved array order, integer-only numbers, explicit null, and SHA-256 over exact canonical bytes. Duplicate keys, floats, NaN, Infinity, unsupported values, and unpaired Unicode surrogates fail closed. Public canonical encoding is independent of the Kernel Journal codec.

## Effect profiles

v0 freezes only:

```text
anc.object.read.v1
anc.object.replace-if-version.v1
anc.execution.launch.v1
```

Execution and completion are orthogonal. Idempotency exposes only `none` and `natural`. Preconditions, Task lineage, provider selection, scheduling, and keyed idempotency are outside v0.

## Contract compatibility

The differ returns:

```text
IDENTICAL
COMPATIBLE_EXTENSION
CALLER_ADAPTATION
SEMANTIC_BREAK
CAPABILITY_CHANGE
COMPLETION_CHANGE
UNKNOWN
```

Unsupported JSON Schema keywords and unproven equivalence produce `UNKNOWN`. A real Ordivon `schemaVersion` tightening from nonnegative integer/default 0 to `const: 1` is classified as `CALLER_ADAPTATION`.

## Binding decisions

```text
PROPOSED/PREPARED + caller adaptation → REBIND
PROPOSED/PREPARED + semantic break    → NEW_EFFECT
PROPOSED/PREPARED + capability change → REAUTHORIZE
DISPATCHED/RUNNING/UNKNOWN/RECONCILING → OBSERVE_ORIGINAL
SUCCEEDED/FAILED/CANCELLED             → KEEP
unknown compatibility                  → FAIL_CLOSED
```

Binding revision is not Dispatch retry. An active or uncertain Dispatch retains its original Binding.
