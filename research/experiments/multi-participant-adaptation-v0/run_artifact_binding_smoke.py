from __future__ import annotations
import argparse,json,tempfile
from pathlib import Path
from anc_canonical import canonical_digest
from ordivon_host import EventKind, GoalCoordinatorHost, HostKernel, HostStorage, TaskDescriptor, VerificationReceipt, VerificationResultItem
from ordivon_host.coordination import CoordinationSuperseded

def run()->dict:
    goal='goal:p4:artifact-binding'; tasks=(('task:p4:artifact:branch-a','participant:p4:artifact-a'),('task:p4:artifact:branch-b','participant:p4:artifact-b')); clock_value=[500]
    def clock(): clock_value[0]+=1; return clock_value[0]
    with tempfile.TemporaryDirectory(prefix='ordivon-p4-artifact-') as td:
        root=Path(td)/'state'
        with HostStorage(root) as storage:
            kernel=HostKernel(storage,clock_ms=clock,owner_id='host:p4:artifact-binding')
            for task,participant in tasks:
                d=TaskDescriptor(task_id=task,goal_id=goal,workload_id='ordivon.computing.p4.artifact-binding.v1',assignee_ref=participant,provider_policy_ref='provider-policy:fixture',domain_ref='p4-mechanical-smoke'); o=storage.put_object(d.to_dict(),kind='task-descriptor'); kernel.create_task(event_id=f'event:{task}:created',kind=EventKind.TASK_CREATED,task_id=task,goal_id=goal,payload={'descriptorDigest':d.digest,'descriptorObjectDigest':o.digest},frontier=('node:p4:candidate',),referenced_objects=(o,))
            coordinator=GoalCoordinatorHost(storage,clock_ms=clock); initial=coordinator.snapshot(goal); artifact_objects=[]
            for index,(task,participant) in enumerate(tasks):
                artifact=storage.put_object({'schemaVersion':1,'kind':'ordivon.p4-branch-artifact','taskId':task,'participantRef':participant,'candidateSourceDigest':'sha256:'+('a' if index==0 else 'b')*64},kind='p4-branch-artifact'); artifact_objects.append(artifact)
                ref=initial.task(task); coordinator.transition_task(task_ref=ref,event_id=f'event:{task}:candidate-submitted',kind=EventKind('p4.candidate-submitted'),payload={'candidateArtifactDigest':artifact.digest,'participantRef':participant},state=ref.state,frontier=('node:p4:verify',),referenced_objects=(artifact,))
            candidate_bound=coordinator.snapshot(goal)
            initial_stale=False
            try: coordinator.assert_current(initial)
            except CoordinationSuperseded: initial_stale=True
            receipt=VerificationReceipt(dispatch_id='dispatch:p4:artifact-binding:verify',method='p4-artifact-binding-smoke.v1',accepted=True,observation_digest=canonical_digest({'artifacts':[x.digest for x in artifact_objects]}),result_items=tuple(VerificationResultItem(subject_ref=task,decision_digest=artifact_objects[i].digest,status='succeeded' if i==0 else 'not-selected',reason=None if i==0 else 'deterministic-join-not-selected',evidence_digest=artifact_objects[i].digest) for i,(task,_) in enumerate(tasks)))
            first=coordinator.apply_verification_result(task_ref=candidate_bound.task(tasks[0][0]),verification=receipt,next_frontier='node:p4:done',event_id='event:p4:artifact:a-result')
            candidate_snapshot_stale=False
            try: coordinator.assert_current(candidate_bound)
            except CoordinationSuperseded: candidate_snapshot_stale=True
        with HostStorage(root) as storage:
            fresh=GoalCoordinatorHost(storage,clock_ms=clock); second=fresh.apply_verification_result(task_ref=candidate_bound.task(tasks[1][0]),verification=receipt,next_frontier='node:p4:done',event_id='event:p4:artifact:b-result'); final=fresh.snapshot(goal)
            retained=[storage.objects.inspect(x.digest).kind for x in artifact_objects]
            task_events=[storage.read_task_event(task).data for task,_ in tasks]
        return {'schemaVersion':1,'kind':'ordivon.p4-artifact-binding-smoke','goalId':goal,'taskCount':2,'participantCount':2,'artifactDigests':[x.digest for x in artifact_objects],'artifactKindsAfterReopen':retained,'initialSnapshotStaleAfterArtifactBinding':initial_stale,'candidateBoundSnapshotStaleAfterFirstResult':candidate_snapshot_stale,'partialApplyReopenPassed':first.revision==candidate_bound.task(tasks[0][0]).revision+1 and second.revision==candidate_bound.task(tasks[1][0]).revision+1,'allFinalRevisionsAdvanced':all(x.revision==candidate_bound.task(x.task_id).revision+1 for x in final.tasks),'taskEventsCarryVerification':all(isinstance(x,dict) and 'verificationDigest' in x for x in task_events),'newCoordinationPrimitiveUsed':False,'coordinationSurface':'ordivon_host.GoalCoordinatorHost + Host StoredObject references'}
def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args(); result=run(); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps(result,sort_keys=True)); return 0 if all((result['initialSnapshotStaleAfterArtifactBinding'],result['candidateBoundSnapshotStaleAfterFirstResult'],result['partialApplyReopenPassed'],result['allFinalRevisionsAdvanced'],result['taskEventsCarryVerification'],not result['newCoordinationPrimitiveUsed'])) else 2
if __name__=='__main__': raise SystemExit(main())
