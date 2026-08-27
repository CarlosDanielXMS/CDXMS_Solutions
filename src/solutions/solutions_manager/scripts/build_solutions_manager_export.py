from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOLUTION = ROOT / "solutions" / "solutions_manager"
EXPORT = SOLUTION / "macrodroid" / "[CDXMS]_Solutions_Manager.macro"
CAPABILITIES = ROOT / "capabilities"

BOOTSTRAP_NAME = "[CDXMS] Bootstrap"
BOOTSTRAP_GUID = -8974663416693308000
JUIF_BUILDER_NAME = "[CDXMS] JUIF UI Builder"
JUIF_BUILDER_GUID = -6466181188242727880
JUIF_RENDERER_NAME = "[CDXMS] Java UI Framework"
JUIF_RENDERER_GUID = -7176705300326504843
REMOTE_SOURCE_NAME = "[CDXMS] Remote Source Manager"
REMOTE_SOURCE_GUID = -611028407650120260

EMBED_ORDER = [
    "json_config_manager",
    "bootstrap",
    "result_manager",
    "logger",
    "string_utils",
    "artifact_manager",
    "dependency_resolver",
    "remote_source_manager",
    "file_integrity",
    "juif_ui_builder",
    "java_ui_framework",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def action_block_exports() -> list[dict]:
    exports: list[dict] = []
    for capability_id in EMBED_ORDER:
        candidates = list((CAPABILITIES / capability_id / "macrodroid").glob("*.ablock"))
        if len(candidates) != 1:
            raise ValueError(f"{capability_id}: esperado exatamente um export .ablock")
        macro = load(candidates[0])["macro"]
        if macro.get("isActionBlock") is not True:
            raise ValueError(f"{capability_id}: export não é Action Block")
        macro = copy.deepcopy(macro)
        macro["exportedActionBlocks"] = []
        exports.append(macro)
    return exports


def result_constraint(result_variable: dict, *, expected: bool, siguid: int) -> dict:
    return {
        "checkCase": False,
        "dictionaryKeys": {"keys": ["success"]},
        "dictionaryType": 0,
        "enableRegex": False,
        "m_booleanValue": expected,
        "m_doubleValue": 0,
        "m_intCompareVariable": False,
        "m_intGreaterThan": False,
        "m_intLessThan": False,
        "m_intNotEqual": False,
        "m_intValue": 0,
        "m_otherValueToCompare": copy.deepcopy(result_variable),
        "m_stringComparisonType": 0,
        "m_stringEqual": True,
        "m_stringValue": "",
        "m_variable": copy.deepcopy(result_variable),
        "disableLogging": False,
        "m_SIGUID": siguid,
        "m_classType": "MacroDroidVariableConstraint",
        "m_comment": "",
        "m_constraintList": [],
        "m_isDisabled": False,
        "m_isOrCondition": False,
    }


def if_result(result_variable: dict, *, siguid: int, constraint_siguid: int, comment: str) -> dict:
    return {
        "disableLogging": False,
        "m_SIGUID": siguid,
        "m_classType": "IfConditionAction",
        "m_comment": comment,
        "m_constraintList": [
            result_constraint(result_variable, expected=True, siguid=constraint_siguid)
        ],
        "m_isDisabled": False,
        "m_isOrCondition": False,
        "childrenCollapsed": False,
        "dontLogIfConditionIsFalse": True,
    }


def text_constraint(variable: dict, *, expected: str, siguid: int) -> dict:
    return {
        "checkCase": True,
        "dictionaryKeys": {"keys": []},
        "dictionaryType": 0,
        "enableRegex": False,
        "m_booleanValue": False,
        "m_doubleValue": 0,
        "m_intCompareVariable": False,
        "m_intGreaterThan": False,
        "m_intLessThan": False,
        "m_intNotEqual": False,
        "m_intValue": 0,
        "m_otherValueToCompare": copy.deepcopy(variable),
        "m_stringComparisonType": 0,
        "m_stringEqual": True,
        "m_stringValue": expected,
        "m_variable": copy.deepcopy(variable),
        "disableLogging": False,
        "m_SIGUID": siguid,
        "m_classType": "MacroDroidVariableConstraint",
        "m_comment": "",
        "m_constraintList": [],
        "m_isDisabled": False,
        "m_isOrCondition": False,
    }


def if_text(variable: dict, *, expected: str, siguid: int, constraint_siguid: int, comment: str) -> dict:
    action = simple_action("IfConditionAction", siguid=siguid, comment=comment)
    action.update(
        {
            "m_constraintList": [
                text_constraint(variable, expected=expected, siguid=constraint_siguid)
            ],
            "childrenCollapsed": False,
            "dontLogIfConditionIsFalse": True,
        }
    )
    return action


def simple_action(class_type: str, *, siguid: int, comment: str = "") -> dict:
    return {
        "disableLogging": False,
        "m_SIGUID": siguid,
        "m_classType": class_type,
        "m_comment": comment,
        "m_constraintList": [],
        "m_isDisabled": False,
        "m_isOrCondition": False,
    }


def bootstrap_action(*, siguid: int) -> dict:
    action = simple_action(
        "ActionBlockAction",
        siguid=siguid,
        comment="Inicializa ou valida o core local antes de abrir o Manager.",
    )
    action.update(
        {
            "actionBlockId": BOOTSTRAP_GUID,
            "actionBlockName": BOOTSTRAP_NAME,
            "continueActionsWithoutWaiting": False,
            "inputDictionaryMap": {},
            "inputVarsMap": {
                "Operation": "initialize_ecosystem",
                "Requested Artifact Type": "solution",
                "Requested Artifact Id": "solutions_manager",
                "Force Repair?": "false",
                "Load Context?": "true",
                "Config Json": "",
                "Session Id": "solutions-manager-session-v1",
                "Correlation Id": "solutions-manager-launch-v1",
            },
            "outputDictionaryMap": {"Resultado": {"keys": []}},
            "outputVarsMap": {"Resultado": "Resultado"},
        }
    )
    return action


def download_test_solution_action(*, siguid: int) -> dict:
    action = simple_action(
        "ActionBlockAction",
        siguid=siguid,
        comment="Baixa e valida o export da Solution de Teste em staging.",
    )
    action.update(
        {
            "actionBlockId": REMOTE_SOURCE_GUID,
            "actionBlockName": REMOTE_SOURCE_NAME,
            "continueActionsWithoutWaiting": False,
            "inputDictionaryMap": {},
            "inputVarsMap": {
                "Operation": "fetch_macrodroid_export",
                "Source Json": "",
                "Source Id": "cdxms_official_github",
                "Remote Path": "solutions/test_solution/macrodroid/[CDXMS]_Test_Solution.macro",
                "Expected File Type": "macrodroid_macro",
                "Cache Root Path": "/storage/emulated/0/Documents/CDXMS_Solutions/packages/downloaded/test_solution",
                "Timeout Seconds": "30",
                "Strict Mode?": "true",
                "Session Id": "solutions-manager-session-v1",
                "Correlation Id": "solutions-manager-download-test-solution-v1",
            },
            "outputDictionaryMap": {"Resultado": {"keys": []}},
            "outputVarsMap": {"Resultado": "Resultado"},
        }
    )
    return action


def toast(message: str, *, siguid: int, comment: str) -> dict:
    action = simple_action("ToastAction", siguid=siguid, comment=comment)
    action.update(
        {
            "cancelPrevious": True,
            "m_backgroundColor": -14606047,
            "m_displayIcon": False,
            "m_duration": 1,
            "m_horizontalPosition": 0,
            "m_imageName": "launcher_no_border",
            "m_imagePackageName": "com.arlosoft.macrodroid",
            "m_imageResourceName": "launcher_no_border",
            "m_messageText": message,
            "m_position": 0,
            "m_textColor": -1,
            "m_tintIcon": False,
            "maintainSpaces": True,
            "useTextOnly": True,
        }
    )
    return action


def build_launch_actions(macro: dict) -> list[dict]:
    current = macro["m_actionList"]
    manual_if = next(
        action
        for action in current
        if action.get("m_classType") == "IfConditionAction"
        and action.get("m_comment") == "Abertura manual."
    )
    builder = next(
        action
        for action in current
        if action.get("m_classType") == "ActionBlockAction"
        and action.get("actionBlockName") == JUIF_BUILDER_NAME
    )
    renderer = next(
        action
        for action in current
        if action.get("m_classType") == "ActionBlockAction"
        and action.get("actionBlockName") == JUIF_RENDERER_NAME
    )
    event_start = next(
        index
        for index, action in enumerate(current)
        if action.get("m_classType") == "IfConditionAction"
        and action.get("m_comment") == "Consome evento JUIF."
    )
    current_event_actions = current[event_start:]
    result_variable = next(
        variable for variable in macro["localVariables"] if variable["m_name"] == "Resultado"
    )

    launch = [
        copy.deepcopy(manual_if),
        bootstrap_action(siguid=-6123400000000000121),
        if_result(
            result_variable,
            siguid=-6123400000000000122,
            constraint_siguid=-6123400000000000222,
            comment="Continua somente após bootstrap confirmado.",
        ),
        copy.deepcopy(builder),
        if_result(
            result_variable,
            siguid=-6123400000000000123,
            constraint_siguid=-6123400000000000223,
            comment="Renderiza somente contrato JUIF válido.",
        ),
        copy.deepcopy(renderer),
        simple_action("ElseAction", siguid=-6123400000000000124),
        toast(
            "Solutions Manager · Falha ao construir a interface: {lv=Resultado[message]}",
            siguid=-6123400000000000125,
            comment="Falha do Builder.",
        ),
        simple_action("EndIfAction", siguid=-6123400000000000126),
        simple_action("ElseAction", siguid=-6123400000000000127),
        toast(
            "Solutions Manager · Falha ao inicializar: {lv=Resultado[message]}",
            siguid=-6123400000000000128,
            comment="Falha do Bootstrap.",
        ),
        simple_action("EndIfAction", siguid=-6123400000000000129),
        simple_action("EndIfAction", siguid=-6123400000000000130),
    ]
    event_action_variable = next(
        variable
        for variable in macro["localVariables"]
        if variable["m_name"] == "Tmp_SmEventAction"
    )
    event_validator = copy.deepcopy(current_event_actions[1])
    event_validator["scriptText"] = event_validator["scriptText"].replace(
        "var allowed={refresh_catalog:1,validate_ecosystem:1,closed:1};",
        "var allowed={refresh_catalog:1,validate_ecosystem:1,download_test_solution:1,closed:1};",
    )
    event_actions = [
        copy.deepcopy(current_event_actions[0]),
        event_validator,
        copy.deepcopy(current_event_actions[2]),
        copy.deepcopy(current_event_actions[3]),
        copy.deepcopy(current_event_actions[4]),
        if_result(
            result_variable,
            siguid=-6123400000000000131,
            constraint_siguid=-6123400000000000231,
            comment="Executa somente eventos JUIF validados.",
        ),
        if_text(
            event_action_variable,
            expected="download_test_solution",
            siguid=-6123400000000000132,
            constraint_siguid=-6123400000000000232,
            comment="Executa o download solicitado pela interface.",
        ),
        download_test_solution_action(siguid=-6123400000000000133),
        if_result(
            result_variable,
            siguid=-6123400000000000134,
            constraint_siguid=-6123400000000000234,
            comment="Confirma o download validado.",
        ),
        toast(
            "Download concluído · {lv=Resultado[data][cache][file_path]} · Importe o arquivo pelo MacroDroid.",
            siguid=-6123400000000000135,
            comment="Informa o arquivo baixado.",
        ),
        simple_action("ElseAction", siguid=-6123400000000000136),
        toast(
            "Falha no download · {lv=Resultado[message]}",
            siguid=-6123400000000000137,
            comment="Expõe a falha do pipeline remoto.",
        ),
        simple_action("EndIfAction", siguid=-6123400000000000138),
        simple_action("ElseAction", siguid=-6123400000000000139),
        toast(
            "Solutions Manager · ação recebida: {lv=Tmp_SmEventAction}",
            siguid=-6123400000000000140,
            comment="Confirma eventos válidos sem operação remota.",
        ),
        simple_action("EndIfAction", siguid=-6123400000000000141),
        simple_action("ElseAction", siguid=-6123400000000000142),
        toast(
            "Solutions Manager · evento rejeitado: {lv=Resultado[message]}",
            siguid=-6123400000000000143,
            comment="Expõe rejeição do contrato de evento.",
        ),
        simple_action("EndIfAction", siguid=-6123400000000000144),
        copy.deepcopy(current_event_actions[-1]),
    ]
    return launch + event_actions


def validate_runtime_closure(macro: dict) -> None:
    embedded = {item["m_name"]: item["m_GUID"] for item in macro["exportedActionBlocks"]}
    expected = {item["m_name"]: item["m_GUID"] for item in action_block_exports()}
    if embedded != expected:
        raise ValueError("closure incorporada não corresponde às capabilities oficiais")

    for owner in [macro, *macro["exportedActionBlocks"]]:
        for action in owner.get("m_actionList", []):
            if action.get("m_classType") != "ActionBlockAction":
                continue
            name = action.get("actionBlockName")
            guid = action.get("actionBlockId")
            if embedded.get(name) != guid:
                raise ValueError(
                    f"{owner['m_name']}: referência inválida para {name}: {guid}"
                )


def main() -> None:
    document = load(EXPORT)
    macro = document["macro"]
    seeds = {
        "Tmp_SmViewModelJson": json.dumps(
            load(SOLUTION / "config.default.json"),
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        "Tmp_SmUiSchemaJson": json.dumps(
            load(SOLUTION / "ui_schema.default.json"),
            ensure_ascii=False,
            separators=(",", ":"),
        ),
    }
    for variable in macro["localVariables"]:
        if variable["m_name"] in seeds:
            variable["m_stringValue"] = seeds[variable["m_name"]]
    macro["m_actionList"] = build_launch_actions(macro)
    macro["exportedActionBlocks"] = action_block_exports()
    macro["m_description"] = (
        "Entrada permanente do CDXMS Solutions. Na primeira execução inicializa o core "
        "com runtime incorporado; nas seguintes abre o Manager e recebe eventos JUIF."
    )
    validate_runtime_closure(macro)
    EXPORT.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "Solutions Manager export: OK "
        f"(actions={len(macro['m_actionList'])}, embedded={len(macro['exportedActionBlocks'])})"
    )


if __name__ == "__main__":
    main()
