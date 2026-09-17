import copy
import json
import tempfile
import unittest
from pathlib import Path
from review_gate import RUBRIC, CRITERIA, digest, evaluate, export_packets, freeze, verify_packets, verify_freeze

class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.case={'case_id':'RV-test','domain':'finance','packet_sha256':'packet','evidence_ids':['e1']}
        self.manifest={'rubric':RUBRIC,'rubric_sha256':digest(RUBRIC),'cases':[self.case]}
        self.profiles=[{'reviewer_id':r,'identity_and_expertise_checked':True,'independent_of_authoring':True,'conflict_declared':False,'qualified_domains':['finance'],'verification_reference':'organizer-checked record'} for r in ('r1','r2','r3')]
    def review(self,r='r1',conclusion='material'):
        return {'case_id':'RV-test','packet_sha256':'packet','rubric_sha256':digest(RUBRIC),'reviewer_id':r,'verdict':'accept','conclusion':conclusion,'required_evidence_ids':['e1'],'ratings':{k:3 for k in CRITERIA},'critical_defects':[],'alternative_answers':['Accept specialist escalation with stated uncertainty.'],'rationale':'Evidence supports case answer within stated synthetic scope.','answer_exposure':False}
    def test_empty_pending(self):
        r=evaluate(self.manifest,[],[],[]); self.assertFalse(r['case_quality_ready']); self.assertFalse(r['held_out_benchmark_ready']); self.assertIsNone(r['reviewer_agreement']['conclusion_agreement_rate'])
    def test_two_reviewers_not_institutional_claim(self):
        r=evaluate(self.manifest,[self.review(),self.review('r2')],self.profiles,[])
        self.assertTrue(r['case_quality_ready']); self.assertFalse(r['institutional_validation_claim']); self.assertEqual(r['reviewer_agreement']['conclusion_agreement_rate'],1)
    def test_duplicate_cannot_count_twice(self):
        with self.assertRaises(ValueError): evaluate(self.manifest,[self.review(),self.review()],self.profiles,[])
    def test_conflict_and_missing_expertise(self):
        for field,value in [('conflict_declared',True),('identity_and_expertise_checked',False),('independent_of_authoring',False),('qualified_domains',[])]:
            p=copy.deepcopy(self.profiles); p[0][field]=value
            self.assertFalse(evaluate(self.manifest,[self.review(),self.review('r2')],p,[])['case_quality_ready'])
    def test_disagreement_requires_adjudicator(self):
        pair=[self.review(),self.review('r2','clean')]
        self.assertFalse(evaluate(self.manifest,pair,self.profiles,[])['case_quality_ready'])
        a={'case_id':'RV-test','review_hashes':[digest(r) for r in pair],'final_review':self.review('r3')}
        self.assertTrue(evaluate(self.manifest,pair,self.profiles,[a])['case_quality_ready'])
        a['final_review']=self.review('r1')
        self.assertFalse(evaluate(self.manifest,pair,self.profiles,[a])['case_quality_ready'])
    def test_review_binding_and_adjudication_binding(self):
        r=self.review();r['packet_sha256']='stale'
        with self.assertRaises(ValueError): evaluate(self.manifest,[r],self.profiles,[])
        pair=[self.review(),self.review('r2','clean')]
        a={'case_id':'RV-test','review_hashes':['wrong','wrong2'],'final_review':self.review('r3')}
        with self.assertRaises(ValueError): evaluate(self.manifest,pair,self.profiles,[a])
    def test_bad_rating_and_external_evidence(self):
        for altered in [{**self.review(),'required_evidence_ids':['other-case']},{**self.review(),'ratings':{k:True for k in CRITERIA}}]:
            with self.assertRaises(ValueError): evaluate(self.manifest,[altered],self.profiles,[])
    def test_low_score_and_critical_defects(self):
        pair=[self.review(),self.review('r2')]; pair[0]['ratings']['domain_realism']=2
        self.assertFalse(evaluate(self.manifest,pair,self.profiles,[])['case_quality_ready'])
        pair[0]['critical_defects']=['Ambiguous evidence']
        self.assertIn('adjudication_required',evaluate(self.manifest,pair,self.profiles,[])['cases'][0]['reasons'])
    def test_no_cherry_picking_extra_reviews(self):
        self.assertFalse(evaluate(self.manifest,[self.review(),self.review('r2'),self.review('r3')],self.profiles,[])['case_quality_ready'])
    def test_freeze_pending_and_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): freeze(d,{'case_quality_ready':False})
            r=evaluate(self.manifest,[self.review(),self.review('r2')],self.profiles,[])
            freeze(d,r)
            with self.assertRaises(FileExistsError): freeze(d,r)
    def test_frozen_inputs_changed(self):
        with tempfile.TemporaryDirectory() as d:
            pair=[self.review(),self.review('r2')]
            r=evaluate(self.manifest,pair,self.profiles,[]);freeze(d,r);verify_freeze(d,r)
            pair[0]['rationale']='Updated rationale after freeze'
            changed=evaluate(self.manifest,pair,self.profiles,[])
            with self.assertRaises(ValueError): verify_freeze(d,changed)
    def test_masked_export_and_integrity(self):
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'source';(source/'data').mkdir(parents=True)
            (source/'data/cases.json').write_text(json.dumps([{'id':'CASE-X-M','domain':'finance','stage':'T0','task':'Assess evidence','document_ids':['CASE-X-M-v1']}]))
            (source/'data/evidence_passages.json').write_text(json.dumps([{'id':'E-CASE-X-M','document_id':'CASE-X-M-v1','quote':'Fictional evidence','line_start':5,'line_end':5}]))
            (source/'manifest.json').write_text('[]')
            target=Path(d)/'pack';m=export_packets(source,target);verify_packets(target,m)
            p=target/m['cases'][0]['path'];raw=p.read_text()
            self.assertNotIn('CASE-X-M',raw);self.assertNotIn('oracle',raw)
            p.write_text(raw.replace('Fictional evidence','Edited evidence'))
            with self.assertRaises(ValueError): verify_packets(target,m)
            with self.assertRaises(ValueError): export_packets(source,target)
    def test_packet_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            m=copy.deepcopy(self.manifest);m['cases'][0]['path']='../elsewhere'
            with self.assertRaises(ValueError): verify_packets(d,m)

if __name__=='__main__': unittest.main()
