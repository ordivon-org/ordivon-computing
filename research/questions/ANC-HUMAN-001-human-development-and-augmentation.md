# ANC-HUMAN-001 — Human Development, Agency, and Human–AI Co-Development

## Question

What minimum dynamic model and evidence practices explain changes in human capability, agency, well-being, and life trajectory across time and context while distinguishing population association from individual intervention and AI augmentation from dependence or displacement?

## H0 result — completed 2026-08-02

Ordivon Human H0 completed at revision `1e0ae9bf744c80bf24f5fd03d05c2baa5001511b`.

The initial ten-level hierarchy did not survive deletion testing because it mixed state domains, actions, context, time, measurement, and causal roles. H0 retained a smaller question-specific structure:

```text
StudySpec
PersonState: body, mind, capability, situated state
Context
action
event or intervention
time and history
observation and measurement
explicit outcomes and value assumptions
```

A deterministic synthetic experiment separated an observational group difference (`−0.3480`), the true population average effect (`+0.3996`), and two individual effects (`+1.0500` and `−0.3100`). Repeated randomized within-person evidence recovered the target effects under the declared model.

Human–AI research now distinguishes model-performed output, joint human–AI system capability, retained human capability, and agency including verification, refusal, replacement, and exit.

The repository remains research-only. H0 admitted no human data collection, universal schema, user profile, score, database, dashboard, model pipeline, or new CI.

Bound evidence: [`../evidence/snapshots/ordivon-human-h0-closeout-20260802t021412z.json`](../evidence/snapshots/ordivon-human-h0-closeout-20260802t021412z.json).

## Why this is an Ordivon Computing question

Ordivon currently represents people mainly as participants, owners of resources and consequences, sources of Goals, and recipients of decisions. That is necessary for system authority but insufficient for reasoning about the person who is developing, learning, tiring, adapting, ageing, collaborating with Agents, or changing goals.

The domain-specific research belongs in `ordivon-human`. Computing retains only the cross-project question: which findings materially revise participant, organization, adaptation, evaluation, Game, Host, or human–Agent system assumptions?

## Existing mature baselines

The project begins from mature frameworks rather than a new universal taxonomy:

- WHO ICF for bodily functioning, activity, participation, and environment;
- NIMH RDoC for dimensional cognition, affect, social processes, regulation, development, and multiple units of analysis;
- OECD well-being frameworks for plural outcomes, distribution, deprivation, and future resources;
- longitudinal multimodal cohort practices represented by NIH All of Us and UK Biobank;
- life-course models for timing, path dependence, reciprocal person–environment interaction, and development across the lifespan;
- established statistical, causal-inference, psychometric, longitudinal, qualitative, and N-of-1 methods.

Ordivon Human must reuse these native concepts where they are sufficient. Renaming them does not create an Agent-native or Ordivon-specific contribution.

## Initial hypothesis tested by H0

The initial hypothesis used three orthogonal views:

```text
level of organization
× variable role
× time and trajectory
```

Candidate levels included biological substrate, bodily functioning, cognition and affect, identity and preferences, behaviour, capability, resources, relationships and institutions, and physical or digital environment.

Candidate variable roles included relatively stable attribute, state, behaviour, resource, environment, event, trajectory, outcome, measurement, and latent construct. Confounder, mediator, moderator, and collider were study-specific causal roles rather than permanent variable types.

H0 retained the need for state, context, action, event, time, observation, and outcome distinctions but rejected the ten-level hierarchy and several proposed variable roles. Stability became a temporal property; trajectory became derived; latent status became epistemic; causal roles remain study-specific.

## Primary failure classes

1. **Static snapshot error** — a cross-sectional value is mistaken for a stable person property or developmental trajectory.
2. **Proxy substitution** — income becomes freedom, body mass becomes health, test score becomes intelligence, engagement becomes well-being, or output becomes capability.
3. **Within/between-person conflation** — differences across people are treated as the effect of changing one person.
4. **Population determinism** — group distributions override current individual evidence.
5. **Causal overclaim** — prediction or association is presented as an intervention mechanism.
6. **Outcome collapse** — health, agency, wealth, relationships, learning, meaning, and contribution are combined without explicit values and trade-offs.
7. **Measurement blindness** — the instrument, sampling process, missingness, observer, platform, or tracking intervention is omitted from the claim.
8. **AI augmentation illusion** — immediate output gain is treated as durable human capability despite dependence, deskilling, goal displacement, or loss of exit.
9. **Ontology accumulation** — more fields and categories create maintenance and apparent precision without changing a real inference.
10. **Privacy inversion** — cheap collection is treated as sufficient reason to retain intimate human data.

## H0 evidence program — completed

### H0-A — Framework composition

Compared WHO ICF, NIMH RDoC, OECD well-being, NIH All of Us, UK Biobank, life-course, within-person, N-of-1, and human–AI evidence against five materially different cases.

### H0-B — Model deletion tests

Tested sleep/cognition, skill/resources, shock/recovery, AI assistance, and relationships/well-being. The permanent hierarchy and non-causal roles were deleted where they added no analytical value.

### H0-C — Population-to-individual inference

Executed a deterministic synthetic experiment with confounded observational selection, heterogeneous effects, two opposite-sign target responses, repeated randomized individual trials, trend, carryover, event windows, and measurement noise.

### H0-D — Human–AI capability transfer

Defined evidence that separates:

```text
model-performed output
human-plus-model system capability
human retained capability without the model
human ability to direct, verify, refuse, replace, and recover from the model
```

A short-term task score remains insufficient.

## Repository and authority boundary

`ordivon-human` may own research documents, reproducible analyses, synthetic fixtures, legally reusable aggregate evidence, and narrowly justified private-study methods.

It does not own:

- a universal user profile or identity service;
- participant authority, consent enforcement, or Host decision routing;
- medical diagnosis or treatment;
- a public personal-data warehouse;
- a mandatory human ontology for other Ordivon projects;
- a personal ranking or optimization score.

Private identifiable observations remain outside public Git and outside Computing's shared research corpus.

## Falsification and reopening

Reopen or materially revise this question only if:

- a bounded H1 study shows that the reduced model omits a necessary distinction;
- the retained distinctions do not change inference, experiment, or system design in real use;
- population and individual evidence cannot be combined without a different structure;
- human–AI capability and agency are fully captured by mature learning or HCI methods without this cross-domain synthesis;
- privacy and maintenance cost exceed the information gained.

H0 reached the intended smaller-model outcome. H1 is ready but inactive; it requires a bounded real measurement study rather than general collection infrastructure.
