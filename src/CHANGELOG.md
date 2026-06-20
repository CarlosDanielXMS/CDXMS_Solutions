# Changelog

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
