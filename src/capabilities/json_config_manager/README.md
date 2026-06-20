# [CDXMS] Json Config Manager v1.0.0

Kernel primitivo de JSON/filesystem do ecossistema CDXMS com JCM JsonPath Engine v1.

## Responsabilidade

Esta capability executa somente o domínio descrito em seu contrato. A saída pública única é `Resultado`.

## Operações

- `ensure_core`
- `repair_core`
- `ensure_folder`
- `validate_json`
- `read_json`
- `exists`
- `write_json`
- `merge_json`
- `ensure_file`
- `backup_file`
- `delete_file`

## Dependências

Nenhuma capability obrigatória além do core.

## Distribuição

O export MacroDroid está em `macrodroid/[CDXMS]_Json_Config_Manager.ablock`. A importação continua manual até homologação específica de importação automática.

## Compatibilidade de booleanos do Magic Text

Flags internas reutilizadas por dicionário são armazenadas como texto canônico `true`/`false`. Entradas booleanas aceitam também as representações localizadas `Verdadeiro`/`Falso`, evitando falsos `PERMISSION_DENIED` em dispositivos configurados em português.
