from __future__ import annotations

import hashlib
import json
import random
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

UNKNOWN = "<unknown>"


@dataclass(frozen=True)
class LawResult:
    law_id: str
    title: str
    trials: int
    hazard_trials: int
    naive_errors: int
    guarded_errors: int
    benign_trials: int
    naive_benign_successes: int
    guarded_benign_successes: int
    abstentions: int
    counterexample: dict[str, Any]

    @property
    def naive_hazard_error_rate(self) -> float:
        return self.naive_errors / self.hazard_trials if self.hazard_trials else 0.0

    @property
    def guarded_hazard_error_rate(self) -> float:
        return self.guarded_errors / self.hazard_trials if self.hazard_trials else 0.0

    @property
    def guarded_benign_success_rate(self) -> float:
        return self.guarded_benign_successes / self.benign_trials if self.benign_trials else 0.0

    def payload(self) -> dict[str, Any]:
        data = asdict(self)
        data.update(
            {
                "naiveHazardErrorRate": self.naive_hazard_error_rate,
                "guardedHazardErrorRate": self.guarded_hazard_error_rate,
                "guardedBenignSuccessRate": self.guarded_benign_success_rate,
            }
        )
        return data


def _first(existing: dict[str, Any] | None, candidate: dict[str, Any]) -> dict[str, Any]:
    return existing if existing is not None else candidate


def run_l1(trials: int, seed: int) -> LawResult:
    """L1: a selected representation is not the represented reality.

    The representation deliberately exposes only a declared subset of fields. The
    violating consumer treats an omitted boolean as False. The guarded consumer
    preserves omission as UNKNOWN. No temporal change is involved; this isolates
    representation/reality separation from freshness.
    """

    rng = random.Random(seed)
    hazard = naive_errors = guarded_errors = 0
    benign = naive_benign = guarded_benign = abstentions = 0
    counterexample: dict[str, Any] | None = None

    for index in range(trials):
        latent_compromised = bool(rng.getrandbits(1))
        expose_latent = rng.random() < 0.55
        representation: dict[str, Any] = {"service": "ready"}
        if expose_latent:
            representation["latent_compromised"] = latent_compromised

        naive_claim_safe = not bool(representation.get("latent_compromised", False))
        guarded_value = representation.get("latent_compromised", UNKNOWN)
        guarded_claim_safe = None if guarded_value == UNKNOWN else not bool(guarded_value)

        distinction_matters = (not expose_latent) and latent_compromised
        if distinction_matters:
            hazard += 1
            if naive_claim_safe:
                naive_errors += 1
            if guarded_claim_safe is True:
                guarded_errors += 1
            if guarded_claim_safe is None:
                abstentions += 1
            counterexample = _first(
                counterexample,
                {
                    "trial": index,
                    "reality": {"latent_compromised": True},
                    "representation": representation,
                    "naiveConclusion": "safe",
                    "guardedConclusion": "unknown",
                    "failure": "omitted reality was collapsed into False",
                },
            )
        else:
            benign += 1
            actual_safe = not latent_compromised
            if naive_claim_safe == actual_safe:
                naive_benign += 1
            if guarded_claim_safe is None:
                abstentions += 1
            elif guarded_claim_safe == actual_safe:
                guarded_benign += 1

    assert counterexample is not None
    return LawResult(
        "L1",
        "Reality–Representation Separation",
        trials,
        hazard,
        naive_errors,
        guarded_errors,
        benign,
        naive_benign,
        guarded_benign,
        abstentions,
        counterexample,
    )


def run_l2(trials: int, seed: int) -> LawResult:
    """L2: evidence/claims are usable only under their binding.

    A payload can remain identical while its entity/revision binding changes. The
    violating consumer reuses the old evidence from payload equality alone. The
    guarded consumer requires the exact entity + revision binding before deciding.
    """

    rng = random.Random(seed)
    hazard = naive_errors = guarded_errors = 0
    benign = naive_benign = guarded_benign = abstentions = 0
    counterexample: dict[str, Any] | None = None

    for index in range(trials):
        evidence_entity = rng.choice(("runtime", "finance", "world"))
        evidence_revision = rng.randrange(1, 6)
        evidence_value = bool(rng.getrandbits(1))
        binding_matches = rng.random() < 0.55
        if binding_matches:
            current_entity = evidence_entity
            current_revision = evidence_revision
            actual_value = evidence_value
        else:
            if rng.random() < 0.5:
                current_entity = rng.choice([x for x in ("runtime", "finance", "world") if x != evidence_entity])
                current_revision = evidence_revision
            else:
                current_entity = evidence_entity
                current_revision = evidence_revision + 1
            actual_value = bool(rng.getrandbits(1))

        naive_value = evidence_value
        guarded_value = evidence_value if (
            current_entity == evidence_entity and current_revision == evidence_revision
        ) else None

        distinction_matters = (not binding_matches) and naive_value != actual_value
        if distinction_matters:
            hazard += 1
            naive_errors += 1
            if guarded_value is not None and guarded_value != actual_value:
                guarded_errors += 1
            if guarded_value is None:
                abstentions += 1
            counterexample = _first(
                counterexample,
                {
                    "trial": index,
                    "evidenceBinding": [evidence_entity, evidence_revision],
                    "currentBinding": [current_entity, current_revision],
                    "evidenceValue": evidence_value,
                    "currentReality": actual_value,
                    "naiveConclusion": evidence_value,
                    "guardedConclusion": "revalidate",
                    "failure": "historical/foreign evidence was promoted outside its binding",
                },
            )
        else:
            benign += 1
            if naive_value == actual_value:
                naive_benign += 1
            if guarded_value is None:
                abstentions += 1
            elif guarded_value == actual_value:
                guarded_benign += 1

    assert counterexample is not None
    return LawResult(
        "L2",
        "Binding Law",
        trials,
        hazard,
        naive_errors,
        guarded_errors,
        benign,
        naive_benign,
        guarded_benign,
        abstentions,
        counterexample,
    )


def run_l3(trials: int, seed: int) -> LawResult:
    """L3: absence of an observed event does not prove absence of change."""

    rng = random.Random(seed)
    hazard = naive_errors = guarded_errors = 0
    benign = naive_benign = guarded_benign = abstentions = 0
    counterexample: dict[str, Any] | None = None

    for index in range(trials):
        initial = rng.randrange(0, 10_000)
        cached = initial
        changed = rng.random() < 0.6
        current = initial + rng.randrange(1, 100) if changed else initial
        event_visible = changed and rng.random() < 0.5

        naive_value = current if event_visible else cached
        guarded_value = current  # action-time owner revalidation
        distinction_matters = changed and not event_visible
        if distinction_matters:
            hazard += 1
            if naive_value != current:
                naive_errors += 1
            if guarded_value != current:
                guarded_errors += 1
            counterexample = _first(
                counterexample,
                {
                    "trial": index,
                    "observedInitial": initial,
                    "currentReality": current,
                    "eventVisible": False,
                    "naiveConclusion": naive_value,
                    "guardedConclusion": guarded_value,
                    "failure": "no event was interpreted as no change",
                },
            )
        else:
            benign += 1
            if naive_value == current:
                naive_benign += 1
            if guarded_value == current:
                guarded_benign += 1

    assert counterexample is not None
    return LawResult(
        "L3",
        "Partial Observation",
        trials,
        hazard,
        naive_errors,
        guarded_errors,
        benign,
        naive_benign,
        guarded_benign,
        abstentions,
        counterexample,
    )


def run_l4(trials: int, seed: int) -> LawResult:
    """L4: choosing/knowing an effect does not grant authority to perform it."""

    rng = random.Random(seed)
    owners = ("runtime", "finance", "world")
    hazard = naive_errors = guarded_errors = 0
    benign = naive_benign = guarded_benign = abstentions = 0
    counterexample: dict[str, Any] | None = None

    for index in range(trials):
        authority_owner = rng.choice(owners)
        selected_owner = rng.choice(owners)
        authorized = authority_owner == selected_owner

        naive_performed = True
        guarded_performed = authorized
        distinction_matters = not authorized
        if distinction_matters:
            hazard += 1
            if naive_performed:
                naive_errors += 1
            if guarded_performed:
                guarded_errors += 1
            else:
                abstentions += 1
            counterexample = _first(
                counterexample,
                {
                    "trial": index,
                    "authorityOwner": authority_owner,
                    "selectedTargetOwner": selected_owner,
                    "naivePerformed": True,
                    "guardedPerformed": False,
                    "failure": "selection was treated as authority and crossed an owner boundary",
                },
            )
        else:
            benign += 1
            if naive_performed:
                naive_benign += 1
            if guarded_performed:
                guarded_benign += 1

    assert counterexample is not None
    return LawResult(
        "L4",
        "Scoped Authority",
        trials,
        hazard,
        naive_errors,
        guarded_errors,
        benign,
        naive_benign,
        guarded_benign,
        abstentions,
        counterexample,
    )


def run_l5(trials: int, seed: int) -> LawResult:
    """L5: causal stages cannot be collapsed into semantic completion."""

    rng = random.Random(seed)
    hazard = naive_errors = guarded_errors = 0
    benign = naive_benign = guarded_benign = abstentions = 0
    counterexample: dict[str, Any] | None = None

    for index in range(trials):
        capability_available = True
        selected = True
        admitted = True
        intervention_attempted = True
        mechanical_success = True
        transition_happened = rng.random() < 0.55
        semantic_goal_satisfied = transition_happened

        naive_complete = mechanical_success
        guarded_complete = mechanical_success and semantic_goal_satisfied
        distinction_matters = (
            capability_available
            and selected
            and admitted
            and intervention_attempted
            and mechanical_success
            and not transition_happened
        )
        if distinction_matters:
            hazard += 1
            if naive_complete:
                naive_errors += 1
            if guarded_complete:
                guarded_errors += 1
            counterexample = _first(
                counterexample,
                {
                    "trial": index,
                    "capability": True,
                    "selected": True,
                    "admitted": True,
                    "attempted": True,
                    "mechanicalSuccess": True,
                    "transitionHappened": False,
                    "semanticGoalSatisfied": False,
                    "naiveConclusion": "complete",
                    "guardedConclusion": "not complete",
                    "failure": "mechanical success was collapsed into semantic consequence",
                },
            )
        else:
            benign += 1
            if naive_complete == semantic_goal_satisfied:
                naive_benign += 1
            if guarded_complete == semantic_goal_satisfied:
                guarded_benign += 1

    assert counterexample is not None
    return LawResult(
        "L5",
        "Causal Non-Collapse",
        trials,
        hazard,
        naive_errors,
        guarded_errors,
        benign,
        naive_benign,
        guarded_benign,
        abstentions,
        counterexample,
    )


def physical_probes() -> dict[str, Any]:
    """Small physical probes that are deliberately not simulated world transitions."""

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)

        # L1: a selected JSON projection omits an existing reality field.
        reality = {"service": "ready", "latent_compromised": True}
        projection = {"service": reality["service"]}
        l1_naive_safe = not projection.get("latent_compromised", False)

        # L2: same payload bytes can belong to different identity bindings.
        left = root / "runtime.state"
        right = root / "finance.state"
        left.write_text("ready\n")
        right.write_text("ready\n")
        left_digest = hashlib.sha256(left.read_bytes()).hexdigest()
        right_digest = hashlib.sha256(right.read_bytes()).hexdigest()

        # L3: a cached observation can become stale without an event transport.
        changing = root / "owner.state"
        changing.write_text("revision-1\n")
        cached = changing.read_text()
        changing.write_text("revision-2\n")
        current = changing.read_text()

        # L4 is semantic authority, so the physical probe records that path access
        # alone does not encode owner authority. Both files are mechanically writable.
        runtime_target = root / "runtime-owned"
        finance_target = root / "finance-owned"
        runtime_target.write_text("untouched\n")
        finance_target.write_text("untouched\n")
        mechanically_writable = {
            "runtime": runtime_target.parent.exists(),
            "finance": finance_target.parent.exists(),
        }

        # L5: /usr/bin/true exits zero while the domain target remains unchanged.
        semantic_target = root / "semantic.target"
        semantic_target.write_text("before\n")
        process = subprocess.run(["/usr/bin/true"], check=False)
        after = semantic_target.read_text()

    return {
        "L1": {
            "reality": reality,
            "projection": projection,
            "naiveSafe": l1_naive_safe,
            "demonstrates": "an omitted property exists in reality while the projection looks ready",
        },
        "L2": {
            "leftIdentity": "runtime.state",
            "rightIdentity": "finance.state",
            "leftDigest": left_digest,
            "rightDigest": right_digest,
            "sameContentDigest": left_digest == right_digest,
            "demonstrates": "content equality does not collapse owner/entity identity",
        },
        "L3": {
            "cachedObservation": cached.strip(),
            "currentReality": current.strip(),
            "eventTransport": "none",
            "staleWithoutEvent": cached != current,
        },
        "L4": {
            "mechanicallyWritable": mechanically_writable,
            "demonstrates": "mechanical reachability alone carries no semantic owner authority",
        },
        "L5": {
            "processExitCode": process.returncode,
            "semanticStateAfter": after.strip(),
            "semanticGoal": "after",
            "mechanicalSuccessWithoutSemanticSuccess": process.returncode == 0 and after.strip() != "after",
        },
    }


def run_all(trials_per_law: int = 10_000) -> dict[str, Any]:
    runners: tuple[tuple[Callable[[int, int], LawResult], int], ...] = (
        (run_l1, 0xA11CE),
        (run_l2, 0xB1D1),
        (run_l3, 0x0B53),
        (run_l4, 0xA07A),
        (run_l5, 0xCA55A1),
    )
    results = [runner(trials_per_law, seed) for runner, seed in runners]
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.wl0-semantic-law-falsification",
        "trialsPerLaw": trials_per_law,
        "results": [result.payload() for result in results],
        "physicalProbes": physical_probes(),
        "acceptance": {
            "everyLawHasCounterexample": all(result.hazard_trials > 0 for result in results),
            "everyNaiveViolationProducesObservedError": all(result.naive_errors > 0 for result in results),
            "allGuardsEliminateHazardErrors": all(result.guarded_errors == 0 for result in results),
            "allGuardsPermitBenignSuccess": all(result.guarded_benign_successes > 0 for result in results),
        },
    }
    canonical = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    receipt["receiptDigest"] = "sha256:" + hashlib.sha256(canonical).hexdigest()
    return receipt


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10_000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    receipt = run_all(args.trials)
    rendered = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")
    return 0 if all(receipt["acceptance"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
