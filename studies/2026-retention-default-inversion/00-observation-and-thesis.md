# Observation and thesis

## 1. Triggering trajectory

The Station Zero review began as a source-level audit of correctness, ownership, concurrency, evidence, recovery, and product behavior. It found and repaired real failures. It also missed a more basic problem: the audit treated existing constraints as presumptively legitimate.

The failure became visible when the R1 product-loop change had semantic tests, type checks, browser execution, exact World-Tick verification, and a materially lower player-interaction count, yet the default gate still failed because global branch coverage was just below a fixed percentage. Additional tests began to be written for the metric rather than for a newly identified failure.

A broader review then found the same pattern in:

- historical milestone receipts executed in current CI;
- old evaluations tested against their own historical revisions;
- compatibility paths kept active for possible future comparison;
- release checks run at ordinary pull-request frequency;
- exact product wording treated as a stable contract;
- zero-dependency and fixed-version choices promoted into permanent acceptance criteria;
- deletion requiring migration, replacement, equal-budget comparison, retained compatibility evidence, and rollback, while retention required only historical existence or hypothetical future use.

The audit was strict about whether existing rules were implemented correctly. It was insufficiently strict about whether those rules still deserved to exist.

## 2. The previous hidden assumption

The previous practical default was:

```text
structure already exists
→ infer that it once had a reason
→ preserve it while uncertainty remains
→ require the deleting party to prove no current or future value
```

This creates asymmetric evidence burdens. Every added structure acquires path-dependent protection. Tests, documentation, compatibility consumers, and release rules then accumulate around it, making later deletion appear increasingly expensive. The structure manufactures evidence for its own permanence.

This is especially dangerous when implementation and reconstruction become cheaper while attention, comprehension, creative energy, and external consequence remain scarce.

## 3. The inversion

The corrected default is:

```text
existing or proposed persistent structure
→ place outside the active system by default
→ ask whether a current capability or protected failure rescues it
→ retain only the narrowest form with positive recurring net value
→ otherwise localize, archive, or delete
```

The burden of proof therefore moves:

```text
old default
retention is implicit
removal is prosecuted

new default
removal from the active path is implicit
retention is audited
```

This does not mean every audit begins by physically deleting files before inspection. It means the decision model grants no evidentiary weight to existence alone.

## 4. Active removal is not historical destruction

Four actions must remain distinct:

1. **remove from the active path** — stop loading, building, serving, testing, or requiring the structure by default;
2. **archive** — preserve history, evidence, or a reproducible reference outside current execution and default Context;
3. **delete the current implementation** — remove source that no longer serves a current responsibility while Git retains recoverability;
4. **destroy unique evidence or externally governed data** — a separate consequence-bearing action that requires the relevant authority and retention obligations.

Ordivon adopts the first three aggressively when value is unproven. It does not use this principle to erase participant-owned data, legal records, third-party rights, unique evidence, or difficult-to-reconstruct external state without the appropriate domain decision.

## 5. Why the inversion follows from the scarcity shift

When implementation was expensive and reconstruction slow, preserving working structure often protected scarce labor. Agent-assisted generation, repository inspection, disposable Workspaces, exact source history, and rapid testing reduce part of that scarcity.

The relative cost increasingly moves toward:

- understanding an oversized active system;
- maintaining compatibility with inactive paths;
- waiting for broad gates unrelated to the current change;
- carrying obsolete assumptions into model Context;
- allowing historical process to displace product judgment;
- spending finite attention proving that cheap implementation should remain protected.

A retained structure is therefore not free. It is a recurring commitment of attention and future design space.

## 6. Scope

The inversion applies most strongly to persistent active structures:

- code modules and shared abstractions;
- tests and CI gates;
- APIs and compatibility surfaces;
- schemas, versions, policies, and protocol objects;
- release processes and evidence machinery;
- current documentation and default Agent Context;
- portfolios, governance mechanisms, and organizational procedures.

Creative content uses a different admission test. A character, place, activity, visual composition, ritual, or story may be retained because it is affecting, expressive, memorable, playful, or worth revisiting. The rule attacks accidental permanent infrastructure, not abundance in reversible creative space.

## 7. Thesis

> A persistent structure has no active legitimacy merely because it exists, once worked, is tested, is documented, or may be useful later. Continued active retention must identify a current consumer, a concrete capability or protected failure, the insufficiency of narrower alternatives, recurring net benefit, and a review horizon. Uncertainty favors reversible removal or archive rather than indefinite compatibility.
