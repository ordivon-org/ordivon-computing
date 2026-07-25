# Status

## Completed

- M0 semantic reference kernel implemented.
- 16 unit and conformance tests pass on the current runtime.
- Dispatch is represented independently from Effect.
- VerificationPlan and evidence ownership are enforced.
- Scripted Ordivon adapter covers success, rejection, response loss, reconciliation, Artifact projection, and uncertainty.

## Current claim boundary

The experiment proves internal reference semantics and scripted adapter behaviour. It does not yet prove live Ordivon conformance, durability, Tool ABI stability, or production readiness.

## Next executable work

Run M1 against a live Ordivon Workspace for:

1. versioned read;
2. atomic mutation;
3. asynchronous command;
4. Observation and Artifact projection;
5. response-loss reconciliation without redispatch.
