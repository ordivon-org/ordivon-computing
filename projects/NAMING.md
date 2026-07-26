# Ordivon repository naming

Ordivon is the shared brand. Platform repositories use:

```text
ordivon-<stable responsibility>
```

The suffix describes the state the project owns and its durable role in the system. It must not describe an implementation language, a temporary research phase, or a marketing slogan.

## Current matrix

| Repository | Stable responsibility | Does not own |
|---|---|---|
| `ordivon-architecture` | Cross-layer architecture, specifications, reference implementations, conformance, and evaluation | Production Tasks, Jobs, processes, or user-facing workspaces |
| `ordivon-runtime` | Durable trusted-local execution: Workspace, Job, Attempt, Artifact, cancellation, observation, and recovery | Model cognition, Goal planning, or product UI |
| `ordivon-edge` | Connectivity, transport observation and selection, recovery, and remote Runtime reachability | Task semantics or local process ownership |
| `ordivon-web` | Public website, project presentation, and documentation entrypoint | Private Goal/Task operations |
| `ordivon-workbench` | Planned user-facing Agent Host, thin Task controller, review, and approval surface | Linux process ownership or protocol research |

Domain systems may retain a distinct product noun until a deliberate migration is completed. They must still declare their relationship to Ordivon in metadata and documentation.

## Naming rules

1. Use lowercase kebab-case for repository names.
2. Prefix Ordivon platform projects with `ordivon-`.
3. Choose one stable responsibility noun: `architecture`, `runtime`, `edge`, `workbench`, or `web`.
4. Do not use `core`; it is ambiguous across the Semantic Kernel, Runtime Core, and product core.
5. Do not use `platform`; it hides the actual state owner.
6. Do not use `research` for a repository that also carries stable specifications and executable conformance.
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
