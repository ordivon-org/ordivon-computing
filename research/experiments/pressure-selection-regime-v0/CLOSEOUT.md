# Pressure Selection Regime v0 — Closeout

Status: **complete negative representation-admission result**.

## Frozen question

Does a compact regime-aware pressure-selection guide improve fresh-Agent choice of the next discriminating research action across heterogeneous Ordivon cases without creating a universal scalar score or selector service?

## Live campaign

- Harness: `684333be5146d4f705a91edb396e83c6a1150e1f`
- model: DeepSeek V4 Flash
- cases: 10 source-derived cases
- treatments: `RAW_FACTS`, `REGIME_GUIDE`
- replicates: 2 per case/treatment
- trials: 40/40 complete
- Runtime Job: `job-01a03df8-d126-7d32-b94b-900b8fd92e4f`

| arm | exact | hard gate violation | premature optimization | unjustified scalarization | failure to stop | total tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RAW_FACTS | 20/20 | 0 | 0 | 0 | 0 | 24,737 |
| REGIME_GUIDE | 20/20 | 0 | 0 | 0 | 0 | 32,371 |

The guide increased tokens by 7,634, approximately 30.9%, and changed no measured decision outcome.

## Verdict

`CompactDefaultPressureSelectionGuide = NOT_EARNED`.

No Pro follow-up is justified: both arms are already at exact ceiling on the pre-frozen corpus, so a stronger model cannot demonstrate an incremental treatment benefit here. Harder synthetic cases are not manufactured after result visibility.

The result does **not** show that pressure selection is solved globally. It shows that when relevant facts, candidates, owner constraints and target operation are already present in the local decision surface, a capable fresh Agent reconstructs the right local judgment without permanent extra guide text.

The open problem remains upstream evidence acquisition/open-world pressure discovery and downstream prospective research-policy calibration. See `../../PRESSURE-SELECTION-VALUE-OF-INFORMATION-AUDIT-20260826.md`.
