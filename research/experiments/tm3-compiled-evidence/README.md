# TM3 — Compiled Evidence vs Iterative Agent Search

TM3 tests the next contraction after TM2.

TM2 showed that two deterministic owner-evidence searches can locate every hidden required source file across both Harness and Security holdouts, yet the Agent still consumes nearly the entire observation budget.

TM3 asks:

> For exact diagnostic/symbolic, retrieval-dominated questions, is the tractable research strategy to avoid iterative Agent discovery and instead deterministically compile a bounded evidence packet, then use one model call for semantic synthesis?

The accepted TM2 `evidence_first` trials are the frozen iterative comparator; they are not re-run.

For each of the same two exact owner revisions, TM3:

1. executes the same two frozen literal-search anchors;
2. parses matched file/line identities without semantic interpretation;
3. ranks candidate files mechanically by number of distinct anchors matched, then hit count, then path;
4. reads bounded windows around first matches, up to the same total eight-observation budget;
5. gives the compiled packet to `deepseek-v4-flash` once with only a `submit` Tool;
6. scores the submission with the same hidden causal oracle as TM2.

No iterative search/read Tool is available to the model and no TM0 taste prose is supplied.

A positive result would not justify a new framework. It would establish a conditional research-world-model prior: **when exact owner evidence makes retrieval cheap and deterministic, compile first and reserve probabilistic cognition for semantic synthesis.**
