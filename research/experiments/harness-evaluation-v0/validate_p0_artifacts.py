#!/usr/bin/env python3
"""Validate the Track R P0 frozen-baseline artifacts without external dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
KINDS = {
    "ordivon.evaluation-system-manifest",
    "ordivon.evaluation-suite",
    "ordivon.component-test-baseline",
    "ordivon.evaluation-summary",
    "ordivon.evaluation-p0-closeout",
}
NULLABLE_CONFIGURATION_FIELDS = {
    "configuration.provider.providerId",
    "configuration.provider.modelId",
    "configuration.provider.modelRevision",
    "configuration.provider.adapterRevision",
    "configuration.digests.promptSet",
    "configuration.digests.contextPolicy",
    "configuration.digests.toolCatalog",
    "configuration.digests.toolGrant",
    "configuration.digests.budgetProfile",
    "configuration.digests.environment",
}


def canonical_payload(document: dict[str, Any]) -> bytes:
    payload = dict(document)
    payload.pop("integrity", None)
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def payload_digest(document: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_payload(document)).hexdigest()


def file_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact(value: dict[str, Any], expected: set[str], label: str) -> None:
    actual = set(value)
    require(
        actual == expected,
        f"{label} fields differ; missing={sorted(expected - actual)}, extra={sorted(actual - expected)}",
    )


def nonempty(value: Any, label: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), f"{label} must be a non-empty string")
    return value


def digest(value: Any, label: str, *, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    require(isinstance(value, str) and bool(DIGEST_RE.fullmatch(value)), f"{label} must be sha256:<64 lowercase hex>")


def revision(value: Any, label: str) -> None:
    require(isinstance(value, str) and bool(REVISION_RE.fullmatch(value)), f"{label} must be a full lowercase Git revision")


def nullable_count(value: Any, label: str) -> None:
    require(
        value is None or (isinstance(value, int) and not isinstance(value, bool) and value >= 0),
        f"{label} must be null or a non-negative integer",
    )


def string_list(value: Any, label: str, *, minimum: int = 0, unique: bool = False) -> list[str]:
    require(isinstance(value, list) and len(value) >= minimum, f"{label} must contain at least {minimum} entries")
    for index, item in enumerate(value):
        nonempty(item, f"{label}[{index}]")
    if unique:
        require(len(value) == len(set(value)), f"{label} entries must be unique")
    return value


def validate_integrity(document: dict[str, Any]) -> None:
    integrity = document.get("integrity")
    require(isinstance(integrity, dict), "integrity must be an object")
    exact(integrity, {"algorithm", "canonicalization", "payloadDigest"}, "integrity")
    require(integrity["algorithm"] == "sha256", "unsupported integrity algorithm")
    require(integrity["canonicalization"] == "ordivon-evidence-json-v1", "unsupported canonicalization")
    digest(integrity["payloadDigest"], "integrity.payloadDigest")
    require(integrity["payloadDigest"] == payload_digest(document), "integrity payloadDigest differs")


def validate_file_ref(value: Any, label: str) -> dict[str, str]:
    require(isinstance(value, dict), f"{label} must be an object")
    exact(value, {"path", "digest"}, label)
    path = nonempty(value["path"], f"{label}.path")
    relative = PurePosixPath(path)
    require(not relative.is_absolute() and ".." not in relative.parts, f"{label}.path must be normalized and relative")
    digest(value["digest"], f"{label}.digest")
    return value


def validate_system_manifest(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "manifestId",
        "capturedAt",
        "systemSnapshot",
        "evaluationContract",
        "configuration",
        "privacy",
        "unavailableFields",
        "limitations",
        "integrity",
    }
    exact(document, expected, "Evaluation System Manifest")
    require(document["schemaVersion"] == 1, "unsupported manifest schemaVersion")
    require(document["kind"] == "ordivon.evaluation-system-manifest", "unsupported manifest kind")
    nonempty(document["manifestId"], "manifestId")
    nonempty(document["capturedAt"], "capturedAt")
    validate_file_ref(document["systemSnapshot"], "systemSnapshot")

    contract = document["evaluationContract"]
    require(isinstance(contract, dict), "evaluationContract must be an object")
    exact(
        contract,
        {"taskSchema", "trialSchema", "resultSchema", "failureSchema", "failureTaxonomy", "suite", "graderSet"},
        "evaluationContract",
    )
    for field in ("taskSchema", "trialSchema", "resultSchema", "failureSchema", "failureTaxonomy", "suite"):
        validate_file_ref(contract[field], f"evaluationContract.{field}")
    if contract["graderSet"] is not None:
        validate_file_ref(contract["graderSet"], "evaluationContract.graderSet")

    configuration = document["configuration"]
    require(isinstance(configuration, dict), "configuration must be an object")
    exact(configuration, {"provider", "digests"}, "configuration")
    provider = configuration["provider"]
    require(isinstance(provider, dict), "configuration.provider must be an object")
    exact(provider, {"providerId", "modelId", "modelRevision", "adapterRevision"}, "configuration.provider")
    for field, value in provider.items():
        if value is not None:
            nonempty(value, f"configuration.provider.{field}")
    digests = configuration["digests"]
    require(isinstance(digests, dict), "configuration.digests must be an object")
    exact(digests, {"promptSet", "contextPolicy", "toolCatalog", "toolGrant", "budgetProfile", "environment"}, "configuration.digests")
    for field, value in digests.items():
        digest(value, f"configuration.digests.{field}", nullable=True)

    privacy = document["privacy"]
    require(isinstance(privacy, dict), "privacy must be an object")
    exact(privacy, {"secretsIncluded", "rawReasoningRequired"}, "privacy")
    require(privacy["secretsIncluded"] is False, "evaluation manifests must not include secrets")
    require(privacy["rawReasoningRequired"] is False, "raw private reasoning cannot be required")

    unavailable = set(string_list(document["unavailableFields"], "unavailableFields", unique=True))
    require(unavailable <= NULLABLE_CONFIGURATION_FIELDS, "unavailableFields contains an unsupported path")
    observed_nulls: set[str] = set()
    for field, value in provider.items():
        if value is None:
            observed_nulls.add(f"configuration.provider.{field}")
    for field, value in digests.items():
        if value is None:
            observed_nulls.add(f"configuration.digests.{field}")
    require(unavailable == observed_nulls, "unavailableFields must exactly identify null configuration fields")
    string_list(document["limitations"], "limitations", minimum=1)
    validate_integrity(document)


def validate_suite(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "suiteId",
        "suiteVersion",
        "purpose",
        "workloadFamilies",
        "comparisonPolicy",
        "metrics",
        "integrity",
    }
    exact(document, expected, "Evaluation Suite")
    require(document["schemaVersion"] == 1, "unsupported suite schemaVersion")
    require(document["kind"] == "ordivon.evaluation-suite", "unsupported suite kind")
    nonempty(document["suiteId"], "suiteId")
    require(isinstance(document["suiteVersion"], int) and document["suiteVersion"] >= 1, "suiteVersion must be positive")
    nonempty(document["purpose"], "purpose")

    families = document["workloadFamilies"]
    require(isinstance(families, list) and families, "workloadFamilies must be non-empty")
    family_ids: list[str] = []
    for index, family in enumerate(families):
        label = f"workloadFamilies[{index}]"
        require(isinstance(family, dict), f"{label} must be an object")
        exact(
            family,
            {
                "familyId",
                "status",
                "priority",
                "validatedTaskCount",
                "targetTaskCount",
                "taskRefs",
                "targetFailureCodes",
                "admissionEvidenceRefs",
                "limitations",
            },
            label,
        )
        family_ids.append(nonempty(family["familyId"], f"{label}.familyId"))
        require(family["status"] in {"admitted", "candidate", "historical_only", "blocked"}, f"{label}.status is unsupported")
        require(family["priority"] in {"P0", "P1", "P2"}, f"{label}.priority is unsupported")
        for field in ("validatedTaskCount", "targetTaskCount"):
            require(isinstance(family[field], int) and family[field] >= 0, f"{label}.{field} must be non-negative")
        require(family["targetTaskCount"] >= family["validatedTaskCount"], f"{label} targetTaskCount is too small")
        task_refs = family["taskRefs"]
        require(isinstance(task_refs, list), f"{label}.taskRefs must be a list")
        for task_index, task_ref in enumerate(task_refs):
            task_label = f"{label}.taskRefs[{task_index}]"
            require(isinstance(task_ref, dict), f"{task_label} must be an object")
            exact(task_ref, {"repositoryId", "taskId", "taskVersion", "path", "digest"}, task_label)
            nonempty(task_ref["repositoryId"], f"{task_label}.repositoryId")
            nonempty(task_ref["taskId"], f"{task_label}.taskId")
            require(isinstance(task_ref["taskVersion"], int) and task_ref["taskVersion"] >= 1, f"{task_label}.taskVersion must be positive")
            nonempty(task_ref["path"], f"{task_label}.path")
            digest(task_ref["digest"], f"{task_label}.digest", nullable=True)
        require(len(task_refs) >= family["validatedTaskCount"], f"{label} has fewer taskRefs than validatedTaskCount")
        string_list(family["targetFailureCodes"], f"{label}.targetFailureCodes", unique=True)
        string_list(family["admissionEvidenceRefs"], f"{label}.admissionEvidenceRefs", unique=True)
        string_list(family["limitations"], f"{label}.limitations")
    require(len(family_ids) == len(set(family_ids)), "workload family identifiers must be unique")

    policy = document["comparisonPolicy"]
    require(isinstance(policy, dict), "comparisonPolicy must be an object")
    exact(
        policy,
        {
            "smokeTrials",
            "developmentTrials",
            "architectureDecisionMinTrials",
            "architectureDecisionMaxTrials",
            "requireSameTaskVersion",
            "requireSameVerifierRevision",
            "requireSystemManifest",
            "reviewTriggers",
        },
        "comparisonPolicy",
    )
    for field in ("smokeTrials", "developmentTrials", "architectureDecisionMinTrials", "architectureDecisionMaxTrials"):
        require(isinstance(policy[field], int) and policy[field] >= 1, f"comparisonPolicy.{field} must be positive")
    require(policy["smokeTrials"] <= policy["developmentTrials"] <= policy["architectureDecisionMinTrials"], "comparison trial thresholds are not monotonic")
    require(policy["architectureDecisionMinTrials"] <= policy["architectureDecisionMaxTrials"], "architecture decision trial range is invalid")
    for field in ("requireSameTaskVersion", "requireSameVerifierRevision", "requireSystemManifest"):
        require(policy[field] is True, f"comparisonPolicy.{field} must remain true")
    string_list(policy["reviewTriggers"], "comparisonPolicy.reviewTriggers", minimum=1, unique=True)

    metrics = document["metrics"]
    require(isinstance(metrics, dict), "metrics must be an object")
    exact(metrics, {"primary", "guardrails", "diagnostic", "forbidGlobalScore"}, "metrics")
    string_list(metrics["primary"], "metrics.primary", minimum=1, unique=True)
    string_list(metrics["guardrails"], "metrics.guardrails", minimum=1, unique=True)
    string_list(metrics["diagnostic"], "metrics.diagnostic", minimum=1, unique=True)
    require(metrics["forbidGlobalScore"] is True, "a heterogeneous suite cannot emit one global score")
    validate_integrity(document)


def validate_component_baseline(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "baselineId",
        "capturedAt",
        "systemManifest",
        "scope",
        "components",
        "aggregate",
        "limitations",
        "integrity",
    }
    exact(document, expected, "Component Test Baseline")
    require(document["schemaVersion"] == 1, "unsupported baseline schemaVersion")
    require(document["kind"] == "ordivon.component-test-baseline", "unsupported baseline kind")
    nonempty(document["baselineId"], "baselineId")
    nonempty(document["capturedAt"], "capturedAt")
    validate_file_ref(document["systemManifest"], "systemManifest")
    nonempty(document["scope"], "scope")

    components = document["components"]
    require(isinstance(components, list) and components, "components must be non-empty")
    component_ids: list[str] = []
    test_suites = 0
    contract_checks = 0
    passed = failed = ignored = 0
    for component_index, component in enumerate(components):
        label = f"components[{component_index}]"
        require(isinstance(component, dict), f"{label} must be an object")
        exact(component, {"componentId", "repositoryId", "revision", "sourceStateDigest", "checks"}, label)
        component_ids.append(nonempty(component["componentId"], f"{label}.componentId"))
        nonempty(component["repositoryId"], f"{label}.repositoryId")
        revision(component["revision"], f"{label}.revision")
        digest(component["sourceStateDigest"], f"{label}.sourceStateDigest")
        checks = component["checks"]
        require(isinstance(checks, list) and checks, f"{label}.checks must be non-empty")
        check_ids: list[str] = []
        for check_index, check in enumerate(checks):
            check_label = f"{label}.checks[{check_index}]"
            require(isinstance(check, dict), f"{check_label} must be an object")
            exact(check, {"checkId", "checkKind", "command", "status", "passed", "failed", "ignored", "durationMs", "evidence"}, check_label)
            check_ids.append(nonempty(check["checkId"], f"{check_label}.checkId"))
            require(check["checkKind"] in {"test_suite", "contract_check"}, f"{check_label}.checkKind is unsupported")
            nonempty(check["command"], f"{check_label}.command")
            require(check["status"] in {"passed", "failed"}, f"{check_label}.status is unsupported")
            for field in ("passed", "failed", "ignored", "durationMs"):
                nullable_count(check[field], f"{check_label}.{field}")
            evidence = check["evidence"]
            require(isinstance(evidence, dict), f"{check_label}.evidence must be an object")
            exact(evidence, {"jobId", "stdoutArtifactId", "stdoutDigest", "terminalEvidenceArtifactId", "terminalEvidenceDigest"}, f"{check_label}.evidence")
            for field in ("jobId", "stdoutArtifactId", "terminalEvidenceArtifactId"):
                nonempty(evidence[field], f"{check_label}.evidence.{field}")
            digest(evidence["stdoutDigest"], f"{check_label}.evidence.stdoutDigest")
            digest(evidence["terminalEvidenceDigest"], f"{check_label}.evidence.terminalEvidenceDigest")
            if check["checkKind"] == "test_suite":
                test_suites += 1
                require(all(check[field] is not None for field in ("passed", "failed", "ignored")), f"{check_label} test counts cannot be null")
                passed += check["passed"]
                failed += check["failed"]
                ignored += check["ignored"]
            else:
                contract_checks += 1
                require(all(check[field] is None for field in ("passed", "failed", "ignored")), f"{check_label} contract counts must remain null")
        require(len(check_ids) == len(set(check_ids)), f"{label} check identifiers must be unique")
    require(len(component_ids) == len(set(component_ids)), "component identifiers must be unique")

    aggregate = document["aggregate"]
    require(isinstance(aggregate, dict), "aggregate must be an object")
    exact(aggregate, {"testSuites", "contractChecks", "passed", "failed", "ignored", "productQualityClaim"}, "aggregate")
    expected_aggregate = {
        "testSuites": test_suites,
        "contractChecks": contract_checks,
        "passed": passed,
        "failed": failed,
        "ignored": ignored,
        "productQualityClaim": False,
    }
    require(aggregate == expected_aggregate, f"aggregate differs; expected={expected_aggregate}")
    string_list(document["limitations"], "limitations", minimum=1)
    validate_integrity(document)


def validate_summary(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "summaryId",
        "generatedAt",
        "suite",
        "source",
        "inventory",
        "groups",
        "comparisonCandidates",
        "policy",
        "limitations",
        "integrity",
    }
    exact(document, expected, "Evaluation Summary")
    require(document["schemaVersion"] == 1, "unsupported summary schemaVersion")
    require(document["kind"] == "ordivon.evaluation-summary", "unsupported summary kind")
    nonempty(document["summaryId"], "summaryId")
    nonempty(document["generatedAt"], "generatedAt")
    validate_file_ref(document["suite"], "suite")
    source = document["source"]
    require(isinstance(source, dict), "source must be an object")
    exact(source, {"recordCount", "recordSetDigest"}, "source")
    nullable_count(source["recordCount"], "source.recordCount")
    digest(source["recordSetDigest"], "source.recordSetDigest")
    inventory = document["inventory"]
    require(isinstance(inventory, dict), "inventory must be an object")
    exact(inventory, {"tasks", "trials", "results", "failures"}, "inventory")
    for field, value in inventory.items():
        nullable_count(value, f"inventory.{field}")
    require(source["recordCount"] == sum(inventory.values()), "source.recordCount differs from inventory")
    require(isinstance(document["groups"], list), "groups must be a list")
    require(isinstance(document["comparisonCandidates"], list), "comparisonCandidates must be a list")
    for candidate_index, candidate in enumerate(document["comparisonCandidates"]):
        label = f"comparisonCandidates[{candidate_index}]"
        require(isinstance(candidate, dict), f"{label} must be an object")
        exact(candidate, {"taskRef", "groupIds", "eligible", "blockers"}, label)
        require(isinstance(candidate["taskRef"], dict), f"{label}.taskRef must be an object")
        exact(candidate["taskRef"], {"taskId", "taskVersion"}, f"{label}.taskRef")
        nonempty(candidate["taskRef"]["taskId"], f"{label}.taskRef.taskId")
        require(isinstance(candidate["taskRef"]["taskVersion"], int) and candidate["taskRef"]["taskVersion"] >= 1, f"{label}.taskRef.taskVersion must be positive")
        string_list(candidate["groupIds"], f"{label}.groupIds", minimum=1, unique=True)
        require(isinstance(candidate["eligible"], bool), f"{label}.eligible must be boolean")
        blockers = string_list(candidate["blockers"], f"{label}.blockers", unique=True)
        require(candidate["eligible"] == (not blockers), f"{label}.eligible differs from blockers")
    policy = document["policy"]
    require(isinstance(policy, dict), "policy must be an object")
    exact(policy, {"minimumTrialsPerGroup", "globalScoreGenerated"}, "policy")
    require(isinstance(policy["minimumTrialsPerGroup"], int) and policy["minimumTrialsPerGroup"] >= 1, "minimumTrialsPerGroup must be positive")
    require(policy["globalScoreGenerated"] is False, "heterogeneous task groups cannot emit a global score")
    string_list(document["limitations"], "limitations", minimum=1)
    validate_integrity(document)


def validate_closeout(document: dict[str, Any]) -> None:
    expected = {
        "schemaVersion",
        "kind",
        "closeoutId",
        "capturedAt",
        "baseRevision",
        "implementationBranch",
        "implementationRevisions",
        "testedRevision",
        "conformance",
        "artifacts",
        "results",
        "integration",
        "nextGate",
        "limitations",
        "integrity",
    }
    exact(document, expected, "Evaluation P0 Closeout")
    require(document["schemaVersion"] == 1, "unsupported closeout schemaVersion")
    require(document["kind"] == "ordivon.evaluation-p0-closeout", "unsupported closeout kind")
    nonempty(document["closeoutId"], "closeoutId")
    nonempty(document["capturedAt"], "capturedAt")
    revision(document["baseRevision"], "baseRevision")
    nonempty(document["implementationBranch"], "implementationBranch")
    revisions = string_list(document["implementationRevisions"], "implementationRevisions", minimum=1, unique=True)
    for index, value in enumerate(revisions):
        revision(value, f"implementationRevisions[{index}]")
    revision(document["testedRevision"], "testedRevision")
    require(document["testedRevision"] in revisions, "testedRevision must be one of implementationRevisions")

    conformance = document["conformance"]
    require(isinstance(conformance, dict), "conformance must be an object")
    exact(
        conformance,
        {
            "status",
            "capturedAt",
            "receiptKind",
            "repositoryRevision",
            "receiptPayloadDigest",
            "runtimeJobId",
            "stdoutArtifactId",
            "stdoutDigest",
            "terminalEvidenceArtifactId",
            "terminalEvidenceDigest",
        },
        "conformance",
    )
    require(conformance["status"] == "passed", "closeout conformance must be passed")
    nonempty(conformance["capturedAt"], "conformance.capturedAt")
    require(conformance["receiptKind"] == "ordivon-conformance-gate", "unsupported conformance receipt kind")
    revision(conformance["repositoryRevision"], "conformance.repositoryRevision")
    require(conformance["repositoryRevision"] == document["testedRevision"], "conformance repositoryRevision differs from testedRevision")
    digest(conformance["receiptPayloadDigest"], "conformance.receiptPayloadDigest")
    for field in ("runtimeJobId", "stdoutArtifactId", "terminalEvidenceArtifactId"):
        nonempty(conformance[field], f"conformance.{field}")
    digest(conformance["stdoutDigest"], "conformance.stdoutDigest")
    digest(conformance["terminalEvidenceDigest"], "conformance.terminalEvidenceDigest")

    artifacts = document["artifacts"]
    require(isinstance(artifacts, dict), "artifacts must be an object")
    exact(artifacts, {"systemManifest", "componentBaseline", "dogfoodSummary", "suite"}, "artifacts")
    for name, reference in artifacts.items():
        validate_file_ref(reference, f"artifacts.{name}")

    results = document["results"]
    require(isinstance(results, dict), "results must be an object")
    exact(results, {"componentHealth", "dogfood", "trackRTests"}, "results")
    component = results["componentHealth"]
    require(isinstance(component, dict), "results.componentHealth must be an object")
    exact(component, {"testSuites", "contractChecks", "passed", "failed", "ignored", "productQualityClaim"}, "results.componentHealth")
    for field in ("testSuites", "contractChecks", "passed", "failed", "ignored"):
        require(isinstance(component[field], int) and not isinstance(component[field], bool) and component[field] >= 0, f"results.componentHealth.{field} must be non-negative")
    require(component["productQualityClaim"] is False, "component health cannot claim product quality")
    dogfood = results["dogfood"]
    require(isinstance(dogfood, dict), "results.dogfood must be an object")
    exact(dogfood, {"tasks", "trials", "results", "failures", "configurationGroups", "eligibleComparisons", "globalScoreGenerated"}, "results.dogfood")
    for field in ("tasks", "trials", "results", "failures", "configurationGroups", "eligibleComparisons"):
        require(isinstance(dogfood[field], int) and not isinstance(dogfood[field], bool) and dogfood[field] >= 0, f"results.dogfood.{field} must be non-negative")
    require(dogfood["globalScoreGenerated"] is False, "P0 dogfood cannot generate a global score")
    require(isinstance(results["trackRTests"], int) and results["trackRTests"] >= 1, "trackRTests must be positive")

    integration = document["integration"]
    require(isinstance(integration, dict), "integration must be an object")
    exact(integration, {"status", "targetBranch", "targetHeadAtCloseout", "blocker", "foreignIndexStats", "foreignIndexPaths"}, "integration")
    require(integration["status"] in {"ready_unmerged", "integrated"}, "unsupported integration status")
    nonempty(integration["targetBranch"], "integration.targetBranch")
    revision(integration["targetHeadAtCloseout"], "integration.targetHeadAtCloseout")
    stats = integration["foreignIndexStats"]
    require(isinstance(stats, dict), "integration.foreignIndexStats must be an object")
    exact(stats, {"files", "insertions", "deletions"}, "integration.foreignIndexStats")
    for field, value in stats.items():
        require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"integration.foreignIndexStats.{field} must be non-negative")
    paths = string_list(integration["foreignIndexPaths"], "integration.foreignIndexPaths", unique=True)
    require(stats["files"] == len(paths), "foreignIndexStats.files differs from foreignIndexPaths")
    if integration["status"] == "ready_unmerged":
        nonempty(integration["blocker"], "integration.blocker")
        require(bool(paths), "ready_unmerged closeout must identify blocking paths")
    else:
        require(integration["blocker"] is None, "integrated closeout blocker must be null")
        require(not paths, "integrated closeout cannot retain foreign blocking paths")

    next_gate = document["nextGate"]
    require(isinstance(next_gate, dict), "nextGate must be an object")
    exact(next_gate, {"stage", "taskId", "minimumTrialsPerConfiguration", "requirements"}, "nextGate")
    nonempty(next_gate["stage"], "nextGate.stage")
    nonempty(next_gate["taskId"], "nextGate.taskId")
    require(isinstance(next_gate["minimumTrialsPerConfiguration"], int) and next_gate["minimumTrialsPerConfiguration"] >= 1, "minimumTrialsPerConfiguration must be positive")
    string_list(next_gate["requirements"], "nextGate.requirements", minimum=1, unique=True)
    string_list(document["limitations"], "limitations", minimum=1)
    validate_integrity(document)


def validate_document(document: dict[str, Any]) -> None:
    kind = document.get("kind")
    if kind == "ordivon.evaluation-system-manifest":
        validate_system_manifest(document)
    elif kind == "ordivon.evaluation-suite":
        validate_suite(document)
    elif kind == "ordivon.component-test-baseline":
        validate_component_baseline(document)
    elif kind == "ordivon.evaluation-summary":
        validate_summary(document)
    elif kind == "ordivon.evaluation-p0-closeout":
        validate_closeout(document)
    else:
        raise ValueError(f"unsupported P0 artifact kind: {kind!r}")


def discover(paths: Iterable[Path]) -> list[Path]:
    discovered: list[Path] = []
    for path in paths:
        if path.is_dir():
            discovered.extend(sorted(path.rglob("*.json")))
        else:
            discovered.append(path)
    return sorted(set(discovered))


def load_documents(paths: Iterable[Path]) -> list[tuple[Path, dict[str, Any]]]:
    loaded: list[tuple[Path, dict[str, Any]]] = []
    for path in discover(paths):
        value = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(value, dict) and value.get("kind") in KINDS:
            loaded.append((path, value))
    require(bool(loaded), "no P0 artifacts found")
    return loaded


def write_digests(loaded: list[tuple[Path, dict[str, Any]]]) -> None:
    for path, document in loaded:
        document["integrity"] = {
            "algorithm": "sha256",
            "canonicalization": "ordivon-evidence-json-v1",
            "payloadDigest": payload_digest(document),
        }
        path.write_text(json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def validate_collection(loaded: list[tuple[Path, dict[str, Any]]], *, root: Path | None = None) -> None:
    identities: set[tuple[str, str]] = set()
    for _, document in loaded:
        validate_document(document)
        identity_field = {
            "ordivon.evaluation-system-manifest": "manifestId",
            "ordivon.evaluation-suite": "suiteId",
            "ordivon.component-test-baseline": "baselineId",
            "ordivon.evaluation-summary": "summaryId",
            "ordivon.evaluation-p0-closeout": "closeoutId",
        }[document["kind"]]
        identity = (document["kind"], document[identity_field])
        require(identity not in identities, f"duplicate P0 artifact identity: {identity}")
        identities.add(identity)

    if root is None:
        return
    root = root.resolve()
    for _, document in loaded:
        refs: list[dict[str, str]] = []
        if document["kind"] == "ordivon.evaluation-system-manifest":
            refs.append(document["systemSnapshot"])
            refs.extend(
                value
                for value in document["evaluationContract"].values()
                if isinstance(value, dict)
            )
        elif document["kind"] == "ordivon.component-test-baseline":
            refs.append(document["systemManifest"])
        elif document["kind"] == "ordivon.evaluation-summary":
            refs.append(document["suite"])
        elif document["kind"] == "ordivon.evaluation-p0-closeout":
            refs.extend(document["artifacts"].values())
        for reference in refs:
            path = (root / reference["path"]).resolve()
            require(path.is_relative_to(root), f"reference escapes root: {reference['path']}")
            require(path.is_file(), f"referenced file is missing: {reference['path']}")
            require(file_digest(path) == reference["digest"], f"referenced file digest differs: {reference['path']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--write-digests", action="store_true")
    args = parser.parse_args()
    loaded = load_documents(args.paths)
    if args.write_digests:
        write_digests(loaded)
        loaded = load_documents(args.paths)
    validate_collection(loaded, root=args.root)
    print(
        json.dumps(
            {
                "schemaVersion": 1,
                "kind": "ordivon.evaluation-p0-validation-result",
                "ok": True,
                "records": len(loaded),
                "paths": [str(path) for path, _ in loaded],
            },
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
