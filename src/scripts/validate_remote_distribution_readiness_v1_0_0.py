#!/usr/bin/env python3
import json, hashlib, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
WARNINGS = []
CAPABILITIES = [
    'json_config_manager', 'bootstrap', 'result_manager', 'logger',
    'string_utils', 'artifact_manager', 'dependency_resolver', 'remote_source_manager',
]

def error(message):
    ERRORS.append(message)

def load(relative):
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        error(f'{relative}: JSON inválido: {exc}')
        return {}

# Complete merged baseline, not a delta.
required_root = [
    '.cdxms_root.json', 'README.md', 'CHANGELOG.md', 'release.json',
    'checksums.json', 'core/manifest.json', 'core/registry.default.json',
    'core/settings.default.json', 'core/enums.json', 'core/errors.json',
    'core/result_contract.json', 'core/compatibility.json',
    'core/remote_manifest.json', 'catalogs/sources.json',
    'catalogs/local_catalog.default.json',
]
for relative in required_root:
    if not (ROOT / relative).is_file():
        error(f'Arquivo obrigatório ausente: {relative}')

for capability in CAPABILITIES:
    base = Path('capabilities') / capability
    required = [
        'manifest.json', 'contract.json', 'config.default.json',
        'remote_manifest.json', 'README.md', 'body.md', 'tests/manual_test.md',
    ]
    for name in required:
        if not (ROOT / base / name).is_file():
            error(f'Arquivo obrigatório ausente: {base / name}')
    exports = list((ROOT / base / 'macrodroid').glob('*.ablock'))
    if len(exports) != 1:
        error(f'{capability}: esperado exatamente 1 export .ablock, encontrado {len(exports)}')

# Minimal source/catalog design: one source; no premature channel matrix.
if (ROOT / 'channels').exists():
    error('A pasta channels/ não deve existir nesta fase mínima.')
extra_catalogs = [p.name for p in (ROOT / 'catalogs').glob('*.catalog.json')]
if extra_catalogs:
    error(f'Catálogos paralelos não permitidos nesta fase: {extra_catalogs}')

sources = load('catalogs/sources.json')
source_items = sources.get('sources', [])
if len(source_items) != 1:
    error('Deve existir exatamente uma fonte remota oficial nesta fase.')
else:
    source = source_items[0]
    expected = {
        'id': 'cdxms_official_github',
        'type': 'github_raw',
        'ref': 'develop',
        'catalog_path': 'catalogs/local_catalog.default.json',
    }
    for key, value in expected.items():
        if source.get(key) != value:
            error(f'sources.json: {key} deve ser {value!r}.')
    base_url = source.get('base_raw_url', '')
    if '/blob/' in base_url:
        error('sources.json: URL /blob/ não pode ser usada para download.')
    if not base_url.startswith('https://raw.githubusercontent.com/'):
        error('sources.json: base_raw_url deve usar raw.githubusercontent.com.')

catalog = load('catalogs/local_catalog.default.json')
if catalog.get('file_type') != 'local_catalog':
    error('local_catalog.default.json: file_type inválido.')
listed = {item.get('artifact_id') for item in catalog.get('capabilities', [])}
if listed != set(CAPABILITIES):
    error(f'Catálogo de capabilities divergente: {sorted(listed)}')

# Core settings stay minimal and use develop only for homologation.
settings = load('core/settings.default.json').get('settings', {})
if settings.get('default_remote_ref') != 'develop':
    error('core/settings.default.json: default_remote_ref deve ser develop nesta homologação.')
if settings.get('allow_dev_branch_install') is not True:
    error('core/settings.default.json: allow_dev_branch_install deve ser true nesta homologação.')
for premature in ['connect_timeout_seconds', 'read_timeout_seconds', 'max_redirects', 'catalog_ttl_seconds']:
    if premature in settings:
        error(f'Configuração HTTP prematura no core: {premature}')

# Remote manifests preserve schema v1 fields and checksum every source file.
remote_paths = ['core/remote_manifest.json'] + [f'capabilities/{c}/remote_manifest.json' for c in CAPABILITIES]
for relative in remote_paths:
    manifest = load(relative)
    if manifest.get('schema_version') != 1:
        error(f'{relative}: schema_version deve permanecer 1.')
    source = manifest.get('source', {})
    for key in ['type', 'repository', 'ref', 'base_raw_url']:
        if not source.get(key):
            error(f'{relative}: source.{key} ausente.')
    if source.get('type') != 'github_raw':
        error(f'{relative}: source.type deve ser github_raw.')
    if source.get('ref') != 'develop':
        error(f'{relative}: source.ref deve ser develop na homologação.')
    if '/blob/' in source.get('base_raw_url', ''):
        error(f'{relative}: URL /blob/ proibida.')
    for index, item in enumerate(manifest.get('files', [])):
        for key in ['path', 'target_path', 'write_policy', 'file_role', 'checksum_sha256']:
            if key not in item:
                error(f'{relative}: files[{index}].{key} ausente.')
        source_file = ROOT / item.get('path', '')
        if not source_file.is_file():
            error(f'{relative}: source file ausente: {item.get("path")}')
        elif item.get('checksum_sha256') != hashlib.sha256(source_file.read_bytes()).hexdigest():
            error(f'{relative}: checksum divergente para {item.get("path")}')

# Release remains backward compatible: path is preserved and remote_manifest_path is additive.
release = load('release.json')
for artifact in release.get('artifacts', []):
    if not artifact.get('path'):
        error(f'release.json: path ausente para {artifact.get("artifact_id")}')
    if not artifact.get('remote_manifest_path'):
        error(f'release.json: remote_manifest_path ausente para {artifact.get("artifact_id")}')

# MacroDroid exports: contract matches inputs, one output, GUID calls are consistent.
exports_by_name = {}
parsed_exports = []
for capability in CAPABILITIES:
    export_path = next((ROOT / 'capabilities' / capability / 'macrodroid').glob('*.ablock'))
    export = load(export_path.relative_to(ROOT).as_posix())
    macro = export.get('macro', {})
    parsed_exports.append((capability, export_path, macro))
    exports_by_name[macro.get('m_name')] = macro.get('m_GUID')
    if export.get('macroExportVersion') != 1:
        error(f'{export_path}: macroExportVersion inválido.')
    if macro.get('isActionBlock') is not True:
        error(f'{export_path}: export não é Action Block.')
    if macro.get('breakpoints') not in ([], None):
        error(f'{export_path}: breakpoints ativos.')
    outputs = [v.get('m_name') for v in macro.get('localVariables', []) if v.get('supportsOutput')]
    if outputs != ['Resultado']:
        error(f'{export_path}: saída pública inválida: {outputs}')
    contract = load(f'capabilities/{capability}/contract.json')
    contract_inputs = [i.get('name') for i in contract.get('inputs', [])]
    export_inputs = [v.get('m_name') for v in macro.get('localVariables', []) if v.get('supportsInput')]
    if contract_inputs != export_inputs:
        error(f'{capability}: inputs do contract/export divergentes.')

for capability, export_path, macro in parsed_exports:
    for action in macro.get('m_actionList', []):
        if action.get('m_classType') == 'ActionBlockAction':
            name = action.get('actionBlockName')
            if name in exports_by_name and action.get('actionBlockId') != exports_by_name[name]:
                error(f'{capability}: GUID divergente ao chamar {name}.')

am_macro = next(m for c, _, m in parsed_exports if c == 'artifact_manager')
if any(a.get('m_classType') == 'ShellScriptAction' for a in am_macro.get('m_actionList', [])):
    error('Artifact Manager não pode usar ShellScriptAction como executor normal.')
am_text = json.dumps(am_macro, ensure_ascii=False)
for marker in ['json_config_manager', 'jcm_apply_plan', 'jcm_verification_plan']:
    if marker not in am_text:
        error(f'Artifact Manager: marcador obrigatório ausente: {marker}')

dr_manifest = load('capabilities/dependency_resolver/manifest.json')
if dr_manifest.get('purity') != 'pure' or dr_manifest.get('side_effects') not in ([], None):
    error('Dependency Resolver deve permanecer puro/stateless.')

# Full checksums over the complete src tree; checksums.json excludes itself to avoid recursion.
checksums = load('checksums.json')
expected_files = {
    p.relative_to(ROOT).as_posix()
    for p in ROOT.rglob('*')
    if p.is_file() and p.relative_to(ROOT).as_posix() != 'checksums.json'
}
actual_files = set(checksums.get('files', {}))
if actual_files != expected_files:
    missing = sorted(expected_files - actual_files)
    extra = sorted(actual_files - expected_files)
    error(f'checksums.json não cobre a árvore completa. missing={missing}, extra={extra}')
for relative, expected in checksums.get('files', {}).items():
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    if actual != expected:
        error(f'checksum divergente: {relative}')


# JCM must not expose localized booleans through dictionary Magic Text.
jcm_export = load(ROOT / 'capabilities/json_config_manager/macrodroid/[CDXMS]_Json_Config_Manager.ablock')
jcm_init = next((a.get('scriptText','') for a in jcm_export.get('macro',{}).get('m_actionList',[]) if a.get('m_classType') == 'JavaScriptAction'), '')
for fragment in ['valid_file_path: safePath(filePath, true) ? "true" : "false"', 'valid_folder_path: safePath(folderPath, false) ? "true" : "false"']:
    if fragment not in jcm_init: error('JCM sem serialização locale-safe: ' + fragment)

if ERRORS:
    print('VALIDATION FAILED — CDXMS remote distribution readiness v1.0.0')
    for item in ERRORS:
        print('-', item)
    raise SystemExit(1)

print('VALIDATION OK — CDXMS remote distribution readiness v1.0.0')
print(f'files={len(expected_files)+1} capabilities={len(CAPABILITIES)} remote_manifests={len(remote_paths)} sources=1 catalogs=1')
print('overengineering_checks=PASS schema_compatibility_checks=PASS full_merged_package_checks=PASS')
