# WL0 — Semantic Law Falsification

This experiment attacks five candidate cross-project semantic laws by deliberately removing each distinction in isolation.

The acceptance pattern is not “the guarded design passes.” For each law the experiment requires all of the following:

1. construct states in which collapsing the distinction creates a wrong conclusion or unauthorized consequence;
2. reproduce that failure repeatedly under a deterministic high-volume randomized campaign;
3. restore only the challenged distinction and drive the hazard error rate to zero;
4. retain benign trials in which the guard still permits ordinary successful work;
5. preserve one minimal counterexample and one small physical probe where possible.

The five candidates are:

- **L1 Reality–Representation Separation** — an Agent-visible representation cannot be equated with the represented reality;
- **L2 Binding Law** — a representation/evidence item is actionable only under the identity/revision/domain binding it established;
- **L3 Partial Observation** — no observed change does not prove no world change;
- **L4 Scoped Authority** — selection, knowledge, or mechanical reachability does not grant owner authority;
- **L5 Causal Non-Collapse** — possibility, selection, admission, intervention, transition, observation, and semantic consequence remain distinct stages.

The randomized models are deliberately tiny. Their purpose is to search counterexample space without importing Runtime, Host, Finance, World, or Game implementation mechanics into a new framework. Existing owner-native evidence remains the stronger external corroboration.

Run:

```bash
python law_falsification.py --trials 10000 --output evidence/wl0-law-falsification.json
python -m unittest -v test_wl0.py
```

The script is standard-library only and deterministic for the fixed seeds in source.
