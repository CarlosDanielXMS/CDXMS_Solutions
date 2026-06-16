# CDXMS — JCM Final v1.0.0

Package completo do `[CDXMS] Json Config Manager`.

Principais entregas:

- Action Block final em `capabilities/json_config_manager/macrodroid/`.
- Contrato com saída única `Resultado`.
- JCM JsonPath Engine v1.
- Leitura completa de config/documento via Json Path vazio ou `$`.
- Bloqueio de escrita/merge com múltiplos alvos.
- Core mínimo e arquivos oficiais de contrato.

## Incremento — Result Manager v1.0.0

- Adicionada capability `result_manager`.
- Action Block `[CDXMS] Registrar Resultado` em `capabilities/result_manager/macrodroid/`.
- Operações: `build_result`, `normalize_result`, `validate_result`, `propagate_result`, `wrap_error`, `register_result`.
- Capability pura: sem GitHub, sem filesystem, sem JCM e sem efeitos colaterais.
