# ANC-EFFECT-001 — Tool-Contract Change Detection and Adoption

## Question

How can a Host, model, and live Runtime detect, understand, and adopt Tool-contract changes during a long-lived task while preserving already completed work and active executions?

## Triggering observation

A live MCP Runtime required:

```json
{"type":"integer","const":1,"minimum":1,"maximum":1}
```

while the active model-visible schema still allowed:

```json
{"type":"integer","minimum":0}
```

The same Tool therefore had different executable contracts across the model, Host snapshot, and live service.

## Current hypothesis

```text
normalize executable Tool catalog
→ compute stable catalog identity
→ bind Task or session
→ detect later identity change
→ produce semantic diff
→ rebind pending Effects
→ preserve completed Facts and active execution identities
```

Change classification should distinguish compatible extension, caller adaptation, semantic change, and capability change.

## First artifact

Build a catalog normalizer and differ that can detect the observed field narrowing and emit a machine-readable compatibility result. Connect it to a small rebind simulation for pending, completed, and running Effects.

## Evidence

- reproducible detection of normalized contract changes;
- correct classification of the known schema tightening;
- successful re-encoding of a pending call;
- continued observation of an already running Job;
- explicit treatment of semantic changes not visible in JSON Schema alone.

## Related material

- [`../../knowledge/agents/tool-contracts-and-world-interfaces.md`](../../knowledge/agents/tool-contracts-and-world-interfaces.md)
- [`../../knowledge/cases/tool-contract-drift.md`](../../knowledge/cases/tool-contract-drift.md)
- [`../../studies/2026-computing-stack-walkthrough/14-world-interfaces.md`](../../studies/2026-computing-stack-walkthrough/14-world-interfaces.md)
- Ordivon
