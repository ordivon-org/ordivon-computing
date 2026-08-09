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

The closed question `ANC-EFFECT-001` is indexed in the research portfolio; its full historical narrative is Git-only. Current Tool-drift responsibility is summarized in the Computer responsibility map.
## 2026-08-10 recurrence: frozen Agent app snapshot

The same responsibility reappeared in a materially stronger form during P1-B. Owner-native Runtime `tools/list` exposed 19 Tools and `workspace.exec.executionTarget` / `windowsAuthority`; the current ChatGPT-loaded Ordivon Runtime app exposed 12 Tools and neither field. Owner-native Host `tools/list` exposed 6 Tools and `task.checkpoint.continuityDisposition`; the current ChatGPT-loaded Host app exposed 4 Tools and omitted that field. Re-listing app resources inside the same conversation did not change the loaded definitions.

This recurrence sharpens the earlier model:

```text
repository capability
!= deployed service
!= owner-native tools/list
!= approved / client-loaded app snapshot
```

The narrow operational rule is therefore: when an Agent-facing app uses a frozen approved Tool snapshot, server evolution requires explicit client/app adoption before new capabilities are usable. A live server catalog digest remains necessary evidence, but it is not proof of Agent-effective capability. Do not solve this by inventing a second central Tool registry; first use the app/provider's own refresh/review/republication boundary and then re-observe the client-loaded schema.

The exact P1-B observation is retained at `research/experiments/p1b-mcp-contract-freshness-v0/evidence/p1b-b0-58a945a.json`.
