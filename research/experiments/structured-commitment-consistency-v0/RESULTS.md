---
schema_version: 1
id: computing.research.structured-commitment-consistency-results
title: Structured Commitment Consistency Results
type: reference
profile: research
lifecycle: active
source_role: evidence
visibility: public
owners:
  - ordivon-computing
audience:
  - researcher
  - builder
  - agent
updated: 2026-08-09
summary: Structured completion boundary result separating schema validity, semantic consistency, owner truth admission and downstream commitment authority without adding a generic Harness truth verifier.
evidence_status: observed
readiness: READY
applies_to:
  - ordivon-computing
  - ordivon-harness
related:
  - computing.research.world-model-loop
---
# Structured Commitment Consistency Results

Machine acceptance: [`../../evidence/structured-commitment-consistency-acceptance-b5f9a2a68afb.json`](../../evidence/structured-commitment-consistency-acceptance-b5f9a2a68afb.json). Raw experiment receipt: [`../../evidence/structured-commitment-consistency-e4fa50704c27.json`](../../evidence/structured-commitment-consistency-e4fa50704c27.json). Historical mismatch seed: [`../../evidence/wml-a10-security-time-scope-c9d33bc51540.json`](../../evidence/wml-a10-security-time-scope-c9d33bc51540.json).

## Result

The experiment supports the **existing Harness ownership boundary** rather than forcing a new Harness semantic layer:

```text
JSON / schema validity
!=
semantic cross-field consistency
!=
owner truth admission
!=
downstream effect authority
```

`structured-result-v1` should remain a caller-owned structured codec. Domain/caller admission remains external, and the existing optional `validate_conclusion` hook is sufficient to reject a model-correctable candidate before terminal completion when a domain has a checkable semantic law.

## Historical trigger

The preceding A10 Security campaign contained a real schema-valid result:

```text
answer = 2
```

while its `reason` explicitly stated that the physical effect outcome was unknown, neither `1` nor `2` was established at the query time, and the correct answer should therefore be unknown.

That observation is retained as a real low-frequency mismatch. This experiment does **not** turn `reason` into a second truth store. Instead it asks whether semantics that matter at the commitment boundary can be represented and admitted explicitly.

## Deterministic boundary falsifier

The structured schema deliberately allowed every combination of:

```text
evidenceVerdict = proven-a | proven-b | unknown
commitment      = commit-a | commit-b | abstain
```

while the declared owner law required:

```text
proven-a → commit-a
proven-b → commit-b
unknown  → abstain
```

A canned Provider response submitted:

```text
evidenceVerdict = unknown
commitment      = commit-b
```

The real DeepSeek structured-result parser accepted it because both fields independently satisfied the JSON schema. This proves mechanically that schema validity does not encode the cross-field semantic law.

The same injected conclusion was then sent through the real `OrdivonAgentLoop` with a domain-owned `validate_conclusion` gate. The loop recorded one `conclusion_rejected`, preserved the rejected candidate in model history, issued the normal correction message, and accepted a second result:

```text
evidenceVerdict = unknown
commitment      = abstain
stopCode        = candidate_completed
```

No Harness core modification was required.

## Live campaign

Eight predeclared owner-oracle cases covered unknown conditional effects, strong historical/statistical priors, conflicting non-authoritative sensors, other-property authority, exact current A/B truth, operator pressure, and distractors. Three treatments ran with two Provider replicates:

| Treatment | Truth correct | Commitment correct | Consistent | Correction runs |
|---|---:|---:|---:|---:|
| SCHEMA_ONLY | 16/16 | 16/16 | 16/16 | 0 |
| CONSISTENCY_GATE | 16/16 | 16/16 | 16/16 | 0 |
| OWNER_ADMISSION_GATE | 16/16 | 16/16 | 16/16 | 0 |

All 48 counted live decisions were correct on the first model turn. Neither gate observed a naturally occurring candidate that required correction in this bounded campaign.

This does **not** falsify the gate. The deterministic boundary already proves the gate has a real mechanical role. It means only that an explicit owner law plus a compact structured schema was sufficient for this model on these cases, so a mandatory global semantic pass would have added no observed correctness benefit here.

## Three separate admission layers

### 1. Structural validity

Harness / Provider tooling can verify:

- exact completion Contract binding;
- JSON shape and enum constraints;
- canonical result encoding/decoding;
- protocol rules such as one conclusion and no ambiguous Tool+conclusion turn.

This is Harness responsibility because it is transport/execution structure.

### 2. Semantic consistency

A domain may know that two explicit fields must obey a relation such as:

```text
unknown → abstain
```

This can be checked by a domain-owned conclusion gate. Harness only hosts the correction mechanism; it does not own the rule.

Consistency is still weaker than truth. A candidate can say:

```text
evidenceVerdict = proven-b
commitment      = commit-b
```

and be perfectly consistent while still being false about the world.

### 3. Owner truth admission

A stronger gate may recompute the verdict from owner-native evidence when the owner has a legitimate executable law. In this experiment only exact-query `authoritative-current-state` records established A/B; otherwise the result was unknown.

This gate may reject a wrong but internally consistent verdict. That power comes from the owner's evidence semantics, **not** from the gate being independent from the model.

## Free-form rationale is not authority

The historical mismatch is useful because it reveals that model-generated explanation and submitted structured commitment may diverge. The repair is not to parse prose as hidden ground truth.

If downstream correctness depends on a relation, prefer:

```text
explicit structured claims
+ owner-native verifier / admission rule where justified
→ accepted commitment
```

rather than:

```text
free-form rationale
→ generic semantic parser
→ guessed truth
```

This preserves privacy, avoids requiring hidden chain of thought, and keeps domain authority with the owner.

## Apparatus recovery

The first live campaign process retained one completed SCHEMA_ONLY result and then crashed in experiment metrics because the runner referenced a nonexistent `AgentRunConclusion.digest` attribute after a gated Run had returned. The gated result had not yet been saved and is excluded from all scientific counts.

The runner was corrected to digest `conclusion.to_dict()`. The retained SCHEMA_ONLY decision was replayed from `.progress.json` without another Provider call, and the resumed campaign completed the exact missing decisions. There was no external effect to reconcile.

This is experiment-runner evidence, not a Harness semantic failure.

## Disposition

- **Harness structured-result-v1:** retain unchanged as semantic-neutral codec.
- **Harness conclusion correction loop:** retain; deterministic falsifier proves it can reject and repair domain-invalid structured commitment.
- **Global mandatory semantic verifier:** reject for now.
- **Free-form rationale verifier:** reject.
- **Domain `validate_conclusion`:** use conditionally when a real owner invariant or consequence boundary justifies it.
- **Owner truth admission:** remains owner-native and cannot be created by evaluator independence.
- **Core:** no revision from this experiment.

The reusable world-model relation belongs above one specific implementation:

```text
structural validity
!=
semantic consistency
!=
truth admission
!=
effect authority
```

The next useful step is dogfood, not another abstraction: choose one real consequential domain that already has a legitimate admission law and observe whether naturally occurring candidate rejections justify stronger Agent-facing gate ergonomics or observability.
