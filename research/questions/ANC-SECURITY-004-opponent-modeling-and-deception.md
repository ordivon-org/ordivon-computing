# ANC-SECURITY-004 — Opponent Modelling, Deception, and Information State

## Status

- Epistemic status: deferred reference question at M4
- Status authority: [`../portfolio.json`](../portfolio.json)
- Parent: `ANC-SECURITY-001`
- Depends conceptually on: `ANC-SECURITY-003`
- GitHub Issue: #73
- Reactivation condition: held-out policies and deliberate Context loss; Round 1 found diagnostic value but no objective-success or transfer benefit

## Question

How should an Agent represent and revise beliefs about an adaptive opponent, and
how should Ordivon distinguish authoritative world truth, actor observation,
actor belief, communicated claim, intended belief effect, deception, and
counter-deception?

## Why this question exists

In a non-adversarial loop, feedback is commonly treated as noisy evidence about
the world. Under intelligent opposition, feedback may be selected or fabricated
to cause a particular belief and action.

The same observed failure can result from:

- natural fault;
- hidden environment change;
- friendly action;
- opponent countermeasure;
- decoy or false flag;
- manipulated Tool output;
- evaluator intervention.

A transcript alone may preserve the words without preserving the competing
causal hypotheses.

## Candidate information layers

```text
world truth
  what actually holds in the environment

observation
  what one actor can perceive

belief
  the actor's probability or confidence over possible world/opponent states

claim
  information communicated by another actor, Tool, document, or service

intended belief effect
  what the sender wants the receiver to believe or do

deception hypothesis
  the receiver's hypothesis that observation or claim was strategically shaped

mutual / higher-order belief
  beliefs about what another actor believes, knows, or expects
```

The list is intentionally provisional.

## Core subquestions

1. Which opponent properties matter: objective, knowledge, capability, policy,
   risk preference, resource state, detection threshold, or organization?
2. Should opponent models be structured state, natural-language hypotheses,
   latent model state, or an ensemble of competing models?
3. How should an Agent retain contradictory explanations across Context and
   model replacement?
4. When should evidence update world belief versus opponent belief?
5. Can an actor detect that an opponent is modelling it and deliberately change
   its observable policy?
6. How should second-order beliefs be bounded so they do not cause unproductive
   recursive reasoning?
7. What counts as deception success: wrong belief, wrong action, resource
   misallocation, lost initiative, or changed strategic outcome?

## Required comparisons

- opponent modelling in reinforcement learning and game theory;
- POSG belief-state and information-structure models;
- Bayesian and signalling games;
- MITRE Engage and classical cyber deception/denial;
- honeypots, honeytokens, decoys, sinkholes, and moving-target defense;
- prompt/context/memory/Tool-output manipulation;
- Melting Pot and unfamiliar social-partner evaluation;
- ordinary provenance and trust labels.

## Experiment families

### Attribution ambiguity

Create identical observations from natural failure and active countermeasure.
Measure whether explicit competing hypotheses improve later choices.

### Policy switch

Change the opponent policy mid-Campaign. Test detection speed, false positives,
and adaptation quality.

### Deception and counter-deception

Allow both sides to expose decoys, conceal assets, communicate claims, and test
one another. Preserve independent world truth.

### Explicit versus implicit opponent state

Compare transcript-only, latent recurrent, natural-language hypothesis, and
structured/ensemble approaches.

### First-order versus second-order reasoning

Test whether modelling what the opponent believes improves decisions or merely
increases cost and hallucinated complexity.

## Evidence required

- authoritative world truth separate from every actor's observation;
- time-indexed hypotheses, confidence, supporting evidence, and revisions;
- explicit identification of observations later shown to be deceptive;
- information outcome separate from physical/tactical outcome;
- held-out opponent policies and deception styles;
- false-positive and stale-model costs;
- negative cases where explicit modelling worsens performance.

## Falsifiers

Reduce or delete the proposed structures if:

- transcript or recurrent state performs equivalently;
- explicit models overfit to known opponents;
- belief records become stale faster than they help;
- second-order reasoning adds no robust value;
- deception cannot be grounded separately from evaluator confusion or ordinary
  task failure.

## Cross-project implications

- Game may provide actor-specific observation and authoritative hidden state;
- Host may compile bounded opponent hypotheses into Context;
- Security may evaluate information position and deception outcome;
- Link may expose communication and path facts but should not infer intent;
- Runtime and Edge should preserve effects and world changes without assigning
  adversarial meaning.
