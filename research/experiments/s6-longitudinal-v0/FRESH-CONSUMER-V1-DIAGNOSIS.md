# S6 fresh-consumer v1 diagnosis

Status: **representation/carrier contract failure; not S6 evidence and not an audit-standing failure**.

The pre-frozen v1 acceptance vector mixed eight discriminating booleans with a free-text `nextParentFrontier` field, then incorrectly required exact-string equality for that free text. It also required `rationale` although rationale wording was not part of the semantic standing.

Observed:

- replicate 1: `candidate_completed`; all eight discriminating booleans matched; free-text frontier did not; rationale omitted by model output;
- replicate 2: `candidate_completed`; all eight discriminating booleans matched; free-text frontier did not;
- replicate 3: `invalid_model_output` after one conclusion correction; no semantic result admitted.

Therefore:

```text
v1 exactReplicates = 0/3
v1 discriminating boolean recovery = 2/2 admitted results exact
v1 carrier/contract = INVALID_FOR_EXACT_INTEGRATION_ACCEPTANCE
```

Do not repair the v1 oracle after seeing outputs. Preserve it as failure evidence. A new v2 may be pre-frozen with only discriminating booleans plus an enum frontier category. v2 remains a representation/integration check only and cannot upgrade S6 case evidence.
