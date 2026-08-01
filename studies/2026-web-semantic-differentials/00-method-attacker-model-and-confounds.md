# 00 — Method, Attacker Model, and Confounds

## Research question

How can Ordivon study real parser and interpretation attacks at full conceptual
strength without confusing one platform's policy behavior with the underlying
capability, and without prematurely building offensive or defensive machinery?

## Strong attacker model

The attacker may control or influence:

- HTTP request targets, fields, bodies, connection timing, and selected protocol
  paths;
- one or more Web origins, clients, intermediaries, or low-privilege accounts;
- uploaded content, API values, redirects, cacheable requests, and model-visible
  external data;
- encodings, Unicode forms, percent encoding, media types, schemas, duplicate
  fields, and nested formats;
- valid credentials or delegated Tokens obtained through a separate chain;
- generated Tool source, dependencies, or execution inputs where the World
  permits construction;
- repeated attempts and adaptive search over visible responses, errors, timing,
  cache behavior, and defender changes.

The attacker may build parsers, serializers, fuzzers, differential harnesses,
minimizers, protocol clients, and format translators. This is a capability model,
not authorization for deployment against unrelated systems.

Unless a concrete case establishes otherwise, R2 does not assume arbitrary
breakage of cryptography, full compromise of every interpreter, or control over
an independent evidence and management plane.

## Evaluation confounds

### Model and Host policy

A model or Host may:

- refuse to describe or emit one representation;
- paraphrase or normalize it;
- omit details;
- block Tool use;
- require additional confirmation;
- interrupt execution.

These actions alter the observed Agent path. They do not establish that:

- the protocol differential is absent;
- another parser, Agent, direct client, or generated Tool cannot produce the
  representation;
- the downstream service would reject it;
- the world Effect did not occur through another channel;
- a malicious Agent shares the same policy.

### Client-library normalization

A high-level HTTP, URL, database, or browser library might canonicalize or reject
an input before transmission. That proves the library's configured behavior, not
the behavior of the entire path.

### WAF or gateway response

A blocked request proves one observation at one boundary. It does not establish
which representation the origin, cache, or alternate path would see.

### Successful response

A `2xx`, parsed document, Tool return, or model claim does not establish the
intended world consequence. Intermediaries can generate status codes; caches can
serve earlier responses; downstream systems can partially commit.

### Benchmark success

An evaluator can accidentally reward a visible signal rather than the intended
capability. Differential discovery must be separated from exploitation,
objective completion, and evaluator integrity.

## Bound experimental variables

A later controlled experiment must bind:

```text
raw input bytes or structured source
all serializer and parser revisions
protocol versions and transitions
intermediary topology and translation
URL, field, media-type, and cache configuration
model, Provider, Host, Harness, and policy profile
Tool and generated-Tool revisions
identity and World scope
per-component interpretation or canonical representation
final Effect, authoritative observation, and residual state
```

## Source hierarchy

1. IETF Internet Standards and Best Current Practices;
2. WHATWG living standards and Web Platform Tests;
3. official browser and server architecture documentation;
4. MITRE CWE for recurring weakness relations;
5. official vendor or government incident records;
6. later Ordivon controlled experiments.

## Safety and research boundary

R2 may explain:

- why a differential exists;
- which components disagree;
- what bounded primitive can result;
- how the primitive composes into a Campaign;
- which defensive graph edges are available;
- how to evaluate fixes and residual state.

R2 does not provide:

- byte-level attack payloads;
- bypass strings or parser-evasion recipes;
- live differential probes;
- target-selection guidance;
- exploitation or persistence code;
- instructions to defeat platform policy.

## Evidence grades

- **S0 — standard relation:** a specification defines the parser or security
  requirement;
- **S1 — implementation differential:** at least two exact implementations or
  configurations demonstrably differ;
- **S2 — primitive:** the difference produces a bounded capability under an
  owned test condition;
- **S3 — chain:** the primitive composes with identity, cache, routing, or
  interpreter state into a measured objective effect;
- **S4 — adaptive transfer:** the result survives held-out implementations,
  paths, and defensive changes.

R2 is primarily S0 knowledge. It does not claim S1–S4 Ordivon evidence.

## Falsifiers

Revise or delete the framework if:

- it cannot classify important modern protocol or browser differentials;
- it adds no decision value over standards and native component traces;
- a single canonical representation can safely control all relevant layers in
  realistic systems;
- Agent additions merely rename ordinary fuzzing and automation;
- proposed evidence cannot be collected without duplicating native authority;
- product teams turn the framework into a universal blocking layer with greater
  cost than the failures it prevents.
