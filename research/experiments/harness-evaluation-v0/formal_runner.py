from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterable

JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]

RUNNER_STATE_KIND = "ordivon.evaluation-runner-state"
TRIAL_INTENT_KIND = "ordivon.evaluation-trial-intent"
TRIAL_DISPOSITION_KIND = "ordivon.evaluation-trial-disposition"
RUNNER_SCHEMA_VERSION = 1
RUNNER_STAGES = (
    "planned",
    "prepared",
    "executing",
    "evidence_collected",
    "verified",
    "disposed",
    "closed",
)
VALIDITY_VALUES = frozenset({"valid", "invalid", "unknown"})
SEMANTIC_OUTCOMES = frozenset(
    {"accepted", "rejected", "not_reached", "not_applicable", "unknown"}
)
COMPARATIVE_OUTCOMES = frozenset(
    {"improved", "equivalent", "regressed", "inconclusive", "not_applicable", "unknown"}
)
FAILURE_ATTRIBUTIONS = frozenset(
    {"none", "candidate", "infrastructure", "evaluator", "environment", "policy", "multiple", "unknown"}
)

_FORBIDDEN_KEYS = frozenset(
    {
        "api_key",
        "apikey",
        "authorization",
        "bearer_token",
        "password",
        "private_reasoning",
        "raw_reasoning",
        "secret",
        "token",
    }
)
_FORBIDDEN_TEXT = (
    "bearer ",
    "/root/.config/ordivon/secrets",
    "private reasoning",
    "raw chain of thought",
)


class FormalRunnerError(RuntimeError):
    pass


class FormalRunnerConflict(FormalRunnerError):
    pass


class FormalRunnerPolicyError(FormalRunnerError):
    pass


def canonical_bytes(value: JsonValue) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_digest(value: JsonValue) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value)).hexdigest()


def with_integrity(value: dict[str, JsonValue]) -> dict[str, JsonValue]:
    if "integrity" in value:
        raise ValueError("integrity is owned by the formal runner")
    result = dict(value)
    result["integrity"] = {
        "algorithm": "sha256",
        "canonicalization": "ordivon-evidence-json-v1",
        "payloadDigest": canonical_digest(value),
    }
    return result


def verify_integrity(value: dict[str, Any]) -> None:
    integrity = value.get("integrity")
    if not isinstance(integrity, dict) or set(integrity) != {
        "algorithm",
        "canonicalization",
        "payloadDigest",
    }:
        raise FormalRunnerError("record integrity object differs")
    if integrity.get("algorithm") != "sha256" or integrity.get(
        "canonicalization"
    ) != "ordivon-evidence-json-v1":
        raise FormalRunnerError("record integrity algorithm differs")
    payload = dict(value)
    payload.pop("integrity")
    if integrity.get("payloadDigest") != canonical_digest(payload):
        raise FormalRunnerError("record integrity digest differs")


def reject_sensitive_content(value: JsonValue, *, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            lowered = key.lower()
            normalized = "".join(character for character in lowered if character.isalnum())
            forbidden_normalized = {
                "apikey",
                "authorization",
                "bearertoken",
                "password",
                "privatereasoning",
                "rawreasoning",
                "secret",
                "token",
            }
            if lowered in _FORBIDDEN_KEYS or normalized in forbidden_normalized:
                raise FormalRunnerPolicyError(f"sensitive field is forbidden at {path}.{key}")
            reject_sensitive_content(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_sensitive_content(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if any(token in lowered for token in _FORBIDDEN_TEXT):
            raise FormalRunnerPolicyError(f"sensitive text is forbidden at {path}")


def validate_completion_artifact(
    value: dict[str, Any],
    *,
    task_id: str,
    task_version: int,
    source_revision: str,
) -> dict[str, Any]:
    expected = {
        "schemaVersion",
        "kind",
        "taskId",
        "taskVersion",
        "sourceRevision",
        "changedPaths",
        "visibleCheck",
        "finalSourceDigest",
        "summary",
    }
    if set(value) != expected:
        raise FormalRunnerPolicyError("Completion Artifact fields differ")
    if (
        value["schemaVersion"] != 1
        or value["kind"] != "ordivon.evaluation-completion-artifact"
        or value["taskId"] != task_id
        or value["taskVersion"] != task_version
        or value["sourceRevision"] != source_revision
    ):
        raise FormalRunnerPolicyError("Completion Artifact identity differs")
    if value["changedPaths"] != ["allocation.py"]:
        raise FormalRunnerPolicyError(
            "Completion Artifact may claim only allocation.py as the source change"
        )
    visible = value["visibleCheck"]
    if (
        not isinstance(visible, dict)
        or set(visible) != {"checkId", "status"}
        or visible.get("checkId") != "visible-tests"
        or visible.get("status") != "passed"
    ):
        raise FormalRunnerPolicyError("Completion Artifact visible Check differs")
    digest_value = value["finalSourceDigest"]
    if (
        not isinstance(digest_value, str)
        or len(digest_value) != 71
        or not digest_value.startswith("sha256:")
    ):
        raise FormalRunnerPolicyError("Completion Artifact source digest differs")
    try:
        int(digest_value[7:], 16)
    except ValueError as error:
        raise FormalRunnerPolicyError(
            "Completion Artifact source digest is not hexadecimal"
        ) from error
    summary = value["summary"]
    if not isinstance(summary, str) or not summary.strip() or len(summary.encode()) > 2_048:
        raise FormalRunnerPolicyError("Completion Artifact summary differs")
    reject_sensitive_content(value)
    return value


def _private_directory(path: Path, *, create: bool) -> Path:
    value = path.expanduser()
    if value.is_symlink():
        raise FormalRunnerPolicyError("Trial root cannot be a symlink")
    if not value.exists():
        if not create:
            raise FileNotFoundError(value)
        value.mkdir(parents=True, mode=0o700)
        os.chmod(value, 0o700)
    resolved = value.resolve(strict=True)
    if not resolved.is_dir() or stat.S_IMODE(resolved.stat().st_mode) != 0o700:
        raise FormalRunnerPolicyError("Trial root must be a private 0700 directory")
    return resolved


def _read_json(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise FormalRunnerPolicyError(f"record is not a regular file: {path.name}")
    if stat.S_IMODE(path.stat().st_mode) != 0o600:
        raise FormalRunnerPolicyError(f"record is not private 0600: {path.name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise FormalRunnerError(f"record must be an object: {path.name}")
    verify_integrity(value)
    reject_sensitive_content(value)
    return value


def _atomic_write(path: Path, value: dict[str, JsonValue]) -> None:
    reject_sensitive_content(value)
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    ).encode("utf-8") + b"\n"
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _write_once(path: Path, value: dict[str, JsonValue]) -> None:
    if path.exists():
        current = _read_json(path)
        if current != value:
            raise FormalRunnerConflict(f"write-once record differs: {path.name}")
        return
    _atomic_write(path, value)


@dataclass(frozen=True, slots=True)
class TrialDisposition:
    trial_id: str
    validity: str
    semantic_outcome: str
    comparative_outcome: str
    failure_attribution: str
    comparison_eligible: bool
    reasons: tuple[str, ...]
    selection_digest: str

    def __post_init__(self) -> None:
        if not self.trial_id or self.trial_id != self.trial_id.strip():
            raise ValueError("Trial identity must be non-empty and trimmed")
        if self.validity not in VALIDITY_VALUES:
            raise ValueError(f"unsupported Trial validity: {self.validity}")
        if self.semantic_outcome not in SEMANTIC_OUTCOMES:
            raise ValueError(f"unsupported semantic outcome: {self.semantic_outcome}")
        if self.comparative_outcome not in COMPARATIVE_OUTCOMES:
            raise ValueError(
                f"unsupported comparative outcome: {self.comparative_outcome}"
            )
        if self.failure_attribution not in FAILURE_ATTRIBUTIONS:
            raise ValueError(
                f"unsupported failure attribution: {self.failure_attribution}"
            )
        if len(self.selection_digest) != 71 or not self.selection_digest.startswith(
            "sha256:"
        ):
            raise ValueError("Selection digest must be sha256:<64 hex>")
        if self.comparison_eligible and self.validity != "valid":
            raise ValueError("only a valid Trial can be comparison-eligible")
        if self.comparison_eligible and self.semantic_outcome not in {
            "accepted",
            "rejected",
        }:
            raise ValueError(
                "comparison-eligible Trial requires an adjudicated semantic outcome"
            )
        if self.validity == "valid" and self.failure_attribution in {
            "infrastructure",
            "evaluator",
            "environment",
            "unknown",
        }:
            raise ValueError(
                "valid Trial cannot retain unresolved infrastructure/evaluator/environment attribution"
            )
        if len(self.reasons) != len(set(self.reasons)):
            raise ValueError("Disposition reasons must be unique")

    def to_dict(self) -> dict[str, JsonValue]:
        return with_integrity(
            {
                "schemaVersion": RUNNER_SCHEMA_VERSION,
                "kind": TRIAL_DISPOSITION_KIND,
                "trialId": self.trial_id,
                "validity": self.validity,
                "semanticOutcome": self.semantic_outcome,
                "comparativeOutcome": self.comparative_outcome,
                "failureAttribution": self.failure_attribution,
                "comparisonEligible": self.comparison_eligible,
                "reasons": list(self.reasons),
                "selectionDigest": self.selection_digest,
            }
        )


class TrialRecordStore:
    def __init__(self, root: str | Path) -> None:
        self.root = _private_directory(Path(root), create=False)
        self.intent_path = self.root / "intent.json"
        self.state_path = self.root / "runner-state.json"

    @classmethod
    def initialize(
        cls,
        root: str | Path,
        *,
        trial_id: str,
        configuration_id: str,
        task_ref: dict[str, JsonValue],
        created_at_ms: int,
    ) -> "TrialRecordStore":
        if created_at_ms < 0:
            raise ValueError("Trial creation time must be non-negative")
        private_root = _private_directory(Path(root), create=True)
        store = cls(private_root)
        intent = with_integrity(
            {
                "schemaVersion": RUNNER_SCHEMA_VERSION,
                "kind": TRIAL_INTENT_KIND,
                "trialId": trial_id,
                "configurationId": configuration_id,
                "taskRef": task_ref,
                "createdAtMs": created_at_ms,
            }
        )
        _write_once(store.intent_path, intent)
        if store.state_path.exists():
            state = store.state()
            if state["trialId"] != trial_id:
                raise FormalRunnerConflict("existing Runner state belongs to another Trial")
        else:
            _atomic_write(
                store.state_path,
                with_integrity(
                    {
                        "schemaVersion": RUNNER_SCHEMA_VERSION,
                        "kind": RUNNER_STATE_KIND,
                        "trialId": trial_id,
                        "stage": "planned",
                        "revision": 1,
                        "updatedAtMs": created_at_ms,
                        "recordDigests": {},
                    }
                ),
            )
        return store

    @property
    def trial_id(self) -> str:
        intent = self.intent()
        value = intent.get("trialId")
        if not isinstance(value, str):
            raise FormalRunnerError("Trial intent omitted trialId")
        return value

    def intent(self) -> dict[str, Any]:
        return _read_json(self.intent_path)

    def state(self) -> dict[str, Any]:
        value = _read_json(self.state_path)
        if value.get("kind") != RUNNER_STATE_KIND:
            raise FormalRunnerError("Runner state kind differs")
        stage = value.get("stage")
        if stage not in RUNNER_STAGES:
            raise FormalRunnerError("Runner state stage differs")
        return value

    def write_record(
        self,
        name: str,
        value: dict[str, JsonValue],
        *,
        minimum_stage: str | None = None,
    ) -> str:
        if not name or "/" in name or name.startswith(".") or not name.endswith(".json"):
            raise ValueError("record name must be one simple .json filename")
        state = self.state()
        if minimum_stage is not None and RUNNER_STAGES.index(state["stage"]) < RUNNER_STAGES.index(
            minimum_stage
        ):
            raise FormalRunnerConflict(
                f"record {name} requires stage {minimum_stage}, observed {state['stage']}"
            )
        record = value if "integrity" in value else with_integrity(value)
        verify_integrity(record)
        reject_sensitive_content(record)
        path = self.root / name
        _write_once(path, record)
        digest = record["integrity"]["payloadDigest"]
        if not isinstance(digest, str):
            raise FormalRunnerError("record digest is not a string")
        return digest

    def record(self, name: str) -> dict[str, Any]:
        return _read_json(self.root / name)

    def advance(
        self,
        *,
        expected_stage: str,
        next_stage: str,
        updated_at_ms: int,
        records: Iterable[str] = (),
    ) -> dict[str, Any]:
        if expected_stage not in RUNNER_STAGES or next_stage not in RUNNER_STAGES:
            raise ValueError("Runner stage is unsupported")
        if RUNNER_STAGES.index(next_stage) != RUNNER_STAGES.index(expected_stage) + 1:
            raise ValueError("Runner state may advance exactly one stage")
        if updated_at_ms < 0:
            raise ValueError("Runner update time must be non-negative")
        current = self.state()
        if current["stage"] != expected_stage:
            if current["stage"] == next_stage:
                return current
            raise FormalRunnerConflict(
                f"Runner stage differs: expected {expected_stage}, observed {current['stage']}"
            )
        record_digests = dict(current["recordDigests"])
        for name in records:
            record = self.record(name)
            digest = record["integrity"]["payloadDigest"]
            if not isinstance(digest, str):
                raise FormalRunnerError(f"record {name} omitted digest")
            existing = record_digests.get(name)
            if existing is not None and existing != digest:
                raise FormalRunnerConflict(f"Runner record digest changed: {name}")
            record_digests[name] = digest
        next_value = with_integrity(
            {
                "schemaVersion": RUNNER_SCHEMA_VERSION,
                "kind": RUNNER_STATE_KIND,
                "trialId": current["trialId"],
                "stage": next_stage,
                "revision": current["revision"] + 1,
                "updatedAtMs": updated_at_ms,
                "recordDigests": dict(sorted(record_digests.items())),
            }
        )
        _atomic_write(self.state_path, next_value)
        return next_value

    def record_selection(
        self,
        selection: dict[str, JsonValue],
        *,
        require_complete: bool = False,
    ) -> str:
        if selection.get("kind") != "ordivon.observation-selection-manifest":
            raise FormalRunnerPolicyError("Observation Selection kind differs")
        completeness = selection.get("completeness")
        privacy = selection.get("privacy")
        if not isinstance(completeness, dict):
            raise FormalRunnerPolicyError("Observation Selection completeness differs")
        if completeness.get("trialValidityInferred") is not False:
            raise FormalRunnerPolicyError(
                "Observation Selection must not infer Trial validity"
            )
        if require_complete and completeness.get("complete") is not True:
            raise FormalRunnerPolicyError("Observation Selection is incomplete")
        if not isinstance(privacy, dict) or privacy.get("metadataOnly") is not True:
            raise FormalRunnerPolicyError("Observation Selection is not metadata-only")
        if privacy.get("payloadBytesCopied") is not False or privacy.get(
            "secretForbiddenPresent"
        ) is not False:
            raise FormalRunnerPolicyError("Observation Selection privacy gate failed")
        selection_digest = selection.get("selectionDigest")
        if (
            not isinstance(selection_digest, str)
            or len(selection_digest) != 71
            or not selection_digest.startswith("sha256:")
            or any(
                character not in "0123456789abcdef"
                for character in selection_digest[7:]
            )
        ):
            raise FormalRunnerPolicyError("Observation Selection digest is invalid")
        return self.write_record(
            "observation-selection.json",
            selection,
            minimum_stage="evidence_collected",
        )

    def admit_selection(self, selection: dict[str, JsonValue]) -> str:
        return self.record_selection(selection, require_complete=True)

    def dispose(self, disposition: TrialDisposition, *, updated_at_ms: int) -> dict[str, Any]:
        if disposition.trial_id != self.trial_id:
            raise FormalRunnerConflict("Disposition belongs to another Trial")
        selection = self.record("observation-selection.json")
        if disposition.selection_digest != selection.get("selectionDigest"):
            raise FormalRunnerConflict("Disposition Selection digest differs")
        completeness = selection.get("completeness")
        selection_complete = (
            isinstance(completeness, dict)
            and completeness.get("complete") is True
        )
        if disposition.validity == "valid" and not selection_complete:
            raise FormalRunnerPolicyError(
                "valid Trial requires a complete Observation Selection"
            )
        if disposition.comparison_eligible and not selection_complete:
            raise FormalRunnerPolicyError(
                "comparison-eligible Trial requires a complete Observation Selection"
            )
        self.write_record(
            "disposition.json",
            disposition.to_dict(),
            minimum_stage="verified",
        )
        return self.advance(
            expected_stage="verified",
            next_stage="disposed",
            updated_at_ms=updated_at_ms,
            records=("disposition.json", "observation-selection.json"),
        )

    def doctor(self) -> dict[str, JsonValue]:
        intent = self.intent()
        state = self.state()
        if intent["trialId"] != state["trialId"]:
            raise FormalRunnerError("Trial intent and Runner state identities differ")
        checked = 0
        for name, expected_digest in state["recordDigests"].items():
            record = self.record(name)
            if record["integrity"]["payloadDigest"] != expected_digest:
                raise FormalRunnerError(f"Runner record digest differs: {name}")
            checked += 1
        temporary_files = [path.name for path in self.root.glob(".*.tmp")]
        if temporary_files:
            raise FormalRunnerError(
                f"Runner temporary files remain: {sorted(temporary_files)}"
            )
        return {
            "schemaVersion": 1,
            "kind": "ordivon.evaluation-runner-doctor",
            "healthy": True,
            "trialId": self.trial_id,
            "stage": state["stage"],
            "revision": state["revision"],
            "checkedRecords": checked,
            "temporaryFiles": [],
        }


__all__ = [
    "COMPARATIVE_OUTCOMES",
    "FAILURE_ATTRIBUTIONS",
    "FormalRunnerConflict",
    "FormalRunnerError",
    "FormalRunnerPolicyError",
    "RUNNER_STAGES",
    "SEMANTIC_OUTCOMES",
    "TRIAL_DISPOSITION_KIND",
    "TRIAL_INTENT_KIND",
    "TrialDisposition",
    "TrialRecordStore",
    "VALIDITY_VALUES",
    "canonical_bytes",
    "canonical_digest",
    "reject_sensitive_content",
    "validate_completion_artifact",
    "verify_integrity",
    "with_integrity",
]
