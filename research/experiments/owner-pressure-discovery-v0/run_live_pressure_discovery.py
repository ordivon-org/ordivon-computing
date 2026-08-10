from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
COMPUTING_ROOT = HERE.parents[2]
HARNESS_ROOT = Path('/root/projects/ordivon-harness')
for path in (COMPUTING_ROOT / 'packages/ordivon-protocol/src', HARNESS_ROOT / 'src', HERE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from anc_canonical import canonical_digest
from evaluator import evaluate
from ordivon_harness.api import AgentTurnRequest, DeepSeekSettings, DeepSeekTurnAdapter
from ordivon_harness.core import AgentTurnAdapterError
from ordivon_harness.domain_tools import (
    AgentToolCall,
    AgentToolDefinition,
    DomainToolCatalog,
    DomainToolLoopPlan,
    DomainToolLoopRunner,
    RunBudget,
    ToolObservation,
)

SECRET = Path('/root/.config/ordivon/secrets/deepseek.json')
NO_TOOLS = canonical_digest({'tools': []})
PRESSURE_CLASSES = (
    'shared_method_pressure',
    'shared_knowledge_candidate',
    'confirming_owner_evidence',
    'owner_local_gap',
    'churn',
)
RESPONSIBILITIES = ('CR-04', 'CR-05', 'CR-06', 'CR-09', 'CR-17', 'none')
ACTIONS = ('propose_bounded_falsifier', 'no_new_computer_experiment')

ASSESSMENT_SCHEMA: dict[str, Any] = {
    'type': 'object',
    'additionalProperties': False,
    'properties': {
        'cards': {
            'type': 'array',
            'minItems': 1,
            'maxItems': 8,
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'properties': {
                    'cardId': {'type': 'string', 'minLength': 1, 'maxLength': 120},
                    'pressureClass': {'type': 'string', 'enum': list(PRESSURE_CLASSES)},
                    'requiresComputerExperiment': {'type': 'boolean'},
                    'targetResponsibilityId': {'type': 'string', 'enum': list(RESPONSIBILITIES)},
                    'reason': {'type': 'string', 'minLength': 1, 'maxLength': 1200},
                },
                'required': ['cardId', 'pressureClass', 'requiresComputerExperiment', 'targetResponsibilityId', 'reason'],
            },
        },
        'selection': {
            'type': 'object',
            'additionalProperties': False,
            'properties': {
                'selectedCardId': {'type': 'string', 'minLength': 1, 'maxLength': 120},
                'action': {'type': 'string', 'enum': list(ACTIONS)},
                'targetResponsibilityId': {'type': 'string', 'enum': list(RESPONSIBILITIES)},
                'falsifier': {
                    'type': 'object',
                    'additionalProperties': False,
                    'properties': {
                        'hypothesis': {'type': 'string', 'minLength': 1, 'maxLength': 1600},
                        'baseline': {'type': 'string', 'minLength': 1, 'maxLength': 160},
                        'oracle': {'type': 'string', 'minLength': 1, 'maxLength': 160},
                        'holdout': {'type': 'string', 'minLength': 1, 'maxLength': 160},
                        'promotionBoundary': {'type': 'string', 'minLength': 1, 'maxLength': 200},
                        'deletionOutcome': {'type': 'string', 'minLength': 1, 'maxLength': 200},
                    },
                    'required': ['hypothesis', 'baseline', 'oracle', 'holdout', 'promotionBoundary', 'deletionOutcome'],
                },
            },
            'required': ['selectedCardId', 'action', 'targetResponsibilityId', 'falsifier'],
        },
        'summary': {'type': 'string', 'minLength': 1, 'maxLength': 1800},
    },
    'required': ['cards', 'selection', 'summary'],
}
COMPLETION = {'mode': 'structured-result-v1', 'resultKind': 'owner-pressure-assessment-v1', 'resultSchema': ASSESSMENT_SCHEMA}

INSPECT = AgentToolDefinition(
    'inspect_owner_evidence',
    'Read the exact frozen bounded owner-native evidence for one inventory card. This is observation only and grants no owner authority.',
    {
        'type': 'object',
        'additionalProperties': False,
        'properties': {'cardId': {'type': 'string', 'minLength': 1, 'maxLength': 120}},
        'required': ['cardId'],
    },
)
SUBMIT = AgentToolDefinition(
    'submit_pressure_assessment',
    'Submit the complete pressure assessment for every card in this split and one selected next research action. Use selectedCardId="none" and no_new_computer_experiment when no owner delta forces a new Computer experiment.',
    ASSESSMENT_SCHEMA,
)
CATALOG = DomainToolCatalog('domain:computer-owner-pressure-discovery', '1', (INSPECT, SUBMIT))

SHARED_CLAIMS = [
    'Owner revision movement is review pressure, not automatic shared world-model change.',
    'A shared Computer change requires a durable responsibility or relation that materially affects more than owner-local implementation; ordinary bug fixes, packaging, UX and CI churn stay local.',
    'Confirming evidence can strengthen an existing responsibility without opening a new Computer experiment.',
    'A shared knowledge candidate may be reusable without requiring a new shared layer or immediate experiment.',
    'Named architecture categories such as Skill, Multi, Graph, Memory, World manager or Organization have no existence entitlement.',
    'Before consequence admission, planning may be recomputable; after exact owner admission, identity/UNKNOWN/reconciliation may need durability.',
    'The next adaptation experiment must start from real owner-native pressure and use independent owner-bound evaluation; the proposing Agent does not own owner truth or product promotion.',
]
CLASS_GUIDE = {
    'shared_method_pressure': 'A current owner result exposes a limitation or contradiction in the shared Computer research/adaptation method that merits a bounded Computer experiment now.',
    'shared_knowledge_candidate': 'A reusable cross-project relation appears useful to Knowledge, but current evidence does not force a new Computer experiment or shared product layer.',
    'confirming_owner_evidence': 'The owner result materially reinforces an existing Computer responsibility or rejection without creating a new unresolved shared question.',
    'owner_local_gap': 'A real unresolved responsibility exists, but current evidence places it inside one owner rather than Computer.',
    'churn': 'The change is maintenance, UI/docs, packaging, or another local change with no material shared-model pressure.',
}
FALSIFIER_ENUMS = {
    'baseline': 'full_evidence_one_shot',
    'oracle': 'owner_native_evidence_plus_independent_evaluator',
    'holdout': 'frozen_owner_delta_holdout',
    'promotionBoundary': 'computer_research_only_no_product_authority',
    'deletionOutcome': 'retain_existing_manual_or_full_context_review',
}
NULL_FALSIFIER = {key: 'none' for key in ('hypothesis', 'baseline', 'oracle', 'holdout', 'promotionBoundary', 'deletionOutcome')}


def usage_tokens(usage: dict[str, Any]) -> int:
    for key in ('totalTokens', 'total_tokens'):
        value = usage.get(key)
        if isinstance(value, int):
            return value
    return 0


def rotate(items: list[dict[str, Any]], amount: int) -> list[dict[str, Any]]:
    if not items:
        return []
    amount %= len(items)
    return items[amount:] + items[:amount]


def metadata(card: dict[str, Any]) -> dict[str, Any]:
    return {
        'cardId': card['cardId'],
        'repositoryId': card['repositoryId'],
        'revision': card['revision'],
        'title': card['title'],
        'changedSummary': card['changedSummary'],
        'evidenceDigest': card['evidenceDigest'],
    }


def instruction(split: str, cards: list[dict[str, Any]], *, include_evidence: bool) -> str:
    payload: dict[str, Any] = {
        'experiment': 'COMPUTER-C6-OWNER-PRESSURE-DISCOVERY',
        'split': split,
        'objective': 'Classify every owner delta, decide whether any one forces a new bounded Computer experiment now, and propose the smallest falsifier only when justified.',
        'sharedClaims': SHARED_CLAIMS,
        'pressureClasses': CLASS_GUIDE,
        'rules': [
            'Classify every card exactly once.',
            'A high-value owner change may still be confirming evidence or owner-local rather than a new Computer experiment.',
            'Do not invent a new architecture category just to continue an RSI phase ladder.',
            'Use selectedCardId="none", action="no_new_computer_experiment", targetResponsibilityId="none", and all falsifier fields="none" if no card forces a new Computer experiment.',
            'If proposing an experiment, use the exact allowed falsifier boundary strings supplied below and write only the hypothesis freely.',
            'Owner truth, evaluator truth, product merge/deploy and Core promotion remain outside your authority.',
        ],
        'allowedFalsifierBoundary': FALSIFIER_ENUMS,
        'inventory': [metadata(card) for card in cards],
    }
    if include_evidence:
        payload['ownerEvidence'] = [
            {'cardId': card['cardId'], 'evidenceDigest': card['evidenceDigest'], 'evidence': card['evidence']}
            for card in cards
        ]
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def validate_assessment(value: dict[str, Any], cards: list[dict[str, Any]]) -> None:
    expected = {card['cardId'] for card in cards}
    rows = value.get('cards')
    if not isinstance(rows, list) or len(rows) != len(cards):
        raise ValueError('assessment must contain exactly one row for every split card')
    observed = [row.get('cardId') for row in rows if isinstance(row, dict)]
    if len(observed) != len(set(observed)) or set(observed) != expected:
        raise ValueError('assessment card identity set differs from split inventory')
    selection = value.get('selection')
    if not isinstance(selection, dict):
        raise ValueError('assessment selection is missing')
    selected = selection.get('selectedCardId')
    if selected != 'none' and selected not in expected:
        raise ValueError('selectedCardId is not in split inventory or none')
    action = selection.get('action')
    falsifier = selection.get('falsifier')
    if not isinstance(falsifier, dict):
        raise ValueError('falsifier is missing')
    if action == 'no_new_computer_experiment':
        if selected != 'none' or selection.get('targetResponsibilityId') != 'none' or any(falsifier.get(key) != 'none' for key in NULL_FALSIFIER):
            raise ValueError('null selection must use none identity/target/falsifier')
    elif action == 'propose_bounded_falsifier':
        if selected == 'none' or selection.get('targetResponsibilityId') == 'none':
            raise ValueError('bounded falsifier requires selected card and responsibility')
        for key, expected_value in FALSIFIER_ENUMS.items():
            if falsifier.get(key) != expected_value:
                raise ValueError(f'falsifier boundary differs: {key}')
        if not isinstance(falsifier.get('hypothesis'), str) or not falsifier['hypothesis'].strip() or falsifier['hypothesis'] == 'none':
            raise ValueError('bounded falsifier requires a concrete hypothesis')
    else:
        raise ValueError('selection action differs')


@dataclass
class SelectiveBridge:
    cards: list[dict[str, Any]]
    max_inspections: int

    def __post_init__(self) -> None:
        self.catalog = CATALOG
        self.bridge_identity = {
            'schemaVersion': 1,
            'kind': 'ordivon.computer-pressure-selection-bridge',
            'truthRole': 'research-only-read-projection',
            'corpusDigest': canonical_digest({'cards': [metadata(card) for card in self.cards]}),
        }
        self.by_id = {card['cardId']: card for card in self.cards}
        self.inspected: list[str] = []
        self.submitted: dict[str, Any] | None = None
        self.tool_sequence: list[str] = []

    def execute(self, call: AgentToolCall, *, step_id: str) -> ToolObservation:
        self.tool_sequence.append(call.name)
        if call.name == 'inspect_owner_evidence':
            card_id = call.arguments.get('cardId')
            if not isinstance(card_id, str) or card_id not in self.by_id:
                raise ValueError('unknown cardId')
            if card_id not in self.inspected:
                if len(self.inspected) >= self.max_inspections:
                    raise ValueError('bounded owner-evidence inspection limit exceeded')
                self.inspected.append(card_id)
            card = self.by_id[card_id]
            content = {
                'cardId': card_id,
                'repositoryId': card['repositoryId'],
                'revision': card['revision'],
                'evidenceDigest': card['evidenceDigest'],
                'evidence': card['evidence'],
                'inspectionIndex': self.inspected.index(card_id) + 1,
                'remainingDistinctInspections': self.max_inspections - len(self.inspected),
            }
        elif call.name == 'submit_pressure_assessment':
            if self.submitted is not None:
                raise ValueError('pressure assessment already submitted')
            value = dict(call.arguments)
            validate_assessment(value, self.cards)
            self.submitted = value
            content = {'acceptedForIndependentEvaluation': True, 'cardCount': len(value['cards']), 'ownerAuthorityChanged': False}
        else:
            raise ValueError('unexpected Tool')
        return ToolObservation(tool_call_id=call.tool_call_id, tool_name=call.name, status='observed', structured_content={**content, 'stepId': step_id})


def one_shot(settings: DeepSeekSettings, cards: list[dict[str, Any]], split: str, replicate: int) -> dict[str, Any]:
    prompt = instruction(split, cards, include_evidence=True)
    attempts: list[dict[str, Any]] = []
    total_tokens = 0
    for presentation in (1, 2):
        messages: tuple[dict[str, str], ...] = (
            {'role': 'system', 'content': 'Act as a bounded Computer research reviewer. Owner evidence is input, not your authority. Submit exactly one structured pressure assessment.'},
            {'role': 'user', 'content': prompt},
        )
        if presentation == 2:
            messages = (*messages, {'role': 'user', 'content': 'Provider-presentation correction only: submit the required structured result exactly. Do not change the evidence, classification task, or authority boundary.'})
        adapter = DeepSeekTurnAdapter(settings, completion_contract=COMPLETION)
        req = AgentTurnRequest(
            harness_run_id=f'harness-run:c6:{split}:baseline:r{replicate}',
            turn_id=f'turn:c6:{split}:baseline:r{replicate}:presentation-{presentation}',
            sequence=1,
            assignment_id=f'assignment:c6:{split}:baseline:r{replicate}',
            context_digest=canonical_digest({'messages': list(messages), 'split': split, 'replicate': replicate, 'presentation': presentation}),
            tool_catalog_digest=NO_TOOLS,
            messages=messages,
            tools=(),
            remaining_budget={'modelCalls': 1, 'toolCalls': 0, 'totalTokens': 32768, 'wallTimeMs': 120000},
        )
        try:
            result = adapter.invoke(req)
        except AgentTurnAdapterError as error:
            attempts.append({'presentation': presentation, 'valid': False, 'failure': type(error).__name__ + ': ' + str(error), 'requestDigest': req.digest})
            continue
        tokens = usage_tokens(result.usage); total_tokens += tokens
        evidence = {'presentation': presentation, 'valid': result.conclusion is not None, 'requestDigest': req.digest, 'providerRequestDigest': adapter.provider_request_digest(req), 'resultDigest': result.digest, 'modelCallId': result.model_call_id, 'usage': result.usage, 'tokens': tokens, 'rawResponseDigest': result.raw_response_digest}
        attempts.append(evidence)
        if result.conclusion is None:
            continue
        value = json.loads(result.conclusion.summary)
        validate_assessment(value, cards)
        return {'assessment': value, 'tokens': total_tokens, 'providerAttempts': len(attempts), 'presentationCorrections': len(attempts)-1, 'modelEvidence': attempts}
    raise RuntimeError('baseline Provider presentation remained invalid after one correction')


def selective(settings: DeepSeekSettings, cards: list[dict[str, Any]], split: str, replicate: int, max_inspections: int) -> dict[str, Any]:
    prompt = instruction(split, cards, include_evidence=False)
    bridge = SelectiveBridge(cards, max_inspections)
    budget = RunBudget(
        max_model_calls=5,
        max_tool_calls=max_inspections + 1,
        max_observation_bytes=65536,
        max_wall_time_ms=180000,
        max_total_tokens=65536,
        max_model_retries=1,
        max_tool_corrections=2,
        max_conclusion_corrections=1,
        max_observation_only_turns=1,
        max_no_progress_turns=2,
        max_model_observation_bytes=65536,
    )
    adapter = DeepSeekTurnAdapter(settings)
    plan = DomainToolLoopPlan(
        harness_run_id=f'harness-run:c6:{split}:selective:r{replicate}',
        assignment_id=f'assignment:c6:{split}:selective:r{replicate}',
        context_digest=canonical_digest({'prompt': prompt, 'split': split, 'replicate': replicate}),
        initial_messages=(
            {'role': 'system', 'content': 'Act as a bounded Computer research reviewer. Inspect owner evidence selectively, then submit exactly one complete assessment through submit_pressure_assessment. The hidden evaluator is unavailable.'},
            {'role': 'user', 'content': prompt},
        ),
        allowed_tools=('inspect_owner_evidence', 'submit_pressure_assessment'),
        budget=budget,
    )
    result = DomainToolLoopRunner(adapter, bridge).run(plan)
    if bridge.submitted is None:
        raise RuntimeError('selective Agent did not submit a pressure assessment')
    validate_assessment(bridge.submitted, cards)
    return {
        'assessment': bridge.submitted,
        'tokens': usage_tokens(result.usage),
        'providerAttempts': result.model_calls,
        'presentationCorrections': 0,
        'inspectedCardIds': bridge.inspected,
        'inspectionCount': len(bridge.inspected),
        'toolSequence': bridge.tool_sequence,
        'stopCode': result.stop_code.value,
        'candidateCompleted': result.candidate_completed,
        'usage': result.usage,
    }


def aggregate(rows: list[dict[str, Any]], treatment: str) -> dict[str, Any]:
    selected = [row for row in rows if row['treatment'] == treatment]
    valid = [row for row in selected if row.get('valid')]
    return {
        'trajectories': len(selected),
        'validTrajectories': len(valid),
        'invalidTrajectories': len(selected)-len(valid),
        'decisionCorrect': sum(bool(row.get('evaluation', {}).get('decisionCorrect')) for row in valid),
        'classificationCorrect': sum(int(row.get('evaluation', {}).get('cardsCorrect', 0)) for row in valid),
        'classificationTotal': sum(int(row.get('evaluation', {}).get('cardsTotal', 0)) for row in valid),
        'falsePromotions': sum(int(row.get('evaluation', {}).get('falsePromotions', 0)) for row in valid),
        'tokens': sum(int(row.get('tokens', 0)) for row in valid),
        'providerAttempts': sum(int(row.get('providerAttempts', 0)) for row in valid),
        'presentationCorrections': sum(int(row.get('presentationCorrections', 0)) for row in valid),
        'inspectionCount': sum(int(row.get('inspectionCount', 0)) for row in valid),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--secret', type=Path, default=SECRET)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args(); args.output_dir.mkdir(parents=True, exist_ok=True)
    settings = DeepSeekSettings.from_secret_file(args.secret, max_output_tokens=6000, timeout_seconds=120.0)
    cards_doc = json.loads((HERE/'fixtures/cards.json').read_text())
    oracle = json.loads((HERE/'fixtures/oracle.json').read_text())
    plan_doc = json.loads((HERE/'plan-v1.json').read_text())
    all_rows: list[dict[str, Any]] = []
    for split, replicate_count, max_inspections in (('development', 5, 3), ('holdout', 3, 2)):
        source_cards = [card for card in cards_doc['cards'] if card['split'] == split]
        rows=[]
        for replicate in range(1, replicate_count+1):
            cards = rotate(source_cards, replicate-1)
            order=('full-evidence-baseline','selective-inspection') if replicate%2 else ('selective-inspection','full-evidence-baseline')
            for treatment in order:
                try:
                    raw = one_shot(settings,cards,split,replicate) if treatment=='full-evidence-baseline' else selective(settings,cards,split,replicate,max_inspections)
                    evaluation=evaluate(raw['assessment'],cards,oracle,split)
                    row={'split':split,'replicate':replicate,'treatment':treatment,'valid':True,**raw,'evaluation':evaluation}
                except Exception as error:
                    row={'split':split,'replicate':replicate,'treatment':treatment,'valid':False,'failure':type(error).__name__+': '+str(error)}
                rows.append(row); all_rows.append(row)
        metrics={t:aggregate(rows,t) for t in ('full-evidence-baseline','selective-inspection')}
        (args.output_dir/f'{split}.json').write_text(json.dumps({'schemaVersion':1,'kind':f'ordivon.owner-pressure-{split}','provider':{'adapterId':DeepSeekTurnAdapter.adapter_id,'model':settings.model,'credentialScopeId':settings.credential_scope_id},'rows':rows,'metrics':metrics},indent=2,ensure_ascii=False)+'\n')
    dev=json.loads((args.output_dir/'development.json').read_text())['metrics']; hold=json.loads((args.output_dir/'holdout.json').read_text())['metrics']; bdev=dev['full-evidence-baseline']; cdev=dev['selective-inspection']; bhold=hold['full-evidence-baseline']; chold=hold['selective-inspection']
    def accuracy(m:dict[str,Any])->float:return m['classificationCorrect']/max(1,m['classificationTotal'])
    token_ratio=(cdev['tokens']+chold['tokens'])/max(1,bdev['tokens']+bhold['tokens'])
    avg_dev_inspect=cdev['inspectionCount']/max(1,cdev['validTrajectories']); avg_hold_inspect=chold['inspectionCount']/max(1,chold['validTrajectories'])
    all_valid=all(row.get('valid') for row in all_rows)
    rule=plan_doc['promotionRule']
    promotion=all_valid and cdev['decisionCorrect']>=rule['candidateDevelopmentDecisionMinimum'] and chold['decisionCorrect']>=rule['candidateHoldoutDecisionMinimum'] and cdev['decisionCorrect']>=bdev['decisionCorrect'] and chold['decisionCorrect']>=bhold['decisionCorrect'] and cdev['falsePromotions']<=bdev['falsePromotions'] and chold['falsePromotions']<=bhold['falsePromotions'] and accuracy(cdev)+rule['candidateClassificationAccuracyWithinBaseline']>=accuracy(bdev) and accuracy(chold)+rule['candidateClassificationAccuracyWithinBaseline']>=accuracy(bhold) and token_ratio<=rule['maxCandidateToBaselineTokenRatio'] and avg_dev_inspect<=rule['maxAverageDevelopmentInspections'] and avg_hold_inspect<=rule['maxAverageHoldoutInspections']
    closeout={'schemaVersion':1,'kind':'ordivon.owner-pressure-live-closeout','validCampaign':all_valid,'developmentMetrics':dev,'holdoutMetrics':hold,'baselineClassificationAccuracy':{'development':accuracy(bdev),'holdout':accuracy(bhold)},'candidateClassificationAccuracy':{'development':accuracy(cdev),'holdout':accuracy(chold)},'candidateToBaselineTokenRatio':token_ratio,'candidateAverageInspections':{'development':avg_dev_inspect,'holdout':avg_hold_inspect},'promotionRulePassed':promotion,'disposition':'retain_bounded_selective_pressure_triage' if promotion else ('retain_full_evidence_or_manual_review_baseline' if all_valid else 'incomplete_provider_or_apparatus_failure'),'authority':{'newDaemonAuthorized':False,'centralOwnerRegistryAuthorized':False,'automaticPromotionAuthorized':False,'automaticEvaluatorAuthorityAuthorized':False},'claimLimit':'one frozen current-owner delta family; this can establish bounded pressure-selection value, not autonomous open-ended problem discovery or RSI'}
    (args.output_dir/'closeout.json').write_text(json.dumps(closeout,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'valid':all_valid,'development':dev,'holdout':hold,'tokenRatio':token_ratio,'avgInspections':closeout['candidateAverageInspections'],'promotion':promotion,'disposition':closeout['disposition']},sort_keys=True))
    return 0 if all_valid else 2

if __name__=='__main__':
    raise SystemExit(main())
