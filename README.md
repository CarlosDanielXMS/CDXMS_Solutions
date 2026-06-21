# CDXMS Solutions

Ecossistema modular de solutions e capabilities para MacroDroid.

A árvore operacional está em `src/`. Esta entrega mantém a versão pré-release `1.0.0`, consolida o Artifact Manager com apply via JCM e formaliza a homologação do `[CDXMS] Remote Source Manager` para documentos JSON do plano de controle via GitHub raw.

## Estado desta consolidação

- Remote Source Manager v1.0.0: **homologado no dispositivo para o plano de controle remoto**;
- macro de evidência: `[CDXMS] Homologar Remote Source Manager v1.0.6 TEMP`;
- resultado: `23/23` verificações aprovadas;
- source ref exercitado: `aad55e5969b41c456bb92e096bde2c381101e385`;
- head remoto na formalização: `d79fa8cbed54048900fcb12fcb873408b7a70478`;
- payloads de artifacts e validação SHA-256 em runtime permanecem fora do escopo homologado.

## Validação

```bash
python src/capabilities/remote_source_manager/scripts/validate_remote_source_manager_incremental.py
python src/scripts/validate_rsm_jcm_runtime_bridge_v1_0_0.py
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
python src/scripts/validate_am_local_apply_v1_0_0.py
```

## Evidência de runtime

A homologação confirmou no MacroDroid real:

- `validate_source` e `get_source_status` sem acesso à rede;
- bloqueios de host, `/blob/`, fonte desabilitada, `Source Id` divergente, traversal e JSON inválido;
- HTTP `200` com persistência física no staging;
- releitura do JSON pelo `[CDXMS] Json Config Manager`;
- HTTP `404` tratado como `HTTP_UNEXPECTED_STATUS`;
- ausência de alteração no registry;
- contrato All Files Access com caminho completo em `saveResponseAllFilesAccessPath` e `saveResponseFileName` vazio.
