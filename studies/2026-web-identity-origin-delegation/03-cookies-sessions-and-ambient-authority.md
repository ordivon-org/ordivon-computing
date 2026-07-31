# 03 — Cookies, Sessions, and Ambient Authority

## Why Cookies exist

HTTP interactions are largely request/response oriented. Applications need
continuity across requests: authentication, preferences, carts, workflows,
anti-abuse state, and recovery. Cookies let servers store browser-managed state
and maintain sessions.

RFC 10025, published in July 2026 and obsoleting RFC 6265, retains the central
security observation: Cookies have historical security and privacy flaws but
remain widely used. [R08]

## Ambient authority

Cookie-based authentication separates:

```text
designation
  the URL selected for a request

authorization
  the Cookie automatically attached by the user agent
```

RFC 10025 describes this as ambient authority: a remote party may cause a user
agent to issue a request, and the user agent can attach Cookies even when the
remote party does not know their contents. This can let the remote party
exercise authority at an unwary server. [R08]

The attacker does not need to steal the secret to use its effects.

## Session identity is not participant intent

A valid session proves, at most, that the request is associated with a browser
state accepted by the server. It does not prove:

- which page or Agent selected the target;
- which human currently controls the browser;
- that the human understood the action;
- that the action belongs to the original Task;
- that the session has not outlived its intended context;
- that same-origin code remains trustworthy;
- that downstream delegated calls preserve the actor chain.

## Cookie scope dimensions

Cookie behavior depends on attributes and browser rules including:

- host or domain scope;
- path scope;
- Secure transport requirement;
- HttpOnly script access restriction;
- SameSite request context;
- expiration and session lifetime;
- prefixes and related validation rules;
- partitioning and top-level site context where supported.

Each attribute removes or conditions some edges. No single attribute converts a
Cookie into explicit per-action authorization.

## Host scope and sibling risk

Broad domain-scoped Cookies can be sent to multiple subdomains. This supports
large applications but increases the authority inherited by sibling services
and their deployment chains.

```text
registrable domain
+ many independently deployed subdomains
+ broad Cookie scope
→ weakest sibling can influence or receive shared session state
```

Exact behavior depends on Cookie attributes and current standards, but the
architectural lesson is stable: administrative and deployment boundaries should
not be hidden behind one broad credential scope.

## Secure and HttpOnly

- `Secure` restricts Cookie transmission to secure contexts as defined by the
  Cookie specification and user agent; it does not prove the receiving
  application is uncompromised.
- `HttpOnly` prevents access through ordinary script APIs; it does not prevent
  browser attachment to requests and therefore does not eliminate CSRF.

Confidentiality of the secret and misuse of its ambient authority are distinct.

## SameSite

SameSite conditions Cookie attachment on the relationship between the request's
site context and the Cookie's site. It reduces several cross-site request paths,
but:

- same-site is broader than same-origin;
- sibling subdomain compromise can remain relevant;
- navigations and method rules matter;
- legacy and compatibility behavior must be understood;
- same-origin compromise bypasses the cross-site distinction;
- server-side authorization remains necessary.

SameSite is a graph cut, not a complete intent protocol.

## Session lifecycle

A robust session model includes:

```text
issuance
binding to account and authentication event
privilege and assurance level
rotation
idle and absolute expiry
reauthentication for sensitive effects
revocation
logout semantics
multi-device visibility
residual browser and server state
```

Deleting a browser Cookie may not invalidate a server-side session, refresh
token, API token, device grant, or downstream delegated identity.

## Authentication assurance versus session authority

WebAuthn creates scoped public-key credentials and binds ceremonies to an RP ID,
origin validation, and user presence or verification signals. [R09]

This substantially improves authentication and phishing resistance, but a
successful ceremony can still produce an overbroad or long-lived application
session. Strong authentication does not automatically narrow every later
resource and action.

```text
strong authentication
→ confidence in identity proof
≠ explicit approval of every subsequent Effect
```

## Attack chains

### Cross-site ambient action

```text
victim has active session
→ attacker causes browser request to sensitive endpoint
→ browser attaches Cookie under applicable rules
→ server treats session as sufficient authorization
→ state change occurs without current participant intent
```

### Same-origin compromise

```text
XSS or compromised dependency
→ code executes inside trusted origin
→ browser policy allows session-bound APIs
→ attacker performs actions or reads application-visible state
```

SameSite and CSRF tokens are not designed to distinguish trusted from malicious
code within the same origin.

### Residual session after apparent logout

```text
one browser state item removed
→ refresh token, server session, device session, or downstream token remains
→ actor continues through another path
```

Campaign closure requires inventory and invalidation, not only UI state.

### Agent inherits browser session

```text
Agent receives browser-control capability
→ current tab contains authenticated state
→ external data influences action selection
→ browser performs valid session-bound request
→ server cannot distinguish user-selected from hijacker-selected intent
```

## Defensive principles

- Prefer host-only and narrowly scoped Cookies where architecture permits.
- Use Secure, HttpOnly, SameSite, prefix, lifetime, and rotation mechanisms as
  complementary controls.
- Require anti-CSRF or request-context validation for state-changing operations.
- Bind high-consequence actions to explicit transaction data and fresh
  participant confirmation.
- Reauthenticate or increase assurance for privilege transitions.
- Inventory server sessions, refresh tokens, API tokens, delegated tokens, and
  device grants during incident response.
- Distinguish authentication assurance from authorization scope and intent.
- Do not expose high-value browser sessions to general-purpose Agent navigation
  without bounded task and effect controls.

## Ordivon implication

World may observe session class, origin/site context, browser/body revision,
identity provider, expiry, and resulting Effects without storing reusable bearer
secrets. Host owns participant intent and Task linkage. Security evaluates
ambient-authority abuse, session persistence, and residual closure.
