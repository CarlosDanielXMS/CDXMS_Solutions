# Corpo do Action Block — [CDXMS] JUIF UI Builder v1.0.0

## Objetivo

Validar e transformar um schema declarativo de UI, combinado com um JSON de configuração, em um contrato JUIF normalizado e compatível com o `[CDXMS] Java UI Framework`.

## Tipo

Capability pura. Não grava arquivos, não altera variáveis globais, não exibe UI e não acessa rede.

## Entradas

| Entrada | Tipo | Obrigatória | Valor padrão | Descrição |
|---|---|---:|---|---|
| `Config Json` | Texto/JSON | Sim | `{}` | Objeto JSON com os valores usados para hidratar propriedades declaradas por `bind`. |
| `UI Schema Json` | Texto/JSON | Sim | — | Schema multipágina contendo `state`, `pages`, sections, fields, lists, components, actions e `shell` opcional. |
| `Escape Json` | Booleano | Não | `true` | Quando verdadeiro, também gera `juif_ui_json_escaped` para fronteiras textuais do MacroDroid. |

## Saída

| Saída | Tipo | Descrição |
|---|---|---|
| `Resultado` | Dicionário | Saída pública única no contrato universal CDXMS. Em sucesso, `data` contém o JSON JUIF, a versão escapada, o mapping e o catálogo suportado. |

## Variáveis de trabalho

| Variável | Tipo | Exposição | Descrição |
|---|---|---|---|
| `Tmp_ResultJson` | Texto | Interna | Resultado universal serializado pelo JavaScript antes da publicação com `JSON Parse`. |

## Corpo completo — passo a passo

### Ação 1 — Action Group

- **Ação MacroDroid:** `Action Group`.
- **Nome do grupo:** `01 — Build JUIF UI Contract`.
- **Rótulo:** `01 — Build and Publish Resultado`.
- **Children collapsed:** desabilitado.
- **Dont log if condition is false:** desabilitado.
- **Comentário:** constrói o contrato JUIF v1.0.0 sem persistência ou efeitos colaterais.

### Ação 2 — JavaScript Code

- **Ação MacroDroid:** `JavaScript Code` (`JavaScriptAction`).
- **Engine:** `JetPack JavascriptEngine`.
- **Block next action:** habilitado.
- **Console output variable:** nenhuma.
- **Variável de saída textual:** `Tmp_ResultJson`.
- **Logging:** habilitado conforme padrão da macro.
- **Entradas consumidas por Magic Text em blocos de comentário:**
  - `{lv=Config Json}`;
  - `{lv=UI Schema Json}`;
  - `{lv=Escape Json}`.
- **Processamento interno:**
  1. valida entradas obrigatórias e tipos;
  2. normaliza BOM, quebras, JSON entre aspas, escapes e o caso legado `{{...}}`;
  3. interpreta `Config Json` e `UI Schema Json`;
  4. valida `pages` como lista não vazia e exige `page.id`;
  5. preserva `state` já declarado pelo schema;
  6. hidrata propriedades `bind` a partir de `Config Json`;
  7. monta `mapping_json` com origem, destino, tipo e propriedade de valor;
  8. normaliza `sections`, `fields`, `lists`, `components` e `actions`;
  9. aceita os 26 tipos do protótipo sem alteração semântica;
  10. aceita os 10 novos tipos do catálogo v1.0.0;
  11. normaliza `shell` e o alias `navigation`;
  12. normaliza aliases de shell: `top_bar`, `bottom_bar`, `rail`, `drawer` e `tabs`;
  13. converte a lista de páginas do schema em objeto indexado por `page.id`, como esperado pelo renderer;
  14. serializa `juif_ui_json` e, quando solicitado, `juif_ui_json_escaped`;
  15. publica o contrato universal CDXMS em `Tmp_ResultJson`.
- **Erros estruturados:**
  - `MISSING_REQUIRED_INPUT`;
  - `INVALID_INPUT_TYPE`;
  - `INVALID_JSON`;
  - `INVALID_ENUM_VALUE`;
  - `PROCESSING_FAILED`.

### Ação 3 — JSON Parse

- **Ação MacroDroid:** `JSON Parse` (`JsonParseAction`).
- **String source:** `Tmp_ResultJson`.
- **Dictionary target:** `Resultado`.
- **Dictionary keys:** raiz do dicionário, sem chave interna.
- **Objetivo:** transformar o texto JSON produzido pela ação anterior na única saída pública do Action Block.

### Ação 4 — End Action Group

- **Ação MacroDroid:** `End Action Group`.
- **Objetivo:** encerrar `01 — Build JUIF UI Contract`.

### Ação 5 — Exit Action Block

- **Ação MacroDroid:** `Exit Action Block`.
- **Output option:** `0` — encerramento normal.
- **Objetivo:** finalizar explicitamente a capability após `Resultado` estar publicado.

## Catálogo suportado

O Builder aceita 36 componentes. Os 26 tipos do protótipo foram preservados e os novos tipos são:

```text
top_app_bar
bottom_navigation
navigation_rail
navigation_drawer
tab_bar
search_bar
chip
chip_group
empty_state
loading_indicator
```

O contrato canônico do catálogo fica em:

```text
capabilities/java_ui_framework/component_catalog.json
```

## Efeitos colaterais

Nenhum.
