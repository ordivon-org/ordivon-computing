from __future__ import annotations

from typing import Any, Mapping


def render_markdown(result: Mapping[str, Any]) -> str:
    summary = result["summary"]
    decisions = result["decisions"]
    lines = [
        "# R6 Real-Model Adversarial Transfer Results",
        "",
        f"Source revision: `{result['sourceRevision']}`",
        f"Host revision: `{result['hostRevision']}`",
        f"Result digest: `{result['resultDigest']}`",
        "",
        "## Summary",
        "",
        f"- Trials: **{summary['trialCount']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Failed: **{summary['failed']}**",
        f"- Infrastructure errors: **{summary['errors']}**",
        f"- Attack objective successes: **{summary['attackObjectiveSuccesses']}**",
        f"- Authorized utility successes: **{summary['authorizedUtility']}**",
        f"- False completion proposals: **{summary['falseCompletions']}**",
        f"- Host verifier false accepts: **{summary['hostVerifierFalseAccepts']}**",
        f"- Utility reached without candidate completion: **{summary['utilityWithoutCandidateCompletion']}**",
        f"- Stop codes: `{summary['stopCodes']}`",
        f"- Completion reason codes: `{summary['completionReasonCodes']}`",
        "",
        "## Model / profile matrix",
        "",
        "| Model / profile | Trials | Passed | Attack success | Utility | False completion | Verifier false accept |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, item in sorted(summary["profiles"].items()):
        lines.append(
            f"| `{name}` | {item['trials']} | {item['passed']} | "
            f"{item['attackObjectiveSuccesses']} | {item['authorizedUtility']} | "
            f"{item['falseCompletions']} | {item['hostVerifierFalseAccepts']} |"
        )
    lines.extend(
        [
            "",
            "## Consequence counts",
            "",
            "| Model / profile | Secret read | Outbox changed | Registry changed | Memory changed | Opaque exec |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for name, item in sorted(summary["profiles"].items()):
        lines.append(
            f"| `{name}` | {item['secretReadObserved']} | {item['outboxChanged']} | "
            f"{item['registryChanged']} | {item['memoryChanged']} | {item['opaqueExecObserved']} |"
        )
    lines.extend(
        [
            "",
            "## Architecture decision",
            "",
            f"- Ambient attack objective successes: **{decisions['ambientAttackObjectiveSuccesses']}**",
            f"- Gated attack objective successes: **{decisions['gatedAttackObjectiveSuccesses']}**",
            f"- Host verifier false accepts: **{decisions['hostVerifierFalseAccepts']}**",
            "",
            "### Retain",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in decisions["retain"])
    lines.extend(["", "### Investigate", ""])
    if decisions["investigate"]:
        lines.extend(f"- {item}" for item in decisions["investigate"])
    else:
        lines.append("- none from this matrix")
    lines.extend(["", "### Do not infer", ""])
    lines.extend(f"- {item}" for item in decisions["doNotInfer"])
    lines.extend(["", "## Next falsifier", "", str(decisions["nextFalsifier"]), ""])
    non_passed = [item for item in result["trials"] if item["status"] != "passed"]
    if non_passed:
        lines.extend(["## Non-pass diagnostics", ""] )
        for item in non_passed:
            detail = item.get("stopDetail") or item.get("error") or "none"
            lines.append(
                f"- `{item['trialId']}`: stop=`{item.get('stopCode')}`, "
                f"completion=`{item.get('completionReasonCode')}`, "
                f"failures=`{item.get('hardFailures')}`, detail={detail}"
            )
        lines.append("")
    errors = [item for item in result["trials"] if item["status"] == "error"]
    if errors:
        lines.extend(["## Infrastructure errors", ""])
        for item in errors:
            lines.append(f"- `{item['trialId']}`: {item['error']}")
        lines.append("")
    return "\n".join(lines)
