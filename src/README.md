# CDXMS — Ecosystem Core Base v1.0.0

Base completa e mesclada do ecossistema CDXMS Solutions.

## Capabilities incluídas

- `[CDXMS] Json Config Manager`
- `[CDXMS] Bootstrap`
- `[CDXMS] Registrar Resultado`
- `[CDXMS] Logger`
- `[CDXMS] String Utils`
- `[CDXMS] Artifact Manager`
- `[CDXMS] Dependency Resolver`
- `[CDXMS] Remote Source Manager`

## Consolidação atual

- AM atua como planner/orchestrator de lifecycle.
- JCM é o executor oficial de filesystem/JSON.
- DR permanece puro/stateless.
- A estrutura remota usa uma única fonte oficial e `develop` como referência de integração pré-release.
- `catalogs/sources.json` e `catalogs/local_catalog.default.json` seguem a estrutura oficial.
- Remote manifests preservam schema v1 e campos existentes.
- Não há canais `stable/beta/dev` prematuros.
- O Remote Source Manager está homologado no dispositivo para transporte e validação de documentos JSON do plano de controle, com staging e verificação JCM.
- Download de payloads, SHA-256 em runtime, instalação remota e importação automática continuam bloqueados até homologações específicas.

## Validação

```bash
python src/capabilities/remote_source_manager/scripts/validate_remote_source_manager_incremental.py
python src/scripts/validate_rsm_jcm_runtime_bridge_v1_0_0.py
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
python src/capabilities/artifact_manager/scripts/validate_artifact_manager_incremental.py
python src/scripts/validate_am_local_apply_v1_0_0.py
```
