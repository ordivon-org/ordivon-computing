from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def canonical(value: str) -> str:
    text = " ".join(value.strip().replace("`", "").split())
    aliases = {
        "uv run ordivon-studio production-context <production-root> [--source-repo BINDING_ID=PATH]": "uv run ordivon-studio production-context <production-root>",
    }
    return aliases.get(text, text)


def evaluate(trial: dict[str, Any], expected: str) -> dict[str, Any]:
    result = trial.get("result")
    valid = bool(trial.get("resultSchemaValid", result is not None))
    selected = canonical(str(result.get("selectedOperation", ""))) if isinstance(result, dict) else ""
    needs = bool(result.get("needsMoreInfo")) if isinstance(result, dict) else False
    expected = canonical(expected)
    success = valid and selected == expected
    abstain = valid and selected == "" and needs
    return {
        "caseId": trial["caseId"],
        "treatment": trial["treatment"],
        "replicate": trial["replicate"],
        "model": trial["model"],
        "stopCode": trial["stopCode"],
        "schemaValid": valid,
        "selectedOperation": selected,
        "expectedOperation": expected,
        "taskSuccess": success,
        "abstain": abstain,
        "totalTokens": int(trial.get("usage", {}).get("totalTokens", 0) or 0),
        "elapsedMs": trial.get("elapsedMs"),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("campaign")
    p.add_argument("--case-file", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    campaign = json.loads(Path(args.campaign).read_text())
    case_doc = json.loads(Path(args.case_file).read_text())
    expected = {case["caseId"]: case["expectedOperation"] for case in case_doc["cases"]}
    rows = [evaluate(trial, expected[trial["caseId"]]) for trial in campaign["trials"]]
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["caseId"], row["treatment"])].append(row)
    by_case = []
    for (case, treatment), items in sorted(groups.items()):
        by_case.append(
            {
                "caseId": case,
                "treatment": treatment,
                "trials": len(items),
                "schemaValid": sum(x["schemaValid"] for x in items),
                "taskSuccess": sum(x["taskSuccess"] for x in items),
                "abstain": sum(x["abstain"] for x in items),
                "noProgress": sum(x["stopCode"] == "no_progress" for x in items),
                "selections": [x["selectedOperation"] for x in items if x["schemaValid"]],
                "meanTokens": round(sum(x["totalTokens"] for x in items) / len(items), 1),
                "meanElapsedMs": round(sum(int(x["elapsedMs"] or 0) for x in items) / len(items), 1),
            }
        )
    by_treatment = {}
    for treatment in ("raw", "compiled"):
        items = [x for x in rows if x["treatment"] == treatment]
        by_treatment[treatment] = {
            "trials": len(items),
            "schemaValid": sum(x["schemaValid"] for x in items),
            "taskSuccess": sum(x["taskSuccess"] for x in items),
            "abstain": sum(x["abstain"] for x in items),
            "noProgress": sum(x["stopCode"] == "no_progress" for x in items),
            "totalTokens": sum(x["totalTokens"] for x in items),
        }
    out = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.acs-post-implementation-discovery-evaluation",
        "campaign": args.campaign,
        "caseFile": args.case_file,
        "model": campaign["model"],
        "byTreatment": by_treatment,
        "byCase": by_case,
        "trials": rows,
        "interpretationBoundary": (
            "This is next-operation discoverability, not semantic task-completion quality. "
            "Raw packets intentionally represent pre-ACS consumer entry material; compiled packets represent current documented entry material."
        ),
    }
    Path(args.output).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"byTreatment": by_treatment, "byCase": by_case}, indent=2))


if __name__ == "__main__":
    main()
