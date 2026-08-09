# P1-B MCP Contract Freshness v0

Status: B0 mismatch frozen; B1 explicit ChatGPT app snapshot refresh remains external to the current Agent tool surface.

This experiment implements P1-B from [`../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md`](../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md). It distinguishes four facts that must not be collapsed:

```text
repository capability
!= deployed/live service
!= owner-native tools/list
!= ChatGPT-loaded app snapshot
```

## B0 result

The owner-native live services are current and expose the expected contracts:

- Runtime `workspace.exec` includes `executionTarget` and `windowsAuthority`;
- Host `task.checkpoint` includes `continuityDisposition=continue|complete|abandon`;
- Runtime live catalog contains 19 Tools;
- Host live catalog contains 6 Tools.

The current ChatGPT session remains bound to an older app snapshot:

- `Ordivon_WSL_Operator` exposes 12 Tools and its `workspace.exec.execution` schema omits both Windows fields;
- `Ordivon_Host` exposes 4 Tools and its `task.checkpoint` schema omits `continuityDisposition`;
- re-requesting the installed app resources inside the same session does not change those loaded definitions.

This is classified as **client snapshot/adoption drift**, not server mismatch and not a Runtime/Host implementation defect.

## Product boundary discovered during B1

OpenAI's current custom MCP app model uses a frozen approved snapshot of available Tools and inputs. Server-side Tool changes do not automatically update that snapshot. An explicit app action refresh/review or app recreation/republication is required depending on the workspace/app publication mode. Therefore restarting Ordivon services or merely re-listing resources inside one existing ChatGPT session is not a valid refresh experiment.

P1-B1 now requires an explicit ChatGPT Apps-side refresh/rebuild of the two Ordivon app snapshots, followed by a **new chat** that re-observes the client-loaded definitions. This UI/admin operation is outside the current MCP tools themselves.

## Reproducible owner probe

`probe_live_catalog.py` reads the private local Bearer credentials only to query the loopback MCP origins. It emits no credential value or raw environment content.

```bash
python research/experiments/p1b-mcp-contract-freshness-v0/probe_live_catalog.py
```

The probe fails closed unless all three expected live fields are present.

## B1 success gate

After the explicit ChatGPT app refresh/rebuild, a fresh conversation must observe:

```text
Runtime client-loaded workspace.exec
  executionTarget   present
  windowsAuthority  present

Host client-loaded task.checkpoint
  continuityDisposition present
```

Tool-count equality is useful evidence but not sufficient by itself; field-level client schemas are the gate.

## B2 remains blocked

Do not run the ordinary connector `windows_native` smoke or close a Host continuity Task until B1 is proven from the refreshed client snapshot. Raw loopback MCP calls are diagnostic owner evidence only and cannot substitute for the Agent-facing connector test.

## Non-solutions

- no Runtime redeploy;
- no Host redeploy;
- no central Tool registry;
- no raw-MCP workaround presented as ordinary connector success;
- no attempt to smuggle fields through a stale client schema;
- no P0 live Trial while the Agent-facing contract remains stale.
