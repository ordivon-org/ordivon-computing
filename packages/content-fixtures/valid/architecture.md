---
schema_version: 1
id: fixture.valid.architecture
title: Valid fixture architecture
type: architecture
profile: engineering
lifecycle: active
source_role: canonical
visibility: internal
owners:
  - ordivon-fixture
audience:
  - maintainer
updated: 2026-08-03
---
# Valid fixture architecture

## Purpose

Protect the accepted architecture document shape.

## Boundaries

The fixture has no external effect.

## Components

One document and one checker.

## Data flow

Fixture to parser to receipt.

## Failure modes

Missing metadata or sections cause a strict failure.

## Verification

The unit test checks a receipt whose readiness field is `READY`.
