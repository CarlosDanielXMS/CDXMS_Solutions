#!/usr/bin/env python3
import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
ablock = root / 'capabilities' / 'logger' / 'macrodroid' / '[CDXMS]_Logger.ablock'
manifest = root / 'capabilities' / 'logger' / 'manifest.json'
contract = root / 'capabilities' / 'logger' / 'contract.json'

for path in [ablock, manifest, contract]:
    if not path.exists():
        raise SystemExit(f'[ERRO] Arquivo obrigatório ausente: {path}')

export = json.loads(ablock.read_text(encoding='utf-8'))
macro = export.get('macro', {})
if export.get('macroExportVersion') != 1:
    raise SystemExit('[ERRO] macroExportVersion inválido.')
if macro.get('isActionBlock') is not True:
    raise SystemExit('[ERRO] Export não é Action Block.')
if macro.get('m_name') != '[CDXMS] Logger':
    raise SystemExit('[ERRO] Nome do Action Block inválido.')

locals_ = macro.get('localVariables', [])
outputs = [v for v in locals_ if v.get('supportsOutput')]
if [v.get('m_name') for v in outputs] != ['Resultado']:
    raise SystemExit('[ERRO] Saída pública precisa ser somente Resultado.')
for v in outputs:
    if v.get('m_name', '').startswith('Tmp_'):
        raise SystemExit('[ERRO] Variável Tmp_* exposta como output.')

if len(macro.get('exportedActionBlocks', [])) < 2:
    raise SystemExit('[ERRO] Logger deve exportar JCM e Result Manager como dependências de importação.')

print('[OK] Logger v1.0.0 estruturalmente válido.')
