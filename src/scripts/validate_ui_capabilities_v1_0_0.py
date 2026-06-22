from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


for script in [
    ROOT / "capabilities/juif_ui_builder/scripts/validate_juif_ui_builder_incremental.py",
    ROOT / "capabilities/java_ui_framework/scripts/validate_java_ui_framework_incremental.py",
]:
    subprocess.run([sys.executable, str(script)], check=True)

# Todos os JSONs e exports do overlay devem permanecer válidos.
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
assert renderer_config["settings"]["shell_mode"] == "persistent_hosts"
assert builder_config["settings"]["shell_mode"] == "persistent_hosts"

# Resultado universal.
expected_forbidden = {"data_json", "error_code", "error_message", "error_json"}
core_contract_path = ROOT / "core/result_contract.json"
if core_contract_path.exists():
    result_contract = load(core_contract_path)["result_contract"]
    assert set(result_contract.get("forbidden_top_level_fields", [])) == expected_forbidden

for export_path in [
    ROOT / "capabilities/juif_ui_builder/macrodroid/[CDXMS]_JUIF_UI_Builder.ablock",
    ROOT / "capabilities/java_ui_framework/macrodroid/[CDXMS]_Java_UI_Framework.ablock",
]:
    export = load(export_path)
    result_var = next(v for v in export["macro"]["localVariables"] if v["m_name"] == "Resultado")
    assert result_var.get("dictionary", {}).get("entries", []) == []
    script_text = "\n".join(
        action.get("scriptText", "")
        for action in export["macro"]["m_actionList"]
        if action.get("scriptText")
    )
    for field in expected_forbidden:
        assert field not in script_text, f"campo proibido {field}: {export_path}"

# O Builder real deve gerar exatamente o default do Framework.
builder_export = load(ROOT / "capabilities/juif_ui_builder/macrodroid/[CDXMS]_JUIF_UI_Builder.ablock")
framework_export = load(ROOT / "capabilities/java_ui_framework/macrodroid/[CDXMS]_Java_UI_Framework.ablock")
builder_vars = {v["m_name"]: v for v in builder_export["macro"]["localVariables"]}
framework_vars = {v["m_name"]: v for v in framework_export["macro"]["localVariables"]}
builder_script = next(
    action["scriptText"]
    for action in builder_export["macro"]["m_actionList"]
    if action.get("m_classType") == "JavaScriptAction"
)
node = shutil.which("node")
if node:
    runtime = (
        builder_script
        .replace("{lv=Config Json}", builder_vars["Config Json"]["m_stringValue"])
        .replace("{lv=UI Schema Json}", builder_vars["UI Schema Json"]["m_stringValue"])
        .replace("{lv=Escape Json}", "true")
    )
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "builder.js"
        source.write_text(runtime + "\nconsole.log(__cdxms_result);\n", encoding="utf-8")
        process = subprocess.run([node, str(source)], check=True, capture_output=True, text=True)
        built_result = json.loads(process.stdout.strip().splitlines()[-1])

    assert built_result["success"] is True
    built_ui = json.loads(built_result["data"]["juif_ui_json"])
    framework_ui = json.loads(framework_vars["JUIF UI Json"]["m_stringValue"])
    assert built_ui == framework_ui, "default do Framework diverge do Builder"

    compact = json.dumps(framework_ui, ensure_ascii=False, separators=(",", ":"))
    escaped = (
        compact.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    assert framework_vars["Tmp_DefaultUiJson"]["m_stringValue"] == escaped
    assert len(json.loads(built_result["data"]["mapping_json"])) == 21

# Remote manifests.
for capability_id in ["java_ui_framework", "juif_ui_builder"]:
    remote_manifest = load(ROOT / f"capabilities/{capability_id}/remote_manifest.json")
    for item in remote_manifest.get("files", []):
        distributed = ROOT / item["path"]
        assert distributed.exists(), f"arquivo remoto ausente: {item['path']}"
        actual = hashlib.sha256(distributed.read_bytes()).hexdigest()
        assert item.get("checksum_sha256") == actual, f"checksum remoto divergente: {item['path']}"

# Mapa completo de checksums.
checksums = load(ROOT / "checksums.json")
assert checksums["scope"] == "complete_src_tree_except_checksums_json"
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT).as_posix()
    if relative == "checksums.json":
        continue
    if relative not in checksums["files"]:
        raise AssertionError(f"arquivo do overlay ausente em checksums.json: {relative}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert checksums["files"][relative] == actual, f"checksum divergente: {relative}"

print("OK: redesign profissional das capabilities de UI validado")
