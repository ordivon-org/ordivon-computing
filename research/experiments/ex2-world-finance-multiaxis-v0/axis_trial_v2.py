from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random

from axis_trial import CORPUS, ROOT, analyze, call_provider, digest, score_trial, secret_paths


def persist(path: pathlib.Path, trials: list[dict], complete: bool) -> None:
    document = {
        "schemaVersion": 1,
        "kind": "ordivon.explanation-ex2-five-axis-live-evidence",
        "apparatusVersion": 2,
        "complete": complete,
        "corpusDigest": digest(CORPUS),
        "authorityFreezeDigest": "sha256:" + hashlib.sha256((ROOT / "authority-freeze-v1.json").read_bytes()).hexdigest(),
        "trialCount": len(trials),
        "trials": trials,
    }
    if complete:
        document["analysis"] = analyze(trials)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "evidence" / "axis-live-v2.json")
    args = parser.parse_args()
    trials: list[dict] = []
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if existing.get("corpusDigest") != digest(CORPUS):
            raise RuntimeError("existing evidence corpus digest differs")
        trials = list(existing.get("trials", []))
    done = {(int(t["replicate"]), str(t["treatment"])) for t in trials}
    secrets = secret_paths()
    for replicate in range(1, int(CORPUS["replicates"]) + 1):
        secret_path = secrets[(replicate - 1) % len(secrets)]
        secret = json.loads(secret_path.read_text(encoding="utf-8"))
        order = ["compact_responsibility", "explicit_five_axis"] if replicate % 2 else ["explicit_five_axis", "compact_responsibility"]
        for treatment in order:
            if (replicate, treatment) in done:
                continue
            cases = list(CORPUS["cases"])
            random.Random(f"ex2-axis:{replicate}:{treatment}").shuffle(cases)
            result, usage = call_provider(secret, treatment, cases)
            trial = score_trial(treatment, replicate, cases, result, usage, secret_path.name)
            trials.append(trial)
            persist(args.output, trials, complete=False)
            print(json.dumps({
                "replicate": replicate,
                "treatment": treatment,
                "axisCorrect": trial["axisCorrect"],
                "axisTotal": trial["axisTotal"],
                "caseExact": trial["caseExact"],
                "caseTotal": trial["caseTotal"],
                "tokens": usage["totalTokens"],
                "calls": usage["providerCalls"],
                "checkpointedTrials": len(trials),
            }, sort_keys=True), flush=True)
    expected = int(CORPUS["replicates"]) * len(CORPUS["treatments"])
    if len(trials) != expected:
        persist(args.output, trials, complete=False)
        raise RuntimeError(f"incomplete evidence: {len(trials)} != {expected}")
    persist(args.output, trials, complete=True)
    final = json.loads(args.output.read_text(encoding="utf-8"))
    print(json.dumps(final["analysis"], sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
