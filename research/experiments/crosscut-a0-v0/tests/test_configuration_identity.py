from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPUTING_ROOT = ROOT.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(
    0,
    str(
        COMPUTING_ROOT
        / "research"
        / "experiments"
        / "observation-plane-v0"
        / "implementation"
    ),
)

from configuration_identity import (  # noqa: E402
    compare_configurations,
    from_evaluation_system_manifest,
    from_security_environment_identity,
)

B5 = (
    COMPUTING_ROOT
    / "research"
    / "experiments"
    / "harness-evaluation-v0"
    / "diagnostics"
    / "b5-native-005-32ec1ea"
    / "system-manifest.json"
)


class ConfigurationIdentityTests(unittest.TestCase):
    def test_evaluation_projection_keeps_environment_digest_only(self) -> None:
        manifest = json.loads(B5.read_text(encoding="utf-8"))
        identity = from_evaluation_system_manifest(manifest)
        environment = next(
            item for item in identity.bindings if item.slot == "execution.environment"
        )
        self.assertEqual(environment.availability, "digest_only")
        self.assertIsNone(environment.ref)
        self.assertEqual(
            len([item for item in identity.bindings if item.role == "verifier_domain"]),
            1,
        )
        self.assertNotIn("taskSchema", identity.to_dict())

    def test_security_environment_remains_opaque_owner_record(self) -> None:
        environment = {
            "environmentId": "environment:test-kvm",
            "providerId": "provider:windows-kvm",
            "providerRevision": "1",
            "imageDigest": "sha256:" + "1" * 64,
            "configurationDigest": "sha256:" + "2" * 64,
            "guardianPolicyDigest": "sha256:" + "3" * 64,
            "observationPlanDigest": "sha256:" + "4" * 64,
        }
        identity = from_security_environment_identity(
            environment,
            security_revision="3c605f2e341cf684ec499d5ea605cd7af40c4558",
        )
        binding = next(
            item for item in identity.bindings if item.slot == "execution.environment"
        )
        self.assertEqual(binding.availability, "inline_owner_record")
        self.assertEqual(binding.kind, "ordivon.security.environment-identity")
        serialized = json.dumps(identity.to_dict(), sort_keys=True)
        self.assertNotIn("guardianPolicyDigest", serialized)
        self.assertNotIn("observationPlanDigest", serialized)

    def test_cross_domain_comparison_never_invents_equivalence(self) -> None:
        evaluation = from_evaluation_system_manifest(
            json.loads(B5.read_text(encoding="utf-8"))
        )
        security = from_security_environment_identity(
            {
                "environmentId": "environment:test-kvm",
                "providerId": "provider:windows-kvm",
                "providerRevision": "1",
                "imageDigest": "sha256:" + "1" * 64,
                "configurationDigest": "sha256:" + "2" * 64,
                "guardianPolicyDigest": "sha256:" + "3" * 64,
                "observationPlanDigest": "sha256:" + "4" * 64,
            },
            security_revision="3c605f2e341cf684ec499d5ea605cd7af40c4558",
        )
        comparison = compare_configurations(evaluation, security)
        self.assertFalse(comparison["sameConfiguration"])
        self.assertFalse(comparison["fullyExplainable"])
        self.assertTrue(comparison["missingFromLeft"] or comparison["missingFromRight"])


if __name__ == "__main__":
    unittest.main()
