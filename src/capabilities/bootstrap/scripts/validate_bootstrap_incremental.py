#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CAP=ROOT/'capabilities'/'bootstrap'
errors=[]
def load(p):
    try:return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:errors.append(f'JSON inválido: {p}: {e}');return {}
for p in [CAP/'manifest.json',CAP/'contract.json',CAP/'config.default.json',CAP/'macrodroid'/'[CDXMS]_Bootstrap.ablock']:
    if not p.exists():errors.append(f'Arquivo ausente: {p}')
ab=load(CAP/'macrodroid'/'[CDXMS]_Bootstrap.ablock') if (CAP/'macrodroid'/'[CDXMS]_Bootstrap.ablock').exists() else {}
m=ab.get('macro',{})
if ab.get('macroExportVersion')!=1:errors.append('macroExportVersion deve ser 1')
if m.get('isActionBlock') is not True:errors.append('Export deve ser Action Block')
if m.get('m_name')!='[CDXMS] Bootstrap':errors.append('Nome interno divergente')
outs=[v.get('m_name') for v in m.get('localVariables',[]) if v.get('supportsOutput')]
if outs!=['Resultado']:errors.append(f'Saída pública inválida: {outs}')
if errors:
 print('VALIDATION FAILED — bootstrap');[print('-',e) for e in errors];raise SystemExit(1)
print('VALIDATION OK — bootstrap v1.0.0')
