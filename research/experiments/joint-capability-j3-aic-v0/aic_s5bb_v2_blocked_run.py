from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ARMS = ["FORCED_LINEARIZATION", "RAW_PARTIAL_ORDER", "BINDING_SET_PROJECTION"]
STOP_PROVIDER = {"provider_rejected", "provider_unavailable"}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


base = load("aic_s5bb_base_v2", ROOT / "aic_s5bb_run.py")


def provider_health(secret: Path, model: str) -> dict[str, Any]:
    cfg = json.loads(secret.read_text())
    url = cfg["baseUrl"].rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply only OK."}],
        "max_tokens": 8,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Authorization": "Bearer " + cfg["apiKey"], "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read(4096).decode("utf-8", errors="replace")
            return {"ok": 200 <= response.status < 300, "httpStatus": response.status, "bodyPrefix": raw[:512]}
    except urllib.error.HTTPError as error:
        raw = error.read(4096).decode("utf-8", errors="replace")
        return {"ok": False, "httpStatus": error.code, "bodyPrefix": raw[:512]}
    except Exception as error:
        return {"ok": False, "httpStatus": None, "errorType": type(error).__name__, "error": str(error)[:512]}


def snapshot(out: Path, payload: dict[str, Any]) -> None:
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--models", default="deepseek-v4-flash,deepseek-v4-pro")
    ap.add_argument("--replicates", type=int, default=2)
    ap.add_argument("--cases", default="all")
    ap.add_argument("--seed", type=int, default=202608261)
    ap.add_argument("--secret", default="/root/.config/ordivon/secrets/deepseek.json")
    args = ap.parse_args()

    secret = Path(args.secret)
    data = json.loads((ROOT / "analysis-s5b-partial-order.json").read_text())
    by = {x["case"]: x for x in data["targeted"]}
    case_ids = list(by) if args.cases == "all" else [x for x in args.cases.split(",") if x]
    models = [x for x in args.models.split(",") if x]
    blocks = [(case_id, model, rep) for model in models for case_id in case_ids for rep in range(1, args.replicates + 1)]
    rng = random.Random(args.seed)
    rng.shuffle(blocks)

    health = {model: provider_health(secret, model) for model in models}
    payload: dict[str, Any] = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.aic-s5bb-v2-blocked-campaign",
        "experimentId": "COJC-J3-AIC-SET-VALUED-CURRENTNESS-S5B-B-V2",
        "scheduleSeed": args.seed,
        "plannedBlocks": len(blocks),
        "plannedCalls": len(blocks) * len(ARMS),
        "healthGate": health,
        "blocks": [],
        "completedBlocks": 0,
        "completeSemanticBlocks": 0,
        "providerInvalidBlocks": 0,
        "campaignStopped": False,
        "stopReason": None,
    }
    out = Path(args.output)
    snapshot(out, payload)

    failed_health = [m for m, h in health.items() if not h.get("ok")]
    if failed_health:
        payload["campaignStopped"] = True
        payload["stopReason"] = "provider_health_gate_failed:" + ",".join(failed_health)
        snapshot(out, payload)
        print(json.dumps({"stopped": True, "reason": payload["stopReason"], "health": health}, ensure_ascii=False), flush=True)
        return

    for block_index, (case_id, model, rep) in enumerate(blocks, 1):
        arm_order = list(ARMS)
        block_rng = random.Random(args.seed ^ (block_index * 1000003))
        block_rng.shuffle(arm_order)
        b: dict[str, Any] = {
            "blockIndex": block_index,
            "case": case_id,
            "model": model,
            "replicate": rep,
            "armOrder": arm_order,
            "rows": [],
            "status": "running",
            "completeForComparison": False,
            "providerInvalid": False,
        }
        payload["blocks"].append(b)
        snapshot(out, payload)

        stop_after_block = False
        for arm in arm_order:
            row = base.run_one(by[case_id], arm, model, rep, secret)
            b["rows"].append(row)
            stop_code = row.get("stopCode")
            print(json.dumps({
                "block": block_index,
                "plannedBlocks": len(blocks),
                "case": case_id,
                "model": model,
                "replicate": rep,
                "arm": arm,
                "valid": row.get("valid"),
                "stopCode": stop_code,
                "safe": row.get("evaluation", {}).get("safeActionCorrect"),
                "multiplicity": row.get("evaluation", {}).get("multiplicityCorrect"),
                "strict": row.get("evaluation", {}).get("strictAccepted"),
                "safetyError": row.get("evaluation", {}).get("safetyError"),
            }, ensure_ascii=False), flush=True)
            if stop_code in STOP_PROVIDER:
                b["providerInvalid"] = True
                b["status"] = "provider-invalid"
                stop_after_block = True
                break

        if not b["providerInvalid"]:
            if len(b["rows"]) == 3 and all(bool(r.get("valid")) for r in b["rows"]):
                b["status"] = "complete"
                b["completeForComparison"] = True
                payload["completeSemanticBlocks"] += 1
            else:
                b["status"] = "semantic-incomplete"
        else:
            payload["providerInvalidBlocks"] += 1

        payload["completedBlocks"] += 1
        snapshot(out, payload)

        if stop_after_block:
            payload["campaignStopped"] = True
            payload["stopReason"] = f"provider_state_changed_at_block:{block_index}:{b['rows'][-1].get('stopCode')}"
            snapshot(out, payload)
            break

        # Small pacing interval between complete blocks; not part of treatment semantics.
        time.sleep(0.35)

    print(json.dumps({
        "completedBlocks": payload["completedBlocks"],
        "plannedBlocks": payload["plannedBlocks"],
        "completeSemanticBlocks": payload["completeSemanticBlocks"],
        "providerInvalidBlocks": payload["providerInvalidBlocks"],
        "campaignStopped": payload["campaignStopped"],
        "stopReason": payload["stopReason"],
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
