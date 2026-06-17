#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def fail(msg):
    errors.append(msg)

# JSON validity
for path in ROOT.rglob('*.json'):
    try:
        json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'JSON inválido: {path.relative_to(ROOT)} :: {exc}')

release = json.loads((ROOT / 'release.json').read_text(encoding='utf-8'))
ids = [a.get('artifact_id') for a in release.get('artifacts', [])]
for expected in ['json_config_manager','bootstrap','result_manager','logger','string_utils','artifact_manager']:
    if expected not in ids:
        fail(f'Artifact ausente no release.json: {expected}')

ab_path = ROOT / 'capabilities' / 'artifact_manager' / 'macrodroid' / '[CDXMS]_Artifact_Manager.ablock'
ab = json.loads(ab_path.read_text(encoding='utf-8'))
macro = ab.get('macro', {})
js = [a for a in macro.get('m_actionList', []) if a.get('m_classType') == 'JavaScriptAction']
parse = [a for a in macro.get('m_actionList', []) if a.get('m_classType') == 'JsonParseAction']
if not js or not parse:
    fail('Artifact Manager precisa conter JavaScriptAction e JsonParseAction')
else:
    if js[0].get('stringVariableName') != parse[0].get('stringVarName'):
        fail('Saída da JavaScriptAction diverge da entrada da JsonParseAction no Artifact Manager')
    if js[0].get('stringVariableName') != 'Tmp_ArtifactWorkJson':
        fail('Artifact Manager deve usar Tmp_ArtifactWorkJson como fronteira JS -> JSON Parse')
    if parse[0].get('dictionaryVarName') != 'Resultado':
        fail('Artifact Manager deve publicar JsonParseAction em Resultado')

if errors:
    print('VALIDATION FAILED — Core + Artifact Manager v1.0.0 incremental merged')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('VALIDATION OK — Core + Artifact Manager v1.0.0 incremental merged')
