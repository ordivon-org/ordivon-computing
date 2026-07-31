# 08 — Ordivon Insertion and the R2 Gate

## R1 result

R1 establishes that external authority is a graph, not a token or identity
field:

```text
participant
→ Task and Effect
→ acting Agent / service / Tool
→ browser or workload context
→ origin, site, endpoint, and path
→ credential and authentication event
→ authorization and delegation
→ concrete resource/action/parameters
→ world Effect
→ verification, revocation, and residual state
```

No current repository owns this complete graph, and no repository should copy
all native state to pretend it does.

## Host responsibilities

Host should own:

- participant purpose and current Task;
- stable Effect identity;
- which Agent or subtask is acting;
- semantic delegation and acceptable consequence;
- Context compilation that marks external content as evidence rather than
  authority;
- ToolGrant or equivalent Task-scoped capability selection;
- `UNKNOWN` and reconciliation;
- accepted Task completion.

Host should not store browser Cookies, replace OAuth authorization servers, or
become a universal IAM system.

## World responsibilities

World-native modules and providers may own facts about:

- URL, origin, site, endpoint, redirect, path, and provider;
- browser, frame, worker, extension, or body context;
- workload identity and generation;
- session or credential class and validity metadata, without exposing bearer
  secrets unnecessarily;
- Tool and Adapter revision, generated-Tool provenance, build, deployment, and
  retirement;
- provider-native authorization transactions, token families, Receipts, and
  callbacks;
- external object and Effect state;
- revocation, destruction, reconstruction, and residual observations.

R1 does not establish one World identity service or database. The facts remain
component-native until a cross-workload invariant is demonstrated.

## Runtime responsibilities

Runtime owns:

- Workspace and source truth;
- process and Job identity;
- local files, streams, and Artifacts;
- disposable build and test environments;
- local credential mounts or absence as an execution fact;
- process-tree and local residual evidence.

Runtime should not decide whether one OAuth delegation or browser action serves
the participant's intent.

## Security responsibilities

Security may own:

- strong attacker and defender profiles;
- Campaign and Actor identity;
- attack and defense authority-graph hypotheses;
- deception, hijacking, impersonation, and delegation-abuse interpretation;
- cumulative, adaptive, and held-out Trial families;
- tactical, operational, strategic, information, containment, recovery, and
  evaluator-integrity outcomes;
- Campaign-level residual closure requirements.

Security should not duplicate native browser, OAuth, workload, Runtime, or
provider journals.

## Game responsibilities

Game is the preferred early experimental substrate for:

- authoritative hidden intent and world state;
- user, Agent, browser, service, and attacker roles;
- controllable origins, sites, sessions, tokens, delegations, and Tools;
- attacker and defender policy switches;
- repeated seeds and counterfactual branches;
- evaluator-manipulation cases;
- no public-world consequence.

## Constraint audit

### Retain

- capability and consequence separation;
- component-native identity and evidence;
- explicit Effect and `UNKNOWN`;
- independent verification;
- generated Tool provenance;
- narrow delegation and revocation;
- residual closure.

### Do not promote yet

- universal Agent identity;
- universal authorization Schema;
- centralized World IAM;
- generic browser broker;
- generic token service;
- always-on Security policy engine;
- automatic classification of external content intent;
- mandatory approval for reversible research;
- assumption that every Agent needs browser authority.

### Deletion tests

A proposed shared identity object should be deleted or localized if:

- ordinary OAuth, workload identity, Host Task references, and provider IDs
  express the required relation;
- it duplicates token or session state;
- it cannot survive body and model replacement without false continuity;
- it has only one real consumer;
- it adds no recovery, attribution, or consequence reduction;
- it becomes an always-on approval bottleneck.

## Immediate product implications

R1 is a knowledge baseline, not an instruction to mutate World or Security now.
Future product reviews should ask:

1. Does this Tool or browser action inherit ambient authority?
2. Is the grant tied to a Task, resource, action, and lifetime?
3. Are participant, acting Agent, workload, and Tool identities distinguishable?
4. Can an attacker preserve authority through refresh, delegation, or body
   replacement?
5. Is the final world Effect independently verified?
6. Can all residual sessions, tokens, Tools, and bodies be classified?
7. Does a proposed control create more net acceleration than friction?

## R2 route

R2 should study **Web interpretation and semantic differentials**:

```text
HTTP request and response framing
URL, header, and Cookie parsing
proxy, CDN, gateway, framework, and application interpretation
encoding, normalization, and multi-stage decoding
HTML parsing and active-content boundaries
MIME and content sniffing
template, query, command, and serialization interpreters
request smuggling and cache interaction
data, code, instruction, and authority confusion
Agent-driven differential discovery and defensive normalization
```

The central question is:

> When several components interpret the same bytes or structured values, which
> interpretation controls policy, execution, evidence, and recovery?

R2 remains non-operational and standards-led. It may analyze real vulnerability
chains but will not provide exploit payloads or public-target procedures.

## Completion criteria

R1 is complete when:

- origin, site, endpoint, participant, workload, and Agent are distinct;
- authentication, authorization, delegation, intent, and consequence are
  distinct;
- Cookies, CSRF, CORS, OAuth, WebAuthn, and workload identity fit one causal
  authority graph without losing native semantics;
- a strong adaptive Agent attacker is represented;
- model/Host safety behavior is treated as a configuration variable rather than
  proof of lower-layer security;
- product implications remain narrow and deletion-tested;
- R2 has an explicit standards and attack-chain question.

These criteria are satisfied by this study.
