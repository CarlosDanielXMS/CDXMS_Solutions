#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
required = [
    'capabilities/string_utils/manifest.json',
    'capabilities/string_utils/contract.json',
    'capabilities/string_utils/config.default.json',
    'capabilities/string_utils/remote_manifest.json',
    'capabilities/string_utils/README.md',
    'capabilities/string_utils/body.md',
    'capabilities/string_utils/tests/manual_test.md',
    'capabilities/string_utils/macrodroid/[CDXMS]_String_Utils.ablock',
    'core/enums.json',
    'core/errors.json',
    'release.json',
]
missing = [p for p in required if not (ROOT / p).exists()]
if missing:
    raise SystemExit('Arquivos ausentes: ' + ', '.join(missing))
manifest = json.loads((ROOT/'capabilities/string_utils/manifest.json').read_text(encoding='utf-8'))
assert manifest['capability']['id'] == 'string_utils'
assert manifest['requires']['capabilities']['result_manager'] == '>=1.0.0'
ablock = json.loads((ROOT/'capabilities/string_utils/macrodroid/[CDXMS]_String_Utils.ablock').read_text(encoding='utf-8'))
assert ablock['macroExportVersion'] == 1
assert ablock['macro']['isActionBlock'] is True
assert ablock['macro']['m_name'] == '[CDXMS] String Utils'
outputs = [v['m_name'] for v in ablock['macro']['localVariables'] if v.get('supportsOutput')]
assert outputs == ['Resultado'], outputs
leaked = [v['m_name'] for v in ablock['macro']['localVariables'] if v.get('supportsOutput') and v['m_name'].startswith('Tmp_')]
assert not leaked, leaked
print('[OK] String Utils incremental package estruturalmente válido.')
