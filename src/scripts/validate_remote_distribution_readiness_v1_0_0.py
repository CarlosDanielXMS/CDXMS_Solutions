from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPABILITIES = ROOT / "capabilities"
SOLUTIONS = ROOT / "solutions"
TEXT_SUFFIXES = {".ablock", ".json", ".macro", ".md", ".py", ".js"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitkeep":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def export_for(directory: Path) -> tuple[Path, dict]:
    candidates = list((directory / "macrodroid").glob("*.ablock"))
    candidates += list((directory / "macrodroid").glob("*.macro"))
    assert len(candidates) == 1, f"{directory}: esperado exatamente um export MacroDroid"
    return candidates[0], load(candidates[0])


def validate_json_tree() -> None:
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".json", ".macro", ".ablock"}:
            load(path)


def validate_capabilities() -> dict[str, dict]:
    exports: dict[str, dict] = {}
    name_to_id: dict[str, str] = {}
    records: list[tuple[Path, dict, dict, dict]] = []

    for directory in sorted(CAPABILITIES.iterdir()):
        if not directory.is_dir():
            continue
        manifest = load(directory / "manifest.json")
        contract = load(directory / "contract.json")
        export_path, document = export_for(directory)
        macro = document["macro"]
        capability_id = manifest["capability"]["id"]
        assert capability_id == directory.name
        assert manifest["artifact_type"] == "capability"
        assert document["macroExportVersion"] == 1
        assert macro["isActionBlock"] is True
        assert macro["m_name"] == manifest["macrodroid_export"]["expected_name"]
        assert macro["m_triggerList"] == []
        assert document.get("globalVariables", []) == []
        assert len([v for v in macro["localVariables"] if v.get("supportsOutput")]) == 1
        assert next(v for v in macro["localVariables"] if v.get("supportsOutput"))["m_name"] == "Resultado"
        assert all(str(v.get("description", "")).strip() for v in macro["localVariables"])
        assert set(manifest["operations"]) == set(contract["operations"])
        assert manifest["macrodroid_export"]["file_path"] == export_path.relative_to(ROOT).as_posix()
        exports[macro["m_name"]] = macro
        name_to_id[macro["m_name"]] = capability_id
        records.append((directory, manifest, contract, macro))

    for directory, manifest, _contract, macro in records:
        declared = set(manifest["requires"]["capabilities"])
        invoked = {
            name_to_id[action["actionBlockName"]]
            for action in macro["m_actionList"]
            if action.get("m_classType") == "ActionBlockAction"
        }
        assert declared == invoked, (
            f"{directory.name}: requires deve representar apenas calls reais; "
            f"declared={sorted(declared)} invoked={sorted(invoked)}"
        )
        for action in macro["m_actionList"]:
            if action.get("m_classType") != "ActionBlockAction":
                continue
            target = exports[action["actionBlockName"]]
            assert action["actionBlockId"] == target["m_GUID"], (
                f"{directory.name}: GUID divergente para {action['actionBlockName']}"
            )
    return exports


def validate_remote_manifests() -> int:
    count = 0
    for path in sorted(ROOT.rglob("remote_manifest.json")):
        manifest = load(path)
        assert manifest["file_type"] == "remote_artifact_manifest"
        source = manifest["source"]
        assert source["type"] == "github_raw"
        assert source["repository"] == "CarlosDanielXMS/CDXMS_Solutions"
        assert source["base_raw_url"].startswith("https://raw.githubusercontent.com/")
        assert "/blob/" not in source["base_raw_url"]
        for item in manifest["files"]:
            target = ROOT / item["path"]
            assert target.is_file(), f"{path}: arquivo ausente: {item['path']}"
            assert item["checksum_sha256"] == sha256(target), (
                f"{path}: checksum divergente: {item['path']}"
            )
        count += 1
    return count


def validate_release_and_catalog() -> None:
    release = load(ROOT / "release.json")
    catalog = load(ROOT / "catalogs" / "local_catalog.default.json")
    assert release["status"] == "pre_release"
    assert release["distribution"]["homologation_ref"] == "develop"
    release_ids = {item["artifact_id"] for item in release["artifacts"]}
    catalog_ids = {
        item["artifact_id"]
        for group in ("core", "capabilities", "solutions")
        for item in catalog[group]
    }
    assert release_ids == catalog_ids
    assert "solutions_manager" in release_ids
    for item in release["artifacts"]:
        manifest_path = ROOT / item["path"]
        remote_path = ROOT / item["remote_manifest_path"]
        assert manifest_path.is_file()
        assert remote_path.is_file()
        remote = load(remote_path)
        assert remote["artifact_id"] == item["artifact_id"]
        assert remote["artifact_type"] == item["artifact_type"]
        assert remote["version"] == item["version"]


def validate_orchestration_operations() -> None:
    orchestration = load(SOLUTIONS / "solutions_manager" / "orchestration.json")
    manifests = {
        directory.name: load(directory / "manifest.json")
        for directory in CAPABILITIES.iterdir()
        if directory.is_dir()
    }
    for operation in orchestration["operations"].values():
        for step in operation:
            capability = step.get("capability")
            requested = step.get("operation")
            if not capability or not requested:
                continue
            if requested == "operation_from_plan":
                allowed = set(step["allowed_operations"])
                assert allowed.issubset(set(manifests[capability]["operations"]))
                continue
            assert requested in manifests[capability]["operations"], (
                f"Solutions Manager referencia operação inexistente: {capability}.{requested}"
            )


def validate_complete_checksums() -> int:
    checksums = load(ROOT / "checksums.json")
    assert checksums["algorithm"] == "sha256"
    assert checksums["scope"] == "complete_src_tree_except_checksums_json"
    assert checksums["text_normalization"] == "lf"
    expected = {
        path.relative_to(ROOT).as_posix(): sha256(path)
        for path in sorted(ROOT.rglob("*"))
        if path.is_file() and path.name != "checksums.json"
    }
    assert checksums["files"] == expected, "checksums.json não representa exatamente a árvore src atual"
    return len(expected)


def run_component_validators() -> int:
    scripts = sorted(CAPABILITIES.glob("*/scripts/validate_*.py"))
    scripts.append(ROOT / "scripts" / "validate_ui_capabilities_v1_0_0.py")
    scripts.extend(sorted(SOLUTIONS.glob("*/scripts/validate_*.py")))
    for script in scripts:
        subprocess.run([sys.executable, str(script)], check=True, cwd=ROOT.parent)
    return len(scripts)


def main() -> None:
    validate_json_tree()
    capabilities = validate_capabilities()
    validate_release_and_catalog()
    validate_orchestration_operations()
    remote_manifests = validate_remote_manifests()
    checksum_files = validate_complete_checksums()
    validators = run_component_validators()
    print(
        "VALIDATION OK — CDXMS distribution readiness v1.0.0 "
        f"(capabilities={len(capabilities)}, remote_manifests={remote_manifests}, "
        f"files={checksum_files}, validators={validators})"
    )


if __name__ == "__main__":
    main()
