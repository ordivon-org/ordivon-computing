# Workspace Claimant Discoverability v0 — experiment apparatus

Status: preregistered apparatus candidate; not production code.

Purpose: construct an exact read-only mechanical oracle over current Host Task-head WorkingCheckpoint Workspace references and compare it with candidate reverse-query implementations.

The apparatus deliberately does **not** decide semantic owner/claimant truth.

## Inputs

- Host state root containing `host.sqlite3` and CAS `objects/`.
- Runtime Workspace root used only for local physical-existence comparison.
- Optional exact `--workspace-id` filter.

## Oracle truth role

`current-host-task-head-runtime-navigation-reference`

An empty result means only that no current Host Task head in the scanned scope explicitly names the Workspace. It never means `unclaimed`.

## Protected classifications

- `EXPLICIT_READY_REFERENCE`
- `TERMINAL_HEAD_REFERENCE_ONLY`
- `NO_CURRENT_HEAD_REFERENCE`
- `EXPLICIT_READY_REFERENCE_PHYSICALLY_CURRENT`
- `EXPLICIT_READY_REFERENCE_PHYSICALLY_ABSENT`

## Phase order

1. Freeze current source revisions and observation time.
2. Run `offline_projection.py --summary` and preserve its output as the mechanical census.
3. Freeze benchmark manifest before running a candidate Host implementation.
4. Compare candidate result sets exactly against oracle rows.
5. Run semantic/owner adjudication separately; do not write those labels back into the Host oracle.

## Non-goals

- no Runtime mutation;
- no Host Journal mutation;
- no Workspace cleanup;
- no owner inference from filenames;
- no global relation graph;
- no production MCP changes.
