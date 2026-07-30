# Ordivon repository naming

Ordivon is the shared brand. Platform repositories use:

```text
ordivon-<stable responsibility>
```

The suffix describes the state the project owns and its durable role in the system. It must not describe an implementation language, a temporary research phase, or a marketing slogan.

## Current matrix

| Repository | Stable responsibility | Does not own |
|---|---|---|
| `ordivon-computing` | System-level research structure, cross-layer architecture, protocols, reference implementations, conformance, evaluation, and cross-project synthesis | Production Tasks, Jobs, processes, or user-facing workspaces |
| `ordivon-runtime` | Durable trusted-local execution: Workspace, Job, Runtime Attempt, Artifact, cancellation, observation, and recovery | Model cognition, Goal planning, or product UI |
| `ordivon-host` | Durable Goal and Task continuity, Assignment and Task Attempt state, replaceable Harness coordination, deterministic admission, Runtime Dispatch correlation, verification, and task outcomes | Provider-specific Agent-loop internals, Linux process ownership, Runtime Job truth, protocol research, or user-interface presentation |
| `ordivon-world` | Task-conditioned external interaction: target, identity, path, transport, provider execution, conditioned evidence, uncertainty, reconciliation, and rebinding | Task strategy, trusted-local process lifecycle, native network/provider mechanisms, or domain verdicts |
| `ordivon-web` | Public website, project presentation, and documentation entrypoint | Private Goal/Task operations |
| `ordivon-workbench` | Planned user-facing review, approval, and Task interaction surface over Host contracts | Durable Task ownership, Linux process ownership, or protocol research |

Domain systems may retain a distinct product noun until a deliberate migration is completed. They must still declare their relationship to Ordivon in metadata and documentation.

## Candidate boundaries that are not repositories

`Ordivon Harness` currently names the replaceable cognitive-loop boundary among Model, Context, Skills, Tools, Session, and local subagents. It remains a Host-local interface and Computing research object. Do not create `ordivon-harness` until at least two live Harness adapters and two workloads demonstrate cross-Harness continuation, independent release value, and measurable duplicate-code reduction without Host or Runtime authority leakage.

## Naming rules

1. Use lowercase kebab-case for repository names.
2. Prefix Ordivon platform projects with `ordivon-`.
3. Choose one stable responsibility noun: `computing`, `runtime`, `host`, `world`, `workbench`, or `web`.
4. Do not use `core`; it is ambiguous across the Semantic Kernel, Runtime Core, and product core.
5. Do not use `platform`; it hides the actual state owner.
6. Use `computing` only for the system-level mother project that owns the research structure, architecture, protocols, reference systems, and conformance. Do not use `research` for a repository that also carries stable specifications and executable conformance.
7. Do not rename stable protocol namespaces merely to match branding. `ANC-*` issue IDs and `anc_*` packages remain the technical namespace for agent-native computing contracts.
8. Historical receipts, fixtures, revisions, and repository IDs remain immutable. Active validators may carry aliases for old identities.

## Migration order

```text
repository identity
→ active documentation and scripts
→ public website and project registry
→ local checkout and remotes
→ historical aliases and redirects
```

A repository rename must not rewrite exact historical evidence.
