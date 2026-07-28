from __future__ import annotations

from importlib.resources import files
from typing import Final

SCHEMA_FILES: Final[tuple[str, ...]] = (
    "effect-binding-v1.schema.json",
    "effect-envelope-v1.schema.json",
    "host-workload-v1.schema.json",
    "tool-contract-v1.schema.json",
)
VECTOR_FILES: Final[tuple[str, ...]] = (
    "canonical-vectors.json",
    "canonical-vectors.tsv",
    "host-workload-vectors-v1.json",
)


def _resource_text(group: str, name: str, allowed: tuple[str, ...]) -> str:
    if name not in allowed:
        raise ValueError(f"unknown Ordivon Protocol {group} resource: {name}")
    return files("ordivon_protocol").joinpath(group, name).read_text(encoding="utf-8")


def schema_text(name: str) -> str:
    return _resource_text("schemas", name, SCHEMA_FILES)


def vector_text(name: str) -> str:
    return _resource_text("vectors", name, VECTOR_FILES)
