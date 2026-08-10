from __future__ import annotations
import tempfile
from pathlib import Path
from typing import Any
from anc_canonical import canonical_digest
from ordivon_host import EventKind, GoalCoordinatorHost, HostKernel, HostStorage, TaskDescriptor, VerificationReceipt, VerificationResultItem
from ordivon_host.coordination import CoordinationError, CoordinationSuperseded

def exercise_host_coordination(*,scenario_id:str,treatment:str,candidates:list[dict[str,Any]],join:dict[str,Any])->dict[str,Any]:
    goal_id=f'goal:p4:{scenario_id}:{treatment}'; selected=join['selectedArtifactDigest']
    specs=[(f'task:p4:{scenario_id}:single','participant:p4:single')] if treatment=='single-reflect' else [(f'task:p4:{scenario_id}:branch-a','participant:p4:branch-a'),(f'task:p4:{scenario_id}:branch-b','participant:p4:branch-b')]
    with tempfile.TemporaryDirectory(prefix='ordivon-p4-host-') as td:
        root=Path(td)/'state'; clock_value=[100]
        def clock(): clock_value[0]+=1; return clock_value[0]
        with HostStorage(root) as storage:
            kernel=HostKernel(storage,clock_ms=clock,owner_id=f'host:p4:{treatment}')
            for task_id,participant in specs:
                descriptor=TaskDescriptor(task_id=task_id,goal_id=goal_id,workload_id='ordivon.computing.p4.repair.v1',assignee_ref=participant,provider_policy_ref='provider-policy:deepseek-v4-flash',domain_ref=f'p4-scenario:{scenario_id}')
                obj=storage.put_object(descriptor.to_dict(),kind='task-descriptor')
                kernel.create_task(event_id=f'event:{task_id}:created',kind=EventKind.TASK_CREATED,task_id=task_id,goal_id=goal_id,payload={'descriptorDigest':descriptor.digest,'descriptorObjectDigest':obj.digest},frontier=(f'node:p4:{scenario_id}:candidate',),referenced_objects=(obj,))
            coordinator=GoalCoordinatorHost(storage,clock_ms=clock); frozen=coordinator.snapshot(goal_id)
            candidate_objects={c['candidateId']:storage.put_object({'schemaVersion':1,'kind':'ordivon.p4-candidate-artifact','candidateId':c['candidateId'],'artifactDigest':c['artifactDigest'],'sourceDigest':c['sourceDigest'],'summary':c['summary']},kind='p4-candidate-artifact') for c in candidates}
            items=[]
            if treatment=='single-reflect':
                task_id=specs[0][0]; status='succeeded' if join['accepted'] else 'failed'; reason=None if join['accepted'] else 'no-candidate-passed-verifier'
                items.append(VerificationResultItem(subject_ref=task_id,decision_digest=selected,status=status,reason=reason,evidence_digest=canonical_digest({'candidates':[c['artifactDigest'] for c in candidates],'join':join})))
            else:
                selected_id=join['selectedCandidateId']
                for index,(task_id,_) in enumerate(specs):
                    c=candidates[index]; status='succeeded' if join['accepted'] and c['candidateId']==selected_id else ('not-selected' if join['accepted'] else 'failed'); reason=None if status=='succeeded' else ('deterministic-join-not-selected' if join['accepted'] else 'no-candidate-passed-verifier')
                    items.append(VerificationResultItem(subject_ref=task_id,decision_digest=c['artifactDigest'],status=status,reason=reason,evidence_digest=canonical_digest({'candidate':c['artifactDigest'],'authoritative':c['evaluation']['authoritative']})))
            receipt=VerificationReceipt(dispatch_id=f'dispatch:p4:{scenario_id}:{treatment}:verify',method='hidden-repair-verifier.v1',accepted=join['accepted'],observation_digest=canonical_digest({'scenarioId':scenario_id,'join':join}),result_items=tuple(items))
            stale_blocked=False; rejected_advance_blocked=False; applied=[]
            if join['accepted']:
                first_ref=frozen.task(specs[0][0]); first=coordinator.apply_verification_result(task_ref=first_ref,verification=receipt,next_frontier=f'node:p4:{scenario_id}:done',event_id=f'event:{specs[0][0]}:verified'); applied.append(first.task_id)
                try: coordinator.assert_current(frozen)
                except CoordinationSuperseded: stale_blocked=True
            else:
                try: coordinator.apply_verification_result(task_ref=frozen.task(specs[0][0]),verification=receipt,next_frontier=f'node:p4:{scenario_id}:done',event_id=f'event:{specs[0][0]}:rejected')
                except CoordinationError: rejected_advance_blocked=True
        if join['accepted'] and len(specs)>1:
            with HostStorage(root) as storage:
                fresh=GoalCoordinatorHost(storage,clock_ms=clock); second=fresh.apply_verification_result(task_ref=frozen.task(specs[1][0]),verification=receipt,next_frontier=f'node:p4:{scenario_id}:done',event_id=f'event:{specs[1][0]}:verified'); applied.append(second.task_id); final=fresh.snapshot(goal_id); recovery_ok=len(final.tasks)==len(specs) and all(x.revision==frozen.task(x.task_id).revision+1 for x in final.tasks)
        else: recovery_ok=(join['accepted'] and len(specs)==1) or (not join['accepted'])
    assignees=[p for _,p in specs]
    return {'goalId':goal_id,'taskCount':len(specs),'participantCount':len(set(assignees)),'responsibilityAmbiguous':any(not p for p in assignees),'candidateArtifactCount':len(candidate_objects),'branchEffectIntentCount':0,'verificationAccepted':join['accepted'],'appliedTaskIds':applied,'staleSnapshotBlocked':stale_blocked if join['accepted'] else None,'rejectedAdvanceBlocked':rejected_advance_blocked if not join['accepted'] else None,'partialApplyRecoveryPassed':recovery_ok,'snapshotDigest':frozen.digest,'verificationDigest':canonical_digest(receipt.to_dict())}
