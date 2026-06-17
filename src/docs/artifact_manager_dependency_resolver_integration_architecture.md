# Arquitetura — Artifact Manager + Dependency Resolver

## Decisão

A integração oficial usa orquestração direta: o Artifact Manager permanece responsável pelo lifecycle do artifact e consome o plano produzido pelo Dependency Resolver.

```text
Artifact Manager
  -> validate_artifact
  -> chama/recebe resultado do Dependency Resolver
  -> build_install_plan dependency-aware
  -> install_local_artifact em dry-run
```

## Dependency Resolver

O Dependency Resolver é puro/stateless. Ele recebe manifest, registry e catálogo, e retorna um `resolution_plan`. Ele não chama Artifact Manager, não escreve arquivos, não registra artifacts e não baixa conteúdo remoto.

## Artifact Manager

O Artifact Manager pode receber `Dependency Resolution Json`, geralmente serializado a partir do `Resultado` de `[CDXMS] Dependency Resolver.build_resolution_plan`. Esse JSON é incorporado ao `install_plan` como `dependency_resolution`.

## Regra de bloqueio

Quando `Dependency Resolution Json` indicar `blocked = true` e o Artifact Manager estiver em `Strict Mode? = true`, operações de plano/install retornam `status = blocked` com erro `DEPENDENCY_RESOLUTION_BLOCKED`.

## Sem Action Block intermediário

Não há `[CDXMS] Artifact Installer` nesta etapa. A criação de uma capability intermediária só será considerada futuramente caso o pipeline completo de instalação, download remoto, backup, apply e rollback cresça além do escopo natural do Artifact Manager.
