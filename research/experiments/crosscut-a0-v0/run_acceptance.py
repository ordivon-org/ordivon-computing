from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parent
COMPUTING_ROOT = ROOT.parents[2]
OBSERVATION_IMPLEMENTATION = (
    COMPUTING_ROOT
    / "research"
    / "experiments"
    / "observation-plane-v0"
    / "implementation"
)
sys.path.insert(0, str(OBSERVATION_IMPLEMENTATION))
sys.path.insert(0, str(ROOT))

from ordivon_observation_core import canonical_digest  # noqa: E402
from configuration_identity import (  # noqa: E402
    compare_configurations,
    from_evaluation_system_manifest,
    from_security_environment_identity,
)
from measurement_projection import from_evaluation_metrics  # noqa: E402

B5 = (
    COMPUTING_ROOT
    / "research"
    / "experiments"
    / "harness-evaluation-v0"
    / "diagnostics"
    / "b5-native-005-32ec1ea"
)
SECURITY_REVISION = "3c605f2e341cf684ec499d5ea605cd7af40c4558"


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def git_revision() -> str:
    return subprocess.check_output(
        ["git", "-C", str(COMPUTING_ROOT), "rev-parse", "HEAD"],
        text=True,
    ).strip()


def with_integrity(value: dict[str, Any]) -> dict[str, Any]:
    payload = dict(value)
    payload["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": canonical_digest(value),
    }
    return payload


def run() -> dict[str, Any]:
    manifest = load_object(B5 / "system-manifest.json")
    result = load_object(B5 / "result.json")
    evaluation = from_evaluation_system_manifest(manifest)
    environment_binding = next(
        item for item in evaluation.bindings if item.slot == "execution.environment"
    )
    security_environment = {
        "environmentId": "environment:a0-security-kvm-shape",
        "providerId": "provider:windows-kvm",
        "providerRevision": "1",
        "imageDigest": "sha256:" + "2" * 64,
        "configurationDigest": "sha256:" + "3" * 64,
        "guardianPolicyDigest": "sha256:" + "4" * 64,
        "observationPlanDigest": "sha256:" + "5" * 64,
    }
    security = from_security_environment_identity(
        security_environment,
        security_revision=SECURITY_REVISION,
    )
    comparison = compare_configurations(evaluation, security)
    metrics = result.get("metrics")
    if not isinstance(metrics, dict):
        raise ValueError("B5 Result metrics are missing")
    projection = from_evaluation_metrics(metrics)
    assertions = {
        "evaluationEnvironmentIsExplicitlyDigestOnly": (
            environment_binding.availability == "digest_only"
        ),
        "evaluationDomainContractRemainsOneOpaqueBinding": (
            len(
                [
                    item
                    for item in evaluation.bindings
                    if item.role == "verifier_domain"
                ]
            )
            == 1
        ),
        "securityEnvironmentRemainsOwnerNativeBinding": (
            len(security.bindings) == 2
            and any(
                item.kind == "ordivon.security.environment-identity"
                for item in security.bindings
            )
        ),
        "differentDomainsAreNotDeclaredSameConfiguration": (
            comparison["sameConfiguration"] is False
        ),
        "monetaryCostIsNotInvented": (
            "estimatedCostUsd" in projection.omitted_fields
            and "ordivon.cost.estimated_usd" not in projection.measurements
        ),
        "tokenProjectionRetainsProviderReportedValues": (
            projection.measurements["ordivon.harness.input_tokens"].value
            == metrics["inputTokens"]
            and projection.measurements["ordivon.harness.output_tokens"].value
            == metrics["outputTokens"]
            and projection.measurements["ordivon.harness.cached_input_tokens"].value
            == metrics["cachedInputTokens"]
        ),
        "otelCompatibilityIsAliasOnly": (
            projection.otel_aliases["ordivon.harness.input_tokens"]
            == "gen_ai.usage.input_tokens"
        ),
    }
    if not all(assertions.values()):
        failed = [key for key, passed in assertions.items() if not passed]
        raise RuntimeError(f"A0 M1/U1 acceptance failed: {failed}")
    return with_integrity(
        {
            "schemaVersion": 1,
            "kind": "ordivon.crosscut-a0-m1-u1-acceptance",
            "status": "accepted_bounded_experiment",
            "source": {
                "computingBaseRevision": "c239dff62f9f15baa4ee2056d2db9d7d1b3f12d6",
                "experimentImplementationRevision": git_revision(),
                "securityShapeRevision": SECURITY_REVISION,
                "b5SystemManifestDigest": canonical_digest(manifest),
                "b5ResultDigest": canonical_digest(result),
            },
            "configurationIdentity": {
                "evaluationDigest": evaluation.digest,
                "securityDigest": security.digest,
                "comparison": comparison,
            },
            "measurementProjection": {
                "digest": projection.digest,
                "measurementCount": len(projection.measurements),
                "omittedFields": list(projection.omitted_fields),
                "otelAliasCount": len(projection.otel_aliases),
            },
            "assertions": assertions,
            "decisions": [
                "Configuration identity remains a digest/reference composition experiment, not product authority.",
                "Evaluation environment payload explainability remains incomplete while only its digest is retained.",
                "Usage normalization uses Observation measurements; no writable UsageRecord owner is admitted.",
                "OpenTelemetry names remain rebuildable export aliases rather than durable Ordivon recovery semantics.",
                "O1 fresh current three-owner trajectory remains required before A0 observation expansion.",
            ],
        }
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Cross-cutting A0 M1/U1 acceptance")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "evidence" / "a0-m1-u1-acceptance.json",
    )
    args = parser.parse_args(argv)
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
