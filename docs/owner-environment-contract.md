# Owner Environment Contract

## Purpose

A green warmed Workspace is execution evidence for that Workspace; it is not proof that an owner repository can reconstruct the environment required to test or operate its current source. Each active owner therefore owns its own environment declaration and materialization path. Runtime preserves Workspace isolation; Computing provides only this cross-owner discoverability/conformance vocabulary and does not own another repository's dependency graph.

## Required semantic surface

An active owner SHOULD expose an executable root entrypoint at `scripts/owner-environment` with four bounded modes:

- `bootstrap` — materialize repository-declared dependencies into an owner-local environment. It may use uv, npm/pnpm, Cargo, system-package probes, or another owner-appropriate mechanism.
- `doctor` — verify the already-materialized environment and fail closed on missing/wrong versions or missing required substrate. It must not silently repair.
- `test` — bind the tests it selects to their required dependency profile. It may call `bootstrap` first so a first invocation succeeds for dependency reasons instead of discovering packages by failure.
- `cold-start` — run the same default test contract in a fresh environment with no reliance on a previously warmed `.venv`, `node_modules`, `PYTHONPATH`, or globally installed project packages.

The interface is shared for Agent discoverability; implementation remains owner-local. A repository may expose additional profiles such as `capability:cage`, `resolve`, `audit`, or live/reality tests. Expensive or authority-bearing capability dependencies need not enter the default profile. Tests that require one must bind it explicitly.

## Applicability

The contract is capability-driven, not a central owner allowlist. `scripts/check_owner_environment_contract.py` derives executable pressure from repository-local evidence such as a root build/package manifest, executable code roots, tests, or executable scripts. If such pressure exists, the contract is `REQUIRED`; absence of the entrypoint is a failure. A repository with no executable pressure is reported as `NOT_APPLICABLE`, not as green environment evidence. If that repository later gains code, tests, or a build surface, applicability changes automatically and it must acquire the contract. This avoids manufacturing empty virtual environments for research/representation-only owners while also avoiding a stale hand-maintained registry.

## Dependency roles

Owners should distinguish at least these roles when they exist: runtime, test/dev, audit, capability-specific, system/substrate, and external-service/tool dependencies. A lock or exact immutable source pin should cover materialized software dependencies where practical. Global installation is not a substitute for an owner declaration because it masks missing dependencies in clean environments.

## Admission rule

A dependency-related repair is not closed by `Workspace tests green` alone. The stronger evidence is:

```text
fresh source fence
  -> owner-environment cold-start
  -> bootstrap materializes declared profile
  -> doctor validates that profile
  -> default tests pass
```

This proves environment reproducibility only for the selected profile and source fence. It does not prove live services, credentials, hardware, network availability, domain semantics, or deployment currentness. Those remain with their owners.

## Anti-coupling rules

Computing must not centralize owner dependencies. Runtime must not install domain packages merely to make Workspace tests pass. Host continuity must not imply environment readiness. A shared workstation may cache packages or toolchains, but cache presence is acceleration rather than authority.

`scripts/check_owner_environment_contract.py` performs static applicability plus entrypoint discoverability. `DISCOVERABLE` means the required semantic surface is exposed; `NOT_APPLICABLE` means no executable pressure was detected and is not environment-readiness evidence. Dynamic reproducibility evidence comes only from each applicable owner's `cold-start` mode.
