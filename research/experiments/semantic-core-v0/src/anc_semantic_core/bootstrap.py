from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .authority import AuthorityPolicy, AuthorityRole
from .authorized import AuthorityRoot, AuthorizedKernel
from .identity import IdKind, SemanticId
from .journal import JournalKernel
from .kernel import ReferenceKernel


def local_authority_policy(
    secret: bytes,
    *,
    issuer: str = "issuer:local-semantic-kernel",
    policy_version: str = "authority-policy-v1",
    key_id: str = "local-hmac-v1",
) -> AuthorityPolicy:
    return AuthorityPolicy(
        issuer_id=SemanticId(IdKind.PRINCIPAL, issuer),
        policy_version=policy_version,
        key_id=key_id,
        secret=secret,
    )


@dataclass(frozen=True, slots=True)
class KernelAuthorityViews:
    effects: AuthorizedKernel
    execution: AuthorizedKernel
    verification: AuthorizedKernel
    facts: AuthorizedKernel
    read: AuthorizedKernel


def issue_authority_views(
    reducer,
    policy: AuthorityPolicy,
    *,
    namespace: str,
    trust_domain: str = "local-runtime",
) -> KernelAuthorityViews:
    root = AuthorityRoot(reducer, policy)
    issued = {
        role: root.issue(
            authority_id=SemanticId(
                IdKind.AUTHORITY, f"{namespace}:{role.value}:authority"
            ),
            principal_id=SemanticId(
                IdKind.PRINCIPAL, f"{namespace}:{role.value}:principal"
            ),
            role=role,
            trust_domain=f"{trust_domain}:{role.value}",
            contract_version=f"{role.value}-contract-v1",
        )
        for role in AuthorityRole
    }
    return KernelAuthorityViews(
        effects=issued[AuthorityRole.EFFECT],
        execution=root.combine(
            issued[AuthorityRole.DISPATCH], issued[AuthorityRole.OBSERVATION]
        ),
        verification=issued[AuthorityRole.VERIFICATION],
        facts=issued[AuthorityRole.FACT],
        read=root.read_only(),
    )


def authorized_reference_views(
    secret: bytes,
    *,
    namespace: str,
    trust_domain: str = "local-runtime",
) -> KernelAuthorityViews:
    policy = local_authority_policy(secret)
    return issue_authority_views(
        ReferenceKernel(policy),
        policy,
        namespace=namespace,
        trust_domain=trust_domain,
    )


def authorized_journal_views(
    path: str | Path,
    secret: bytes,
    *,
    namespace: str,
    trust_domain: str = "local-runtime",
) -> KernelAuthorityViews:
    policy = local_authority_policy(secret)
    return issue_authority_views(
        JournalKernel(path, policy),
        policy,
        namespace=namespace,
        trust_domain=trust_domain,
    )
