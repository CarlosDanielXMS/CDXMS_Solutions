from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

CAP = Path(__file__).resolve().parents[1]
STRING_UTILS = CAP.parent / "string_utils"


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


def escape_json_string(value: str) -> str:
    """Equivalent to JSON.stringify(value).slice(1, -1) used by String Utils."""
    return json.dumps(str(value), ensure_ascii=False)[1:-1]


def run_node(script: str) -> str:
    node = shutil.which("node")
    require(node is not None, "Node.js é necessário para validar o motor JavaScript")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "runtime.js"
        path.write_text(script + "\nconsole.log(__cdxms_result);\n", encoding="utf-8")
        process = subprocess.run(
            [node, str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
    return process.stdout.strip().splitlines()[-1]


manifest = load(CAP / "manifest.json")
contract = load(CAP / "contract.json")
config = load(CAP / "config.default.json")
export = load(CAP / "macrodroid" / "[CDXMS]_JUIF_UI_Builder.ablock")
string_manifest = load(STRING_UTILS / "manifest.json")
string_contract = load(STRING_UTILS / "contract.json")
string_export = load(STRING_UTILS / "macrodroid" / "[CDXMS]_String_Utils.ablock")

macro = export["macro"]
string_macro = string_export["macro"]

require(export.get("macroExportVersion") == 1, "macroExportVersion divergente")
require(macro.get("isActionBlock") is True, "export deve ser Action Block")
require(macro.get("m_name") == "[CDXMS] JUIF UI Builder", "nome divergente")
require(macro.get("m_triggerList") == [], "Action Block não deve possuir triggers")
require(manifest["capability"]["version"] == "1.0.0", "versão do Builder não deve ser incrementada")
require(contract["version"] == "1.0.0", "versão do contrato não deve ser incrementada")
require(string_manifest["capability"]["version"] == "1.0.0", "String Utils deve permanecer em 1.0.0")
require(
    "escape_json_string" in string_contract["operations"],
    "String Utils não expõe escape_json_string",
)
require(
    manifest["requires"]["capabilities"].get("string_utils") == ">=1.0.0",
    "manifest deve declarar dependência direta de string_utils",
)

variables = {variable["m_name"]: variable for variable in macro.get("localVariables", [])}
expected_variables = {
    "Config Json",
    "UI Schema Json",
    "Escape Json",
    "Resultado",
    "Tmp_ConfigEscapeResult",
    "Tmp_SchemaEscapeResult",
    "Tmp_CoreResultJson",
    "Tmp_CoreResult",
    "Tmp_CoreResultJsonEscape",
    "Tmp_UiEscapeResult",
    "Tmp_ResultJson",
}
require(set(variables) == expected_variables, "variáveis esperadas divergentes")
require(sum(1 for variable in variables.values() if variable.get("supportsInput")) == 3, "devem existir três entradas públicas")
require(sum(1 for variable in variables.values() if variable.get("supportsOutput")) == 1, "deve existir uma única saída pública")
require(variables["Resultado"].get("supportsOutput") is True, "Resultado deve ser output")
for name in expected_variables - {"Config Json", "UI Schema Json", "Escape Json", "Resultado"}:
    require(variables[name].get("isActionBlockWorkingVar") is True, f"{name} deve ser working")
for name, variable in variables.items():
    require(str(variable.get("description", "")).strip(), f"variável sem descrição: {name}")

expected_actions = [
    "ActionGroupAction",
    "ActionBlockAction",
    "ActionBlockAction",
    "JavaScriptAction",
    "JsonParseAction",
    "ActionBlockAction",
    "ActionBlockAction",
    "JavaScriptAction",
    "JsonParseAction",
    "ActionGroupEndAction",
    "ExitActionBlockAction",
]
actions = macro.get("m_actionList", [])
require([action.get("m_classType") for action in actions] == expected_actions, "sequência de ações divergente")
require(manifest["implementation_audit"]["action_profile"]["total_actions"] == len(actions), "action_profile divergente")

string_calls = {
    1: ("{lv=Config Json}", "Tmp_ConfigEscapeResult"),
    2: ("{lv=UI Schema Json}", "Tmp_SchemaEscapeResult"),
    5: ("{lv=Tmp_CoreResultJson}", "Tmp_CoreResultJsonEscape"),
    6: ("{lv=Tmp_CoreResult[data][juif_ui_json]}", "Tmp_UiEscapeResult"),
}
for index, (text_value, output_variable) in string_calls.items():
    action = actions[index]
    require(action.get("actionBlockName") == "[CDXMS] String Utils", f"ação {index + 1} não chama String Utils")
    require(action.get("actionBlockId") == string_macro["m_GUID"], f"GUID da String Utils divergente na ação {index + 1}")
    require(action.get("continueActionsWithoutWaiting") is False, f"ação {index + 1} deve aguardar")
    require(action.get("inputVarsMap", {}).get("Operation") == "escape_json_string", f"operação divergente na ação {index + 1}")
    require(action.get("inputVarsMap", {}).get("Text") == text_value, f"Text divergente na ação {index + 1}")
    require(action.get("outputVarsMap", {}).get("Resultado") == output_variable, f"output divergente na ação {index + 1}")

core_action = actions[3]
core_parse = actions[4]
final_action = actions[7]
final_parse = actions[8]

require(core_action.get("javascriptEngine") == "JetPack JavascriptEngine", "engine do motor principal divergente")
require(core_action.get("blockNextAction") is True, "motor principal deve bloquear continuação")
require(core_action.get("stringVariableName") == "Tmp_CoreResultJson", "saída do motor principal divergente")
require(core_parse.get("stringVarName") == "Tmp_CoreResultJson", "parse intermediário deve consumir Tmp_CoreResultJson")
require(core_parse.get("dictionaryVarName") == "Tmp_CoreResult", "parse intermediário deve publicar Tmp_CoreResult")
require(final_action.get("javascriptEngine") == "JetPack JavascriptEngine", "engine da finalização divergente")
require(final_action.get("blockNextAction") is True, "finalização deve bloquear continuação")
require(final_action.get("stringVariableName") == "Tmp_ResultJson", "saída da finalização divergente")
require(final_parse.get("stringVarName") == "Tmp_ResultJson", "parse final deve consumir Tmp_ResultJson")
require(final_parse.get("dictionaryVarName") == "Resultado", "parse final deve publicar Resultado")

core_script = core_action["scriptText"]
final_script = final_action["scriptText"]
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
    require(token + ": true" in core_script, "componente ausente no enum: " + token)

for forbidden in [
    "{lv=Config Json}",
    "{lv=UI Schema Json}",
    "function mdBlock",
    "function escapeForMacroDroid",
]:
    require(forbidden not in core_script, "fronteira JSON insegura no motor principal: " + forbidden)

for required in [
    "{lv=Tmp_ConfigEscapeResult[data][value]}",
    "{lv=Tmp_SchemaEscapeResult[data][value]}",
]:
    require(required in core_script, "entrada protegida ausente: " + required)

for required in [
    "{lv=Tmp_CoreResultJsonEscape[data][value]}",
    "{lv=Tmp_UiEscapeResult[data][value]}",
    "{lv=Escape Json}",
]:
    require(required in final_script, "entrada da finalização ausente: " + required)

for script in [core_script, final_script]:
    for forbidden in ["data_json", "error_code", "error_message", "error_json"]:
        require(forbidden not in script, "campo proibido no Resultado: " + forbidden)

default_config_text = variables["Config Json"]["m_stringValue"]
default_schema_text = variables["UI Schema Json"]["m_stringValue"]
default_config = json.loads(default_config_text)
default_schema = json.loads(default_schema_text)
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
require("catalog_tabs_" not in default_schema_text, "chaves antigas de catálogo presentes")

config_types = config["settings"]["supported_component_types"]
require(len(config_types) == 36 and len(set(config_types)) == 36, "config deve conter 36 tipos")
require(config["settings"]["shell_mode"] == "persistent_hosts", "config do Builder não declara shell persistente")
require(manifest["implementation_audit"]["default_ui_pages"] == 7, "auditoria da UI padrão divergente")
require(contract["schema_contract"]["shell_behavior"]["renderer_mode"] == "persistent_hosts", "contrato de shell divergente")

node = shutil.which("node")
if node:
    core_runtime = (
        core_script.replace(
            "{lv=Tmp_ConfigEscapeResult[data][value]}",
            escape_json_string(default_config_text),
        )
        .replace(
            "{lv=Tmp_SchemaEscapeResult[data][value]}",
            escape_json_string(default_schema_text),
        )
    )
    core_result_json = run_node(core_runtime)
    core_result = json.loads(core_result_json)

    require(core_result["success"] is True, "Builder padrão falhou")
    require(core_result["data"]["supported_component_count"] == 36, "Builder publicou contagem divergente")
    require(len(json.loads(core_result["data"]["mapping_json"])) == 21, "mapping padrão deve possuir 21 bindings")

    raw_ui_json = core_result["data"]["juif_ui_json"]
    escaped_ui_json = escape_json_string(raw_ui_json)
    def finalize(escape_value: str):
        runtime = (
            final_script.replace(
                "{lv=Tmp_CoreResultJsonEscape[data][value]}",
                escape_json_string(core_result_json),
            )
            .replace(
                "{lv=Tmp_UiEscapeResult[data][value]}",
                escaped_ui_json,
            )
            .replace("{lv=Escape Json}", escape_value)
        )
        return json.loads(run_node(runtime))

    escaped_result = finalize("true")
    raw_result = finalize("false")

    require(escaped_result["data"]["juif_ui_json"] == raw_ui_json, "JSON cru foi alterado")
    require(
        escaped_result["data"]["juif_ui_json_escaped"] == escaped_ui_json,
        "JSON escapado divergente da String Utils",
    )
    require(
        raw_result["data"]["juif_ui_json_escaped"] == raw_ui_json,
        "Escape Json=false não preservou JSON cru",
    )

    ui = json.loads(raw_ui_json)
    found: set[str] = set()
    collect_types(ui, found)
    require(found == set(config_types), f"Builder não gerou todos os tipos: {set(config_types) - found}")
    require(set(ui["pages"]) == expected_pages, "Builder gerou páginas divergentes")
    require(ui["shell"]["tab_bar"]["type"] == "tab_bar", "Tab Bar não normalizada")
    require(ui["shell"]["navigation_drawer"]["type"] == "navigation_drawer", "Drawer não normalizado")

    bridge_schema = dict(default_schema)
    bridge_schema["event_bridge"] = {
        "enabled": True,
        "intent_action": "com.cdxms.solutions.EVENT",
        "session_id": "builder-validator",
        "source_artifact_id": "validator",
    }
    bridge_runtime = (
        core_script.replace(
            "{lv=Tmp_ConfigEscapeResult[data][value]}",
            escape_json_string(default_config_text),
        )
        .replace(
            "{lv=Tmp_SchemaEscapeResult[data][value]}",
            escape_json_string(json.dumps(bridge_schema, ensure_ascii=False)),
        )
    )
    bridge_result = json.loads(run_node(bridge_runtime))
    bridge_ui = json.loads(bridge_result["data"]["juif_ui_json"])
    require(bridge_ui["event_bridge"]["session_id"] == "builder-validator", "event_bridge não foi preservado")

    invalid_runtime = (
        core_script.replace(
            "{lv=Tmp_ConfigEscapeResult[data][value]}",
            escape_json_string('{"invalid":'),
        )
        .replace(
            "{lv=Tmp_SchemaEscapeResult[data][value]}",
            escape_json_string(default_schema_text),
        )
    )
    invalid_result = json.loads(run_node(invalid_runtime))
    require(invalid_result["success"] is False, "JSON inválido deveria falhar")
    require(invalid_result["error"]["code"] == "INVALID_JSON", "código de JSON inválido divergente")

print("OK: JUIF UI Builder com fronteira JSON via String Utils validado")
