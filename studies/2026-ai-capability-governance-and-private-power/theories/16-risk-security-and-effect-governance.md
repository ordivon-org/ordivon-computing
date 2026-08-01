# Risk, Security, and Effect-Level Governance

## Risk as a socio-technical object

Risk management identifies context, hazards, affected actors, likelihood,
severity, controls, uncertainty, and residual risk. It does not by itself decide
whose values dominate or who bears the cost. NIST's AI RMF is useful as an
operational baseline, while this study adds power, distribution, contestability,
and exit.

## Control-placement question

AI governance can intervene at multiple layers:

```text
training data
model behavior
request / response classifier
identity and access tier
Tool catalog
ToolGrant and resource scope
Runtime admission
Effect identity and idempotency
World verification
account and organization enforcement
```

The research question is not “guards or no guards,” but which layer reduces the
specified harm with the least unnecessary capability loss and acceptable
residual risk.

## Effect-level hypothesis

For agentic systems, a strong candidate architecture is:

```text
rich cognition and controlled simulation
+ explicit authority and provenance
+ narrow Tool and resource grants
+ stable Effect identity
+ UNKNOWN and reconcile-before-redispatch
+ independent consequence verification
```

This allows the model to fail cognitively while bounding external consequence.
It does not solve harms caused by information disclosure, persuasion, or knowledge
itself.

## Defense evidence

A defense claim should name:

- the threatened outcome;
- the graph edge cut;
- authorized utility retained;
- bypass and adaptation evidence;
- recovery and residual state;
- evaluator integrity;
- distributional and privacy cost.

Provider refusal is only one possible graph cut.

## What this theory explains

- precise control placement;
- why content refusal and Effect prevention are different;
- how to compare authorized utility and harm reduction;
- why recovery and residual proof matter after intervention.

## What it does not establish

- the legitimacy of the institution choosing the control;
- whether cognition itself creates unacceptable externality;
- whether a risk estimate is politically neutral;
- how infrastructure concentration affects governance.

## Testable implications

1. In owned Canary worlds, narrow ToolGrant and independent verification should
   prevent unauthorized Effects after model-level susceptibility.
2. Content controls may reduce proposal frequency but need not establish lower-
   layer safety.
3. Some information hazards will survive Effect isolation and justify additional
   capability restrictions.
4. Layer-separated evidence produces different architecture decisions from one
   binary “safe/unsafe” label.

## Falsifiers

- model cognition repeatedly produces severe harm without actionable Effect paths;
- narrow authority controls cannot contain adaptive models at acceptable cost;
- binary Provider refusal labels are as causally informative as full layer traces.

## Primary references

[G014], [G017], [G019], [G020], [G022], and [G024].
