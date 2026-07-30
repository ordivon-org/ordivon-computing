# Evidence contract

Every run emits one canonical JSON object containing:

- ExperimentSpec and exact source revisions;
- WorldManifest and fixture digest;
- variant and dependency versions;
- fault schedule;
- state before interruption and after recovery;
- Context sources, trust, revisions, omissions, and invalidations;
- Effect, backend correlation, response state, and reconciliation evidence;
- DecisionRequests, responses, active time, and reversals;
- authoritative world outcome, hard failures, costs, and decision disposition.

Negative, null, invalid, and incomplete runs remain in evidence. Receipts are
content-addressed and must not be rewritten as success.

## Bound receipts

- `evidence/deterministic-matrix.json` preserves all 16 isolated baseline trials.
- `evidence/live-provider-gauntlet.json` preserves six physical Codex/Hermes trials.
- `evidence/report-statistics.json` derives report aggregates and preserves measurement caveats.
- `evidence/round1-closeout.json` derives the architectural dispositions from the primary receipts.
- `evidence/round1-source-receipt.json` binds the Computing implementation commit, Host implementation and receipt, evidence digests, and clean-environment verification.

The full narrative interpretation is in [`REPORT.md`](REPORT.md). Numerical
claims in its aggregate tables must remain derivable from
`report-statistics.json`; prose may explain significance but must not silently
replace canonical evidence.
