import json, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
errors=[]
am_contract = json.loads((root/'capabilities/artifact_manager/contract.json').read_text(encoding='utf-8'))
inputs=[i['name'] for i in am_contract['inputs']]
if 'Apply Changes?' not in inputs: errors.append('Artifact Manager contract missing Apply Changes?')
ab = json.loads((root/'capabilities/artifact_manager/macrodroid/[CDXMS]_Artifact_Manager.ablock').read_text(encoding='utf-8'))
macro=ab.get('macro',{})
if not macro.get('isActionBlock'): errors.append('Artifact Manager export is not action block')
local_names=[v.get('m_name') for v in macro.get('localVariables',[])]
for name in ['Apply Changes?','Tmp_ArtifactWorkJson','Tmp_ArtifactWork','Resultado']:
    if name not in local_names: errors.append(f'missing local variable {name}')
actions=macro.get('m_actionList',[])
if not any(a.get('m_classType')=='ShellScriptAction' and 'should_apply' in a.get('m_script','') for a in actions):
    errors.append('missing controlled ShellScriptAction apply gate')
if not any(a.get('m_classType')=='JsonParseAction' and a.get('dictionaryVarName')=='Tmp_ArtifactWork' for a in actions):
    errors.append('missing Tmp_ArtifactWork parse')
if not any(a.get('m_classType')=='JsonParseAction' and a.get('dictionaryVarName')=='Resultado' for a in actions):
    errors.append('missing Resultado parse')
macro_path = root/'homologation/am_local_apply/macrodroid/[CDXMS]_Homologar_AM_Local_Apply_v1_0_0_TEMP.macro'
if macro_path.exists():
    hm=json.loads(macro_path.read_text(encoding='utf-8'))['macro']
    found=False
    for embedded in hm.get('exportedActionBlocks',[]):
        if embedded.get('m_name')=='[CDXMS] Artifact Manager':
            found=True
            names=[v.get('m_name') for v in embedded.get('localVariables',[])]
            if 'Apply Changes?' not in names: errors.append('homologation embedded Artifact Manager missing Apply Changes?')
            if len(embedded.get('m_actionList',[])) < 7: errors.append('homologation embedded Artifact Manager not local-apply version')
    if not found: errors.append('homologation macro missing embedded Artifact Manager')
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print('VALIDATION OK — CDXMS Artifact Manager local apply v1.0.0')
