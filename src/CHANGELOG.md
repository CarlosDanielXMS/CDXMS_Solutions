# Changelog

## 1.0.0 — Correções de homologação RSM/JCM

- Mantida versão pré-release `1.0.0`.
- Corrigido `Illegal return statement` no preflight do Remote Source Manager.
- Finalização do RSM agora retorna explicitamente o Resultado em todos os fluxos.
- Mantida ponte escalar para URL e paths usados pelas ações nativas.
- JCM passa a serializar flags internas como `true`/`false`, evitando localização `Verdadeiro`/`Falso` e falsos `PERMISSION_DENIED`.
- Adicionadas validações regressivas para esses dois pontos.

## 1.0.0 — Remote Source Manager

- Mantida versão pré-release `1.0.0`.
- Implementado `[CDXMS] Remote Source Manager` com HTTP Request nativo.
- Adicionadas operações de validação de fonte, status, catálogo, release manifest, remote manifest e JSON de controle.
- Downloads passam primeiro por staging em `packages/downloaded/remote_source_manager/`.
- Código HTTP e headers são capturados; schema, namespace e identidade são validados.
- Staging é relido/verificado pelo Json Config Manager.
- Nenhuma instalação, alteração de registry ou apply final é executada pela capability.
- Bulk payload download e checksum SHA-256 em runtime permanecem bloqueados até homologação específica, evitando falso senso de integridade.

## 1.0.0 — Remote distribution readiness corrigida

- Mantida versão pré-release `1.0.0`.
- Package reconstruído como base completa mesclada, não delta.
- Artifact Manager consolidado para apply físico exclusivamente via JCM.
- Remote manifests padronizados sem quebra do schema v1.
- Adicionados `catalogs/sources.json` e `catalogs/local_catalog.default.json`.
- Homologação remota definida em `develop`.
- `release.json` preserva `artifacts[].path` e adiciona `remote_manifest_path`.
- Removida a proposta prematura de três canais e múltiplos catálogos paralelos.
- Mantida distribuição por arquivos raw individuais; ZIP remoto e importação automática permanecem fora de escopo.

## 1.0.0 — Base anterior

- JCM, Bootstrap, Result Manager, Logger e String Utils.
- Artifact Manager e Dependency Resolver.
- Contrato universal `Resultado`.
- Auditoria e validações pré-release.
