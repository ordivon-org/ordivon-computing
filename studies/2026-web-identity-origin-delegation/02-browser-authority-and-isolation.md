# 02 — Browser Authority and Isolation

## The browser is an authority-bearing operating environment

A modern browser does more than render documents. It:

- resolves and fetches remote resources;
- parses several active content formats;
- executes code;
- stores credentials and persistent state;
- mediates user authentication;
- attaches Cookies and client credentials;
- exposes device and application APIs;
- maintains multiple windows, frames, workers, and service workers;
- performs navigations and redirects;
- enforces origin, site, process, and sandbox boundaries.

A browser-driven Agent therefore operates inside an existing authority system.
It does not begin from a neutral HTTP client.

## Same-origin policy is selective, not absolute isolation

The Web must permit useful cross-origin interactions. Different mechanisms have
different policies:

```text
cross-origin navigation
  broadly allowed

cross-origin form submission or embedded resource request
  often allowed to send

cross-origin response reading from script
  generally restricted unless allowed through CORS or another mechanism

cross-origin window communication
  possible through constrained APIs such as postMessage

cross-origin embedding
  possible subject to response and document policies
```

Therefore, this inference is false:

```text
script cannot read the response
→ script cannot cause a credentialed or state-changing request
```

The distinction between **send authority** and **read authority** is foundational
for CSRF and several browser confused-deputy failures.

## Browser principal graph

One visible tab can contain:

```text
top-level origin
├─ same-origin frames
├─ cross-origin frames
├─ workers and service workers
├─ opener or opened windows
├─ extension content scripts
├─ browser-managed credentials
└─ network requests with varying destinations and modes
```

The top-level site, initiating origin, frame origin, worker origin, process,
extension identity, and authenticated server session can all differ.

## Process isolation

Chromium Site Isolation places cross-site documents into separate sandboxed
renderer processes and allows the browser process to restrict which cross-site
data a renderer receives. It is intended as defense in depth against renderer
compromise, universal cross-site scripting, and speculative side channels. [R05]

Chromium also explicitly states that Site Isolation does not mitigate ordinary
XSS, CSRF, clickjacking, or attacks occurring inside the victim site's own page.
[R06]

This preserves the layer distinction:

```text
same-origin policy
  semantic Web access control

site isolation
  process and data-delivery defense in depth

renderer sandbox
  operating-system consequence reduction

server authorization
  resource and action admission
```

None replaces the others.

## Browser process as independent enforcer

A fully compromised renderer should not automatically receive every cross-site
response, Cookie, device, or browser privilege. Browser-process checks and
process placement can reduce the value of renderer compromise. [R05]

This suggests a general Agent-security principle:

> The component selecting actions should not be the sole enforcer or observer of
> the boundary those actions cross.

For Ordivon, the model or Agent process corresponds more closely to an
untrusted renderer than to the browser process.

## Sandboxed and opaque contexts

Sandboxing can remove or alter origin, navigation, script, form, popup, and other
capabilities. However, combining exceptions can restore significant authority.
The correct analysis is not `sandboxed = safe`, but:

```text
which exact capabilities remain
which context owns them
which other contexts can communicate
which server-side identity is attached
which actions can create durable world effects
```

## Cross-origin communication

Explicit communication APIs are required for legitimate composition. Their
security depends on both endpoint selection and message validation.

Common failure pattern:

```text
broad receiver
+ weak sender-origin validation
+ attacker-controlled message content
+ privileged receiver action
→ cross-origin confused deputy
```

OAuth Security BCP requires strict verification of initiator and receiver when
browser communication mechanisms replace normal redirect flows. [R04]

## Extensions and browser Agents

Extensions, automation layers, accessibility APIs, and browser Agents may have
privileges unavailable to ordinary page script. They can also blur user-action
signals:

- a page click;
- a script-triggered navigation;
- an extension action;
- an Agent-selected action;
- an address-bar or bookmark navigation;
- a human-confirmed action.

Fetch Metadata recognizes this ambiguity and discusses how extension-initiated
requests should be represented so they do not silently bypass server-side
request-context policies. [R07]

## Attack-chain examples

### Compromised renderer

```text
renderer vulnerability
→ code execution inside one renderer
→ attempts to read cross-site state
→ Site Isolation and browser-process filtering limit delivered data
→ attacker searches same-site, same-origin, extension, or server-side paths
```

Defense in depth changes the path and cost; it does not guarantee Campaign
closure.

### Agent inside authenticated browser

```text
external content influences Agent
→ Agent selects navigation or Tool action
→ browser attaches valid session or presents authentication UI
→ server authorizes the request
→ user did not choose the concrete consequence
```

Every browser and server mechanism may behave according to specification while
the intent chain fails.

### Compromised same-origin application

```text
supply-chain or XSS entry
→ active content gains origin authority
→ process isolation does not separate it from victim same-origin data
→ valid session and APIs are used
```

Origin is intentionally coarse. The defense must include code integrity,
least-privilege APIs, consequence binding, and post-action evidence.

## Defensive architecture

- Keep high-value control interfaces on separate origins and, where feasible,
  separate sites and processes.
- Minimize active third-party code inside privileged origins.
- Validate cross-origin message sender, receiver, type, schema, and transaction.
- Treat browser UI and user activation as evidence with defined limitations, not
  universal proof of intent.
- Use server-side authorization for every action regardless of browser policy.
- Bind high-consequence operations to resource, action, transaction, freshness,
  and participant confirmation.
- Preserve the browser context graph in evaluation traces.
- Model extension and Agent actions separately from page actions.

## Ordivon implication

World observations should be able to condition browser Effects on:

```text
top-level origin and site
initiating frame or worker
active session or credential class
redirect and navigation chain
browser/extension/Agent actor
Tool and browser revision
resulting external object or state change
```

Security should infer attack or deception only above those facts.
