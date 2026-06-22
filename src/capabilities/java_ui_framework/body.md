# Corpo do Action Block — [CDXMS] Java UI Framework v1.0.0

## Objetivo

Renderizar um contrato JUIF em um overlay Android, manter state e eventos em runtime e oferecer navegação multipágina com shell persistente e conteúdo rolável independente.

## Tipo

Capability impura de apresentação. Seu efeito colateral esperado é a criação de um overlay `TYPE_APPLICATION_OVERLAY`.

## Entrada

| Entrada | Tipo | Obrigatória | Descrição |
|---|---|---:|---|
| `JUIF UI Json` | Texto/JSON | Não | Contrato JUIF normal produzido pelo Builder ou escrito manualmente. Quando vazio, usa a UI de demonstração embarcada. |

## Saída

| Saída | Tipo | Descrição |
|---|---|---|
| `Resultado` | Dicionário | Saída pública única no contrato universal CDXMS. Informa página atual, state, fallback utilizado, catálogo e presença de shell. |

## Variáveis de trabalho

| Variável | Tipo | Descrição |
|---|---|---|
| `Tmp_JuifVisible` | Booleano | Indica se o overlay está visível. |
| `Tmp_JuifClicked` | Booleano | Indica que um evento foi emitido. |
| `Tmp_JuifAction` | Texto | Última ação/evento emitido. |
| `Tmp_JuifPayload` | Texto/JSON | Payload do último evento, incluindo página atual e snapshot do state. |
| `Tmp_JuifState` | Texto/JSON | State atualizado da interface. |
| `Tmp_JuifCurrentPage` | Texto | Id da página atualmente renderizada. |
| `Tmp_ResultJson` | Texto/JSON | Resultado universal serializado pelo Java Action. |
| `Tmp_JuifUiJsonEscaped` | Texto | Entrada escapada para inserção segura no literal Java. |
| `Tmp_DefaultUiJson` | Texto/JSON | UI de fallback e catálogo interativo usado quando a entrada não é fornecida. |

## Corpo completo — passo a passo

### Ação 1 — Action Group

- **Ação MacroDroid:** `Action Group`.
- **Nome do grupo:** `01 — Prepare JUIF Input`.
- **Rótulo:** `01 — Escape JUIF UI Json`.
- **Children collapsed:** habilitado.
- **Dont log if condition is false:** desabilitado.
- **Comentário:** escapa barras, aspas e quebras antes do Java Action.

### Ação 2 — Text Manipulation: escapar barras

- **Ação MacroDroid:** `Text Manipulation` (`TextManipulationAction`).
- **Source text:** `{lv=JUIF UI Json}`.
- **Operation:** `Replace All`.
- **Search:** `\`.
- **Replacement:** `\\`.
- **Ignore case:** desabilitado.
- **Output variable:** `Tmp_JuifUiJsonEscaped`.
- **Objetivo:** preservar barras existentes quando o JSON for inserido no literal Java.

### Ação 3 — Text Manipulation: escapar aspas

- **Ação MacroDroid:** `Text Manipulation`.
- **Source text:** `{lv=Tmp_JuifUiJsonEscaped}`.
- **Operation:** `Replace All`.
- **Search:** `"`.
- **Replacement:** `\"`.
- **Ignore case:** desabilitado.
- **Output variable:** `Tmp_JuifUiJsonEscaped`.
- **Objetivo:** impedir que aspas do JSON encerrem o literal Java.

### Ação 4 — Text Manipulation: normalizar quebras

- **Ação MacroDroid:** `Text Manipulation`.
- **Source text:** `{lv=Tmp_JuifUiJsonEscaped}`.
- **Operation:** `Replace All`.
- **Search:** quebra de linha real.
- **Replacement:** `\n`.
- **Ignore case:** desabilitado.
- **Output variable:** `Tmp_JuifUiJsonEscaped`.
- **Objetivo:** evitar quebra física do literal Java.

### Ação 5 — End Action Group

- **Ação MacroDroid:** `End Action Group`.
- **Objetivo:** encerrar `01 — Prepare JUIF Input`.

### Ação 6 — Action Group

- **Ação MacroDroid:** `Action Group`.
- **Nome do grupo:** `02 — Render JUIF Overlay`.
- **Rótulo:** `02 — Render and Publish Resultado`.
- **Children collapsed:** desabilitado.
- **Dont log if condition is false:** desabilitado.
- **Comentário:** renderiza a UI declarativa e publica `Resultado` sem persistir configurações.

### Ação 7 — Java Code

- **Ação MacroDroid:** `Java Code` (`JavaAction`).
- **Block next action:** habilitado.
- **Run in background thread:** desabilitado, pois o código cria e manipula views.
- **Response variable:** `Tmp_ResultJson`.
- **Console variable:** nenhuma.
- **Logging:** habilitado conforme padrão da macro.
- **Processamento interno:**
  1. importa as APIs Android e `org.json` necessárias;
  2. inicializa tokens visuais, state, navegação e hosts do shell;
  3. limpa `Tmp_JuifVisible`, `Tmp_JuifClicked`, `Tmp_JuifAction`, `Tmp_JuifPayload`, `Tmp_JuifState` e `Tmp_JuifCurrentPage`;
  4. valida a permissão `SYSTEM_ALERT_WINDOW`;
  5. usa `Tmp_DefaultUiJson` somente quando a entrada estiver ausente ou ainda contiver Magic Text não resolvido;
  6. interpreta `state`, `pages` e `shell`;
  7. converte o contrato legado de página única para uma página `main`;
  8. cria o overlay com `WindowManager.TYPE_APPLICATION_OVERLAY`;
  9. cria os hosts persistentes `Top Host`, `Tab Host`, `Body`, `Rail Host`, `ScrollView`, `Bottom Host` e `Drawer Layer`;
  10. mantém somente o conteúdo da página dentro do `ScrollView`;
  11. resolve visibilidade de shell por `visible_pages` e `hidden_pages`;
  12. resolve seleção por `target`, `active_pages`, `active_prefix` e `selected`;
  13. renderiza os 26 componentes do protótipo;
  14. renderiza e estiliza os 10 componentes adicionados na v1.0.0;
  15. abre e fecha o drawer em camada com scrim e animação;
  16. mantém navegação por `navigate`, `replace`, `back`, `open_drawer`, `close_drawer` e `close`;
  17. mantém state local e emite payloads com ação, página atual e snapshot do state;
  18. retorna o conteúdo ao topo após cada troca de página;
  19. permite fechar o overlay por long press;
  20. publica `Tmp_ResultJson` com `artifact_id=java_ui_framework`.
- **Configuração da janela:**
  - largura: `MATCH_PARENT`;
  - altura: `MATCH_PARENT`;
  - tipo: `TYPE_APPLICATION_OVERLAY`;
  - flag: `FLAG_LAYOUT_IN_SCREEN`;
  - pixel format: `TRANSLUCENT`;
  - soft input: `ADJUST_RESIZE | STATE_UNSPECIFIED`.
- **Resultado de sucesso:** inclui `current_page`, `state`, `using_default_ui`, `component_catalog_version`, `supported_component_count`, `shell_enabled`, `shell_mode` e `drawer_available`.
- **Resultado de erro:** `INVALID_JSON`, `PERMISSION_DENIED`, `PROCESSING_FAILED` ou fallback crítico `UNKNOWN_ERROR`, sempre no contrato universal CDXMS.
### Ação 8 — JSON Parse

- **Ação MacroDroid:** `JSON Parse` (`JsonParseAction`).
- **String source:** `Tmp_ResultJson`.
- **Dictionary target:** `Resultado`.
- **Dictionary keys:** raiz do dicionário, sem chave interna.
- **Objetivo:** publicar a única saída pública do Action Block.

### Ação 9 — End Action Group

- **Ação MacroDroid:** `End Action Group`.
- **Objetivo:** encerrar `02 — Render JUIF Overlay`.

### Ação 10 — Exit Action Block

- **Ação MacroDroid:** `Exit Action Block`.
- **Output option:** `0` — encerramento normal.
- **Objetivo:** finalizar explicitamente a capability após `Resultado` estar publicado.

## Componentes adicionados

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

Os cinco componentes de navegação podem ser usados inline. Quando declarados em `ui.shell`, são distribuídos em hosts persistentes:

- `top_app_bar` — topo;
- `tab_bar` — abaixo da barra superior;
- `navigation_rail` — lateral do body;
- `bottom_navigation` — base;
- `navigation_drawer` — camada sobre o conteúdo.

Os componentes aceitam controle de página e seleção sem duplicar estado entre telas.
## Efeitos colaterais

- exibe overlay Android;
- atualiza variáveis locais de runtime;
- pode escrever no clipboard apenas quando o usuário aciona explicitamente componentes de cópia;
- não grava arquivos, não altera registry e não acessa rede.


## Validação obrigatória do Resultado

Antes do `JSON Parse`, o texto interno deve representar exatamente o contrato universal e não pode conter `data_json`, `error_code`, `error_message` ou `error_json`.


## UI padrão e tutorial

A UI de fallback possui sete páginas e usa todos os 36 componentes. O catálogo utiliza uma única `tab_bar` global para as cinco categorias, uma `bottom_navigation` para as áreas principais e um `navigation_drawer` para o mapa completo da documentação.

A organização evita componentes complexos lado a lado em telas estreitas e mantém o catálogo navegável sem duplicar barras em cada página.
