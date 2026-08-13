from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def run(
    name: str,
    argv: list[str],
    *,
    cwd: pathlib.Path,
    env: dict[str, str] | None = None,
    expected_rc: int = 0,
) -> dict[str, Any]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    started = time.monotonic()
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=merged,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
    )
    elapsed_ms = round((time.monotonic() - started) * 1000)
    record = {
        "name": name,
        "argv": argv,
        "cwd": str(cwd),
        "returnCode": completed.returncode,
        "expectedReturnCode": expected_rc,
        "elapsedMs": elapsed_ms,
        "stdoutDigest": sha256_bytes(completed.stdout),
        "stderrDigest": sha256_bytes(completed.stderr),
        "stdoutBytes": len(completed.stdout),
        "stderrBytes": len(completed.stderr),
        "stdout": completed.stdout.decode("utf-8", errors="replace"),
        "stderr": completed.stderr.decode("utf-8", errors="replace"),
    }
    if completed.returncode != expected_rc:
        raise RuntimeError(json.dumps(record, indent=2, ensure_ascii=False))
    return record


def parse_json(record: dict[str, Any]) -> Any:
    return json.loads(record["stdout"])


def git_status(repo: pathlib.Path) -> str:
    return subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=repo, text=True
    )


def main() -> int:
    repos = {
        "security": pathlib.Path("/root/projects/ordivon-security"),
        "studio": pathlib.Path("/root/projects/ordivon-studio"),
        "finance": pathlib.Path("/root/projects/ordivon-finance"),
        "harness": pathlib.Path("/root/projects/ordivon-harness"),
        "web": pathlib.Path("/root/projects/ordivon-web"),
        "workstation": pathlib.Path("/root/workstation-lab"),
    }
    before = {name: git_status(repo) for name, repo in repos.items()}
    if any(before.values()):
        raise RuntimeError(f"validation requires clean owner repositories: {before}")

    observations: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []

    # Security: existing taxonomy becomes an addressable read-only surface.
    security = run(
        "security-surface",
        [
            str(repos["security"] / ".venv/bin/python"),
            "-m",
            "ordivon_security.cli_surface",
            "--compact",
        ],
        cwd=repos["security"],
        env={"PYTHONPATH": "src"},
    )
    observations.append(security)
    security_value = parse_json(security)
    tiers = {entry["tier"] for entry in security_value["entries"]}
    checks.extend(
        [
            {"id": "security-kind", "pass": security_value["kind"] == "ordivon.security.agent-first-surface"},
            {"id": "security-tier-separation", "pass": tiers == {"constitution", "profile", "integration", "research-apparatus"}},
            {"id": "security-no-authority-invention", "pass": "authority" not in security_value or security_value.get("authority") in (None, [])},
        ]
    )
    observations.append(
        run(
            "security-invalid-arg",
            [str(repos["security"] / ".venv/bin/python"), "-m", "ordivon_security.cli_surface", "--not-a-real-option"],
            cwd=repos["security"],
            env={"PYTHONPATH": "src"},
            expected_rc=2,
        )
    )

    # Studio: one bounded Production context; Git relation never becomes semantic applicability.
    studio = run(
        "studio-production-context",
        [
            str(repos["studio"] / ".venv/bin/python"),
            "-m",
            "ordivon_studio.cli",
            "production-context",
            "productions/runtime-introduction",
            "--source-repo",
            "runtime=/root/projects/ordivon-runtime",
        ],
        cwd=repos["studio"],
        env={"PYTHONPATH": "src"},
    )
    observations.append(studio)
    studio_value = parse_json(studio)
    currentness = studio_value["sourceBindingCurrentness"]
    checks.extend(
        [
            {"id": "studio-derived-truth-role", "pass": studio_value["truthRole"] == "derived-read-only-projection"},
            {"id": "studio-semantic-currentness-not-invented", "pass": currentness["semanticApplicability"] == "not-evaluated"},
            {"id": "studio-escape-hatch", "pass": bool(studio_value.get("escapeHatch", {}).get("productionManifest")) and bool(studio_value.get("escapeHatch", {}).get("claimsManifest"))},
        ]
    )
    observations.append(
        run(
            "studio-unknown-binding-fails-closed",
            [
                str(repos["studio"] / ".venv/bin/python"),
                "-m",
                "ordivon_studio.cli",
                "production-context",
                "productions/runtime-introduction",
                "--source-repo",
                "not-a-binding=/root/projects/ordivon-runtime",
            ],
            cwd=repos["studio"],
            env={"PYTHONPATH": "src"},
            expected_rc=2,
        )
    )

    # Finance: current Agent Context is now the default; no scheduler is introduced.
    finance = run(
        "finance-current-agent-context",
        [
            "./bin/finance-context-compile",
            "goal:primary-capital-allocation",
            "--db",
            "/root/projects/ordivon-finance/state/control/finance.db",
        ],
        cwd=repos["finance"],
        env={"PYTHONPATH": "."},
    )
    observations.append(finance)
    finance_value = parse_json(finance)
    candidate_refs = [
        ref
        for obligation in finance_value.get("obligations", [])
        for ref in obligation.get("candidateOperationRefs", [])
    ]
    checks.extend(
        [
            {"id": "finance-current-context-default", "pass": finance_value.get("schemaVersion") == 15 and finance_value.get("agentSurfaceVersion") == 13},
            {"id": "finance-addressable-operations", "pass": len(finance_value.get("agentOperations", [])) > 0},
            {"id": "finance-candidate-not-scheduler", "pass": len(candidate_refs) > 0 and "selectedOperationRef" not in finance_value and "plan" not in finance_value},
        ]
    )
    with tempfile.TemporaryDirectory(prefix="acs-finance-invalid-") as tmp:
        noncanonical = pathlib.Path(tmp) / "finance.db"
        observations.append(
            run(
                "finance-noncanonical-v15-requires-state-root",
                [
                    str(repos["finance"] / ".venv/bin/python"),
                    "scripts/compile-context.py",
                    "goal:any",
                    "--db",
                    str(noncanonical),
                ],
                cwd=repos["finance"],
                env={"PYTHONPATH": "."},
                expected_rc=2,
            )
        )
        checks.append({"id": "finance-error-before-db-mutation", "pass": not noncanonical.exists()})

    # Harness: compact telemetry is a projection over exact Run evidence.
    harness_state = pathlib.Path("/tmp/ordivon-acs-harness-telemetry-state")
    if harness_state.exists():
        harness = run(
            "harness-telemetry",
            [
                str(repos["harness"] / ".venv/bin/python"),
                "-m",
                "ordivon_harness.cli",
                "--state-root",
                str(harness_state),
                "telemetry",
                "harness-run:acs-telemetry-smoke",
            ],
            cwd=repos["harness"],
            env={"PYTHONPATH": "src"},
        )
        observations.append(harness)
        harness_value = parse_json(harness)
        checks.extend(
            [
                {"id": "harness-derived-telemetry", "pass": harness_value.get("truthRole") == "derived-read-only-projection"},
                {"id": "harness-cache-measurement-only", "pass": harness_value.get("cache", {}).get("policyRole") == "measurement-only"},
                {"id": "harness-inspect-escape-hatch", "pass": "inspect" in harness_value.get("interpretationBoundary", {}).get("escapeHatch", "")},
            ]
        )
        observations.append(
            run(
                "harness-missing-run",
                [
                    str(repos["harness"] / ".venv/bin/python"),
                    "-m",
                    "ordivon_harness.cli",
                    "--state-root",
                    str(harness_state),
                    "telemetry",
                    "harness-run:does-not-exist",
                ],
                cwd=repos["harness"],
                env={"PYTHONPATH": "src"},
                expected_rc=1,
            )
        )
        harness_missing = observations[-1]
        try:
            harness_missing_error = json.loads(harness_missing["stderr"])
        except json.JSONDecodeError:
            harness_missing_error = {}
        checks.append(
            {
                "id": "harness-missing-run-error-is-machine-readable",
                "pass": harness_missing_error.get("ok") is False
                and harness_missing_error.get("error") == "KeyError"
                and "does not exist" in str(harness_missing_error.get("message", "")),
            }
        )
    else:
        checks.append({"id": "harness-live-smoke-state-present", "pass": False})

    # Web: compare only admitted public-source envelopes; semantic applicability remains unevaluated.
    web_currentness = run(
        "web-agent-context-currentness",
        ["/usr/bin/node", "scripts/report-agent-web-currentness.mjs"],
        cwd=repos["web"],
    )
    observations.append(web_currentness)
    web_value = parse_json(web_currentness)
    checks.extend(
        [
            {"id": "web-currentness-truth-role", "pass": web_value.get("truthRole") == "derived-read-only-currentness-projection"},
            {"id": "web-currentness-semantic-boundary", "pass": all(project.get("semanticApplicability") == "not-evaluated" for project in web_value.get("projects", []))},
            {"id": "web-review-not-auto-mutation", "pass": all(project.get("publicationMutationRequired") == "not-evaluated" for project in web_value.get("projects", []))},
        ]
    )
    web_context = run(
        "web-agent-context",
        ["/usr/bin/node", "scripts/report-agent-web-context.mjs"],
        cwd=repos["web"],
    )
    observations.append(web_context)
    web_context_value = parse_json(web_context)
    checks.append(
        {
            "id": "web-captured-snapshot-explicit",
            "pass": web_context_value.get("projectedProjectsTruth", {}).get("truthRole") == "captured-publication-snapshot",
        }
    )
    observations.append(
        run(
            "web-invalid-repo-arg-fails-closed",
            ["/usr/bin/node", "scripts/report-agent-web-currentness.mjs", "--repo", "missing-separator"],
            cwd=repos["web"],
            expected_rc=2,
        )
    )

    # Workstation: observation surface deliberately excludes route/provider selection.
    workstation = run(
        "workstation-network-surface",
        ["/usr/bin/python3", "scripts/network_surface.py"],
        cwd=repos["workstation"],
    )
    observations.append(workstation)
    workstation_value = parse_json(workstation)
    operations = [item["operation"] for item in workstation_value["operations"]]
    boundary = workstation_value["effectBoundary"]
    checks.extend(
        [
            {"id": "workstation-static-consumption-projection", "pass": workstation_value.get("truthRole") == "static-consumption-projection"},
            {"id": "workstation-no-auto-selection", "pass": boundary.get("automaticSelection") is False and not any("select" in operation for operation in operations)},
            {"id": "workstation-no-global-route-mutation", "pass": boundary.get("defaultRouteMutation") is False and boundary.get("systemProxyMutation") is False and boundary.get("tunMutation") is False},
        ]
    )

    after = {name: git_status(repo) for name, repo in repos.items()}
    checks.append({"id": "owner-repositories-stay-clean", "pass": before == after and not any(after.values())})

    passed = sum(bool(check["pass"]) for check in checks)
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.computing.acs-post-implementation-validation",
        "observedAtMs": int(time.time() * 1000),
        "checks": checks,
        "summary": {
            "checks": len(checks),
            "passed": passed,
            "failed": len(checks) - passed,
        },
        "observations": observations,
        "authorityNote": "Derived validation evidence only; owner repositories and live systems remain authoritative.",
    }
    output = EVIDENCE / "post-implementation-validation-v1.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(output), "summary": result["summary"], "digest": sha256_bytes(output.read_bytes())}, indent=2))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
