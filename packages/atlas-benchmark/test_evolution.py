import json
import unittest
from contextlib import contextmanager
from types import SimpleNamespace
from evolution import corpus, check, evaluate

class EvolutionTests(unittest.TestCase):
    def answer(self,stage):
        o=stage['oracle']; return {**o,'probabilities':{s:float(s==o['status']) for s in ('material','clean','insufficient_evidence')}}
    def test_reversals(self):
        self.assertEqual([s['oracle']['status'] for s in corpus()[0]['stages']],['clean','material','clean'])
        self.assertEqual([s['oracle']['status'] for s in corpus()[3]['stages']],['material','insufficient_evidence','clean'])
    def test_stale_confirmation_rejected(self):
        c=corpus()[0]; self.assertFalse(check(c['stages'][1],self.answer(c['stages'][0]))['pass'])
    def test_unknown_not_carried_forward(self):
        c=corpus()[3]; self.assertFalse(check(c['stages'][1],self.answer(c['stages'][0]))['pass'])
    def test_brier_and_numeric(self):
        s=corpus()[0]['stages'][1]; a=self.answer(s)
        self.assertEqual(check(s,a)['brier_score'],0)
        self.assertFalse(check(s,{**a,'value':True})['pass'])
        with self.assertRaises(ValueError): check(s,{**a,'probabilities':{'material':float('nan'),'clean':0,'insufficient_evidence':0}})
    def test_context_denominator_and_no_oracle(self):
        chats=[]; requests=[]
        @contextmanager
        def factory(name):
            chats.append(name); yield SimpleNamespace(usage=None)
        def prompt(text):
            request=json.loads(text); requests.append(request)
            self.assertNotIn('oracle',text)
            cid=request['case_id']; st=request['stage']
            if st==1: raise RuntimeError('provider failure')
            case=next(c for c in corpus() if c['case_id']==cid)
            return json.dumps(self.answer(case['stages'][st]))
        r=evaluate(prompt,factory,json.loads,2)
        self.assertEqual(len(chats),8); self.assertEqual(r['stage_count'],24)
        self.assertEqual(r['failed_count'],8); self.assertAlmostEqual(r['pass_rate'],2/3)
        self.assertTrue(all(x['case_chat_usage']['input_tokens'] is None for x in r['records']))
        self.assertTrue(all(len(x['prior_observed_evidence'])==x['stage'] for x in requests))
    def test_all_failure_not_perfect(self):
        @contextmanager
        def factory(name): yield SimpleNamespace(usage=None)
        r=evaluate(lambda text:'invalid',factory,json.loads)
        self.assertEqual(r['pass_rate'],0); self.assertIsNone(r['mean_brier_completed_only'])
    def test_repeat_limit(self):
        with self.assertRaises(ValueError): evaluate(None,None,None,0)

if __name__=='__main__': unittest.main()
