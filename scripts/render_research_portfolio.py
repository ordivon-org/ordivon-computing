#!/usr/bin/env python3
"""Render the canonical research portfolio into a reviewable Markdown view."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research" / "portfolio.json"
OUTPUT = ROOT / "research" / "PORTFOLIO.md"


def _cell(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value) or "—"
    text = str(value) if value not in (None, "") else "—"
    return text.replace("|", "\\|").replace("\n", " ")


def _table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(_cell(cell) for cell in row) + " |" for row in rows)
    return lines


def render(document: dict[str, Any]) -> str:
    policy = document["policy"]
    lines: list[str] = [
        "# Ordivon Research Portfolio",
        "",
        "> Generated from [`portfolio.json`](portfolio.json). Edit the JSON source, then rerun `python3 scripts/render_research_portfolio.py`.",
        "",
        f"- **As of:** `{document['asOf']}`",
        f"- **Active research-line limit:** `{policy['activeLineLimit']}`",
        f"- **Current active lines:** `{len(document['activeLines'])}`",
        "",
        "The portfolio is the single source of truth for research status, maturity, blockers, next falsifier, and Ready Frontier. Question pages preserve stable hypotheses and experiment contracts; Issues preserve discussion and execution history.",
        "",
        "## Active research lines",
        "",
    ]
    rows = []
    for line in document["activeLines"]:
        rows.append([line["id"], line["priority"], line["title"], line["questions"], line["issues"], line["exitCriteria"]])
    lines.extend(_table(["Line", "Priority", "Question", "Items", "Implementation", "Exit criterion"], rows))

    lines += ["", "## Question and track portfolio", ""]
    order = policy["allowedStatuses"]
    questions = document["questions"]
    for status in order:
        selected = [item for item in questions if item["status"] == status]
        if not selected:
            continue
        lines += [f"### {status.title()}", ""]
        rows = [
            [
                item["id"],
                item["maturity"],
                item["priority"],
                item["owner"],
                item.get("activeLine", "—"),
                (item.get("externalObservation") or {}).get("revision", "—")[:12],
                item["blockedBy"],
                item["nextAction"],
                item["nextFalsifier"],
            ]
            for item in selected
        ]
        lines.extend(_table(["ID", "Maturity", "Priority", "Owner", "Active line", "Observed revision", "Blocked by", "Next action", "Next falsifier"], rows))
        lines.append("")

    lines += ["## Programs", ""]
    rows = [[p["id"], f"#{p['issue']}", p["kind"], p["status"], p["disposition"], p["nextAction"]] for p in document["programs"]]
    lines.extend(_table(["Program", "Issue", "Kind", "Status", "Disposition", "Next action"], rows))

    lines += ["", "## Studies", ""]
    rows = [[s["id"], s["status"], s["role"], s["nextAction"]] for s in document["studies"]]
    lines.extend(_table(["Study", "Status", "Role", "Next action"], rows))

    lines += ["", "## Evidence maturity", ""]
    for maturity, meaning in policy["maturityLevels"].items():
        lines.append(f"- **{maturity}** — {meaning}.")

    lines += [
        "",
        "## Governance rules",
        "",
        f"- **Promotion:** {policy['promotionRule']}",
        f"- **Judgment:** {policy['judgmentRule']}",
        f"- **New question admission:** {policy['newQuestionRule']}",
        f"- **External observations:** {policy['externalObservationRule']}",
        "- Every completed experiment ends in one of: `retain`, `localize`, `shrink`, `defer`, or `delete`.",
        "- `active` is a WIP state, not a statement of importance. `deferred` preserves a valid question without consuming current execution bandwidth.",
        "- Historical evidence is retained through `completed`, `superseded`, or `frozen`; it does not remain in the Ready Frontier.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = json.loads(SOURCE.read_text(encoding="utf-8"))
    content = render(document)
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else ""
        if current != content:
            print("research/PORTFOLIO.md is not synchronized with portfolio.json")
            return 1
        print("research portfolio view is synchronized")
        return 0
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
