# [CDXMS] String Utils v1.0.0

Capability pura para transformação, normalização, comparação e sanitização de textos no ecossistema CDXMS.

## Responsabilidade

A String Utils centraliza operações textuais comuns para evitar que cada capability implemente seu próprio escape, normalização, comparação ou sanitização.

Ela não acessa filesystem, não usa GitHub/CDN, não instala artifacts, não altera registry e não registra logs. A saída pública única é `Resultado`.

## Operações

- `escape_json_string`
- `unescape_json_string`
- `normalize_text`
- `normalize_id`
- `to_snake_case`
- `to_kebab_case`
- `trim`
- `collapse_whitespace`
- `replace_text`
- `contains_text`
- `equals_text`
- `starts_with`
- `ends_with`
- `is_blank`
- `sanitize_file_name`
- `sanitize_path_segment`
- `truncate`

## Dependência

- `[CDXMS] Registrar Resultado >= 1.0.0`

O Action Block chama o Result Manager ao final para publicar `Resultado` de forma padronizada.
