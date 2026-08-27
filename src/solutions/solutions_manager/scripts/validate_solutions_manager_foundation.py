#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
CAPABILITIES = ROOT / "capabilities"
EXPORT_PATH = BASE / "macrodroid" / "[CDXMS]_Solutions_Manager.macro"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def capability_exports() -> dict[str, dict]:
    result: dict[str, dict] = {}
    for directory in sorted(CAPABILITIES.iterdir()):
        if not directory.is_dir():
            continue
        candidates = list((directory / "macrodroid").glob("*.ablock"))
        assert len(candidates) == 1, f"{directory.name}: export .ablock divergente"
        macro = load(candidates[0])["macro"]
        assert macro["isActionBlock"] is True
        result[macro["m_name"]] = macro
    return result


def action_block_calls(owner: dict) -> list[dict]:
    return [
        action
        for action in owner.get("m_actionList", [])
        if action.get("m_classType") == "ActionBlockAction"
    ]


def main() -> None:
    manifest = load(BASE / "manifest.json")
    contract = load(BASE / "contract.json")
    config = load(BASE / "config.default.json")
    machine = load(BASE / "state_machine.json")
    orchestration = load(BASE / "orchestration.json")
    ui = load(BASE / "ui_schema.default.json")
    export = load(EXPORT_PATH)
    macro = export["macro"]

    assert manifest["artifact_type"] == "solution"
    assert manifest["solution"]["id"] == "solutions_manager"
    assert manifest["solution"]["single_entry"] is True
    assert manifest["macrodroid_export"]["status"] == "structurally_ready_for_device_homologation"
    assert manifest["implementation_audit"]["macro_export_ready"] is True
    assert manifest["implementation_audit"]["device_homologation_required"] is True
    assert manifest["distribution_model"]["automatic_macro_import"] is False

    assert export["macroExportVersion"] == 1
    assert export.get("globalVariables", []) == []
    assert macro["isActionBlock"] is False
    assert macro["m_name"] == manifest["macrodroid_export"]["expected_name"]
    assert [item["m_classType"] for item in macro["m_triggerList"]] == [
        "EmptyTrigger",
        "IntentReceivedTrigger",
    ]
    assert macro["m_triggerList"][1]["action"] == "com.cdxms.solutions.EVENT"

    action_classes = [action["m_classType"] for action in macro["m_actionList"]]
    assert len(action_classes) == 20
    assert action_classes[:13] == [
        "IfConditionAction",
        "ActionBlockAction",
        "IfConditionAction",
        "ActionBlockAction",
        "IfConditionAction",
        "ActionBlockAction",
        "ElseAction",
        "ToastAction",
        "EndIfAction",
        "ElseAction",
        "ToastAction",
        "EndIfAction",
        "EndIfAction",
    ]
    assert [call["actionBlockName"] for call in action_block_calls(macro)] == [
        "[CDXMS] Bootstrap",
        "[CDXMS] JUIF UI Builder",
        "[CDXMS] Java UI Framework",
    ]
    bootstrap_call = action_block_calls(macro)[0]
    assert bootstrap_call["continueActionsWithoutWaiting"] is False
    assert bootstrap_call["inputVarsMap"]["Operation"] == "initialize_ecosystem"
    assert bootstrap_call["inputVarsMap"]["Load Context?"] == "true"

    official = capability_exports()
    embedded = macro.get("exportedActionBlocks", [])
    assert len(embedded) == manifest["macrodroid_export"]["embedded_action_block_count"]
    assert len({item["m_name"] for item in embedded}) == len(embedded)
    assert {item["m_name"] for item in embedded} == set(official)
    for item in embedded:
        assert item["m_GUID"] == official[item["m_name"]]["m_GUID"]
        assert item.get("exportedActionBlocks", []) == []

    embedded_guids = {item["m_name"]: item["m_GUID"] for item in embedded}
    for owner in [macro, *embedded]:
        for call in action_block_calls(owner):
            assert call["actionBlockName"] in embedded_guids, (
                f"{owner['m_name']}: dependency not embedded: {call['actionBlockName']}"
            )
            assert call["actionBlockId"] == embedded_guids[call["actionBlockName"]], (
                f"{owner['m_name']}: GUID mismatch: {call['actionBlockName']}"
            )

    variables = {item["m_name"]: item for item in macro["localVariables"]}
    assert set(contract["working_variables"]) == set(variables) - {"Resultado"}
    assert len(contract["outputs"]) == 1
    assert contract["outputs"][0]["name"] == "Resultado"
    assert variables["Resultado"]["supportsOutput"] is True
    assert all(str(item.get("description", "")).strip() for item in variables.values())
    assert set(contract["result"]["forbidden_top_level_fields"]) == {
        "data_json",
        "error_code",
        "error_message",
        "error_json",
    }

    assert config["feature_flags"]["lifecycle_mutations"] is False
    assert config["feature_flags"]["event_bridge"] is True
    assert config["feature_flags"]["business_event_dispatch"] is False
    assert config["feature_flags"]["remote_payload_pipeline"] is False
    assert machine["initial_state"] == "starting"
    assert "waiting_ui_event" in machine["states"]
    assert "launch" in orchestration["operations"]
    assert orchestration["operations"]["refresh_catalog"][2]["operation"] == "verify_sha256"

    page_ids = {page["id"] for page in ui["pages"]}
    expected = {
        "home",
        "catalog",
        "artifact_details",
        "installed",
        "updates",
        "diagnostics",
        "settings",
        "about",
    }
    assert page_ids == expected
    assert {"top_app_bar", "bottom_navigation", "navigation_drawer"}.issubset(ui["shell"])

    print(
        "Solutions Manager foundation: OK "
        f"(actions={len(action_classes)}, embedded={len(embedded)}, pages={len(page_ids)})"
    )


if __name__ == "__main__":
    main()
