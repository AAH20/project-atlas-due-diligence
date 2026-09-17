"""Deterministic public expansion archive. Explicit allowlist excludes organizer files."""
from pathlib import Path
import hashlib, json, zipfile
ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'releases/project-atlas-v0.2-expansion.zip'
allowed = [ROOT / 'datasets/project-atlas/v0.2', ROOT / 'packages/atlas-expansion', ROOT / 'schemas']
files = [p for folder in allowed for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files += [ROOT / name for name in ['README.md', 'LICENSE', 'DATA_LICENSE.md']]
files += sorted((ROOT / 'docs').glob('ATLAS_V02_*.md'))
DEST.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(DEST, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(files):
        name = path.relative_to(ROOT).as_posix()
        assert 'organizer' not in name and path.is_relative_to(ROOT)
        info = zipfile.ZipInfo(name, date_time=(2026, 9, 17, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, path.read_bytes())
with zipfile.ZipFile(DEST) as archive:
    assert archive.testzip() is None
    assert not any('organizer' in name or name.endswith('/answers.json') for name in archive.namelist())
    assert 'datasets/project-atlas/v0.2/worked_answers/cases.json' in archive.namelist()
print(json.dumps({'archive': str(DEST), 'files': len(files), 'bytes': DEST.stat().st_size,
                  'sha256': hashlib.sha256(DEST.read_bytes()).hexdigest(), 'organizer_excluded': True}))
