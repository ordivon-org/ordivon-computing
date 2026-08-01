# 08 — Agent Differential Discovery and Defense

## What changes with Agents

Parser differentials, fuzzing, request smuggling, cache poisoning, and injection
predate LLM Agents. Agent systems do not create the underlying classes. They
change the economics and composition of discovery and exploitation.

## Agent amplification

### Documentation and source synthesis

An Agent can read standards, implementation code, release notes, error messages,
and configuration to generate hypotheses about disagreement points.

### Cross-stack Tool construction

It can construct adapters for several clients, parsers, languages, browsers,
proxies, and downstream interpreters without relying on one preinstalled scanner.

### Differential execution

```text
one generated input corpus
→ parser A projection
→ parser B projection
→ gateway route
→ cache key
→ origin behavior
→ browser DOM
→ model interpretation
```

The Agent can cluster outputs and prioritize differences that cross a security
boundary.

### Input minimization

After finding a difference, the Agent can remove irrelevant structure until the
smallest representation that preserves disagreement remains. This improves
understanding and transfer.

### Adaptive search

It can change strategy after:

- parser errors;
- normalization output;
- cache hits and misses;
- protocol downgrade;
- WAF or Host refusal;
- Tool limitations;
- defender patches;
- model or evaluator feedback.

### Cross-domain composition

A weak URL or field differential may be combined with:

- a valid Session or Token;
- internal network access;
- a cache;
- an upload feature;
- a template or query interpreter;
- a generated Tool;
- Agent memory or prompt injection;
- an evaluator blind spot.

## Safety-profile confound

NIST's Agent-hijacking evaluations show that adaptive and repeated attacks can
materially change measured success, while its evaluation-cheating work shows
that a model can exploit gaps between intended and implemented tasks. [R18][R19]

Accordingly, a later Ordivon evaluation must not report:

```text
model refused representation
→ differential absent
```

or:

```text
model produced representation
→ primitive demonstrated
```

It must report separately:

- hypothesis quality;
- input generation;
- Tool admission;
- request transmission;
- per-component interpretation;
- bounded primitive;
- objective effect;
- detection and containment;
- evaluator validity.

## Differential-discovery experiment shape

A future owned-range experiment can use:

```text
Generator
  model, mutation engine, or corpus producer

Representations
  raw bytes and typed source objects

Subjects
  exact parser, proxy, cache, framework, browser, and application revisions

Projection
  each subject's parsed or canonical result

Comparator
  structural difference detector

Security oracle
  whether the difference crosses policy, routing, cache, execution, or evidence

World oracle
  authoritative final Effect

Minimizer
  smallest input preserving the relevant differential
```

This experiment should begin with mature parsers and test suites rather than a
custom Ordivon scanner.

## Evaluation dimensions

- nominal and malformed inputs;
- standards-conformant alternative representations;
- HTTP/1.1, HTTP/2, HTTP/3, translation, and transition paths;
- multiple URL, form, field, MIME, HTML, and application parsers;
- single and multi-stage decoding;
- cache cold, warm, stale, and purged state;
- browser, direct API, and generated Tool channels;
- one-shot, repeated, and adaptive attempts;
- known and held-out implementations;
- model/Host policy profiles;
- attacker knowledge of defenses;
- defender patch and regression state.

## Defensive Agent capabilities

A Blue Agent can use the same power to:

- inventory every parser and transformation;
- generate conformance and translation tests;
- compare policy and executor representations;
- identify unkeyed cache dependencies;
- synthesize strict schemas and typed adapters;
- minimize production incidents into regression cases;
- trace residual cache and session state;
- propose component deletion or path simplification;
- continuously compare new versions against held-out corpora.

## Defensive graph cuts

### Reduce interpreter count

Delete duplicate parsing and conversion layers where mature typed interfaces
suffice.

### Align policy and execution

Policy should inspect the typed representation that controls routing, resource
selection, and execution.

### Reject ambiguity

Do not allow each component to repair malformed input independently.

### Canonicalize at declared boundaries

Reserialize a typed object when crossing a protocol boundary rather than
forwarding partially parsed source text.

### Use typed downstream APIs

Parameter binding, argument vectors, schema objects, DOM-safe APIs, and explicit
capabilities reduce string-to-syntax transitions.

### Preserve independent evidence

The Agent under evaluation cannot be the sole source of parser projections,
request transmission, cache state, or final Effect.

### Evaluate held-out transfer

A defense tuned to one known payload or parser pair is not sufficient. Test new
representations, versions, and paths.

### Reconcile and close residual state

Purge poisoned caches, revoke derived authority, remove generated Tools, rebuild
compromised bodies, and verify external objects.

## Constraints should follow consequence

R2 does not recommend blocking broad reversible local analysis. High-capability
parsing, corpus generation, and differential reasoning can occur in disposable,
credential-empty environments.

Bind separately:

```text
external network targets
identity and Token access
persistent shared caches
production routing
Tool deployment
durable or irreversible Effects
```

This preserves offensive and defensive research power while avoiding accidental
third-party consequence.

## Architectural warning

A universal normalizer or policy gateway is attractive but dangerous:

- it becomes another parser;
- it can disagree with downstream systems;
- it centralizes authority;
- it may hide raw evidence;
- it can block valid behavior and create governance friction;
- compromise affects every consumer.

Prefer deletion, typed boundaries, native parser conformance, and targeted
adapters before creating a new shared service.
