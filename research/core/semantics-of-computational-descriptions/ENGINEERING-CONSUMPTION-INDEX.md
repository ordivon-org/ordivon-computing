# SCD Engineering Consumption Index

Status: **owner-specific engineering-consumption boundary**.

Semantics of Computational Descriptions (SCD) owns abstract semantic claims about computational descriptions. Engineering may consume those claims when it asserts that a representation, schema, protocol, transformation, migration, normalization, abstraction, compatibility relation, refinement, or transport **preserves or changes meaning**.

This index does not make SCD a runtime service, protocol registry, compiler, theorem engine, or product authority.

## Current engineering consumers

### Versioned protocol / Tool-contract evolution

A schema hash, version label, parser success, field superset, or normalized structural diff can establish structural facts. It does **not** by itself establish semantic equivalence, substitutability, refinement, or preservation.

Engineering claims such as:

```text
old contract ≡ new contract
new contract refines old contract
migration preserves accepted meaning
normalization is semantics-preserving
```

must declare the relevant SCD relation and scope or remain narrower structural/product claims.

Current `ordivon-protocol` remains authority for the exact contracts it publishes and consumers actually use. SCD constrains overclaims about their semantics; it does not replace product compatibility tests.

### Tool-contract drift and Binding

A Tool snapshot/revision/digest identifies an executable contract state. Detecting a changed normalized contract is useful currentness evidence, but semantic drift is a separate claim. Two byte-different contracts may be semantically equivalent for one obligation; byte-identical or schema-compatible representations can still change meaning through external interpretation or dependency changes.

Therefore:

```text
contract identity != semantic equivalence
structural compatibility != semantic preservation
current executable availability != semantic substitutability
```

### Representation and intermediate forms

IRs, JSON documents, prompts, manifests, generated schemas and model-visible representations may serve as computational descriptions. Engineering may use SCD when comparing their admissibility, abstraction, composition, property satisfaction or preservation under transformation.

Do not promote every representation into a shared SCD object model. Local representations remain local until a repeated consumer needs the same semantic relation.

### Static checks and conformance

A checker establishes only the property encoded by the checker. Structural validity, conformance, type checking or successful compilation does not imply complete behavioral/semantic equivalence.

Where a release or migration decision depends on semantic preservation, the required property and equivalence/refinement scope must be explicit.

## Current non-admissions

No current evidence admits:

- a global SemanticCompatibilityService;
- one universal Description schema;
- an SCD registry of all programs/tools/contracts;
- automatic semantic-equivalence inference from Git/schema/version identity;
- moving Runtime realization/evidence truth into SCD;
- moving Harness orchestration into SCD.

## Reopen engineering scope

Add a stronger SCD engineering surface only when a real consumer repeatedly cannot decide a semantics-sensitive migration/compatibility/refinement/property question using owner-local code/tests plus the current source-fenced SCD relation.
