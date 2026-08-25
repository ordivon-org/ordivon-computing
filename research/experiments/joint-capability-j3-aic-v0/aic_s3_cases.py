from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


sem = load("aic_sem_s3", ROOT / "aic_semantic_falsify.py")
s2 = load("aic_s2_cases_for_s3", ROOT / "aic_s2_cases.py")


def naive_effective_snapshot(state) -> dict[str, Any]:
    return {
        "truthRole": "observed-effective-snapshot-only",
        "effectiveController": state.effective_controller,
        "physicalQuota": state.physical_quota,
        "resources": dict(state.resources),
        "activeAnchorLabel": state.active_anchor,
        "eventCountNotExposed": True,
        "warning": "This snapshot reports observed effective/physical state only. It does not establish office-holding, authority validity, normative standing, root sufficiency, remedy, provenance, conflict resolution, or historical validity."
    }


def make_case(case_id: str, description: str, pre_events: list[dict[str, Any]], post_events: list[dict[str, Any]]) -> dict[str, Any]:
    boundary = sem.replay(pre_events)
    final = sem.replay(pre_events + post_events)
    return {
        "scenarioId": case_id,
        "description": description,
        "preHandoffEvents": pre_events,
        "postReplacementEvents": post_events,
        "naiveHandoffSnapshot": naive_effective_snapshot(boundary),
        "governedHandoffFrontier": s2.orthogonal_frontier(boundary),
        "boundaryOracle": s2.expected(boundary),
        "finalOracle": s2.expected(final),
        "fullHistoryDigest": sem.digest(pre_events + post_events),
        "preHistoryDigest": sem.digest(pre_events),
    }


def build() -> list[dict[str, Any]]:
    return [
        make_case(
            "AIC-S3-01-SUCCESSION-THEN-CONTROL-THEFT",
            "Before replacement B lawfully becomes Monitor/controller and quota 2 becomes valid; after replacement C steals the control channel.",
            [
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "S3-C1"},
            ],
            [
                {"type": "steal_control_key", "actor": "C"},
            ],
        ),
        make_case(
            "AIC-S3-02-REFOUNDATION-THEN-AMENDMENT",
            "Before replacement the old root threshold is compromised and an independent refoundation creates lineage I1 with C as Monitor/controller; after replacement the institution adopts quota 2.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "compromise_root", "root": "R2"},
                {"type": "in_band_root_rotation", "newAnchor": "INVALID-S3-INBAND"},
                {"type": "external_refoundation", "anchor": "S3-EXT1", "lineage": "I1", "monitor": "C"},
                {"type": "transfer_control", "actor": "C"},
            ],
            [
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "S3-C1"},
            ],
        ),
        make_case(
            "AIC-S3-03-LIVE-CONTEST-THEN-SANCTION",
            "Before replacement incompatible current-support claims for A and B remain unresolved while A still controls execution; after replacement A sanctions C.",
            [
                {"type": "authority_claim", "claimant": "A", "source": "s3-ctx-a", "standing": "CURRENT_SUPPORT"},
                {"type": "authority_claim", "claimant": "B", "source": "s3-ctx-b", "standing": "CURRENT_SUPPORT"},
            ],
            [
                {"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "S3-S1"},
            ],
        ),
        make_case(
            "AIC-S3-04-INVALID-COERCION-THEN-SUCCESSION",
            "Before replacement B usurps control and imposes invalid coercion, then A recovers control; after replacement B lawfully wins the office and receives control while C's old remedy remains due.",
            [
                {"type": "steal_control_key", "actor": "B"},
                {"type": "sanction", "actor": "B", "target": "C", "amount": 2, "sanctionId": "S3-S1"},
                {"type": "recover_control", "actor": "A"},
            ],
            [
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
            ],
        ),
        make_case(
            "AIC-S3-05-TAMPER-THEN-VALID-REALIGNMENT",
            "Before replacement quota 2 is validly adopted and the running configuration is later tampered back to 1; after replacement a valid amendment makes quota 1 current again.",
            [
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "S3-C1"},
                {"type": "tamper_physical_quota", "quota": 1, "physicalRevision": "S3-T1"},
            ],
            [
                {"type": "valid_amendment", "votes": 3, "quota": 1, "revision": "S3-C2"},
            ],
        ),
        make_case(
            "AIC-S3-06-FULL-COMPROMISE-THEN-INBAND-ATTEMPT",
            "Before replacement two of three roots are compromised; after replacement the compromised lineage attempts an in-band root rotation.",
            [
                {"type": "compromise_root", "root": "R1"},
                {"type": "compromise_root", "root": "R2"},
            ],
            [
                {"type": "in_band_root_rotation", "newAnchor": "S3-ATTACKER-ROOT"},
            ],
        ),
        make_case(
            "AIC-S3-07-SUCCESSION-INCAPACITY-THEN-RECOVERY",
            "Before replacement B lawfully becomes Monitor/controller and the execution channel is disabled without succession; after replacement B's control channel is restored.",
            [
                {"type": "valid_election", "candidate": "B", "votes": 2},
                {"type": "transfer_control", "actor": "B"},
                {"type": "disable_control"},
            ],
            [
                {"type": "recover_control", "actor": "B"},
            ],
        ),
        make_case(
            "AIC-S3-08-INVALIDATED-RESTITUTED-THEN-AMENDMENT",
            "Before replacement A's valid sanction is later invalidated and fully restituted, preserving invalid/reversed sanction history with no remaining remedy; after replacement quota 2 is validly adopted.",
            [
                {"type": "sanction", "actor": "A", "target": "C", "amount": 2, "sanctionId": "S3-S1"},
                {"type": "invalidate_sanction", "sanctionId": "S3-S1"},
                {"type": "restitute", "target": "C", "amount": 2},
            ],
            [
                {"type": "valid_amendment", "votes": 3, "quota": 2, "revision": "S3-C1"},
            ],
        ),
    ]


def main() -> None:
    scenarios = build()
    old_histories: set[str] = set()
    for file_name, key in [("cases-v1.json", "scenarios"), ("cases-s2-v1.json", "scenarios")]:
        data = json.loads((ROOT / file_name).read_text())
        for s in data[key]:
            events = s.get("events") or (s.get("preHandoffEvents", []) + s.get("postReplacementEvents", []))
            old_histories.add(sem.canonical(events))
    copied = [s["scenarioId"] for s in scenarios if sem.canonical(s["preHandoffEvents"] + s["postReplacementEvents"]) in old_histories]

    response_catalog = set(s2.RESPONSE_CATALOG)
    gates = []
    for s in scenarios:
        frontier_text = sem.canonical(s["governedHandoffFrontier"])
        no_action_leak = "requiredResponses" not in frontier_text and not any(x in frontier_text for x in response_catalog)
        boundary = sem.replay(s["preHandoffEvents"])
        frontier_matches = s["governedHandoffFrontier"] == s2.orthogonal_frontier(boundary)
        final = sem.replay(s["preHandoffEvents"] + s["postReplacementEvents"])
        oracle_matches = s["finalOracle"] == s2.expected(final)
        gates.append({
            "scenarioId": s["scenarioId"],
            "noActionLeak": no_action_leak,
            "frontierMatchesBoundaryReplay": frontier_matches,
            "finalOracleMatchesReplay": oracle_matches,
            "ok": no_action_leak and frontier_matches and oracle_matches,
        })

    by_id = {s["scenarioId"]: s for s in scenarios}
    targeted = {
        "replacementNeedsInheritedOffice": by_id["AIC-S3-01-SUCCESSION-THEN-CONTROL-THEFT"]["finalOracle"]["officeHolder"] == "B" and by_id["AIC-S3-01-SUCCESSION-THEN-CONTROL-THEFT"]["finalOracle"]["consequentialAuthorityStatus"] == "CONTROL_MISMATCH",
        "refoundationSurvivesReplacement": by_id["AIC-S3-02-REFOUNDATION-THEN-AMENDMENT"]["finalOracle"]["officeHolder"] == "C" and by_id["AIC-S3-02-REFOUNDATION-THEN-AMENDMENT"]["finalOracle"]["rootAnchorStatus"] == "REANCHORED",
        "contestConstrainsPostReplacementSanction": by_id["AIC-S3-03-LIVE-CONTEST-THEN-SANCTION"]["finalOracle"]["authorityStanding"] == "CONTESTED" and by_id["AIC-S3-03-LIVE-CONTEST-THEN-SANCTION"]["finalOracle"]["remedyDueC"] == 2,
        "oldInvalidityPersistsAcrossNewLawfulSuccession": by_id["AIC-S3-04-INVALID-COERCION-THEN-SUCCESSION"]["finalOracle"]["consequentialAuthorityStatus"] == "AUTHORIZED" and by_id["AIC-S3-04-INVALID-COERCION-THEN-SUCCESSION"]["finalOracle"]["invalidOrReversedSanctionHistory"] == "PRESENT",
        "fullCompromiseStillNeedsExternalReanchor": by_id["AIC-S3-06-FULL-COMPROMISE-THEN-INBAND-ATTEMPT"]["finalOracle"]["consequentialAuthorityStatus"] == "ROOT_COMPROMISED",
        "incapacityDoesNotEraseSuccession": by_id["AIC-S3-07-SUCCESSION-INCAPACITY-THEN-RECOVERY"]["finalOracle"]["officeHolder"] == "B" and by_id["AIC-S3-07-SUCCESSION-INCAPACITY-THEN-RECOVERY"]["finalOracle"]["consequentialAuthorityStatus"] == "AUTHORIZED",
        "completedRemedyDoesNotEraseHistory": by_id["AIC-S3-08-INVALIDATED-RESTITUTED-THEN-AMENDMENT"]["finalOracle"]["remedyDueC"] == 0 and by_id["AIC-S3-08-INVALIDATED-RESTITUTED-THEN-AMENDMENT"]["finalOracle"]["invalidOrReversedSanctionHistory"] == "PRESENT",
    }

    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s3-agent-replacement-cases",
        "experimentId": "COJC-J3-AIC-AGENT-REPLACEMENT-S3",
        "scenarios": scenarios,
    }
    evidence = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s3-deterministic-preflight",
        "experimentId": result["experimentId"],
        "scenarioCount": len(scenarios),
        "copiedPriorFullHistories": copied,
        "scenarioGates": gates,
        "targetedGates": targeted,
        "mandatoryPass": not copied and all(g["ok"] for g in gates) and all(targeted.values()),
        "casesDigest": sem.digest(result),
    }
    (ROOT / "cases-s3-v1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    (ROOT / "evidence-s3-deterministic.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if evidence["mandatoryPass"] else 2)


if __name__ == "__main__":
    main()
