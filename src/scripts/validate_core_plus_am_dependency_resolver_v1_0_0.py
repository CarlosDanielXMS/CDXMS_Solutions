#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for cap in ['json_config_manager','bootstrap','result_manager','logger','string_utils','artifact_manager','dependency_resolver']:
 p=ROOT/'capabilities'/cap
 for f in ['manifest.json','contract.json','config.default.json','remote_manifest.json']:
  q=p/f
  if not q.exists():errors.append(f'ausente: {q}')
  else:
   try:json.loads(q.read_text(encoding='utf-8'))
   except Exception as e:errors.append(f'JSON inválido: {q}: {e}')
if errors:
 print('VALIDATION FAILED');[print('-',e) for e in errors];raise SystemExit(1)
print('VALIDATION OK — core capabilities v1.0.0')
