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
- `[CDXMS] File Integrity`

## Consolidação atual

- AM atua como planner/orchestrator de lifecycle.
- JCM é o executor oficial de filesystem/JSON.
- DR permanece puro/stateless.
- A estrutura remota usa uma única fonte oficial e `develop` como referência de integração pré-release.
- `catalogs/sources.json` e `catalogs/local_catalog.default.json` seguem a estrutura oficial.
- Remote manifests preservam schema v1 e campos existentes.
- Não há canais `stable/beta/dev` prematuros.
- O Remote Source Manager está homologado no dispositivo para transporte e validação de documentos JSON do plano de controle, com staging e verificação JCM.
- SHA-256 runtime foi homologado com `/system/bin/sha256sum` em contexto non-root sem Helper/Shizuku.
- `[CDXMS] File Integrity` encapsula cálculo e comparação SHA-256 e aguarda homologação própria.
- Download de payloads, instalação remota e importação automática continuam bloqueados.

## Validação

```bash
python src/capabilities/remote_source_manager/scripts/validate_remote_source_manager_incremental.py
python src/scripts/validate_rsm_jcm_runtime_bridge_v1_0_0.py
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
python src/capabilities/artifact_manager/scripts/validate_artifact_manager_incremental.py
python src/scripts/validate_am_local_apply_v1_0_0.py
python src/scripts/validate_sha256_runtime_probe_v1_0_1.py
python src/capabilities/file_integrity/scripts/validate_file_integrity_incremental.py
python src/scripts/validate_file_integrity_homologation_v1_0_0.py
```


## SHA-256 runtime — estado atual

- Harness temporário disponível em `tests/homologation/sha256_runtime/`.
- Executor homologado com `7/7` verificações.
- Capability `[CDXMS] File Integrity` implementada.
- Nenhum payload remoto foi habilitado.
- A integração RSM depende da homologação da capability de produção.
