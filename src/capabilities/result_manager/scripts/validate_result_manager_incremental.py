#!/usr/bin/env python3
import json, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[3]
ablock = root / 'capabilities' / 'result_manager' / 'macrodroid' / '[CDXMS]_Registrar_Resultado.ablock'
with ablock.open(encoding='utf-8') as f:
    data = json.load(f)
macro = data.get('macro', {})
errors = []
if data.get('macroExportVersion') != 1: errors.append('macroExportVersion deve ser 1')
if macro.get('isActionBlock') is not True: errors.append('macro.isActionBlock deve ser true')
if macro.get('m_name') != '[CDXMS] Registrar Resultado': errors.append('m_name incorreto')
if data.get('globalVariables') not in ([], None): errors.append('globalVariables deve estar vazio')
outputs = [v.get('m_name') for v in macro.get('localVariables', []) if v.get('supportsOutput')]
if outputs != ['Resultado']: errors.append(f'saídas públicas inválidas: {outputs}')
leaked = [v.get('m_name') for v in macro.get('localVariables', []) if v.get('m_name','').startswith('Tmp_') and v.get('supportsOutput')]
if leaked: errors.append(f'Tmp_* expostas como saída: {leaked}')
if errors:
    print('\n'.join('[ERRO] '+e for e in errors))
    sys.exit(1)
print('[OK] Result Manager export válido.')
