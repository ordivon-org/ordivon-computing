# EX0–EX1 Causal Explanation Pilot

This experiment asks whether Ordivon's current Host/Harness/Runtime responsibility boundaries can be reconstructed more reliably from causal failure chains than from a strong repository-first responsibility summary.

It is deliberately a **research experiment**, not a new documentation authority or product ontology.

## EX0 — authority freeze

`authority-freeze-v1.json` freezes the exact Computing, Host, Harness and Runtime revisions and the narrow canonical dependencies consumed by this pilot. Product repositories remain authoritative for product facts. Computing owns only the experiment and cross-project conclusion.

The freeze applies the current P8/P9 law: declare the exact dependency basis before deriving the explanation; do not treat more raw current context as monotonically safer; synthesize after the decision-relevant dependency set is covered.

## EX1 — paired fresh-Agent test

`pilot-corpus-v1.json` freezes two matched explanation treatments, sixteen unseen boundary/semantic/transfer cases, mechanical oracles, anti-leakage rules and classification thresholds before any live Provider call.

- `repository_first` is a strong control distilled from current canonical owner boundaries.
- `causal_first` states the same ownership facts as concrete failure → missing responsibility → counterfactual deletion chains.
- six fresh paired DeepSeek Flash replicates use the same credential slot per pair and alternate treatment order;
- no prior answer is replayed into later calls;
- only wire/schema-invalid calls may be retried, with retries recorded;
- semantic answers are never repaired.

The experiment measures exact owner attribution, semantic-authority overreach, hard boundary confusion and transfer to robotics/microscopy/hospital cases. A causal explanation can be classified `SUPERIOR`, `CEILING_EQUIVALENT`, or `MIXED_OR_FAILED` only by the thresholds frozen in the corpus.

`trial.py` is experiment-local apparatus. It is not a shared explanation service, evaluator service, Provider router or Harness API candidate.

## Side finding

Before the matrix, `ordivon-harness/scripts/configure_deepseek_api.py --check-only` rejected the currently deployed private secret because the helper requires an exact five-field object, while current Harness source `DeepSeekSettings.from_secret_file()` explicitly admits the optional `credentialScopeId`. Loading through the current package source succeeds. This is a helper/source drift finding owned by Harness; it is not evidence against the Host/Harness/Runtime causal boundary itself and is excluded from the comprehension score.

## Closeout

EX0/EX1 is closed in [`EX0-EX1-REPORT.md`](EX0-EX1-REPORT.md). Across three paired matrices the experiment retained 36 accepted fresh trials, consumed 99,564 reported Provider tokens, and required 46 physical Provider calls including schema-invalid retries.

The three preregistered outcomes were:

- owner attribution: `CEILING_EQUIVALENT` (96/96 vs 96/96);
- existence/minimality stress: `MIXED_OR_FAILED` (119/120 repository-first vs 116/120 pure causal);
- held-out causal + explicit-boundary repair: `REJECT` (105/120 vs 106/120; both below the safe threshold).

The final method finding is stronger than a prose preference. A universal single `primaryOwner` answer is itself the wrong model for Ordivon. Semantic choice, durable structural state, physical truth, external-effect truth and sharing disposition may have different owners simultaneously. [`causal-units-v1.json`](causal-units-v1.json) records the revised multi-axis Host/Harness/Runtime reconstruction.

Pure causal prose is **not** promoted as the canonical Agent-facing form. Causal reconstruction survives as an existence/deletion audit; compact responsibility summaries, explicit negative proof boundaries and owner-native provenance remain first-class. Human/Studio/Web expression remains untested here.
