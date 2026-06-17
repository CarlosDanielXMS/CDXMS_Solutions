# CDXMS Core + Artifact Manager v1.0.0 — Incremental Merged Package

Este ZIP substitui o package anterior do Artifact Manager que havia sido gerado apenas como diferencial.

Aqui, **incremental** significa: base anterior completa + alterações novas mescladas.

## Conteúdo

- Core v1.0.0 homologado.
- Capabilities já existentes:
  - Json Config Manager
  - Bootstrap
  - Registrar Resultado
  - Logger
  - String Utils
- Nova capability:
  - Artifact Manager
- Documentação e scripts de validação atualizados.
- `release.json`, `checksums.json`, `core/enums.json` e `core/errors.json` mesclados corretamente.

## Validação

```bash
python src/scripts/validate_core_plus_artifact_manager_v1_0_0.py
python src/capabilities/artifact_manager/scripts/validate_artifact_manager_incremental.py
```
