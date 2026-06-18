#!/usr/bin/env python3
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
errors = []

def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'JSON inválido: {path} :: {exc}')
        return {}

am_contract = load_json(root / 'capabilities/artifact_manager/contract.json')
inputs = [i.get('name') for i in am_contract.get('inputs', [])]
for name in ['Apply Changes?', 'Dry Run?', 'Target Root Path']:
    if name not in inputs:
        errors.append(f'Artifact Manager contract missing {name}')

contract_text = json.dumps(am_contract, ensure_ascii=False)
for token in ['jcm_apply_plan', 'jcm_verification_plan', 'ARTIFACT_APPLY_REQUIRES_JCM']:
    if token not in contract_text:
        errors.append(f'Artifact Manager contract missing {token}')
if 'side_effects_delegated_to_shell' in contract_text:
    errors.append('Artifact Manager contract still references side_effects_delegated_to_shell')

ab = load_json(root / 'capabilities/artifact_manager/macrodroid/[CDXMS]_Artifact_Manager.ablock')
macro = ab.get('macro', {})
if not macro.get('isActionBlock'):
    errors.append('Artifact Manager export is not action block')
local_names = [v.get('m_name') for v in macro.get('localVariables', [])]
for name in ['Apply Changes?', 'Tmp_ArtifactWorkJson', 'Resultado']:
    if name not in local_names:
        errors.append(f'missing local variable {name}')

actions = macro.get('m_actionList', [])
if any(a.get('m_classType') == 'ShellScriptAction' for a in actions):
    errors.append('Artifact Manager must not use ShellScriptAction for local apply')
if not any(a.get('m_classType') == 'JavaScriptAction' and 'jcm_apply_plan' in a.get('scriptText', '') for a in actions):
    errors.append('missing jcm_apply_plan generation in JavaScriptAction')
if not any(a.get('m_classType') == 'JsonParseAction' and a.get('dictionaryVarName') == 'Resultado' for a in actions):
    errors.append('missing Resultado parse')

manifest = load_json(root / 'capabilities/artifact_manager/manifest.json')
if manifest.get('lifecycle_scope', {}).get('apply_executor') != 'json_config_manager':
    errors.append('Artifact Manager manifest must declare apply_executor=json_config_manager')

config = load_json(root / 'capabilities/artifact_manager/config.default.json')
settings = config.get('settings', {})
if settings.get('allow_shell_apply') is not False:
    errors.append('Artifact Manager config must set allow_shell_apply=false')
if settings.get('require_jcm_executor') is not True:
    errors.append('Artifact Manager config must set require_jcm_executor=true')

if errors:
    print('VALIDATION FAILED — CDXMS Artifact Manager local apply via JCM v1.0.0')
    for e in errors:
        print('-', e)
    sys.exit(1)
print('VALIDATION OK — CDXMS Artifact Manager local apply via JCM v1.0.0')
