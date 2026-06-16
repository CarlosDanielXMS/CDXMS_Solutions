# Corpo do Action Block — [CDXMS] Logger v1.0.0

## Entradas

- `Operation`: operação técnica (`log_event`, `log_result`, `log_error`, `get_log_status`).
- `Level`: severidade (`debug`, `info`, `warning`, `error`, `critical`).
- `Event Type`: classificação lógica do evento.
- `Message`: mensagem humana.
- `Source Artifact Type`: tipo do artifact de origem.
- `Source Artifact Id`: id técnico do artifact de origem.
- `Source Operation`: operação de origem.
- `Result Json`: resultado completo para `log_result`.
- `Data Json`: dados complementares do evento.
- `Error Json`: erro estruturado para `log_error`.
- `Tags Json`: tags em JSON.
- `Log Scope`: escopo do arquivo (`auto`, `events`, `results`, `errors`, `audit`, `runtime`).
- `Log File Name`: nome opcional do arquivo `.jsonl`.
- `Config Json`: configuração completa opcional do Logger.
- `Strict Mode?`: bloqueia JSON inválido nos campos estruturados quando `true`.
- `Session Id`: identificador de sessão.
- `Correlation Id`: identificador de correlação.

## Saída

- `Resultado`: dicionário conforme contrato universal CDXMS.

## Variáveis de trabalho

- `Tmp_LogWorkJson`: JSON temporário com plano de escrita.
- `Tmp_LogWork`: dicionário temporário com path, nome de arquivo, linha de log e payload de resultado.
- `Tmp_DependencyResult`: retorno temporário do JCM.

## Corpo passo a passo

### Grupo 01 — Prepare Log Entry

1. **JavaScript**
   - Engine: `JetPack JavascriptEngine`.
   - Saída: `Tmp_LogWorkJson`.
   - Responsabilidade: normalizar entradas, validar enums, montar `log_entry`, calcular `folder_path`, `file_name`, `log_line` e payload para o Result Manager.
   - Não executa I/O e não consulta GitHub/CDN.

2. **JSON Parse**
   - Entrada: `Tmp_LogWorkJson`.
   - Saída: `Tmp_LogWork`.
   - Responsabilidade: transformar o plano de escrita em dicionário consumível pelas ações nativas.

### Grupo 02 — Persist Log When Required

3. **If Condition**
   - Condição: `Tmp_LogWork[should_write] == true`.
   - Objetivo: impedir escrita para `get_log_status`.

4. **Action Block — [CDXMS] Json Config Manager**
   - `Operation`: `ensure_folder`.
   - `Folder Path`: `{lv=Tmp_LogWork[folder_path]}`.
   - Saída: `Tmp_DependencyResult`.
   - Objetivo: garantir pasta local de log antes do append.

5. **Write to File**
   - `All Files Path`: `{lv=Tmp_LogWork[folder_path]}`.
   - `Filename`: `{lv=Tmp_LogWork[file_name]}`.
   - `Text`: `{lv=Tmp_LogWork[log_line]}`.
   - `Append`: `true`.
   - `Overwrite`: `false`.
   - Objetivo: gravar uma linha JSONL append-only.

6. **End If**

### Grupo 03 — Publish Result

7. **Action Block — [CDXMS] Registrar Resultado**
   - `Operation`: `build_result`.
   - `Source Artifact Type`: `capability`.
   - `Source Artifact Id`: `logger`.
   - `Source Operation`: `{lv=Operation}`.
   - `Success?`: `{lv=Tmp_LogWork[success]}`.
   - `Status`: `{lv=Tmp_LogWork[status]}`.
   - `Message`: `{lv=Tmp_LogWork[result_message]}`.
   - `Data Json`: `{lv=Tmp_LogWork[data_json]}`.
   - `Error Json`: `{lv=Tmp_LogWork[error_json]}`.
   - Saída: `Resultado`.
   - Objetivo: publicar a saída pública única sem duplicar manualmente o contrato.

8. **Exit Action Block**
   - Encerramento explícito após publicação de `Resultado`.
