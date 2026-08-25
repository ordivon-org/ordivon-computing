from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("aic_v3", ROOT / "aic_agent_run_v3.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load aic_agent_run_v3.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

EVIDENCE = ROOT / "evidence-s1-v3-live.json"
CASES = ROOT / "cases-v1.json"
SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
SEED = 202608253
MODELS = ["deepseek-v4-flash", "deepseek-v4-pro"]
TREATMENTS = ["RAW_HISTORY", "CURRENT_BINDING_FRONTIER"]
REPLICATES = (1, 2)


def key(row):
    return (row["scenarioId"], row["treatment"], row["model"], int(row["replicate"]))


def main() -> int:
    cases = json.loads(CASES.read_text())
    by_id = {s["scenarioId"]: s for s in cases["scenarios"]}
    scenario_ids = list(by_id)
    schedule = [
        (sid, treatment, model, rep)
        for sid in scenario_ids
        for treatment in TREATMENTS
        for model in MODELS
        for rep in REPLICATES
    ]
    random.Random(SEED).shuffle(schedule)

    campaign = json.loads(EVIDENCE.read_text())
    rows = list(campaign["rows"])
    done = {key(r) for r in rows}
    if len(done) != len(rows):
        raise RuntimeError(f"duplicate recorded slot keys: rows={len(rows)} unique={len(done)}")
    missing = [slot for slot in schedule if slot not in done]
    print(json.dumps({"recorded": len(rows), "missing": len(missing), "missingSlots": missing}, ensure_ascii=False), flush=True)

    for ordinal, (sid, treatment, model, rep) in enumerate(missing, start=1):
        try:
            row = m.run_one(cases, by_id[sid], treatment, model, rep, SECRET)
        except Exception as error:
            row = {
                "scenarioId": sid,
                "split": by_id[sid]["split"],
                "treatment": treatment,
                "model": model,
                "replicate": rep,
                "valid": False,
                "result": None,
                "stopCode": "exception",
                "errorType": type(error).__name__,
                "error": str(error)[:1500],
                "evaluation": {
                    "strictAccepted": False,
                    "responsesCorrect": False,
                    "standingCorrect": False,
                    "safetyError": False,
                    "gates": {},
                    "safetyGates": {},
                },
                "recoveredAfterSupervisorLoss": True,
            }
        else:
            row["recoveredAfterSupervisorLoss"] = True
        rows.append(row)
        done.add(key(row))
        campaign = {
            "schemaVersion": 1,
            "kind": "ordivon.computing.cojc-j3-aic-fresh-agent-campaign-v3",
            "experimentId": "COJC-J3-AIC-CURRENTNESS-V0-S1-V3",
            "casesDigest": m.canonical_digest(cases),
            "scheduleSeed": SEED,
            "plannedTrials": len(schedule),
            "completedTrials": len(rows),
            "recovery": {
                "sourceLostJobId": "job-01a03709-497c-7983-83cc-b1ddcfbad4eb",
                "rule": "append-only missing scheduled tuple identities; recorded slots are never rerun",
            },
            "rows": rows,
            "summary": m.summarize(rows),
        }
        EVIDENCE.write_text(json.dumps(campaign, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(json.dumps({
            "recoveryIndex": ordinal,
            "recoveryTotal": len(missing),
            "completedTrials": len(rows),
            "scenarioId": sid,
            "treatment": treatment,
            "model": model,
            "replicate": rep,
            "valid": row.get("valid"),
            "responses": None if not isinstance(row.get("result"), dict) else row["result"].get("requiredResponses"),
            "strictAccepted": row.get("evaluation", {}).get("strictAccepted"),
            "safetyError": row.get("evaluation", {}).get("safetyError"),
            "error": row.get("error"),
        }, ensure_ascii=False), flush=True)

    final_keys = {key(r) for r in rows}
    absent = [slot for slot in schedule if slot not in final_keys]
    print(json.dumps({"finalRows": len(rows), "uniqueKeys": len(final_keys), "absent": absent}, ensure_ascii=False), flush=True)
    return 0 if len(rows) == len(schedule) and not absent and len(final_keys) == len(schedule) else 2


if __name__ == "__main__":
    raise SystemExit(main())
