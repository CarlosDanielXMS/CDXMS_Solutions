# CDXMS — AM/DR Concept Remodel v1.0.0

Package incremental mesclado contendo toda a base atual do ecossistema e a remodelagem conceitual entre Artifact Manager e Dependency Resolver.

## Decisão aplicada

- Não foi criado Action Block intermediário.
- `[CDXMS] Dependency Resolver` tornou-se uma capability pura/stateless e não depende mais do Artifact Manager.
- `[CDXMS] Artifact Manager` permanece como orquestrador de lifecycle e passa a aceitar `Dependency Resolution Json` para compor planos dependency-aware.
- A instalação física continua fora desta etapa; a homologação opera em dry-run.

## Arquivos principais

- `src/capabilities/artifact_manager/manifest.json`
- `src/capabilities/artifact_manager/contract.json`
- `src/capabilities/artifact_manager/macrodroid/[CDXMS]_Artifact_Manager.ablock`
- `src/capabilities/dependency_resolver/manifest.json`
- `src/docs/artifact_manager_dependency_resolver_integration_architecture.md`
- `src/homologation/am_dr_integration/macrodroid/[CDXMS]_Homologar_AM_DR_Integration_v1_0_0_TEMP.macro`
