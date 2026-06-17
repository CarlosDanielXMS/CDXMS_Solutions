# Teste manual — Artifact Manager v1.0.0 local apply

## Cenário seguro

Use `Target Root Path` apontando para uma área de homologação:

```text
/storage/emulated/0/Documents/CDXMS_Solutions/runtime/homologation/am_local_apply
```

## Teste 1 — Dry-run

- `Operation = install_local_artifact`
- `Dry Run? = true`
- `Apply Changes? = false`

Esperado: `success = true`, `data.install_plan.side_effects_enabled = false`, sem arquivos obrigatórios criados pelo AM.

## Teste 2 — Aplicação controlada

- `Operation = install_local_artifact`
- `Dry Run? = false`
- `Apply Changes? = true`

Esperado: `success = true`, `data.apply.should_apply = true`, e arquivos criados sob o `Target Root Path` de homologação:

```text
capabilities/<artifact_id>/manifest.json
capabilities/<artifact_id>/contract.json
capabilities/<artifact_id>/config.json
core/registry.json
runtime/capabilities/<artifact_id>.state.json
packages/installed/capabilities/<artifact_id>/install_manifest.json
```
