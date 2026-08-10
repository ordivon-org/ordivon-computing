from __future__ import annotations

# Compatibility facade. Public role protocols live in interfaces.py; the raw
# executable reference reducer lives in reducer.py.
from .errors import (
    IdentityConflict,
    InvalidTransition,
    InvariantViolation,
    NotFound,
    RevisionConflict,
    SemanticError,
)
from .interfaces import (
    EffectView,
    ExecutionView,
    FactView,
    KernelReadView,
    RootBoundView,
    SemanticKernel,
    TransactionalView,
    VerificationView,
)
from .reducer import ReferenceReducer

__all__ = [
    "EffectView",
    "ExecutionView",
    "FactView",
    "IdentityConflict",
    "InvalidTransition",
    "InvariantViolation",
    "KernelReadView",
    "NotFound",
    "ReferenceReducer",
    "RevisionConflict",
    "RootBoundView",
    "SemanticError",
    "SemanticKernel",
    "TransactionalView",
    "VerificationView",
]
