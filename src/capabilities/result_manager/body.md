# Corpo do Action Block — [CDXMS] Registrar Resultado v1.0.0

## Entradas

| Entrada | Tipo | Descrição | Exemplos / opções |
|---|---:|---|---|
| Operation | Texto | Operação técnica do Result Manager. | `build_result`, `normalize_result`, `validate_result`, `propagate_result`, `wrap_error`, `register_result` |
| Source Artifact Type | Texto | Tipo do artifact de origem. | `capability`, `solution`, `core` |
| Source Artifact Id | Texto | Id técnico do artifact de origem. | `bootstrap`, `json_config_manager`, `result_manager` |
| Source Operation | Texto | Operação original que será registrada. | `read_json`, `initialize_ecosystem` |
| Success? | Booleano | Sucesso lógico para construção direta. | `true`, `false` |
| Status | Texto | Status padronizado. Se vazio, deriva de Success?. | `success`, `error`, `blocked` |
| Message | Texto | Mensagem humana em português. | `Operação executada com sucesso.` |
| Data Json | Texto JSON | Objeto para `Resultado.data`. | `{}`, `{"file_path":"core/settings.json"}` |
| Error Json | Texto JSON/null | Erro estruturado. | `null`, `{"code":"INVALID_JSON","message":"JSON inválido."}` |
| Result Json | Texto JSON | Resultado bruto para normalização/validação/propagação. | `{...}` |
| Context Json | Texto JSON | Contexto adicional opcional. | `{"caller":"bootstrap"}` |
| Strict Mode? | Booleano | Bloqueia campos de topo proibidos e contrato inválido. | `true`, `false` |
| Include Raw Result? | Booleano | Inclui resultado bruto em modo debug. | `true`, `false` |
| Session Id | Texto | Sessão para `meta.session_id`. | `session-001` |
| Correlation Id | Texto | Correlação para `meta.correlation_id`. | `corr-001` |

## Saída

| Saída | Tipo | Descrição |
|---|---:|---|
| Resultado | Dicionário | Saída pública única conforme contrato CDXMS. |

## Variáveis de trabalho

| Variável | Tipo | Descrição |
|---|---:|---|
| Tmp_ResultJson | Texto | JSON textual interno publicado em `Resultado` via JSON Parse. |

## Corpo passo a passo

### Ação 1 — Action Group

- Nome/comentário: `01 — Build/Normalize/Validate Result`
- Objetivo: agrupar toda a lógica pura de resultado.

### Ação 2 — JavaScript

- Engine: JavaScript padrão do MacroDroid.
- Saída string: `Tmp_ResultJson`
- Objetivo: validar entradas, executar dispatch por `Operation` e gerar JSON final do contrato CDXMS.
- Observação: o script sempre retorna JSON válido para ser parseado na ação seguinte.

### Ação 3 — JSON Parse

- Entrada: `Tmp_ResultJson`
- Saída: `Resultado`
- `dictionaryKeys`: raiz vazia.
- Objetivo: publicar o resultado final como dicionário público único.

### Ação 4 — Action Group End

- Fecha o grupo lógico.

### Ação 5 — Exit Action Block

- Encerra explicitamente a capability após publicar `Resultado`.
