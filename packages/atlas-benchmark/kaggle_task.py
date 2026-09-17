"""Run in a Kaggle benchmark notebook with pilot.py beside this file."""
import json
import kaggle_benchmarks as kbench
from pilot import Environment, cases, score, parse_response

@kbench.task(name='Atlas evidence pilot')
def atlas_evidence(llm) -> float:
    """Public nine-case development diagnostic; exact arithmetic and IDs only."""
    passed = 0
    for case in cases():
        prompt = case['prompt'] + '\nEvidence: ' + json.dumps(case['documents'])
        response = llm.prompt(prompt + '\nReturn only JSON: {"status":str,"value":number|null,"evidence_ids":[str]}.')
        try:
            measured = score(case, parse_response(response))
            passed += all(measured[k] for k in ('classification_correct','calculation_correct','required_evidence_complete')) and measured['fabricated_citation_count'] == 0
        except (ValueError, TypeError, KeyError):
            pass  # Invalid model output scores zero; provider errors remain run errors.
    return passed / len(cases())

@kbench.task(name='Atlas staged investigation pilot')
def atlas_dynamic(llm) -> float:
    passed = 0
    for case in cases():
        env = Environment(case)
        while not env.closed and env.budget > 0:
            prompt = json.dumps({'observation':env.observation(), 'history':env.events})
            response = llm.prompt(prompt + '\nReturn ONLY JSON action: {"action":"read","document_id":str}, {"action":"advance"}, or {"action":"decide","prediction":{"status":str,"value":number|null,"evidence_ids":[str]}}. Read evidence before citing it. You have at most four actions.')
            try:
                result = env.step(parse_response(response))
            except (ValueError, TypeError, AttributeError):
                break
            if env.closed:
                m = result['metrics']
                passed += result['eligible'] and all(m[k] for k in ('classification_correct','calculation_correct','required_evidence_complete'))
    return passed / len(cases())

# Explicit invocation only; no automatic provider spend on import.
# atlas_evidence.run(llm=kbench.llm)
# atlas_dynamic.run(llm=kbench.llm)
