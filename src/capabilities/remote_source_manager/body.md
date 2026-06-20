# Corpo do Action Block — [CDXMS] Remote Source Manager v1.0.0

## Entradas

| Entrada | Tipo | Obrigatória | Descrição |
|---|---|---:|---|
| Operation | Texto | Sim | `validate_source`, `get_source_status`, `fetch_catalog`, `fetch_release_manifest`, `fetch_remote_manifest` ou `fetch_json`. |
| Source Json | Texto JSON | Não | Fonte completa. Vazio usa `cdxms_official_github` em `develop`. |
| Source Id | Texto | Não | Id esperado da fonte. |
| Remote Path | Texto | Condicional | Path relativo dentro de `base_raw_url`. |
| Expected File Type | Texto | Não | `file_type` esperado em `fetch_json`. |
| Cache Root Path | Texto | Não | Staging dentro do base path CDXMS. |
| Timeout Seconds | Inteiro | Não | Timeout de 5 a 120 segundos. |
| Strict Mode? | Booleano | Não | Ativa bloqueio rigoroso. |
| Session Id | Texto | Não | Rastreabilidade. |
| Correlation Id | Texto | Não | Correlação entre chamadas. |

## Saída

| Saída | Tipo | Descrição |
|---|---|---|
| Resultado | Dicionário | Contrato universal CDXMS. |

## Variáveis de trabalho

- `Tmp_RequestWorkJson`
- `Tmp_RequestWork`
- `Tmp_HttpStatusCode`
- `Tmp_HttpHeaders`
- `Tmp_ResponseText`
- `Tmp_JcmEnsureFolderResult`
- `Tmp_JcmReadResult`
- `Tmp_ShouldRequestText`
- `Tmp_RequestUrl`
- `Tmp_StagingFolderPath`
- `Tmp_StagingFileName`
- `Tmp_StagingFilePath`
- `Tmp_JcmReadResultJson`
- `Tmp_ResultJson`

## Corpo passo a passo

### Grupo 01 — Prepare Remote Request

1. **Action Group — 01 — Prepare Remote Request**
   - Agrupa preflight e montagem da requisição.

2. **JavaScript — Validar fonte e montar request**
   - Engine: `JetPack JavascriptEngine`.
   - Bloquear próximas ações: `true`.
   - Saída: `Tmp_RequestWorkJson`.
   - Valida `Operation`.
   - Carrega `Source Json` ou a fonte oficial default.
   - Exige `source.type = github_raw`.
   - Valida `repository`, `ref`, `https://raw.githubusercontent.com/` e bloqueia `/blob/`.
   - Valida `Remote Path` relativo, sem `..`, URL completa, query, fragmento, barra invertida ou espaço não escapado.
   - Limita a v1.0.0 a `.json` de controle.
   - Valida `Cache Root Path` dentro de `/storage/emulated/0/Documents/CDXMS_Solutions/`.
   - Normaliza timeout para 30 quando fora de 5–120.
   - Monta URL, pasta e arquivo de staging.
   - Para operações sem rede, já monta o Resultado final em `pre_result_json`.

3. **JSON Parse — Tmp_RequestWorkJson → Tmp_RequestWork**
   - Publica o contexto estruturado para diagnóstico.

4. **JavaScript — Materializar ponte escalar**
   - Extrai `should_request`, URL, pasta, nome e caminho do staging para variáveis de texto.
   - Evita dependência de chaves aninhadas de dicionário em ações nativas.

5. **Action Group End**

### Grupo 02 — Execute HTTP Download

6. **Action Group — 02 — Execute HTTP Download**

7. **Action Block — [CDXMS] Json Config Manager**
   - Executa somente quando `Tmp_RequestWork.should_request = true`.
   - Operation: `ensure_folder`.
   - Folder Path: `Tmp_RequestWork.staging.folder_path`.
   - Bloquear próximas ações: `true`.
   - Saída: `Tmp_JcmEnsureFolderResult`.

8. **HTTP Request — Baixar documento remoto para staging**
   - Executa somente quando `should_request = true`.
   - Método: `GET` (`requestType = 0`).
   - URL: `Tmp_RequestWork.request.url`.
   - Headers:
     - `Accept: application/json`;
     - `User-Agent: CDXMS-Remote-Source-Manager/1.0.0`.
   - Follow redirects: `true`.
   - Allow any certificate: `false`.
   - Proxy/basic auth/client certificate: desabilitados.
   - Timeout: 30 segundos no export inicial.
   - Block next action: `true`.
   - Save response: arquivo temporário com All Files Access.
   - Pasta: `Tmp_RequestWork.staging.folder_path`.
   - Arquivo: `Tmp_RequestWork.staging.file_name`.
   - Código HTTP: `Tmp_HttpStatusCode`.
   - Headers de resposta: `Tmp_HttpHeaders`.

9. **Read File — Ler resposta temporária**
   - Executa quando `should_request = true` e HTTP status = 200.
   - All Files Access Path: `Tmp_RequestWork.staging.file_path`.
   - Saída: `Tmp_ResponseText`.


10. **Action Block — [CDXMS] Json Config Manager**
    - Operation: `read_json`.
    - File Path: `Tmp_RequestWork.staging.file_path`.
    - Json Path: `$`.
    - Executa após HTTP 200 e resposta não vazia.
    - Saída: `Tmp_JcmReadResult`.
    - Confirma que o staging é JSON legível pelo executor oficial.

12. **JSON Output — Serializar verificação JCM**
   - Converte `Tmp_JcmReadResult` em `Tmp_JcmReadResultJson`.

13. **Action Group End**

### Grupo 03 — Finalize Result

14. **Action Group — 03 — Finalize Result**

15. **JavaScript — Consolidar Resultado remoto**
    - Engine: `JetPack JavascriptEngine`.
    - Bloquear próximas ações: `true`.
    - Saída: `Tmp_ResultJson`.
    - Valida status 200.
    - Valida `schema_version = 1` e `namespace = CDXMS`.
    - Valida `file_type`/`artifact_type` conforme operação.
    - Exige `Tmp_JcmReadResult.success = true`.
    - Retorna apenas resumo e path de staging; o documento completo permanece no arquivo validado.
    - Não declara checksum como verificado nesta fase.

16. **JSON Parse — Tmp_ResultJson → Resultado**
    - Publica a única saída oficial.

17. **Action Group End**

18. **Exit Action Block**
    - Encerra explicitamente a capability.

## Limitações deliberadas

- O export usa `HTTP Request` nativo, não `curl`.
- O timeout dinâmico é validado no contexto, porém o export inicial mantém 30 s na ação HTTP; evolução dinâmica depende de homologação do campo no dispositivo.
- SHA-256 não é declarado como validado, pois o catálogo nativo auditado não expõe ação de checksum. Payloads críticos permanecem bloqueados.
- A v1.0.0 não baixa em lote nem instala artifacts.

- Os JavaScripts de preflight/finalização usam IIFE com retorno explícito para evitar `Illegal return statement`.
