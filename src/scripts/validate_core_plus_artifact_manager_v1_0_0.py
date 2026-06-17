#!/usr/bin/env python3
import json
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
CAPS = {
    "json_config_manager": "[CDXMS] Json Config Manager",
    "bootstrap": "[CDXMS] Bootstrap",
    "result_manager": "[CDXMS] Registrar Resultado",
    "logger": "[CDXMS] Logger",
    "string_utils": "[CDXMS] String Utils",
    "artifact_manager": "[CDXMS] Artifact Manager",
}
ABLOCKS = {
    "json_config_manager": "[CDXMS]_Json_Config_Manager.ablock",
    "bootstrap": "[CDXMS]_Bootstrap.ablock",
    "result_manager": "[CDXMS]_Registrar_Resultado.ablock",
    "logger": "[CDXMS]_Logger.ablock",
    "string_utils": "[CDXMS]_String_Utils.ablock",
    "artifact_manager": "[CDXMS]_Artifact_Manager.ablock",
}
errors = []
for rel in ["core/enums.json", "core/errors.json", "release.json", "README.md", "CHANGELOG.md"]:
    if not (SRC / rel).exists():
        errors.append(f"missing {rel}")

release = json.loads((SRC / "release.json").read_text(encoding="utf-8"))
ids = {a.get("artifact_id") for a in release.get("artifacts", [])}
for cid in CAPS:
    if cid not in ids:
        errors.append(f"release missing artifact {cid}")

for cid, expected_name in CAPS.items():
    base = SRC / "capabilities" / cid
    for name in ["manifest.json", "contract.json", "config.default.json", "README.md", "body.md"]:
        if not (base / name).exists():
            errors.append(f"missing {base / name}")
    manifest_path = base / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("capability", {}).get("version") != "1.0.0":
            errors.append(f"{cid} version drift")
        if manifest.get("capability", {}).get("id") != cid:
            errors.append(f"{cid} manifest id mismatch")
    ab = base / "macrodroid" / ABLOCKS[cid]
    if not ab.exists():
        errors.append(f"missing ablock {ab}")
        continue
    data = json.loads(ab.read_text(encoding="utf-8"))
    macro = data.get("macro", {})
    if data.get("macroExportVersion") != 1:
        errors.append(f"{cid} invalid macroExportVersion")
    if macro.get("isActionBlock") is not True:
        errors.append(f"{cid} is not action block")
    if macro.get("m_name") != expected_name:
        errors.append(f"{cid} name mismatch: {macro.get('m_name')}")
    outputs = [v.get("m_name") for v in macro.get("localVariables", []) if v.get("supportsOutput")]
    if outputs != ["Resultado"]:
        errors.append(f"{cid} outputs must be ['Resultado'], got {outputs}")
    tmp_outputs = [v.get("m_name") for v in macro.get("localVariables", []) if v.get("supportsOutput") and str(v.get("m_name", "")).startswith("Tmp_")]
    if tmp_outputs:
        errors.append(f"{cid} exposes Tmp outputs: {tmp_outputs}")

enums = json.loads((SRC / "core/enums.json").read_text(encoding="utf-8"))
if "artifact_manager_operation" not in enums.get("enums", {}):
    errors.append("core/enums.json missing artifact_manager_operation")
if "artifact_lifecycle_status" not in enums.get("enums", {}):
    errors.append("core/enums.json missing artifact_lifecycle_status")
errs = json.loads((SRC / "core/errors.json").read_text(encoding="utf-8"))
for code in ["ARTIFACT_INVALID_MANIFEST", "ARTIFACT_PLAN_FAILED", "ARTIFACT_LOCAL_INSTALL_NOT_APPLIED"]:
    if code not in errs.get("errors", {}):
        errors.append(f"core/errors.json missing {code}")

if errors:
    print("VALIDATION FAILED")
    for err in errors:
        print("-", err)
    raise SystemExit(1)
print("VALIDATION OK — CDXMS Core + Artifact Manager v1.0.0 incremental merged")
