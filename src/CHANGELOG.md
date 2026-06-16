# Changelog

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
