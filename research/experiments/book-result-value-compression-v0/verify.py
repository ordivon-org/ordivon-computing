#!/usr/bin/env python3
"""Mechanical consistency check for the retained Book Result/Value experiment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(name: str) -> str:
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


primary_frozen = load("frozen-inputs.json")
assert digest("COMPACT-MAP.md") == primary_frozen["compactMap"]["sha256"]
assert digest("cases.json") == primary_frozen["cases"]["sha256"]
assert digest("SPEC.md") == primary_frozen["spec"]["sha256"]
assert primary_frozen["book"]["sha256"] == "10ed267c4b4eb9d90bf8b45c65c73482d40aae2d91e7359cbeedaeac37bf782c"

primary = load("raw-runs.json")["rows"]
baseline = [r for r in primary if r.get("arm") == "BASELINE" and r.get("ok")]
treatment = [r for r in primary if r.get("arm") == "TREATMENT_PREBOOK" and r.get("ok")]
excluded = [r for r in primary if not r.get("ok")]
assert len(baseline) == 5
assert len(treatment) == 5
assert sum(r["score"]["correct"] for r in baseline) == 110
assert sum(r["score"]["correct"] for r in treatment) == 110
assert sum(r["score"]["classificationCorrect"] for r in baseline) == 60
assert sum(r["score"]["classificationCorrect"] for r in treatment) == 60
assert sum(r["score"]["transferCorrect"] for r in baseline) == 50
assert sum(r["score"]["transferCorrect"] for r in treatment) == 50
assert sum(len(r["result"]["weakCases"]) for r in baseline) == 9
assert sum(len(r["result"]["weakCases"]) for r in treatment) == 12
assert len(excluded) == 1
assert excluded[0]["runId"] == "harness-run:book-resultvalue-v3-treatment_prebook-5-1787594363995"
assert excluded[0]["stopCode"] == "budget_exhausted"
assert {r["usage"]["providerUsage"][0]["prompt_tokens"] for r in baseline} == {24054}
assert {r["usage"]["providerUsage"][0]["prompt_tokens"] for r in treatment} == {24830}

follow_frozen = load("followup-frozen-inputs.json")
assert digest("COMPACT-MAP.md") == follow_frozen["compactMapSha256"]
assert digest("composite-cases.json") == follow_frozen["compositeCasesSha256"]
assert digest("FOLLOWUP-SPEC.md") == follow_frozen["followupSpecSha256"]
assert follow_frozen["bookSha256"] == primary_frozen["book"]["sha256"]

follow = load("followup-raw-runs.json")["rows"]
follow_base = [r for r in follow if r.get("arm") == "BASELINE" and r.get("ok")]
follow_treat = [r for r in follow if r.get("arm") == "TREATMENT_PREBOOK" and r.get("ok")]
assert len(follow_base) == 3
assert len(follow_treat) == 3
assert sum(r["score"]["exactCases"] for r in follow_base) == 10
assert sum(r["score"]["exactCases"] for r in follow_treat) == 12
assert sum(r["score"]["labelErrors"] for r in follow_base) == 28
assert sum(r["score"]["labelErrors"] for r in follow_treat) == 14

print(json.dumps({
    "status": "ok",
    "primary": {
        "baseline": {"acceptedRuns": 5, "correct": 110, "total": 110},
        "treatment": {"acceptedRuns": 5, "correct": 110, "total": 110},
        "accuracyDelta": 0,
        "promptTokenOverheadPerRun": 776,
    },
    "followup": {
        "baseline": {"acceptedRuns": 3, "exactCases": 10, "totalCases": 24, "labelErrors": 28},
        "treatment": {"acceptedRuns": 3, "exactCases": 12, "totalCases": 24, "labelErrors": 14},
    },
    "bookMutationAdmitted": False,
}, indent=2))
