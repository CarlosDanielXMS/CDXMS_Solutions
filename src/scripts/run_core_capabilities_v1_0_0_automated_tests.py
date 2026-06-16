#!/usr/bin/env python3
import json, zipfile, hashlib, subprocess, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
CAPS = {
    'json_config_manager': '[CDXMS] Json Config Manager',
    'bootstrap': '[CDXMS] Bootstrap',
    'result_manager': '[CDXMS] Registrar Resultado',
    'logger': '[CDXMS] Logger',
    'string_utils': '[CDXMS] String Utils',
}
ABLOCKS = {
    'json_config_manager': '[CDXMS]_Json_Config_Manager.ablock',
    'bootstrap': '[CDXMS]_Bootstrap.ablock',
    'result_manager': '[CDXMS]_Registrar_Resultado.ablock',
    'logger': '[CDXMS]_Logger.ablock',
    'string_utils': '[CDXMS]_String_Utils.ablock',
}
DEPENDENCIES = {
    'json_config_manager': {},
    'bootstrap': {'json_config_manager': '>=1.0.0'},
    'result_manager': {},
    'logger': {'json_config_manager': '>=1.0.0', 'result_manager': '>=1.0.0'},
    'string_utils': {'result_manager': '>=1.0.0'},
}
FORBIDDEN_TOP = {'data_json','error_code','error_message','error_json'}
results=[]; failures=[]; warnings=[]; stats={}

def ok(name, details=''): results.append(('PASS', name, details))
def fail(name, details): results.append(('FAIL', name, details)); failures.append((name,details))
def warn(name, details): results.append(('WARN', name, details)); warnings.append((name,details))
def load_json(path): return json.loads(path.read_text(encoding='utf-8'))
def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

json_files=sorted(ROOT.rglob('*.json'))
invalid=[]
for p in json_files:
    try: load_json(p)
    except Exception as exc: invalid.append((p, exc))
if not invalid: ok('JSON validity', f'{len(json_files)} arquivos .json válidos.')
else: fail('JSON validity', '; '.join(f'{p}: {e}' for p,e in invalid))

try:
    ck=load_json(ROOT/'checksums.json')
    mism=[]; missing=[]
    for rel, expected in ck.get('files',{}).items():
        p=ROOT/rel
        if not p.exists(): missing.append(rel); continue
        actual=sha256(p)
        if actual != expected: mism.append((rel, expected, actual))
    if not missing and not mism: ok('checksums.json', f'{len(ck.get("files",{}))} checksums conferem.')
    else: fail('checksums.json', f'ausentes={missing}; divergentes={mism[:10]}')
except Exception as exc: fail('checksums.json', str(exc))

for path in ['core/manifest.json','core/enums.json','core/errors.json','core/result_contract.json','release.json','README.md','CHANGELOG.md','.cdxms_root.json']:
    if (ROOT/path).exists(): ok(f'core file {path}', 'Presente.')
    else: fail(f'core file {path}', 'Ausente.')

try:
    release=load_json(ROOT/'release.json')
    artifacts={a.get('artifact_id'): a for a in release.get('artifacts',[])}
    if set(CAPS).issubset(artifacts): ok('release artifacts', ', '.join(CAPS.keys()))
    else: fail('release artifacts', f'faltando {set(CAPS)-set(artifacts)}')
    drift=[(cid, artifacts[cid].get('version')) for cid in CAPS if artifacts.get(cid,{}).get('version')!='1.0.0']
    if not drift: ok('version lock', 'Todas as capabilities em 1.0.0.')
    else: fail('version lock', str(drift))
except Exception as exc: fail('release.json', str(exc))

try:
    enums=load_json(ROOT/'core/enums.json').get('enums',{})
    errors=load_json(ROOT/'core/errors.json').get('errors',{})
    for key in ['artifact_type','result_status','jcm_operation','bootstrap_operation','result_manager_operation','logger_operation','string_utils_operation']:
        ok(f'enum {key}', 'Presente.') if key in enums else fail(f'enum {key}', 'Ausente.')
    for key in ['MISSING_REQUIRED_INPUT','INVALID_JSON','BOOTSTRAP_CORE_UNAVAILABLE','RESULT_INVALID_CONTRACT','LOGGER_WRITE_FAILED','STRING_TRANSFORM_FAILED']:
        ok(f'error {key}', 'Presente.') if key in errors else fail(f'error {key}', 'Ausente.')
except Exception as exc: fail('core enums/errors', str(exc))

for cid, display in CAPS.items():
    base=ROOT/'capabilities'/cid
    required=['manifest.json','contract.json','config.default.json','remote_manifest.json','README.md','body.md','tests/manual_test.md','macrodroid/'+ABLOCKS[cid]]
    missing=[p for p in required if not (base/p).exists()]
    ok(f'{cid}: required files', 'Todos presentes.') if not missing else fail(f'{cid}: required files', ', '.join(missing))
    try:
        manifest=load_json(base/'manifest.json'); contract=load_json(base/'contract.json'); remote=load_json(base/'remote_manifest.json'); config=load_json(base/'config.default.json')
        ok(f'{cid}: manifest id', cid) if manifest.get('capability',{}).get('id')==cid else fail(f'{cid}: manifest id', str(manifest.get('capability',{}).get('id')))
        ok(f'{cid}: version', '1.0.0') if manifest.get('capability',{}).get('version')=='1.0.0' else fail(f'{cid}: version', str(manifest.get('capability',{}).get('version')))
        ok(f'{cid}: dependencies', str(DEPENDENCIES[cid])) if manifest.get('requires',{}).get('capabilities',{})==DEPENDENCIES[cid] else fail(f'{cid}: dependencies', str(manifest.get('requires',{}).get('capabilities',{})))
        ops=contract.get('operations',{})
        if isinstance(ops, dict): ops=list(ops.keys())
        ok(f'{cid}: operations', f'{len(ops)} coerentes.') if manifest.get('operations')==ops else fail(f'{cid}: operations', f"manifest={manifest.get('operations')} contract={ops}")
        outs=contract.get('outputs',[])
        ok(f'{cid}: contract output', 'Resultado') if len(outs)==1 and outs[0].get('name')=='Resultado' else fail(f'{cid}: contract output', str(outs))
        forbidden=set(contract.get('result',{}).get('forbidden_top_level_fields',[]))
        ok(f'{cid}: forbidden top-level fields', ', '.join(sorted(FORBIDDEN_TOP))) if FORBIDDEN_TOP.issubset(forbidden) else fail(f'{cid}: forbidden top-level fields', str(FORBIDDEN_TOP-forbidden))
        ok(f'{cid}: remote base_raw_url', remote.get('source',{}).get('base_raw_url')) if remote.get('source',{}).get('base_raw_url','').endswith('/src') else fail(f'{cid}: remote base_raw_url', remote.get('source',{}).get('base_raw_url'))
        bad=[f.get('target_path') for f in remote.get('files',[]) if str(f.get('target_path','')).startswith('src/')]
        ok(f'{cid}: target_path no src', 'OK') if not bad else fail(f'{cid}: target_path no src', str(bad))
        ok(f'{cid}: config default', 'schema_version=1 namespace=CDXMS') if config.get('schema_version')==1 and config.get('namespace')=='CDXMS' else fail(f'{cid}: config default', str(config))
    except Exception as exc: fail(f'{cid}: metadata', str(exc))
    try:
        ab=load_json(base/'macrodroid'/ABLOCKS[cid]); macro=ab.get('macro',{})
        ok(f'{cid}: macroExportVersion', '1') if ab.get('macroExportVersion')==1 else fail(f'{cid}: macroExportVersion', str(ab.get('macroExportVersion')))
        ok(f'{cid}: isActionBlock', 'true') if macro.get('isActionBlock') is True else fail(f'{cid}: isActionBlock', str(macro.get('isActionBlock')))
        ok(f'{cid}: m_name', display) if macro.get('m_name')==display else fail(f'{cid}: m_name', str(macro.get('m_name')))
        ok(f'{cid}: no globals', 'OK') if ab.get('globalVariables') in ([], None) else fail(f'{cid}: no globals', str(ab.get('globalVariables')))
        locals_=macro.get('localVariables',[])
        outputs=[v.get('m_name') for v in locals_ if v.get('supportsOutput')]
        ok(f'{cid}: public output', 'Resultado') if outputs==['Resultado'] else fail(f'{cid}: public output', str(outputs))
        leaked=[v.get('m_name') for v in locals_ if v.get('m_name','').startswith('Tmp_') and v.get('supportsOutput')]
        ok(f'{cid}: no Tmp output', 'OK') if not leaked else fail(f'{cid}: no Tmp output', str(leaked))
        actions=macro.get('m_actionList',[]); counter=Counter(a.get('m_classType','') for a in actions)
        stats[cid]={'actions':len(actions),'classes':len(counter),'js':counter.get('JavaScriptAction',0),'shell':counter.get('ShellScriptAction',0),'fileop_v21':counter.get('FileOperationV21Action',0),'textmanip':counter.get('TextManipulationAction',0),'actionblock':counter.get('ActionBlockAction',0)}
        ok(f'{cid}: action stats', str(stats[cid]))
    except Exception as exc: fail(f'{cid}: ablock', str(exc))

for script in sorted((ROOT/'capabilities').glob('*/scripts/*.py')):
    completed=subprocess.run([sys.executable, str(script)], cwd=str(ROOT), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed.returncode==0: ok(f'script {script.relative_to(ROOT)}', completed.stdout.strip())
    else: fail(f'script {script.relative_to(ROOT)}', completed.stdout.strip())

print(f'PASS={sum(1 for r in results if r[0]=="PASS")} WARN={len(warnings)} FAIL={len(failures)}')
for st,name,details in results:
    if st!='PASS': print(st, name, details)
if failures:
    sys.exit(1)
