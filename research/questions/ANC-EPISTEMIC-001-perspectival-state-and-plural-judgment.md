# ANC-EPISTEMIC-001 — Perspectival State and Plural Judgment

## Status

- Epistemic status: deferred cross-domain question at M1
- Status authority: [`../portfolio.json`](../portfolio.json)
- First owner evidence: `ordivon-security` revision `334c4e7f69b2d3ff353580043229c259e79e77b9`
- Materially refines: `ANC-SECURITY-004`, `ANC-ORG-001`, and `ANC-VERIFY-001`
- Second workload required: one non-adversarial Game or Host case
- Implementation status: no shared primitive, service, protocol, or database admitted

## Question

When multiple participants act from bounded, provenance-bearing views of the same changing world, what minimum structure preserves perspective-specific observation, interpretation, commitment, judgment, and unresolved disagreement without inventing a universal truth store or a new consensus platform?

## Why this question exists

Ordivon already distinguishes Context from durable state and Observation from Fact. Security now provides a concrete first workload in which:

```text
one simulated world
→ Red-specific observation
→ Blue-specific observation
→ sensor telemetry
→ management-plane truth
→ different admissible actions and conclusions
```

The broader problem is not limited to deception or cyber conflict. Different conclusions can result from:

- different observations;
- the same evidence interpreted through different causal models;
- the same likely world state evaluated under different commitments, authority, or consequence exposure;
- beliefs about what another participant knows or intends;
- stale or selectively compiled Context;
- deliberate information shaping.

A system that forces these into one global current state may leak privileged evidence, erase legitimate disagreement, create false consensus, or make later evaluation unable to reproduce what one participant could reasonably have concluded.

## Working hypothesis

The first useful representation may be a reproducible composition rather than a new object:

```text
participant or role identity
+ ContextSelection and omissions
+ Observation / Artifact references
+ Claims and competing hypotheses
+ commitments and Authority
+ logical or wall-clock time
+ explicit uncertainty
```

A perspective-specific decision record should allow another process to reconstruct the decision boundary without granting the replacement Actor evidence that the original Actor did not possess.

## Candidate distinctions

1. **world occurrence or domain state** — what holds according to the owning domain, if knowable;
2. **Observation** — one attested reading through one access path;
3. **perspective** — the bounded evidence, role, commitments, authority, and omissions from which cognition operates;
4. **belief or hypothesis** — a revisable interpretation of possible causes or states;
5. **Claim** — a proposition communicated by another source;
6. **judgment** — a decision about value, sufficiency, priority, or action under one participant's responsibility;
7. **Verification** — a bounded evaluation under a declared method and authority;
8. **Fact** — an admitted Claim for one domain, scope, and version.

These distinctions are candidates. The research must delete or merge any layer that changes no behavior, attribution, recovery, or evaluation result.

## Minimum workloads

### Workload A — adversarial information asymmetry

Use an Ordivon Security Contest with exact actor-specific observations, sensor telemetry, and independent simulator truth. Introduce at least one event that supports several causal explanations or is visible to only one side.

Compare:

- transcript-only Actor state;
- explicit source-bound observations and hypotheses;
- equalized observations;
- swapped perspectives;
- deliberate Context loss and Actor replacement.

Measure action choice, attribution quality, stale-belief cost, information leakage, and evidence reconstructibility.

### Workload B — non-adversarial plural judgment

Use Game or Host with two participants who either:

- receive different bounded views of one world; or
- agree on the relevant facts but hold different commitments, authority, costs, or goals.

Compare forced consensus with a Join that preserves a factual core, alternatives, unresolved judgment conflict, and responsibility routing.

The second workload is required before any shared `Perspective`, `BeliefState`, or disagreement protocol is considered.

## Experiment families

### Observation equalization

Give actors the same evidence. If conclusions converge, the original difference was primarily informational. If they do not, inspect interpretation and commitment.

### Perspective swap

Swap actor-specific observations while preserving model, role, and objective; then separately swap role or objective while preserving observations. This distinguishes informational from commitment-driven divergence.

### Context omission and replacement

Remove one provenance-bearing source, replace the model or Harness, and test whether the system preserves what the original Actor knew, did not know, and inferred.

### Competing hypotheses

Preserve several causal explanations instead of one compressed summary. Test whether this improves later decisions under held-out world changes without creating stale-state overhead.

### Disagreement-preserving Join

Join independent Artifacts without requiring one consensus answer. Measure whether retained disagreement improves later action, verification, or responsibility routing.

## Evidence required

- exact participant, role, model, Harness, ContextSelection, world, and time identity;
- the Observation and Artifact set available to each participant;
- explicit omissions or inaccessible evidence where known;
- commitments, authority, and consequence exposure relevant to judgment;
- Claims, hypotheses, confidence, and revisions when the experiment tests them;
- independent world truth in simulation or bounded post-hoc adjudication in open worlds;
- intervention logs for perspective swap, evidence equalization, and Context loss;
- cases where preserving perspectives worsens cost, latency, confusion, or outcome;
- a second materially different workload.

## Falsifiers and deletion outcomes

Absorb this question into existing tracks and reject a shared perspective layer if:

- Observation, Claim, Verification, Fact, ContextSelection, and domain-local Actor state represent both workloads without loss;
- perspective records do not improve action attribution, replacement fidelity, disagreement handling, or held-out performance;
- a transcript plus source references is equally reconstructible at lower cost;
- explicit hypotheses become stale faster than they help;
- different conclusions disappear after ordinary evidence equalization and objective specification;
- the non-adversarial workload exposes no reusable responsibility beyond Security's opponent-model problem.

The deletion outcome is documentation-only retention under `ANC-SECURITY-004` and `ANC-VERIFY-001`, with no protocol or service.

## Cross-project implications

- **Security** supplies the first actor-specific, adversarial, hidden-truth workload;
- **Game** can provide low-consequence multi-faction or player/Agent perspectives and legitimate value conflict;
- **Host** may compile perspective-bound Context and preserve replacement identity without owning domain truth;
- **Harness** must not silently broaden evidence during model or Provider replacement;
- **Verify** should compare trajectories under the evidence actually available to each Actor;
- **Organization** research should preserve disagreement, refusal, and responsibility rather than equating coordination with consensus;
- **World and Runtime** preserve source and effect evidence but should not infer a participant's belief or intent.

## Boundary

This question does not deny external reality, promote relativism, define political legitimacy, or authorize autonomous high-consequence action. It asks how a computing system can preserve the causal role of bounded views and plural judgment while retaining evidence, domain authority, and the possibility of factual correction.
