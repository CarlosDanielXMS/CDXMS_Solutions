from __future__ import annotations

import hashlib
import json
import re
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


def collect_types(node, found: list[str]) -> None:
    if isinstance(node, dict):
        value = node.get("type")
        if isinstance(value, str):
            found.append(value)
        for child in node.values():
            collect_types(child, found)
    elif isinstance(node, list):
        for child in node:
            collect_types(child, found)


def navigation_targets(node, found: list[tuple[str, str]]) -> None:
    if isinstance(node, dict):
        if isinstance(node.get("target"), str) and node["target"]:
            found.append((str(node.get("id", node.get("label", "item"))), node["target"]))
        for child in node.values():
            navigation_targets(child, found)
    elif isinstance(node, list):
        for child in node:
            navigation_targets(child, found)


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
require(actions[6].get("responseVariableName") == "Tmp_ResultJson", "response variable divergente")
require(actions[7].get("stringVarName") == "Tmp_ResultJson", "JSON Parse deve consumir Tmp_ResultJson")
require(actions[7].get("dictionaryVarName") == "Resultado", "JSON Parse deve publicar Resultado")

script = actions[6]["scriptText"]
for token in [
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
]:
    require(token in script, "renderer ausente: " + token)

for token in [
    "juifRootContainer",
    "juifTopHost",
    "juifTabHost",
    "juifBodyContainer",
    "juifRailHost",
    "juifContentScroll",
    "juifBottomHost",
    "juifDrawerLayer",
    "juifRenderShell",
    "juifOpenDrawer",
    "juifCloseDrawer",
]:
    require(token in script, "host/runtime persistente ausente: " + token)

require('data.put("shell_mode", "persistent_hosts")' in script, "shell_mode não publicado")
require('"open_drawer".equals(safeAction)' in script, "open_drawer não tratado")
require('"close_drawer".equals(safeAction)' in script, "close_drawer não tratado")
require('"visible_pages"' in script and '"hidden_pages"' in script, "filtros de visibilidade ausentes")
require('"active_pages"' in script and '"active_prefix"' in script, "seleção agrupada ausente")
require("juifPageContainer.addView(JUIFTopAppBar" not in script, "Top App Bar voltou para dentro do conteúdo rolável")
require("juifPageContainer.addView(JUIFBottomNavigation" not in script, "Bottom Navigation voltou para dentro do conteúdo rolável")
require("juifRequestAction" in script and "dispatcher.post(new Runnable()" in script, "navegação não está adiada para a main loop")
require("juifDispatchActionNow" in script and "juifDispatchAction(" not in script, "dispatch síncrono legado ainda presente")
require("boolean juifRenderPage" in script and "LinearLayout staging" in script, "renderização transacional de página ausente")
require(script.index("nextTabs = JUIFTabBar") < script.index("juifClearHost(juifTabHost)"), "shell é limpo antes da construção da nova Tab Bar")
require("UI_RUNTIME_ERROR" in script and "juifReportRuntimeFailure" in script, "falha de runtime não estruturada")
require("catch(Throwable" in script, "callbacks ainda permitem Error escapar")
require("new HorizontalScrollView.LayoutParams" not in script, "LayoutParams inseguro no HorizontalScrollView")
require("LinearLayout JUIFTabBar" in script and "FrameLayout.LayoutParams.WRAP_CONTENT" in script, "Tab Bar segura ausente")
require('result.put("artifact_id", "java_ui_framework")' in script, "artifact id divergente")
require('data.put("supported_component_count", 36)' in script, "contagem publicada divergente")
require('"PERMISSION_DENIED"' in script and "Settings.canDrawOverlays" in script, "validação de overlay ausente")
require("catch(JSONException e)" in script, "JSON inválido não classificado")
for forbidden in ["data_json", "error_code", "error_message", "error_json"]:
    require(forbidden not in script, "campo proibido no Resultado: " + forbidden)

require(variables["Resultado"].get("dictionary", {}).get("entries", []) == [], "Resultado deve iniciar vazio")

default_ui = json.loads(variables["JUIF UI Json"]["m_stringValue"])
expected_pages = {
    "overview",
    "catalog_layout",
    "catalog_forms",
    "catalog_data",
    "catalog_feedback",
    "catalog_navigation",
    "playground",
}
require(default_ui.get("initial_page") == "overview", "initial_page divergente")
require(set(default_ui.get("pages", {})) == expected_pages, "páginas da UI padrão divergentes")

shell = default_ui.get("shell", {})
require(set(shell) == {"top_app_bar", "tab_bar", "bottom_navigation", "navigation_drawer"}, "shell padrão divergente")
require(shell["top_app_bar"].get("use_page_title") is True, "Top App Bar deve usar título da página")
require(shell["tab_bar"].get("key") == "catalog_section", "estado do catálogo deve ser unificado")
require(set(shell["tab_bar"].get("visible_pages", [])) == expected_pages - {"overview", "playground"}, "visibilidade da Tab Bar divergente")
require(len(shell["tab_bar"].get("items", [])) == 5, "Tab Bar deve possuir cinco categorias")
require(len(shell["bottom_navigation"].get("items", [])) == 3, "Bottom Navigation deve possuir três áreas")
require(shell["navigation_drawer"].get("width") == 304, "largura canônica do drawer divergente")

types: list[str] = []
collect_types(default_ui, types)
canonical_types = [item["type"] for item in catalog["components"]]
require(set(types) == set(canonical_types), f"UI padrão não cobre 36 componentes: {set(canonical_types) - set(types)}")
require(types.count("tab_bar") == 1, "UI padrão deve possuir uma única Tab Bar")
require("catalog_tabs_" not in variables["JUIF UI Json"]["m_stringValue"], "estado fragmentado antigo ainda presente")

targets: list[tuple[str, str]] = []
navigation_targets(shell, targets)
for item_id, target in targets:
    require(target in expected_pages, f"target inválido em {item_id}: {target}")

compact = json.dumps(default_ui, ensure_ascii=False, separators=(",", ":"))
escaped_expected = (
    compact.replace("\\", "\\\\")
    .replace('"', '\\"')
    .replace("\r", "\\r")
    .replace("\n", "\\n")
    .replace("\t", "\\t")
)
require(variables["Tmp_DefaultUiJson"]["m_stringValue"] == escaped_expected, "fallback interno divergente")

catalog_types = [item["type"] for item in catalog["components"]]
config_types = config["settings"]["supported_component_types"]
require(catalog.get("component_count") == 36, "catálogo deve conter 36 componentes")
require(len(catalog_types) == 36 and len(set(catalog_types)) == 36, "tipos duplicados/divergentes")
require(config_types == catalog_types, "config e catálogo divergentes")
require(config["settings"]["shell_mode"] == "persistent_hosts", "config ainda declara shell rolável")
require(config["settings"]["persistent_shell_enabled"] is True, "shell persistente desabilitado")
require(manifest["implementation_audit"]["runtime_hierarchy"] == "persistent_top_tabs_rail_scroll_bottom_drawer_hosts", "auditoria de runtime divergente")
require(contract["shell_contract"]["persistent_shell"] is True, "contrato não declara shell persistente")

# Verificação sintática opcional com o parser BeanShell disponível no ambiente de validação.
parser_jar = Path("/usr/share/java/bsh.jar")
java_bin = shutil.which("java")
if parser_jar.exists() and java_bin:
    normalized = re.sub(
        r"0x[0-9A-Fa-f]{8}\b",
        lambda match: str(int(match.group(0), 16) - (2**32 if int(match.group(0), 16) >= 2**31 else 0)),
        script,
    )
    normalized = re.sub(r"\bfinal\s+", "", normalized)
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "framework.java"
        source.write_text(normalized, encoding="utf-8")
        subprocess.run(
            [java_bin, "-cp", str(parser_jar), "bsh.Parser", str(source)],
            check=True,
            capture_output=True,
            text=True,
        )

print("OK: Java UI Framework profissional com hotfix de navegação validado")
