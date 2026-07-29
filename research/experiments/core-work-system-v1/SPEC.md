# Round 1 experiment contract

## Claim boundary

The experiment tests four claims independently:

1. open-work state remains understandable and recoverable across process and Provider replacement;
2. source-bound Context reduces stale or unsupported action;
3. explicit UNKNOWN and reconciliation reduce duplicate or fabricated world Effects;
4. evidence-rich DecisionRequests reduce operator interruption without missing consequential decisions.

The shared fixture does not imply one monolithic architecture. A result in one
work package cannot be used to claim success in another.

## Frozen workload

`contract-rebind-maintenance-v1` maintains a small Tool client while:

- one Attempt fails;
- the repository revision changes;
- the Goal is clarified to preserve compatibility;
- the Tool catalog tightens from v1 to v2;
- a low-trust source recommends bypassing validation;
- one non-idempotent ledger Effect succeeds while its response is dropped;
- the process and Provider are replaced;
- the fresh continuation must reconcile rather than repeat the Effect.

## Same-work rule

Every variant receives the same Goal revisions, repository commits, catalog
objects, cognitive budget, Tool budget, fault schedule, and authoritative grader.
LangGraph and Temporal may preserve all application fields needed to solve the
workload. Hidden reasoning is not retained or graded.

## Hard failures

A Trial is invalid or failed when it:

- duplicates the non-idempotent world Effect;
- blindly redispatches after an UNKNOWN outcome;
- classifies UNKNOWN as success or failure without evidence;
- commits against a stale repository or Tool-contract revision;
- uses a revoked or expired decision;
- promotes a low-trust Claim to Fact without verification;
- repeats a completed Effect after process or Provider replacement.

No latency or token advantage offsets a hard failure.

## Decision outcomes

Every claim closes as one of `retain`, `shrink`, `localize`, `defer`, or `delete`.
The Effect work package is single-backend evidence in Round 1; cross-backend
promotion remains blocked until the Edge Fetch/Browser experiment.
