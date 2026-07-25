from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class IdKind(StrEnum):
    PRINCIPAL = "principal"
    WORLD_OBJECT = "world_object"
    TASK = "task"
    ATTEMPT = "attempt"
    EFFECT = "effect"
    DISPATCH = "dispatch"
    OBSERVATION = "observation"
    ARTIFACT = "artifact"
    CLAIM = "claim"
    VERIFICATION = "verification"
    FACT = "fact"
    EVENT = "event"


@dataclass(frozen=True, order=True, slots=True)
class SemanticId:
    kind: IdKind
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("identity value must not be empty")
        if self.value != self.value.strip():
            raise ValueError("identity value must not have surrounding whitespace")
        if len(self.value.encode("utf-8")) > 256:
            raise ValueError("identity value exceeds 256 UTF-8 bytes")
        if any(ord(character) < 32 or ord(character) == 127 for character in self.value):
            raise ValueError("identity value must not contain control characters")

    def require(self, expected: IdKind) -> SemanticId:
        if self.kind is not expected:
            raise ValueError(f"expected {expected.value} identity, got {self.kind.value}")
        return self

    def __str__(self) -> str:
        return f"{self.kind.value}:{self.value}"
