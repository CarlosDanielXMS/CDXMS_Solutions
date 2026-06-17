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


## Integração com Dependency Resolver

O Artifact Manager é o orquestrador de lifecycle. Para planos dependency-aware, ele pode receber `Dependency Resolution Json`, preferencialmente produzido por `[CDXMS] Dependency Resolver.build_resolution_plan`, e incorporar esse resultado ao `install_plan`. Na v1.0.0, a execução continua segura em dry-run e sem instalação física real.


## Aplicação local controlada

A v1.0.0 passa a suportar aplicação física controlada para operações elegíveis (`register_artifact`, `unregister_artifact`, `ensure_artifact_files` e `install_local_artifact`). A aplicação só ocorre quando `Dry Run? = false` e `Apply Changes? = true`. Sem esses dois gates, o Artifact Manager retorna apenas plano seguro.

A aplicação cria/atualiza arquivos dentro do `Target Root Path`: manifest, contract, config, registry, runtime state e install marker, conforme a operação. A importação automática de `.ablock`/`.macro` no MacroDroid permanece fora do escopo.
