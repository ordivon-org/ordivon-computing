from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping


def render_markdown(result: Mapping[str, Any]) -> str:
    summary = result["summary"]
    decisions = result["decisions"]
    variants = summary["variants"]
    lines = [
        "# R5 Minimal Adversarial Range Results",
        "",
        f"Source revision: `{result['sourceRevision']}`",
        f"Result digest: `{result['resultDigest']}`",
        "",
        "## Summary",
        "",
        f"- Trials: **{summary['trialCount']}**",
        f"- Passed: **{summary['passed']}**",
        f"- Failed: **{summary['failed']}**",
        f"- Invalid: **{summary['invalid']}**",
        f"- All resets verified: **{str(summary['allResetsVerified']).lower()}**",
        f"- Thin architecture sufficient for R5: **{str(summary['thinArchitectureSufficientForR5']).lower()}**",
        "",
        "## Variant matrix",
        "",
        "| Scenario / variant | Trials | Passed | Failed | Acceptance |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, item in sorted(variants.items()):
        lines.append(
            f"| `{name}` | {item['trialCount']} | {item['passed']} | "
            f"{item['failed']} | {item['acceptanceRate']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Key observations",
            "",
            f"- Model-only open objective successes: **{summary['modelOnlyOpenObjectiveSuccesses']}**",
            f"- Model-only safety-profile objective successes: **{summary['modelOnlySafeObjectiveSuccesses']}**",
            f"- Host provenance/effect-gated objective successes: **{summary['hostGatedObjectiveSuccesses']}**",
            f"- Safety policy changed measured risk: **{str(summary['safetyPolicyChangesMeasuredRisk']).lower()}**",
            "- Safety policy proves universal capability absence: **false**",
            f"- Duplicate Effects in unsafe retry baselines: **{summary['duplicateEffectsAcrossUnsafeBaselines']}**",
            f"- Unauthorized private Effects in parser-differential baseline: **{summary['unauthorizedPrivateEffectsAcrossDifferentialBaselines']}**",
            "",
            "## Architecture disposition",
            "",
            str(decisions["r5Disposition"]),
            "",
            "### Retain",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in decisions["retain"])
    lines.extend(["", "### Localize", ""])
    lines.extend(f"- {item}" for item in decisions["localize"])
    lines.extend(["", "### Do not promote", ""])
    lines.extend(f"- {item}" for item in decisions["doNotPromote"])
    lines.extend(
        [
            "",
            "## Next falsifier",
            "",
            str(decisions["nextFalsifier"]),
            "",
            "## Failure counts",
            "",
        ]
    )
    failure_counts: dict[str, int] = defaultdict(int)
    for trial in result["trials"]:
        for failure in trial["hardFailures"]:
            failure_counts[failure] += 1
    if failure_counts:
        lines.extend(f"- `{name}`: {count}" for name, count in sorted(failure_counts.items()))
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)
