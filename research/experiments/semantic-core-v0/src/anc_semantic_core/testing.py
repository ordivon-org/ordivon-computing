from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .authority import AuthorityPolicy, AuthorityRole
from .authorized import AuthorityRoot, AuthorizedKernel
from .identity import IdKind, SemanticId
from .bootstrap import KernelAuthorityViews, issue_authority_views
from .journal import JournalReducer
from .reducer import ReferenceReducer


_TEST_SECRET = b"agent-native-computing-semantic-core-authority-v1-test-secret"
_ALL_ROLES = tuple(AuthorityRole)


def test_authority_policy() -> AuthorityPolicy:
    return AuthorityPolicy(
        issuer_id=SemanticId(IdKind.PRINCIPAL, "issuer:semantic-core-conformance"),
        policy_version="authority-policy-v1",
        key_id="conformance-hmac-v1",
        secret=_TEST_SECRET,
    )


def authorize_reducer(
    reducer,
    policy: AuthorityPolicy,
    *,
    roles: Iterable[AuthorityRole] = _ALL_ROLES,
    namespace: str = "conformance",
) -> AuthorizedKernel:
    root = AuthorityRoot(reducer, policy)
    views = []
    for role in roles:
        views.append(
            root.issue(
                authority_id=SemanticId(
                    IdKind.AUTHORITY, f"{namespace}:{role.value}:authority"
                ),
                principal_id=SemanticId(
                    IdKind.PRINCIPAL, f"{namespace}:{role.value}:principal"
                ),
                role=role,
                trust_domain=f"{namespace}:{role.value}",
                contract_version=f"{role.value}-contract-v1",
            )
        )
    return root.combine(*views) if views else root.read_only()


def reference_authority_views(
    *, namespace: str = "conformance"
) -> KernelAuthorityViews:
    policy = test_authority_policy()
    return issue_authority_views(
        ReferenceReducer(policy), policy, namespace=namespace
    )


def journal_authority_views(
    path: str | Path, *, namespace: str = "conformance"
) -> KernelAuthorityViews:
    policy = test_authority_policy()
    return issue_authority_views(
        JournalReducer(path, policy), policy, namespace=namespace
    )


def reference_kernel(
    *,
    roles: Iterable[AuthorityRole] = _ALL_ROLES,
    namespace: str = "conformance",
) -> AuthorizedKernel:
    policy = test_authority_policy()
    return authorize_reducer(
        ReferenceReducer(policy), policy, roles=roles, namespace=namespace
    )


def journal_kernel(
    path: str | Path,
    *,
    roles: Iterable[AuthorityRole] = _ALL_ROLES,
    namespace: str = "conformance",
) -> AuthorizedKernel:
    policy = test_authority_policy()
    return authorize_reducer(
        JournalReducer(path, policy), policy, roles=roles, namespace=namespace
    )
