# [CDXMS] Artifact Manager v1.0.0

Capability responsável por validar artifacts CDXMS, calcular paths de destino, construir entradas de registry e gerar planos seguros de lifecycle local.

## Escopo v1.0.0

Esta versão foca em validação, planejamento e contrato. Operações que seriam destrutivas ou persistentes retornam plano seguro por padrão, sem baixar arquivos remotos e sem importar `.macro`/`.ablock` automaticamente no MacroDroid.

## Operações

- `validate_artifact`
- `get_artifact_status`
- `build_registry_entry`
- `build_install_plan`
- `get_target_paths`
- `register_artifact`
- `unregister_artifact`
- `ensure_artifact_files`
- `install_local_artifact`

## Saída

Saída pública única: `Resultado`.
