# Continuous Experiment Loop v0 Execution Plan

Status: execution designed; implementation not started.

Plan: `CEL-R4-001`.

Questions: primary `ANC-VERIFY-001`; downstream consumer `ANC-ADAPT-001` remains blocked until repeated trajectory and promotion evidence exists.

## 1. Decision

Ordivon should learn from the continuous-exploration pattern, but it should not imitate its scale or create a general autonomous-science platform.

The first useful construction is a bounded research loop:

```text
Research Question
→ Hypotheses
→ Candidate configurations or patches
→ isolated implementation
→ repeated formal Trials
→ independent evaluation
→ validity and failure attribution
→ Pareto comparison
→ next-round proposal or stop
→ human-owned promotion decision
```

The loop uses existing product authorities:

- Host owns Task meaning, commitments, verification admission, and TaskOutcome;
- Harness owns Agent Run, Provider Call, Tool Step, recovery, Trace, and CompletionProposal;
- Runtime owns Workspace, Job, Attempt, process, Artifact, physical recovery, and terminal evidence;
- Domain projects own world state and domain outcome;
- HHO-P1 Observation provides a non-authoritative, rebuildable evidence query path;
- HHR-R3 owns formal Trial manifests, validity, results, and failure records;
- CEL-R4 owns only Campaign-level research selection and learning records.

No CEL-R4 record is automatically a product fact, policy update, Skill, deployment, or model-training example.

## 2. Why this follows P1 and R3

P1 answers:

> What committed owner-native events occurred, how are they linked, and is the selected evidence complete?

R3 answers:

> Is this one exact execution a valid Trial, what was its outcome, and which boundary failed?

CEL-R4 answers:

> Given multiple valid comparable Trials, which hypotheses remain plausible, which candidates deserve another round, what did the experiment teach, and should the Campaign stop?

These questions must remain separate. An Observation stream can be complete while the Trial is invalid. A Trial can be valid and negative. A Candidate can fail while the infrastructure and evaluator behave correctly. A Campaign can produce valuable information without producing a promotable winner.

## 3. Scope

### 3.1 In scope

- bounded candidate generation from an admitted Research Question;
- exact candidate identity and lineage;
- isolated patch or configuration implementation;
- repeated R3 Trials under exact Configuration Cells;
- deterministic and domain-owned grading;
- explicit validity, outcome, and failure-attribution axes;
- Pareto and replication-based round selection;
- preservation of negative and null results;
- bounded next-round proposal;
- stop, retain, narrow, or delete decision;
- production of candidate commits and evidence packets for human review.

### 3.2 Out of scope

- a general scheduler or workflow engine;
- automatic merge, release, canary, rollback, or production deployment;
- direct mutation of Host, Harness, Runtime, Observation, or domain authority state;
- online reinforcement learning over production work;
- automatic post-training or Dataset admission;
- unrestricted recursive self-modification;
- one universal objective or intelligence score;
- open-ended autonomous research without a budget and stop condition;
- a new repository or long-running experiment service;
- a universal scientific ontology;
- replacing domain verifiers with an LLM judge;
- raw private Chain-of-Thought retention.

## 4. Research authority and data layout

CEL-R4 remains a file- and Git-backed Track R experiment inside `ordivon-computing`.

```text
research/experiments/experiment-loop-v0/
├── campaigns/<campaign-id>/
│   ├── campaign.json
│   ├── questions/
│   ├── hypotheses/
│   ├── candidates/
│   ├── rounds/
│   ├── observation-selections/
│   ├── evaluations/
│   ├── learning/
│   └── closeout.json
├── schemas/
├── scripts/
└── tests/
```

The directory stores research records and immutable references. It does not copy Host Journal, Harness Journal, Runtime Registry, Observation database, full model transcripts, secret-bearing environment, or source workspaces.

No database is admitted in v0. If repeated campaigns prove that file scans materially dominate work, a local index may be tested as a disposable projection. It cannot become Campaign authority without a separate decision.

## 5. Minimal research records

## 5.1 `ResearchQuestionSpec`

Immutable statement of:

```text
questionId
objective
baseline
measurable claims
allowed change surface
forbidden change surface
workload and holdout refs
metric definitions
risk class
budget policy
stop conditions
promotion boundary
limitations
integrity
```

A question is not admitted unless at least one outcome can be measured independently of the Proposer.

## 5.2 `CampaignManifest`

Binds:

```text
campaignId
questionRef
base source revisions
P1 contract and mapping versions
R3 plan and Task/Suite versions
role implementation identities
candidate policy
trial policy
selection policy
resource budget
parallelism ceiling
privacy policy
human release authority
createdAt
integrity
```

Any material change creates a new Campaign or explicit Manifest revision. Results from different Campaign manifests are not silently pooled.

## 5.3 `HypothesisRecord`

Contains:

```text
hypothesisId
campaignId
statement
mechanism
predicted observable change
predicted trade-offs
supporting evidence refs
contradicting evidence refs
proposer identity
createdAt
status
integrity
```

The hypothesis status may become `supported`, `contradicted`, `inconclusive`, or `superseded`; it never becomes a product fact by itself.

## 5.4 `CandidateManifest`

Binds one exact candidate:

```text
candidateId
campaignId
roundId
hypothesisRefs
parentCandidateRefs
base revision
patch or configuration digest
allowed paths
changed paths
implementation identity
System Manifest template
expected evaluator
risk declaration
integrity
```

A Candidate is invalid when it changes a forbidden path, verifier, hidden holdout, Trial schema, baseline receipt, budget accounting, or evidence collector.

## 5.5 `ConfigurationCell`

One exact evaluated system:

```text
candidateId
Task / Suite identity
model / Provider / Adapter
Harness implementation
Context and Tool policy
budget
Runtime environment
verifier and grader bundle
observation mapping versions
replication policy
configurationDigest
```

Changing one material field creates another Configuration Cell.

## 5.6 `TrialDisposition`

Trial interpretation uses separate axes.

### Validity

```text
valid
invalid
unknown
```

### Semantic outcome

```text
accepted
rejected
not_reached
not_applicable
unknown
```

This axis records whether the authoritative Task or domain acceptance boundary was reached and what it decided. Runtime success, Harness completion, or a model final message cannot directly set it.

### Comparative outcome

```text
improved
equivalent
regressed
inconclusive
not_applicable
unknown
```

This axis is derived only after a valid comparable Trial group exists. A single baseline Trial normally uses `not_applicable`.

### Failure attribution

```text
none
candidate
infrastructure
evaluator
environment
policy
multiple
unknown
```

### Selection eligibility

A Trial is selection-eligible only when:

- validity is `valid`;
- required P1 source streams are complete;
- the Configuration Cell identity is exact;
- required deterministic and domain graders completed;
- no forbidden Candidate mutation occurred;
- no unresolved duplicate dispatch, false completion, privacy violation, or contaminated environment remains.

A valid rejected, regressed, or inconclusive Trial remains eligible as evidence against a Candidate or hypothesis. Invalid or unknown Trials are retained but excluded from performance comparison.

## 5.7 `GraderBundle`

A versioned set of independent graders:

```text
deterministic assertions
hidden holdout verifier
domain verifier
trajectory rules
resource and cost accounting
optional rubric grader
human calibration refs
bundle digest
```

The Proposer cannot edit the active Grader Bundle. An LLM rubric grader may classify or summarize evidence but cannot be the sole authority for a promotable candidate when deterministic or domain verification is possible.

## 5.8 `RoundDecision`

Records:

```text
roundId
admitted candidates
valid Trial groups
invalid and unknown Trial groups
Pareto frontier
replication decision
eliminated candidates and reasons
retained diversity candidate
next-round budget
stop or continue decision
search-controller identity
review refs
integrity
```

## 5.9 `LearningUpdate`

A bounded knowledge record:

```text
claim
scope
supporting Trial and Grader refs
contradicting refs
confidence class
known confounders
negative result
recommended next test
not-authorized-for
integrity
```

A Learning Update is useful only when another process can determine which exact evidence produced it. It cannot silently rewrite prior updates.

## 5.10 `CampaignReceipt`

Final closeout containing:

```text
question and Manifest identity
round and candidate counts
valid / invalid / unknown Trial counts
baseline and final Pareto frontier
replication result
verified improvement claims
negative results
resource use
human decision
retained artifacts and owner refs
limitations
retain / narrow / delete disposition
integrity
```

## 6. Role separation

## 6.1 Proposer

May:

- read admitted question, public workload specification, prior Learning Updates, and bounded observation summaries;
- propose hypotheses and Candidates;
- predict measurable effects and trade-offs.

May not:

- modify hidden graders or holdouts;
- mark a Trial valid;
- accept a TaskOutcome;
- choose production promotion alone.

## 6.2 Implementer

May:

- transform an admitted Candidate into an isolated patch or configuration;
- use Harness and Runtime through existing authorities;
- emit exact patch, build, and test references.

May not:

- change the Candidate after Trial start;
- edit outside allowed paths;
- alter evaluator code or baseline evidence;
- reuse a contaminated Workspace.

## 6.3 Evaluator

May:

- execute the frozen Grader Bundle;
- issue deterministic and domain verdicts;
- produce TrialDisposition and GraderResult records;
- identify evidence incompleteness and disagreement.

May not:

- generate the Candidate it alone evaluates when another independent evaluator is available;
- repair candidate output before scoring;
- convert missing measurements into zero;
- infer semantic success from Runtime success.

## 6.4 Search Controller

May:

- compare selection-eligible Trial groups;
- preserve a baseline and diversity candidate;
- request replication;
- allocate the next bounded round;
- stop when evidence or budget requires it.

May not:

- dispatch product Effects directly;
- modify Candidate bytes;
- override invalidity or grader disagreement;
- promote to production.

## 6.5 Human release authority

Owns:

- merge, release, canary, rollback, publication, and consequential deployment decisions;
- changes to objectives, hidden graders, promotion thresholds, or risk policy;
- acceptance of major architecture deletion or expansion.

The first Experiment Loop can be highly automated internally while still stopping at a candidate commit and review packet.

## 7. Candidate isolation and anti-gaming

Each Candidate uses:

- one exact clean base revision;
- one isolated Runtime Workspace;
- one immutable Candidate Manifest;
- one path allowlist and denylist;
- one patch digest before Trial execution;
- fresh initial state per replicate;
- separate private evaluator/holdout location;
- no inherited untracked files or mutable benchmark output.

The runner rejects a Candidate when it:

- edits tests or graders outside the declared allowed surface;
- changes benchmark input, timeout, sample count, or metric calculation;
- suppresses errors or removes assertions;
- reads hidden holdout paths through unauthorized Tools;
- modifies Observation mappings to hide events;
- changes token, wall-time, CPU, memory, or disk accounting;
- depends on an uncommitted sibling repository;
- leaves unresolved Jobs, processes, or Workspaces.

The same model may assist several roles, but the Campaign must retain distinct prompts, tool authority, evidence visibility, and implementation identities. A single model self-score is never sufficient promotion evidence.

## 8. Search and selection policy v0

CEL-R4 does not begin with reinforcement learning, Bayesian optimization, or an open-ended evolutionary population. The first controller is deterministic and inspectable.

### 8.1 Candidate generation

Per round:

- one baseline Candidate is retained unchanged;
- up to three new Candidates are admitted;
- at least one Candidate should test a materially different mechanism rather than a parameter-only variation;
- near-duplicate patches are deduplicated by normalized diff and declared mechanism.

### 8.2 Trial policy

Default first live Campaign:

- maximum three rounds;
- maximum four Candidates per round including baseline;
- three valid Trials per Candidate for development comparison;
- one fresh-process replication for the provisional winner;
- sequential execution by default until state isolation and accounting are proven;
- parallel execution only across distinct state roots and Workspaces after a deterministic contamination test.

Token limits are explicit but not artificially tight. Compute, wall time, Job count, disk growth, and external consequence limits remain bounded. A Campaign may increase model budget only by creating a new Manifest revision.

### 8.3 Multi-objective comparison

No single global score is required. The first Campaign uses a Pareto frontier over:

```text
correctness and verifier pass
recovery and duplicate-dispatch safety
throughput / latency
CPU / memory / disk
model and Runtime cost
implementation complexity delta
maintenance and rollback burden
```

Hard safety and validity gates dominate performance. A faster Candidate with weaker recovery, evidence, or verification is rejected rather than traded through a scalar score.

### 8.4 Next-round rule

The Search Controller may continue with:

- the verified Pareto leader;
- one diversity Candidate whose mechanism is not dominated on all dimensions;
- one new Candidate derived from observed failure or bottleneck;
- the unchanged baseline.

It stops when:

- no Candidate produces a replicated verified improvement;
- the remaining uncertainty is dominated by evaluator or infrastructure instability;
- marginal information gain is low relative to remaining budget;
- all admissible Candidates violate hard gates;
- the Campaign reaches its round, Trial, compute, or time limit;
- human review changes the question or promotion boundary.

## 9. Execution state machine

```text
DRAFT
→ PREFLIGHTED
→ ROUND_OPEN
→ CANDIDATES_FROZEN
→ TRIALS_RUNNING
→ EVALUATING
→ ROUND_DECIDED
→ NEXT_ROUND | REPLICATION
→ CLOSEOUT_PENDING
→ CLOSED
```

Terminal exceptional states:

```text
STOPPED_INVALID_QUESTION
STOPPED_EVALUATOR_UNSTABLE
STOPPED_INFRASTRUCTURE_UNSTABLE
STOPPED_PRIVACY
STOPPED_BUDGET
STOPPED_HUMAN
ABANDONED
```

Every transition writes one immutable research record or atomic orchestration state referencing owner-native work. Restart must reconcile existing R3 Trial, Host Task, Harness Run, and Runtime Job identities before any new dispatch.

## 10. First evidence program

## E0 — retrospective shadow encoding

Use the existing Harness independent-store performance investigation as a historical fixture:

- baseline per-event admission behavior;
- observed 10,000-event duration;
- candidate batch-admission hypothesis;
- correctness and performance gates;
- negative and unresolved findings.

E0 validates CEL records only. It does not claim that the historical work was automatically proposed or selected.

Gate:

- the historical sequence can be represented without rewriting Host, Harness, Runtime, or benchmark evidence;
- missing historical facts remain unknown;
- no artificial winner is declared.

## E1 — first live self-customer: Observation Gateway optimization

After P1 Core passes, optimize one bounded Gateway dimension while preserving semantics.

Initial question:

> Which bounded ingest batch and SQLite index strategy improves accepted metadata-event throughput and common trajectory-query latency without weakening duplicate detection, sequence completeness, privacy rejection, backup/restore, or rebuild behavior?

Allowed Candidate surface:

```text
Gateway batch admission implementation
SQLite indexes
bounded transaction grouping
query plans
non-semantic cache or prepared-statement use
```

Forbidden surface:

```text
Envelope identity
privacy rules
source sequence rules
same-ID/different-bytes corruption behavior
owner exporter mappings
acceptance thresholds
benchmark data or grader code
```

Strong baseline:

- current accepted P1 Core Gateway implementation.

Grader Bundle:

- complete Gateway tests;
- duplicate/response-loss/gap/corruption matrix;
- privacy acceptance;
- backup/restore and rebuild-from-owner checks;
- 100 events/second sustained load;
- one-million-event query benchmark;
- CPU, memory, WAL, database size, and complexity delta.

Promotion boundary:

- candidate commit and review packet only;
- human decides merge;
- post-merge P1 regression gates run independently.

## E2 — Harness policy experiment

Only after R3 completes a stable repeated native baseline:

- change one Context, Tool exposure, stopping, or recovery policy at a time;
- use held-out Tasks or seeds;
- compare success, false completion, unnecessary actions, token use, recovery, and request-human quality;
- do not mix model, Tool, Task, and policy changes in one Cell.

This phase may provide the first evidence that unblocks part of `ANC-ADAPT-001`.

## E3 — Security adversarial consumer

Only after Security provides held-out opponents/worlds and an evaluator resistant to direct manipulation:

- Red and Blue candidate policies remain Security-owned;
- CEL-R4 may allocate bounded rounds and retain comparative evidence;
- Security owns Contest/Campaign meaning and outcome;
- held-out transfer must beat a static-opponent baseline before coevolution machinery is retained.

Security does not become the generic Experiment Loop owner.

## 11. P1 refinements required by CEL-R4

P1 remains non-authoritative but must expose enough stable evidence for experiment selection:

1. generic namespaced relation targets can reference external `evaluation.campaign`, `evaluation.configuration`, `evaluation.trial`, and `evaluation.grader-result` identities without adding fixed nullable fields;
2. relation vocabulary includes `derived_from` and `evaluates` in addition to execution relations;
3. a trajectory query reports completeness per native source stream, but never Trial validity;
4. Track R can freeze an `ObservationSelectionManifest` containing selected event IDs, canonical digests, query identity, mapping versions, and completeness claims;
5. rebuilding Observation from intact owners reproduces native event IDs and relation edges, while ingest timestamps and receipts may differ;
6. synthetic acceptance includes repeated Trial grouping, one valid negative result, one invalid Trial, and one incomplete trajectory without conflating them;
7. P1 metrics expose observation lag and cost but do not choose experiment winners.

## 12. R3 refinements required by CEL-R4

R3 must provide:

- explicit Trial validity, outcome, and failure-attribution axes;
- `ObservationSelectionManifest` references;
- exact Configuration Cell identity;
- preservation of valid negative results;
- exclusion of invalid/unknown Trials from selection statistics;
- Grader Bundle identity and disagreement records;
- repeated Trial groups and replication identity;
- no automatic Candidate generation or next-round decision.

R3 remains independently useful even if CEL-R4 is deleted.

## 13. Acceptance gates

### Contract and authority

- all CEL records validate and bind immutable owner references;
- deleting CEL files cannot alter or delete Host, Harness, Runtime, Observation, R3, or domain evidence;
- CEL has no product database, service, scheduler, model router, or deployment credentials;
- proposer, evaluator, controller, and release authority are distinguishable.

### Trial validity

- valid accepted, valid rejected, comparatively regressed, invalid, infrastructure-failed, evaluator-failed, and incomplete-evidence examples remain distinguishable;
- only valid and complete Trial groups enter Pareto comparison;
- missing values remain unknown;
- a physically successful Runtime Job cannot become Candidate improvement without domain and Host verification.

### Search

- baseline is retained every round;
- same-diff Candidates are deduplicated;
- at least one mechanism-diverse Candidate is preserved when budget permits;
- winner replication uses fresh process, state root, and Workspace;
- round decisions are deterministically reproducible from frozen inputs.

### Anti-gaming

- Candidate cannot modify hidden grader, workload, metric, or observation mapping paths;
- benchmark and timeout changes invalidate the Candidate;
- secret-like content and private reasoning are absent;
- evaluator disagreement blocks promotion;
- no automatic merge or deployment occurs.

### First live Campaign

- E1 completes at least one baseline plus two materially distinct Candidates;
- each compared Candidate has three valid Trials;
- one provisional winner receives fresh replication;
- Campaign emits at least one useful negative or null result;
- final result is a candidate commit plus evidence packet and human decision;
- measured improvement survives independent post-campaign regression gates.

## 14. Closeout outputs

```text
cel-contract-v1.json
cel-plan-receipt.json
e0-shadow-closeout.json
e1-campaign-manifest.json
e1-candidates/*.json
e1-rounds/*.json
e1-trial-groups/*.json
e1-observation-selections/*.json
e1-evaluations/*.json
e1-learning/*.json
e1-replication.json
e1-campaign-closeout.json
cel-r4-closeout.json
```

Every output binds exact source revisions, P1 envelope and mapping versions, R3 plan and Task/Suite versions, role identities, Candidate digest, Grader Bundle, Trial refs, and integrity digest.

## 15. Stop and deletion conditions

Stop and redesign if:

- Candidate generation cannot be separated from evaluator authority;
- repeated Trials remain too unstable for selection;
- most rounds diagnose infrastructure rather than candidate differences;
- the loop requires copying owner databases or full transcripts;
- the Search Controller requires direct product dispatch or deployment authority;
- useful decisions require a universal scalar score;
- hidden grader protection requires a permanent centralized security service;
- file/Git records cannot support one bounded Campaign without a database;
- a fixed human-designed candidate set yields the same decisions with materially less cost;
- static held-out evaluation predicts Security decisions as well as coevolution;
- the loop optimizes benchmark scores without replicated real improvement.

Delete or narrow CEL-R4 if its only result is orchestration overhead around scripts and receipts that are already easy to operate directly.

## 16. Ready Frontier

CEL-R4 implementation does not begin now.

The immediate sequence is:

```text
finish HHO-P0 closeout
→ implement and accept HHO-P1 Core
→ execute HHR-R3 deterministic smoke and repeated native baseline
→ freeze TrialDisposition and ObservationSelectionManifest from real evidence
→ implement CEL-R4 E0 shadow records
→ run E1 Observation Gateway self-optimization
```

Before that point, current P0 and P1 engineering may use CEL terminology as design guidance, but must not claim an automated discovery loop.
