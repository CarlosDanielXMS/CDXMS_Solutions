#!/usr/bin/env python3
import json
from pathlib import Path
import sys


def find_src_root(script_file: str) -> Path:
    current = Path(script_file).resolve()
    candidates = [current.parent, *current.parents]
    for candidate in candidates:
        if (candidate / 'capabilities').is_dir() and (candidate / 'core').is_dir():
            return candidate
        if (candidate / 'src' / 'capabilities').is_dir() and (candidate / 'src' / 'core').is_dir():
            return candidate / 'src'
    raise SystemExit('[ERRO] Não foi possível localizar a raiz src do repositório/package.')


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise SystemExit(f'[ERRO] JSON inválido ou arquivo ilegível: {path}: {exc}')

ROOT = find_src_root(__file__)
base = ROOT / 'capabilities' / 'bootstrap'
required = [
    base / 'manifest.json',
    base / 'contract.json',
    base / 'config.default.json',
    base / 'remote_manifest.json',
    base / 'macrodroid' / '[CDXMS]_Bootstrap.ablock',
    ROOT / 'core' / 'enums.json',
    ROOT / 'core' / 'errors.json',
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit('[ERRO] Arquivos obrigatórios ausentes: ' + ', '.join(missing))

manifest = load_json(base / 'manifest.json')
contract = load_json(base / 'contract.json')
remote = load_json(base / 'remote_manifest.json')
ablock = load_json(base / 'macrodroid' / '[CDXMS]_Bootstrap.ablock')
enums = load_json(ROOT / 'core' / 'enums.json')
core_errors = load_json(ROOT / 'core' / 'errors.json')

errors = []
if manifest.get('capability', {}).get('id') != 'bootstrap': errors.append('manifest capability.id deve ser bootstrap')
if manifest.get('capability', {}).get('version') != '1.0.0': errors.append('version deve permanecer 1.0.0')
if manifest.get('macrodroid_export', {}).get('file_path') != 'capabilities/bootstrap/macrodroid/[CDXMS]_Bootstrap.ablock': errors.append('macrodroid_export.file_path inválido')
if manifest.get('requires', {}).get('capabilities', {}).get('json_config_manager') != '>=1.0.0': errors.append('dependência json_config_manager >=1.0.0 ausente')
contract_ops = list(contract.get('operations', {}).keys()) if isinstance(contract.get('operations'), dict) else contract.get('operations')
if manifest.get('operations') != contract_ops: errors.append('operations do manifest e contract divergentes')
outputs = contract.get('outputs', [])
if len(outputs) != 1 or outputs[0].get('name') != 'Resultado': errors.append('contract deve ter saída única Resultado')
if not set(['data_json','error_code','error_message','error_json']).issubset(set(contract.get('result', {}).get('forbidden_top_level_fields', []))): errors.append('campos top-level proibidos não declarados no contrato')
if not remote.get('source', {}).get('base_raw_url', '').endswith('/src'): errors.append('remote_manifest base_raw_url deve terminar com /src')
for item in remote.get('files', []):
    if str(item.get('target_path', '')).startswith('src/'):
        errors.append('target_path não deve começar com src/: ' + item.get('target_path', ''))
macro = ablock.get('macro', {})
if ablock.get('macroExportVersion') != 1: errors.append('macroExportVersion deve ser 1')
if macro.get('isActionBlock') is not True: errors.append('export deve ser Action Block')
if macro.get('m_name') != '[CDXMS] Bootstrap': errors.append('m_name inválido')
outputs = [v.get('m_name') for v in macro.get('localVariables', []) if v.get('supportsOutput')]
if outputs != ['Resultado']: errors.append(f'saídas públicas inválidas: {outputs}')
if 'bootstrap_operation' not in enums.get('enums', {}): errors.append('enum bootstrap_operation ausente')
if 'BOOTSTRAP_CORE_UNAVAILABLE' not in core_errors.get('errors', {}): errors.append('erro BOOTSTRAP_CORE_UNAVAILABLE ausente')

if errors:
    print('\n'.join('[ERRO] ' + e for e in errors))
    sys.exit(1)
print('[OK] Bootstrap v1.0.0 estruturalmente válido.')
