"""Expert case-validation protocol. Code Apache-2.0; Atlas-derived packets retain dataset terms."""
import argparse
import hashlib
import json
import secrets
from pathlib import Path

CRITERIA = ('evidence_sufficiency', 'materiality_clarity', 'answer_resolvability', 'alternative_answers', 'domain_realism')
STATUSES = ('material', 'clean', 'insufficient_evidence')
RUBRIC = {'version':'atlas-case-review-v0.3','criteria':list(CRITERIA),'anchors':{'0':'unusable or unsupported','1':'major gaps','2':'partially supported; revisions needed','3':'supported with explicit limitations','4':'fully supported and decision-useful within stated scope'},'minimum_each':3,'reviewers_per_case':2,'rating_disagreement_threshold':1,'scope':'case quality validation; not agent grading or institutional certification'}


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()


def digest(value): return hashlib.sha256(canonical(value)).hexdigest()


def read(path): return json.loads(Path(path).read_text())


def export_packets(source, target):
    source=Path(source); target=Path(target)
    if target.exists(): raise ValueError('packet directory already exists; create a new release')
    cases=read(source/'data/cases.json'); passages=read(source/'data/evidence_passages.json')
    salt=secrets.token_hex(24)
    packets=[]; mapping=[]
    for case in cases:
        opaque='RV-'+hashlib.sha256((salt+case['id']).encode()).hexdigest()[:16]
        docs=[]; locators=[]
        for i, passage in enumerate(p for p in passages if p['document_id'] in case['document_ids']):
            eid=f'{opaque}/E{i+1}'
            docs.append({'id':eid,'quote':passage['quote'],'line_start':passage['line_start'],'line_end':passage['line_end']})
            locators.append({'opaque_evidence_id':eid,'source_evidence_id':passage['id'],'source_document_id':passage['document_id']})
        if not docs: raise ValueError('case has no evidence')
        packet={'case_id':opaque,'domain':case['domain'],'stage':case['stage'],'task':case['task'],'evidence':docs,'instructions':'Independently determine the supported conclusion, evidence insufficiency and accepted alternatives. Rate case quality using the rubric. Disclose prior author-label exposure. Source exercises are public; identity masking does not establish an unseen benchmark.','license':'Atlas dataset research/education/evaluation terms; not Apache-licensed fixture data.'}
        packets.append(packet); mapping.append({'case_id':opaque,'source_case_id':case['id'],'evidence_mapping':locators})
    target.mkdir(parents=True)
    (target/'packets').mkdir()
    entries=[]
    for p in packets:
        rel=f'packets/{p["case_id"]}.json'
        (target/rel).write_text(json.dumps(p,indent=2)+'\n')
        entries.append({'case_id':p['case_id'],'domain':p['domain'],'path':rel,'packet_sha256':digest(p),'evidence_ids':[e['id'] for e in p['evidence']]})
    manifest={'protocol':'atlas-case-review-v0.3','rubric':RUBRIC,'rubric_sha256':digest(RUBRIC),'source_files':{str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source/'data/cases.json',source/'data/evidence_passages.json',source/'manifest.json']},'public_answer_exposure':'source labels and exercises public; never describe this release as unseen','cases':entries}
    (target/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (target/'organizer-mapping.json').write_text(json.dumps(mapping,indent=2)+'\n')
    (target/'reviews.json').write_text('[]\n')
    (target/'adjudications.json').write_text('[]\n')
    (target/'reviewers.json').write_text('[]\n')
    return manifest


def verify_packets(root, manifest):
    root=Path(root).resolve()
    if manifest.get('rubric') != RUBRIC or manifest.get('rubric_sha256') != digest(RUBRIC): raise ValueError('rubric changed')
    ids=set()
    if not manifest.get('cases'): raise ValueError('empty case release')
    for case in manifest['cases']:
        if case['case_id'] in ids: raise ValueError('duplicate manifest case')
        ids.add(case['case_id'])
        path=(root/case['path']).resolve()
        if not path.is_relative_to(root): raise ValueError('packet path escapes release')
        packet=read(path)
        if digest(packet)!=case['packet_sha256']: raise ValueError('packet changed')
        if packet['case_id']!=case['case_id'] or packet['domain']!=case['domain'] or [e['id'] for e in packet['evidence']]!=case['evidence_ids']: raise ValueError('manifest packet metadata mismatch')


def validate_review(review, case, rubric_hash):
    required={'case_id','packet_sha256','rubric_sha256','reviewer_id','verdict','conclusion','required_evidence_ids','ratings','critical_defects','alternative_answers','rationale','answer_exposure'}
    if not isinstance(review,dict) or set(review)!=required: raise ValueError('review fields missing or unknown')
    if review['packet_sha256']!=case['packet_sha256'] or review['rubric_sha256']!=rubric_hash: raise ValueError('stale review')
    if review['verdict'] not in ('accept','revise','reject') or review['conclusion'] not in STATUSES: raise ValueError('invalid review decision')
    if not isinstance(review['reviewer_id'],str) or not review['reviewer_id'].strip(): raise ValueError('missing reviewer ID')
    ratings=review['ratings']
    if not isinstance(ratings,dict) or set(ratings)!=set(CRITERIA) or any(type(x)!=int or not 0<=x<=4 for x in ratings.values()): raise ValueError('invalid ratings')
    for key in ('critical_defects','alternative_answers','required_evidence_ids'):
        if not isinstance(review[key],list) or not all(isinstance(x,str) and x.strip() for x in review[key]): raise ValueError('invalid list')
        if len(review[key])!=len(set(review[key])): raise ValueError('duplicate list entry')
    if not set(review['required_evidence_ids'])<=set(case['evidence_ids']): raise ValueError('citation outside packet')
    if not review['required_evidence_ids']: raise ValueError('evidence locator required even for insufficiency')
    if not isinstance(review['rationale'],str) or not review['rationale'].strip() or type(review['answer_exposure'])!=bool: raise ValueError('rationale/exposure required')


def profile_ok(profile, domain):
    return profile is not None and profile.get('identity_and_expertise_checked') is True and profile.get('independent_of_authoring') is True and profile.get('conflict_declared') is False and domain in profile.get('qualified_domains',[]) and isinstance(profile.get('verification_reference'),str) and bool(profile['verification_reference'].strip())


def acceptable(review):
    return review['verdict']=='accept' and not review['critical_defects'] and all(v>=RUBRIC['minimum_each'] for v in review['ratings'].values())


def evaluate(manifest, reviews, profiles, adjudications):
    if manifest.get('rubric_sha256')!=digest(RUBRIC) or manifest.get('rubric')!=RUBRIC: raise ValueError('rubric mismatch')
    cases={c['case_id']:c for c in manifest['cases']}
    if not cases or len(cases)!=len(manifest['cases']): raise ValueError('empty/duplicate cases')
    by_profile={p['reviewer_id']:p for p in profiles}
    if len(by_profile)!=len(profiles): raise ValueError('duplicate reviewer profile')
    grouped={cid:[] for cid in cases}; adjudicated={}
    for review in reviews:
        cid=review['case_id']
        if cid not in cases: raise ValueError('unknown review case')
        validate_review(review,cases[cid],manifest['rubric_sha256'])
        if any(r['reviewer_id']==review['reviewer_id'] for r in grouped[cid]): raise ValueError('duplicate reviewer for case')
        grouped[cid].append(review)
    for a in adjudications:
        if set(a)!= {'case_id','review_hashes','final_review'} or a['case_id'] not in cases or a['case_id'] in adjudicated: raise ValueError('invalid/duplicate adjudication')
        cid=a['case_id']; final=a['final_review']
        if final['case_id']!=cid: raise ValueError('adjudication case mismatch')
        validate_review(final,cases[cid],manifest['rubric_sha256'])
        if not isinstance(a['review_hashes'],list) or len(a['review_hashes'])!=2 or len(set(a['review_hashes']))!=2 or set(a['review_hashes'])!={digest(r) for r in grouped[cid]}: raise ValueError('adjudication refers to different reviews')
        adjudicated[cid]=a
    results=[]
    for cid,case in cases.items():
        pair=grouped[cid]; reasons=[]; selected=None
        if len(pair)!=2: reasons.append('exactly_two_reviews_required')
        elif not all(profile_ok(by_profile.get(r['reviewer_id']),case['domain']) for r in pair): reasons.append('reviewer_qualification_or_independence_unverified')
        else:
            left,right=pair
            disagreement=left['conclusion']!=right['conclusion'] or left['verdict']!=right['verdict'] or set(left['required_evidence_ids'])!=set(right['required_evidence_ids']) or any(abs(left['ratings'][k]-right['ratings'][k])>1 for k in CRITERIA) or bool(left['critical_defects'] or right['critical_defects']) or set(left['alternative_answers'])!=set(right['alternative_answers'])
            if disagreement:
                a=adjudicated.get(cid)
                if a is None: reasons.append('adjudication_required')
                elif a['final_review']['reviewer_id'] in {r['reviewer_id'] for r in pair} or not profile_ok(by_profile.get(a['final_review']['reviewer_id']),case['domain']): reasons.append('independent_qualified_adjudicator_required')
                else: selected=a['final_review']
            else:
                if not all(acceptable(r) for r in pair): reasons.append('case_quality_revision_required')
                else: selected=left  # Conclusions, evidence and alternatives agree; retain both ratings.
            if selected is not None and not acceptable(selected): reasons.append('case_quality_revision_required'); selected=None
        results.append({'case_id':cid,'case_quality_ready':not reasons,'reasons':reasons,'review_hashes':[digest(r) for r in pair],'answer_exposure_declared':any(r['answer_exposure'] for r in pair),'accepted_conclusion':selected['conclusion'] if selected else None,'accepted_evidence_ids':selected['required_evidence_ids'] if selected else [],'accepted_alternative_answers':selected['alternative_answers'] if selected else [],'adjudication_sha256':digest(adjudicated[cid]) if cid in adjudicated else None})
    ready=all(r['case_quality_ready'] for r in results)
    paired=[pair for pair in grouped.values() if len(pair)==2]
    agreement={'paired_case_count':len(paired),'conclusion_agreement_rate':sum(a['conclusion']==b['conclusion'] for a,b in paired)/len(paired) if paired else None,'mean_absolute_rating_difference':sum(abs(a['ratings'][k]-b['ratings'][k]) for a,b in paired for k in CRITERIA)/(len(paired)*len(CRITERIA)) if paired else None,'qualification_policy':'descriptive agreement across complete pairs; not proof of qualification or case validity'}
    return {'protocol':'atlas-case-review-v0.3','manifest_sha256':digest(manifest),'review_set_sha256':digest(sorted(reviews,key=lambda r:(r['case_id'],r['reviewer_id']))),'profile_set_sha256':digest(sorted(profiles,key=lambda p:p['reviewer_id'])),'adjudication_set_sha256':digest(sorted(adjudications,key=lambda a:a['case_id'])),'reviewer_agreement':agreement,'case_count':len(cases),'ready_count':sum(r['case_quality_ready'] for r in results),'case_quality_ready':ready,'held_out_benchmark_ready':False,'institutional_validation_claim':False,'identity_policy':'qualifications and conflicts are externally checked by organizer; software cannot authenticate expertise','cases':results}


def verify_freeze(root, result):
    path=Path(root)/"FROZEN_REVIEW.json"
    if path.exists() and read(path)!=result:
        raise ValueError("frozen review or its inputs changed; create a new release")


def freeze(root, result):
    if result.get('case_quality_ready') is not True: raise ValueError('case review gate not passed')
    path=Path(root)/'FROZEN_REVIEW.json'
    # Content-addressed inputs; existing freeze never silently replaced.
    with path.open('x') as f: f.write(json.dumps(result,indent=2)+'\n')
    return path


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    sub=parser.add_subparsers(dest='command',required=True)
    ex=sub.add_parser('export'); ex.add_argument('source',type=Path); ex.add_argument('target',type=Path)
    for name in ('check','freeze'):
        cmd=sub.add_parser(name); cmd.add_argument('release',type=Path)
    args=parser.parse_args()
    if args.command=='export': print(json.dumps({'case_count':len(export_packets(args.source,args.target)['cases']),'status':'review_pending'}))
    else:
        manifest=read(args.release/'manifest.json'); verify_packets(args.release,manifest)
        result=evaluate(manifest,read(args.release/'reviews.json'),read(args.release/'reviewers.json'),read(args.release/'adjudications.json'))
        verify_freeze(args.release,result)
        if args.command=='freeze': print(freeze(args.release,result))
        else: print(json.dumps(result,indent=2))
