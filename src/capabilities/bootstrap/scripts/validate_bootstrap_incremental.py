import json
from pathlib import Path
root = Path(__file__).resolve().parents[4]
errors = []

def load(path):
    try:
        return json.loads((root/path).read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f"{path}: {exc}")
        return None

manifest = load(Path('capabilities/bootstrap/manifest.json'))
contract = load(Path('capabilities/bootstrap/contract.json'))
remote = load(Path('capabilities/bootstrap/remote_manifest.json'))
enums = load(Path('core/enums.json'))
core_errors = load(Path('core/errors.json'))

if manifest:
    assert manifest['capability']['id'] == 'bootstrap'
    assert manifest['macrodroid_export']['file_path'] == 'capabilities/bootstrap/macrodroid/[CDXMS]_Bootstrap.ablock'
if contract:
    outputs = contract.get('outputs', [])
    assert len(outputs) == 1 and outputs[0]['name'] == 'Resultado'
    assert 'data_json' in contract['result']['forbidden_top_level_fields']
if remote:
    assert remote['source']['base_raw_url'].endswith('/src')
    for f in remote['files']:
        assert not f['target_path'].startswith('src/')
if enums:
    assert 'bootstrap_operation' in enums['enums']
if core_errors:
    assert 'BOOTSTRAP_CORE_UNAVAILABLE' in core_errors['errors']

if errors:
    raise SystemExit('\n'.join(errors))
print('[OK] Bootstrap incremental package validado.')
