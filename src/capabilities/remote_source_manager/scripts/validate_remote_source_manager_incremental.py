#!/usr/bin/env python3
import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CAP = ROOT / 'capabilities' / 'remote_source_manager'
ERRORS = []

def error(msg): ERRORS.append(msg)
def load(path):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: error(f'{path}: JSON inválido: {exc}'); return {}

required = ['manifest.json','contract.json','config.default.json','remote_manifest.json','README.md','body.md','tests/manual_test.md','macrodroid/[CDXMS]_Remote_Source_Manager.ablock']
for rel in required:
    if not (CAP/rel).is_file(): error(f'Arquivo ausente: {rel}')

manifest = load(CAP/'manifest.json')
contract = load(CAP/'contract.json')
config = load(CAP/'config.default.json')
export = load(CAP/'macrodroid/[CDXMS]_Remote_Source_Manager.ablock')
macro = export.get('macro', {})

if manifest.get('capability',{}).get('id') != 'remote_source_manager': error('manifest artifact id inválido')
if macro.get('m_name') != '[CDXMS] Remote Source Manager': error('nome do Action Block inválido')
if macro.get('isActionBlock') is not True: error('export não é Action Block')
if export.get('macroExportVersion') != 1: error('macroExportVersion inválido')
if macro.get('breakpoints') not in ([],None): error('breakpoints ativos')

inputs_contract = [x.get('name') for x in contract.get('inputs',[])]
inputs_export = [x.get('m_name') for x in macro.get('localVariables',[]) if x.get('supportsInput')]
if inputs_contract != inputs_export: error(f'inputs divergentes: contract={inputs_contract} export={inputs_export}')
outputs = [x.get('m_name') for x in macro.get('localVariables',[]) if x.get('supportsOutput')]
if outputs != ['Resultado']: error(f'saída pública inválida: {outputs}')
works = [x.get('m_name') for x in macro.get('localVariables',[]) if x.get('isActionBlockWorkingVar')]
if not works or any(not x.startswith('Tmp_') for x in works): error(f'variáveis de trabalho inválidas: {works}')

classes = [x.get('m_classType') for x in macro.get('m_actionList',[])]
if classes.count('HttpRequestAction') != 1: error('esperado exatamente 1 HttpRequestAction')
if classes.count('ActionBlockAction') != 2: error('esperadas 2 chamadas JCM')
if 'ShellScriptAction' in classes: error('ShellScriptAction não permitido no Remote Source Manager')
if classes[-1:] != ['ExitActionBlockAction']: error('última ação deve ser ExitActionBlockAction')

http = next((x for x in macro.get('m_actionList',[]) if x.get('m_classType')=='HttpRequestAction'), {})
rc = http.get('requestConfig',{})
checks = {
 'requestType':0,'followRedirects':True,'allowAnyCertificate':False,'blockNextAction':True,
 'saveReturnCodeToVariable':True,'returnCodeVariableName':'Tmp_HttpStatusCode',
 'saveReturnHeadersToVariable':True,'returnHeadersVariableName':'Tmp_HttpHeaders',
 'saveResponseUseAllFilesAccess':True,'saveResponseType':2,
}
for key,value in checks.items():
    if rc.get(key) != value: error(f'HTTP requestConfig.{key} esperado {value!r}, obtido {rc.get(key)!r}')
if '/blob/' in rc.get('urlToOpen',''): error('URL /blob/ no export')
if rc.get('urlToOpen') != '{lv=Tmp_RequestUrl}': error('HTTP URL não usa ponte escalar validada')
if rc.get('saveResponseAllFilesAccessPath') != '{lv=Tmp_StagingFilePath}': error('HTTP saveResponseAllFilesAccessPath deve receber o caminho completo Tmp_StagingFilePath')
if rc.get('saveResponseFileName') != '': error('HTTP saveResponseFileName deve permanecer vazio no modo All Files Access homologado')

jcm_calls = [x for x in macro.get('m_actionList',[]) if x.get('m_classType')=='ActionBlockAction']
for call in jcm_calls:
    if call.get('actionBlockName') != '[CDXMS] Json Config Manager': error('dependência inesperada no export')
    if call.get('actionBlockId') != -8263168847136168061: error('GUID JCM divergente')
    if call.get('continueActionsWithoutWaiting') is not False: error('chamada JCM deve aguardar')
ops = [x.get('inputVarsMap',{}).get('Operation') for x in jcm_calls]
if ops != ['ensure_folder','read_json']: error(f'operações JCM divergentes: {ops}')


# Regressões de homologação: JavaScriptAction publica pela última expressão.
js_actions = [x for x in macro.get('m_actionList',[]) if x.get('m_classType') == 'JavaScriptAction']
prep = next((x for x in js_actions if x.get('actionLabel') == 'Validar fonte e montar request'), {})
finalize = next((x for x in js_actions if x.get('actionLabel') == 'Consolidar Resultado remoto'), {})
for label, action in [('preflight', prep), ('finalização', finalize)]:
    script = action.get('scriptText','')
    if script.lstrip().startswith('(function(){'):
        error(f'{label} JavaScript não deve depender do retorno de IIFE')
    if not script.rstrip().endswith('__rsmOutput;'):
        error(f'{label} JavaScript deve publicar pela última expressão')
prep_script = prep.get('scriptText','')
finalize_script = finalize.get('scriptText','')
if 'pre_result_json' in prep_script or 'pre_result_json' in finalize_script:
    error('JSON textual aninhado pre_result_json é proibido')
if 'pre_result:preResult' not in prep_script or 'pre_result:r' not in prep_script:
    error('preflight não publica pre_result como objeto em todos os fluxos')
if 'work.pre_result && typeof work.pre_result === "object"' not in finalize_script:
    error('finalização não lê pre_result como objeto')
if '__rsmOutput = JSON.stringify(pre);' not in finalize_script:
    error('finalização não serializa pre_result exatamente uma vez')
if 'return pre;' in finalize.get('scriptText',''):
    error('finalização ainda usa return no fluxo principal')
for required_var in ['Tmp_ShouldRequestText','Tmp_RequestUrl','Tmp_StagingFolderPath','Tmp_StagingFileName','Tmp_StagingFilePath','Tmp_JcmReadResultJson']:
    if required_var not in works: error(f'ponte escalar ausente: {required_var}')

supported = set(manifest.get('operations',[]))
expected = {'validate_source','get_source_status','fetch_catalog','fetch_release_manifest','fetch_remote_manifest','fetch_json'}
if supported != expected: error(f'operações divergentes: {supported}')
if config.get('settings',{}).get('artifact_payload_download_enabled') is not False: error('payload download deve permanecer bloqueado')
if config.get('settings',{}).get('allowed_hosts') != ['raw.githubusercontent.com']: error('host permitido inválido')

# Integration with catalog/release/core enums/errors.
catalog = load(ROOT/'catalogs/local_catalog.default.json')
ids = {x.get('artifact_id') for x in catalog.get('capabilities',[])}
if 'remote_source_manager' not in ids: error('capability ausente do catálogo')
release = load(ROOT/'release.json')
release_ids = {x.get('artifact_id') for x in release.get('artifacts',[])}
if 'remote_source_manager' not in release_ids: error('capability ausente da release')
enums = load(ROOT/'core/enums.json').get('enums',{})
if set(enums.get('remote_source_manager_operation',{}).values()) != expected: error('enum de operações divergente')
errors = load(ROOT/'core/errors.json').get('errors',{})
for code in ['REMOTE_SOURCE_INVALID','REMOTE_SOURCE_DISABLED','HTTP_REQUEST_FAILED','HTTP_UNEXPECTED_STATUS','HTTP_INVALID_RESPONSE','REMOTE_CACHE_VERIFICATION_FAILED']:
    if code not in errors: error(f'erro core ausente: {code}')

remote = load(CAP/'remote_manifest.json')
for item in remote.get('files',[]):
    path = ROOT/item.get('path','')
    if not path.is_file(): error(f'arquivo remoto ausente: {item.get("path")}')
    elif hashlib.sha256(path.read_bytes()).hexdigest() != item.get('checksum_sha256'): error(f'checksum remoto divergente: {item.get("path")}')

if ERRORS:
    print('VALIDATION FAILED — Remote Source Manager v1.0.0')
    for item in ERRORS: print('-',item)
    raise SystemExit(1)
print('VALIDATION OK — Remote Source Manager v1.0.0')
print(f'actions={len(classes)} working_vars={len(works)} operations={len(expected)} http_requests=1 jcm_calls=2')
print('scope=control_plane_only artifact_payload_download_enabled=false checksum=false_success_claim_blocked')
