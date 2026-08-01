#!/usr/bin/env python3
"""Build research-local G7 governance and dependency graphs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "research" / "data" / "ai-capability-governance"


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def write(path: Path, value: dict[str, Any]) -> None:
    value["resultDigest"] = digest(value)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def provider_cases() -> dict[str, Any]:
    cases = [
        {
            "providerId": "provider:openai",
            "label": "OpenAI",
            "mode": "hosted-administratively-tiered",
            "distribution": ["consumer-chat", "api", "coding-agent", "enterprise"],
            "powerDimensions": ["normative", "observational", "enforcement", "adjudicative", "infrastructural", "epistemic"],
            "capabilityConditions": ["identity", "organization", "approved-use", "model", "surface", "region"],
            "counterPower": ["policy-publication", "support", "appeal", "enterprise-controls", "provider-exit"],
            "evidenceRefs": ["G017", "G018", "G019", "G020", "G026", "G027", "G028"],
            "behaviorEvidence": "limited-r6-g6-not-openai",
        },
        {
            "providerId": "provider:anthropic",
            "label": "Anthropic",
            "mode": "hosted-constitutional-and-tiered",
            "distribution": ["consumer-chat", "api", "enterprise", "cloud-marketplace", "verified-access"],
            "powerDimensions": ["normative", "observational", "enforcement", "adjudicative", "infrastructural", "epistemic"],
            "capabilityConditions": ["organization", "verification", "retention-mode", "surface", "region", "ownership"],
            "counterPower": ["constitution-publication", "versioned-rsp", "appeal", "aggregate-transparency", "provider-exit"],
            "evidenceRefs": ["G021", "G022", "G023", "G024", "G025", "G029", "G030", "G031", "G032", "G033", "G034"],
            "behaviorEvidence": "none-controlled-in-g6",
        },
        {
            "providerId": "provider:google",
            "label": "Google Gemini",
            "mode": "hosted-cloud-project-monitored",
            "distribution": ["api", "ai-studio", "cloud"],
            "powerDimensions": ["normative", "observational", "enforcement", "adjudicative", "infrastructural", "epistemic"],
            "capabilityConditions": ["project", "billing", "region", "safety-setting", "model", "approval"],
            "counterPower": ["operational-monitoring-disclosure", "appeal", "cloud-contract", "provider-exit"],
            "evidenceRefs": ["G035", "G036", "G037", "G038"],
            "behaviorEvidence": "none-controlled-in-g6",
        },
        {
            "providerId": "provider:xai",
            "label": "xAI",
            "mode": "hosted-contractual-discretion",
            "distribution": ["consumer", "enterprise", "api", "x-integration"],
            "powerDimensions": ["normative", "observational", "enforcement", "adjudicative", "infrastructural", "epistemic"],
            "capabilityConditions": ["account", "surface", "feature", "region", "contract"],
            "counterPower": ["published-terms", "support", "provider-exit"],
            "evidenceRefs": ["G039", "G040", "G041", "G042"],
            "behaviorEvidence": "none-controlled-in-g6",
        },
        {
            "providerId": "provider:deepseek",
            "label": "DeepSeek",
            "mode": "hosted-jurisdiction-bound-compatible-api",
            "distribution": ["consumer", "open-platform-api", "openai-compatible", "anthropic-compatible"],
            "powerDimensions": ["normative", "observational", "enforcement", "adjudicative", "infrastructural", "epistemic"],
            "capabilityConditions": ["account", "api", "model", "region", "law"],
            "counterPower": ["published-terms", "api-compatibility", "provider-exit"],
            "evidenceRefs": ["G043", "G044", "G045", "G046", "G067"],
            "behaviorEvidence": "r6-and-g6-controlled",
        },
        {
            "providerId": "provider:kimi",
            "label": "Kimi",
            "mode": "hosted-content-reviewed-api",
            "distribution": ["consumer", "agent", "api", "enterprise"],
            "powerDimensions": ["normative", "observational", "enforcement", "adjudicative", "infrastructural", "epistemic"],
            "capabilityConditions": ["account", "surface", "region", "content-review"],
            "counterPower": ["request-id-support", "api-no-training-claim", "provider-exit"],
            "evidenceRefs": ["G047", "G048", "G049"],
            "behaviorEvidence": "none-controlled-in-g6",
        },
        {
            "providerId": "provider:meta-llama4",
            "label": "Meta Llama 4",
            "mode": "licensed-downloadable-weights",
            "distribution": ["downloadable-weights", "derivatives", "third-party-hosting"],
            "powerDimensions": ["normative", "infrastructural", "epistemic"],
            "capabilityConditions": ["license", "acceptable-use", "trade-law", "region", "scale"],
            "counterPower": ["local-inference", "forkability", "self-hosting", "distributor-substitution"],
            "evidenceRefs": ["G050", "G051", "G052"],
            "behaviorEvidence": "not-executed-in-g6",
        },
    ]
    result = {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance.provider-case-index",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "caseCount": len(cases),
        "cases": cases,
        "prohibitions": ["no-provider-power-score", "no-refusal-leaderboard", "no-inferred-false-positive-rate"],
    }
    return result


def institution_cases() -> dict[str, Any]:
    cases = [
        {
            "institutionId": "jurisdiction:eu",
            "label": "European Union",
            "mode": "comprehensive-risk-and-market-regulation",
            "counterPower": ["documentation", "reason-giving", "audit", "incident-reporting", "regulator-review"],
            "consolidation": ["compliance-cost", "designation", "market-access", "regulatory-information-power"],
            "evidenceRefs": ["G015", "G016", "G053", "G054"],
        },
        {
            "institutionId": "jurisdiction:us",
            "label": "United States",
            "mode": "innovation-infrastructure-national-security",
            "counterPower": ["courts", "sector-regulators", "consumer-protection", "competition", "civil-rights"],
            "consolidation": ["procurement", "classified-use", "export-control", "chip-cloud-partnership", "allied-distribution"],
            "evidenceRefs": ["G055", "G056", "G057"],
        },
        {
            "institutionId": "jurisdiction:china",
            "label": "China",
            "mode": "filing-content-data-and-platform-administration",
            "counterPower": ["public-service-registration", "administrative-publication"],
            "consolidation": ["filing", "security-assessment", "content-duty", "app-store-control", "service-suspension"],
            "evidenceRefs": ["G058", "G059", "G060", "G061"],
        },
        {
            "institutionId": "jurisdiction:canada",
            "label": "Canada",
            "mode": "voluntary-code-public-sector-and-sovereignty",
            "counterPower": ["consultation", "public-register", "privacy", "human-rights", "public-sector-directive"],
            "consolidation": ["procurement", "preferred-infrastructure", "sovereign-supplier-selection"],
            "evidenceRefs": ["G062", "G063", "G064", "G065", "G066"],
        },
        {
            "institutionId": "layer:compute-cloud-export",
            "label": "Compute, cloud, and export-control layer",
            "mode": "infrastructure-chokepoint-governance",
            "counterPower": ["provider-substitution", "local-compute", "open-hardware", "legal-review"],
            "consolidation": ["chip-concentration", "cloud-concentration", "identity-and-sanctions", "recordkeeping", "revocation"],
            "evidenceRefs": ["G006", "G012", "G013", "G055", "G056"],
        },
    ]
    return {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance.institution-case-index",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "caseCount": len(cases),
        "cases": cases,
        "requiredEvaluation": ["counter-power-effect", "consolidation-effect"],
    }


def governance_graph() -> dict[str, Any]:
    nodes = [
        {"nodeId": "actor:user-hosted", "type": "User", "label": "Hosted-service user"},
        {"nodeId": "actor:local-deployer", "type": "Organization", "label": "Local or self-hosted deployer"},
        {"nodeId": "actor:ordivon-host", "type": "ApplicationHost", "label": "Ordivon Host"},
        {"nodeId": "provider:openai", "type": "Provider", "label": "OpenAI"},
        {"nodeId": "provider:anthropic", "type": "Provider", "label": "Anthropic"},
        {"nodeId": "provider:google", "type": "Provider", "label": "Google Gemini"},
        {"nodeId": "provider:xai", "type": "Provider", "label": "xAI"},
        {"nodeId": "provider:deepseek", "type": "Provider", "label": "DeepSeek"},
        {"nodeId": "provider:kimi", "type": "Provider", "label": "Kimi"},
        {"nodeId": "provider:meta-llama4", "type": "ModelDeveloper", "label": "Meta Llama 4 upstream"},
        {"nodeId": "jurisdiction:eu", "type": "Regulator", "label": "European Union institutions"},
        {"nodeId": "jurisdiction:us", "type": "State", "label": "United States federal system"},
        {"nodeId": "jurisdiction:china", "type": "State", "label": "Chinese administrative system"},
        {"nodeId": "jurisdiction:canada", "type": "State", "label": "Canadian federal system"},
        {"nodeId": "layer:cloud-compute", "type": "ComputeProvider", "label": "Cloud and compute layer"},
        {"nodeId": "resource:inference", "type": "InferenceAccess", "label": "Hosted inference capability"},
        {"nodeId": "resource:weights", "type": "ModelWeights", "label": "Downloadable model weights"},
        {"nodeId": "resource:account", "type": "Account", "label": "Provider account / organization tenant"},
        {"nodeId": "resource:data", "type": "RetentionState", "label": "Prompt, response, safety, and account data"},
        {"nodeId": "resource:eligibility", "type": "RegionEligibility", "label": "Identity, region, ownership, and trade eligibility"},
        {"nodeId": "resource:tool-authority", "type": "ToolAuthority", "label": "Tool and external Effect authority"},
        {"nodeId": "resource:appeal", "type": "AppealChannel", "label": "Appeal and review channel"},
        {"nodeId": "resource:task-state", "type": "TaskState", "label": "Durable Task and trace state"},
    ]
    edges: list[dict[str, Any]] = []

    def edge(edge_id: str, subject: str, predicate: str, obj: str, dims: list[str], refs: list[str], claim: str, confidence: str = "high") -> None:
        edges.append({
            "edgeId": edge_id,
            "subjectId": subject,
            "predicate": predicate,
            "objectId": obj,
            "powerDimensions": dims,
            "evidenceRefs": refs,
            "claimClass": "D",
            "confidence": confidence,
            "claim": claim,
        })

    providers = [
        ("provider:openai", ["G017", "G018", "G019", "G020"]),
        ("provider:anthropic", ["G021", "G022", "G023", "G024", "G025"]),
        ("provider:google", ["G035", "G036", "G037"]),
        ("provider:xai", ["G039", "G040", "G041"]),
        ("provider:deepseek", ["G043", "G044", "G045"]),
        ("provider:kimi", ["G047", "G048", "G049"]),
    ]
    for index, (provider, refs) in enumerate(providers, start=1):
        edge(f"g{index:02d}", provider, "defines", "resource:inference", ["normative", "epistemic"], refs, "Provider defines hosted capability and allowed-use conditions.")
        edge(f"g{index+10:02d}", provider, "observes", "resource:data", ["observational"], refs, "Provider may process or retain request/account data under surface-specific terms.")
        edge(f"g{index+20:02d}", provider, "restricts", "resource:account", ["enforcement", "infrastructural"], refs, "Provider can limit or terminate hosted account or service access.")
        edge(f"g{index+30:02d}", provider, "reviews", "resource:appeal", ["adjudicative"], refs, "Provider operates the first-instance support or appeal channel.")

    edge("g50", "provider:meta-llama4", "licenses", "resource:weights", ["normative", "infrastructural"], ["G050", "G051"], "Meta grants downloadable-weight rights under a private community license and AUP.")
    edge("g51", "actor:local-deployer", "controls", "resource:tool-authority", ["enforcement", "infrastructural"], ["G050", "G052"], "A local deployer selects the execution and Tool boundary after lawful acquisition.")
    edge("g52", "actor:ordivon-host", "controls", "resource:task-state", ["infrastructural"], ["G067"], "G6 preserves caller/Host-owned history rather than Provider-hidden conversation state.")
    edge("g53", "actor:ordivon-host", "restricts", "resource:tool-authority", ["enforcement", "infrastructural"], ["G068"], "R6 ToolGrant prevents unauthorized owned-world Effects after model proposals.")
    edge("g60", "jurisdiction:eu", "regulates", "resource:inference", ["normative", "adjudicative"], ["G015", "G016", "G053", "G054"], "EU law imposes GPAI and platform duties and external review.")
    edge("g61", "jurisdiction:us", "conditions", "resource:eligibility", ["normative", "infrastructural"], ["G055", "G056", "G057"], "US policy links AI capability to infrastructure, procurement, national security, and international distribution.")
    edge("g62", "jurisdiction:china", "conditions", "resource:eligibility", ["normative", "enforcement", "infrastructural"], ["G058", "G059", "G060", "G061"], "Chinese filing, content, data, and platform rules condition public service operation.")
    edge("g63", "jurisdiction:canada", "regulates", "resource:inference", ["normative", "adjudicative"], ["G062", "G063", "G064", "G065", "G066"], "Canada combines voluntary commitments, public-sector controls, privacy, and sovereignty policy.")
    edge("g64", "layer:cloud-compute", "conditions", "resource:inference", ["infrastructural", "observational", "enforcement"], ["G012", "G013"], "Compute and cloud operators can make capability detectable, excludable, recordable, and revocable.")
    edge("g65", "jurisdiction:us", "regulates", "layer:cloud-compute", ["normative", "infrastructural"], ["G055", "G056"], "Export and national-security policy use infrastructure firms as capability-distribution points.")
    edge("g66", "actor:user-hosted", "appeals_to", "resource:appeal", ["adjudicative"], ["G017", "G025", "G035", "G049"], "Hosted users may use Provider-operated support or appeal channels of varying specificity.", "medium")

    return {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance.governance-graph",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "question": "Who can decide what about whom, under which rule and review?",
        "nodeCount": len(nodes),
        "edgeCount": len(edges),
        "nodes": nodes,
        "edges": edges,
        "prohibitions": ["no-power-score", "no-central-policy-engine", "no-user-risk-score"],
    }


def dependency_graph() -> dict[str, Any]:
    nodes = [
        {"nodeId": "actor:user-hosted", "type": "actor", "label": "Hosted-service user"},
        {"nodeId": "actor:ordivon-host", "type": "actor", "label": "Ordivon Host"},
        {"nodeId": "actor:local-deployer", "type": "actor", "label": "Local deployer"},
        {"nodeId": "provider:hosted", "type": "provider-class", "label": "Hosted model Provider"},
        {"nodeId": "provider:open-weight-upstream", "type": "provider-class", "label": "Open-weight upstream developer"},
        {"nodeId": "layer:cloud", "type": "infrastructure", "label": "Cloud or datacentre"},
        {"nodeId": "layer:accelerator", "type": "infrastructure", "label": "Accelerator and memory supply"},
        {"nodeId": "layer:identity-payment", "type": "infrastructure", "label": "Identity, billing, sanctions and trade eligibility"},
        {"nodeId": "resource:inference", "type": "resource", "label": "Inference capability"},
        {"nodeId": "resource:weights", "type": "resource", "label": "Model weights"},
        {"nodeId": "resource:task-state", "type": "resource", "label": "Task, Context, Tool and trace state"},
        {"nodeId": "resource:tool-authority", "type": "resource", "label": "Tool and World Effect authority"},
        {"nodeId": "resource:compute", "type": "resource", "label": "Compute capacity"},
        {"nodeId": "resource:provider-trust", "type": "resource", "label": "Provider-specific account and access tier"},
    ]
    edges = [
        {
            "edgeId": "d01",
            "fromId": "actor:user-hosted",
            "toId": "provider:hosted",
            "dependency": "account-and-service-access",
            "substitutability": "partial",
            "switchingCost": "medium-to-high",
            "privateStateAtRisk": ["conversation", "account-trust", "billing", "integrations"],
            "evidenceRefs": ["G017", "G023", "G035", "G040", "G043", "G047"],
        },
        {
            "edgeId": "d02",
            "fromId": "provider:hosted",
            "toId": "resource:inference",
            "dependency": "supplies-and-can-revoke",
            "substitutability": "partial",
            "switchingCost": "model-and-surface-dependent",
            "privateStateAtRisk": ["model-availability", "routing", "access-tier"],
            "evidenceRefs": ["G020", "G022", "G035", "G039"],
        },
        {
            "edgeId": "d03",
            "fromId": "provider:hosted",
            "toId": "layer:cloud",
            "dependency": "training-and-inference-infrastructure",
            "substitutability": "partial",
            "switchingCost": "high-at-frontier-scale",
            "privateStateAtRisk": ["deployment", "capacity", "telemetry"],
            "evidenceRefs": ["G012", "G013"],
        },
        {
            "edgeId": "d04",
            "fromId": "layer:cloud",
            "toId": "layer:accelerator",
            "dependency": "hardware-capacity",
            "substitutability": "limited",
            "switchingCost": "high",
            "privateStateAtRisk": ["capacity", "performance", "supply"],
            "evidenceRefs": ["G012", "G013"],
        },
        {
            "edgeId": "d05",
            "fromId": "provider:hosted",
            "toId": "layer:identity-payment",
            "dependency": "eligibility-and-billing",
            "substitutability": "partial",
            "switchingCost": "jurisdiction-dependent",
            "privateStateAtRisk": ["account", "organization", "region", "ownership", "sanctions"],
            "evidenceRefs": ["G020", "G033", "G036", "G039", "G044"],
        },
        {
            "edgeId": "d06",
            "fromId": "actor:ordivon-host",
            "toId": "provider:hosted",
            "dependency": "current-cognition-supplier",
            "substitutability": "partial",
            "switchingCost": "reduced-by-adapter-and-caller-state",
            "privateStateAtRisk": ["provider-specific-tool-semantics", "model-quality", "access-tier"],
            "evidenceRefs": ["G046", "G067", "G068"],
        },
        {
            "edgeId": "d07",
            "fromId": "actor:ordivon-host",
            "toId": "resource:task-state",
            "dependency": "owns-durable-state",
            "substitutability": "full-with-evidence-preserved",
            "switchingCost": "low-to-medium",
            "privateStateAtRisk": [],
            "evidenceRefs": ["G067", "G068"],
        },
        {
            "edgeId": "d08",
            "fromId": "actor:ordivon-host",
            "toId": "resource:tool-authority",
            "dependency": "owns-authority-boundary",
            "substitutability": "host-local",
            "switchingCost": "low-when-contract-bound",
            "privateStateAtRisk": [],
            "evidenceRefs": ["G068"],
        },
        {
            "edgeId": "d09",
            "fromId": "actor:local-deployer",
            "toId": "provider:open-weight-upstream",
            "dependency": "weight-and-license-source",
            "substitutability": "partial",
            "switchingCost": "model-and-license-dependent",
            "privateStateAtRisk": ["updates", "provenance", "license-rights"],
            "evidenceRefs": ["G050", "G051", "G052"],
        },
        {
            "edgeId": "d10",
            "fromId": "actor:local-deployer",
            "toId": "resource:weights",
            "dependency": "possesses-local-copy",
            "substitutability": "high-after-lawful-download",
            "switchingCost": "storage-and-conversion-dependent",
            "privateStateAtRisk": [],
            "evidenceRefs": ["G050", "G052"],
        },
        {
            "edgeId": "d11",
            "fromId": "actor:local-deployer",
            "toId": "resource:compute",
            "dependency": "local-inference-and-fine-tuning",
            "substitutability": "partial",
            "switchingCost": "capability-dependent",
            "privateStateAtRisk": ["performance", "capacity", "operations"],
            "evidenceRefs": ["G012", "G013", "G050"],
        },
        {
            "edgeId": "d12",
            "fromId": "resource:compute",
            "toId": "layer:accelerator",
            "dependency": "hardware-supply",
            "substitutability": "limited-at-high-capability",
            "switchingCost": "high",
            "privateStateAtRisk": ["availability", "performance"],
            "evidenceRefs": ["G012", "G013"],
        },
        {
            "edgeId": "d13",
            "fromId": "actor:user-hosted",
            "toId": "resource:provider-trust",
            "dependency": "identity-and-access-history",
            "substitutability": "not-portable",
            "switchingCost": "high-for-verified-capability",
            "privateStateAtRisk": ["verification", "reputation", "organization-approval"],
            "evidenceRefs": ["G020", "G028", "G033"],
        },
    ]
    return {
        "schemaVersion": 1,
        "kind": "ordivon.ai-capability-governance.dependency-graph",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "question": "Who cannot continue without which resource, and at what switching cost?",
        "nodeCount": len(nodes),
        "edgeCount": len(edges),
        "nodes": nodes,
        "edges": edges,
        "prohibitions": ["no-market-share-proxy-for-dependency", "no-power-score", "no-assumed-zero-cost-exit"],
    }


def main() -> int:
    outputs = {
        DATA / "provider-cases" / "index.json": provider_cases(),
        DATA / "institutions" / "index.json": institution_cases(),
        DATA / "graphs" / "governance-graph.json": governance_graph(),
        DATA / "graphs" / "dependency-graph.json": dependency_graph(),
    }
    for path, value in outputs.items():
        write(path, value)
        print(path.relative_to(ROOT), value.get("caseCount", value.get("edgeCount")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
