import json, pathlib, sys
base=pathlib.Path(__file__).resolve().parents[1]
errors=[]
def read(p): return json.loads((base/p).read_text(encoding='utf-8'))
dr=read('capabilities/dependency_resolver/manifest.json')
am=read('capabilities/artifact_manager/manifest.json')
amc=read('capabilities/artifact_manager/contract.json')
if 'artifact_manager' in dr.get('requires',{}).get('capabilities',{}): errors.append('Dependency Resolver still depends on Artifact Manager')
if am.get('integrates_with',{}).get('capabilities',{}).get('dependency_resolver') != '>=1.0.0': errors.append('Artifact Manager integration metadata missing')
if not any(i.get('name')=='Dependency Resolution Json' for i in amc.get('inputs',[])): errors.append('Artifact Manager contract missing Dependency Resolution Json')
ab=read('capabilities/artifact_manager/macrodroid/[CDXMS]_Artifact_Manager.ablock')
vars=[v.get('m_name') for v in ab['macro'].get('localVariables',[])]
if 'Dependency Resolution Json' not in vars: errors.append('Artifact Manager ablock missing Dependency Resolution Json input')
script=ab['macro']['m_actionList'][1].get('scriptText','')
for needle in ['normalizeResolutionPlan','Dependency Resolution Json','dependency_resolution']:
    if needle not in script: errors.append(f'Artifact Manager script missing {needle}')
macro=read('homologation/am_dr_integration/macrodroid/[CDXMS]_Homologar_AM_DR_Integration_v1_0_0_TEMP.macro')
if not any(a.get('m_classType')=='JsonOutputAction' and a.get('dictionaryVarName')=='Tmp_DR_ResolutionPlan' for a in macro['macro']['m_actionList']): errors.append('Homologation macro missing JsonOutputAction for DR result')
if not any(a.get('m_classType')=='ActionBlockAction' and a.get('actionBlockName')=='[CDXMS] Artifact Manager' and 'Dependency Resolution Json' in a.get('inputVarsMap',{}) for a in macro['macro']['m_actionList']): errors.append('Homologation macro does not pass Dependency Resolution Json to AM')
if errors:
    print('VALIDATION FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print('VALIDATION OK — CDXMS AM/DR Concept Remodel v1.0.0')
