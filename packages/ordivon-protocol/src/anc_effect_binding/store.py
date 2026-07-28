from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

from anc_canonical import canonical_bytes, loads_strict, validate_digest

from .model import (
    SignedEffectBinding,
    binding_digest,
    signed_effect_binding_from_dict,
)


class BindingStoreError(RuntimeError):
    pass


class BindingArtifactMissing(BindingStoreError):
    pass


class BindingArtifactCorrupt(BindingStoreError):
    pass


class BindingStore(Protocol):
    def put(self, signed_binding: SignedEffectBinding) -> str: ...

    def get(self, digest: str) -> SignedEffectBinding: ...


class FileBindingStore:
    """Small content-addressed store for complete signed Binding artifacts."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, signed_binding: SignedEffectBinding) -> str:
        digest = binding_digest(signed_binding.binding)
        payload = canonical_bytes(signed_binding.to_dict())
        path = self._path(digest)
        if path.exists():
            if path.read_bytes() != payload:
                raise BindingArtifactCorrupt("Binding digest already maps to different bytes")
            return digest
        temporary = path.with_suffix(f".tmp-{os.getpid()}")
        temporary.write_bytes(payload)
        os.replace(temporary, path)
        return digest

    def get(self, digest: str) -> SignedEffectBinding:
        path = self._path(digest)
        if not path.exists():
            raise BindingArtifactMissing(f"Binding artifact is missing: {digest}")
        try:
            value = loads_strict(path.read_bytes())
            if not isinstance(value, dict):
                raise ValueError("signed Binding artifact must be an object")
            signed = signed_effect_binding_from_dict(value)
        except (OSError, ValueError) as error:
            raise BindingArtifactCorrupt(f"Binding artifact cannot be decoded: {digest}") from error
        if binding_digest(signed.binding) != digest:
            raise BindingArtifactCorrupt("Binding artifact digest does not match its content address")
        return signed

    def _path(self, digest: str) -> Path:
        validate_digest(digest)
        return self.root / f"{digest[7:]}.json"
