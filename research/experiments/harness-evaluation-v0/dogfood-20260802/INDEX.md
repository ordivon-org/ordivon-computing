# Curated Dogfood Evidence Index

This index covers the curated subset of the 2026-08-02 Harness dogfood and stress-test batch. It intentionally retains representative evidence rather than every successful or failed iteration.

## Counts

| Category | Files |
|---|---:|
| Original untracked inputs | 120 |
| Committed evidence records | 44 |
| Formal evidence | 13 |
| Diagnostic failure records | 24 |
| Supporting task definitions | 7 |
| Deleted after external backup | 76 |
| Exact duplicate groups | 0 |
| Canonical JSON duplicate groups | 0 |

## Representative formal evidence

- **Provenance repair:** one accepted, isolation-safe repair; the preceding verifier rejection is retained only as diagnosis.
- **Cancel stress:** one accepted cancellation-after-dispatch trajectory with Runtime Job binding preserved.
- **Resume stress:** one accepted duplicate-resume trajectory with one durable result.
- **Concurrent resume stress:** one accepted trajectory with durable Provider fencing and one recorded result.
- **Operator handoff:** one read-only capsule reconstructed identically across three fresh processes, with stale revision rejection.

## Retained diagnostic failures

- opaque Runtime Job identity rejected by Harness schema validation;
- hidden verifier/environment requirements after candidate completion;
- Tool `waitMs` contract drift at operator handoff;
- resume state loss;
- concurrent-resume `EventConflict` leakage;
- line-number versus UTF-8 byte-offset Tool contract drift.

Diagnostic records remain under `failures/` and are classified as `diagnostic_failure` in both the inventory and provenance manifest. They are not pass evidence.

## Machine-readable records

- [`inventory.json`](inventory.json) — disposition, summary, digest, revision, capture time, and rationale for all 120 original files;
- [`provenance-manifest.json`](provenance-manifest.json) — provenance and SHA-256 bindings for every committed evidence record;
- [`CURATION-REPORT.md`](CURATION-REPORT.md) — policy, duplicate analysis, deletion/recovery procedure, and remaining limitations.
