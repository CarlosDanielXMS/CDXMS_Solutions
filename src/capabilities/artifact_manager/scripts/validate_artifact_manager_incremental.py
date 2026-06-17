import json
from pathlib import Path
root = Path(__file__).resolve().parents[3]
cap = root / "capabilities" / "artifact_manager"
ablock = cap / "macrodroid" / "[CDXMS]_Artifact_Manager.ablock"
required = [cap/"manifest.json", cap/"contract.json", cap/"config.default.json", cap/"remote_manifest.json", cap/"README.md", cap/"body.md", ablock]
for p in required:
    if not p.exists():
        raise SystemExit(f"Missing file: {p}")
manifest=json.loads((cap/"manifest.json").read_text(encoding="utf-8"))
if manifest["capability"]["version"] != "1.0.0":
    raise SystemExit("Invalid version")
d=json.loads(ablock.read_text(encoding="utf-8"))
if d.get("macroExportVersion") != 1:
    raise SystemExit("Invalid macroExportVersion")
m=d.get("macro",{})
if m.get("isActionBlock") is not True:
    raise SystemExit("Export is not Action Block")
if m.get("m_name") != "[CDXMS] Artifact Manager":
    raise SystemExit("Invalid action block name")
outs=[v for v in m.get("localVariables",[]) if v.get("supportsOutput")]
if [v.get("m_name") for v in outs] != ["Resultado"]:
    raise SystemExit("Expected single output Resultado")
if any(v.get("m_name","").startswith("Tmp_") and v.get("supportsOutput") for v in m.get("localVariables",[])):
    raise SystemExit("Tmp variable exposed as output")
print("VALIDATION OK — CDXMS Artifact Manager v1.0.0 incremental")
