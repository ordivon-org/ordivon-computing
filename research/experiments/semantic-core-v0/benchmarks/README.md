# Semantic Core benchmarks

The benchmark harness measures algorithmic growth on the same machine and exact revision. It is not a cross-machine leaderboard.

```bash
PYTHONPATH=src python3.12 benchmarks/benchmark_semantic_core.py \
  --profile standard \
  --source-revision "$(git rev-parse HEAD)" \
  --output benchmark-results/<revision>.json
```

`smoke` is suitable for routine validation. `standard` measures the 10–200 Effect in-memory curve and 10–100 Effect Journal curve.

Interpretation priorities:

1. growth in per-command cost as state grows;
2. Journal reopen cost as entry count grows;
3. relative change on the same environment;
4. absolute latency only after the growth curve is stable.

Benchmark result files are immutable evidence bound to a source revision. They are not a mutable current-status document.

## Retained receipts

- `baseline-bf60668.json` — pre-optimization exact main baseline.
- `prototype-23353fd.json` — exact incremental reducer plus rejected checkpoint prototype.
- `optimized-dd4730e.json` — final incremental reducer and Journal v3 exact implementation receipt.

The checkpoint prototype remains in Git history but not in the runtime. Its negative result is a decision artifact, not an invitation to maintain an unused feature.

- `binding-edge-2f4d7ca.json` — Journal v4 and optional Binding-edge regression receipt; unbound command cost remains flat after K12.
