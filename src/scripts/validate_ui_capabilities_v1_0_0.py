from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".ablock", ".json", ".macro", ".md", ".py", ".js"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha256(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitkeep":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


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
assert renderer_config["settings"]["navigation_dispatch"] == "posted_main_loop"
assert renderer_config["settings"]["transactional_page_rendering"] is True
assert renderer_config["settings"]["transactional_shell_rendering"] is True

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
builder_scripts = [
    action["scriptText"]
    for action in builder_export["macro"]["m_actionList"]
    if action.get("m_classType") == "JavaScriptAction"
]
assert len(builder_scripts) == 2
core_script, final_script = builder_scripts
node = shutil.which("node")
if node:
    def escape_json_string(value: str) -> str:
        return json.dumps(str(value), ensure_ascii=False)[1:-1]

    core_runtime = (
        core_script
        .replace(
            "{lv=Tmp_ConfigEscapeResult[data][value]}",
            escape_json_string(builder_vars["Config Json"]["m_stringValue"]),
        )
        .replace(
            "{lv=Tmp_SchemaEscapeResult[data][value]}",
            escape_json_string(builder_vars["UI Schema Json"]["m_stringValue"]),
        )
    )
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "builder_core.js"
        source.write_text(core_runtime + "\nconsole.log(__cdxms_result);\n", encoding="utf-8")
        process = subprocess.run([node, str(source)], check=True, capture_output=True, text=True)
        core_result_json = process.stdout.strip().splitlines()[-1]
        core_result = json.loads(core_result_json)

        raw_ui = core_result["data"]["juif_ui_json"]
        escaped_ui = escape_json_string(raw_ui)
        final_runtime = (
            final_script
            .replace(
                "{lv=Tmp_CoreResultJsonEscape[data][value]}",
                escape_json_string(core_result_json),
            )
            .replace("{lv=Tmp_UiEscapeResult[data][value]}", escaped_ui)
            .replace(
                "{lv=Tmp_UiDoubleEscapeResult[data][value]}",
                escape_json_string(escaped_ui),
            )
            .replace("{lv=Escape Json}", "true")
        )
        source = Path(tmp) / "builder_final.js"
        source.write_text(final_runtime + "\nconsole.log(__cdxms_result);\n", encoding="utf-8")
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
        actual = canonical_sha256(distributed)
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
    actual = canonical_sha256(path)
    assert checksums["files"][relative] == actual, f"checksum divergente: {relative}"

print("OK: redesign profissional e hotfix de navegação das capabilities de UI validados")
