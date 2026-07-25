from __future__ import annotations


class SemanticError(RuntimeError):
    pass


class NotFound(SemanticError):
    pass


class IdentityConflict(SemanticError):
    pass


class RevisionConflict(SemanticError):
    pass


class InvalidTransition(SemanticError):
    pass


class InvariantViolation(SemanticError):
    pass
