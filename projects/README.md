# Projects

This directory maps real projects into the Agent-Native Computing research stack. Each implementation repository remains the source of truth for its code, tests, Issues, releases, runtime state, deployment revision, and current capabilities.

## Project family

| Project | Stable role | Current authority | Public orientation |
| --- | --- | --- | --- |
| [Computing](https://github.com/zycxfyh/ordivon-computing) | shared theory, research state, promoted contracts, and conformance | [`docs/authority.md`](../docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Host](https://github.com/zycxfyh/ordivon-host) | durable Task continuity, commitments, verification, and outcomes | [Host authority](https://github.com/zycxfyh/ordivon-host/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Harness](https://github.com/zycxfyh/ordivon-harness) | caller-neutral Agent Runs, Provider adapters, Tool steps, durable Run continuity, and recovery | [Harness authority](https://github.com/zycxfyh/ordivon-harness/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Runtime](https://github.com/zycxfyh/ordivon-runtime) | physical local execution, Jobs, process state, Artifacts, and recovery | [Runtime authority](https://github.com/zycxfyh/ordivon-runtime/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Game](https://github.com/zycxfyh/ordivon-game) | Station Zero, authoritative game Worlds, player intervention, and replay | [Game authority](https://github.com/zycxfyh/ordivon-game/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [World](https://github.com/zycxfyh/ordivon-world) | retained Cloudflare adapter and private network operator tools | [World authority](https://github.com/zycxfyh/ordivon-world/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Human](https://github.com/zycxfyh/ordivon-human) | problem-driven human research, practical paths, methods, and limits | [Human authority](https://github.com/zycxfyh/ordivon-human/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Security](https://github.com/zycxfyh/ordivon-security) | bounded strategic adversarial experiments and evaluation | [Security authority](https://github.com/zycxfyh/ordivon-security/blob/main/docs/authority.md) | [Project directory](https://ordivon.com/projects) |
| [Web](https://github.com/zycxfyh/ordivon-web) | public orientation, publication, and dated interpretation | [Web authority](https://github.com/zycxfyh/ordivon-web/blob/main/content/editorial/authority.md) | [Public site](https://ordivon.com/) |

Use this table for navigation and stable role discovery. Use the owning repository for current implementation or research facts, and the public page for reader-facing orientation and maturity language.

## Project-family decisions

Cross-project ownership, admission, extraction, merge, and retirement rationale is indexed in [`decisions/README.md`](decisions/README.md). Decision records preserve why a boundary was considered or accepted, the alternatives and evidence, and the conditions that would reopen it.

A record under review does not create a project, replace mutable GitHub Issue state, or modify stable identity. [`registry.yaml`](registry.yaml) remains the only stable project-identity registry, and implementation work begins only after the decision reaches the required status and an owning repository or Issue exists.

## Truth hierarchy

When sources disagree about an implementation claim, use this order:

1. implementation code plus its tests, and exact-revision runtime or acceptance evidence;
2. contracts maintained in the implementation repository;
3. Issue and pull-request descriptions or discussion;
4. Ordivon Computing summaries, maps, and charters.

Evidence must remain bound to the revision and observation time that produced it. A lower source may summarize a higher source, but it cannot override it; stale Computing prose is corrected from implementation and runtime truth rather than treated as an independent maturity authority.

- [`registry.yaml`](registry.yaml) — stable project identities, roles, research branches, focus, and feedback sources;
- [`conformance.toml`](conformance.toml) — Protocol relationships and cross-project conformance profiles; repository URL and sibling path are derived from each stable project ID.

Neither file records mutable maturity, phase, deployment health, or a floating “latest revision.” In particular, the registry is not a maturity ledger. Those facts belong to the implementation repository, live runtime, or an immutable observation captured at a specific time.

The root conformance tool validates that every protocol participant exists in the broader project registry, captures exact local Git revisions, verifies the independent Host's full Computing Protocol package pin, verifies the Game's frozen vector-manifest pin, and emits digest-bound revision vectors or System Snapshots:

```bash
python3.12 scripts/ordivon_conformance.py manifest
python3.12 scripts/ordivon_conformance.py vector --require-all --require-clean
```

Protocol-path changes additionally run the bounded consumer gate against clean exact checkouts:

```bash
python3.12 scripts/check_protocol_consumers.py   --computing-root /path/to/ordivon-computing   --host-root /path/to/ordivon-host   --game-root /path/to/ordivon-game   --receipt /tmp/ordivon-protocol-consumers.json
```

This gate proves only released Artifact equality and the Host/Game contract suites. It does not turn Computing into a product CI controller, inspect unrelated product maturity, or run on ordinary research prose.

Cross-repository experiments bind exact repository commits, service binaries, Tool-contract digests, and evidence Artifacts through [`../research/evidence/system-snapshot.schema.json`](../research/evidence/system-snapshot.schema.json). A snapshot is historical evidence, not a mutable declaration of current system state.
