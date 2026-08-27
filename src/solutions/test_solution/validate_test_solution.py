from __future__ import annotations

import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
EXPORT = BASE / "macrodroid/[CDXMS]_Test_Solution.macro"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


manifest = load(BASE / "manifest.json")
contract = load(BASE / "contract.json")
config = load(BASE / "config.default.json")
schema = load(BASE / "ui_schema.default.json")
remote = load(BASE / "remote_manifest.json")
document = load(EXPORT)
macro = document["macro"]

assert document["macroExportVersion"] == 1
assert document["globalVariables"] == []
assert macro["m_name"] == "[CDXMS] Test Solution"
assert macro["isActionBlock"] is False
assert [item["m_classType"] for item in macro["m_triggerList"]] == ["EmptyTrigger"]
assert len(macro["m_actionList"]) == 13
assert [
    item["actionBlockName"]
    for item in macro["m_actionList"]
    if item["m_classType"] == "ActionBlockAction"
] == [
    "[CDXMS] Bootstrap",
    "[CDXMS] JUIF UI Builder",
    "[CDXMS] Java UI Framework",
]

variables = {item["m_name"]: item for item in macro["localVariables"]}
assert set(variables) == {
    "Tmp_TestViewModelJson",
    "Tmp_TestUiSchemaJson",
    "Resultado",
}
assert json.loads(variables["Tmp_TestViewModelJson"]["m_stringValue"]) == config
assert json.loads(variables["Tmp_TestUiSchemaJson"]["m_stringValue"]) == schema
assert variables["Resultado"]["supportsOutput"] is True

embedded = {item["m_name"]: item for item in macro["exportedActionBlocks"]}
assert set(embedded) == {
    "[CDXMS] Json Config Manager",
    "[CDXMS] Bootstrap",
    "[CDXMS] String Utils",
    "[CDXMS] JUIF UI Builder",
    "[CDXMS] Java UI Framework",
}
for owner in [macro, *embedded.values()]:
    for action in owner.get("m_actionList", []):
        if action.get("m_classType") != "ActionBlockAction":
            continue
        dependency = embedded[action["actionBlockName"]]
        assert action["actionBlockId"] == dependency["m_GUID"]

builder_core = next(
    action["scriptText"]
    for action in embedded["[CDXMS] JUIF UI Builder"]["m_actionList"]
    if action.get("actionLabel") == "Construir contrato JUIF"
)
assert "function decodeJsonTransportLayer" in builder_core
assert "decoded_transport_layers" in builder_core

assert manifest["artifact_id"] == "test_solution"
assert contract["artifact_id"] == "test_solution"
assert remote["macrodroid_export"]["manual_import_required"] is True
assert remote["macrodroid_export"]["expected_name"] == macro["m_name"]
assert {page["id"] for page in schema["pages"]} == {"overview", "components"}

print(
    "Test Solution: OK "
    f"(actions={len(macro['m_actionList'])}, embedded={len(embedded)}, pages={len(schema['pages'])})"
)
