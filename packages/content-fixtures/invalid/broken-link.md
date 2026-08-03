---
schema_version: 1
id: fixture.invalid.broken-link
title: Broken link fixture
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
# Broken link fixture

## Purpose

Retain a named link failure.

## Boundaries

The fixture is not documentation.

## Components

One missing target.

## Data flow

[Missing target](does-not-exist.md)

## Failure modes

The checker emits LINK001.

## Verification

The invalid fixture must not pass strict validation.
