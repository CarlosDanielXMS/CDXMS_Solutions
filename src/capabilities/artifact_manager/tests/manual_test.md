# Teste manual — [CDXMS] Artifact Manager v1.0.0

## Pré-requisito

Importar `[CDXMS] Artifact Manager` no MacroDroid.

## Teste 1 — validate_artifact

Entrada:

- Operation: `validate_artifact`
- Manifest Json:

```json
{"schema_version":1,"namespace":"CDXMS","artifact_type":"capability","capability":{"id":"demo_capability","version":"1.0.0","display_name":"[CDXMS] Demo"}}
```

Esperado:

- `Resultado.success = Verdadeiro`
- `Resultado.data.valid = Verdadeiro`

## Teste 2 — build_install_plan

Usar o mesmo manifest e `Operation = build_install_plan`.

Esperado:

- `Resultado.success = Verdadeiro`
- `Resultado.data.install_plan.files` preenchido.
