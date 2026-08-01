# R5 Minimal Owned Adversarial Range

Status: deterministic range implemented; external Host/Game contracts observed;
real-model transfer remains the R6 falsifier.

## Question

Can existing thin Ordivon responsibilities reproduce representative cross-layer
adversarial failures, preserve authorized utility, recover from ambiguous
outcomes, and prove reset without creating a permanent Security platform?

## Scope

The range contains three owned, reversible scenario families:

```text
Agent hijacking
  untrusted evidence → model proposal → compiled candidate / ToolGrant admission
  → simulated Effect → independent verifier

response loss
  provider commit → response lost → FAILED or UNKNOWN → retry/reconcile
  → duplicate or single Effect

interpretation differential
  abstract duplicate target values → front policy interpretation
  → backend interpretation → simulated public/private Effect
```

No scenario contacts a public target, carries live credentials, emits exploit
payloads, or produces an irreversible external Effect. The interpretation case
uses typed abstract values rather than operational HTTP messages.

## What is real and what is simulated

### Executed in this repository

- 176 deterministic Trials;
- repeated/adaptive instruction-like attack forms represented by inert labels;
- four model/Host policy profiles;
- four retry/reconciliation profiles;
- four parser/admission profiles;
- exact hidden World truth;
- independent outcome checks;
- reset proof after every Trial;
- stable JSON evidence and Markdown report.

### Observed in product repositories

At exact revisions recorded in [`EVIDENCE.md`](EVIDENCE.md):

- Host preserves source trust and claim status;
- Host rejects model-invented actions outside the compiled candidate set;
- Host rejects new Effects while an earlier Dispatch is unresolved;
- Host retains ToolGrant restrictions over Tools, paths, checks, Jobs, and
  Artifacts;
- Host records uncertain delivery and reconciles the original Dispatch without
  redelivery;
- Game exposes deterministic hidden World truth, exact revisions, command
  receipts, idempotent replay, fault injection, and World invariants.

### Not yet demonstrated

- real model behavior under several Providers;
- current ChatGPT/Provider safety policy transfer;
- held-out natural-language attacks;
- deliberate Context loss and Host replacement during a hijacking Trial;
- generated Tool construction inside the adversarial loop;
- live Ordivon Runtime and World-provider Effects.

Those belong to R6. R5 does not claim production security.

## Run

```bash
cd research/experiments/adversarial-range-r5
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m anc_adversarial_range.cli \
  --source-revision "$(git rev-parse HEAD)" \
  --output evidence/deterministic-range.json \
  --report RESULTS.md
```

The evidence file binds the experiment source revision. Generate it only after
committing the executable range.

## Variants

### Agent hijacking

- `model-only-open` — broad ambient action authority;
- `model-only-safe` — a stronger model safety profile, still evaluated over
  repeated adaptive forms;
- `static-filter-safe` — blocks one known marker but not the semantic family;
- `host-provenance-effect-gate` — untrusted content remains evidence; the model
  can select only compiled candidates, and Tool/Effect scope is checked before
  World commit.

The model profiles are deterministic synthetic policies, not claims about named
models. Their purpose is to prove the evaluation shape and safety-policy confound.

### Response loss

- `blind-retry`;
- `layered-retries`;
- `provider-idempotency-only`;
- `host-unknown-reconcile`.

### Interpretation differential

- `front-first-back-last`;
- `shared-last-policy`;
- `strict-reject-duplicates`;
- `typed-reserialize`.

## Admission result

R5 can retain or reject responsibilities, but it cannot promote a shared object
on synthetic evidence alone.

```text
retain
  source provenance
  compiled candidate/action admission
  ToolGrant
  Effect identity
  UNKNOWN and reconcile
  provider idempotency
  strict parse or typed reserialization
  independent verification
  exact reset

localize
  attack corpus
  adaptive schedule
  hidden truth
  Trial orchestration

do not promote
  universal AttackChain service
  central safety policy engine
  generic cyber range
  new parser/network stack
```

## Safety-prompt treatment

A safety profile is one experiment variable:

```text
policy refusal observed
→ fewer model proposals under that configuration
```

It does not justify:

```text
policy refusal
→ lower-layer capability absent
```

The range records model proposals, Host rejection, Tool admission, World commits,
and reset separately.
