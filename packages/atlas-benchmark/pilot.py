"""Public, deterministic development fixtures; no model-performance claims."""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'benchmarks/atlas-agentic-v0.1'


def cases():
    result = []
    for domain, field, limit in [('tenant_cogs', 'margin', 0), ('funding', 'gap', 0), ('capacity', 'shortfall', 0)]:
        for variant in ('material', 'clean', 'insufficient_evidence'):
            cid = f'{domain}-{variant}'
            a, b = {'tenant_cogs': (100, 120 if variant == 'material' else 60), 'funding': (200, 150 if variant == 'material' else 220), 'capacity': (64, 48 if variant == 'material' else 80)}[domain]
            docs = [{'id': f'{cid}/claim@T0', 'stage': 0, 'text': f'{domain}: required/revenue={a}; amounts in synthetic units.'}]
            if variant != 'insufficient_evidence':
                docs.append({'id': f'{cid}/verified@T1', 'stage': 1, 'text': f'Verified cost/available={b}.'})
            value = (a-b)/a if domain == 'tenant_cogs' else max(a-b, 0)
            result.append({'case_id': cid, 'domain': domain, 'documents': docs, 'prompt': f'Classify {domain} as material, clean or insufficient_evidence. Calculate {field} from supplied evidence. Margin=(revenue-cost)/revenue; gap and shortfall=max(required-available,0). Cite document IDs. Do not infer missing evidence.', 'oracle': {'status': variant, 'value': None if variant == 'insufficient_evidence' else value, 'evidence_ids': [d['id'] for d in docs]}})
    return result


def score(case, prediction):
    if not isinstance(prediction, dict):
        raise ValueError('prediction must be an object')
    status = prediction.get('status')
    if status not in ('material', 'clean', 'insufficient_evidence'):
        raise ValueError('invalid status')
    citations = prediction.get('evidence_ids', [])
    if not isinstance(citations, list) or not all(isinstance(x, str) for x in citations):
        raise ValueError('invalid citations')
    ids = set(citations)
    expected = case['oracle']
    valid = {d['id'] for d in case['documents']}
    val = prediction.get('value')
    numeric = val is None if expected['value'] is None else isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(val) and math.isclose(val, expected['value'], abs_tol=1e-6)
    return {'classification_correct': status == expected['status'], 'calculation_correct': numeric, 'required_evidence_complete': set(expected['evidence_ids']) <= ids, 'fabricated_citation_count': len(ids-valid), 'semantic_support': 'unreviewed'}


class Environment:
    """Budgeted staged evidence; oracle is never returned in observations."""
    def __init__(self, case, budget=4):
        self.case, self.budget, self.stage, self.closed = case, budget, 0, False
        self.visible, self.events = [], []

    def step(self, action):
        if self.closed or self.budget <= 0:
            raise ValueError('episode closed or budget exhausted')
        self.budget -= 1
        kind = action.get('action')
        response = {}
        if kind == 'advance':
            self.stage = min(1, self.stage + 1)
            response = {'stage': self.stage}
        elif kind == 'read':
            doc = next((d for d in self.case['documents'] if d['id'] == action.get('document_id')), None)
            if doc is None or doc['stage'] > self.stage:
                response = {'denied': True}
            else:
                self.visible.append(doc['id'])
                response = dict(doc)
        elif kind == 'decide':
            supplied = action.get('prediction', {})
            measured = score(self.case, supplied)
            unseen = set(supplied.get('evidence_ids', [])) - set(self.visible)
            response = {'metrics': measured, 'unseen_citations': sorted(unseen), 'eligible': not unseen and measured['fabricated_citation_count'] == 0}
            self.closed = True
        else:
            raise ValueError('unknown action')
        self.events.append({'sequence': len(self.events), 'stage': self.stage, 'budget_remaining': self.budget, 'action': action, 'response': response})
        return response

    def observation(self):
        return {'case_id': self.case['case_id'], 'stage': self.stage, 'budget_remaining': self.budget, 'document_catalog': [{'id': d['id'], 'stage': d['stage']} for d in self.case['documents'] if d['stage'] <= self.stage], 'prompt': self.case['prompt']}


def reconcile(invoices, receipts):
    """Teaching repair target: invoices recognized once, receipts summed separately."""
    unique = {}
    for invoice in invoices:
        key = invoice['id']
        if key in unique and unique[key] != invoice:
            raise ValueError('conflicting invoice')
        unique[key] = invoice
    if any(r['invoice_id'] not in unique for r in receipts):
        raise ValueError('orphan receipt')
    return {'revenue': sum(i['amount'] for i in unique.values()), 'cash': sum(r['amount'] for r in receipts)}


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    corpus = cases()
    raw = json.dumps(corpus, sort_keys=True, indent=2) + '\n'
    (OUT/'public-cases.json').write_text(raw)
    reference = []
    replay = []
    for case in corpus:
        env = Environment(case)
        env.step({'action': 'read', 'document_id': case['documents'][0]['id']})
        if len(case['documents']) > 1:
            env.step({'action': 'advance'})
            env.step({'action': 'read', 'document_id': case['documents'][1]['id']})
        result = env.step({'action': 'decide', 'prediction': case['oracle']})
        reference.append({'case_id': case['case_id'], **result})
        replay.append({'case_id': case['case_id'], 'events': env.events})
    (OUT/'results').mkdir(exist_ok=True)
    (OUT/'results/reference.json').write_text(json.dumps({'kind': 'oracle-assisted harness self-check; not an agent', 'corpus_sha256': hashlib.sha256(raw.encode()).hexdigest(), 'results': reference}, indent=2)+'\n')
    (OUT/'results/replay.json').write_text(json.dumps(replay, indent=2)+'\n')
    print('PASS: 9 public cases, 3 domains, reference self-check and replay generated')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--predictions', type=Path)
    args = parser.parse_args()
    if args.predictions:
        predictions = json.loads(args.predictions.read_text())
        index = {c['case_id']: c for c in cases()}
        if not isinstance(predictions, list) or len({p['case_id'] for p in predictions}) != len(predictions) or any(p['case_id'] not in index for p in predictions):
            raise ValueError('duplicate/unknown cases or invalid prediction array')
        by_id = {p['case_id']: p for p in predictions}
        print(json.dumps([{'case_id': cid, **(score(c, by_id[cid]) if cid in by_id else {'missing': True, 'classification_correct': False, 'calculation_correct': False})} for cid, c in index.items()], indent=2))
    else:
        build()
