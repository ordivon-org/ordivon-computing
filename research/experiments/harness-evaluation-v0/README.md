# Harness Evaluation v0

Status: the R0–R2 evidence contract, curated dogfood set, and P0 frozen evaluation control plane are implemented. Track R remains active for repeated same-Task capability comparisons.

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
- [`formal-trial-plan-v1.json`](formal-trial-plan-v1.json) — machine-readable plan `HHR-R3-001`, currently `designed_not_executed`.

R3 remains designed but is blocked by [`../observation-plane-v0/P0-P1-DESIGN.md`](../observation-plane-v0/P0-P1-DESIGN.md). Host and Harness must first become independently durable, and Host/Harness/Runtime owner-native evidence must become automatically queryable. After that prerequisite, R3 proves the runner with a deterministic cross-layer smoke, runs three sequential native Ordivon Harness DeepSeek Trials, and executes five bounded fault cells. One-shot and Hermes ACP comparisons remain conditional on baseline closeout. Three Trials support development diagnosis; five to ten valid Trials per competitive configuration remain required for an architecture decision.

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
