#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAP = ROOT / 'capabilities' / 'artifact_manager'
ABLOCK = CAP / 'macrodroid' / '[CDXMS]_Artifact_Manager.ablock'
MANIFEST = CAP / 'manifest.json'
CONTRACT = CAP / 'contract.json'
CONFIG = CAP / 'config.default.json'
BODY = CAP / 'body.md'
README = CAP / 'README.md'

errors = []

def fail(msg):
    errors.append(msg)

def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'JSON inválido: {path} :: {exc}')
        return {}

for required in [ABLOCK, MANIFEST, CONTRACT, CONFIG, BODY, README]:
    if not required.exists():
        fail(f'Arquivo obrigatório ausente: {required}')

ab = load_json(ABLOCK) if ABLOCK.exists() else {}
macro = ab.get('macro', {})
if ab.get('macroExportVersion') != 1:
    fail('macroExportVersion deve ser 1')
if macro.get('isActionBlock') is not True:
    fail('Artifact Manager deve ser Action Block')
if macro.get('m_name') != '[CDXMS] Artifact Manager':
    fail('Nome interno inválido')
if ab.get('globalVariables') not in ([], None):
    fail('Não deve exportar variáveis globais')

locals_ = macro.get('localVariables', [])
local_names = {v.get('m_name') for v in locals_}
outputs = [v.get('m_name') for v in locals_ if v.get('supportsOutput')]
if outputs != ['Resultado']:
    fail(f'Saída pública deve ser somente Resultado, encontrado: {outputs}')
for required_local in ['Operation', 'Artifact Type', 'Artifact Id', 'Apply Changes?', 'Dry Run?', 'Resultado', 'Tmp_ArtifactWorkJson']:
    if required_local not in local_names:
        fail(f'Variável local obrigatória ausente: {required_local}')
for name in local_names:
    if str(name).startswith('Tmp_'):
        v = next(x for x in locals_ if x.get('m_name') == name)
        if v.get('supportsOutput'):
            fail(f'Variável de trabalho exposta como output: {name}')

actions = macro.get('m_actionList', [])
js_actions = [a for a in actions if a.get('m_classType') == 'JavaScriptAction']
parse_actions = [a for a in actions if a.get('m_classType') == 'JsonParseAction']
shell_actions = [a for a in actions if a.get('m_classType') == 'ShellScriptAction']
if len(js_actions) != 1:
    fail(f'Deve haver exatamente 1 JavaScriptAction, encontrado: {len(js_actions)}')
if len(parse_actions) != 1:
    fail(f'Deve haver exatamente 1 JsonParseAction, encontrado: {len(parse_actions)}')
if shell_actions:
    fail('Artifact Manager não pode conter ShellScriptAction como executor de apply')
if js_actions:
    script = js_actions[0].get('scriptText', '')
    for expected in ['json_config_manager', 'jcm_apply_plan', 'jcm_verification_plan']:
        if expected not in script:
            fail(f'JavaScriptAction deve declarar {expected}')
    if 'side_effects_delegated_to_shell' in script:
        fail('JavaScriptAction não pode retornar side_effects_delegated_to_shell')
if js_actions and parse_actions:
    js_out = js_actions[0].get('stringVariableName')
    parse_in = parse_actions[0].get('stringVarName')
    parse_out = parse_actions[0].get('dictionaryVarName')
    if js_out != 'Tmp_ArtifactWorkJson':
        fail(f'JavaScriptAction deve publicar em Tmp_ArtifactWorkJson, encontrado: {js_out}')
    if parse_in != 'Tmp_ArtifactWorkJson':
        fail(f'JsonParseAction deve ler Tmp_ArtifactWorkJson, encontrado: {parse_in}')
    if parse_out != 'Resultado':
        fail(f'JsonParseAction deve publicar em Resultado, encontrado: {parse_out}')

manifest = load_json(MANIFEST) if MANIFEST.exists() else {}
ops = manifest.get('operations', [])
for expected in ['build_jcm_apply_plan', 'verify_local_apply', 'install_local_artifact']:
    if expected not in ops:
        fail(f'Operação esperada ausente no manifest: {expected}')
if manifest.get('lifecycle_scope', {}).get('apply_executor') != 'json_config_manager':
    fail('Manifest deve declarar apply_executor=json_config_manager')

contract = load_json(CONTRACT) if CONTRACT.exists() else {}
contract_text = json.dumps(contract, ensure_ascii=False)
if 'side_effects_delegated_to_shell' in contract_text:
    fail('Contrato não deve declarar side_effects_delegated_to_shell')
for expected in ['jcm_apply_plan', 'jcm_verification_plan', 'ARTIFACT_APPLY_REQUIRES_JCM']:
    if expected not in contract_text:
        fail(f'Contrato deve declarar {expected}')

config = load_json(CONFIG) if CONFIG.exists() else {}
settings = config.get('settings', {})
if settings.get('apply_executor') != 'json_config_manager':
    fail('Config deve usar apply_executor=json_config_manager')
if settings.get('allow_shell_apply') is not False:
    fail('Config deve bloquear allow_shell_apply=false')
if settings.get('require_post_write_verification') is not True:
    fail('Config deve exigir require_post_write_verification=true')

for path in [BODY, README]:
    text = path.read_text(encoding='utf-8') if path.exists() else ''
    if 'Shell Script' in text or 'ShellScriptAction' in text:
        fail(f'{path.name} não deve orientar Shell como executor do AM')
    if 'Json Config Manager' not in text:
        fail(f'{path.name} deve documentar execução via Json Config Manager')

if errors:
    print('VALIDATION FAILED — CDXMS Artifact Manager v1.0.0 JCM apply consolidation')
    for err in errors:
        print(f'- {err}')
    raise SystemExit(1)

print('VALIDATION OK — CDXMS Artifact Manager v1.0.0 JCM apply consolidation')
print(f'actions={len(actions)} inputs={len([v for v in locals_ if v.get("supportsInput")])} outputs={outputs}')
