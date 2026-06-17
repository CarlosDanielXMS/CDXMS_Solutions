import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
release = json.loads((root / 'release.json').read_text(encoding='utf-8'))
ids = [a['artifact_id'] for a in release['artifacts']]
required = ['json_config_manager','bootstrap','result_manager','logger','string_utils','artifact_manager','dependency_resolver']
missing = [x for x in required if x not in ids]
assert not missing, missing
for artifact_id in required:
    manifest = root / 'capabilities' / artifact_id / 'manifest.json'
    assert manifest.exists(), manifest
    m = json.loads(manifest.read_text(encoding='utf-8'))
    assert m['artifact_type'] == 'capability'
print('VALIDATION OK — CDXMS Core + AM + Dependency Resolver v1.0.0 incremental merged')
