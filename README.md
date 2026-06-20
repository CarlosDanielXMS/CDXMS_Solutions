# CDXMS Solutions

Ecossistema modular de solutions e capabilities para MacroDroid.

A árvore operacional está em `src/`. Esta entrega mantém a versão pré-release `1.0.0`, consolida o Artifact Manager com apply via JCM e implementa o `[CDXMS] Remote Source Manager` para documentos JSON de controle via GitHub raw durante homologação em `develop`.

## Validação

```bash
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
python src/scripts/validate_am_local_apply_v1_0_0.py
python src/capabilities/remote_source_manager/scripts/validate_remote_source_manager_incremental.py
```
