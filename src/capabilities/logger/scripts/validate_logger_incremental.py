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
base = ROOT / 'capabilities' / 'logger'
required = [
    base / 'manifest.json',
    base / 'contract.json',
    base / 'config.default.json',
    base / 'remote_manifest.json',
    base / 'macrodroid' / '[CDXMS]_Logger.ablock',
]
missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
if missing:
    raise SystemExit('[ERRO] Arquivos obrigatórios ausentes: ' + ', '.join(missing))
manifest = load_json(base / 'manifest.json')
contract = load_json(base / 'contract.json')
remote = load_json(base / 'remote_manifest.json')
ablock = load_json(base / 'macrodroid' / '[CDXMS]_Logger.ablock')
errors = []
if manifest.get('capability', {}).get('id') != 'logger': errors.append('manifest capability.id inválido')
if manifest.get('capability', {}).get('version') != '1.0.0': errors.append('version deve permanecer 1.0.0')
expected_deps = {'json_config_manager': '>=1.0.0', 'result_manager': '>=1.0.0'}
if manifest.get('requires', {}).get('capabilities', {}) != expected_deps: errors.append('dependências inválidas')
contract_ops = list(contract.get('operations', {}).keys()) if isinstance(contract.get('operations'), dict) else contract.get('operations')
if manifest.get('operations') != contract_ops: errors.append('operations do manifest e contract divergentes')
if not remote.get('source', {}).get('base_raw_url', '').endswith('/src'): errors.append('remote_manifest base_raw_url deve terminar com /src')
for item in remote.get('files', []):
    if str(item.get('target_path', '')).startswith('src/'):
        errors.append('target_path não deve começar com src/: ' + item.get('target_path', ''))
macro = ablock.get('macro', {})
if ablock.get('macroExportVersion') != 1: errors.append('macroExportVersion inválido')
if macro.get('isActionBlock') is not True: errors.append('export não é Action Block')
if macro.get('m_name') != '[CDXMS] Logger': errors.append('nome do Action Block inválido')
outputs = [v.get('m_name') for v in macro.get('localVariables', []) if v.get('supportsOutput')]
if outputs != ['Resultado']: errors.append('saída pública precisa ser somente Resultado')
if len(macro.get('exportedActionBlocks', [])) < 2: errors.append('Logger deve exportar JCM e Result Manager como dependências de importação')
if errors:
    print('\n'.join('[ERRO] '+e for e in errors))
    sys.exit(1)
print('[OK] Logger v1.0.0 estruturalmente válido.')
