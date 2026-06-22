#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
CAP=ROOT/'capabilities/file_integrity'
EXPORT=CAP/'macrodroid/[CDXMS]_File_Integrity.ablock'
ERRORS=[]
def error(msg): ERRORS.append(msg)
def load(path):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc: error(f'{path}: JSON inválido: {exc}'); return {}

for rel in ['README.md','body.md','config.default.json','contract.json','manifest.json','remote_manifest.json','tests/manual_test.md']:
    if not (CAP/rel).is_file(): error(f'Arquivo obrigatório ausente: {rel}')

payload=load(EXPORT)
macro=payload.get('macro',{})
actions=macro.get('m_actionList',[])
if payload.get('macroExportVersion')!=1: error('macroExportVersion deve ser 1')
if macro.get('m_name')!='[CDXMS] File Integrity': error('Nome divergente')
if macro.get('isActionBlock') is not True: error('Export deve ser Action Block')
if macro.get('m_GUID')!=-4096156049327197001: error('GUID divergente')
if len(actions)!=21: error(f'Perfil de ações inesperado: {len(actions)}')
inputs=[v.get('m_name') for v in macro.get('localVariables',[]) if v.get('supportsInput')]
expected_inputs=['Operation','File Path','Expected SHA-256','Session Id','Correlation Id']
if inputs!=expected_inputs: error(f'Inputs divergentes: {inputs}')
outputs=[v.get('m_name') for v in macro.get('localVariables',[]) if v.get('supportsOutput')]
if outputs!=['Resultado']: error(f'Output divergente: {outputs}')
working=[v for v in macro.get('localVariables',[]) if v.get('isActionBlockWorkingVar')]
if not working or any(not v.get('description') for v in working): error('Todas as variáveis de trabalho devem possuir descrição')

shells=[a for a in actions if a.get('m_classType')=='ShellScriptAction']
if len(shells)!=1: error(f'Deve existir exatamente uma ShellScriptAction: {len(shells)}')
else:
    shell=shells[0]
    if shell.get('m_nonRoot') is not True: error('Shell deve ser non-root')
    if shell.get('useHelper') is not False: error('Shell não pode usar Helper')
    if shell.get('useShizuku') is not False: error('Shell não pode usar Shizuku')
    script=shell.get('m_script','')
    if '/system/bin/sha256sum' not in script: error('Executor homologado ausente')
    for forbidden in ['eval ', 'curl ', 'wget ', 'rm -rf', '{lv=Operation}', '{lv=Expected SHA-256}']:
        if forbidden in script: error(f'Conteúdo proibido no shell: {forbidden}')
    if '$EXECUTOR "$FILE_PATH"' not in script: error('Path não está protegido por aspas no comando')

js_actions=[a for a in actions if a.get('m_classType')=='JavaScriptAction']
if len(js_actions)!=7: error(f'Esperadas 7 JavaScriptAction: {len(js_actions)}')
for action in js_actions:
    code=action.get('scriptText','')
    if re.search(r'(?m)^return\b',code): error(f'Return no escopo principal: {action.get("actionLabel")}')
    with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8') as h:
        h.write(code); path=Path(h.name)
    try:
        result=subprocess.run(['node','--check',str(path)],capture_output=True,text=True,check=False)
        if result.returncode!=0: error(f'JavaScript inválido em {action.get("actionLabel")}: {result.stderr}')
    finally: path.unlink(missing_ok=True)

pre=next((a.get('scriptText','') for a in js_actions if a.get('actionLabel')=='Validar operação e caminho'),'')
for marker in ['calculate_sha256','verify_sha256','UNSAFE_FILE_PATH','^[0-9a-f]{64}$','pre_result']:
    if marker not in pre: error(f'Preflight sem marcador: {marker}')
final=next((a.get('scriptText','') for a in js_actions if a.get('actionLabel')=='Consolidar Resultado de integridade'),'')
for marker in ['CHECKSUM_MISMATCH','CHECKSUM_EXECUTOR_UNAVAILABLE','CHECKSUM_INVALID_OUTPUT','FILE_NOT_FOUND','cleanup']:
    if marker not in final: error(f'Finalização sem marcador: {marker}')

jcm_calls=[a for a in actions if a.get('m_classType')=='ActionBlockAction']
if [a.get('inputVarsMap',{}).get('Operation') for a in jcm_calls]!=['ensure_folder','delete_file']:
    error('Chamadas JCM devem ser ensure_folder e delete_file')
if any(a.get('actionBlockId')!=-8263168847136168061 for a in jcm_calls): error('GUID do JCM divergente')

read=[a for a in actions if a.get('m_classType')=='ReadFileAction']
if len(read)!=1 or read[0].get('allFilesAccessPath')!='{lv=Tmp_ReportFilePath}' or read[0].get('variableName')!='Tmp_ShellReportJson':
    error('ReadFileAction não lê o relatório temporário validado')

manifest=load(CAP/'manifest.json')
if manifest.get('requires',{}).get('capabilities',{}).get('json_config_manager')!='>=1.0.0': error('Dependência JCM ausente')
audit=manifest.get('implementation_audit',{})
evidence=audit.get('runtime_evidence',{})
if evidence.get('passed_checks')!=7 or evidence.get('failed_checks')!=0 or evidence.get('selected_executor')!='/system/bin/sha256sum': error('Evidência runtime divergente')
prod=audit.get('production_capability_homologation',{})
if prod.get('status')!='homologated': error('Capability deve permanecer marcada como homologated após a validação real')
if prod.get('manual_homologation_required') is not False: error('manual_homologation_required deve ser false após homologação')
if prod.get('passed_checks')!=11 or prod.get('failed_checks')!=0: error('Evidência da homologação de produção deve registrar 11/11')
if prod.get('macro')!='[CDXMS] Homologar File Integrity v1.0.0 TEMP': error('Macro de evidência da homologação divergente')

contract=load(CAP/'contract.json')
if [x.get('name') for x in contract.get('inputs',[])]!=inputs: error('Contract/export inputs divergentes')
if set(contract.get('operations',{}))!={'calculate_sha256','verify_sha256'}: error('Operações do contrato divergentes')

if ERRORS:
    print('File Integrity incremental validator: FAIL')
    for item in ERRORS: print('-',item)
    raise SystemExit(1)
print('File Integrity incremental validator: OK')
print(f'actions={len(actions)} working_vars={len(working)} shell=1 jcm_calls=2 operations=2')
