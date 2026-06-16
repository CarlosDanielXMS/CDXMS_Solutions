# Aplicação — CDXMS Core Capabilities v1.0.0 Final Sanitized

Este pacote deve ser aplicado sobre a pasta `src/` do repositório `CarlosDanielXMS/CDXMS_Solutions`, branch `feat/create-ecosystem-core`.

## Importante

As versões permanecem `1.0.0`. Este é um saneamento pré-release, não um patch público.

## Passos

1. Copiar o conteúdo da pasta `src/` deste pacote sobre a pasta `src/` do repositório.
2. Executar:

```bash
python src/scripts/validate_core_capabilities_v1_0_0_sanitized.py
```

3. Conferir `src/docs/pre_release_capability_sanitization_report.md`.
4. Importar os `.ablock` no MacroDroid real.
5. Executar os testes manuais de cada capability.

## Capabilities incluídas

- json_config_manager
- bootstrap
- result_manager
- logger
- string_utils
