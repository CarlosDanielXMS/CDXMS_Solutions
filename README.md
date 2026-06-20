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

Esta consolidação parte do head remoto `feat/create-ecosystem-core` em `aad55e5969b41c456bb92e096bde2c381101e385` e corrige exclusivamente os bridges de execução identificados na homologação real do RSM/JCM.

## Persistência da resposta HTTP confirmada no dispositivo

A base desta consolidação é o head remoto `feat/create-ecosystem-core` em `aad55e5969b41c456bb92e096bde2c381101e385`.

Um export mínimo criado e executado no MacroDroid confirmou que, no modo All Files Access, `saveResponseAllFilesAccessPath` deve conter o caminho completo do arquivo e `saveResponseFileName` deve permanecer vazio. O Remote Source Manager foi ajustado exclusivamente para esse contrato nativo.
