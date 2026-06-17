#!/usr/bin/env python3
import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
macro = root / 'homologation/am_dr_integration/macrodroid/[CDXMS]_Homologar_AM_DR_Integration_v1_0_0_TEMP.macro'
obj = json.loads(macro.read_text(encoding='utf-8'))
errors=[]
if obj.get('macroExportVersion') != 1: errors.append('macroExportVersion inválido')
m = obj.get('macro', {})
if m.get('isActionBlock') is not False: errors.append('macro temporária não deve ser Action Block')
if m.get('m_name') != '[CDXMS] Homologar AM + DR Integration v1.0.0 TEMP': errors.append('nome da macro inválido')
blocks = {b.get('m_name') for b in m.get('exportedActionBlocks', [])}
for expected in ['[CDXMS] Artifact Manager','[CDXMS] Dependency Resolver','[CDXMS] Bootstrap','[CDXMS] Logger']:
    if expected not in blocks: errors.append(f'Action Block embutido ausente: {expected}')
actions = m.get('m_actionList', [])
calls = [a.get('actionBlockName') for a in actions if a.get('m_classType') == 'ActionBlockAction']
if '[CDXMS] Artifact Manager' not in calls: errors.append('macro não chama Artifact Manager')
if '[CDXMS] Dependency Resolver' not in calls: errors.append('macro não chama Dependency Resolver')
if not any(v.get('m_name') == 'Tmp_AMDR_Summary' for v in m.get('localVariables', [])): errors.append('Tmp_AMDR_Summary ausente')
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print('VALIDATION OK — AM + DR Integration homologation temp macro v1.0.0')
print(f'actions={len(actions)} exported_action_blocks={len(blocks)}')
