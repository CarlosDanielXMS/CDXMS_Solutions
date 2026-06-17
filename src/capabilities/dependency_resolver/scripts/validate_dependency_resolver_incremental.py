import json
from pathlib import Path

root = Path(__file__).resolve().parents[3]
ablock = root / 'capabilities' / 'dependency_resolver' / 'macrodroid' / '[CDXMS]_Dependency_Resolver.ablock'
obj = json.loads(ablock.read_text(encoding='utf-8'))
macro = obj['macro']
assert macro['isActionBlock'] is True
assert macro['m_name'] == '[CDXMS] Dependency Resolver'
outputs = [v['m_name'] for v in macro['localVariables'] if v.get('supportsOutput')]
assert outputs == ['Resultado']
assert not [v['m_name'] for v in macro['localVariables'] if v.get('supportsOutput') and v['m_name'].startswith('Tmp_')]
assert any(a.get('m_classType') == 'JavaScriptAction' for a in macro['m_actionList'])
assert any(a.get('m_classType') == 'JsonParseAction' and a.get('dictionaryVarName') == 'Resultado' for a in macro['m_actionList'])
print('VALIDATION OK — CDXMS Dependency Resolver v1.0.0 incremental')
