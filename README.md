# CDXMS — Artifact Manager Local Apply v1.0.0

Package incremental mesclado contendo todo o ecossistema atual e a evolução do Artifact Manager para aplicação local real controlada.

## Decisão

A aplicação física é permitida somente com double-gate:

```text
Dry Run? = false
Apply Changes? = true
```

Sem esses dois gates, o Artifact Manager continua retornando plano seguro.

## Escopo aplicado

- Criação de diretórios do artifact.
- Escrita de `manifest.json`, `contract.json` e `config.json`.
- Escrita/merge planejado de `core/registry.json` a partir do Registry Json informado.
- Escrita de runtime state.
- Escrita de install marker.

## Fora de escopo

- Download remoto.
- Importação automática de `.ablock`/`.macro` no MacroDroid.
- Rollback transacional completo.
