# Artifact Manager — Arquitetura Consolidada v1.0.0

## Status

Este documento consolida o Artifact Manager após a decisão arquitetural de remover Shell como executor normal de lifecycle e delegar todo filesystem/JSON ao Json Config Manager.

## Decisão central

```text
Artifact Manager = planner/orchestrator de lifecycle
Json Config Manager = executor físico de filesystem/JSON
Dependency Resolver = resolvedor puro/stateless
Solutions Manager = macro permanente de entrada, bootstrap e orquestração do usuário
GitHub Distribution Layer = origem remota/cache de packages
```

O Artifact Manager não cria arquivos, não cria diretórios e não executa Shell como caminho normal.

## Objetivo

O AM deve:

- validar artifacts;
- calcular paths;
- construir registry entry;
- montar plano de instalação;
- montar plano de apply via JCM;
- montar plano de verificação pós-escrita;
- bloquear falso sucesso físico;
- retornar Resultado universal;
- manter compatibilidade com origem local e futura origem GitHub.

## Fora de escopo

- Download remoto direto.
- Importação automática de `.macro` e `.ablock` no MacroDroid.
- UI do Manager.
- Resolver dependências com side effects.
- Criar Action Block intermediário de instalação.

## Fluxo local

```text
Entrada
  -> AM valida operation/artifact
  -> AM consome dependency_resolution opcional
  -> AM monta install_plan
  -> AM monta jcm_apply_plan
  -> AM monta jcm_verification_plan
  -> Orquestrador executa plano usando JCM
  -> Orquestrador executa verificação usando JCM
  -> AM/Manager consolida estado instalado/registrado/verificado
```

## Fluxo futuro com GitHub

```text
Solutions Manager
  -> GitHub Distribution Layer
      -> baixa release/catalog/package
      -> valida HTTP/status/JSON/checksum
      -> salva cache/package via JCM
  -> Artifact Manager
      -> valida package local
      -> calcula lifecycle
      -> aplica via JCM
      -> verifica via JCM
      -> registra
```

## Contrato de apply

`apply.should_apply` só fica verdadeiro quando:

- operação é elegível;
- `Dry Run? = false`;
- `Apply Changes? = true`;
- artifact está válido;
- dependências não bloquearam o fluxo.

Mesmo com `should_apply = true`, o AM não pode marcar `applied=true` nem `verified=true` sem evidência de execução/verificação JCM.

## Critério de sucesso físico

```text
apply.should_apply = true
apply.applied = true
apply.verified = true
apply.executor = json_config_manager
```

## Anti-patterns bloqueados

- Plano gerado como se fosse instalação.
- `success=true` com `verified=false` em operação física.
- Shell como executor normal do AM.
- Dependency Resolver gravando arquivos.
- Manager baixando remoto e escrevendo em produção sem cache/validação.


## Entrada única

A arquitetura v1 não usa uma macro Installer separada. `[CDXMS] Solutions Manager` incorpora o runtime mínimo necessário, executa Bootstrap na primeira abertura e atua como manager nas execuções seguintes.

O Artifact Manager permanece interno e não deve ser chamado diretamente pelo usuário. Ele recebe somente artifacts locais ou staged_verified e continua proibido de declarar instalação sem apply e verificação JCM.
