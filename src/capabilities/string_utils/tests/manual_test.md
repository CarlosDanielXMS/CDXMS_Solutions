# Testes manuais — [CDXMS] String Utils v1.0.0

Importe primeiro `[CDXMS] Registrar Resultado` e depois `[CDXMS] String Utils`.

## Teste 1 — escape_json_string

Entradas:

- Operation: `escape_json_string`
- Text: `linha 1
"teste"`

Esperado:

- `Resultado.success = true`
- `Resultado.data.value` contém o texto escapado sem aspas externas
- `Resultado.data.quoted_value` contém uma string JSON válida entre aspas

## Teste 2 — normalize_id

Entradas:

- Operation: `normalize_id`
- Text: `  Json Config Manager!!!  `

Esperado:

- `Resultado.data.value = json_config_manager`

## Teste 3 — to_kebab_case

Entradas:

- Operation: `to_kebab_case`
- Text: `Olá Mundo CDXMS`

Esperado:

- `Resultado.data.value = ola-mundo-cdxms`

## Teste 4 — contains_text normalizado

Entradas:

- Operation: `contains_text`
- Text: `Configuração do Usuário`
- Search Text: `configuracao`
- Comparison Mode: `normalized`

Esperado:

- `Resultado.data.value = true`

## Teste 5 — sanitize_file_name

Entradas:

- Operation: `sanitize_file_name`
- Text: `arquivo: inválido?.json`

Esperado:

- `Resultado.data.value` sem caracteres inválidos como `:` e `?`

## Teste 6 — erro de operação

Entradas:

- Operation: `operacao_inexistente`

Esperado:

- `Resultado.success = false`
- `Resultado.error.code = UNSUPPORTED_OPERATION`
