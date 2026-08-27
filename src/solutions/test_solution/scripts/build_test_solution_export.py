from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOLUTION = Path(__file__).resolve().parents[1]
MANAGER_EXPORT = (
    ROOT / "solutions/solutions_manager/macrodroid/[CDXMS]_Solutions_Manager.macro"
)
TARGET = SOLUTION / "macrodroid/[CDXMS]_Test_Solution.macro"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compact(path: Path) -> str:
    return json.dumps(load(path), ensure_ascii=False, separators=(",", ":"))


def replace_strings(value):
    replacements = {
        "Tmp_SmViewModelJson": "Tmp_TestViewModelJson",
        "Tmp_SmUiSchemaJson": "Tmp_TestUiSchemaJson",
        "solutions-manager-session-v1": "test-solution-session-v1",
        "solutions-manager-launch-v1": "test-solution-launch-v1",
        "solutions_manager": "test_solution",
        "Solutions Manager": "Test Solution",
    }
    if isinstance(value, dict):
        return {key: replace_strings(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_strings(item) for item in value]
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
    return value


def remap_siguids(value, offset: int) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "m_SIGUID" and isinstance(item, int):
                value[key] = item - offset
            else:
                remap_siguids(item, offset)
    elif isinstance(value, list):
        for item in value:
            remap_siguids(item, offset)


def runtime_closure(actions: list[dict], available: list[dict]) -> list[dict]:
    by_name = {item["m_name"]: item for item in available}
    required = {
        action["actionBlockName"]
        for action in actions
        if action.get("m_classType") == "ActionBlockAction"
    }
    pending = list(required)
    while pending:
        name = pending.pop()
        block = by_name[name]
        for action in block.get("m_actionList", []):
            if action.get("m_classType") != "ActionBlockAction":
                continue
            dependency = action["actionBlockName"]
            if dependency not in required:
                required.add(dependency)
                pending.append(dependency)
    closure = []
    for item in available:
        if item["m_name"] in required:
            block = copy.deepcopy(item)
            block["exportedActionBlocks"] = []
            closure.append(block)
    return closure


def main() -> None:
    manager_document = load(MANAGER_EXPORT)
    manager = manager_document["macro"]
    macro = copy.deepcopy(manager)

    trigger = copy.deepcopy(manager["m_triggerList"][0])
    trigger["m_SIGUID"] = -6123400000000001191
    trigger["m_comment"] = "Execução manual da Solution de Teste."
    macro["m_triggerList"] = [trigger]

    actions = replace_strings(copy.deepcopy(manager["m_actionList"][:13]))
    actions[0]["m_constraintList"][0]["m_siGuidThatInvoked"] = trigger["m_SIGUID"]
    remap_siguids(actions, 1_000_000)
    macro["m_actionList"] = actions

    selected_variables = []
    for variable in manager["localVariables"]:
        if variable["m_name"] not in {
            "Resultado",
            "Tmp_SmViewModelJson",
            "Tmp_SmUiSchemaJson",
        }:
            continue
        variable = copy.deepcopy(variable)
        if variable["m_name"] == "Tmp_SmViewModelJson":
            variable["m_name"] = "Tmp_TestViewModelJson"
            variable["m_stringValue"] = compact(SOLUTION / "config.default.json")
            variable["description"] = "Dados da interface de homologação."
        elif variable["m_name"] == "Tmp_SmUiSchemaJson":
            variable["m_name"] = "Tmp_TestUiSchemaJson"
            variable["m_stringValue"] = compact(SOLUTION / "ui_schema.default.json")
            variable["description"] = "Schema JUIF completo da Solution de Teste."
        selected_variables.append(variable)
    macro["localVariables"] = selected_variables

    macro["m_GUID"] = -6123400000000001000
    macro["m_name"] = "[CDXMS] Test Solution"
    macro["m_category"] = "[CDXMS] Solutions"
    macro["m_description"] = (
        "Solution genérica de homologação. Executa Bootstrap, JUIF UI Builder e "
        "Java UI Framework sem operações destrutivas."
    )
    macro["lastEditedTimestamp"] = 1787860800000
    macro["exportedActionBlocks"] = runtime_closure(
        macro["m_actionList"], manager["exportedActionBlocks"]
    )

    document = {"macroExportVersion": 1, "macro": macro, "globalVariables": []}
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Test Solution export: OK (actions={len(macro['m_actionList'])}, "
        f"embedded={len(macro['exportedActionBlocks'])})"
    )


if __name__ == "__main__":
    main()
