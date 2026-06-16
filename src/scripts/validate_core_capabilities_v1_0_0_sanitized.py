#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT
CAPS = {
  "json_config_manager": "[CDXMS] Json Config Manager",
  "bootstrap": "[CDXMS] Bootstrap",
  "result_manager": "[CDXMS] Registrar Resultado",
  "logger": "[CDXMS] Logger",
  "string_utils": "[CDXMS] String Utils",
}
ABLOCKS = {
  "json_config_manager": "[CDXMS]_Json_Config_Manager.ablock",
  "bootstrap": "[CDXMS]_Bootstrap.ablock",
  "result_manager": "[CDXMS]_Registrar_Resultado.ablock",
  "logger": "[CDXMS]_Logger.ablock",
  "string_utils": "[CDXMS]_String_Utils.ablock",
}
errors=[]
for cid, expected_name in CAPS.items():
    base = SRC / "capabilities" / cid
    for name in ["manifest.json","contract.json","config.default.json","README.md","body.md"]:
        if not (base/name).exists(): errors.append(f"missing {base/name}")
    manifest=json.loads((base/"manifest.json").read_text(encoding="utf-8"))
    if manifest["capability"]["version"] != "1.0.0": errors.append(f"{cid} version drift")
    audit=manifest.get("implementation_audit",{})
    if audit.get("stage") != "pre_release_1_0_0_sanitization": errors.append(f"{cid} missing implementation_audit")
    ab=base/"macrodroid"/ABLOCKS[cid]
    if not ab.exists(): errors.append(f"missing ablock {ab}"); continue
    data=json.loads(ab.read_text(encoding="utf-8"))
    macro=data.get("macro",{})
    if data.get("macroExportVersion") != 1: errors.append(f"{cid} invalid macroExportVersion")
    if macro.get("isActionBlock") is not True: errors.append(f"{cid} is not action block")
    if macro.get("m_name") != expected_name: errors.append(f"{cid} name mismatch: {macro.get('m_name')}")
    outs=[v.get("m_name") for v in macro.get("localVariables",[]) if v.get("supportsOutput")]
    if outs != ["Resultado"]: errors.append(f"{cid} outputs must be ['Resultado'], got {outs}")
if errors:
    print("VALIDATION FAILED")
    for e in errors: print("-", e)
    raise SystemExit(1)
print("VALIDATION OK — CDXMS core capabilities v1.0.0 pre-release sanitized")
