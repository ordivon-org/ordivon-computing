from __future__ import annotations

from typing import Any


def project_delivery(
    *,
    owner: str,
    source_revision: str | None,
    published_revision: str | None,
    active_revision: str | None,
    deployable: bool,
    publication_authority: str,
    activation_authority: str | None = None,
) -> dict[str, Any]:
    observations = {
        "source": {"revision": source_revision, "known": source_revision is not None},
        "published": {"revision": published_revision, "known": published_revision is not None, "authority": publication_authority},
        "active": {"revision": active_revision, "known": active_revision is not None, "authority": activation_authority},
    }
    gaps: list[str] = []
    if source_revision is None:
        state = "source_unknown"
    elif published_revision is None:
        state = "publication_unknown"
        gaps.append("publication_unknown")
    elif not deployable:
        if source_revision == published_revision:
            state = "source_published"
        else:
            state = "source_not_published"
            gaps.append("source_vs_published")
    elif active_revision is None:
        state = "activation_unknown"
        if source_revision != published_revision:
            gaps.append("source_vs_published")
        gaps.append("active_unknown")
    else:
        if source_revision != published_revision:
            gaps.append("source_vs_published")
        if source_revision != active_revision:
            gaps.append("source_vs_active")
        if published_revision != active_revision:
            gaps.append("published_vs_active")
        if source_revision == published_revision == active_revision:
            state = "converged"
        elif source_revision == active_revision and source_revision != published_revision:
            state = "active_source_not_published"
        elif source_revision == published_revision and source_revision != active_revision:
            state = "published_source_not_active"
        elif published_revision == active_revision and source_revision != active_revision:
            state = "source_ahead_of_published_active_identity"
        else:
            state = "three_way_divergence"
    return {
        "schemaVersion": 1,
        "kind": "ordivon.crosscut-delivery-projection",
        "truthRole": "rebuildable-read-only-projection",
        "owner": owner,
        "deployable": deployable,
        "observations": observations,
        "state": state,
        "gaps": gaps,
        "truthBoundary": {
            "sourceAuthorityRemainsGitOwner": True,
            "publicationAuthorityRemainsRemoteOwner": True,
            "activationAuthorityRemainsRuntimeOwner": True,
            "projectionMayNotDeployOrPublish": True,
            "revisionEqualityDoesNotClaimAncestry": True,
        },
    }
