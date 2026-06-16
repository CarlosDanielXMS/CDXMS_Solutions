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

## Saneamento pré-release v1.0.0

A capability permanece na versão `1.0.0`. Este ajuste registra a auditoria de ações nativas, JS e Shell antes da primeira release oficial.

- Política: `native_first_when_safe_clear_and_homologated`.
- JS: `1` ocorrência(s).
- Shell: `0` ocorrência(s).
- Decisão: Mantém JavaScript centralizado porque o Action Block precisa suportar 17 operações por Operation e retornar Resultado homogêneo. TextManipulationAction será preferida em fluxos externos simples, mas dentro desta capability o script reduz duplicação e edge cases.

