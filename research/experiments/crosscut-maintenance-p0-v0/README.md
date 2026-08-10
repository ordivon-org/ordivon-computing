# Cross-cut maintenance P0 v0

Status: implementation and live acceptance target for Ordivon cross-cutting maintenance foundations.

This experiment deliberately does **not** create a daemon, writable global state, Tool registry, Loop engine, Graph authority, or garbage collector. It composes owner-native maintenance facts into a rebuildable Agent-facing view.

P0 responsibilities:

- **P0-A Maintenance Projection** — combine Host integrity, Runtime Workspace/cache lifecycle, Computing content lifecycle, compatibility debt and dirty aging without copying authority.
- **P0-B Compatibility Erasure** — every retained compatibility path must name a current consumer, protected durable state, recovery requirement or external contract; otherwise it is a deletion candidate.
- **P0-C Fast lifecycle evidence** — compare Runtime classification without byte walking against byte-measured scans before changing cadence.
- **P0-D Dirty aging** — old dirty Workspaces enter checkpoint/export, owner review or quarantine-review queues; dirty state is never automatically deleted.
- **P0-E Lifecycle vocabulary** — only `authoritative`, `evidence`, `rebuildable`, `ephemeral`, `cache`, `compatibility`, `quarantine`, and `unknown` are shared. Cleanup remains owner-local.

The key invariant is: **shared classification, separate authority**. A cross-cut projection may tell an Agent where friction exists; it cannot decide that Host, Runtime, Security, Finance, World or another owner may discard state.

Acceptance uses only standard-library deterministic tests plus one live receipt generated from current owner-native reports. The first compatibility-erasure dogfood removes the semantic-core experiment's `ReferenceKernel` / `JournalKernel` source aliases after repository-wide search proves their only consumers are the experiment's own compatibility tests. Historical `EffectSpec` Journal decoding remains because it protects retained durable evidence rather than source-name convenience.

## Accepted live result

The final P0 receipt is `evidence/p0-live-acceptance.json` with acceptance digest `sha256:2fc4c1c7bdf7e01db63de11c81b13b7f776035947d805c3e62eafb221534b427`.

The current projection composes ten signals without acquiring any of their authority: Host integrity; Runtime health/deployment, Workspace lifecycle, and execution cache; Computing content and conformance; World and Workstation owner doctors; compatibility debt; and dirty-Workspace aging.

Observed P0 facts at acceptance:

- production Runtime `44d5ebc01ad38a5fffbbc9ab8958bf0192d6345f` was healthy, active, restart-free, with 20 Tools, no Artifact mismatches, and no recovery-required Jobs;
- Runtime classified 4 active, 34 dirty, and 179 closable Workspaces; 92 were policy-eligible for owner reclaim, representing 4,717,169,549 estimated bytes;
- Runtime reported 34,990,803,873 legacy build-cache bytes with zero cache-integrity issues;
- three fast lifecycle scans had a 1.705 s median while the byte-measured scan took 6.180 s, a 3.63x slowdown, supporting hourly fast classification and daily byte measurement while authorizing no Runtime mutation;
- dirty aging classified 14 recent, 12 checkpoint/export, and 8 owner-review Workspaces; automatic dirty deletion remained false;
- World offline doctor was healthy; Workstation doctor was not, demonstrating that owner-native invariant conflicts can be surfaced without the cross-cut layer deciding which owner must change;
- Computing's complete conformance gate did not run to assertions because the current environment lacks Vale. The projection records `vale_missing` rather than treating unavailable validation as success;
- the first compatibility-erasure dogfood removed `ReferenceKernel` and `JournalKernel`, while historical `EffectSpec` Journal decoding remains because retained durable history still depends on it. The final compatibility summary is one removed, one justified retained, zero current removal candidates, and zero unsupported debt.

Deterministic validation at closeout: 14 P0 tests pass; the semantic-core experiment's complete 100-test suite passes after source-alias deletion; Ruff passes for the new P0 package and the directly edited semantic-core test/API surface. Existing broader `journal.py` Ruff modernization findings are outside this P0 and were not rewritten opportunistically.
