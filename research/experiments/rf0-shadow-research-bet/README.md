# RF0 — Shadow ResearchBet Calibration

RF0 is the minimum prospective calibration record for the Research Frontier Model.

It is deliberately **shadow-only**:

- the evaluated Agent does not receive a ResearchBet;
- it does not change owner authority, scheduling, admission, or Tool selection;
- it is not a service, registry, score, planner, or new semantic primitive;
- it records a research prediction *before* outcome evidence is known, then binds the later outcome and prediction error.

The purpose is to make research-taste claims falsifiable without recreating the TM1 failure mode where methodological prose itself changed Agent cognition.

A `ResearchBet` freezes:

- the owner question/evidence identity;
- a revisable evidence-topology hypothesis;
- the chosen operator policy and real alternatives;
- the predicted decision/frontier change;
- budget and stopping rule;
- an explicit falsifier.

A `ResearchOutcome` later records:

- accepted owner-bound evidence;
- actual closed-loop cost;
- actual frontier delta;
- prediction error;
- the resulting World Model / operator-prior update.

`research-bet-v1.schema.json` and `research-outcome-v1.schema.json` are research record schemas only. They do not imply a Runtime/Host protocol or product API.

`rf1-game-stopping-bet.json` is RF0's first genuinely prospective consumer. It is frozen before RF1 accepted live trials and remains invisible to the evaluated Game auditor.
