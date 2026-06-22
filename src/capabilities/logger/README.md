# [CDXMS] Logger v1.0.0

Capability de observabilidade local para registrar eventos, resultados e erros em JSON Lines.

## Responsabilidade

Esta capability executa somente o domínio descrito em seu contrato. A saída pública única é `Resultado`.

## Operações

- `log_event`
- `log_result`
- `log_error`
- `get_log_status`

## Dependências

{"json_config_manager": ">=1.0.0", "result_manager": ">=1.0.0"}

## Distribuição

O export MacroDroid está em `macrodroid/[CDXMS]_Logger.ablock`. A importação continua manual até homologação específica de importação automática.
