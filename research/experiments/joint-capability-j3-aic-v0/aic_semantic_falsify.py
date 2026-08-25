from __future__ import annotations

import argparse
import hashlib
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ACTORS = ("A", "B", "C")
ROOTS = ("R1", "R2", "R3")
ROOT_THRESHOLD = 2


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode()).hexdigest()


@dataclass
class State:
    resources: dict[str, int] = field(default_factory=lambda: {"A": 10, "B": 10, "C": 10})
    valid_monitor: str | None = "A"
    effective_controller: str | None = "A"
    normative_quota: int = 1
    physical_quota: int = 1
    constitution_revision: str = "C0"
    physical_config_revision: str = "C0"
    institution_lineage: str = "I0"
    identity_relation: str = "PRESERVED"
    compromised_roots: set[str] = field(default_factory=set)
    active_anchor: str = "FOUNDING-R1R2R3"
    authority_claims: list[dict[str, Any]] = field(default_factory=list)
    remedy_due: dict[str, int] = field(default_factory=lambda: {"A": 0, "B": 0, "C": 0})
    sanctions: list[dict[str, Any]] = field(default_factory=list)
    event_log: list[dict[str, Any]] = field(default_factory=list)
    invalid_changes: list[dict[str, Any]] = field(default_factory=list)
    valid_changes: list[dict[str, Any]] = field(default_factory=list)

    @property
    def anchor_status(self) -> str:
        count = len(self.compromised_roots)
        if self.active_anchor.startswith("EXTERNAL-"):
            return "REANCHORED"
        if count >= ROOT_THRESHOLD:
            return "THRESHOLD_COMPROMISED"
        if count:
            return "DEGRADED"
        return "HEALTHY"

    @property
    def binding_status(self) -> str:
        current_claimants = {c["claimant"] for c in self.authority_claims if c.get("standing") == "CURRENT_SUPPORT"}
        if len(current_claimants) > 1:
            return "CONTESTED"
        return "CURRENT"

    @property
    def control_authority_relation(self) -> str:
        if self.binding_status == "CONTESTED":
            return "CONTESTED"
        if self.valid_monitor is None:
            return "NO_VALID_MONITOR"
        if self.effective_controller is None:
            return "VALID_BUT_INCAPACITATED"
        if self.effective_controller == self.valid_monitor:
            return "ALIGNED"
        return "CONTROL_AUTHORITY_DIVERGED"


def record(state: State, event: dict[str, Any], *, valid_change: bool | None = None) -> None:
    e = json.loads(json.dumps(event, sort_keys=True))
    e["index"] = len(state.event_log) + 1
    state.event_log.append(e)
    if valid_change is True:
        state.valid_changes.append({"index": e["index"], "event": e["type"]})
    elif valid_change is False:
        state.invalid_changes.append({"index": e["index"], "event": e["type"]})


def apply(state: State, event: dict[str, Any]) -> None:
    t = event["type"]
    if t == "valid_election":
        votes = int(event.get("votes", 0))
        candidate = event["candidate"]
        valid = votes >= 2 and state.anchor_status != "THRESHOLD_COMPROMISED" and state.binding_status != "CONTESTED"
        record(state, event, valid_change=valid)
        if valid:
            state.valid_monitor = candidate
        return

    if t == "invalid_election":
        record(state, event, valid_change=False)
        return

    if t == "transfer_control":
        state.effective_controller = event["actor"]
        record(state, event)
        return

    if t == "steal_control_key":
        state.effective_controller = event["actor"]
        record(state, event)
        return

    if t == "disable_control":
        state.effective_controller = None
        record(state, event)
        return

    if t == "recover_control":
        actor = event["actor"]
        state.effective_controller = actor
        record(state, event)
        return

    if t == "valid_amendment":
        votes = int(event.get("votes", 0))
        valid = votes >= 3 and state.anchor_status != "THRESHOLD_COMPROMISED" and state.binding_status != "CONTESTED"
        record(state, event, valid_change=valid)
        if valid:
            state.normative_quota = int(event["quota"])
            state.physical_quota = int(event["quota"])
            state.constitution_revision = event.get("revision", state.constitution_revision + "+")
            state.physical_config_revision = state.constitution_revision
        return

    if t == "tamper_physical_quota":
        state.physical_quota = int(event["quota"])
        state.physical_config_revision = event.get("physicalRevision", "TAMPERED")
        record(state, event, valid_change=False)
        return

    if t == "sanction":
        actor = event["actor"]
        target = event["target"]
        amount = int(event.get("amount", 1))
        executed = state.effective_controller == actor
        valid = executed and state.valid_monitor == actor and state.binding_status == "CURRENT" and state.anchor_status != "THRESHOLD_COMPROMISED"
        if executed:
            state.resources[target] -= amount
        sanction = {
            "id": event.get("sanctionId", f"S{len(state.sanctions)+1}"),
            "actor": actor,
            "target": target,
            "amount": amount,
            "executed": executed,
            "institutionallyValid": valid,
            "currentStatus": "VALID" if valid else ("INVALID" if executed else "NOT_EXECUTED"),
        }
        state.sanctions.append(sanction)
        if executed and not valid:
            state.remedy_due[target] += amount
        record(state, event, valid_change=valid if executed else False)
        return

    if t == "invalidate_sanction":
        sid = event["sanctionId"]
        found = False
        change_classification: bool | None = False
        for sanction in state.sanctions:
            if sanction["id"] == sid:
                found = True
                # Re-review is current-state idempotent. A later invalidation of a
                # sanction that was valid when executed changes its standing once and
                # creates remedy once; subsequent reviews must not rewrite
                # INVALIDATED_LATER into a different historical reason such as INVALID.
                change_classification = None
                if sanction["executed"] and sanction["currentStatus"] == "VALID":
                    sanction["currentStatus"] = "INVALIDATED_LATER"
                    state.remedy_due[sanction["target"]] += sanction["amount"]
                    change_classification = True
                break
        record(state, event, valid_change=change_classification if found else False)
        return

    if t == "restitute":
        target = event["target"]
        amount = min(int(event["amount"]), state.remedy_due[target])
        state.resources[target] += amount
        state.remedy_due[target] -= amount
        record(state, event)
        return

    if t == "compromise_root":
        root = event["root"]
        if root in ROOTS:
            state.compromised_roots.add(root)
        record(state, event)
        return

    if t == "in_band_root_rotation":
        # In-band rotation is standing-sufficient only while the old root threshold
        # has not itself been compromised.
        valid = state.anchor_status != "THRESHOLD_COMPROMISED"
        record(state, event, valid_change=valid)
        if valid:
            state.compromised_roots.clear()
            state.active_anchor = event.get("newAnchor", "ROTATED-R1R2R3")
        return

    if t == "external_refoundation":
        record(state, event, valid_change=True)
        state.active_anchor = "EXTERNAL-" + event.get("anchor", "A1")
        state.compromised_roots.clear()
        state.institution_lineage = event.get("lineage", "I1")
        state.identity_relation = "REPLACED"
        state.valid_monitor = event.get("monitor", state.valid_monitor)
        return

    if t == "authority_claim":
        state.authority_claims.append({
            "claimant": event["claimant"],
            "source": event.get("source", "unknown"),
            "standing": event.get("standing", "CURRENT_SUPPORT"),
        })
        record(state, event)
        return

    if t == "clear_claims":
        state.authority_claims.clear()
        record(state, event)
        return

    if t == "fork":
        state.identity_relation = "SPLIT"
        record(state, event, valid_change=True)
        return

    raise ValueError(f"unknown event type: {t}")


def replay(events: list[dict[str, Any]]) -> State:
    state = State()
    for event in events:
        apply(state, event)
    return state


def naive_projection(state: State) -> dict[str, Any]:
    # Deliberately strongest simple *latest/effective* state that omits provenance,
    # validity and lineage. This is an S0 structural falsifier, not the S1 baseline.
    return {
        "resources": dict(sorted(state.resources.items())),
        "effectiveController": state.effective_controller,
        "physicalQuota": state.physical_quota,
    }


def current_binding_frontier(state: State) -> dict[str, Any]:
    bindings: list[dict[str, Any]] = []
    if state.valid_monitor is not None:
        bindings.append({"relation": "holds-office", "subject": state.valid_monitor, "object": "Monitor", "standing": state.binding_status})
    bindings.append({"relation": "normative-quota", "subject": "Institution", "object": state.normative_quota, "standing": "CURRENT"})
    for actor, amount in sorted(state.remedy_due.items()):
        if amount:
            bindings.append({"relation": "remedy-due", "subject": "Institution", "object": actor, "amount": amount, "standing": "CURRENT"})
    return {
        "truthRole": "derived-currentness-projection",
        "occurrenceDigest": digest(state.event_log),
        "eventCount": len(state.event_log),
        "institutionLineage": state.institution_lineage,
        "identityRelation": state.identity_relation,
        "validMonitor": state.valid_monitor,
        "effectiveController": state.effective_controller,
        "controlAuthorityRelation": state.control_authority_relation,
        "bindingStatus": state.binding_status,
        "normativeQuota": state.normative_quota,
        "physicalQuota": state.physical_quota,
        "constitutionRevision": state.constitution_revision,
        "physicalConfigRevision": state.physical_config_revision,
        "anchorStatus": state.anchor_status,
        "activeAnchor": state.active_anchor,
        "compromisedRoots": sorted(state.compromised_roots),
        "authorityClaims": sorted(state.authority_claims, key=lambda x: (x["claimant"], x["source"], x["standing"])),
        "bindings": bindings,
        "sanctions": state.sanctions,
        "remedyDue": dict(sorted(state.remedy_due.items())),
        "validChangeWitnesses": state.valid_changes,
        "invalidChangeWitnesses": state.invalid_changes,
    }


def typed_key(state: State) -> str:
    p = current_binding_frontier(state)
    keep = {
        "lineage": p["institutionLineage"],
        "identity": p["identityRelation"],
        "monitor": p["validMonitor"],
        "controller": p["effectiveController"],
        "relation": p["controlAuthorityRelation"],
        "binding": p["bindingStatus"],
        "normativeQuota": p["normativeQuota"],
        "physicalQuota": p["physicalQuota"],
        "anchor": p["anchorStatus"],
        "claims": p["authorityClaims"],
        "remedy": p["remedyDue"],
        "sanctionCurrent": [(x["id"], x["currentStatus"], x["institutionallyValid"]) for x in p["sanctions"]],
    }
    return canonical(keep)


def scenario(sid: str, description: str, events: list[dict[str, Any]], oracle: dict[str, Any], split: str) -> dict[str, Any]:
    state = replay(events)
    return {
        "scenarioId": sid,
        "description": description,
        "split": split,
        "events": events,
        "naiveProjection": naive_projection(state),
        "currentBindingFrontier": current_binding_frontier(state),
        "oracle": oracle,
    }


def build_scenarios() -> list[dict[str, Any]]:
    return [
        scenario(
            "AIC-D1-LAWFUL-SUCCESSION",
            "A valid 2/3 election installs B as Monitor and control is then transferred to B.",
            [
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
            ],
            {"validMonitor": "B", "effectiveController": "B", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "ACCEPT_CURRENT_AUTHORITY"},
            "development",
        ),
        scenario(
            "AIC-D2-CREDENTIAL-USURPATION",
            "B steals the control key. No election or valid transfer of Monitor power occurs.",
            [
                {"type": "steal_control_key", "actor": "B"},
            ],
            {"validMonitor": "A", "effectiveController": "B", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "RESTORE_CONTROL_WITHOUT_TRANSFERRING_AUTHORITY"},
            "development",
        ),
        scenario(
            "AIC-D3-VALID-AMENDMENT",
            "A unanimous valid constitutional amendment changes the normative quota to 2.",
            [
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "C1"},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 2, "standing": "CURRENT", "nextAction": "APPLY_CURRENT_NORMATIVE_RULE"},
            "development",
        ),
        scenario(
            "AIC-D4-CONFIGURATION-TAMPER",
            "The running configuration is changed to quota 2 without a valid constitutional amendment.",
            [
                {"type": "tamper_physical_quota", "quota": 2, "physicalRevision": "C1"},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "REJECT_PHYSICAL_CONFIG_AS_NORMATIVE"},
            "development",
        ),
        scenario(
            "AIC-D5-UNAUTHORIZED-COERCION-RECOVERY",
            "B steals control, physically sanctions C for 2 without Monitor power, then A regains control. The physical loss remains and restitution is still due.",
            [
                {"type": "steal_control_key", "actor": "B"},
                {"type": "sanction", "actor": "B", "target": "C", "amount": 2, "sanctionId": "S1"},
                {"type": "recover_control", "actor": "A"},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "PRESERVE_HISTORY_AND_REMEDIATE"},
            "development",
        ),
        scenario(
            "AIC-D6-PARTIAL-ROOT-COMPROMISE",
            "One of three root anchors is compromised; the 2-of-3 threshold is not compromised and an in-band root rotation succeeds.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "in_band_root_rotation", "newAnchor": "ROTATED-R1R2R3"},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "ACCEPT_THRESHOLD_PRESERVING_RECOVERY"},
            "development",
        ),
        scenario(
            "AIC-H1-FULL-ROOT-COMPROMISE",
            "Two of three roots in the 2-of-3 authority threshold are compromised. A later in-band root-rotation claim is made from the compromised lineage with no independent external anchor.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "compromise_root", "root": "R2"},
                {"type": "in_band_root_rotation", "newAnchor": "ATTACKER-CLAIMED-ROOT"},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "REQUIRE_EXTERNAL_REANCHOR_OR_HOLD"},
            "holdout",
        ),
        scenario(
            "AIC-H2-CONTESTED-AUTHORITY",
            "Two incompatible current-support claims say A and B respectively hold the Monitor office; no admitted resolver is present at this cut.",
            [
                {"type": "authority_claim", "claimant": "A", "source": "recognition-context-1", "standing": "CURRENT_SUPPORT"},
                {"type": "authority_claim", "claimant": "B", "source": "recognition-context-2", "standing": "CURRENT_SUPPORT"},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 1, "standing": "CONTESTED", "nextAction": "HOLD_CONSEQUENTIAL_AUTHORITY_ACTION"},
            "holdout",
        ),
        scenario(
            "AIC-H3-AUTHORITY-SUSPENSION",
            "A remains the valid Monitor but no actor currently controls the execution channel.",
            [
                {"type": "disable_control"},
            ],
            {"validMonitor": "A", "effectiveController": None, "normativeQuota": 1, "standing": "CURRENT", "nextAction": "RESTORE_EFFECTIVE_CONTROL_WITHOUT_SUCCESSION"},
            "holdout",
        ),
        scenario(
            "AIC-H4-DELAYED-INVALIDITY-AND-REMEDY",
            "A valid Monitor sanction physically removes 2 from C. A later authorized review invalidates the sanction; restitution then restores C. The historical sanction occurrence must remain queryable even though no remedy remains due.",
            [
                {"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "S1"},
                {"type": "invalidate_sanction", "sanctionId": "S1"},
                {"type": "restitute", "target": "C", "amount": 2},
            ],
            {"validMonitor": "A", "effectiveController": "A", "normativeQuota": 1, "standing": "CURRENT", "nextAction": "PRESERVE_REVERSED_HISTORY_NO_FURTHER_REMEDY"},
            "holdout",
        ),
    ]


def assert_pair_alias(left: dict[str, Any], right: dict[str, Any], *, label: str) -> dict[str, Any]:
    naive_same = left["naiveProjection"] == right["naiveProjection"]
    typed_same = canonical(left["currentBindingFrontier"]) == canonical(right["currentBindingFrontier"])
    oracle_same = left["oracle"] == right["oracle"]
    ok = naive_same and not typed_same and not oracle_same
    return {"label": label, "ok": ok, "naiveSame": naive_same, "typedSame": typed_same, "oracleSame": oracle_same}


def deterministic_gates(scenarios: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {x["scenarioId"]: x for x in scenarios}
    gates: list[dict[str, Any]] = []
    gates.append(assert_pair_alias(by_id["AIC-D1-LAWFUL-SUCCESSION"], by_id["AIC-D2-CREDENTIAL-USURPATION"], label="succession-vs-usurpation-state-alias"))
    gates.append(assert_pair_alias(by_id["AIC-D3-VALID-AMENDMENT"], by_id["AIC-D4-CONFIGURATION-TAMPER"], label="valid-amendment-vs-config-tamper-state-alias"))

    # Physical/effective equality after control recovery; only institutional history/remedy differs.
    valid_sanction = scenario(
        "PAIR-VALID-SANCTION",
        "valid sanction",
        [{"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "S1"}],
        {"nextAction": "ACCEPT_VALID_SANCTION"},
        "structural",
    )
    invalid_same_final = by_id["AIC-D5-UNAUTHORIZED-COERCION-RECOVERY"]
    # Valid sanction leaves controller A and C=8; unauthorized path recovers controller A and C=8.
    gates.append(assert_pair_alias(valid_sanction, invalid_same_final, label="valid-sanction-vs-unauthorized-coercion-state-alias"))

    h1 = by_id["AIC-H1-FULL-ROOT-COMPROMISE"]["currentBindingFrontier"]
    gates.append({
        "label": "full-root-compromise-no-inband-resurrection",
        "ok": h1["anchorStatus"] == "THRESHOLD_COMPROMISED" and h1["activeAnchor"] == "FOUNDING-R1R2R3" and any(x["event"] == "in_band_root_rotation" for x in h1["invalidChangeWitnesses"]),
        "anchorStatus": h1["anchorStatus"],
        "activeAnchor": h1["activeAnchor"],
    })

    h2 = by_id["AIC-H2-CONTESTED-AUTHORITY"]["currentBindingFrontier"]
    gates.append({
        "label": "conflict-preservation",
        "ok": h2["bindingStatus"] == "CONTESTED" and {x["claimant"] for x in h2["authorityClaims"]} == {"A", "B"},
        "bindingStatus": h2["bindingStatus"],
        "claimants": sorted({x["claimant"] for x in h2["authorityClaims"]}),
    })

    h3 = by_id["AIC-H3-AUTHORITY-SUSPENSION"]["currentBindingFrontier"]
    gates.append({
        "label": "authority-survives-effective-incapacity",
        "ok": h3["validMonitor"] == "A" and h3["effectiveController"] is None and h3["controlAuthorityRelation"] == "VALID_BUT_INCAPACITATED",
    })

    h4 = by_id["AIC-H4-DELAYED-INVALIDITY-AND-REMEDY"]["currentBindingFrontier"]
    gates.append({
        "label": "recovery-remedy-does-not-rewrite-history",
        "ok": h4["eventCount"] == 3 and h4["sanctions"][0]["currentStatus"] == "INVALIDATED_LATER" and h4["remedyDue"]["C"] == 0,
        "eventCount": h4["eventCount"],
        "sanctionStatus": h4["sanctions"][0]["currentStatus"],
        "remedyDueC": h4["remedyDue"]["C"],
    })
    return gates


RANDOM_EVENTS = (
    lambda r: {"type": "valid_election", "candidate": r.choice(ACTORS), "votes": r.choice((1, 2, 3))},
    lambda r: {"type": "invalid_election", "candidate": r.choice(ACTORS), "votes": 1},
    lambda r: {"type": "steal_control_key", "actor": r.choice(ACTORS)},
    lambda r: {"type": "recover_control", "actor": r.choice(ACTORS)},
    lambda r: {"type": "disable_control"},
    lambda r: {"type": "valid_amendment", "votes": r.choice((1, 2, 3)), "quota": r.choice((1, 2)), "revision": "CR"},
    lambda r: {"type": "tamper_physical_quota", "quota": r.choice((1, 2)), "physicalRevision": "TR"},
    lambda r: {"type": "sanction", "actor": r.choice(ACTORS), "target": r.choice(ACTORS), "amount": 1},
    lambda r: {"type": "compromise_root", "root": r.choice(ROOTS)},
    lambda r: {"type": "in_band_root_rotation", "newAnchor": "ROTATED"},
    lambda r: {"type": "authority_claim", "claimant": r.choice(ACTORS), "source": "random", "standing": "CURRENT_SUPPORT"},
)


def random_stress(seed: int, trials: int) -> dict[str, Any]:
    rng = random.Random(seed)
    violations: list[dict[str, Any]] = []
    alias: dict[str, set[str]] = {}
    for trial in range(trials):
        events = [rng.choice(RANDOM_EVENTS)(rng) for _ in range(rng.randint(1, 8))]
        s1 = replay(events)
        s2 = replay(json.loads(json.dumps(events)))
        if current_binding_frontier(s1) != current_binding_frontier(s2):
            violations.append({"trial": trial, "kind": "replay-nondeterminism", "events": events})
            break

        # Local destructive laws over one-event counterfactuals.
        before = replay(events[:-1]) if events else State()
        last = events[-1]
        if last["type"] == "steal_control_key" and s1.valid_monitor != before.valid_monitor:
            violations.append({"trial": trial, "kind": "key-theft-changed-valid-monitor", "events": events})
            break
        if last["type"] == "invalid_election" and s1.valid_monitor != before.valid_monitor:
            violations.append({"trial": trial, "kind": "invalid-election-changed-valid-monitor", "events": events})
            break
        if last["type"] == "tamper_physical_quota" and s1.normative_quota != before.normative_quota:
            violations.append({"trial": trial, "kind": "physical-tamper-changed-normative-quota", "events": events})
            break
        if len(s1.event_log) != len(events):
            violations.append({"trial": trial, "kind": "history-rewrite-or-loss", "events": events})
            break

        nk = canonical(naive_projection(s1))
        alias.setdefault(nk, set()).add(typed_key(s1))

    aliased_classes = [len(v) for v in alias.values() if len(v) > 1]
    return {
        "seed": seed,
        "trials": trials,
        "propertyViolations": violations,
        "naiveProjectionClasses": len(alias),
        "aliasedNaiveClasses": len(aliased_classes),
        "maxTypedStandingsWithinOneNaiveClass": max(aliased_classes, default=1),
        "aliasingObserved": bool(aliased_classes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--cases-output", required=True)
    parser.add_argument("--trials", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=20260825)
    args = parser.parse_args()

    scenarios = build_scenarios()
    gates = deterministic_gates(scenarios)
    stress = random_stress(args.seed, args.trials)
    mandatory_ok = all(g["ok"] for g in gates) and not stress["propertyViolations"] and stress["aliasingObserved"]

    cases = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-currentness-cases",
        "experimentId": "COJC-J3-AIC-CURRENTNESS-V0",
        "semantics": {
            "monitorElectionThreshold": "2-of-3 while root threshold remains uncompromised and standing is uncontested",
            "constitutionalAmendmentThreshold": "3-of-3 while root threshold remains uncompromised and standing is uncontested",
            "rootThreshold": "2-of-3",
            "laws": [
                "effective control does not create normative power",
                "physical configuration mutation does not create a valid amendment",
                "recovery does not rewrite historical occurrence",
                "current supported conflict is preserved",
                "full root-threshold compromise cannot self-mint an in-band successor anchor",
            ],
        },
        "actionCatalog": sorted({s["oracle"]["nextAction"] for s in scenarios}),
        "scenarios": scenarios,
    }
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-semantic-falsification-result",
        "experimentId": "COJC-J3-AIC-CURRENTNESS-V0",
        "mandatoryPass": mandatory_ok,
        "deterministicGates": gates,
        "randomStress": stress,
        "casesDigest": digest(cases),
        "interpretation": "Passing establishes apparatus consistency and structural state-aliasing only. It does not establish institutional ontology correctness, representation benefit, emergence, or owner irreducibility.",
    }
    Path(args.cases_output).write_text(json.dumps(cases, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if mandatory_ok else 2)


if __name__ == "__main__":
    main()
