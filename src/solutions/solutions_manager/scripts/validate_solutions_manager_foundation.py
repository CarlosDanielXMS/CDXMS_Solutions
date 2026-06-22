#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def load(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def main() -> None:
    manifest = load("manifest.json")
    contract = load("contract.json")
    config = load("config.default.json")
    machine = load("state_machine.json")
    orchestration = load("orchestration.json")
    ui = load("ui_schema.default.json")

    assert manifest["artifact_type"] == "solution"
    assert manifest["solution"]["id"] == "solutions_manager"
    assert manifest["solution"]["single_entry"] is True
    assert manifest["macrodroid_export"]["status"] == "pending_implementation"
    assert manifest["implementation_audit"]["critical_gate"] == "juif_to_macrodroid_event_bridge"

    assert len(contract["outputs"]) == 1
    assert contract["outputs"][0]["name"] == "Resultado"
    assert set(contract["result"]["forbidden_top_level_fields"]) == {
        "data_json", "error_code", "error_message", "error_json"
    }

    assert config["feature_flags"]["lifecycle_mutations"] is False
    assert config["feature_flags"]["event_bridge"] is False
    assert machine["initial_state"] == "starting"
    assert "waiting_ui_event" in machine["states"]
    assert "launch" in orchestration["operations"]

    page_ids = {page["id"] for page in ui["pages"]}
    expected = {"home", "catalog", "artifact_details", "installed", "updates", "diagnostics", "settings", "about"}
    assert page_ids == expected
    assert {"top_app_bar", "bottom_navigation", "navigation_drawer"}.issubset(ui["shell"])

    print("Solutions Manager foundation: OK")


if __name__ == "__main__":
    main()
