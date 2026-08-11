# EX0–EX1 closeout — authority freeze and Host/Harness/Runtime causal pilot

## Result

EX0 succeeded. EX1 succeeded **as a falsification experiment**, not as confirmation of the initial representation hypothesis.

The strong result is not “causal-first prose explains Ordivon better.” The live tests showed the opposite lesson:

> Causal reconstruction is useful for auditing why a responsibility exists, but a single causal narrative and a single-primary-owner taxonomy are not reliable canonical Agent-facing representations. Ordivon's actual authority model is multi-axis: semantic choice, durable structural state, physical truth, external-effect truth and sharing disposition can have different owners at the same time.

The retained method is therefore **causal existence audit + explicit proof-boundary laws + multi-axis authority**, with owner-native product facts remaining authoritative.

## EX0 — exact authority freeze

The pilot froze only the decision-relevant current sources before explanation derivation:

| Owner | Frozen revision | Source-state digest |
| --- | --- | --- |
| Computing | `124feebcf145bfe53dac8aac33f81697267bd5e1` | `sha256:22ad5572f134fe2b04c961035f895c0fd65a5358a684d9f091e4d23118031084` |
| Host | `19207a8fc3c6a9661eb6fcbb2d27e6a1dc5c617c` | `sha256:0282270e7faff91cd95a00094c3fb82bba9474959c59c027ec69d14bed91631c` |
| Harness | `305dfe4aa10c6309c9e828211818ddc536ca1f7c` | `sha256:bc5c310f94d4e011645cd82fbb71b0963b60896231ac84dc10aeb299ec3cfb76` |
| Runtime | `dabb7b328c84288de2ec94e45a9299307f3491c7` | `sha256:0e8d448634b196d5a90b4241c0956b567488be2a0971d188b808d6e35115cadc` |

`authority-freeze-v1.json` binds the exact canonical dependency files and digests. Computing's own dependency digests were mechanically re-hashed inside the frozen Workspace; Host/Harness/Runtime canonical dependency digests were independently re-hashed inside their frozen Runtime Workspaces.

This follows the current P8/P9 research law: predeclare the applicability basis, consume only decision-relevant owner-native evidence, then perform fresh synthesis. The pilot did **not** copy dynamic production state into Computing or treat document recency as authority.

### Authority friction found during EX0

The Harness helper `scripts/configure_deepseek_api.py --check-only` rejected the current private DeepSeek secret because the helper requires an exact five-field object. Current Harness product source `DeepSeekSettings.from_secret_file()` explicitly permits the additional `credentialScopeId`, and loading through the current package source succeeded with `deepseek-v4-flash` and the current credential scope.

Disposition: this is a Harness helper/source drift finding. Product source is stronger authority for the accepted schema. The pilot did not mutate the secret or count this as a Harness architecture failure.

## EX1-A — owner-attribution pilot

The first live matrix compared a strong repository-first responsibility summary with a causal failure-chain summary.

- 16 frozen unseen cases;
- 10 hard Host/Harness/Runtime boundary cases;
- 3 semantic-overreach cases;
- 3 transfer cases (robotics, microscopy, hospital);
- 6 paired fresh DeepSeek Flash replicates;
- treatment order alternated by replicate;
- same credential slot within each pair;
- `thinking=disabled`;
- no prior result replay;
- semantic answers were never repaired.

Results:

| Treatment | Correct | Accuracy | Domain overreach | Transfer | Tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| repository-first | 96/96 | 100% | 0/18 | 18/18 | 15,273 |
| causal-first | 96/96 | 100% | 0/18 | 18/18 | 15,728 |

Predeclared classification: **CEILING_EQUIVALENT**.

Interpretation: the test had no discriminative power. Current three-repository canonical boundaries are already strong enough that a fresh model solved all owner-attribution and transfer cases from the compact responsibility summary. Causal prose neither improved correctness nor token use.

Wire-level note: repository-first required three extra physical Provider calls across two replicates because DeepSeek first returned wrong answer cardinality. Those were schema-invalid retries allowed by the frozen protocol and do not alter the 96/96 semantic result.

## EX1-B — existence/minimality stress

Because EX1-A hit a complete ceiling, a new stress corpus was frozen **before** any second-wave call. It changed the question from “which repository owns this?” to “what smallest owner, if any, is justified?”

Changes:

- Host/Harness/Runtime names were replaced by per-replicate opaque labels;
- `CLASSICAL_SUBSTRATE`, `CALLER_OR_DOMAIN`, and `NO_SHARED_MECHANISM` became available answers;
- cases attacked architecture hunger, classical delegation, domain-local effects and counterfactual deletion;
- 20 cases × 6 paired fresh replicates.

Results:

| Treatment | Correct | Accuracy | False Ordivon admission on anti-overbuild | Tokens |
| --- | ---: | ---: | ---: | ---: |
| repository-first | 119/120 | 99.17% | 0/54 | 16,974 |
| pure causal-first | 116/120 | 96.67% | 0/54 | 17,377 |

Predeclared classification: **MIXED_OR_FAILED**.

The real pure-causal failure was E16. In three causal replicates, a case where an arbitrary shell command may have produced an external payment was incorrectly pulled back into Runtime/classical execution even though only the external payment provider could prove occurrence. This reproduced exactly the boundary Runtime's Effect Kernel warns against:

```text
Execution Result != External Effect Receipt != Semantic Completion
```

Pure causal prose had stated that the owner of the uncertain fact should reconcile it, but the story made Runtime's local-reconciliation role more salient than the negative external-effect boundary. That is a representation failure.

E12 was different: both treatments answered `NO_SHARED_MECHANISM` instead of the frozen `CALLER_OR_DOMAIN`. Their reasons correctly said the provider-specific Finance receipt should remain local because no second consumer exists. The case therefore exposed overlap between two dimensions—local/domain ownership and no shared promotion—rather than a genuine causal misunderstanding. The preregistered primary result remains unchanged; this diagnosis is post-result method analysis.

## EX1-C — held-out causal + negative-boundary repair

We then revised the hypothesis rather than repairing E16 in place:

> If causal explanation is retained, explicit negative authority inequalities must travel with the causal chain.

A completely new 20-case held-out corpus was frozen. E12/E16 wording was not reused. Both treatments received the same facts, including:

```text
Host checkpoint != current physical/domain truth
Harness candidate completion != Task/domain completion
Runtime Execution Result != External Effect Receipt != Semantic Completion
arbitrary shell execution remains externally OPAQUE
```

The revised causal treatment organized those facts as failure chains; the control kept a repository/responsibility organization.

Results:

| Treatment | Correct | Accuracy | Critical external-effect overreach | False Ordivon anti-overbuild | Tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| repository-first | 105/120 | 87.50% | 0/12 | 2/36 | 17,086 |
| causal + boundaries | 106/120 | 88.33% | 0/12 | 2/36 | 17,126 |

Predeclared classification: **REJECT** because neither representation reached the 97.5% safe threshold.

The external-effect repair itself worked: neither representation committed a critical external-effect overreach. The remaining failures exposed a deeper test/modeling error.

### Why the held-out taxonomy failed

The error clusters were not random:

1. `CLASSICAL_SUBSTRATE` vs `NO_SHARED_MECHANISM` was not mutually exclusive. A generic distributed scheduler or stateless Provider SDK is classical substrate **and therefore** does not justify a new Ordivon layer.
2. `CALLER_OR_DOMAIN` vs `NO_SHARED_MECHANISM` was not mutually exclusive. A domain-specific evaluator/effect contract can remain domain-owned **and therefore** not graduate into shared infrastructure.
3. H17 forced “Agent chooses the WorkingSet” and “Harness persists/proves WorkingSet structure” into one owner. Both are true on different authority axes.
4. H09 forced “domain judges scientific validity” and “Host admits/records a verified Task outcome” into one owner. Again, judgment authority and durable state/admission authority are distinct.

The benchmark therefore recreated exactly the category error Ordivon's own architecture tries to eliminate: collapsing distinct facts into one state/owner.

## Revised Explanation Unit

Do **not** ask every feature or scenario for one universal `primaryOwner`.

The retained experimental unit asks separate questions:

1. **Reality / pressure** — what recurring failure exists?
2. **Classical baseline** — which mature mechanisms already own parts of the problem?
3. **Residual missing responsibility** — what exact non-bypassable responsibility remains unowned?
4. **Semantic choice** — who decides meaning, relevance, strategy or domain validity?
5. **Durable structural state** — who persists/validates the identity and transitions?
6. **Physical truth** — who proves execution/process/byte facts?
7. **External-effect truth** — who can prove the outside-world effect itself?
8. **Counterfactual deletion** — what concrete capability disappears if the candidate mechanism is removed while neighboring owners remain?
9. **Negative proof boundaries** — what tempting stronger claim is explicitly false?
10. **Sharing disposition** — classical delegation / domain-local / shared / not justified yet.
11. **Evidence and reopen condition** — what proves the current scope, and what new result would force revision?
12. **Feynman projection** — only after the authority axes are preserved.

This is an experiment/research lens, not a new product protocol.

## Host causal identity

**Reality:** semantic work outlives model/Run/process sessions and competing replacements can race.

**Residual responsibility:** durable Task/revision/checkpoint, consequence-level commitment/participant decision, verification and Task outcome admission.

**Delete Host:** Harness Runs and Runtime Jobs still exist, but there is no single revision-fenced semantic identity for what long-lived work still exists and what commitments/unknowns remain.

**Negative law:** Host semantic state is not current Runtime/Git/domain truth and does not own Provider execution.

Feynman form:

> Host is the durable notebook and commitment ledger for unfinished work. It remembers what the work still means, but its notes tell a replacement Agent where to re-check reality; the notes are not reality itself.

## Harness causal identity

**Reality:** one bounded cognition episode has selected cognition, caller interaction, transient observations, Provider call state, Tool action authority and recovery state that are neither the long-lived Task nor a physical process.

**Residual responsibility:** caller-neutral Agent Run structural cognition + Provider/Tool continuity.

**Delete Harness:** each caller rebuilds Provider/tool/recovery/current-cognition semantics or leaks those facts upward into Task state.

**Negative laws:** History != Cognition; Observation != Retention; Agent semantic choice != Harness structural truth; Tool intent != physical effect; Run completion != Task/domain completion.

Feynman form:

> Harness is the flight recorder and control rig for one stretch of thinking. It proves what the Agent saw and was allowed to do and how that Run resumes, but the Agent still decides what the evidence means and the caller/domain decides whether the larger objective is really satisfied.

## Runtime causal identity

**Reality:** an admitted action is not physical reality, and crashes/timeouts/drift/response loss create uncertainty about the exact operation/process/results.

**Residual responsibility:** stable Agent operation identity → one physical Attempt/process tree → bounded evidence → reconciliation without guessed success or blind redispatch.

**Delete Runtime:** Host/Harness can still decide and remember work, while every application again hand-rolls source binding, physical dispatch identity, process-tree evidence, cancellation and response-loss recovery.

**Negative law:** Runtime Execution Result != External Effect Receipt != Semantic Completion. Arbitrary execution is OPAQUE.

Feynman form:

> Runtime answers what exact local action really ran, what process tree belonged to it, what bytes came back, and what is still unknown after interruption. It does not turn exit 0 into proof that an outside payment/message/order happened or that the user's goal is complete.

`causal-units-v1.json` records these units with the new multi-axis representation.

## What EX1 actually proved

### Retain

- causal reconstruction as an **existence audit**;
- counterfactual deletion;
- classical-baseline comparison;
- explicit negative proof-boundary laws;
- owner-native evidence and exact applicability basis;
- multi-axis authority rather than one primary owner;
- strong compact repository/responsibility summaries for Agent navigation.

### Reject

- the assumption that causal prose is intrinsically better for fresh Agents;
- single-primary-owner explanation taxonomy;
- mutually exclusive `classical / local-domain / no-shared` categories;
- explaining a project only by a positive role without its strongest negative boundary;
- using comprehension benchmark accuracy to overwrite owner-native truth.

### Not yet tested

- human comprehension;
- diagrams/animation/interactive removal experiments;
- Studio narrative forms;
- Web information architecture;
- whether the multi-axis unit improves transfer beyond the current strong repository-first baseline;
- other Ordivon projects.

## EX1 disposition

EX1 is **complete**, but it does not authorize immediate EX2 using the original single-owner causal schema.

Before whole-family expansion, EX2 must consume the revised multi-axis Explanation Unit. The first expansion batch should include World plus one domain laboratory specifically because they stress the axes that Host/Harness/Runtime alone cannot fully separate: external-effect truth, domain semantic judgment and sharing/localization.

No new Explanation Service, ontology server, evaluator service or product schema is justified.

## Evidence volume

Across EX1-A/B/C, 36 accepted fresh Provider trials consumed **99,564 reported tokens**. Wire/schema-invalid retries raised physical Provider calls to **46**. The primary evidence files are `evidence/live-v1.json`, `evidence/stress-live-v1.json`, and `evidence/heldout-live-v1.json`; all retain per-case answers/reasons, request digests, Provider usage, retry corrections, opaque-label mappings and preregistered aggregate analysis.
