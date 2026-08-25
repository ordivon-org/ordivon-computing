from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("sem", ROOT / "aic_semantic_falsify.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load aic_semantic_falsify.py")
sem = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sem
spec.loader.exec_module(sem)

RESPONSE_CATALOG = [
    "RESTORE_EFFECTIVE_CONTROL",
    "REJECT_PHYSICAL_CONFIG_AS_NORMATIVE",
    "REMEDIATE_C",
    "REQUIRE_EXTERNAL_REANCHOR",
    "PRESERVE_AUTHORITY_CONFLICT",
    "HOLD_CONSEQUENTIAL_AUTHORITY_EFFECTS",
    "PRESERVE_INVALID_OR_REVERSED_SANCTION_HISTORY",
]


def consequence_authority_status(state) -> str:
    if state.binding_status == "CONTESTED":
        return "CONTESTED"
    if state.anchor_status == "THRESHOLD_COMPROMISED":
        return "ROOT_COMPROMISED"
    if state.valid_monitor is None:
        return "NO_VALID_MONITOR"
    if state.effective_controller is None:
        return "CONTROL_UNAVAILABLE"
    if state.effective_controller != state.valid_monitor:
        return "CONTROL_MISMATCH"
    return "AUTHORIZED"


def invalid_sanction_history(state) -> str:
    return "PRESENT" if any(s["currentStatus"] in {"INVALID", "INVALIDATED_LATER"} for s in state.sanctions) else "ABSENT"


def response_oracle(state) -> list[str]:
    responses: list[str] = []
    if state.binding_status == "CONTESTED":
        responses.extend(["PRESERVE_AUTHORITY_CONFLICT", "HOLD_CONSEQUENTIAL_AUTHORITY_EFFECTS"])
    elif state.anchor_status == "THRESHOLD_COMPROMISED":
        responses.append("REQUIRE_EXTERNAL_REANCHOR")
    elif state.valid_monitor is not None and state.effective_controller != state.valid_monitor:
        responses.append("RESTORE_EFFECTIVE_CONTROL")
    if state.physical_quota != state.normative_quota:
        responses.append("REJECT_PHYSICAL_CONFIG_AS_NORMATIVE")
    if state.remedy_due.get("C", 0) > 0:
        responses.append("REMEDIATE_C")
    if invalid_sanction_history(state) == "PRESENT":
        responses.append("PRESERVE_INVALID_OR_REVERSED_SANCTION_HISTORY")
    return sorted(set(responses))


def expected(state) -> dict[str, Any]:
    return {
        "officeHolder": state.valid_monitor if state.valid_monitor is not None else "NONE",
        "effectiveController": state.effective_controller if state.effective_controller is not None else "NONE",
        "authorityStanding": state.binding_status,
        "consequentialAuthorityStatus": consequence_authority_status(state),
        "normativeQuota": state.normative_quota,
        "physicalNormStanding": "CURRENT" if state.physical_quota == state.normative_quota else "NOT_CURRENT",
        "rootAnchorStatus": state.anchor_status,
        "remedyDueC": state.remedy_due.get("C", 0),
        "invalidOrReversedSanctionHistory": invalid_sanction_history(state),
        "requiredResponses": response_oracle(state),
    }


def orthogonal_frontier(state) -> dict[str, Any]:
    conflict_claimants = sorted({c["claimant"] for c in state.authority_claims if c.get("standing") == "CURRENT_SUPPORT"})
    return {
        "truthRole": "derived-current-binding-frontier-v2",
        "occurrenceDigest": sem.digest(state.event_log),
        "eventCount": len(state.event_log),
        "lineage": {
            "institutionLineage": state.institution_lineage,
            "identityRelation": state.identity_relation,
        },
        "authority": {
            "officeHolder": state.valid_monitor,
            "authorityStanding": state.binding_status,
            "effectiveController": state.effective_controller,
            "consequentialAuthorityStatus": consequence_authority_status(state),
            "conflictClaimants": conflict_claimants if state.binding_status == "CONTESTED" else [],
        },
        "norm": {
            "normativeQuota": state.normative_quota,
            "physicalQuota": state.physical_quota,
            "physicalNormStanding": "CURRENT" if state.physical_quota == state.normative_quota else "NOT_CURRENT",
        },
        "root": {
            "rootAnchorStatus": state.anchor_status,
            "activeAnchor": state.active_anchor,
        },
        "remedy": {
            "remedyDueC": state.remedy_due.get("C", 0),
        },
        "historicalValidity": {
            "invalidOrReversedSanctionHistory": invalid_sanction_history(state),
        },
    }


def scenario(sid: str, description: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    state = sem.replay(events)
    full = sem.current_binding_frontier(state)
    ortho = orthogonal_frontier(state)
    return {
        "scenarioId": sid,
        "description": description,
        "events": events,
        "eventCount": len(events),
        "fullFrontierV1": full,
        "orthogonalFrontierV2": ortho,
        "oracle": expected(state),
    }


def build() -> list[dict[str, Any]]:
    return [
        scenario(
            "AIC-S2-01-RECOVERED-USURPATION-THEN-SUCCESSION",
            "B previously usurped control and imposed an invalid sanction; A recovered and restitution was paid; later B lawfully wins the Monitor office and receives control.",
            [
                {"type": "steal_control_key", "actor": "B"},
                {"type": "sanction", "actor": "B", "target": "C", "amount": 2, "sanctionId": "S1"},
                {"type": "recover_control", "actor": "A"},
                {"type": "restitute", "target": "C", "amount": 2},
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
            ],
        ),
        scenario(
            "AIC-S2-02-OLD-TAMPER-LATER-VALID-RULE",
            "A valid amendment changes quota to 2, a physical tamper moves it back to 1, and a later valid amendment makes quota 1 the current valid rule again.",
            [
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "C1"},
                {"type": "tamper_physical_quota", "quota": 1, "physicalRevision": "T1"},
                {"type": "valid_amendment", "votes": 3, "quota": 1, "revision": "C2"},
                {"type": "transfer_control", "actor": "A"},
            ],
        ),
        scenario(
            "AIC-S2-03-PARTIAL-COMPROMISE-ROTATE-SUCCESSION",
            "One root is compromised, a valid in-band rotation restores a healthy anchor set, then C lawfully becomes Monitor and controller.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "in_band_root_rotation", "newAnchor": "ROTATED-SAFE"},
                {"type": "valid_election", "candidate": "C", "votes": 2},
                {"type": "transfer_control", "actor": "C"},
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "C1"},
            ],
        ),
        scenario(
            "AIC-S2-04-FULL-COMPROMISE-EXTERNAL-REFOUNDATION",
            "The old root threshold is fully compromised and cannot self-rotate; an independent external refoundation creates lineage I1 with C as Monitor and C receives control.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "compromise_root", "root": "R2"},
                {"type": "in_band_root_rotation", "newAnchor": "INVALID-INBAND"},
                {"type": "external_refoundation", "anchor": "EXT1", "lineage": "I1", "monitor": "C"},
                {"type": "transfer_control", "actor": "C"},
            ],
        ),
        scenario(
            "AIC-S2-05-CONTEST-RESOLVED-THEN-SUCCESSION",
            "A and B have incompatible current-support claims, the admitted dispute process clears those claims, then B wins a valid election and receives control.",
            [
                {"type": "authority_claim", "claimant": "A", "source": "ctx-1", "standing": "CURRENT_SUPPORT"},
                {"type": "authority_claim", "claimant": "B", "source": "ctx-2", "standing": "CURRENT_SUPPORT"},
                {"type": "clear_claims"},
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
            ],
        ),
        scenario(
            "AIC-S2-06-LAWFUL-SUCCESSION-THEN-INCAPACITY",
            "B lawfully becomes Monitor/controller, the institution validly adopts quota 2, and the execution channel is then disabled without succession.",
            [
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "C1"},
                {"type": "disable_control"},
            ],
        ),
        scenario(
            "AIC-S2-07-INVALID-PAST-VALID-CURRENT-SANCTION",
            "An old B usurpation caused an invalid sanction and restitution; after recovery, A later issues a valid sanction. Current power is valid despite invalid coercion in history.",
            [
                {"type": "steal_control_key", "actor": "B"},
                {"type": "sanction", "actor": "B", "target": "C", "amount": 2, "sanctionId": "S1"},
                {"type": "recover_control", "actor": "A"},
                {"type": "restitute", "target": "C", "amount": 2},
                {"type": "sanction", "actor": "A", "target": "C", "amount": 1, "sanctionId": "S2"},
            ],
        ),
        scenario(
            "AIC-S2-08-DELAYED-INVALIDITY-WITH-CURRENT-REMEDY",
            "A valid sanction is followed by an unrelated valid quota amendment; later review invalidates the old sanction, leaving current restitution due to C.",
            [
                {"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "S1"},
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "C1"},
                {"type": "transfer_control", "actor": "A"},
                {"type": "invalidate_sanction", "sanctionId": "S1"},
            ],
        ),
        scenario(
            "AIC-S2-09-CONTESTED-AUTHORITY-WITH-USURPED-CONTROL",
            "A and B have incompatible current authority claims and B also steals effective control; no dispute resolver is admitted at this cut.",
            [
                {"type": "authority_claim", "claimant": "A", "source": "ctx-1", "standing": "CURRENT_SUPPORT"},
                {"type": "authority_claim", "claimant": "B", "source": "ctx-2", "standing": "CURRENT_SUPPORT"},
                {"type": "steal_control_key", "actor": "B"},
                {"type": "tamper_physical_quota", "quota": 1, "physicalRevision": "NO-OP-TAMPER"},
            ],
        ),
        scenario(
            "AIC-S2-10-ROOT-COMPROMISE-PLUS-USURPED-CONTROL",
            "The root threshold is compromised, B steals control, and the compromised lineage attempts an invalid in-band rotation.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "compromise_root", "root": "R2"},
                {"type": "steal_control_key", "actor": "B"},
                {"type": "in_band_root_rotation", "newAnchor": "ATTACKER-ROOT"},
            ],
        ),
        scenario(
            "AIC-S2-11-OLD-TAMPER-OLD-USURPATION-CURRENTLY-RECOVERED",
            "A physical tamper and B usurpation both occurred; B imposed invalid coercion, A recovered control, then a valid amendment makes the physical quota current. Remedy to C remains due.",
            [
                {"type": "tamper_physical_quota", "quota": 2, "physicalRevision": "T1"},
                {"type": "steal_control_key", "actor": "B"},
                {"type": "sanction", "actor": "B", "target": "C", "amount": 1, "sanctionId": "S1"},
                {"type": "recover_control", "actor": "A"},
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "C1"},
            ],
        ),
        scenario(
            "AIC-S2-12-PAST-CONTEST-RESOLVED-CURRENT-CONTROL-RECOVERED",
            "B lawfully succeeds, later A/B recognition claims create a temporary contest, admitted resolution clears it, control is suspended, and B's execution channel is then restored.",
            [
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
                {"type": "authority_claim", "claimant": "A", "source": "ctx-1", "standing": "CURRENT_SUPPORT"},
                {"type": "authority_claim", "claimant": "B", "source": "ctx-2", "standing": "CURRENT_SUPPORT"},
                {"type": "clear_claims"},
                {"type": "disable_control"},
                {"type": "recover_control", "actor": "B"},
            ],
        ),
    ]


def main() -> None:
    old = json.loads((ROOT / "cases-v1.json").read_text())
    old_histories = {sem.canonical(s["events"]) for s in old["scenarios"]}
    scenarios = build()
    ids = [s["scenarioId"] for s in scenarios]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate scenario ids")
    copied = [s["scenarioId"] for s in scenarios if sem.canonical(s["events"]) in old_histories]

    gates = []
    for s in scenarios:
        f = s["orthogonalFrontierV2"]
        o = s["oracle"]
        no_action_leak = "requiredResponses" not in sem.canonical(f) and not any(x in sem.canonical(f) for x in RESPONSE_CATALOG)
        coord_ok = (
            (f["authority"]["officeHolder"] if f["authority"]["officeHolder"] is not None else "NONE") == o["officeHolder"]
            and (f["authority"]["effectiveController"] if f["authority"]["effectiveController"] is not None else "NONE") == o["effectiveController"]
            and f["authority"]["authorityStanding"] == o["authorityStanding"]
            and f["authority"]["consequentialAuthorityStatus"] == o["consequentialAuthorityStatus"]
            and f["norm"]["normativeQuota"] == o["normativeQuota"]
            and f["norm"]["physicalNormStanding"] == o["physicalNormStanding"]
            and f["root"]["rootAnchorStatus"] == o["rootAnchorStatus"]
            and f["remedy"]["remedyDueC"] == o["remedyDueC"]
            and f["historicalValidity"]["invalidOrReversedSanctionHistory"] == o["invalidOrReversedSanctionHistory"]
        )
        gates.append({"scenarioId": s["scenarioId"], "noActionLeak": no_action_leak, "coordinatesMatchOracle": coord_ok, "ok": no_action_leak and coord_ok})

    by_id = {s["scenarioId"]: s for s in scenarios}
    targeted = {
        "pastInvalidityDoesNotDisableCurrentAuthority": all(by_id[x]["oracle"]["consequentialAuthorityStatus"] == "AUTHORIZED" for x in ["AIC-S2-01-RECOVERED-USURPATION-THEN-SUCCESSION", "AIC-S2-07-INVALID-PAST-VALID-CURRENT-SANCTION", "AIC-S2-11-OLD-TAMPER-OLD-USURPATION-CURRENTLY-RECOVERED"]),
        "fullRootCompromiseBlocksCurrentConsequenceAuthority": by_id["AIC-S2-10-ROOT-COMPROMISE-PLUS-USURPED-CONTROL"]["oracle"]["consequentialAuthorityStatus"] == "ROOT_COMPROMISED",
        "externalRefoundationProducesReanchoredReplacement": by_id["AIC-S2-04-FULL-COMPROMISE-EXTERNAL-REFOUNDATION"]["oracle"]["rootAnchorStatus"] == "REANCHORED" and by_id["AIC-S2-04-FULL-COMPROMISE-EXTERNAL-REFOUNDATION"]["orthogonalFrontierV2"]["lineage"]["identityRelation"] == "REPLACED",
        "resolvedContestIsNotCurrentContest": all(by_id[x]["oracle"]["authorityStanding"] == "CURRENT" for x in ["AIC-S2-05-CONTEST-RESOLVED-THEN-SUCCESSION", "AIC-S2-12-PAST-CONTEST-RESOLVED-CURRENT-CONTROL-RECOVERED"]),
        "liveContestRemainsContest": by_id["AIC-S2-09-CONTESTED-AUTHORITY-WITH-USURPED-CONTROL"]["oracle"]["authorityStanding"] == "CONTESTED",
    }

    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s2-cases",
        "experimentId": "COJC-J3-AIC-ORTHOGONAL-FRONTIER-S2",
        "responseCatalog": RESPONSE_CATALOG,
        "scenarios": scenarios,
    }
    evidence = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s2-deterministic-preflight",
        "experimentId": "COJC-J3-AIC-ORTHOGONAL-FRONTIER-S2",
        "scenarioCount": len(scenarios),
        "copiedS1Histories": copied,
        "scenarioGates": gates,
        "targetedGates": targeted,
        "mandatoryPass": not copied and all(g["ok"] for g in gates) and all(targeted.values()),
        "casesDigest": sem.digest(result),
    }
    (ROOT / "cases-s2-v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    (ROOT / "evidence-s2-deterministic.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if evidence["mandatoryPass"] else 2)


if __name__ == "__main__":
    main()
