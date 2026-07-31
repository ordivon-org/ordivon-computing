# 00 — Method, Attacker Model, and Evaluation Confounds

## Research question

Which distinctions are required to reason correctly about identity and authority
when a browser or Agent can combine external content, persistent sessions,
delegated API access, generated Tools, and long-running Tasks?

## Why a strong attacker model is necessary

A defensive architecture optimized only against malformed input or a fixed
proof-of-concept will overestimate its safety. The relevant adversary may use:

- protocol-valid messages;
- legitimate accounts, OAuth clients, or resource servers;
- attacker-controlled origins and redirect targets;
- trusted browser affordances such as navigation, forms, embedded resources,
  and automatic credentials;
- compromised but correctly signed same-origin code;
- leaked bearer authority;
- delegated identities and downstream service calls;
- repeated probabilistic attempts;
- Agent-generated parsing, automation, or adaptation Tools;
- multi-step social, Web, identity, and API composition;
- attacks on monitors, logs, consent UI, and evaluators.

The strongest useful attacker model is not unlimited magic. It explicitly states
which trust roots remain intact. Unless a case demonstrates otherwise, R1 does
not assume compromise of:

- mathematically strong cryptography without key possession;
- hardware or workload attestation roots;
- an independent management plane;
- an independent evidence store;
- every browser process simultaneously;
- every identity provider, resource server, and endpoint at once.

## Authority path under study

```text
participant
  expresses purpose and owns resources

user agent / Agent Host
  selects and compiles current context

Web principal
  origin, site, frame, top-level site, process, or extension context

identity proof
  password, session, passkey, client key, workload identity, token

authorization grant
  audience, resource, action, amount, duration, delegation chain

execution context
  browser, Runtime, Tool, body, path, provider, current world state

resource server
  admits or rejects the concrete operation

world consequence
  actual durable observation or change
```

No single layer may infer the entire chain from one identifier.

## Source hierarchy

Use:

1. WHATWG and W3C living standards for browser behavior;
2. IETF RFCs and Best Current Practices for Cookies, origin semantics, OAuth,
   token restriction, and delegation;
3. official browser architecture documents for process isolation;
4. official workload-identity specifications;
5. official Agent-security evaluations for Agent-specific claims;
6. Ordivon executable evidence only when a future controlled experiment exists.

## Safety-profile and Host confounds

NIST's Agent-hijacking work demonstrates why adaptive and repeated attacks must
be measured against the complete configured system, while its evaluation-
cheating work shows that an Agent can exploit gaps between the intended task and
its implemented scorer or affordances. These results support treating model,
Host, policy, Tool, and evaluator behavior as bound experimental variables—not
as substitutes for world evidence. [R17][R18]

A model, provider, Host, Harness, system prompt, policy layer, or Tool broker may
refuse, rewrite, omit, or interrupt an action. That behavior is part of the
configured system and must be recorded, but it cannot be used to infer that:

- the underlying vulnerability does not exist;
- a differently configured or malicious Agent lacks the capability;
- the browser or identity mechanism is safe;
- a generated Tool could not perform the same action;
- a defender has observed or contained the world consequence.

Conversely, an Agent producing an aggressive plan does not establish that the
plan is executable, authorized, novel, or effective.

Later experiments must bind at least:

```text
model and provider
system and developer policy revisions
Host and Harness revision
Tool catalog and grants
World and identity configuration
attacker and defender prompt/profile
refusal, action, and world-outcome traces
independent verification
```

This prevents two symmetrical errors:

1. interpreting policy-induced non-action as absence of offensive capability;
2. interpreting unrestricted generated text as demonstrated offensive ability.

## Capability versus permission

R1 deliberately maximizes conceptual attacker capability while retaining a
strict external-consequence boundary:

```text
deep mechanism and attack-chain knowledge
+ strong hypothetical attacker
+ complete defensive analysis
≠ permission for public-target action
```

This follows Ordivon A7: capability and consequence are independent dimensions.

## Evidence claims

R1 labels statements as:

- **standard-defined** — required or described by a primary specification;
- **implementation-defined** — browser or provider-specific behavior;
- **observed** — supported by official experiment or incident evidence;
- **inferred** — derived from supported mechanisms under stated assumptions;
- **hypothesized** — Agent-era consequence requiring later experiment.

## Threat-model matrix

| Attacker | Capability | Main boundary tested |
|---|---|---|
| Web attacker | arbitrary origins, endpoints, accounts, clients, content, navigations | origin, ambient authority, redirects |
| Network attacker | observe, block, alter, or spoof unprotected traffic | TLS, endpoint identity, downgrade |
| Same-origin attacker | execute within a trusted origin through XSS or supply-chain compromise | origin as coarse trust unit |
| Browser-component attacker | extension or renderer compromise within declared scope | process, browser-process enforcement |
| Token attacker | obtain bearer or delegated credentials | replay, audience, sender constraint |
| Resource-server attacker | receive valid tokens or induce misrouting | audience, mix-up, downstream trust |
| Agent hijacker | shape external data interpreted by an Agent | data/instruction/authority separation |
| Adaptive Agent | retry, construct Tools, coordinate, and change path | cumulative and held-out evaluation |
| Evaluator attacker | exploit scoring, logging, or evidence gaps | evaluation integrity |

## Non-goals

R1 does not:

- teach account takeover or token theft procedures;
- enumerate bypass payloads;
- construct malicious browser extensions;
- provide exploit code or live CSRF/CORS test instructions;
- claim that every refusal can or should be bypassed;
- create a production identity architecture from standards reading alone;
- treat all user-agent behavior as identical across implementations;
- assume that more controls automatically improve net safety or productivity.

## Falsifiers

Revise R1 if:

- the proposed distinctions cannot explain important identity incidents;
- origin, authentication, authorization, delegation, intent, and consequence can
  be safely collapsed in realistic Agent workloads;
- generated Tool or Agent identity adds no failure class beyond ordinary service
  identity and OAuth clients;
- native standards already own every cross-layer invariant proposed for
  Ordivon;
- the framework encourages centralization without measurable recovery or
  attribution benefit;
- its recurring conceptual overhead exceeds the errors it prevents.
