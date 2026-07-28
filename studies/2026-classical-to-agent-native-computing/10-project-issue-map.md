# Cross-Project Issue Map

## 1. Routing rule

Research synthesis belongs in Ordivon Computing. Executable questions belong in the repository that owns the mechanism, data, or decision required to answer them.

For cross-project requests:

```text
Project A needs capability from Project B
→ implementation or compatibility Issue is filed in Project B
→ Project A records the dependency or experiment locally
→ Computing records the cross-project research relation
```

This prevents the requesting project from silently creating a shadow implementation of another project's responsibility.

The research source is Ordivon Computing PR #55. The comparative program is coordinated by Computing #56.

## 2. Issue classes

- **RESEARCH** — compare a hypothesis with a strong baseline; implementation is optional until the result justifies it.
- **P0/P1 implementation** — a bounded mechanism or compatibility surface required by a current experiment or product path.
- **M5-R/P1-R domain experiment** — a domain laboratory tests a cross-cutting claim without becoming the generic implementation owner.
- **publication** — public taxonomy and status must reflect actual responsibility and evidence.

## 3. Created issue set

| Repository | Issue | Responsibility or question |
|---|---|---|
| `ordivon-computing` | #56 — adversarially validate Ordivon against strongest external baselines | coordinate E1–E7, preserve baselines, data, negative results, and deletion decisions |
| `ordivon-host` | #5 — compare open-work continuity with LangGraph and Temporal | test whether R2 is distinct from ordinary workflow state |
| `ordivon-host` | #6 — bind Context provenance, trust, and invalidation to each invocation | implement the minimum E3 observation and invalidation boundary |
| `ordivon-host` | #7 — implement evidence-rich DecisionRequest and measure attention | test R1 as a product responsibility before Protocol promotion |
| `ordivon-runtime` | #56 — compare Effect commitment with plain MCP Tools and durable Activities | test whether R6 adds value beyond existing Tool/Activity mechanisms |
| `ordivon-runtime` | #57 — add a contained execution profile beside trusted-local mode | preserve the personal high-authority profile without generalizing it |
| `ordivon-runtime` | #58 — migrate MCP adapter to the 2026 stateless core | retire legacy Core Tasks while preserving Runtime Job truth |
| `ordivon-edge` | #24 — expose a Host-consumable Fetch/Browser Effect backend | provide the second real Effect backend requested by Host and Computing |
| `ordivon-link` | #18 — expose versioned network observations as Host Context sources | provide network evidence without moving Context ownership into Link |
| `ordivon-game` | #40 — run equal-budget single-Agent and multi-Agent ablations | test R4 without confusing architecture benefit with additional compute |
| `ordivon-security` | #10 — build Context-poisoning and Tool-output injection campaigns | adversarially test R3, R5, containment, and trust escalation |
| `ordivon-web` | #25 — publish the substrate/overlay project taxonomy | remove obsolete single-stack and parallel-product implications |

## 4. Cross-project compatibility ownership

The following routes apply the provider-owns-the-request rule:

### Game requires Host capabilities

- Host #4 owns the minimum Game workload and multi-Actor Host extension requirements.
- Game #39 owns convergence of the embedded Game Host toward one logical Ordivon Host.
- Game #40 owns the domain evaluation, not the generic Host implementation.

### Host requires an external Effect backend

- Edge #24 owns the structured Fetch/Browser ToolContract, Receipt, Artifact, and reconciliation surface.
- Runtime #56 consumes this as the second backend in the Effect-commitment comparison.

### Host requires network evidence

- Link #18 owns versioned, expiring, secret-free network Observations.
- Host #6 owns selection, trust, and invalidation when those Observations enter Context.

### Security requires containment and world bodies

- Runtime #57 owns the contained local execution profile.
- Edge #21 owns the persistent network-attached adversarial body design.
- Link #13 owns the persistent range data plane and attachment.
- Security #10 owns the poisoning campaign and evaluation result.
- Computing `ANC-SECURITY-002` owns comparison with mature substrates and evaluation science.

### Finance requires generic execution comparison

- Finance #525 owns capital-domain authority, broker identity, Receipt, reconciliation, and accepted capital truth.
- Finance #526 owns the comparison and migration decision.
- Any missing generic Host or Runtime mechanism must be requested in that provider repository rather than implemented as new generic infrastructure in Finance.

## 5. Complementary Agent-world and evaluation issues

`ANC-SECURITY-002` produced a second, non-duplicative issue graph focused on mature execution/network substrates and statistically valid Agent evaluation:

| Repository | Issue | Owned correction or experiment |
|---|---|---|
| `ordivon-computing` | #57 — align Agent world, body, evaluation, and evidence | comparative owner for the Link/Edge/Security hypothesis set |
| `ordivon-edge` | #25 — separate Agent presence, Sandbox, and Execution identity/lifecycle | correct the overloaded Edge Node identity before persistent providers |
| `ordivon-link` | #19 — define a CNI-compatible NetworkAttachment evidence contract | add Agent-specific identity/evidence above mature network backends |
| `ordivon-security` | #11 — replace uniform component verbs with Campaign phases/native plans | stop Security from overriding component-native lifecycles |
| `ordivon-security` | #12 — separate reconstruction equivalence and outcome dimensions | distinguish run validity, closure, objective, containment, and evidence quality |
| `ordivon-security` | #13 — repeated evaluation, hidden scoring, and cheating review | establish trial families, uncertainty, controls, and grader-gaming review |
| `ordivon-host` | #8 — expose a Security-compatible Agent/Goal/Task/Attempt binding | let Security identify evaluated cognition without copying Host truth |
| `ordivon-runtime` | #59 — expose supervisor Job binding and process residual evidence | provide execution/terminal evidence without acquiring Edge or Campaign semantics |
| `ordivon-security` | #14 — run the first single evaluated Agent Campaign | learn evaluation semantics before adaptive Red/Blue and before custom P0-D completion |

This graph follows the same routing rule: each compatibility requirement is located in the repository that must supply it.

## 6. Existing issues reused rather than duplicated

The following Issues already owned related work and were reused:

- Computing #1 — Agent-native construction program;
- Computing #8 — multi-Agent branch, Join, and Artifact coordination;
- Computing #9 — evaluation, replay, and data flywheel;
- Computing #10 — Goal workspace and organization interface;
- Computing #44 — personal-developer reliability and low friction;
- Computing #46 — adversarial Agent systems program;
- Host #2 — operator handoff capsule;
- Host #4 — Game-requested Host compatibility investigation;
- Edge #21 — persistent network-attached adversarial Node;
- Link #13 — persistent range data plane and Edge attachment;
- Game #7 — M5 replay, evaluation, and first playable receipt;
- Game #39 — Game-side Host convergence;
- Security #4 — adaptive Red/Blue maximum-elicitation campaign.

No duplicate Host/Game convergence Issue was created.

## 7. Closure discipline

An Issue is not closed because prose, a type, or a successful demonstration exists. Closure requires the evidence stated in its acceptance criteria. A research Issue may close with a negative result when:

- the baseline matches or outperforms Ordivon;
- the proposed abstraction is reduced to local policy or metadata;
- the mechanism is removed or explicitly deferred;
- the resulting data and decision are preserved in Computing.

Issue state remains in GitHub. This chapter preserves responsibility routing and the initial experiment graph.
