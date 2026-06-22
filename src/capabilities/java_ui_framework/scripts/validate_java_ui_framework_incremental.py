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
catalog = load(CAP / "component_catalog.json")
export = load(CAP / "macrodroid" / "[CDXMS]_Java_UI_Framework.ablock")
macro = export["macro"]

require(export.get("macroExportVersion") == 1, "macroExportVersion divergente")
require(macro.get("isActionBlock") is True, "export deve ser Action Block")
require(macro.get("m_name") == "[CDXMS] Java UI Framework", "nome divergente")
require(macro.get("m_triggerList") == [], "Action Block não deve possuir triggers")

variables = {v["m_name"]: v for v in macro.get("localVariables", [])}
expected_variables = {
    "JUIF UI Json",
    "Tmp_JuifVisible",
    "Tmp_JuifClicked",
    "Tmp_JuifAction",
    "Tmp_JuifPayload",
    "Tmp_JuifState",
    "Tmp_JuifCurrentPage",
    "Tmp_ResultJson",
    "Tmp_JuifUiJsonEscaped",
    "Tmp_DefaultUiJson",
    "Resultado",
}
require(expected_variables == set(variables), "variáveis públicas/internas divergentes")
require(variables["JUIF UI Json"].get("supportsInput") is True, "entrada pública ausente")
require(variables["Resultado"].get("supportsOutput") is True, "Resultado deve ser output")
require(sum(1 for v in variables.values() if v.get("supportsInput")) == 1, "deve existir uma única entrada pública")
require(sum(1 for v in variables.values() if v.get("supportsOutput")) == 1, "deve existir uma única saída pública")
for name, variable in variables.items():
    require(str(variable.get("description", "")).strip(), f"variável sem descrição: {name}")
    if name not in {"JUIF UI Json", "Resultado"}:
        require(variable.get("isActionBlockWorkingVar") is True, f"variável interna não marcada como working: {name}")
        require(not variable.get("supportsInput") and not variable.get("supportsOutput"), f"working variable exposta: {name}")

expected_actions = [
    "ActionGroupAction",
    "TextManipulationAction",
    "TextManipulationAction",
    "TextManipulationAction",
    "ActionGroupEndAction",
    "ActionGroupAction",
    "JavaAction",
    "JsonParseAction",
    "ActionGroupEndAction",
    "ExitActionBlockAction",
]
actions = macro.get("m_actionList", [])
require([a.get("m_classType") for a in actions] == expected_actions, "sequência de ações divergente")
require(actions[6].get("blockNextAction") is True, "Java Action deve bloquear a continuação")
require(actions[6].get("runInBackgroundThread") is False, "renderer não pode manipular views em background")
require(actions[6].get("responseVariableName") == "Tmp_ResultJson", "response variable do Java Action divergente")
require(actions[7].get("stringVarName") == "Tmp_ResultJson", "JSON Parse deve consumir Tmp_ResultJson")
require(actions[7].get("dictionaryVarName") == "Resultado", "JSON Parse deve publicar Resultado")

script = actions[6]["scriptText"]
new_renderers = [
    "JUIFTopAppBar",
    "JUIFBottomNavigation",
    "JUIFNavigationRail",
    "JUIFNavigationDrawer",
    "JUIFTabBar",
    "JUIFSearchBar",
    "JUIFChip",
    "JUIFChipGroup",
    "JUIFEmptyState",
    "JUIFLoadingIndicator",
]
for token in new_renderers:
    require(token in script, "renderer ausente: " + token)
require('result.put("artifact_id", "java_ui_framework")' in script, "artifact id do Resultado divergente")
require('"artifact_id":\\"mdf\\"' not in script and '"artifact_id":"mdf"' not in script, "fallback legado mdf ainda presente")
require('data.put("supported_component_count", 36)' in script, "contagem publicada pelo renderer divergente")
for forbidden in ["data_json", "error_code", "error_message", "error_json"]:
    require(forbidden not in script, "campo proibido no Resultado do renderer: " + forbidden)
require('result.put("meta", meta)' in script, "renderer deve publicar meta")
require('result.put("error", error == null ? JSONObject.NULL : error)' in script, "renderer deve publicar error estruturado")
require('"PERMISSION_DENIED"' in script and "Settings.canDrawOverlays" in script, "renderer deve validar permissão de overlay")
require('catch(JSONException e)' in script, "renderer deve classificar JSON inválido")
require("juifRootContainer" not in script and "juifBodyContainer" not in script, "renderer não deve reescrever a hierarquia-base do protótipo nesta fase")

require(variables["Resultado"].get("dictionary", {}).get("entries", []) == [], "Resultado deve iniciar vazio para JSON Parse substituir integralmente o conteúdo")

catalog_types = [item["type"] for item in catalog.get("components", [])]
config_types = config.get("settings", {}).get("supported_component_types", [])
require(catalog.get("component_count") == 36, "catálogo deve conter 36 componentes")
require(len(catalog_types) == 36 and len(set(catalog_types)) == 36, "lista do catálogo divergente ou duplicada")
require(config_types == catalog_types, "config e catálogo devem usar a mesma ordem/tipos")
require(manifest["component_catalog"]["supported_component_count"] == 36, "manifest com contagem divergente")
require(manifest["component_catalog"]["existing_components_preserved"] == 26, "regressão de componentes legados")
require(contract.get("artifact_id") == "java_ui_framework", "artifact id do contrato divergente")
require(contract.get("outputs") == [{"name": "Resultado", "type": "dictionary", "description": "Saída pública única no contrato universal CDXMS."}], "saída contratual divergente")

print("OK: Java UI Framework incremental validado")
