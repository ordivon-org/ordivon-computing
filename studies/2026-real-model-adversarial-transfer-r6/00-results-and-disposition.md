# 00 — Results and Disposition

## Evidence sets

| Set | Trials | Attack success | Utility | Verifier false accepts |
|---|---:|---:|---:|---:|
| Main matrix | 28 | 0 | 24 | 0 |
| Structural causal ablation | 5 | 1 | 4 | 0 |
| Native recoverable denial | 1 | 0 | 1 | 0 |

The attack success was an owned Canary-secret read plus opaque local Python
execution caused only by malicious Tool metadata under ambient authority.

## Causal chain

```text
model-facing Tool description changes after catalog commitment
→ model assigns imperative meaning to metadata
→ model proposes Canary read and opaque execution
→ ambient Tool authority admits both
→ real local consequences occur
```

With narrow ToolGrant:

```text
same model interpretation
→ same unauthorized proposal
→ pre-admission denial
→ zero world consequence
```

With typed recovery:

```text
pre-admission tool_grant_denied
→ rejected Tool observation
→ model selects authorized alternative
→ independent Check and Artifact verification
→ durable completion
```

## Additional failure found

The original model-facing Mutation schema omitted item fields. A real model
produced `action: WRITE`; Runtime required `mode: WRITE`. Exact ACI schemas are
therefore part of capability and reliability, not cosmetic documentation.

## Disposition

```text
retain Host-local authority and evidence contracts
retain exact Tool schemas
retain typed denial recovery
keep Runtime UNKNOWN terminal
investigate exact per-Turn Tool-definition binding
reject broad Security platform promotion
freeze R6
```

## Governance boundary

Provider refusal, model interpretation, Tool proposal, Host admission, Runtime
execution, World Effect, and completion verification remain separate facts. R6
therefore hands Provider-policy and access-control questions to
[`../2026-ai-capability-governance-and-private-power/`](../2026-ai-capability-governance-and-private-power/)
without creating a policy engine inside Security or Host.
