import unittest
from candidate import reconcile
class Contract(unittest.TestCase):
    def test_partial_and_duplicate(self):
        i={'id':'x','amount':100}
        self.assertEqual(reconcile([i,i],[{'invoice_id':'x','amount':40}]),{'revenue':100,'cash':40})
    def test_empty(self): self.assertEqual(reconcile([],[]),{'revenue':0,'cash':0})
    def test_orphan(self):
        with self.assertRaises(ValueError): reconcile([], [{'invoice_id':'missing','amount':1}])
    def test_conflicting(self):
        with self.assertRaises(ValueError): reconcile([{'id':'x','amount':1},{'id':'x','amount':2}],[])
if __name__ == '__main__': unittest.main()
