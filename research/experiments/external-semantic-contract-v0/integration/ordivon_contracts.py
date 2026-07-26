from __future__ import annotations

from typing import Any, Protocol

from anc_canonical import JsonValue, canonical_digest
from anc_tool_contract import ToolContract, normalize_mcp_tool_contract


class ToolCatalogClient(Protocol):
    def list_tools(self) -> tuple[dict[str, Any], ...]: ...


ORDIVON_SEMANTIC_PROFILES: dict[str, dict[str, JsonValue]] = {
    "workspace.read": {
        "semanticAction": "anc.object.read.v1",
        "execution": "synchronous",
        "completion": "response",
        "effectClass": "observe",
        "idempotencySupport": "natural",
        "correlation": "receipt",
        "cancellation": "unsupported",
        "evidence": ["observation", "version"],
        "capabilityClass": "workspace-file-read",
    },
    "workspace.mutate": {
        "semanticAction": "anc.object.replace-if-version.v1",
        "execution": "synchronous",
        "completion": "response",
        "effectClass": "change",
        "idempotencySupport": "natural",
        "correlation": "receipt",
        "cancellation": "unsupported",
        "evidence": ["observation", "version"],
        "capabilityClass": "workspace-file-mutation",
    },
    "workspace.exec": {
        "semanticAction": "anc.execution.launch.v1",
        "execution": "asynchronous",
        "completion": "terminal-observation",
        "effectClass": "change",
        "idempotencySupport": "keyed",
        "correlation": "stable-key",
        "cancellation": "supported",
        "evidence": ["observation", "artifact"],
        "capabilityClass": "workspace-execution",
    },
    "task.observe": {
        "semanticAction": "anc.execution.observe.v1",
        "execution": "synchronous",
        "completion": "response",
        "effectClass": "observe",
        "idempotencySupport": "natural",
        "correlation": "stable-key",
        "cancellation": "unsupported",
        "evidence": ["observation", "artifact-reference"],
        "capabilityClass": "job-observation",
    },
    "artifact.read": {
        "semanticAction": "anc.artifact.read.v1",
        "execution": "synchronous",
        "completion": "response",
        "effectClass": "observe",
        "idempotencySupport": "natural",
        "correlation": "stable-key",
        "cancellation": "unsupported",
        "evidence": ["artifact-bytes", "artifact-digest"],
        "capabilityClass": "job-artifact-read",
    },
}


def discover_ordivon_contracts(
    client: ToolCatalogClient,
    *,
    operations: tuple[str, ...] = tuple(ORDIVON_SEMANTIC_PROFILES),
) -> dict[str, ToolContract]:
    catalog = {tool.get("name"): tool for tool in client.list_tools()}
    missing = [operation for operation in operations if operation not in catalog]
    if missing:
        raise ValueError(f"Ordivon Tool catalog is missing operations: {missing}")
    selected = [
        {
            "name": catalog[operation]["name"],
            "inputSchema": catalog[operation].get("inputSchema"),
            "outputSchema": catalog[operation].get("outputSchema"),
            "execution": catalog[operation].get("execution"),
        }
        for operation in sorted(operations)
    ]
    revision = "mcp-catalog:" + canonical_digest(selected)[7:]
    return {
        operation: normalize_mcp_tool_contract(
            catalog[operation],
            provider_id="ordivon-runtime",
            revision=revision,
            semantics=ORDIVON_SEMANTIC_PROFILES[operation],
        )
        for operation in operations
    }


def contract_snapshot(contracts: dict[str, ToolContract]) -> dict[str, JsonValue]:
    if not contracts:
        raise ValueError("contract snapshot cannot be empty")
    revisions = {contract.revision for contract in contracts.values()}
    if len(revisions) != 1:
        raise ValueError("one catalog snapshot must use one revision")
    return {
        "schemaVersion": 1,
        "providerId": "ordivon-runtime",
        "catalogRevision": next(iter(revisions)),
        "contracts": {
            operation: contracts[operation].to_dict()
            for operation in sorted(contracts)
        },
    }
