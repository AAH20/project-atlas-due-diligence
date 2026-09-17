"""Check regeneration determinism and reject a materially corrupted ledger."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil,csv
from validate import validate
BASE=Path(__file__).resolve().parents[2]
archive=BASE/'releases/project-atlas-v0.1.zip'
def digest():return hashlib.sha256(archive.read_bytes()).hexdigest()
before=digest();subprocess.run([sys.executable,str(BASE/'packages/atlas-generator/build.py')],check=True,capture_output=True);after=digest();assert before==after,'Regeneration not deterministic'
valid=validate()
with tempfile.TemporaryDirectory(prefix='atlas-validation-') as temporary:
    copy=Path(temporary)/'pack';shutil.copytree(BASE/'datasets/project-atlas/v0.1',copy)
    p=copy/'data/ledger.csv'
    with p.open() as f:records=list(csv.DictReader(f))
    records[0]['signed_cents']=str(int(records[0]['signed_cents'])+100)
    with p.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    try:validate(copy)
    except AssertionError:rejected=True
    else:raise AssertionError('Unbalanced journal accepted')
report={'status':'PASS','deterministic_archive_sha256':after,'corrupt_journal_rejected':rejected,'automated_validation':valid,'public_release':'PUBLIC_TEACHING_PREVIEW_EXPERT_REVIEW_PENDING'}
(BASE/'evaluations/reference/results').mkdir(exist_ok=True);(BASE/'evaluations/reference/results/release-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
