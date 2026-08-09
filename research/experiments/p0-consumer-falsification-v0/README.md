# P0 Consumer Falsification v0

Status: deterministic apparatus stage. No live Provider comparison is claimed here.

This experiment executes the first two deterministic gates from [`../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md`](../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md):

- **P0-A0** — prove that a strong scripted one-shot cell and a current Harness cell can consume the same frozen repository-repair Task and independent verifier without reviving historical B5;
- **P0-B0** — prove that direct consequence-Tool exposure and one no-Tool deliberation followed by the same Tool exposure can be isolated as a single treatment variable under the current Harness H2 lifecycle composition.

## P0-A0 boundary

The frozen Task remains `HARNESS-REPO-REPAIR-001` version 1. The scripted one-shot cell receives the complete visible fixture and produces the known oracle candidate. The scripted Harness cell uses the current public dependency-inverted `DomainToolLoopRunner` with an evaluation-local repository-repair bridge. Both pass the same visible and hidden verifier. The hidden verifier is never included in model-visible Task material.

The current high-level `HarnessAgentRun` handle is also probed explicitly. At the current Harness boundary it supports the exact no-Tool and independent-search surfaces but does not accept this custom repository-repair Tool catalog. That is retained as a **surface-closure gap**, not silently worked around by calling the historical B4 composition “current HarnessAgentRun.” The lower public domain-loop surface remains sufficient for A0 apparatus acceptance.

A0 is non-competitive and does not decide retain/shrink/delete. Its next live S/H canary remains blocked until the Agent-visible MCP contract is fresh enough to exercise the current Runtime/Host surface without schema ambiguity.

## P0-B0 boundary

B0 defines two mechanically scored contexts over the same bounded irreversible `commit_rebalance` effect:

- one where holding misses the required service margin and the effect is applicable, so the oracle is `act`;
- one where holding already satisfies the objective while the effect is inapplicable and only burns reserve, so the oracle is `hold`.

The oracle is derived from the numeric Context, not accepted from the fixture label.

Treatments:

```text
DIRECT
Context + consequence Tool
→ Provider turn/loop
→ effect intent or hold conclusion

LATE AUTHORITY
Context, no consequence Tool
→ non-authoritative deliberation
→ same Context + exact deliberation record + same consequence Tool
→ effect intent or hold conclusion
```

The late path uses current advanced/internal `DeliberationThenToolRunner.run_lifecycle_bound()` so both phases share one aggregate budget, cancellation authority and absolute deadline. This experiment does not promote H2 into the recommended public API.

## Run

Use the current Harness project environment so `anc_canonical` and the exact Harness source dependencies are available:

```bash
cd /root/projects/ordivon-harness
uv run python /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/run_p0_a0_scripted_comparator.py
uv run python /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/run_p0_b0_authority_timing.py
uv run python -m unittest discover \
  -s /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/tests \
  -p 'test_*.py' -v
```

During authoring from an isolated dirty Computing Workspace, pass `--allow-dirty-computing`. Final evidence receipts must be regenerated from an exact clean committed Computing revision.

## Stop rules

- Do not resume `run_b5_native_trial.py` as the new campaign.
- Do not add a new Harness Tool-surface abstraction merely to make this benchmark fit `HarnessAgentRun`.
- Do not infer a live authority-timing benefit from scripted B0 acceptance.
- Do not move to Game confirmation before a live Harness-native D/L result reproduces.
- Do not start live P0 Provider calls until the ordinary Agent-visible MCP contract freshness gate is closed.
