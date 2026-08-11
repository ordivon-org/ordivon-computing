# FS0 — Shadow Portfolio Calibration

FS0 tests whether Ordivon's current Research Frontier Model can choose **which real owner pressure deserves the next unit of research budget** before outcomes are known.

It is shadow-only:

- owner tasks continue independently;
- no owner Agent receives FS0 rankings or rationales;
- FS0 does not start, stop, slow, or prioritize owner work;
- predictions freeze before later owner checkpoints used as outcomes;
- no universal tractability scalar is introduced.

## Cohort

The accepted primary cohort contains four materially different live owner pressures plus one deliberately admission-blocked negative control:

- `H-P6` — Harness recursive-discovery token utilization;
- `R-P5` — Runtime P5 physical foundation closeout;
- `G-AF3` — Game AF003 cross-encounter generalization;
- `HOST-PKG` — Host core-package dependency-surface pressure;
- `F-C2-BLOCKED` — Finance C2 remote effect-principal activation, currently blocked on an independently administered Linux/systemd host.

Crosscut HP is recorded as observational-only because it is itself testing TM4/RF evidence-topology/operator-policy priors and would contaminate the selector evaluation.

## Treatments

The same `deepseek-v4-flash` selector is run under two shadow treatments:

- `raw`: choose from the frozen owner cards using ordinary bounded research judgment;
- `rfm`: same cards plus a compact representation of currently supported Research Frontier priors. This is safe to test here because the selector has no authority over the owner tasks.

Each treatment runs five independent replicates. The selector must rank the cohort, choose one `nextBudgetChoice`, explicitly defer any currently non-closable pressure, and predict topology/operator/cost/frontier-delta for each candidate.

## Deterministic baselines

FS0 also freezes three intentionally simple baselines:

- `newest-task`: choose the most recently created live owner task in the primary cohort;
- `narrowest-scope`: choose the pressure with the smallest explicit owner-local semantic surface;
- `closest-to-closure`: choose the pressure whose owner checkpoint already has a bounded final validation/release path.

These are baselines, not claimed best policies.

## Outcome model

FS0 does not score research value with one scalar. Later owner-native outcomes are represented as vectors:

- frontier delta: no-op / ambiguity reduction / defect discovery / owner mechanism change / prior narrowing/generalization / new capability;
- cost: model calls/tokens when owner evidence provides them, wall/validation/physical burden, external blockers;
- prediction error: topology, operator, closure, and value-direction errors;
- selection regret: pairwise/partial-order regret where one candidate clearly dominates another on accepted outcome vectors.

If owner outcomes are not yet available, FS0 closes only the **prediction-freeze stage** and leaves outcome calibration pending. It must not fabricate terminal results.
