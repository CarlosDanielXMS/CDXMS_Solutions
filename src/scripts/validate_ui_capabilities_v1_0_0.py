from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


for script in [
    ROOT / "capabilities/juif_ui_builder/scripts/validate_juif_ui_builder_incremental.py",
    ROOT / "capabilities/java_ui_framework/scripts/validate_java_ui_framework_incremental.py",
]:
    subprocess.run([sys.executable, str(script)], check=True)

# Todo JSON/export contido no overlay deve continuar estruturalmente válido.
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.suffix in {".json", ".ablock", ".macro"}:
        load(path)

release = load(ROOT / "release.json")
release_ids = {item["artifact_id"] for item in release["artifacts"]}
assert {"java_ui_framework", "juif_ui_builder"}.issubset(release_ids)
assert release["status"] == "pre_release"

catalog = load(ROOT / "catalogs/local_catalog.default.json")
capability_ids = {item["artifact_id"] for item in catalog["capabilities"]}
assert {"java_ui_framework", "juif_ui_builder"}.issubset(capability_ids)

renderer_catalog = load(ROOT / "capabilities/java_ui_framework/component_catalog.json")
renderer_config = load(ROOT / "capabilities/java_ui_framework/config.default.json")
builder_config = load(ROOT / "capabilities/juif_ui_builder/config.default.json")
canonical_types = [item["type"] for item in renderer_catalog["components"]]
assert renderer_catalog["component_count"] == 36
assert renderer_config["settings"]["supported_component_types"] == canonical_types
assert builder_config["settings"]["supported_component_types"] == canonical_types

# O package preserva o mapa completo remoto e sobrepõe hashes dos arquivos novos/modificados.
checksums = load(ROOT / "checksums.json")
assert checksums["scope"] == "complete_src_tree_except_checksums_json"
checksum_files = checksums["files"]
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT).as_posix()
    if relative == "checksums.json":
        continue
    assert relative in checksum_files, f"arquivo do overlay ausente em checksums.json: {relative}"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert checksum_files[relative] == actual, f"checksum divergente: {relative}"

print("OK: integração das capabilities de UI validada")

# Resultado universal: validar scripts e defaults contra o contrato do core.
core_contract_path = ROOT / "core/result_contract.json"
expected_forbidden = {"data_json", "error_code", "error_message", "error_json"}
expected_required = {
    "schema_version", "namespace", "success", "status", "artifact_type",
    "artifact_id", "operation", "message", "data", "error",
}
if core_contract_path.exists():
    result_contract = load(core_contract_path)["result_contract"]
    forbidden = set(result_contract.get("forbidden_top_level_fields", []))
    required = {name for name, spec in result_contract.get("fields", {}).items() if spec.get("required") is True}
    assert forbidden == expected_forbidden
    assert expected_required.issubset(required)
else:
    # O patch é distribuído sem duplicar o core inalterado. Após a extração na raiz
    # do projeto, o contrato real será usado automaticamente.
    forbidden = expected_forbidden
for export_path in [
    ROOT / "capabilities/juif_ui_builder/macrodroid/[CDXMS]_JUIF_UI_Builder.ablock",
    ROOT / "capabilities/java_ui_framework/macrodroid/[CDXMS]_Java_UI_Framework.ablock",
]:
    export = load(export_path)
    result_var = next(v for v in export["macro"]["localVariables"] if v["m_name"] == "Resultado")
    default_keys = {e.get("key") for e in result_var.get("dictionary", {}).get("entries", [])}
    assert not (default_keys & forbidden), f"Resultado default contém campos proibidos em {export_path}"
    script_text = "\n".join(a.get("scriptText", "") for a in export["macro"]["m_actionList"] if a.get("scriptText"))
    for field in forbidden:
        assert field not in script_text, f"script contém campo proibido {field}: {export_path}"

print("OK: contrato universal de Resultado validado")

# Remote manifests devem apontar para os bytes efetivamente distribuídos.
for capability_id in ["java_ui_framework", "juif_ui_builder"]:
    remote_manifest_path = ROOT / f"capabilities/{capability_id}/remote_manifest.json"
    remote_manifest = load(remote_manifest_path)
    for item in remote_manifest.get("files", []):
        distributed_path = ROOT / item["path"]
        assert distributed_path.exists(), f"arquivo remoto ausente: {item['path']}"
        actual = hashlib.sha256(distributed_path.read_bytes()).hexdigest()
        assert item.get("checksum_sha256") == actual, f"checksum remoto divergente: {item['path']}"

print("OK: remote manifests das capabilities de UI validados")
