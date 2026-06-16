# [CDXMS] Logger v1.0.0

Capability de observabilidade local do ecossistema CDXMS.

O Logger registra eventos, resultados e erros em arquivos locais no formato JSON Lines, mantendo o padrão de saída pública única `Resultado` através do `[CDXMS] Registrar Resultado`.

## Responsabilidades

- Registrar eventos operacionais em `/logs/events/`.
- Registrar resultados em `/logs/results/`.
- Registrar erros em `/logs/errors/`.
- Retornar status calculado sem gravar arquivo quando `Operation = get_log_status`.
- Manter rastreabilidade com `Session Id` e `Correlation Id`.
- Não baixar nada do GitHub/CDN.
- Não instalar, registrar, atualizar ou remover artifacts.

## Dependências

- `[CDXMS] Json Config Manager >= 1.0.0` para garantir a pasta alvo antes da escrita.
- `[CDXMS] Registrar Resultado >= 1.0.0` para publicar a saída `Resultado`.

## Operações

- `log_event`
- `log_result`
- `log_error`
- `get_log_status`

## Armazenamento no dispositivo

```text
/storage/emulated/0/Documents/CDXMS_Solutions/logs/events/cdxms-events-YYYY-MM-DD.jsonl
/storage/emulated/0/Documents/CDXMS_Solutions/logs/results/cdxms-results-YYYY-MM-DD.jsonl
/storage/emulated/0/Documents/CDXMS_Solutions/logs/errors/cdxms-errors-YYYY-MM-DD.jsonl
```

Cada linha é um JSON completo e independente.

## Saneamento pré-release v1.0.0

A capability permanece na versão `1.0.0`. Este ajuste registra a auditoria de ações nativas, JS e Shell antes da primeira release oficial.

- Política: `native_first_when_safe_clear_and_homologated`.
- JS: `1` ocorrência(s).
- Shell: `0` ocorrência(s).
- Decisão: Mantém JCM para garantia de estrutura, WriteToFileAction para persistência e Result Manager para publicação; JavaScript fica restrito à montagem da linha JSONL e validação do payload.

