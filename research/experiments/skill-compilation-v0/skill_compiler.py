from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()


def compile_candidates(discovery: dict[str, Any]) -> dict[str, Any]:
    incidents=discovery["actualRuntimeEvidence"]
    classes={x["operationClass"] for x in incidents}
    branches=discovery["currentContractBranches"]
    repeated=len(incidents)>=3 and len(classes)>=2
    source_control=discovery["negativeOwnershipControl"]
    source_decision={
        "candidate":source_control["candidate"],
        "admission":"rejected",
        "reason":"deterministic_classical_mechanics_and_publication_consequence_belong_to_git_runtime_and_owner_authority",
    }
    if not repeated:
        return {"sourceLanding":source_decision,"recoverySkill":None}
    procedure=(
        "When a Tool response is UNKNOWN or lost, do not equate delivery loss with operation failure. "
        "First recover the exact durable identity or inspect exact physical state. For Runtime durable exec/execPlan/execBound, "
        "query task.list by the exact clientRequestId; consume/observe an existing Job, and only admit the same request after proving no Job exists. "
        "For workspace.open with an explicit workspaceId, use workspace.get and do not repeat open blindly. "
        "For workspace.patch, use workspace.patch.get before another patch. For workspace.mutate, which has no durable replay receipt, "
        "read/get/changes the exact target and retry only after proving the intended mutation was not applied. "
        "For Host task.checkpoint, replay the identical checkpoint against the original expectedRevision so an already-committed transition converges. "
        "If a Runtime process may have performed an external effect, reconcile the Runtime Job and then observe the external authority before any redispatch; "
        "Runtime execution identity does not make the external effect idempotent."
    )
    skill={
        "schemaVersion":1,
        "kind":"ordivon.skill-candidate",
        "skillId":"skill:reconcile-before-redispatch:v1",
        "status":"research_candidate",
        "owner":"ordivon-computing-research",
        "selectionOwnerHypothesis":"Harness_or_primary_Agent",
        "executionOwner":"existing_Tool_Runtime_Host_or_domain_authority",
        "purpose":"Choose the safe recovery procedure after response loss without creating a second execution authority.",
        "trigger":"tool_response_unknown_or_lost",
        "procedureText":procedure,
        "evidenceBasis":[x["incidentId"] for x in incidents],
        "operationClasses":[x["operationClass"] for x in branches],
        "forbidden":["blind_redispatch","infer_domain_failure_from_transport_loss","claim_external_effect_idempotency","create_new_execution_authority"],
        "promotionBoundary":"research_skill_only_until_live_holdout_and_owner_consumer",
        "deletionTrigger":"raw_tool_contract_facts_match_or_exceed_skill_on_holdout_or_skill_adds_no_decision_value",
    }
    skill["integrity"]={"algorithm":"sha256","payloadDigest":digest(skill)}
    return {"sourceLanding":source_decision,"recoverySkill":skill}


def main() -> int:
    root=Path(__file__).resolve().parent
    discovery=json.loads((root/'fixtures/discovery-incidents.json').read_text())
    result=compile_candidates(discovery)
    out=root/'skill/reconcile-before-redispatch.skill.json'; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result["recoverySkill"],indent=2,ensure_ascii=False)+"\n")
    receipt={"schemaVersion":1,"kind":"ordivon.skill-compilation-receipt","sourceLandingControl":result["sourceLanding"],"compiledSkillRef":"skill/reconcile-before-redispatch.skill.json","skillDigest":result["recoverySkill"]["integrity"]["payloadDigest"]}
    receipt["integrity"]={"algorithm":"sha256","payloadDigest":digest(receipt)}
    (root/'compilation-receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(receipt,sort_keys=True))
    return 0

if __name__=='__main__': raise SystemExit(main())
