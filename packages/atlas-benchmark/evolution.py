"""Atlas evolution v0.2 public development diagnostic. Apache-2.0."""
import hashlib
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ('material', 'clean', 'insufficient_evidence')
USAGE_FIELDS = ('input_tokens', 'output_tokens', 'input_tokens_cost_nanodollars', 'output_tokens_cost_nanodollars', 'total_backend_latency_ms')


def corpus():
    scenarios = []
    for cid, values in [('AT-E201', [220,150,240]), ('AT-E202',[None,150,240]), ('AT-E203',[220,230,240]), ('AT-E204',[150,None,240])]:
        stages=[]
        for stage, available in enumerate(values):
            doc_id=f'{cid}/funding@T{stage}'
            gap=None if available is None else max(200-available,0)
            status='insufficient_evidence' if available is None else 'material' if gap else 'clean'
            stages.append({'stage':stage,'document':{'id':doc_id,'text':f'Required acquisition funding: 200 synthetic units. Current verified available funding: {available if available is not None else "unknown; prior confirmation withdrawn"}. This version supersedes all earlier funding confirmations.'},'oracle':{'status':status,'value':gap,'evidence_ids':[doc_id]}})
        scenarios.append({'case_id':cid,'family':'funding-version-update','stages':stages})
    return scenarios


def check(stage, prediction):
    if not isinstance(prediction,dict): raise ValueError('prediction must be an object')
    status=prediction.get('status')
    if status not in STATUSES: raise ValueError('invalid status')
    ids=prediction.get('evidence_ids')
    if not isinstance(ids,list) or not all(isinstance(x,str) for x in ids): raise ValueError('invalid evidence IDs')
    probs=prediction.get('probabilities')
    if not isinstance(probs,dict) or set(probs)!=set(STATUSES): raise ValueError('three probabilities required')
    if any(isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) or v<0 or v>1 for v in probs.values()) or not math.isclose(sum(probs.values()),1,abs_tol=1e-6): raise ValueError('invalid probability distribution')
    expected=stage['oracle']; value=prediction.get('value')
    numeric=value is None if expected['value'] is None else isinstance(value,(float,int)) and not isinstance(value,bool) and math.isfinite(value) and math.isclose(value,expected['value'],abs_tol=1e-6)
    evidence=set(ids)==set(expected['evidence_ids'])
    classification=status==expected['status']
    return {'pass':classification and numeric and evidence,'classification_correct':classification,'calculation_correct':numeric,'current_version_only':evidence,'brier_score':sum((probs[s]-int(s==expected['status']))**2 for s in STATUSES),'semantic_support':'unreviewed'}


def usage_record(usage):
    return {field:getattr(usage,field,None) if usage is not None else None for field in USAGE_FIELDS}


def evaluate(prompt, chat_factory, parse, repetitions=1):
    """Each case/repetition gets fresh chat; evidence stages share that case's chat."""
    if isinstance(repetitions,bool) or not isinstance(repetitions,int) or not 1<=repetitions<=10: raise ValueError('repetitions must be 1..10')
    records=[]
    data=corpus()
    for repetition in range(repetitions):
        for case in data:
            with chat_factory(f'{case["case_id"]}-repeat-{repetition}') as chat:
                history=[]
                for stage in case['stages']:
                    request={'case_id':case['case_id'],'stage':stage['stage'],'evidence':stage['document'],'prior_observed_evidence':history,'instructions':'Use current funding evidence; gap=max(200-available,0). Missing current availability means insufficient_evidence and null gap. Report material if gap>0, otherwise clean. Return JSON with status, value, evidence_ids and probabilities for material/clean/insufficient_evidence summing to one. Cite only current evidence. Never infer funding from a superseded confirmation.'}
                    started=time.perf_counter(); utc=datetime.now(timezone.utc).isoformat()
                    record={'case_id':case['case_id'],'stage':stage['stage'],'repetition':repetition,'started_utc':utc,'status':'failed','pass':False,'prediction':None,'error':None}
                    try:
                        response=prompt(json.dumps(request,sort_keys=True))
                        prediction=parse(response)
                        record.update(check(stage,prediction),prediction=prediction,status='completed')
                    except Exception as exc:
                        # Provider/schema failures remain in denominator and are visible.
                        record['error']=type(exc).__name__
                    record['wall_latency_ms']=(time.perf_counter()-started)*1000
                    records.append(record)
                    history.append(stage['document'])  # Only observed evidence, no oracle/grade.
                usage=usage_record(getattr(chat,'usage',None))
                for record in records[-len(case['stages']):]:
                    record['case_chat_usage']=usage  # Repeated reference, not additive per-stage usage.
    count=len(records); completed=[r for r in records if r['status']=='completed']
    return {'release':'evolution-v0.2','kind':'public development diagnostic; not frontier benchmark','context_policy':'fresh case/repetition chat; stages share within-case context','corpus_sha256':hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest(),'repetitions':repetitions,'stage_count':count,'completed_count':len(completed),'failed_count':count-len(completed),'pass_rate':sum(r['pass'] for r in records)/count,'mean_brier_completed_only':sum(r['brier_score'] for r in completed)/len(completed) if completed else None,'usage_policy':'case-chat usage repeated across stage rows; count each case/repetition once. Missing usage is null.','records':records}


def build():
    root=Path(__file__).resolve().parents[2]/'benchmarks/atlas-agentic-v0.1/evolution-v0.2'
    root.mkdir(parents=True,exist_ok=True)
    (root/'public-cases.json').write_text(json.dumps(corpus(),indent=2)+'\n')
    print('PASS: four public funding trajectories, twelve stage decisions')

if __name__=='__main__': build()
