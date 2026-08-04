# P0 frozen evaluation baseline

This directory freezes the first cross-stack evaluation control plane for the selected Host, Harness, and Runtime revisions.

## Contents

- `system-manifest.json` binds the System Snapshot, evaluation schemas, failure taxonomy, and suite. Configuration fields that were not observed remain `null` and are listed under `unavailableFields`.
- `component-baseline.json` records four deterministic test suites and one Runtime acceptance-contract check. Its aggregate is 601 passed, 0 failed, and 22 explicitly ignored system tests. It sets `productQualityClaim` to `false`.
- `dogfood-summary.json` is a deterministic projection of the curated dogfood Task, Trial, Result, and Failure records. It generates no cross-task global score and currently admits no architecture comparison.

## Boundary

This baseline proves that the selected component revisions and evaluation contracts were healthy enough to begin formal Trials. It does not prove useful Agent work, model superiority, end-user value, production reliability, or readiness to tune prompts, tools, policies, or models.

The next valid measurement must use the same versioned Task and verifier across repeated configurations and bind a complete System Manifest for every Trial.
