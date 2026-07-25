from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .transport import ToolProtocolError, ToolRejected, ToolTransportError


@dataclass(slots=True)
class StreamableHttpMcpClient:
    """Minimal stateless MCP Streamable HTTP client using only the Python standard library."""

    endpoint: str
    bearer_token: str
    timeout_seconds: float = 10.0
    _next_request_id: int = field(default=1, init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.endpoint.startswith(("http://", "https://")):
            raise ValueError("MCP endpoint must be HTTP or HTTPS")
        if not self.bearer_token:
            raise ValueError("MCP bearer token must not be empty")
        if self.timeout_seconds <= 0:
            raise ValueError("MCP timeout must be positive")

    def initialize(self) -> dict[str, Any]:
        return self._request(
            "initialize",
            {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {
                    "name": "anc-semantic-core",
                    "version": "0.1.0",
                },
            },
        )

    def list_tools(self) -> tuple[dict[str, Any], ...]:
        result = self._request("tools/list", {})
        tools = result.get("tools")
        if not isinstance(tools, list) or not all(isinstance(tool, dict) for tool in tools):
            raise ToolProtocolError("tools/list did not return a Tool array")
        return tuple(tools)

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if not name:
            raise ValueError("Tool name must not be empty")
        result = self._request(
            "tools/call",
            {"name": name, "arguments": arguments},
        )
        structured = result.get("structuredContent")
        if result.get("isError") is True:
            error = structured.get("error") if isinstance(structured, dict) else None
            if not isinstance(error, dict):
                raise ToolProtocolError(f"MCP Tool returned an unstructured error: {name}")
            raise ToolRejected(
                name,
                code=str(error.get("code", "TOOL_ERROR")),
                message=str(error.get("message", "Tool call failed")),
                field=error.get("field") if isinstance(error.get("field"), str) else None,
                retryable=error.get("retryable") is True,
                detail=error,
            )
        if not isinstance(structured, dict):
            raise ToolProtocolError(f"MCP Tool returned no structured content: {name}")
        return structured

    def _request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        request_id = self._next_request_id
        self._next_request_id += 1
        body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        request = Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            },
        )
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = response.read()
        except HTTPError as error:
            detail = error.read(512).decode("utf-8", errors="replace")
            raise ToolTransportError(
                f"MCP HTTP {error.code} for {method}: {detail}"
            ) from error
        except (URLError, TimeoutError, OSError) as error:
            raise ToolTransportError(f"MCP transport failed for {method}: {error}") from error
        try:
            envelope = json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ToolProtocolError(f"MCP returned invalid JSON for {method}") from error
        if not isinstance(envelope, dict):
            raise ToolProtocolError(f"MCP returned a non-object envelope for {method}")
        if envelope.get("id") != request_id:
            raise ToolProtocolError(f"MCP response identity mismatch for {method}")
        protocol_error = envelope.get("error")
        if protocol_error is not None:
            raise ToolProtocolError(f"MCP protocol error for {method}: {protocol_error}")
        result = envelope.get("result")
        if not isinstance(result, dict):
            raise ToolProtocolError(f"MCP returned no result object for {method}")
        return result
