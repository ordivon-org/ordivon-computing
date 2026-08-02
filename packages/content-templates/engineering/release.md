---
schema_version: 1
id: project.release.version
title: Release title
type: release
profile: engineering
lifecycle: active
source_role: canonical
visibility: public
owners:
  - owning-project
audience:
  - user
  - integrator
updated: YYYY-MM-DD
summary: Exact released capability, compatibility boundary, and rollback path.
evidence_status: verified
readiness: READY
applies_to:
  - version
related: []
---
# Release title

## Release identity

State version, commit, artifact, and publication identity.

## Changes

Describe user-visible and contract-visible changes.

## Compatibility

State supported consumers, migrations, and known breaks.

## Verification

Link acceptance evidence and reproducible checks.

## Rollback

State the supported rollback or revert path.
