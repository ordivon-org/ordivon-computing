from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from typing import Any

from anc_semantic_core.transport import ToolProtocolError, ToolRejected, ToolTransportError


class LocalMcpToolCaller:
    """Test-only local MCP caller; not a production transport implementation."""

    def __init__(self, endpoint: str, token: str) -> None:
        self.endpoint = endpoint
        self.token = token
        self.request_id = 100
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def initialize(self) -> dict[str, Any]:
        result = self._rpc(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {
                    "name": "anc-semantic-core-live",
                    "version": "0.1.0",
                },
            },
        )
        if not isinstance(result, dict):
            raise ToolProtocolError("initialize returned a non-object result")
        return result

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((name, arguments))
        result = self._rpc(
            "tools/call",
            {"name": name, "arguments": arguments},
        )
        if not isinstance(result, dict):
            raise ToolProtocolError(f"Tool {name} returned a non-object result")
        structured = result.get("structuredContent")
        if result.get("isError") is True:
            detail = structured.get("error") if isinstance(structured, dict) else None
            if not isinstance(detail, dict):
                raise ToolProtocolError(f"unstructured Tool error from {name}")
            raise ToolRejected(
                name,
                code=str(detail.get("code", "TOOL_ERROR")),
                message=str(detail.get("message", "tool failed")),
                field=detail.get("field") if isinstance(detail.get("field"), str) else None,
                retryable=detail.get("retryable") is True,
                detail=detail,
            )
        if not isinstance(structured, dict):
            raise ToolProtocolError(f"Tool {name} returned no structuredContent")
        return structured

    def _rpc(self, method: str, params: dict[str, Any]) -> Any:
        self.request_id += 1
        body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": self.request_id,
                "method": method,
                "params": params,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = response.read()
        except urllib.error.HTTPError as error:
            detail = error.read(512).decode("utf-8", errors="replace")
            raise ToolTransportError(f"HTTP {error.code}: {detail}") from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise ToolTransportError(str(error)) from error
        try:
            envelope = json.loads(payload)
        except json.JSONDecodeError as error:
            raise ToolProtocolError("invalid MCP JSON response") from error
        if not isinstance(envelope, dict):
            raise ToolProtocolError("invalid MCP response envelope")
        if "error" in envelope:
            raise ToolProtocolError(f"MCP RPC error: {envelope['error']}")
        if "result" not in envelope:
            raise ToolProtocolError("MCP response has no result")
        return envelope["result"]


def digest_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"
