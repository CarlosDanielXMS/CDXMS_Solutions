# Corpo do Action Block — [CDXMS] JUIF UI Builder v1.0.0

## Objetivo

Validar e transformar um schema declarativo de UI, combinado com um JSON de configuração, em um contrato JUIF normalizado e compatível com o `[CDXMS] Java UI Framework`.

## Tipo

Capability pura. Não grava arquivos, não altera variáveis globais, não exibe UI e não acessa rede.

## Entradas

| Entrada | Tipo | Obrigatória | Valor padrão | Descrição |
|---|---|---:|---|---|
| `Config Json` | Texto/JSON | Sim | JSON de demonstração | Valores usados para hidratar propriedades declaradas por `bind`. |
| `UI Schema Json` | Texto/JSON | Sim | Schema canônico | Schema multipágina com `state`, `pages`, sections, fields, lists, components, actions e `shell`. |
| `Escape Json` | Booleano | Não | `true` | Define se `juif_ui_json_escaped` recebe o JSON escapado ou o mesmo valor cru. |

## Saída

| Saída | Tipo | Descrição |
|---|---|---|
| `Resultado` | Dicionário | Saída pública única no contrato universal CDXMS. |

Em sucesso, `Resultado.data` contém:

```text
juif_ui_json
juif_ui_json_escaped
mapping_json
component_catalog_version
supported_components
supported_component_count
```

## Variáveis de trabalho

| Variável | Tipo | Descrição |
|---|---|---|
| `Tmp_ConfigEscapeResult` | Dicionário | Resultado da `String Utils` ao escapar `Config Json`. |
| `Tmp_SchemaEscapeResult` | Dicionário | Resultado da `String Utils` ao escapar `UI Schema Json`. |
| `Tmp_CoreResultJson` | Texto | Resultado intermediário serializado pelo motor principal. |
| `Tmp_CoreResult` | Dicionário | Resultado intermediário parseado. |
| `Tmp_CoreResultJsonEscape` | Dicionário | Resultado da `String Utils` ao escapar o envelope intermediário. |
| `Tmp_UiEscapeResult` | Dicionário | JUIF UI Json escapado uma vez. |
| `Tmp_ResultJson` | Texto | Resultado universal final antes do último `JSON Parse`. |

## Corpo completo — passo a passo

### Ação 1 — Action Group

- **Ação:** `Action Group`.
- **Nome:** `01 — Build JUIF UI Contract`.
- **Rótulo:** `01 — Build and Publish Resultado`.
- **Children collapsed:** desabilitado.
- **Dont log if condition is false:** desabilitado.
- **Objetivo:** agrupar toda a construção e publicação do contrato.

### Ação 2 — Action Block: escapar Config Json

- **Ação:** `Action Block`.
- **Action Block:** `[CDXMS] String Utils`.
- **Aguardar conclusão:** sim.
- **Entradas:**
  - `Operation = escape_json_string`;
  - `Text = {lv=Config Json}`.
- **Saída:**
  - `Resultado -> Tmp_ConfigEscapeResult`.
- **Objetivo:** impedir que aspas, barras e quebras do JSON cru quebrem o código JavaScript.

### Ação 3 — Action Block: escapar UI Schema Json

- **Ação:** `Action Block`.
- **Action Block:** `[CDXMS] String Utils`.
- **Aguardar conclusão:** sim.
- **Entradas:**
  - `Operation = escape_json_string`;
  - `Text = {lv=UI Schema Json}`.
- **Saída:**
  - `Resultado -> Tmp_SchemaEscapeResult`.

### Ação 4 — JavaScript Code: construir contrato

- **Ação:** `JavaScript Code` (`JavaScriptAction`).
- **Engine:** `JetPack JavascriptEngine`.
- **Block next action:** habilitado.
- **Variável textual de saída:** `Tmp_CoreResultJson`.
- **Entradas consumidas:**
  - `{lv=Tmp_ConfigEscapeResult[data][value]}`;
  - `{lv=Tmp_SchemaEscapeResult[data][value]}`.
- **Não permitido:** inserir `{lv=Config Json}` ou `{lv=UI Schema Json}` diretamente no script.
- **Processamento:**
  1. interpreta os JSONs já protegidos;
  2. valida `pages` e `page.id`;
  3. preserva o `state` declarado;
  4. hidrata propriedades `bind`;
  5. monta `mapping_json`;
  6. normaliza sections, fields, lists, components e actions;
  7. normaliza o shell persistente;
  8. gera `juif_ui_json`;
  9. monta um Resultado intermediário no contrato universal.
- **Erros:** `MISSING_REQUIRED_INPUT`, `INVALID_INPUT_TYPE`, `INVALID_JSON`, `INVALID_ENUM_VALUE` e `PROCESSING_FAILED`.

### Ação 5 — JSON Parse: Resultado intermediário

- **String source:** `Tmp_CoreResultJson`.
- **Dictionary target:** `Tmp_CoreResult`.
- **Dictionary keys:** raiz.
- **Objetivo:** disponibilizar os campos intermediários para as ações seguintes.

### Ação 6 — Action Block: escapar envelope intermediário

- **Action Block:** `[CDXMS] String Utils`.
- **Aguardar conclusão:** sim.
- **Entradas:**
  - `Operation = escape_json_string`;
  - `Text = {lv=Tmp_CoreResultJson}`.
- **Saída:** `Resultado -> Tmp_CoreResultJsonEscape`.
- **Objetivo:** permitir que o JavaScript final reconstrua o envelope sem receber JSON cru.

### Ação 7 — Action Block: escapar JUIF UI Json

- **Action Block:** `[CDXMS] String Utils`.
- **Aguardar conclusão:** sim.
- **Entradas:**
  - `Operation = escape_json_string`;
  - `Text = {lv=Tmp_CoreResult[data][juif_ui_json]}`.
- **Saída:** `Resultado -> Tmp_UiEscapeResult`.
- **Objetivo:** produzir o valor canônico de `juif_ui_json_escaped`.

### Ação 8 — JavaScript Code: finalizar Resultado

- **Engine:** `JetPack JavascriptEngine`.
- **Block next action:** habilitado.
- **Variável textual de saída:** `Tmp_ResultJson`.
- **Entradas consumidas:**
  - `{lv=Tmp_CoreResultJsonEscape[data][value]}`;
  - `{lv=Tmp_UiEscapeResult[data][value]}`;
  - `{lv=Escape Json}`.
- **Comportamento:**
  1. reconstrói o Resultado intermediário;
  2. preserva `juif_ui_json` cru;
  3. preserva o valor canônico da `String Utils` em `juif_ui_json_escaped` quando `Escape Json = true`, sem executar um segundo escape;
  4. usa o valor cru quando `Escape Json = false`;
  5. serializa o Resultado final.

### Ação 9 — JSON Parse: publicar Resultado

- **String source:** `Tmp_ResultJson`.
- **Dictionary target:** `Resultado`.
- **Dictionary keys:** raiz.
- **Objetivo:** publicar a única saída pública.

### Ação 10 — End Action Group

- encerra `01 — Build JUIF UI Contract`.

### Ação 11 — Exit Action Block

- **Output option:** `0`.
- finaliza explicitamente a capability.

## Catálogo suportado

O Builder aceita 36 componentes. O contrato canônico fica em:

```text
capabilities/java_ui_framework/component_catalog.json
```

## Efeitos colaterais

Nenhum.

## Regras de fronteira

- `Config Json` e `UI Schema Json` nunca entram crus no JavaScript;
- o Builder não possui função manual de escape JSON;
- todo escape é delegado a `[CDXMS] String Utils`;
- `Resultado.data` permanece a estrutura pública canônica;
- versões continuam em `1.0.0` até a primeira release.

## UI padrão canônica

- `initial_page`: `overview`;
- sete páginas;
- shell persistente;
- state de catálogo unificado em `catalog_section`;
- 21 bindings;
- cobertura de 36/36 componentes.
