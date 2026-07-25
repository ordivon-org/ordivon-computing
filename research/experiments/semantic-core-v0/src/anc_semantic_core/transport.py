from __future__ import annotations

from typing import Any


class ToolCallError(RuntimeError):
    """Base error after a Tool invocation has begun and delivery may be uncertain."""


class ToolTransportError(ToolCallError):
    pass


class ToolProtocolError(ToolCallError):
    pass


class ToolRejected(ToolProtocolError):
    """Structured rejection returned by a Tool endpoint."""

    def __init__(
        self,
        tool_name: str,
        *,
        code: str,
        message: str,
        field: str | None = None,
        retryable: bool = False,
        detail: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(f"{tool_name} rejected the call: {code}: {message}")
        self.tool_name = tool_name
        self.code = code
        self.message = message
        self.field = field
        self.retryable = retryable
        self.detail = detail or {}
