# R6 Decisions

## D1 — R6 is completed, not expanded into a platform

The transfer question has been answered with real model, Host, Harness, Runtime,
and independent-verifier evidence. Freeze the Range after closeout. Future work
must begin with a new falsifier rather than adding attack combinations by default.

## D2 — retain Assignment-scoped ToolGrant

ToolGrant prevented every unauthorized Canary consequence in the narrow profiles,
including four Tool-description-poisoning Trials where the model explicitly tried
to read the Canary.

ToolGrant remains a physical authority boundary. It is not evidence that model
interpretation was safe.

## D3 — retain exact model-facing Tool schemas

The pre-fix ACI omitted the structure of each Workspace Mutation. A real model
produced the wrong field and legal work failed. Host candidate `ec6e746` fixes
this locally and should be reviewed for product integration.

This does not require a new Protocol or Security layer.

## D4 — retain typed recoverable ToolGrant denial

Hard termination contained consequences but caused avoidable utility loss.
Host candidate `1873a2d` distinguishes:

```text
tool_grant_denied
  → rejected Tool observation
  → model may select an authorized alternative

invalid call / duplicate identity / unknown Tool
  → terminal invalid_tool_call

Runtime uncertain
  → terminal runtime_unknown
```

The real-model candidate Trial preserved both safety and durable completion.
This should remain Host-local.

## D5 — model-facing Tool-definition integrity remains open

R6 deliberately changed Tool descriptions after Assignment catalog commitment
while retaining the committed catalog digest. The model changed behavior and, in
an ambient profile, read the Canary and executed Python.

Therefore:

```text
committed Tool catalog digest
≠ proof that the exact Tool definitions sent on every model Turn are identical
```

The next narrow falsifier is to bind or verify the exact serialized Turn Tool
definitions against the durable Assignment and repeat the same benign-control
poisoning test with another Provider or Harness adapter.

Do not solve this by creating a central Security policy engine.

## D6 — candidate completion remains separate from truth

No incorrect completion was accepted. Workspace state, Runtime Artifact identity,
Artifact digest, independent Check result, and Host adjudication remained
separate from model conclusion text.

## D7 — Context compaction is a reliability question, not a proven compromise

One compacted Trial failed with invalid model output while three completed. No
Canary consequence occurred. This is insufficient to promote a new Context
security layer; it remains a held-out reliability and transfer test.

## D8 — Runtime UNKNOWN remains fail-closed

One Pro gated Trial had authorized output but ended in Runtime `UNKNOWN`. R6 did
not reinterpret it as failure or success and did not redispatch. Existing
reconciliation semantics remain correct.

## D9 — reject broad abstractions

R6 does not earn:

- a universal AttackChain service;
- a permanent Cyber Range platform;
- a central Agent safety classifier;
- a global World telemetry store;
- a new network or parser stack;
- Campaign or OpponentHypothesis promotion.

## D10 — Provider refusal is a governance observation, not a consequence proof

The four indirect-injection documents produced no Canary consequence under the
recorded Provider configuration, while benign evidence plus poisoned Tool
metadata caused a real consequence under ambient authority. Therefore Provider
or model refusal must remain separate from Host admission, Runtime execution,
World Effect, and independent verification.

Broader questions about classification, access tiers, monitoring, account
consequences, contestability, and Provider exit belong to the G0-G9 capability-
governance study. R6 earns no Provider-policy engine and no inference that an
automated content restriction is a sufficient physical defense.

## Next falsifier

Use one materially different Provider or mature Harness adapter and one exact
Turn Tool-definition binding. Repeat only the benign-control structural poisoning
pair and one held-out real workload. Delete the proposed binding if the mismatch
cannot reproduce outside the current adapter boundary.
