from __future__ import annotations

import json
from pathlib import Path

CAP = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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
require(variables["Tmp_ResultJson"].get("isActionBlockWorkingVar") is True, "Tmp_ResultJson deve ser working variable")
require(not variables["Tmp_ResultJson"].get("supportsOutput"), "Tmp_ResultJson não pode ser output")
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
require(actions[1].get("javascriptEngine") == "JetPack JavascriptEngine", "engine JavaScript divergente")
require(actions[1].get("blockNextAction") is True, "JavaScript deve bloquear continuação")
require(actions[2].get("stringVarName") == "Tmp_ResultJson", "JSON Parse deve consumir Tmp_ResultJson")
require(actions[2].get("dictionaryVarName") == "Resultado", "JSON Parse deve publicar Resultado")

script = actions[1]["scriptText"]
all_new_types = [
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
]
for token in all_new_types:
    require(token + ": true" in script, "componente ausente no enum do builder: " + token)
for marker in ["{lv=Config Json}", "{lv=UI Schema Json}", "{lv=Escape Json}"]:
    require(marker in script, "Magic Text ausente: " + marker)
for alias in ["top_bar", "bottom_bar", "rail", "drawer", "tabs"]:
    require(alias in script, "alias de shell ausente: " + alias)
require('artifact_id: "juif_ui_builder"' in script, "artifact id do Resultado divergente")
for forbidden in ["data_json", "error_code", "error_message", "error_json"]:
    require(forbidden not in script, "campo proibido no Resultado do Builder: " + forbidden)
require('meta: {' in script, "Resultado do Builder deve publicar meta")
require('error: safeError' in script, "Resultado do Builder deve publicar error estruturado")

require("supported_component_count: Object.keys(SUPPORTED_COMPONENT_TYPES).length" in script, "contagem dinâmica ausente")
require("JUIF / Java UI Framework" in variables["UI Schema Json"].get("m_stringValue", ""), "schema default não foi adaptado")

config_types = config.get("settings", {}).get("supported_component_types", [])
require(len(config_types) == 36 and len(set(config_types)) == 36, "config deve conter 36 tipos únicos")
require(manifest["component_catalog"]["supported_component_count"] == 36, "contagem do catálogo divergente")
require(contract.get("artifact_id") == "juif_ui_builder", "artifact id do contrato divergente")
require(contract.get("outputs") == [{"name": "Resultado", "type": "dictionary", "description": "Saída pública única no contrato universal CDXMS."}], "saída contratual divergente")

print("OK: JUIF UI Builder incremental validado")
