from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


COMMON_KEYS = {
    "disableLogging",
    "m_SIGUID",
    "m_classType",
    "m_comment",
    "m_constraintList",
    "m_isDisabled",
    "m_isOrCondition",
}


def build_catalog(source: Path) -> dict:
    document = json.loads(source.read_text(encoding="utf-8-sig"))
    macro = document["macro"]
    triggers = macro.get("m_triggerList", [])
    occurrences = Counter(item["m_classType"] for item in triggers)
    parameters: dict[str, set[str]] = defaultdict(set)
    comments: dict[str, set[str]] = defaultdict(set)

    for trigger in triggers:
        class_type = trigger["m_classType"]
        parameters[class_type].update(set(trigger) - COMMON_KEYS)
        comment = str(trigger.get("m_comment", "")).strip()
        if comment:
            comments[class_type].add(comment)

    edited_at = datetime.fromtimestamp(
        macro.get("lastEditedTimestamp", 0) / 1000,
        tz=timezone.utc,
    ).isoformat()
    entries = [
        {
            "class_type": class_type,
            "occurrences": occurrences[class_type],
            "parameter_keys": sorted(parameters[class_type]),
            "comments": sorted(comments[class_type]),
        }
        for class_type in sorted(occurrences)
    ]
    return {
        "schema_version": 1,
        "namespace": "CDXMS",
        "file_type": "macrodroid_native_trigger_catalog",
        "catalog_version": "0.1.0",
        "source": {
            "file_name": re.sub(r"^\d+-", "", source.name),
            "macro_name": macro.get("m_name", ""),
            "macro_export_version": document.get("macroExportVersion"),
            "last_edited_at_utc": edited_at,
            "macrodroid_version_context": "5.67.x",
            "complete": False,
            "completeness_note": "Snapshot de referência fornecido pelo projeto; não representa garantia de cobertura total da versão.",
        },
        "summary": {
            "trigger_instances": len(triggers),
            "unique_trigger_classes": len(occurrences),
        },
        "triggers": entries,
    }


def render_markdown(catalog: dict) -> str:
    source = catalog["source"]
    summary = catalog["summary"]
    lines = [
        "# CDXMS — Catálogo de Estruturas de Gatilhos MacroDroid v0.1",
        "",
        "## Escopo",
        "",
        f"Catálogo estrutural extraído de `{source['file_name']}`, editado em "
        f"`{source['last_edited_at_utc']}`, no contexto do MacroDroid "
        f"`{source['macrodroid_version_context']}`.",
        "",
        f"- instâncias analisadas: **{summary['trigger_instances']}**;",
        f"- classes nativas únicas: **{summary['unique_trigger_classes']}**;",
        "- cobertura: parcial; o arquivo-fonte não contém necessariamente todos os gatilhos da versão.",
        "",
        "Este catálogo registra a forma serializada observada. Ele não substitui a documentação do MacroDroid nem autoriza gerar exports sem homologação no aplicativo.",
        "",
        "## Regras de uso no CDXMS",
        "",
        "1. Preferir gatilho nativo antes de polling, UI Interaction ou loop permanente.",
        "2. Confirmar disponibilidade e permissões na versão/dispositivo alvo.",
        "3. Documentar debounce, duplicação, timeout e retomada após reboot quando aplicáveis.",
        "4. Tratar valores recebidos como entrada não confiável, especialmente Intents, webhooks, notificações e conteúdo de tela.",
        "5. Usar constraints no ponto mais próximo do gatilho sem duplicar validações de domínio.",
        "",
        "## Inventário estrutural",
        "",
        "| Classe interna | Instâncias | Parâmetros específicos observados |",
        "|---|---:|---|",
    ]
    for item in catalog["triggers"]:
        parameters = ", ".join(f"`{key}`" for key in item["parameter_keys"]) or "—"
        lines.append(
            f"| `{item['class_type']}` | {item['occurrences']} | {parameters} |"
        )
    lines.extend(
        [
            "",
            "## Atualização",
            "",
            "Regere o catálogo sempre que um novo export de referência for coletado:",
            "",
            "```bash",
            "python src/scripts/generate_macrodroid_trigger_catalog.py All_triggers.macro src/docs",
            "```",
            "",
            "Toda diferença deve ser revisada como mudança de implementação interna do MacroDroid, não como contrato estável da plataforma.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    catalog = build_catalog(args.source)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "macro_droid_trigger_catalog_v0_1.json"
    md_path = args.output_dir / "macro_droid_trigger_catalog_v0_1.md"
    json_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(catalog), encoding="utf-8")
    print(
        f"Trigger catalog: OK ({catalog['summary']['trigger_instances']} instances, "
        f"{catalog['summary']['unique_trigger_classes']} classes)"
    )


if __name__ == "__main__":
    main()
