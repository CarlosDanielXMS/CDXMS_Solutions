# Changelog

## 1.1.0 incremental — Bootstrap

- Adicionada capability `[CDXMS] Bootstrap` v1.0.0.
- Bootstrap passa a depender do JCM `>=1.0.0`.
- Adicionadas operações `initialize_ecosystem`, `verify_core`, `repair_core`, `ensure_runtime`, `load_context` e `get_status`.
- Mantida saída pública única `Resultado`.
- Dados úteis permanecem em `Resultado.data`.
- Bootstrap não depende de GitHub/CDN e não executa lifecycle remoto.
- `remote_manifest.json` usa `base_raw_url` com `/src` e `target_path` sem `src/`.

## 1.0.0 final — JCM

- Adicionada JCM JsonPath Engine v1.
- Suporte a `config.services[id="x"].name`.
- Suporte a JsonPath canônico `$.items[?(@.id=="x")].name`.
- Suporte a `$`, wildcard, recursive descent, slice e union.
- `read_json` com Json Path vazio/$ retorna documento completo.
- `exists` passa a verificar Json Path quando informado.
- `write_json` e `merge_json` bloqueiam múltiplos matches.
- Resultado mantém `data` como dicionário oficial.
- Removidos campos top-level não padronizados do contrato.

## Bootstrap 1.0.0

- Adicionada capability `[CDXMS] Bootstrap`.
- Incluído export MacroDroid em `capabilities/bootstrap/macrodroid/[CDXMS]_Bootstrap.ablock`.
- Bootstrap usa o JCM para garantir core, runtime e contexto local.
- Mantida saída pública única `Resultado`.
- Sem dependência operacional de GitHub/CDN.
