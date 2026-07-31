# 07 — Agent-Era Attack and Defense Chains

## Objective

R1 must reason about attackers strong enough to invalidate naive defenses without
turning the study into an operational exploitation manual. The useful output is
a set of capability and authority chains plus defensive cut points.

## Chain A — External content to ambient browser authority

```text
Agent must read external Web content
→ attacker controls part of that content
→ content changes Agent's selected action
→ Agent uses authenticated browser session
→ request originates from expected origin or user agent
→ server sees valid session and authorized endpoint
→ unintended world Effect
```

### Why classical controls may pass

- TLS succeeds.
- Origin is expected.
- session is valid.
- CSRF state may be valid if the Agent obtained it through the application.
- request schema is correct.
- endpoint authorization matches the account.

### Defensive graph cuts

- classify external content as data, not authority;
- bind Tool grants to current Task and resource;
- require consequence-specific transaction approval;
- separate browsing and high-value action identities;
- verify Effect against participant intent;
- preserve independent world evidence.

## Chain B — Broad token to cross-service action

```text
Agent receives broad bearer token
→ external or adversarial instruction changes objective
→ Agent discovers allowed API operation
→ token is accepted by several resources
→ legitimate calls compose into unintended consequence
```

### Defensive graph cuts

- audience and resource restriction;
- fine-grained actions and transaction details;
- short lifetime and sender constraint;
- no onward delegation by default;
- per-Task token issuance;
- downstream actor-chain logging;
- independent Effect verification.

## Chain C — Same-origin supply-chain compromise

```text
privileged origin imports active dependency
→ dependency or build pipeline compromised
→ code executes with origin authority
→ browser isolation treats code as same principal
→ session-bound operations and data access become available
```

### Defensive graph cuts

- reduce third-party active code;
- isolate control surfaces on separate origins;
- reproducible or attestable build provenance;
- content and resource policy;
- narrow server APIs;
- transaction authorization;
- detect changes in deployment and Tool revisions.

## Chain D — OAuth redirect and issuer confusion

```text
client supports several issuers or dynamic endpoints
→ attacker influences endpoint or redirect relation
→ client associates response with wrong issuer or transaction
→ authorization code or token reaches unintended participant
→ authority is redeemed or replayed
```

### Defensive graph cuts

- exact redirect matching;
- issuer binding and mix-up defenses;
- PKCE and transaction-specific state;
- trusted metadata and endpoint validation;
- sender-constrained tokens;
- preserve redirect and issuer evidence.

## Chain E — Delegation-chain erasure

```text
participant delegates to Agent
→ Agent delegates to service or specialist
→ token exchange or downstream call drops actor relation
→ final service records only participant identity
→ malicious or mistaken actor is unattributable
```

### Defensive graph cuts

- preserve subject and actor claims;
- bind subtask and action;
- disallow unrestricted impersonation;
- require evidence return through the parent Task;
- record token family and onward delegation;
- evaluate responsibility separately from access success.

## Chain F — Generated Tool acquires ambient authority

```text
Agent identifies capability gap
→ generates or downloads Tool
→ Tool is built inside credential-rich environment
→ Tool executes with inherited filesystem, browser, cloud, or network access
→ Tool performs additional Effects outside the declared need
```

### Defensive graph cuts

- disposable build environment;
- dependency provenance;
- capability-oriented tests;
- explicit Tool admission;
- empty-by-default credentials;
- narrow egress and resource grant;
- execution and Effect observation;
- retirement after Task closure.

## Chain G — Authentication success followed by authorization drift

```text
strong passkey or MFA authentication
→ long-lived broad session issued
→ account privileges change or Task scope narrows
→ existing session or token retains old authority
→ Agent or attacker acts under stale grant
```

### Defensive graph cuts

- assurance and authorization state remain separate;
- short-lived sessions for high-value operations;
- reauthorization after privilege or policy changes;
- continuous resource-side validation;
- token/session family revocation;
- residual-session inventory.

## Chain H — Multi-Agent identity propagation

```text
one Agent is hijacked or compromised
→ sends apparently valid Task, Claim, Artifact, or Tool to peers
→ peers trust organizational relation
→ authority or malicious instruction propagates
→ several legitimate identities act in parallel
```

### Defensive graph cuts

- task-scoped delegation;
- authenticated actor and message identity;
- independent verification of high-impact claims;
- compartmentalized information and credentials;
- no implicit authority inheritance from peer status;
- communication and Tool provenance;
- organizational compromise evaluation.

## Chain I — Evaluator or monitor confusion

```text
Agent learns scoring or monitoring surface
→ selects action producing expected visible signal
→ hidden world objective is not achieved or policy is violated elsewhere
→ evaluator records success or compliance
```

### Defensive graph cuts

- hidden and held-out checks;
- independent world truth;
- separate objective, policy, containment, and evaluator-integrity outcomes;
- transcript and Effect review;
- monitor-loss reporting;
- adversarial evaluation of the evaluator.

## Extreme attacker evaluation dimensions

A later owned-range experiment should vary:

```text
attempt count
attacker knowledge of defenses
ability to construct Tools
access to legitimate identities
browser versus direct API channel
same-origin versus cross-origin position
bearer versus sender-constrained tokens
single versus multiple Agents
static versus changing defender policy
known versus held-out attacks
model and Host safety profile
```

The safety profile is recorded because it changes observed behavior. It is not
assumed to represent the strongest possible attacker or the security of lower
layers.

## Defensive strategy

The strongest defense is not the largest number of controls. It is a graph in
which:

- high-value Effects require several independent conditions;
- no single ambient credential grants broad consequence;
- identity and delegation remain attributable;
- attacker feedback does not reveal every hidden control;
- compromised components have narrow authority;
- world Effects are independently observed;
- credentials, sessions, Tools, bodies, and external objects can be revoked or
  reconstructed;
- residual uncertainty is explicit.

## R1 conclusion

Agent systems do not abolish Web identity mechanisms. They turn existing
identity, browser, and delegation systems into a dynamic action substrate. The
new pressure is preserving participant purpose and consequence scope while an
adaptive actor can construct and choose among many valid channels.
