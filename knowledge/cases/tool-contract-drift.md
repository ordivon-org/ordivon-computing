# Case: Tool Contract Drift

## Observed case

A live MCP runtime exposed a tightened field contract:

```json
{
  "type": "integer",
  "const": 1,
  "minimum": 1,
  "maximum": 1
}
```

The active model-visible Tool schema still allowed:

```json
{
  "type": "integer",
  "minimum": 0
}
```

A call containing `schemaVersion: 0` was valid under the visible schema but rejected by the live runtime.

## Distributed contract state

The effective Tool contract existed simultaneously in several places:

```text
model-visible schema
approved application snapshot
Host Tool catalog
live MCP runtime
```

The system did not share one atomic contract state. The failure was therefore contract drift across components, not simply an invalid model choice or a broken server.

## Minimal change detection

The relevant difference is a real narrowing of the accepted input set:

```text
minimum 0
→ exactly 1
```

A durable Host can normalize executable Tool definitions, compute a catalog identity, and bind a task or session to that identity.

```text
normalize catalog
→ hash or revision
→ bind
→ compare before later execution
```

When the identity changes, the Host can produce a semantic diff and re-encode pending Effects under the new contract.

## Change classes

Useful classes include:

- compatible extension, such as an optional output field;
- caller adaptation, such as a new required value or narrower range;
- semantic change, where structure remains similar but world behaviour changes;
- capability change, where the action space expands or contracts.

The third and fourth classes require more than raw JSON Schema comparison.

## Continuity rule

Contract adoption should preserve already-observed facts and running executions:

```text
pending Effect
→ rebind to the new contract

completed Effect
→ preserve its result

active long-running Job
→ continue observation by stable execution identity
```

The research question is tracked as [`../../research/questions/ANC-EFFECT-001-tool-contract-evolution.md`](../../research/questions/ANC-EFFECT-001-tool-contract-evolution.md).
