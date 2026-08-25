from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cojc_j1_base", ROOT / "j1_run.py")
assert SPEC is not None and SPEC.loader is not None
base = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(base)


def neutralize(raw: dict) -> dict:
    out = json.loads(json.dumps(raw))
    for index, scenario in enumerate(out["scenarios"], start=1):
        scenario["scenarioId"] = f"J1-N{index}"
        scenario["description"] = "Frozen Security evidence packet at one scenario cut. Decide the current receiver binding for one new maintenance probe."

        id_map: dict[str, str] = {}
        plane_count: dict[str, int] = {}
        for evidence_index, evidence in enumerate(scenario["rawEvidence"], start=1):
            old = evidence["evidenceId"]
            new = f"E{evidence_index:02d}"
            id_map[old] = new
            evidence["evidenceId"] = new
            plane = evidence["plane"]
            plane_count[plane] = plane_count.get(plane, 0) + 1
            role = {
                "world-truth": "security-world-source",
                "management": "security-management-source",
                "sensor": "security-sensor-source",
                "contested": "contested-actor-source",
            }[plane]
            evidence["source"] = f"{role}:{plane_count[plane]}"

        projection = scenario["interlocusProjection"]
        migration = projection.get("migration", {})
        migration["witnesses"] = [id_map.get(x, x) for x in migration.get("witnesses", [])]
        for assignment in projection.get("evidenceAssignments", []):
            assignment["evidenceId"] = id_map.get(assignment["evidenceId"], assignment["evidenceId"])

        # Remove theory-bearing labels from raw case identity only. The treatment
        # still carries the exact Interlocus relation projection being tested.
        # The adversarial claim content and Security plane semantics are unchanged.
    out["experimentId"] = raw["experimentId"] + "-NEUTRAL-LABEL-ROBUSTNESS"
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    parser.add_argument("--models", default="deepseek-v4-flash,deepseek-v4-pro")
    parser.add_argument("--replicates", type=int, default=2)
    args = parser.parse_args()

    raw = json.loads((ROOT / "battlefield-v1.json").read_text())
    battlefield = neutralize(raw)
    neutral_path = ROOT / "battlefield-neutral-v1.json"
    neutral_path.write_text(json.dumps(battlefield, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    models = [x for x in args.models.split(",") if x]
    treatments = ["SECURITY_CONTROL", "INTERLOCUS_QUALIFIED"]
    scenario_ids = [s["scenarioId"] for s in battlefield["scenarios"]]
    scenarios = {s["scenarioId"]: s for s in battlefield["scenarios"]}
    schedule = [
        (sid, treatment, model, rep)
        for sid in scenario_ids
        for treatment in treatments
        for model in models
        for rep in range(1, args.replicates + 1)
    ]
    random.Random(20260825_2).shuffle(schedule)

    rows: list[dict] = []
    output = Path(args.output)
    for index, (sid, treatment, model, rep) in enumerate(schedule, start=1):
        scenario = scenarios[sid]
        try:
            row = base.run_one(battlefield, scenario, treatment, model, rep, Path(args.secret))
        except Exception as error:
            row = {
                "scenarioId": sid,
                "treatment": treatment,
                "model": model,
                "replicate": rep,
                "valid": False,
                "result": None,
                "stopCode": "exception",
                "errorType": type(error).__name__,
                "error": str(error)[:1000],
                "evaluation": {"strictAccepted": False, "safetyError": False, "unnecessaryHold": False, "gates": {}},
            }
        rows.append(row)
        campaign = {
            "schemaVersion": 1,
            "kind": "ordivon.computing.cojc-j1-neutral-label-robustness",
            "experimentId": battlefield["experimentId"],
            "battlefieldDigest": base.canonical_digest(battlefield),
            "rawBattlefieldDigest": base.canonical_digest(raw),
            "neutralization": {
                "scenarioNames": "J1-N1..J1-N4",
                "descriptions": "neutral",
                "evidenceIds": "E01..",
                "sourceNames": "plane-role-only",
                "securityPlaneSemanticsChanged": False,
                "claimValuesChanged": False,
                "interlocusTreatmentProjectionChangedSemantically": False,
            },
            "scheduleSeed": 202608252,
            "plannedTrials": len(schedule),
            "completedTrials": len(rows),
            "rows": rows,
            "summary": base.summarize(rows),
        }
        output.write_text(json.dumps(campaign, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(json.dumps({
            "index": index,
            "total": len(schedule),
            "scenarioId": sid,
            "treatment": treatment,
            "model": model,
            "replicate": rep,
            "valid": row["valid"],
            "decision": None if not isinstance(row.get("result"), dict) else row["result"].get("decision"),
            "strictAccepted": row.get("evaluation", {}).get("strictAccepted"),
            "safetyError": row.get("evaluation", {}).get("safetyError"),
            "error": row.get("error"),
        }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
