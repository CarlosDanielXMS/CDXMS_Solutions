# Teste Manual — [CDXMS] Bootstrap v1.0.0

## Pré-condição

- `[CDXMS] Json Config Manager` importado e validado.
- Estrutura JCM v1.0.0 aplicada em `src/` no repositório e no dispositivo sem `src/`.

## Teste 1 — initialize_ecosystem

Entradas:

```text
Operation = initialize_ecosystem
Load Context? = true
```

Esperado:

```text
Resultado.success = true
Resultado.status = success
Resultado.data.bootstrap_status = ready
Resultado.data.core preenchido
Resultado.data.runtime preenchido
Resultado.data.context.settings preenchido
Resultado.data.context.registry preenchido
```

## Teste 2 — verify_core

Entradas:

```text
Operation = verify_core
```

Esperado quando core íntegro:

```text
Resultado.success = true
Resultado.data.bootstrap_status = ready
Resultado.data.missing_files = []
```

## Teste 3 — load_context para capability

Entradas:

```text
Operation = load_context
Requested Artifact Type = capability
Requested Artifact Id = json_config_manager
```

Esperado:

```text
Resultado.success = true
Resultado.data.context.settings preenchido
Resultado.data.context.registry preenchido
Resultado.data.context.artifact_config preenchido quando config local existir
```

## Teste 4 — get_status

Entradas:

```text
Operation = get_status
```

Esperado:

```text
Resultado.success = true
Resultado.data.bootstrap_status em ready/needs_repair/partial
Resultado.data.installed_capabilities presente
Resultado.data.installed_solutions presente
```
