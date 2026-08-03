# Harness Dogfood Evidence Curation Report

## Scope

The curation started from 120 untracked files in `ordivon-computing` at revision `67076892dfde6f032ff5fe8636ed07bfd73b782c`. The batch contained raw Host/Harness evidence, evaluation Task/Trial/Result/Failure projections, stress-test iterations, and a one-off projection generator.

No protocol, core research, content-engineering implementation, or other repository was modified.

## Recovery-first handling

Before any deletion, all 120 originals were archived outside the repository as `untracked-evidence.tar.gz` with SHA-256 `0de0815551ae7a2f8e7630e8218e31b1b5ca4ea5c6455790bfab50c74e4d56cc`. The archive is accompanied by the original path list and per-file SHA-256 list.

## Disposition

- **44 evidence records committed:** 13 formal evidence records, 24 diagnostic-failure records, and 7 supporting Task definitions.
- **76 files deleted after backup:** superseded iterations, lower-value intermediate projections, one Task definition not selected for retention, and the one-off generator.
- **0 invalid JSON files:** all 119 JSON inputs parsed.
- **0 exact duplicates and 0 canonical-JSON duplicates:** redundancy was semantic and trajectory-level rather than byte-level.

The complete per-file decision is recorded in `inventory.json`; no original file lacks a disposition.

## Selection rule

Formal retention requires a bounded scenario, interpretable source revision, a coherent Task/Trial/Result chain when applicable, and evidence that adds information beyond another retained iteration. Passing results are sampled, not exhaustively committed.

Diagnostic failures are retained only when they isolate a materially different boundary failure and have a concrete correction. Their classification is preserved as `diagnostic_failure`; rejected or non-adjudicated runs are never presented as passes.

## Semantic duplicate reduction

The main repeated groups were:

1. raw/focused/focused-Pro rejection-classification attempts, superseded by the action-ready schema-drift diagnostic;
2. repeated provenance-repair attempts, reduced to one verifier rejection and one accepted repair;
3. repeated successful resume evidence, reduced to the timestamped and fully projected `resume-stress-pro-004` chain;
4. two pre-fence concurrent-resume failures, reduced to the more specific staggered `EventConflict` case;
5. two accepted concurrent-resume iterations, reduced to `concurrent-resume-stress-004`, which additionally proves one Provider invocation and durable Provider fencing.

Raw evidence and evaluation projections were not treated as duplicates: the former preserves execution receipts, while Task/Trial/Result/Failure records preserve the evaluation interpretation.

## Verification

The evaluation validator checks the retained Task/Trial/Result/Failure records. The curation verification also recomputes every retained file SHA-256, the manifest payload digest, JSON parsing, and exact summary agreement between the inventory and manifest.

## Restore

Current operator-host recovery directory:

```text
/root/backups/ordivon-computing/evidence-curation-20260803T1947+0800/
```

```bash
sha256sum -c /root/backups/ordivon-computing/evidence-curation-20260803T1947+0800/untracked-evidence.tar.gz.sha256
tar -xzf /root/backups/ordivon-computing/evidence-curation-20260803T1947+0800/untracked-evidence.tar.gz -C /root/projects/ordivon-computing
```

## Remaining limitations

- Several raw stress records do not carry a top-level integrity object; the curation manifest supplies the immutable file-level SHA-256 binding.
- Task capture times are derived from the first related Trial start because Task records do not include a native capture timestamp.
- The external archive is host-local and should enter the normal backup rotation.
- Iterations not selected for retention remain recoverable but are not CI-visible after deletion.
