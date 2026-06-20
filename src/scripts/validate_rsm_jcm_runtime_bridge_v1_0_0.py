#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JCM_PATH = ROOT / "capabilities/json_config_manager/macrodroid/[CDXMS]_Json_Config_Manager.ablock"
RSM_PATH = ROOT / "capabilities/remote_source_manager/macrodroid/[CDXMS]_Remote_Source_Manager.ablock"


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION FAILED — {message}")


def load_macro(path: Path) -> dict:
    if not path.is_file():
        fail(f"arquivo ausente: {path.relative_to(ROOT)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    macro = payload.get("macro")
    if not isinstance(macro, dict):
        fail(f"macro inválida: {path.relative_to(ROOT)}")
    return macro


def javascript_actions(macro: dict) -> list[dict]:
    return [
        action
        for action in macro.get("m_actionList", [])
        if action.get("m_classType") == "JavaScriptAction"
    ]


def node_check(script: str) -> None:
    node = shutil.which("node")
    if not node:
        return
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
        handle.write(script)
        temp_path = Path(handle.name)
    try:
        completed = subprocess.run(
            [node, "--check", str(temp_path)],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            fail(f"JavaScript inválido: {completed.stderr.strip()}")
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> None:
    jcm = load_macro(JCM_PATH)
    rsm = load_macro(RSM_PATH)

    if len(jcm.get("m_actionList", [])) != 119:
        fail("perfil de ações do JCM foi alterado inesperadamente")
    if len(rsm.get("m_actionList", [])) != 21:
        fail("perfil de ações do RSM foi alterado inesperadamente")

    jcm_init = jcm["m_actionList"][1].get("scriptText", "")
    required_jcm_fragments = [
        "valid_file_path: safePath(filePath, true),",
        "valid_folder_path: safePath(folderPath, false),",
        '"verdadeiro"',
        '"falso"',
    ]
    for fragment in required_jcm_fragments:
        if fragment not in jcm_init:
            fail(f"JCM init sem fragmento obrigatório: {fragment}")

    forbidden_jcm_fragments = [
        'valid_file_path: safePath(filePath, true) ? "true" : "false"',
        'valid_folder_path: safePath(folderPath, false) ? "true" : "false"',
    ]
    for fragment in forbidden_jcm_fragments:
        if fragment in jcm_init:
            fail(f"JCM ainda serializa flag nativa como string: {fragment}")

    boolean_constraint_keys = set()
    for action in jcm.get("m_actionList", []):
        for constraint in action.get("m_constraintList", []):
            keys = tuple(constraint.get("dictionaryKeys", {}).get("keys", []))
            if keys in {("valid_file_path",), ("valid_folder_path",)}:
                if constraint.get("m_booleanValue") is not True:
                    fail(f"constraint {keys[0]} não é booleana")
                boolean_constraint_keys.add(keys[0])

    if boolean_constraint_keys != {"valid_file_path", "valid_folder_path"}:
        fail("constraints booleanas esperadas não foram encontradas")

    localized_file_checks = 0
    localized_folder_checks = 0
    for action in javascript_actions(jcm):
        script = action.get("scriptText", "")
        node_check(script)
        localized_file_checks += script.count(
            '["true","1","yes","y","sim","s","verdadeiro"].indexOf('
            'String(`{lv=Tmp_Work[valid_file_path]}`).trim().toLowerCase()) >= 0'
        )
        localized_folder_checks += script.count(
            '["true","1","yes","y","sim","s","verdadeiro"].indexOf('
            'String(`{lv=Tmp_Work[valid_folder_path]}`).trim().toLowerCase()) >= 0'
        )

    if localized_file_checks != 7:
        fail(f"esperados 7 checks localizados de valid_file_path, encontrados {localized_file_checks}")
    if localized_folder_checks != 1:
        fail(f"esperado 1 check localizado de valid_folder_path, encontrado {localized_folder_checks}")

    preflight = rsm["m_actionList"][1].get("scriptText", "")
    finalizer = rsm["m_actionList"][17].get("scriptText", "")
    for name, script in (("preflight", preflight), ("finalizer", finalizer)):
        node_check(script)
        if script.lstrip().startswith("(function(){"):
            fail(f"RSM {name} ainda depende de IIFE")
        if not script.rstrip().endswith("__rsmOutput;"):
            fail(f"RSM {name} não publica pela última expressão")
        if "return JSON.stringify({ operation:op" in script:
            fail(f"RSM {name} ainda contém return de fluxo principal")

    if 'let __rsmOutput = "";' not in preflight:
        fail("RSM preflight sem variável explícita de saída")
    if 'let __rsmOutput = "";' not in finalizer:
        fail("RSM finalizer sem variável explícita de saída")
    if "return pre;" in finalizer:
        fail("RSM finalizer ainda usa return pre no fluxo principal")
    if "pre_result_json" in preflight or "pre_result_json" in finalizer:
        fail("RSM ainda usa JSON textual aninhado em pre_result_json")
    if "pre_result:preResult" not in preflight or "pre_result:r" not in preflight:
        fail("RSM preflight não mantém pre_result como objeto")
    if 'work.pre_result && typeof work.pre_result === "object"' not in finalizer:
        fail("RSM finalizer não consome pre_result como objeto")
    if "__rsmOutput = JSON.stringify(pre);" not in finalizer:
        fail("RSM finalizer não serializa pre_result exatamente uma vez")

    print("VALIDATION OK — RSM/JCM runtime bridge v1.0.0")
    print("jcm_actions=119")
    print("rsm_actions=21")
    print("native_boolean_constraints=2")
    print("localized_javascript_checks=8")
    print("rsm_output_mode=last_expression")


if __name__ == "__main__":
    main()
