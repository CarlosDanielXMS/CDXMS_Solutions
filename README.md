# CDXMS Bootstrap v1.0.0 — Pacote Incremental

Este pacote foi gerado para ser aplicado **sobre a branch remota existente**:

```text
CarlosDanielXMS/CDXMS_Solutions
branch: feat/create-ecosystem-core
raiz distribuível: src/
```

Ele não recria a base do repositório e não duplica o JCM. Ele adiciona a capability `bootstrap` e atualiza apenas os arquivos compartilhados necessários.

## Aplicação esperada

Copiar o conteúdo de `src/` deste pacote para a pasta `src/` do repositório.

Arquivos novos:

```text
src/capabilities/bootstrap/**
src/docs/bootstrap_architecture.md
```

Arquivos compartilhados atualizados:

```text
src/core/enums.json
src/core/errors.json
src/README.md
src/CHANGELOG.md
src/release.json
src/checksums.json
```

## Observação importante

O export `.ablock` final do Bootstrap ainda deve ser criado no MacroDroid real, porque precisa referenciar o JCM via `ActionBlockAction` com IDs internos válidos.
