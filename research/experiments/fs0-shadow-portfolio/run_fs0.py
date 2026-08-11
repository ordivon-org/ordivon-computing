from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
COHORT = ROOT / "cohort-v1.json"
SECRET = Path("/root/.config/ordivon/secrets/deepseek.json")
CANDIDATES = ["H-P6", "R-P5", "G-AF3", "HOST-PKG", "F-C2-BLOCKED"]

RFM_PRIORS = [
    "Tractability is conditional on current evidence topology, available operator policy, verification path, authority/recovery constraints and budget; it is not an intrinsic scalar property of the question.",
    "Prefer evidence or experiments likely to change the research frontier over activity that merely produces more observations.",
    "A strong simpler/classical baseline must be considered before an adaptive Agent loop; adaptive-selection overhead and semantic path dependence are real costs.",
    "Current admission matters: a high-value direction whose required authority/resource does not exist may deserve DEFER rather than immediate budget.",
    "Topology labels are revisable hypotheses; exact/local-looking cues can hide distributed causes and large/distributed surfaces can still reduce to a local defect.",
    "Owner-native truth and authority remain with the owner. Do not select work merely because another layer could conveniently centralize it.",
    "No-change, abstention or deferral can be correct when current evidence cannot justify a closable experiment.",
]


def load_secret() -> dict[str, Any]:
    return json.loads(SECRET.read_text())


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def tool() -> list[dict[str, Any]]:
    assessment = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "enum": CANDIDATES},
            "topologyHypothesis": {"type": "string"},
            "operatorPolicy": {"type": "string"},
            "predictedFrontierDelta": {"type": "string", "enum": ["no-op", "ambiguity-reduction", "defect-discovery", "owner-mechanism-change", "prior-narrowing", "prior-generalization", "new-capability"]},
            "dominantCost": {"type": "string"},
            "closureRisk": {"type": "string"},
            "whyNotFirst": {"type": "string"}
        },
        "required": ["id", "topologyHypothesis", "operatorPolicy", "predictedFrontierDelta", "dominantCost", "closureRisk", "whyNotFirst"],
        "additionalProperties": False
    }
    return [{
        "type": "function",
        "function": {
            "name": "submit_shadow_portfolio",
            "description": "Freeze a shadow research-portfolio choice. This has no authority over owner tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nextBudgetChoice": {"type": "string", "enum": CANDIDATES},
                    "ranking": {"type": "array", "items": {"type": "string", "enum": CANDIDATES}, "minItems": 5, "maxItems": 5},
                    "deferNow": {"type": "array", "items": {"type": "string", "enum": CANDIDATES}},
                    "choiceRationale": {"type": "string"},
                    "predictedDiscriminator": {"type": "string"},
                    "selectionFalsifier": {"type": "string"},
                    "assessments": {"type": "array", "items": assessment, "minItems": 5, "maxItems": 5}
                },
                "required": ["nextBudgetChoice", "ranking", "deferNow", "choiceRationale", "predictedDiscriminator", "selectionFalsifier", "assessments"],
                "additionalProperties": False
            }
        }
    }]


def call_model(treatment: str, cohort: dict[str, Any], replicate: int) -> dict[str, Any]:
    secret = load_secret()
    system = (
        "You are a shadow research-portfolio selector. You have no authority over the owner tasks. "
        "Assume only one additional unit of research budget can be allocated now. Rank all frozen candidates by current expected research value and closability, not project importance. "
        "Do not use a universal scalar score. A blocked or non-closable problem may be deferred. Use only the supplied frozen cards; do not assume later outcomes."
    )
    payload: dict[str, Any] = {
        "replicate": replicate,
        "treatment": treatment,
        "portfolioQuestion": "If exactly one current owner pressure receives the next additional unit of research budget, which should it be?",
        "frontierValueSemantics": ["no-op", "ambiguity-reduction", "defect-discovery", "owner-mechanism-change", "prior-narrowing", "prior-generalization", "new-capability"],
        "candidates": cohort["primaryCandidates"],
    }
    if treatment == "rfm":
        payload["researchFrontierPriors"] = RFM_PRIORS
    body = {
        "model": secret["model"],
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}
        ],
        "tools": tool(),
        "tool_choice": "required",
        "thinking": {"type": "disabled"},
        "temperature": 0.35,
        "max_tokens": 5000,
        "stream": False
    }
    encoded = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
    retries = 0
    started = time.time_ns()
    while True:
        request = urllib.request.Request(
            str(secret["baseUrl"]).rstrip("/") + "/chat/completions",
            data=encoded,
            headers={"Authorization": "Bearer " + str(secret["apiKey"]), "Content-Type": "application/json", "User-Agent": "ordivon-computing-fs0/1"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                raw = response.read(4_194_304)
            break
        except urllib.error.HTTPError as error:
            detail = error.read(4096).decode(errors="replace")
            raise RuntimeError(f"Provider HTTP {error.code}: {detail}") from error
        except (http.client.HTTPException, urllib.error.URLError, TimeoutError, OSError):
            if retries >= 1:
                raise
            retries += 1
            time.sleep(0.5)
    response = json.loads(raw)
    message = response["choices"][0]["message"]
    calls = message.get("tool_calls")
    if not isinstance(calls, list) or not calls:
        raise ValueError("no tool call")
    call = calls[0]
    function = call.get("function")
    if not isinstance(function, dict) or function.get("name") != "submit_shadow_portfolio":
        raise ValueError("unexpected tool")
    result = json.loads(function["arguments"])
    ranking = result.get("ranking")
    if not isinstance(ranking, list) or len(ranking) != 5 or set(ranking) != set(CANDIDATES):
        raise ValueError("ranking must contain every candidate exactly once")
    assessments = result.get("assessments")
    if not isinstance(assessments, list) or {item.get("id") for item in assessments if isinstance(item, dict)} != set(CANDIDATES):
        raise ValueError("assessments must contain every candidate exactly once")
    usage = response.get("usage", {})
    return {
        "treatment": treatment,
        "replicate": replicate,
        "result": result,
        "usage": {
            "inputTokens": int(usage.get("prompt_tokens", 0) or 0),
            "outputTokens": int(usage.get("completion_tokens", 0) or 0),
            "totalTokens": int(usage.get("total_tokens", 0) or 0),
            "elapsedMs": (time.time_ns() - started) // 1_000_000,
            "transportRetries": retries,
        }
    }


def load_or_run(path: Path, treatment: str, replicate: int, cohort: dict[str, Any]) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text())
    record = call_model(treatment, cohort, replicate)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    tmp.replace(path)
    return record


def aggregate(trials: list[dict[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for treatment in ("raw", "rfm"):
        group = [trial for trial in trials if trial["treatment"] == treatment]
        top_counts = {candidate: sum(trial["result"]["nextBudgetChoice"] == candidate for trial in group) for candidate in CANDIDATES}
        defer_counts = {candidate: sum(candidate in trial["result"]["deferNow"] for trial in group) for candidate in CANDIDATES}
        rank_sums = {candidate: sum(trial["result"]["ranking"].index(candidate) + 1 for trial in group) for candidate in CANDIDATES}
        out[treatment] = {
            "replicates": len(group),
            "topChoiceCounts": top_counts,
            "deferCounts": defer_counts,
            "meanRank": {candidate: rank_sums[candidate] / len(group) for candidate in CANDIDATES},
            "negativeControlTopChoices": top_counts["F-C2-BLOCKED"],
            "negativeControlDeferrals": defer_counts["F-C2-BLOCKED"],
            "totalTokens": sum(trial["usage"]["totalTokens"] for trial in group),
            "totalElapsedMs": sum(trial["usage"]["elapsedMs"] for trial in group),
        }
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=5)
    parser.add_argument("--output", type=Path, default=ROOT / "evidence" / "fs0-predictions-v1.json")
    args = parser.parse_args()
    cohort = json.loads(COHORT.read_text())
    progress = args.output.parent / (args.output.stem + "-progress")
    trials: list[dict[str, Any]] = []
    for treatment in ("raw", "rfm"):
        for replicate in range(1, args.replicates + 1):
            path = progress / f"{treatment}-r{replicate}.json"
            trials.append(load_or_run(path, treatment, replicate, cohort))
    receipt = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.fs0-shadow-portfolio-predictions",
        "status": "prediction-freeze",
        "shadowOnly": True,
        "cohortDigest": digest(cohort),
        "provider": "deepseek",
        "model": load_secret()["model"],
        "replicatesPerTreatment": args.replicates,
        "trials": trials,
        "aggregate": aggregate(trials),
    }
    receipt["receiptDigest"] = digest(receipt)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"aggregate": receipt["aggregate"], "receiptDigest": receipt["receiptDigest"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
