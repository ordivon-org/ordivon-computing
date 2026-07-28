from __future__ import annotations

from enum import StrEnum


class ExecutionKind(StrEnum):
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"


class CompletionKind(StrEnum):
    RESPONSE = "response"
    TERMINAL_OBSERVATION = "terminal-observation"
    ACCEPTED_VERIFICATION = "accepted-verification"
