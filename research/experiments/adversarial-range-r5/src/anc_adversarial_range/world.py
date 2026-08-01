from __future__ import annotations

from dataclasses import dataclass

from .model import JsonValue, Receipt, canonical_digest, require_identity


@dataclass(frozen=True, slots=True)
class CommitRecord:
    effect_id: str
    resource_id: str
    payload_digest: str
    actor_id: str
    source_id: str
    receipt_id: str

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "effectId": self.effect_id,
            "resourceId": self.resource_id,
            "payloadDigest": self.payload_digest,
            "actorId": self.actor_id,
            "sourceId": self.source_id,
            "receiptId": self.receipt_id,
        }


class SimulatedWorld:
    """Owned deterministic world with exact hidden truth and reset proof."""

    def __init__(self) -> None:
        self._commits: list[CommitRecord] = []
        self._idempotency: dict[str, Receipt] = {}
        self._memory: dict[str, str] = {}
        self._generated_tools: set[str] = set()

    def commit(
        self,
        *,
        effect_id: str,
        resource_id: str,
        payload: JsonValue,
        actor_id: str,
        source_id: str,
        idempotency_key: str | None = None,
    ) -> Receipt:
        require_identity(effect_id, "effect")
        require_identity(resource_id, "resource")
        require_identity(actor_id, "actor")
        require_identity(source_id, "source")
        payload_digest = canonical_digest(payload)
        if idempotency_key is not None:
            require_identity(idempotency_key, "idempotency-key")
            existing = self._idempotency.get(idempotency_key)
            if existing is not None:
                if existing.effect_id != effect_id or existing.payload_digest != payload_digest:
                    raise ValueError("idempotency conflict")
                return existing
        commit_index = len(self._commits) + 1
        receipt = Receipt(
            receipt_id=f"receipt:commit-{commit_index}",
            effect_id=effect_id,
            idempotency_key=idempotency_key,
            commit_index=commit_index,
            payload_digest=payload_digest,
        )
        self._commits.append(
            CommitRecord(
                effect_id=effect_id,
                resource_id=resource_id,
                payload_digest=payload_digest,
                actor_id=actor_id,
                source_id=source_id,
                receipt_id=receipt.receipt_id,
            )
        )
        if idempotency_key is not None:
            self._idempotency[idempotency_key] = receipt
        return receipt

    def lookup_idempotency(self, key: str) -> Receipt | None:
        return self._idempotency.get(key)

    def count_effect(self, effect_id: str) -> int:
        return sum(item.effect_id == effect_id for item in self._commits)

    def count_resource(self, resource_id: str) -> int:
        return sum(item.resource_id == resource_id for item in self._commits)

    def commit_records(self) -> tuple[CommitRecord, ...]:
        return tuple(self._commits)

    def remember(self, memory_id: str, value: str) -> None:
        require_identity(memory_id, "memory")
        self._memory[memory_id] = value

    def generate_tool(self, tool_id: str) -> None:
        require_identity(tool_id, "tool")
        self._generated_tools.add(tool_id)

    def residuals(self) -> tuple[str, ...]:
        values: list[str] = []
        values.extend(f"commit:{item.receipt_id}" for item in self._commits)
        values.extend(f"memory:{key}" for key in sorted(self._memory))
        values.extend(f"generated-tool:{key}" for key in sorted(self._generated_tools))
        return tuple(values)

    def snapshot(self) -> dict[str, JsonValue]:
        return {
            "commits": [item.to_dict() for item in self._commits],
            "idempotencyKeys": sorted(self._idempotency),
            "memory": dict(sorted(self._memory.items())),
            "generatedTools": sorted(self._generated_tools),
        }

    def reset(self) -> dict[str, JsonValue]:
        before = self.snapshot()
        self._commits.clear()
        self._idempotency.clear()
        self._memory.clear()
        self._generated_tools.clear()
        after = self.snapshot()
        return {
            "beforeDigest": canonical_digest(before),
            "afterDigest": canonical_digest(after),
            "residualCountAfterReset": len(self.residuals()),
            "resetVerified": not self._commits and not self._memory and not self._generated_tools,
        }
