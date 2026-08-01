#!/usr/bin/env python3
"""Validate G3-G7 cases, empirical evidence, and research-local graphs."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

STUDY = Path(__file__).resolve().parents[1]
ROOT = STUDY.parents[1]
DATA = ROOT / "research" / "data" / "ai-capability-governance"
REFERENCE_PATTERN = re.compile(r"\[(G\d{3})\]")
SECRET_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}"),
    re.compile(r"\"apiKey\"\s*:\s*\"[^\"]+\""),
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest_without_result(value: dict[str, Any]) -> str:
    projection = dict(value)
    projection.pop("resultDigest", None)
    return "sha256:" + hashlib.sha256(canonical(projection)).hexdigest()


def require(condition: bool, message: str, issues: list[str]) -> None:
    if not condition:
        issues.append(message)


def load(path: Path, issues: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        issues.append(f"cannot load {path.relative_to(ROOT)}: {error}")
        return None
    if not isinstance(value, dict):
        issues.append(f"root is not an object: {path.relative_to(ROOT)}")
        return None
    return value


def reference_ids(issues: list[str]) -> set[str]:
    text = (STUDY / "REFERENCES.md").read_text(encoding="utf-8")
    defined = set(re.findall(r"^### \[(G\d{3})\]", text, re.MULTILINE))
    require(len(defined) == 68, f"expected 68 references, observed {len(defined)}", issues)
    used: set[str] = set()
    for path in STUDY.rglob("*.md"):
        if path.name == "REFERENCES.md":
            continue
        used.update(REFERENCE_PATTERN.findall(path.read_text(encoding="utf-8")))
    require(not (used - defined), f"undefined references: {sorted(used - defined)}", issues)
    return defined


def check_required_files(issues: list[str]) -> None:
    expected = [
        "30-g3-provider-deep-cases.md",
        "40-g4-comparative-provider-ecology.md",
        "50-g5-state-and-regulatory-interaction.md",
        "60-g6-controlled-empirical-audit.md",
        "70-g7-governance-and-dependency-graphs.md",
        "providers/openai.md",
        "providers/anthropic.md",
        "providers/google.md",
        "providers/xai.md",
        "providers/deepseek.md",
        "providers/kimi.md",
        "providers/meta-open-weight.md",
        "institutions/european-union.md",
        "institutions/united-states.md",
        "institutions/china.md",
        "institutions/canada.md",
        "institutions/compute-cloud-and-export-control.md",
        "experiments/run_deepseek_surface_portability.py",
        "experiments/build_r6_layer_reclassification.py",
        "experiments/build_g7_graphs.py",
    ]
    for relative in expected:
        require((STUDY / relative).is_file(), f"missing study file: {relative}", issues)


def check_json_digest(path: Path, issues: list[str]) -> dict[str, Any] | None:
    value = load(path, issues)
    if value is None:
        return None
    require(value.get("schemaVersion") == 1, f"schemaVersion differs: {path.relative_to(ROOT)}", issues)
    require(value.get("resultDigest") == digest_without_result(value), f"resultDigest differs: {path.relative_to(ROOT)}", issues)
    return value


def check_g6(issues: list[str]) -> None:
    base = DATA / "controlled-observations"
    pilot = check_json_digest(base / "deepseek-surface-portability.json", issues)
    confirm = check_json_digest(base / "deepseek-surface-portability-confirmation.json", issues)
    r6 = check_json_digest(base / "r6-layer-reclassification.json", issues)

    if pilot:
        require(pilot.get("kind") == "ordivon.ai-capability-governance.surface-portability-pilot", "pilot kind differs", issues)
        summary = pilot.get("summary", {})
        require(summary == {"trials": 8, "observed": 7, "errors": 1, "continuityPassed": 7}, f"pilot summary differs: {summary}", issues)
        require(pilot.get("rawPromptsRetained") is False, "pilot retained raw prompts", issues)
        require(pilot.get("rawResponsesRetained") is False, "pilot retained raw responses", issues)
        require(pilot.get("secretRetained") is False, "pilot retained a secret", issues)
        trials = pilot.get("trials", [])
        require(len({item.get("trialId") for item in trials}) == 8, "pilot Trial identities differ", issues)
        errors = [item for item in trials if item.get("status") == "error"]
        require(len(errors) == 1 and errors[0].get("error", {}).get("type") == "IncompleteRead", "pilot error classification differs", issues)

    if confirm:
        require(confirm.get("kind") == "ordivon.ai-capability-governance.surface-portability-confirmation", "confirmation kind differs", issues)
        summary = confirm.get("summary", {})
        require(summary == {"trials": 2, "observed": 2, "errors": 0, "continuityPassed": 2}, f"confirmation summary differs: {summary}", issues)
        require(confirm.get("rawPromptsRetained") is False and confirm.get("rawResponsesRetained") is False, "confirmation retained raw content", issues)
        require(confirm.get("secretRetained") is False, "confirmation retained a secret", issues)

    if r6:
        expected = {
            "formalTrials": 34,
            "providerPolicyInterventionsObservable": 0,
            "unauthorizedProposalsObserved": 8,
            "terminalPreAdmissionDenials": 5,
            "typedPreAdmissionDenials": 2,
            "runtimeUnknown": 1,
            "unauthorizedWorldEffects": 1,
            "attackObjectiveSuccesses": 1,
            "authorizedUtility": 29,
            "hostVerifierAccepted": 25,
            "hostVerifierFalseAccepts": 0,
            "typedDenialRecoveredUtility": 2,
            "hardStopContainedButLostUtility": 5,
        }
        require(r6.get("summary") == expected, f"R6 reclassification summary differs: {r6.get('summary')}", issues)
        observations = r6.get("observations", [])
        require(len(observations) == 34, "R6 reclassification does not contain 34 observations", issues)
        require(len({item.get("observationId") for item in observations}) == 34, "R6 observation identities differ", issues)
        require(r6.get("claimBoundary", {}).get("providerPolicyInterventionObservableFromR6") is False, "R6 overclaims Provider-policy visibility", issues)


def check_case_indexes(defined: set[str], issues: list[str]) -> None:
    provider = check_json_digest(DATA / "provider-cases" / "index.json", issues)
    institution = check_json_digest(DATA / "institutions" / "index.json", issues)
    if provider:
        require(provider.get("caseCount") == 7 and len(provider.get("cases", [])) == 7, "Provider case count differs", issues)
        ids = [item.get("providerId") for item in provider.get("cases", [])]
        require(len(ids) == len(set(ids)), "Provider case identities differ", issues)
        require("no-provider-power-score" in provider.get("prohibitions", []), "Provider index lacks scoring prohibition", issues)
        for item in provider.get("cases", []):
            refs = set(item.get("evidenceRefs", []))
            require(bool(refs) and refs <= defined, f"Provider case evidence differs: {item.get('providerId')}", issues)
    if institution:
        require(institution.get("caseCount") == 5 and len(institution.get("cases", [])) == 5, "institution case count differs", issues)
        ids = [item.get("institutionId") for item in institution.get("cases", [])]
        require(len(ids) == len(set(ids)), "institution case identities differ", issues)
        for item in institution.get("cases", []):
            refs = set(item.get("evidenceRefs", []))
            require(bool(refs) and refs <= defined, f"institution evidence differs: {item.get('institutionId')}", issues)


def check_graph(path: Path, expected_nodes: int, expected_edges: int, defined: set[str], issues: list[str]) -> None:
    value = check_json_digest(path, issues)
    if value is None:
        return
    nodes = value.get("nodes", [])
    edges = value.get("edges", [])
    require(value.get("nodeCount") == expected_nodes == len(nodes), f"node count differs: {path.name}", issues)
    require(value.get("edgeCount") == expected_edges == len(edges), f"edge count differs: {path.name}", issues)
    node_ids = {item.get("nodeId") for item in nodes}
    require(None not in node_ids and len(node_ids) == len(nodes), f"node identities differ: {path.name}", issues)
    edge_ids = [item.get("edgeId") for item in edges]
    require(None not in edge_ids and len(edge_ids) == len(set(edge_ids)), f"edge identities differ: {path.name}", issues)
    for edge in edges:
        source = edge.get("subjectId", edge.get("fromId"))
        target = edge.get("objectId", edge.get("toId"))
        require(source in node_ids, f"unresolved source {source}: {path.name}", issues)
        require(target in node_ids, f"unresolved target {target}: {path.name}", issues)
        refs = set(edge.get("evidenceRefs", []))
        require(bool(refs) and refs <= defined, f"edge evidence differs {edge.get('edgeId')}: {path.name}", issues)
    text = path.read_text(encoding="utf-8").lower()
    require("powerscore" not in text and "power_score" not in text, f"scalar power score found: {path.name}", issues)


def check_secrets(issues: list[str]) -> None:
    roots = (STUDY, DATA)
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".json", ".py"}:
                continue
            text = path.read_text(encoding="utf-8")
            for pattern in SECRET_PATTERNS:
                require(pattern.search(text) is None, f"possible secret in {path.relative_to(ROOT)}", issues)


def main() -> int:
    issues: list[str] = []
    check_required_files(issues)
    defined = reference_ids(issues)
    check_g6(issues)
    check_case_indexes(defined, issues)
    check_graph(DATA / "graphs" / "governance-graph.json", 23, 35, defined, issues)
    check_graph(DATA / "graphs" / "dependency-graph.json", 14, 13, defined, issues)
    check_secrets(issues)
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance-g3-g7-validation",
        "ok": not issues,
        "providerCases": 7,
        "institutionCases": 5,
        "controlledTrials": 44,
        "governanceGraph": {"nodes": 23, "edges": 35},
        "dependencyGraph": {"nodes": 14, "edges": 13},
        "issues": sorted(set(issues)),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
