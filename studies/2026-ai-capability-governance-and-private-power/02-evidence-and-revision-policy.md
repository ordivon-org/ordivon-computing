# G0 Evidence and Revision Policy

## 1. Evidence classes

```text
E0  analytical concept or normative proposal
E1  official Provider policy, terms, constitution, or access documentation
E2  official technical report, system card, classifier paper, or implementation evidence
E3  statute, regulation, court, regulator, or other public authority record
E4  aggregate transparency, enforcement, appeal, or market data
E5  controlled reproducible observation or experiment
E6  individual incident, account report, leaked record, or litigation allegation
E7  causal chain supported by multiple independent evidence classes
```

Evidence class is not quality rank alone. An E1 policy is authoritative about the
published rule but may be weak evidence about actual implementation. An E5
experiment can establish observed behavior under one configuration but not the
Provider's intent or population-wide error rate.

## 2. Source hierarchy

Prefer in order, subject to the claim:

1. exact official policy or legal text;
2. official technical documentation and transparency reports;
3. peer-reviewed scholarship and primary research papers;
4. regulator, court, standards, or government records;
5. archived Provider pages and version diffs;
6. high-quality investigative reporting;
7. individual reports, forums, and social media.

Lower-tier sources are retained when they supply unique incident leads, but their
claims remain explicitly provisional.

## 3. Revision binding

Every Provider or legal record should preserve:

```text
sourceId
publisher
canonical URL or DOI
retrievedAt
publishedAt / effectiveAt when available
observed revision, version, or page label
content digest when lawfully archived
previous revision
changed clauses
change classification
```

A current page must not silently overwrite historical claims. Search-engine
snippets, web archives, and cached copies are supporting evidence, not automatic
proof that an older rule remained effective.

## 4. Policy-to-implementation separation

For every material rule, create distinct records for:

```text
Normative Rule
Technical Mechanism
Observed Intervention
Account / Organization Consequence
Appeal / Remedy
Residual Uncertainty
```

Do not infer a classifier from a policy statement or infer the full policy from a
single classifier event.

## 5. Provider-intervention ledger

Controlled observations should record separately:

- Provider and model;
- model revision or observation date;
- surface and API mode;
- account/organization/access tier;
- region and retention mode when material and lawful to record;
- request identity and latency;
- extra review or routing signal;
- model proposal;
- refusal or rewritten content;
- Tool definitions shown to the model;
- Tool Calls proposed;
- Host admission or rejection;
- Runtime admission, rejection, `UNKNOWN`, or observation;
- World Effect and independent verification;
- authorized utility;
- recovery and residual state.

A refusal is an intervention result, not an attack-defense verdict.

## 6. Enforcement statistics

Aggregate ban, appeal, reversal, or moderation counts require denominators and
category definitions. Without active-account counts, cause categories, automation
rates, duplicate-account handling, and unappealed-error estimates, the following
must not be inferred:

- false-positive rate;
- fraction of legitimate users affected;
- relative strictness across Providers;
- intent or political motivation;
- quality of all unappealed decisions.

Reversal counts prove that reversible error exists, not its total prevalence.

## 7. Incident and allegation discipline

For E6 material, record:

```text
claimant
claim date
claimed event
available artifacts
Provider response
independent corroboration
alternative explanations
legal or procedural status
unresolved facts
```

Do not convert an allegation into a Provider-wide rule.

## 8. Causal claim requirements

A C-class claim should include:

1. temporal order;
2. mechanism;
3. affected resource or capability;
4. competing explanations;
5. comparison or counterfactual;
6. independent consequence evidence;
7. residual uncertainty.

Policy timing alone does not establish causation.

## 9. Normative claim requirements

An N-class claim must name:

- protected interests and rights;
- plausible harms and severity;
- all materially affected parties;
- distribution of benefits and burdens;
- necessity and proportionality;
- narrower alternatives;
- explanation, appeal, remedy, and exit;
- uncertainty and reversibility.

“Safety,” “freedom,” “innovation,” and “national security” are not self-executing
justifications.

## 10. Architecture claim requirements

An A-class Ordivon implication requires:

- at least one reproduced engineering failure;
- a second materially different consumer, Provider, surface, or workload;
- exact ownership;
- compatibility with thin-core and provider-neutral boundaries;
- cost, complexity, privacy, and governance analysis;
- a deletion or rollback test.

Political disagreement with a Provider is not sufficient evidence for a new
Ordivon subsystem.

## 11. Evidence redaction

Do not store Provider secrets, API keys, personal account data, raw flagged
conversations, or third-party sensitive content in public research evidence.
Preserve identities through safe digests and bounded metadata when possible.
Owned Canary content may be stored only when it creates no reusable third-party
harm and is explicitly marked.

## 12. Counterevidence and revision

Every theory and provider case must include:

- evidence supporting the interpretation;
- evidence weakening it;
- facts that would reverse the conclusion;
- observed policy changes;
- confidence and unresolved questions.

The study should become less certain when evidence conflicts, not more rhetorical.
