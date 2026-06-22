from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

CAP = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def collect_types(node, found: set[str]) -> None:
    if isinstance(node, dict):
        value = node.get("type")
        if isinstance(value, str):
            found.add(value)
        for child in node.values():
            collect_types(child, found)
    elif isinstance(node, list):
        for child in node:
            collect_types(child, found)


manifest = load(CAP / "manifest.json")
contract = load(CAP / "contract.json")
config = load(CAP / "config.default.json")
export = load(CAP / "macrodroid" / "[CDXMS]_JUIF_UI_Builder.ablock")
macro = export["macro"]

require(export.get("macroExportVersion") == 1, "macroExportVersion divergente")
require(macro.get("isActionBlock") is True, "export deve ser Action Block")
require(macro.get("m_name") == "[CDXMS] JUIF UI Builder", "nome divergente")
require(macro.get("m_triggerList") == [], "Action Block não deve possuir triggers")

variables = {v["m_name"]: v for v in macro.get("localVariables", [])}
expected_variables = {"Config Json", "UI Schema Json", "Escape Json", "Resultado", "Tmp_ResultJson"}
require(set(variables) == expected_variables, "variáveis esperadas divergentes")
require(sum(1 for v in variables.values() if v.get("supportsInput")) == 3, "devem existir três entradas públicas")
require(sum(1 for v in variables.values() if v.get("supportsOutput")) == 1, "deve existir uma única saída pública")
require(variables["Resultado"].get("supportsOutput") is True, "Resultado deve ser output")
require(variables["Tmp_ResultJson"].get("isActionBlockWorkingVar") is True, "Tmp_ResultJson deve ser working")
for name, variable in variables.items():
    require(str(variable.get("description", "")).strip(), f"variável sem descrição: {name}")

expected_actions = [
    "ActionGroupAction",
    "JavaScriptAction",
    "JsonParseAction",
    "ActionGroupEndAction",
    "ExitActionBlockAction",
]
actions = macro.get("m_actionList", [])
require([a.get("m_classType") for a in actions] == expected_actions, "sequência de ações divergente")
require(actions[1].get("javascriptEngine") == "JetPack JavascriptEngine", "engine divergente")
require(actions[1].get("blockNextAction") is True, "JavaScript deve bloquear continuação")
require(actions[2].get("stringVarName") == "Tmp_ResultJson", "JSON Parse deve consumir Tmp_ResultJson")
require(actions[2].get("dictionaryVarName") == "Resultado", "JSON Parse deve publicar Resultado")

script = actions[1]["scriptText"]
for token in [
    "top_app_bar",
    "bottom_navigation",
    "navigation_rail",
    "navigation_drawer",
    "tab_bar",
    "search_bar",
    "chip",
    "chip_group",
    "empty_state",
    "loading_indicator",
]:
    require(token + ": true" in script, "componente ausente no enum: " + token)
for marker in ["{lv=Config Json}", "{lv=UI Schema Json}", "{lv=Escape Json}"]:
    require(marker in script, "Magic Text ausente: " + marker)
for forbidden in ["data_json", "error_code", "error_message", "error_json"]:
    require(forbidden not in script, "campo proibido no Resultado: " + forbidden)

default_config = json.loads(variables["Config Json"]["m_stringValue"])
default_schema = json.loads(variables["UI Schema Json"]["m_stringValue"])
expected_pages = {
    "overview",
    "catalog_layout",
    "catalog_forms",
    "catalog_data",
    "catalog_feedback",
    "catalog_navigation",
    "playground",
}
require(default_schema.get("initial_page") == "overview", "initial_page divergente")
require({page.get("id") for page in default_schema.get("pages", [])} == expected_pages, "páginas divergentes")
require(default_schema["shell"]["tab_bar"]["key"] == "catalog_section", "estado de tabs fragmentado")
require(set(default_schema["shell"]["tab_bar"]["visible_pages"]) == expected_pages - {"overview", "playground"}, "visible_pages divergente")
require(len(default_schema["shell"]["tab_bar"]["items"]) == 5, "catálogo deve possuir cinco tabs")
require(len(default_schema["shell"]["bottom_navigation"]["items"]) == 3, "navegação principal divergente")
require("navigation_drawer" in default_schema["shell"], "drawer padrão ausente")
require(default_config["metrics"]["components"] == 36, "Config padrão deve documentar 36 componentes")
require("catalog_tabs_" not in variables["UI Schema Json"]["m_stringValue"], "chaves antigas de catálogo presentes")

config_types = config["settings"]["supported_component_types"]
require(len(config_types) == 36 and len(set(config_types)) == 36, "config deve conter 36 tipos")
require(config["settings"]["shell_mode"] == "persistent_hosts", "config do Builder não declara shell persistente")
require(manifest["implementation_audit"]["default_ui_pages"] == 7, "auditoria da UI padrão divergente")
require(contract["schema_contract"]["shell_behavior"]["renderer_mode"] == "persistent_hosts", "contrato de shell divergente")

node = shutil.which("node")
if node:
    config_text = variables["Config Json"]["m_stringValue"]
    schema_text = variables["UI Schema Json"]["m_stringValue"]
    runtime = (
        script.replace("{lv=Config Json}", config_text)
        .replace("{lv=UI Schema Json}", schema_text)
        .replace("{lv=Escape Json}", "true")
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "builder.js"
        path.write_text(runtime + "\nconsole.log(__cdxms_result);\n", encoding="utf-8")
        process = subprocess.run([node, str(path)], check=True, capture_output=True, text=True)
        result = json.loads(process.stdout.strip().splitlines()[-1])

    require(result["success"] is True, "Builder padrão falhou")
    require(result["data"]["supported_component_count"] == 36, "Builder publicou contagem divergente")
    require(len(json.loads(result["data"]["mapping_json"])) == 21, "mapping padrão deve possuir 21 bindings")
    ui = json.loads(result["data"]["juif_ui_json"])
    found: set[str] = set()
    collect_types(ui, found)
    require(found == set(config_types), f"Builder não gerou todos os tipos: {set(config_types) - found}")
    require(set(ui["pages"]) == expected_pages, "Builder gerou páginas divergentes")
    require(ui["shell"]["tab_bar"]["type"] == "tab_bar", "Tab Bar não normalizada")
    require(ui["shell"]["navigation_drawer"]["type"] == "navigation_drawer", "Drawer não normalizado")

print("OK: JUIF UI Builder profissional validado")
