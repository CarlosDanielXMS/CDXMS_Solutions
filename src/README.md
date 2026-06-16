# CDXMS — Ecosystem Core Base v1.0.0

Base inicial do ecossistema CDXMS Solutions para MacroDroid.

## Capabilities incluídas

- `[CDXMS] Json Config Manager`
- `[CDXMS] Bootstrap`
- `[CDXMS] Registrar Resultado`
- `[CDXMS] Logger`

## Incremento — Logger v1.0.0

- Adicionada capability `logger`.
- Action Block `[CDXMS] Logger` em `capabilities/logger/macrodroid/`.
- Registros locais em JSON Lines por escopo e data.
- Operações: `log_event`, `log_result`, `log_error`, `get_log_status`.
- Dependências: JCM e Result Manager.
- Sem GitHub/CDN em runtime.
