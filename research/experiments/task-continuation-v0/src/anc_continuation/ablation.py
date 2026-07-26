from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from anc_canonical import JsonValue, canonical_bytes

from .context import ContextCompiler
from .store import FileObjectStore
from .validation import CapsuleValidationError, CapsuleValidator
from .workload import baseline_receipt, load_manifest


def capsule_ablation_receipt(checkpoint_root: str | Path) -> dict[str, JsonValue]:
    root = Path(checkpoint_root)
    manifest = load_manifest(root)
    store = FileObjectStore(root / "objects")
    capsule = store.get_capsule(str(manifest["capsuleDigest"]))
    variants = {
        "full": capsule,
        "withoutDecisionArtifact": replace(capsule, artifacts=()),
        "withoutCheckpointFact": replace(capsule, facts=()),
        "withoutCurrentBinding": replace(capsule, current_bindings=()),
        "withoutCompletedEffects": replace(capsule, completed_effects=()),
    }
    results: list[JsonValue] = []
    for name, variant in variants.items():
        try:
            report = CapsuleValidator(store).validate(variant, world_root=root)
            context = ContextCompiler().compile(variant, report)
            outcome = "valid"
            failure = None
            provenance_complete = bool(report.completed_effect_ids)
            forbidden_effect_count = len(context.payload["forbiddenEffects"])
        except CapsuleValidationError as error:
            outcome = "fail-closed"
            failure = str(error)
            provenance_complete = False
            forbidden_effect_count = 0
        results.append(
            {
                "variant": name,
                "bytes": len(canonical_bytes(variant.to_dict())),
                "outcome": outcome,
                "failure": failure,
                "provenanceComplete": provenance_complete,
                "forbiddenEffectCount": forbidden_effect_count,
            }
        )
    baselines = baseline_receipt(root)
    return {
        "schemaVersion": 1,
        "kind": "anc.task-capsule-ablation-receipt",
        "sourceRevision": manifest["sourceRevision"],
        "capsuleDigest": manifest["capsuleDigest"],
        "capsuleVariants": results,
        "baselineResults": baselines["results"],
    }
