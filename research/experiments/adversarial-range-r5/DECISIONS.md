# R5 Decisions

## D1 — retain the range as research-only

The implementation stays under `research/experiments/`. It is not a production
Security, Game, Host, Runtime, or World component.

## D2 — reuse existing ownership

R5 found no need for a new permanent layer:

```text
Host
  provenance, compiled candidates, ToolGrant, Effect admission, UNKNOWN,
  reconciliation, completion

Game / experiment-local World
  hidden truth, deterministic consequences, seeds, reset

Runtime
  future executable bodies and Artifacts

Security
  future adaptive interpretation and Campaign scoring
```

## D3 — safety policy remains a configuration variable

Synthetic safety reduced measured attack success but did not eliminate it. R5
therefore records refusal separately from Host admission and World effect.

## D4 — retain provider-native idempotency as a strong baseline

Provider idempotency solved the response-loss case with fewer Host semantics than
a general transaction system. Host `UNKNOWN + reconcile` remains necessary where
provider support is absent or the current outcome is not directly returned.

## D5 — prefer strict rejection or typed reserialization

A universal normalizer is rejected. The experiment retains two local strategies:

- reject ambiguous representation;
- parse into one typed object, apply policy to it, then reserialize for the next
  boundary.

## D6 — do not promote AttackChain

The study-local and Trial-local graphs were sufficient. No shared `AttackChain`,
`Campaign`, or `OpponentHypothesis` protocol object is admitted by R5.

## D7 — R6 is a transfer test, not a larger platform build

R6 should replace synthetic model policies with real model/Host profiles and
held-out attacks while reusing this result envelope where useful. If the envelope
adds no value over Host/Game native receipts, it should be deleted or localized.
