import unittest
from pilot import Environment, cases, reconcile, score

class PilotTests(unittest.TestCase):
    def test_oracles(self):
        for c in cases():
            s = score(c, c['oracle'])
            self.assertTrue(s['classification_correct'] and s['calculation_correct'] and s['required_evidence_complete'])
    def test_wrong_and_fabricated(self):
        c = cases()[0]
        s = score(c, {'status':'clean','value':999,'evidence_ids':['invented']})
        self.assertFalse(s['classification_correct'])
        self.assertFalse(s['calculation_correct'])
        self.assertEqual(s['fabricated_citation_count'],1)
    def test_nonfinite(self):
        self.assertFalse(score(cases()[0], {**cases()[0]['oracle'], 'value':float('nan')})['calculation_correct'])
    def test_stage_denied(self):
        c = cases()[0]; e = Environment(c)
        self.assertTrue(e.step({'action':'read','document_id':c['documents'][1]['id']})['denied'])
        self.assertNotIn('oracle', e.observation())
    def test_unseen_citation_ineligible(self):
        c = cases()[0]; e = Environment(c)
        self.assertFalse(e.step({'action':'decide','prediction':c['oracle']})['eligible'])
        with self.assertRaises(ValueError): e.step({'action':'advance'})
    def test_budget(self):
        e = Environment(cases()[0],1); e.step({'action':'advance'})
        with self.assertRaises(ValueError): e.step({'action':'advance'})
    def test_duplicate_invoice_and_partial_receipts(self):
        invoice={'id':'a','amount':100}
        self.assertEqual(reconcile([invoice,invoice],[{'invoice_id':'a','amount':30},{'invoice_id':'a','amount':20}]),{'revenue':100,'cash':50})
    def test_conflict_and_orphan(self):
        with self.assertRaises(ValueError): reconcile([{'id':'a','amount':1},{'id':'a','amount':2}],[])
        with self.assertRaises(ValueError): reconcile([], [{'invoice_id':'x','amount':1}])
    def test_invalid_prediction(self):
        with self.assertRaises(ValueError): score(cases()[0], {'status':'yes'})

if __name__ == '__main__': unittest.main()
