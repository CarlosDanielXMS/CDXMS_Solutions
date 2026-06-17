#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAP = ROOT / 'capabilities' / 'artifact_manager'
ABLOCK = CAP / 'macrodroid' / '[CDXMS]_Artifact_Manager.ablock'
MANIFEST = CAP / 'manifest.json'
CONTRACT = CAP / 'contract.json'
CONFIG = CAP / 'config.default.json'

errors = []

def fail(msg):
    errors.append(msg)

def load_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        fail(f'JSON inválido: {path} :: {exc}')
        return {}

for required in [ABLOCK, MANIFEST, CONTRACT, CONFIG]:
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
for name in local_names:
    if str(name).startswith('Tmp_'):
        v = next(x for x in locals_ if x.get('m_name') == name)
        if v.get('supportsOutput'):
            fail(f'Variável de trabalho exposta como output: {name}')

js_actions = [a for a in macro.get('m_actionList', []) if a.get('m_classType') == 'JavaScriptAction']
parse_actions = [a for a in macro.get('m_actionList', []) if a.get('m_classType') == 'JsonParseAction']
if len(js_actions) != 1:
    fail(f'Deve haver exatamente 1 JavaScriptAction, encontrado: {len(js_actions)}')
if len(parse_actions) != 1:
    fail(f'Deve haver exatamente 1 JsonParseAction, encontrado: {len(parse_actions)}')
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
    if js_out != parse_in:
        fail(f'Inconsistência: JavaScriptAction publica em {js_out}, JsonParseAction lê {parse_in}')
    if js_out not in local_names:
        fail(f'Variável de saída do JavaScript não existe nas locais: {js_out}')

manifest = load_json(MANIFEST) if MANIFEST.exists() else {}
ops = manifest.get('operations', [])
expected_ops = [
    'validate_artifact', 'get_artifact_status', 'build_registry_entry',
    'build_install_plan', 'get_target_paths', 'register_artifact',
    'unregister_artifact', 'ensure_artifact_files', 'install_local_artifact'
]
if ops != expected_ops:
    fail(f'Operações do manifest divergentes: {ops}')

if errors:
    print('VALIDATION FAILED — CDXMS Artifact Manager v1.0.0')
    for err in errors:
        print(f'- {err}')
    raise SystemExit(1)

print('VALIDATION OK — CDXMS Artifact Manager v1.0.0 incremental')
print(f'actions={len(macro.get("m_actionList", []))} inputs={len([v for v in locals_ if v.get("supportsInput")])} outputs={outputs}')
