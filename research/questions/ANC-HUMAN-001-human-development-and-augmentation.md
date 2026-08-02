# ANC-HUMAN-001 — Human Development, Agency, and Human–AI Co-Development

## Question

What minimum dynamic model and evidence practices explain changes in human capability, agency, well-being, and life trajectory across time and context while distinguishing population association from individual intervention and AI augmentation from dependence or displacement?

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

## Initial hypothesis

A useful minimum model needs three orthogonal views:

```text
level of organization
× variable role
× time and trajectory
```

Candidate levels include biological substrate, bodily functioning, cognition and affect, identity and preferences, behaviour, capability, resources, relationships and institutions, and physical or digital environment.

Candidate variable roles include relatively stable attribute, state, behaviour, resource, environment, event, trajectory, outcome, measurement, and latent construct. Confounder, mediator, moderator, and collider are study-specific causal roles rather than permanent variable types.

The model should preserve feedback, heterogeneity, developmental timing, measurement error, selection, and history without assuming a universal scalar human objective.

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

## H0 evidence program

### H0-A — Framework composition

Map several materially different questions across ICF, RDoC, OECD well-being, cohort, life-course, and Ordivon-specific human–AI concerns. Record which concepts are directly reused, which combinations are required, and which proposed additions have no consumer.

### H0-B — Model deletion tests

Represent contrasting cases such as:

- sleep, stress, and cognitive performance;
- skill formation, income, time autonomy, and tool access;
- a health or financial shock and recovery trajectory;
- AI-assisted work with immediate performance gain but uncertain transfer;
- social support, participation, and subjective well-being.

Delete each proposed layer or variable distinction in turn. Retain it only if the deletion causes a named analytical, causal, measurement, privacy, or intervention failure.

### H0-C — Population-to-individual inference

Compare a population association, a longitudinal within-person estimate, and a bounded N-of-1 intervention under simulated heterogeneity, trends, regression to the mean, carryover, and measurement error.

### H0-D — Human–AI capability transfer

Define evidence that separates:

```text
model-performed output
human-plus-model system capability
human retained capability without the model
human ability to direct, verify, refuse, replace, and recover from the model
```

A short-term task score alone is insufficient.

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

## Falsification and narrowing

Narrow or close the branch if:

- existing mature frameworks answer the selected questions without an additional Ordivon synthesis;
- the proposed model does not change measurement, inference, experiment, or system design;
- population and within-person distinctions create no decision improvement in real studies;
- human–AI augmentation can be adequately evaluated by existing learning and human-computer-interaction methods without a separate Ordivon research program;
- the repository accumulates taxonomy, data, or dashboards faster than falsifiable findings;
- privacy and maintenance cost exceed the information gained.

The default outcome of H0 is a smaller model, not a comprehensive platform.
