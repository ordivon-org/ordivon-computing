from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable

from ordivon_observation_core import canonical_digest

_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_AVAILABILITY = {"retained_ref", "inline_owner_record", "digest_only"}
_ROLES = {
    "implementation",
    "execution_environment",
    "cognition",
    "authority",
    "input",
    "verifier_domain",
}


class ConfigurationIdentityError(ValueError):
    pass


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ConfigurationIdentityError(f"{label} must be non-empty and trimmed")
    return value


def _digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise ConfigurationIdentityError(f"{label} must be a canonical SHA-256 digest")
    return value


@dataclass(frozen=True, slots=True, order=True)
class MaterialBinding:
    slot: str
    role: str
    owner: str
    kind: str
    binding_id: str
    digest: str
    availability: str
    ref: str | None = None

    def __post_init__(self) -> None:
        _text(self.slot, "binding slot")
        if self.role not in _ROLES:
            raise ConfigurationIdentityError(f"unsupported binding role: {self.role}")
        _text(self.owner, "binding owner")
        _text(self.kind, "binding kind")
        _text(self.binding_id, "binding identity")
        _digest(self.digest, "binding digest")
        if self.availability not in _AVAILABILITY:
            raise ConfigurationIdentityError(
                f"unsupported binding availability: {self.availability}"
            )
        if self.ref is not None:
            _text(self.ref, "binding reference")
        if self.availability == "retained_ref" and self.ref is None:
            raise ConfigurationIdentityError("retained_ref binding requires a reference")

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "role": self.role,
            "owner": self.owner,
            "kind": self.kind,
            "bindingId": self.binding_id,
            "digest": self.digest,
            "availability": self.availability,
            "ref": self.ref,
        }


@dataclass(frozen=True, slots=True)
class ConfigurationIdentity:
    configuration_id: str
    bindings: tuple[MaterialBinding, ...]
    unavailable_fields: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _text(self.configuration_id, "configuration identity")
        if not self.bindings:
            raise ConfigurationIdentityError("configuration identity requires bindings")
        ordered = tuple(sorted(self.bindings))
        if self.bindings != ordered:
            raise ConfigurationIdentityError("configuration bindings must be sorted")
        slots = [item.slot for item in self.bindings]
        if len(slots) != len(set(slots)):
            raise ConfigurationIdentityError("configuration binding slots must be unique")
        if tuple(sorted(set(self.unavailable_fields))) != self.unavailable_fields:
            raise ConfigurationIdentityError(
                "unavailable fields must be unique and sorted"
            )
        if tuple(self.limitations) != self.limitations:
            raise ConfigurationIdentityError("limitations must be a tuple")

    @classmethod
    def build(
        cls,
        configuration_id: str,
        bindings: Iterable[MaterialBinding],
        *,
        unavailable_fields: Iterable[str] = (),
        limitations: Iterable[str] = (),
    ) -> "ConfigurationIdentity":
        return cls(
            configuration_id=configuration_id,
            bindings=tuple(sorted(bindings)),
            unavailable_fields=tuple(sorted(set(unavailable_fields))),
            limitations=tuple(limitations),
        )

    @property
    def digest(self) -> str:
        return canonical_digest(self.payload())

    def payload(self) -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "kind": "ordivon.configuration-identity-experiment",
            "configurationId": self.configuration_id,
            "bindings": [item.to_dict() for item in self.bindings],
            "unavailableFields": list(self.unavailable_fields),
            "limitations": list(self.limitations),
        }

    def to_dict(self) -> dict[str, Any]:
        value = self.payload()
        value["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": self.digest,
        }
        return value


def _binding(
    slot: str,
    role: str,
    owner: str,
    kind: str,
    binding_id: str,
    digest: str,
    *,
    availability: str,
    ref: str | None = None,
) -> MaterialBinding:
    return MaterialBinding(
        slot=slot,
        role=role,
        owner=owner,
        kind=kind,
        binding_id=binding_id,
        digest=digest,
        availability=availability,
        ref=ref,
    )


def from_evaluation_system_manifest(document: dict[str, Any]) -> ConfigurationIdentity:
    if document.get("kind") != "ordivon.evaluation-system-manifest":
        raise ConfigurationIdentityError("unsupported Evaluation System Manifest")
    manifest_id = _text(document.get("manifestId"), "manifestId")
    snapshot = document.get("systemSnapshot")
    configuration = document.get("configuration")
    evaluation_contract = document.get("evaluationContract")
    unavailable = document.get("unavailableFields")
    limitations = document.get("limitations")
    if not isinstance(snapshot, dict) or not isinstance(configuration, dict):
        raise ConfigurationIdentityError("Evaluation manifest configuration is missing")
    if not isinstance(evaluation_contract, dict):
        raise ConfigurationIdentityError("Evaluation contract is missing")
    if not isinstance(unavailable, list) or any(not isinstance(x, str) for x in unavailable):
        raise ConfigurationIdentityError("unavailableFields must contain strings")
    if not isinstance(limitations, list) or any(not isinstance(x, str) for x in limitations):
        raise ConfigurationIdentityError("limitations must contain strings")
    provider = configuration.get("provider")
    digests = configuration.get("digests")
    if not isinstance(provider, dict) or not isinstance(digests, dict):
        raise ConfigurationIdentityError("Evaluation provider or digest set is missing")

    provider_id = _text(provider.get("providerId"), "providerId")
    model_id = _text(provider.get("modelId"), "modelId")
    bindings = [
        _binding(
            "implementation.system_snapshot",
            "implementation",
            "ordivon-computing",
            "ordivon.system-snapshot",
            str(snapshot.get("path")),
            _digest(snapshot.get("digest"), "System Snapshot digest"),
            availability="retained_ref",
            ref=str(snapshot.get("path")),
        ),
        _binding(
            "cognition.provider",
            "cognition",
            "evaluation-system-manifest",
            "ordivon.provider-configuration",
            f"provider:{provider_id}/{model_id}",
            canonical_digest(provider),
            availability="inline_owner_record",
            ref="system-manifest#configuration.provider",
        ),
        _binding(
            "verifier_domain.evaluation_contract",
            "verifier_domain",
            "ordivon-computing",
            "ordivon.evaluation-contract",
            f"evaluation-contract:{manifest_id}",
            canonical_digest(evaluation_contract),
            availability="inline_owner_record",
            ref="system-manifest#evaluationContract",
        ),
    ]
    digest_slots = {
        "promptSet": ("cognition.prompt_set", "cognition", "ordivon.prompt-set"),
        "contextPolicy": ("cognition.context_policy", "cognition", "ordivon.context-policy"),
        "toolCatalog": ("cognition.tool_catalog", "cognition", "ordivon.tool-catalog"),
        "toolGrant": ("authority.tool_grant", "authority", "ordivon.tool-grant"),
        "budgetProfile": ("authority.budget_profile", "authority", "ordivon.budget-profile"),
        "environment": (
            "execution.environment",
            "execution_environment",
            "ordivon.execution-environment",
        ),
    }
    for source_field, (slot, role, kind) in digest_slots.items():
        bindings.append(
            _binding(
                slot,
                role,
                "evaluation-system-manifest",
                kind,
                f"{manifest_id}:{source_field}",
                _digest(digests.get(source_field), f"{source_field} digest"),
                availability="digest_only",
            )
        )
    return ConfigurationIdentity.build(
        f"configuration:{manifest_id}",
        bindings,
        unavailable_fields=unavailable,
        limitations=limitations,
    )


def from_security_environment_identity(
    environment: dict[str, Any],
    *,
    security_revision: str,
) -> ConfigurationIdentity:
    required = {
        "environmentId",
        "providerId",
        "providerRevision",
        "imageDigest",
        "configurationDigest",
        "guardianPolicyDigest",
        "observationPlanDigest",
    }
    if set(environment) != required:
        raise ConfigurationIdentityError("Security EnvironmentIdentity fields differ")
    environment_id = _text(environment["environmentId"], "Security environment identity")
    for field in (
        "imageDigest",
        "configurationDigest",
        "guardianPolicyDigest",
        "observationPlanDigest",
    ):
        _digest(environment[field], field)
    _text(environment["providerId"], "Security provider identity")
    _text(environment["providerRevision"], "Security provider revision")
    _text(security_revision, "Security revision")
    return ConfigurationIdentity.build(
        f"configuration:{environment_id}",
        (
            _binding(
                "implementation.security",
                "implementation",
                "ordivon-security",
                "git-revision",
                "ordivon-security",
                "sha256:" + __import__("hashlib").sha256(security_revision.encode()).hexdigest(),
                availability="inline_owner_record",
                ref=f"git:{security_revision}",
            ),
            _binding(
                "execution.environment",
                "execution_environment",
                "ordivon-security",
                "ordivon.security.environment-identity",
                environment_id,
                canonical_digest(environment),
                availability="inline_owner_record",
                ref=f"security-environment:{environment_id}",
            ),
        ),
        limitations=(
            "Security-specific environment fields remain inside the owner-native EnvironmentIdentity digest.",
        ),
    )


def compare_configurations(
    left: ConfigurationIdentity,
    right: ConfigurationIdentity,
) -> dict[str, Any]:
    left_map = {item.slot: item for item in left.bindings}
    right_map = {item.slot: item for item in right.bindings}
    all_slots = sorted(set(left_map) | set(right_map))
    equal: list[str] = []
    changed: list[str] = []
    missing_left: list[str] = []
    missing_right: list[str] = []
    digest_only: list[str] = []
    for slot in all_slots:
        a = left_map.get(slot)
        b = right_map.get(slot)
        if a is None:
            missing_left.append(slot)
            continue
        if b is None:
            missing_right.append(slot)
            continue
        if a.digest == b.digest:
            equal.append(slot)
        else:
            changed.append(slot)
        if a.availability == "digest_only" or b.availability == "digest_only":
            digest_only.append(slot)
    same = not changed and not missing_left and not missing_right
    return {
        "schemaVersion": 1,
        "kind": "ordivon.configuration-comparison-experiment",
        "leftConfigurationId": left.configuration_id,
        "rightConfigurationId": right.configuration_id,
        "sameConfiguration": same,
        "equalSlots": equal,
        "changedSlots": changed,
        "missingFromLeft": missing_left,
        "missingFromRight": missing_right,
        "digestOnlySharedSlots": sorted(set(digest_only)),
        "fullyExplainable": (
            not digest_only
            and not left.unavailable_fields
            and not right.unavailable_fields
        ),
    }
