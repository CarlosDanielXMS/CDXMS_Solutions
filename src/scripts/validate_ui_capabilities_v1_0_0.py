from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


for script in [
    ROOT / "capabilities/juif_ui_builder/scripts/validate_juif_ui_builder_incremental.py",
    ROOT / "capabilities/java_ui_framework/scripts/validate_java_ui_framework_incremental.py",
]:
    subprocess.run([sys.executable, str(script)], check=True)

# Todo JSON/export contido no overlay deve continuar estruturalmente válido.
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.suffix in {".json", ".ablock", ".macro"}:
        load(path)

release = load(ROOT / "release.json")
release_ids = {item["artifact_id"] for item in release["artifacts"]}
assert {"java_ui_framework", "juif_ui_builder"}.issubset(release_ids)
assert release["status"] == "pre_release"

catalog = load(ROOT / "catalogs/local_catalog.default.json")
capability_ids = {item["artifact_id"] for item in catalog["capabilities"]}
assert {"java_ui_framework", "juif_ui_builder"}.issubset(capability_ids)

renderer_catalog = load(ROOT / "capabilities/java_ui_framework/component_catalog.json")
renderer_config = load(ROOT / "capabilities/java_ui_framework/config.default.json")
builder_config = load(ROOT / "capabilities/juif_ui_builder/config.default.json")
canonical_types = [item["type"] for item in renderer_catalog["components"]]
assert renderer_catalog["component_count"] == 36
assert renderer_config["settings"]["supported_component_types"] == canonical_types
assert builder_config["settings"]["supported_component_types"] == canonical_types

# O package preserva o mapa completo remoto e sobrepõe hashes dos arquivos novos/modificados.
checksums = load(ROOT / "checksums.json")
assert checksums["scope"] == "complete_src_tree_except_checksums_json"
checksum_files = checksums["files"]
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(ROOT).as_posix()
    if relative == "checksums.json":
        continue
    assert relative in checksum_files, f"arquivo do overlay ausente em checksums.json: {relative}"
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    assert checksum_files[relative] == actual, f"checksum divergente: {relative}"

print("OK: integração das capabilities de UI validada")
