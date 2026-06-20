# CDXMS Solutions

Ecossistema modular de solutions e capabilities para MacroDroid.

A árvore operacional está em `src/`. Esta entrega mantém a versão pré-release `1.0.0`, consolida o Artifact Manager com apply via JCM e implementa o `[CDXMS] Remote Source Manager` para documentos JSON de controle via GitHub raw durante homologação em `develop`.

## Validação

```bash
python src/scripts/validate_remote_distribution_readiness_v1_0_0.py
python src/scripts/validate_am_local_apply_v1_0_0.py
python src/capabilities/remote_source_manager/scripts/validate_remote_source_manager_incremental.py
```

## Correção de homologação

Esta consolidação corrige o fluxo JavaScript do Remote Source Manager e a interpretação localizada de booleanos do JCM, mantendo a versão pré-release `1.0.0`.

## Base remota verificada

Esta consolidação parte do head remoto `feat/create-ecosystem-core` em `dcc8dba9460e54f519555d3d14a8d0c3f72d711c` e corrige exclusivamente os bridges de execução identificados na homologação real do RSM/JCM.


- O RSM mantém resultados de preflight como objeto (`pre_result`), sem JSON textual aninhado.
