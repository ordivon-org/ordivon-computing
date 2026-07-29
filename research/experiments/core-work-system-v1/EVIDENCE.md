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
