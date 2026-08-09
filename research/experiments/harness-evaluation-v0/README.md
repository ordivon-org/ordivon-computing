# Harness Evaluation v0

Status: the R0–R2 evidence contract, Observation Minimum Core, B3 cross-owner Selection, B4 Formal Runner/fault-cell acceptance, and the C1 independent durable Harness-to-Runtime evidence canary are complete. The historical B5 DeepSeek campaign remains **provider-blocked and frozen** and must not be resumed. C1 fixed a three-replica policy and retained all outcomes: zero replicas reached semantic completion within the eight-call budget, while replica 3 still produced two real Runtime Jobs, survived an injected Patch response loss, left candidate code that passed visible and hidden verification, and yielded a complete two-owner Observation Selection with `trialValidityInferred=false`. The former Harness H4 acceptance blocker is retired by current owner evidence at `5a42afdf5e01a6f5ad2b12738c52a249edb91dda`. New work must not resume B5; the current Ready Frontier instead authorizes a fresh minimal comparison design bound to current Harness/Runtime/Provider identities. See [`../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md`](../../P0-P1-CONSUMER-FALSIFICATION-DESIGN.md).

## Question

Can a thin research envelope describe materially different Agent Harness experiments, support exact comparison and failure attribution, and preserve existing Host, Harness, Runtime, and Provider-native semantics?

## Hypothesis

Four append-only research records remain sufficient for one Trial:

```text
Task Definition
Trial Manifest
Trial Result
Failure Record
```

A comparison additionally requires a frozen System Manifest, a versioned Suite, and a deterministic Summary. These derived records reference component-native receipts and Artifacts rather than creating a second execution plane.

## Contents

### Trial evidence contract

- [`schemas/task.schema.json`](schemas/task.schema.json) — formal Task and Task-QA metadata;
- [`schemas/trial.schema.json`](schemas/trial.schema.json) — one exact evaluation configuration;
- [`schemas/result.schema.json`](schemas/result.schema.json) — outcome, verifier, actions, cost, and evidence;
- [`schemas/failure-record.schema.json`](schemas/failure-record.schema.json) — first observable failure and recovery attribution;
- [`failure-taxonomy.yaml`](failure-taxonomy.yaml) — Task-to-Operator failure classes derived from observed Ordivon failures;
- [`validate_evaluation_evidence.py`](validate_evaluation_evidence.py) — standard-library semantic and integrity validator.

### P0 control plane

- [`suite-v1.json`](suite-v1.json) — admitted, candidate, and historical workload families plus comparison and metric policy;
- [`schemas/system-manifest.schema.json`](schemas/system-manifest.schema.json) — frozen system and configuration identity;
- [`schemas/suite.schema.json`](schemas/suite.schema.json) — versioned suite declaration;
- [`schemas/component-baseline.schema.json`](schemas/component-baseline.schema.json) — deterministic component-health receipt;
- [`schemas/summary.schema.json`](schemas/summary.schema.json) — descriptive Trial aggregation without a heterogeneous global score;
- [`schemas/closeout.schema.json`](schemas/closeout.schema.json) — exact tested revision, gate evidence, integration status, and next-gate contract;
- [`validate_p0_artifacts.py`](validate_p0_artifacts.py) — semantic, integrity, reference, aggregate, and closeout validator;
- [`summarize_evaluation.py`](summarize_evaluation.py) — deterministic grouping and comparison-eligibility analysis;
- [`baselines/p0-20260804/`](baselines/p0-20260804/) — frozen Host, Harness, Runtime baseline, dogfood projection, and machine-verifiable closeout.

### Preserved evidence

- [`examples/`](examples/) — historical projections from H3, H4, and the Codex→Hermes H5 trajectory;
- [`dogfood-20260802/INDEX.md`](dogfood-20260802/INDEX.md) — curated real-run evidence index; diagnostic failures remain separate from accepted evidence;
- [`tests/`](tests/) — contract, tamper, relation, aggregation, and boundary tests.

### R3 formal Trial campaign

- [`FORMAL-TRIAL-DESIGN.md`](FORMAL-TRIAL-DESIGN.md) — claim boundaries, campaign phases, evidence chain, fault cells, review policy, promotion gates, and stop conditions;
- [`formal-trial-plan-v1.json`](formal-trial-plan-v1.json) — frozen machine-readable campaign design `HHR-R3-001`; its embedded design status is historical, while current execution state is recorded by the cognitive-reform program and research portfolio.

R3 has executed through deterministic B4 acceptance. HHO-P0, the three owner exporters, B3 cross-owner Selection, and B4 are complete. B4 uses a private file-backed `TrialRecordStore`, the independent Harness repository-repair Runtime surface, real Runtime Workspaces and Jobs, Host semantic verification, three owner exporters, and one frozen Observation Selection. The scripted integrated smoke reconciles Host and Runtime response loss without duplicate physical work, survives process reopen, and rejects Runtime success when the required Completion Artifact is absent. Version-bound deterministic cells re-run stale Assignment, invalid Tool correction, and Observation gap/mapping/privacy rejection proofs.

The subsequent B5 DeepSeek attempts are retained as diagnostics, not as a completed baseline. The current execution program records `B5=blocked_provider_capability`, zero valid complete Trials, and no authorization for further B5 canaries or B6. C1 then exercised the independent Harness package boundary against the production Runtime without Host execution authority. Its fixed three-replica set is preserved under [`evidence/c1-independent-runtime-c29b648/`](evidence/c1-independent-runtime-c29b648/): task success was 0/3, so it is not a model-quality baseline, but replica 3 proved durable Harness→Runtime execution, Patch reconciliation, owner-native verification evidence, and a complete independent Harness/Runtime Observation Selection. This evidence also exposed a Harness reconciliation-path metadata bug and a separate H4 repeatability conflict. Those historical facts remain part of C1 evidence, but current Harness owner evidence has since repaired and closed the blocker. No additional C1 sampling or B5 canary is authorized. The next comparison is a fresh current-revision campaign described by the 2026-08-10 P0/P1 design. The historical comparison rule remains unchanged: development diagnosis needs three valid complete comparable Trials, while an architecture decision requires five to ten selection-eligible Trials per competitive configuration when cost permits.

R3 does not generate Candidates or allocate another round. The downstream [`../experiment-loop-v0/`](../experiment-loop-v0/) plan consumes stable R3 Trial groups only after the deterministic smoke and repeated native baseline pass.

### Agent-first operations

- [`query_evaluation.py`](query_evaluation.py) — dependency-free, stateless JSON queries over validated Task, Trial, Result, and Failure records.

Track R has no persistent analytical database, experiment server, dashboard, projection timer, or dedicated backup system. Agents and tools read the committed records directly, validate them before use, and derive summaries on demand. Git preserves reconstructable history; Host, Harness, and Runtime retain their own operational evidence and recovery authority.

A local Parquet, DuckDB, MLflow, systemd, and restic data plane was implemented and exercised, then removed from the active system. It duplicated reconstructable records, consumed about 823 MB of installed dependencies, and primarily served a human experiment-browsing workflow that is not part of current Ordivon use. The experiment remains recoverable from Git history.

## P0 result

The frozen component baseline binds exact clean revisions of Ordivon Computing, Host, Harness, and Runtime. Four deterministic test suites report 601 passed, 0 failed, and 22 explicitly ignored Runtime system tests. One additional Runtime check proves only that the local-acceptance facility exists.

This is a component-health result, not an Agent product score. The baseline therefore fixes `productQualityClaim` to `false`.

The curated dogfood projection contains 7 Tasks, 10 Trials, 10 Results, and 6 Failure Records. It produces 10 exact configuration groups and admits no architecture comparison: every candidate is blocked by insufficient repetition, missing System Snapshot binding, fewer than two comparable configurations, or differing verifier identity.

## Validate

```bash
python3.12 research/experiments/harness-evaluation-v0/validate_evaluation_evidence.py \
  research/experiments/harness-evaluation-v0/examples/**/*.json

python3.12 research/experiments/harness-evaluation-v0/validate_p0_artifacts.py \
  --root . \
  research/experiments/harness-evaluation-v0/suite-v1.json \
  research/experiments/harness-evaluation-v0/baselines/p0-20260804

python3.12 -m unittest discover \
  -s research/experiments/harness-evaluation-v0/tests \
  -p 'test_*.py'

set -a
. /etc/ordivon/ordivon-runtime.env
set +a
python3.12 research/experiments/harness-evaluation-v0/run_b4_deterministic_smoke.py
```

Use `--write-digests` only while authoring a new record before its first commit. A committed record is immutable; corrections create a new version or superseding record.

Query the current curated records without installing or starting a service:

```bash
python3.12 research/experiments/harness-evaluation-v0/query_evaluation.py status
python3.12 research/experiments/harness-evaluation-v0/query_evaluation.py list --kind trial
python3.12 research/experiments/harness-evaluation-v0/query_evaluation.py \
  show dogfood:20260802:provenance-verifier-rejected-pro
python3.12 research/experiments/harness-evaluation-v0/query_evaluation.py \
  failures --class HARNESS --recovered true
python3.12 research/experiments/harness-evaluation-v0/query_evaluation.py comparison-readiness
```

All commands emit structured JSON. They create no database, cache, background process, or derived authority.

## Comparison gate

A capability comparison requires:

- the same Task ID and version;
- the same verifier identity and revision;
- a complete `bindings.systemManifestRef` for every new Trial; legacy Trial records may omit it but cannot become comparison-eligible;
- at least three Trials per configuration for development evidence;
- five to ten Trials per configuration for an architecture decision when cost permits;
- trajectory review for all failures, false completions, anomalous-cost successes, duplicate Effects, and grader disagreements.

Capability suites may graduate into regression suites after the expected behavior becomes stable. Heterogeneous Tasks remain separate; no global score is generated.

## Historical admission

The H3–H5 examples are projections, not rewritten source receipts. Each retains the source repository path, exact SHA-256 file digest, and limitations of the historical observation. Fields absent from the original evidence are `null`; they are not inferred.

The examples establish that the common envelope can represent:

- one Codex App Server Run that leaves the Host Task waiting;
- one Hermes ACP Run with a different Session/Prompt lifecycle and no retained thought text;
- one two-Harness replacement trajectory with stale-completion rejection, response-loss recovery, verified Artifacts, and accepted TaskOutcome.

They do not establish comparative model quality because Task, model, budget, Harness, and environment conditions differ.

## Boundaries

This experiment does not:

- execute an Agent or dispatch Runtime work;
- alter Host completion state;
- require Provider reasoning text;
- provide a model leaderboard or one cross-task score;
- define a universal trace format;
- own product-native lifecycle or operational truth;
- authorize a standalone Eval service, repository, dataset service, model router, or post-training pipeline.

Host remains the Task and semantic-decision authority. Harness remains the Run and Tool-trajectory authority. Runtime remains the physical execution authority. Track R owns only research Task admission, derived Trial and Failure envelopes, comparison policy, and interpretation.

## Canonicalization domain

Track R records use `ordivon-evidence-json-v1`: sorted-key compact JSON over the finite JSON number domain admitted by the evaluation schemas. This label is intentionally distinct from the integer-only strict `anc_canonical` protocol domain. The two profiles may share byte ordering without claiming the same accepted value set.

## B5 native baseline runner

`run_b5_native_trial.py` executes exactly one sequential native Ordivon Harness Trial. Each invocation creates a fresh historical source repository, Runtime Workspace, Host state, Harness state, and Provider conversation. It uses the frozen independent repository-repair Tool surface, DeepSeek non-thinking adapter, independent visible and hidden verification, Host semantic acceptance or rejection, the three owner exporters, one complete `ObservationSelectionManifest`, and the B4 `TrialRecordStore`.

A valid Trial may be accepted or rejected. Candidate failure is retained as a valid negative result only when the Runtime Workspace is closed, all three owner streams are complete, the verifier ran, and the Trial disposition is unambiguous. Infrastructure or Selection failure does not count toward the required three Trials.

The first clean native canary at revision `ad3ca58` linked no Runtime Job. Its Workspace closed correctly, but the pre-fix Runner stopped at `executing` and retained no Harness Trace or Selection. It is preserved under [`diagnostics/b5-native-001-ad3ca58/`](diagnostics/b5-native-001-ad3ca58/) as invalid diagnostic evidence and is excluded from the baseline. The current Runner retains privacy-safe incomplete Selections and closes invalid or unknown Trials with explicit failure attribution.

All three baseline Trials must use the same Provider, model, adapter, credential scope, prompt/context/tool/budget policy, and exact owner revision vector. Credential bytes, raw Provider responses, and private reasoning are never written to evidence. Trials are strictly sequential.

```bash
set -a
. /etc/ordivon/ordivon-runtime.env
set +a
python3.12 research/experiments/harness-evaluation-v0/run_b5_native_trial.py \
  --trial-number 1 \
  --deepseek-secret /root/.config/ordivon/secrets/deepseek.json \
  --output-root /path/to/private-trial-root
```

B5 does not authorize B6, TCG, Child Runs, a graph store, a daemon, concurrent campaigns, or automatic credential rotation.
