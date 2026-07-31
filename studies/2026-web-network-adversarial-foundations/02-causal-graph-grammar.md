# 02 — Causal Graph Grammar

## Why a graph rather than a list

A vulnerability list answers which known concrete defects exist. It does not by
itself answer:

- which useful system property made the defect reachable;
- which identities, paths, or trust assumptions are required;
- which bounded capability exploitation would create;
- how several weak capabilities combine;
- which defender action breaks the path;
- how an adaptive opponent can route around that action;
- what evidence proves the final world outcome;
- what persists after the original vulnerability is removed.

R0 therefore uses a typed causal graph. It is an analysis grammar, not a new
wire protocol or database schema.

## Node classes

### G0 — Indispensable affordance

The useful property: connectivity, delegation, dynamic interpretation,
composition, caching, asynchronous execution, encryption, or automation.

### G1 — Structural tension

The unavoidable or recurring conflict introduced by the affordance.

### G2 — Assumption, trust boundary, or exposure

A concrete condition that safe behavior depends on: parser agreement, identity
scope, egress, freshness, build integrity, isolation, observer independence, or
operator response.

### G3 — Weakness

A recurring design or implementation failure class.

### G4 — Concrete vulnerability or hazardous state

The product-, version-, configuration-, or deployment-specific condition that
can be exercised.

### G5 — Exploit primitive

The bounded capability obtained: read, write, execute, impersonate, request,
redirect, persist, conceal, influence, or deny.

### G6 — Attack-chain state

A joined capability or changed position that enables later action: an internal
network position, a privileged identity, a trusted update channel, a durable
body, a poisoned memory, or a disabled observer.

### G7 — Campaign action and adaptation

Reconnaissance, resource preparation, access, execution, persistence,
credential acquisition, discovery, movement, collection, command and control,
exfiltration, impact, deception, defense impairment, withdrawal, or a revised
path after counteraction.

### G8 — World outcome and residual state

The actual domain consequence, evidence quality, remaining capability,
uncertainty, service state, and future option space.

## Edge types

Use explicit relations rather than an untyped arrow:

- `requires` — a precondition must hold;
- `enables` — creates a new capability or reachable state;
- `amplifies` — increases scale, reliability, speed, or consequence;
- `bypasses` — avoids a policy or observation boundary;
- `inherits` — receives authority or trust from another component;
- `conditions` — makes evidence or capability valid only under a path, identity,
  version, time, or environment;
- `conceals` — reduces defender observability or attribution;
- `persists-through` — survives a restart, patch, model replacement, or body
  replacement;
- `propagates-to` — transfers code, instruction, memory, identity, or capability;
- `invalidates` — makes a previous claim, decision, or binding stale;
- `detects` — creates evidence for a condition;
- `blocks` — removes a feasible attacker edge;
- `recovers` — restores required service or authority;
- `eradicates` — removes or invalidates adversary capability;
- `verifies` — establishes a declared world outcome;
- `leaves-residual` — preserves unclosed state or uncertainty.

## Hyperedges and joins

Many failures require several conditions simultaneously:

```text
valid low-privilege identity
+ reachable management interface
+ authorization weakness
+ permissive egress
→ higher-value primitive
```

This is a hyperedge, not a simple pairwise chain. Removing any one required
condition may break the path. Other conditions merely amplify the path and may
change the nature or consequence without being strictly necessary.

## A non-operational parser-differential example

```text
G0 compatibility across heterogeneous HTTP components
→ G1 tolerance versus unambiguous framing
→ G2 front and back recipients interpret one message differently
→ G3 inconsistent parsing and policy application
→ G4 one concrete deployment accepts an ambiguous request
→ G5 attacker can cause a hidden request to reach a downstream component
→ G6 downstream request executes under a connection or policy context not
     intended by the front component
→ G7 the actor combines the primitive with identity, cache, or internal-service
     conditions
→ G8 a world state changes; evidence must identify what each recipient parsed
```

RFC 9112 explicitly recognizes that lenient parsing differences among multiple
recipients can produce request-smuggling vulnerabilities. [R12]

The lesson is not that compatibility should be deleted. It is that security
policy and execution cannot safely depend on divergent interpretations.

## Attack graph and defense graph are dual but not symmetric

A defense can act on several levels:

```text
remove exposure
reject ambiguous input
reduce identity scope
remove egress
observe the primitive
interrupt the joined state
rotate inherited authority
restore the service
verify residual closure
```

The defender does not need to eliminate every weakness if it can reliably make
all high-consequence paths infeasible or strategically unattractive. Conversely,
a patch that removes one vulnerability is insufficient if the actor already
owns a later chain state such as a credential, session, web shell, external
object, or poisoned durable memory.

## Adaptive search

An Agent opponent changes graph reasoning in four ways:

1. it can search several candidate paths in parallel;
2. it can generate a local Tool to test or realize one edge;
3. it can update beliefs after each observation;
4. it can route around a removed edge while preserving Campaign objective.

This does not make the graph infinite or make defense impossible. It changes the
unit of evaluation from one fixed path to a distribution of paths, attempts,
Tools, identities, worlds, and opponent policies.

## Minimum chain dossier

Every analyzed chain should record:

```text
affordance and value
structural tension
assumptions and trust boundaries
weaknesses and concrete vulnerabilities
required exposures and identities
obtained primitives
joined chain states
actor objective and observed actions
defender controls and missed opportunities
world outcome and residual state
evidence source, uncertainty, and counterfactual breakpoints
Agent amplification hypothesis
Ordivon ownership and deletion decision
```

## Anti-patterns

Do not:

- draw an arrow directly from `internet` to `compromise`;
- equate a CVE with a full Campaign;
- infer root compromise from a single suspicious response;
- infer safety from a blocked payload;
- treat ATT&CK as a causal software graph;
- treat a successful benchmark score as evaluator integrity;
- assign adversarial intent inside World observation components;
- create a universal graph service before two real consumers need one.
