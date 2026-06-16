# Changelog

## 1.0.0 — String Utils

- Adicionada capability `[CDXMS] String Utils`.
- Adicionado contrato para escape/desescape JSON, normalização, comparação e sanitização textual.
- Adicionados enums e erros de String Utils ao core.
- Action Block exportado em `capabilities/string_utils/macrodroid/`.
- String Utils usa Result Manager para publicar `Resultado`.

## 1.0.0 — Logger

- Adicionada capability `[CDXMS] Logger`.
- Adicionado contrato para observabilidade local em JSON Lines.
- Adicionados enums e erros de Logger ao core.
- Action Block exportado em `capabilities/logger/macrodroid/`.
- Logger passa a usar JCM para garantir pasta local e Result Manager para publicar `Resultado`.

## 1.0.0 — Result Manager

- Adicionada capability `[CDXMS] Registrar Resultado`.
- Adicionado contrato para construção, normalização, validação e propagação de `Resultado`.
- Mantido padrão de saída pública única.
- Adicionados enums e erros de Result Manager ao core.
- Action Block exportado em `capabilities/result_manager/macrodroid/`.

## 1.0.0 final

- Adicionada JCM JsonPath Engine v1.
- Suporte a `config.services[id="x"].name`.
- Suporte a JsonPath canônico `$.items[?(@.id=="x")].name`.
- Suporte a `$`, wildcard, recursive descent, slice e union.
- `read_json` com Json Path vazio/$ retorna documento completo.
- `exists` passa a verificar Json Path quando informado.
- `write_json` e `merge_json` bloqueiam múltiplos matches.
- Resultado mantém `data` como dicionário oficial.
- Removidos campos top-level não padronizados do contrato.
