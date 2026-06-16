# [CDXMS] Bootstrap — Corpo do Action Block v1.0.0

## Entradas

| Entrada | Tipo | Obrigatória | Descrição |
|---|---:|---:|---|
| `Operation` | Texto | Sim | Operação técnica: `initialize_ecosystem`, `verify_core`, `repair_core`, `ensure_runtime`, `load_context`, `get_status`. |
| `Requested Artifact Type` | Texto | Não | Tipo contextual: `core`, `capability`, `solution`, `package`, `catalog`. |
| `Requested Artifact Id` | Texto | Não | Id técnico contextual, como `json_config_manager`, `bootstrap` ou `solutions_manager`. |
| `Force Repair?` | Boolean | Não | Permite reparo explícito quando a operação for `repair_core`. |
| `Load Context?` | Boolean | Não | Carrega settings/registry/config contextual uma única vez. |
| `Config Json` | Texto JSON | Não | Config completa já carregada por orquestrador. Evita chamada ao JCM para config própria. |
| `Session Id` | Texto | Não | Identificador da sessão. |
| `Correlation Id` | Texto | Não | Identificador de correlação entre chamadas. |

## Saída

| Saída | Tipo | Descrição |
|---|---:|---|
| `Resultado` | Dicionário | Saída pública única. Dados úteis em `Resultado.data`. |

## Variáveis de trabalho

- `Tmp_Result`: dicionário interno antes da publicação em `Resultado`.
- `Tmp_JcmResult`: retorno de chamadas ao `[CDXMS] Json Config Manager`.
- `Tmp_Config`: config completa do Bootstrap, carregada uma única vez.
- `Tmp_Settings`: core/settings.json carregado completo.
- `Tmp_Registry`: core/registry.json carregado completo.
- `Tmp_ArtifactConfig`: config completa do artifact contextual, quando solicitado.
- `Tmp_Checks`: lista de verificações executadas.
- `Tmp_MissingFiles`: lista de arquivos obrigatórios ausentes.
- `Tmp_RuntimePaths`: lista de diretórios runtime/configurados.
- `Tmp_OperationValid`: flag booleana de validação da operação.

## Corpo passo a passo

### 01 — Initialize Runtime

1. **Action Group — `01 — Initialize Runtime`**
   - Objetivo: preparar variáveis de trabalho sem consultar rede ou artifact remoto.

2. **Set Variable**
   - Variável: `Tmp_Result`
   - Tipo: Dicionário
   - Valor inicial: `{}`
   - Observação: dicionário interno que será publicado em `Resultado` no final.

3. **Set Variable**
   - Variável: `Tmp_Checks`
   - Tipo: Lista
   - Valor inicial: `[]`

4. **Set Variable**
   - Variável: `Tmp_MissingFiles`
   - Tipo: Lista
   - Valor inicial: `[]`

5. **Set Variable**
   - Variável: `Tmp_RuntimePaths`
   - Tipo: Lista
   - Valor inicial baseado em `Config Json` quando informado; caso contrário, usar defaults de `capabilities/bootstrap/config.json` carregados pelo JCM no passo 03.

### 02 — Validate Operation

6. **If Clause**
   - Condição: `Operation` vazio
   - Ações internas:
     - montar `Resultado.success = false`
     - `Resultado.status = error`
     - `Resultado.error.code = MISSING_REQUIRED_INPUT`
     - `Resultado.message = A operação do Bootstrap não foi informada.`
     - **Exit Action Block**

7. **If / Else If**
   - Validar `Operation` contra:
     - `initialize_ecosystem`
     - `verify_core`
     - `repair_core`
     - `ensure_runtime`
     - `load_context`
     - `get_status`
   - Se não corresponder:
     - erro `UNSUPPORTED_OPERATION`
     - **Exit Action Block**

### 03 — Load Bootstrap Config Once

8. **If Clause**
   - Condição: `Config Json` não vazio
   - Ação: `JSON Parse`
     - Entrada: `Config Json`
     - Saída: `Tmp_Config`
   - Se falhar, retornar `INVALID_JSON`.

9. **Else**
   - **Action Block**
     - Action Block: `[CDXMS] Json Config Manager`
     - Bloquear próximas ações: Sim
     - Entradas:
       - `Operation = read_json`
       - `File Path = capabilities/bootstrap/config.json`
       - `Json Path = $`
     - Saída:
       - `Resultado -> Tmp_JcmResult`
   - **If Clause**
     - Se `Tmp_JcmResult.success = false`, propagar erro com `BOOTSTRAP_CONTEXT_LOAD_FAILED`.
   - **Set Variable**
     - `Tmp_Config = Tmp_JcmResult.data.value`

### 04 — Dispatch Operation

10. **If Clause** — `Operation = initialize_ecosystem`
    - Chamar branch `05 — Initialize Ecosystem`.

11. **Else If** — `Operation = verify_core`
    - Chamar branch `06 — Verify Core`.

12. **Else If** — `Operation = repair_core`
    - Chamar branch `07 — Repair Core`.

13. **Else If** — `Operation = ensure_runtime`
    - Chamar branch `08 — Ensure Runtime`.

14. **Else If** — `Operation = load_context`
    - Chamar branch `09 — Load Context`.

15. **Else If** — `Operation = get_status`
    - Chamar branch `10 — Get Status`.

### 05 — Initialize Ecosystem

16. **Action Group — `05 — Initialize Ecosystem`**

17. **Action Block — `[CDXMS] Json Config Manager`**
    - `Operation = ensure_core`
    - Saída: `Tmp_JcmResult`
    - Bloquear próximas ações: Sim

18. **If Clause**
    - Se `Tmp_JcmResult.success = false`, retornar `BOOTSTRAP_CORE_UNAVAILABLE` propagando `Tmp_JcmResult.error` em `Resultado.error.details.cause`.

19. Executar branch `08 — Ensure Runtime`.

20. Se `Load Context? = true`, executar branch `09 — Load Context`.

21. Montar sucesso:
    - `Resultado.success = true`
    - `Resultado.status = success`
    - `Resultado.message = Ecossistema CDXMS inicializado localmente com sucesso.`
    - `Resultado.data.bootstrap_status = ready`
    - `Resultado.data.core = Tmp_JcmResult.data`
    - `Resultado.data.runtime = dados da branch ensure_runtime`
    - `Resultado.data.context = contexto carregado quando aplicável`

### 06 — Verify Core

22. **Action Group — `06 — Verify Core`**

23. Para cada arquivo obrigatório em `Tmp_Config.settings.required_core_files`:
    - **Action Block — `[CDXMS] Json Config Manager`**
      - `Operation = exists`
      - `File Path = <arquivo>`
      - Saída: `Tmp_JcmResult`
    - Se não existir, adicionar item em `Tmp_MissingFiles`.

24. Montar resultado:
    - Se `Tmp_MissingFiles` vazio:
      - `success = true`, `status = success`, `bootstrap_status = ready`
    - Caso contrário:
      - `success = false`, `status = blocked`, `bootstrap_status = needs_repair`, `error.code = BOOTSTRAP_REPAIR_REQUIRED`

### 07 — Repair Core

25. **Action Group — `07 — Repair Core`**

26. Se `Force Repair? = false`, primeiro executar `verify_core`.
    - Se `verify_core` retornar ready, retornar sucesso sem reparo destrutivo.

27. **Action Block — `[CDXMS] Json Config Manager`**
    - `Operation = repair_core`
    - Saída: `Tmp_JcmResult`
    - Bloquear próximas ações: Sim

28. Se falhar, retornar `BOOTSTRAP_CORE_UNAVAILABLE`.

29. Executar `verify_core` novamente e retornar resultado consolidado.

### 08 — Ensure Runtime

30. **Action Group — `08 — Ensure Runtime`**

31. Para cada path em `Tmp_Config.settings.runtime_paths`:
    - **Action Block — `[CDXMS] Json Config Manager`**
      - `Operation = ensure_folder`
      - `Folder Path = <path>`
      - Saída: `Tmp_JcmResult`
    - Se algum falhar, retornar `BOOTSTRAP_RUNTIME_UNAVAILABLE`.

32. Garantir arquivos runtime mínimos via JCM `ensure_file`:
    - `runtime/last_result.json`
    - `runtime/locks.json`
    - `runtime/sessions.json`

33. Retornar `Resultado.data.runtime.created_paths`.

### 09 — Load Context

34. **Action Group — `09 — Load Context`**

35. **Action Block — `[CDXMS] Json Config Manager`**
    - `Operation = read_json`
    - `File Path = core/settings.json`
    - `Json Path = $`
    - Saída: `Tmp_JcmResult`

36. Salvar `Tmp_Settings = Tmp_JcmResult.data.value`.

37. **Action Block — `[CDXMS] Json Config Manager`**
    - `Operation = read_json`
    - `File Path = core/registry.json`
    - `Json Path = $`
    - Saída: `Tmp_JcmResult`

38. Salvar `Tmp_Registry = Tmp_JcmResult.data.value`.

39. Se `Requested Artifact Type` e `Requested Artifact Id` estiverem preenchidos:
    - montar path: `<type_plural>/<id>/config.json`
    - chamar JCM `read_json` com `Json Path = $`
    - salvar em `Tmp_ArtifactConfig` se existir.

40. Montar `Resultado.data.context` com:
    - `settings`
    - `registry`
    - `artifact_type`
    - `artifact_id`
    - `artifact_config`

### 10 — Get Status

41. **Action Group — `10 — Get Status`**

42. Executar `verify_core` sem reparar.

43. Ler `core/registry.json` completo usando JCM `read_json` com `$`.

44. Montar resumo:
    - `core_version`
    - `installed_capabilities`
    - `installed_solutions`
    - `bootstrap_status`

### 11 — Finalize Result

45. Garantir que `Resultado` tenha os campos top-level:
    - `schema_version`
    - `namespace`
    - `success`
    - `status`
    - `artifact_type`
    - `artifact_id`
    - `operation`
    - `message`
    - `data`
    - `error`
    - `meta`

46. **Exit Action Block**

## Observação de implementação

O export `.ablock` do Bootstrap deve ser criado no MacroDroid real, porque ele precisa referenciar o `[CDXMS] Json Config Manager` por `ActionBlockAction` com IDs internos válidos. Não gerar esse export manualmente sem testar importação e execução.
