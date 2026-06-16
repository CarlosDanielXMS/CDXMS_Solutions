# Testes manuais — [CDXMS] Logger v1.0.0

## Pré-requisitos

1. Importar `[CDXMS] Json Config Manager`.
2. Importar `[CDXMS] Registrar Resultado`.
3. Importar `[CDXMS] Logger`.
4. Executar `[CDXMS] Bootstrap` com `initialize_ecosystem` pelo menos uma vez.

## Teste 1 — log_event

Entradas:

```text
Operation = log_event
Level = info
Event Type = bootstrap.started
Message = Bootstrap iniciado para teste.
Source Artifact Type = capability
Source Artifact Id = bootstrap
Source Operation = initialize_ecosystem
Data Json = {"test":true}
Tags Json = ["manual","logger"]
Log Scope = auto
```

Resultado esperado:

- `Resultado.success = true`.
- Arquivo criado/anexado em `logs/events/cdxms-events-YYYY-MM-DD.jsonl`.
- Última linha contém `log_type = log_event`.

## Teste 2 — log_error

Entradas:

```text
Operation = log_error
Level = error
Event Type = jcm.read_json.failed
Message = Falha simulada de leitura JSON.
Source Artifact Id = json_config_manager
Source Operation = read_json
Error Json = {"code":"FILE_NOT_FOUND","message":"Arquivo não encontrado."}
Log Scope = auto
```

Resultado esperado:

- `Resultado.success = true`.
- Arquivo criado/anexado em `logs/errors/cdxms-errors-YYYY-MM-DD.jsonl`.

## Teste 3 — get_log_status

Entradas:

```text
Operation = get_log_status
```

Resultado esperado:

- `Resultado.success = true`.
- Nenhuma escrita de arquivo deve ocorrer.
- `Resultado.data.supported_operations` contém `log_event`, `log_result`, `log_error`, `get_log_status`.
