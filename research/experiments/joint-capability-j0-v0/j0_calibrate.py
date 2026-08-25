#!/usr/bin/env python3
"""Deterministic COJC J0 calibration over already accepted Ordivon evidence.

This script does not infer emergence. It verifies that the programme's classification
rules reproduce one scoped positive interaction (PAL F12) and one non-identifiable
negative candidate (PAL F15) before any new cross-owner experiment is admitted.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
F12 = ROOT / "research/experiments/pal-foundations-v0/f12-results-v0.json"
F15 = ROOT / "research/experiments/pal-foundations-v0/f15-disposition-v0.json"
CONTRACT = ROOT / "research/experiments/joint-capability-j0-v0/experiment-contract.json"
CANDIDATES = ROOT / "research/experiments/joint-capability-j0-v0/candidate-dispositions-v0.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    f12 = load(F12)
    f15 = load(F15)
    contract = load(CONTRACT)
    candidates = load(CANDIDATES)

    interactions = f12.get("interaction", [])
    f12_pattern_ok = bool(interactions) and all(
        x.get("Y00") == 0
        and x.get("Y10") == 0
        and x.get("Y01") == 0
        and x.get("Y11") == 1
        and x.get("binaryInteractionContrast") == 1
        for x in interactions
    )
    f12_scope_ok = (
        f12.get("status") == "completed-scoped-positive"
        and f12.get("interpretation", {}).get("scopedComplementaritySupported") is True
        and f12.get("interpretation", {}).get("broadComplementarityCreditLawSupported") is False
    )

    f15_ok = (
        f15.get("status") == "not-admitted-current-world-nonidentifiable"
        and f15.get("decision", "").startswith("Do not run")
        and "ambient transport already completes" in f15.get("reason", "")
    )

    selected = [
        c["candidateId"]
        for c in candidates.get("candidates", [])
        if c.get("disposition") == "ADMIT_NEXT_DESIGN"
    ]

    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.cojc-j0-calibration-result",
        "experimentId": contract["experimentId"],
        "calibration": {
            "F12": {
                "passed": f12_pattern_ok and f12_scope_ok,
                "classification": "SCOPED_COMPLEMENTARITY" if f12_pattern_ok and f12_scope_ok else "CALIBRATION_FAILURE",
                "emergenceClaimed": False,
            },
            "F15": {
                "passed": f15_ok,
                "classification": "NONIDENTIFIABLE_CURRENT_WORLD" if f15_ok else "CALIBRATION_FAILURE",
                "positiveInteractionManufactured": False,
            },
        },
        "candidateTournament": {
            "selectedForNextDesign": selected,
            "selectionCount": len(selected),
            "source": str(CANDIDATES.relative_to(ROOT)),
        },
        "programmeGuard": {
            "emergenceAdmitted": False,
            "phaseTransitionAdmitted": False,
            "sharedCompositionMachineryAdmitted": False,
        },
    }
    result["passed"] = result["calibration"]["F12"]["passed"] and result["calibration"]["F15"]["passed"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
