# P0 Consumer Falsification v0

Status: Computer-owned P0 live phase closed. Deterministic apparatus and bounded live Provider evidence are retained; cross-domain product confirmation remains owner-native follow-up rather than Computing implementation.

This experiment executes the first two deterministic gates from [`../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md`](../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md):

- **P0-A0** — prove that a strong scripted one-shot cell and a current Harness cell can consume the same frozen repository-repair Task and independent verifier without reviving historical B5;
- **P0-B0** — prove that direct consequence-Tool exposure and one no-Tool deliberation followed by the same Tool exposure can be isolated as a single treatment variable under the current Harness H2 lifecycle composition.

## P0-A0 boundary

The frozen Task remains `HARNESS-REPO-REPAIR-001` version 1. The scripted one-shot cell receives the complete visible fixture and produces the known oracle candidate. The scripted Harness cell uses the current public dependency-inverted `DomainToolLoopRunner` with an evaluation-local repository-repair bridge. Both pass the same visible and hidden verifier. The hidden verifier is never included in model-visible Task material.

The current high-level `HarnessAgentRun` handle is also probed explicitly. At the current Harness boundary it supports the exact no-Tool and independent-search surfaces but does not accept this custom repository-repair Tool catalog. That is retained as a **surface-closure gap**, not silently worked around by calling the historical B4 composition “current HarnessAgentRun.” The lower public domain-loop surface remains sufficient for A0 apparatus acceptance.

A0 is non-competitive and does not decide retain/shrink/delete. The former Agent-visible MCP freshness blocker is now closed by refreshed ordinary connector evidence; the accepted live group below therefore proceeds from the current Agent-facing contract rather than the stale pre-refresh snapshot.

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

## Live P0 closeout

The accepted live apparatus is frozen at Computing `9b9906e9a6fe3f601f28dabec1652ba2cf6f8cf8` with `deepseek-v4-flash` through the current Harness DeepSeek adapter. The retained machine closeout is [`evidence/p0-live-closeout.json`](evidence/p0-live-closeout.json); exact per-Trial receipts live under [`evidence/live/`](evidence/live/).

### P0-A

Five exact S/H pairs were selection-valid under the corrected common configuration. The strong one-shot cell produced **0/5 accepted candidates and 0/5 verifier-passing candidates** at an average 1,868 Provider tokens. The current public `DomainToolLoopRunner` produced **3/5 accepted candidates and 4/5 verifier-passing candidate bytes** at an average 14,810 tokens, about 7.93× the one-shot token cost.

The scoped disposition is therefore **retain and localize**: current public domain Tool cognition has measurable correctness value on this bounded bare-model repository-repair workload and must not be deleted as equivalent to one-shot cognition. The result does not justify expanding `HarnessAgentRun`, does not prove universal Harness superiority, and does not itself measure durable Run continuation or response-loss recovery. One-shot remains the lower-cost baseline.

Two early live findings were retained as method corrections rather than silently discarded: Trial validity was initially conflated with semantic success, and the first aggregate token ceilings were too small for the Adapter's conservative per-call request bound. The accepted group was rerun only after both problems were fixed and regression-tested.

### P0-B

Three valid ACT and three valid HOLD pairs isolated only initial consequence-Tool visibility. On ACT, Direct and Late Authority were both **3/3 oracle-correct**. On HOLD, Direct was **0/3 oracle-correct and emitted three effect intents**, while Late Authority was **3/3 oracle-correct and emitted zero effect intents**.

This is repeatable Harness-native evidence that one non-authoritative deliberation opportunity before consequence authority can improve act/hold calibration in this bounded configuration without producing false HOLDs in the matched ACT fixture. It authorizes a conditional second-domain owner-native confirmation; it does **not** authorize public H2 promotion, a universal deliberation phase, an abstention service, or a policy engine.

## Run

Use the current Harness project environment so `anc_canonical` and the exact Harness source dependencies are available:

```bash
cd /root/projects/ordivon-harness
uv run python /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/run_p0_a0_scripted_comparator.py
uv run python /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/run_p0_b0_authority_timing.py
uv run python /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/run_p0_live.py a --replicate 1 --order SH
uv run python /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/run_p0_live.py b --replicate 1 --fixture margin-window-a
uv run python -m unittest discover \
  -s /root/projects/ordivon-computing/research/experiments/p0-consumer-falsification-v0/tests \
  -p 'test_*.py' -v
```

During authoring from an isolated dirty Computing Workspace, pass `--allow-dirty-computing`. Final evidence receipts must be regenerated from an exact clean committed Computing revision.

## Frozen deterministic evidence

The first clean exact-revision receipts bind Computing `bbdfbd54874fba9f5117fcb2687fe67035240863`, Host `95cd5479e71281baed5a1d1c34cbfaadffe2a22f`, Harness `5a42afdf5e01a6f5ad2b12738c52a249edb91dda`, and Runtime `480ef703d1d28a5a5b6ac7d7111a7764a22574d7`, all observed clean at execution time:

- [`evidence/p0-a0-bbdfbd5.json`](evidence/p0-a0-bbdfbd5.json) — same visible frozen Task, same hidden verifier, same scripted oracle candidate; records the `HarnessAgentRun` custom-Tool closure gap and authorizes no live or architecture claim.
- [`evidence/p0-b0-bbdfbd5.json`](evidence/p0-b0-bbdfbd5.json) — mechanically scored ACT/HOLD fixtures and exact direct/late Tool-exposure isolation; records no live Provider evidence, no Security generalization, no Game confirmation and no public H2 promotion.

These receipts are deterministic apparatus evidence. They do not increase `ANC-VERIFY-001` or `ANC-VERIFY-002` maturity beyond M4.

## Stop rules

- Do not resume `run_b5_native_trial.py` as the new campaign.
- Do not add a new Harness Tool-surface abstraction merely to make this benchmark fit `HarnessAgentRun`.
- Do not infer a live authority-timing benefit from scripted B0 acceptance; use the retained live group instead.
- Do not promote the Harness-native authority-timing result as a shared public cognition primitive without owner-native second-domain confirmation.
- Do not reopen P1-B merely because the pre-refresh evidence is still historical; the refreshed connector smoke is closed and P0 consumed the refreshed surface.
