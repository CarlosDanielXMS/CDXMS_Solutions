# [CDXMS] Artifact Manager v1.0.0

Capability responsável por validar artifacts CDXMS, calcular paths de destino, construir entradas de registry, gerar planos seguros de lifecycle local e orquestrar aplicação física **exclusivamente por meio do Json Config Manager**.

## Escopo v1.0.0

Esta versão consolida o Artifact Manager como planner/orchestrator de lifecycle. Ele não baixa arquivos remotos e não importa `.macro`/`.ablock` automaticamente no MacroDroid.

O AM não cria diretórios, não grava arquivos e não executa Shell como fluxo normal. Toda operação física deve ser feita pelo `[CDXMS] Json Config Manager`.

## Operações

- `validate_artifact`
- `get_artifact_status`
- `build_registry_entry`
- `build_install_plan`
- `build_jcm_apply_plan`
- `get_target_paths`
- `register_artifact`
- `unregister_artifact`
- `ensure_artifact_files`
- `install_local_artifact`
- `verify_local_apply`

## Saída

Saída pública única: `Resultado`.

## Integração com Dependency Resolver

O Artifact Manager é o orquestrador de lifecycle. Para planos dependency-aware, ele pode receber `Dependency Resolution Json`, preferencialmente produzido por `[CDXMS] Dependency Resolver.build_resolution_plan`, e incorporar esse resultado ao `install_plan`.

O Dependency Resolver permanece puro/stateless. Ele não instala, não grava e não depende do AM.

## Integração com Json Config Manager

O executor físico oficial é:

```text
json_config_manager
```

O AM gera:

```text
jcm_apply_plan
jcm_verification_plan
```

Esses planos descrevem as operações JCM necessárias, por exemplo:

```text
ensure_folder
write_json
merge_json
read_json
exists
backup_file
delete_file
```

O AM só pode considerar uma aplicação física como concluída quando a verificação pós-escrita confirmar:

```text
apply.should_apply = true
apply.applied = true
apply.verified = true
apply.executor = json_config_manager
```

## Gates de segurança

A aplicação só é elegível quando:

```text
Dry Run? = false
Apply Changes? = true
```

Sem esses dois gates, o AM retorna plano seguro e não deve executar efeito colateral.

## Exports MacroDroid

Arquivos `.ablock` e `.macro` são tratados como implementation artifacts. O AM pode planejar, validar e disponibilizar esses arquivos no filesystem, mas a importação automática dentro do MacroDroid permanece fora do escopo desta fase.

## GitHub remoto

A origem remota via GitHub fica fora desta capability. O fluxo futuro será:

```text
GitHub Distribution Layer
  -> baixa e valida catalog/package
  -> salva package/cache via JCM
Artifact Manager
  -> valida package local
  -> resolve/consome dependências
  -> gera plano de lifecycle
  -> aplica via JCM
  -> verifica e registra
```
