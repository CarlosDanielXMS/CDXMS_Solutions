# [CDXMS] Java UI Framework v1.0.0

Capability de apresentação responsável por renderizar contratos JUIF em overlay Android por meio do `JavaAction` do MacroDroid.

## Estado

- 26 componentes do protótipo preservados;
- 10 componentes adicionais refinados no mesmo sistema visual;
- catálogo total de 36 componentes;
- shell persistente com hosts independentes;
- saída pública única `Resultado`;
- pronta para homologação visual e interativa em dispositivo.

## Arquitetura visual

O overlay utiliza uma estrutura de aplicação completa:

```text
Overlay
├── Top App Bar persistente
├── Tab Bar persistente e contextual
├── Body
│   ├── Navigation Rail opcional
│   └── ScrollView
│       └── Conteúdo da página
├── Bottom Navigation persistente
└── Navigation Drawer em camada com scrim
```

Somente o conteúdo da página é rolável. As barras de navegação permanecem estáveis durante a leitura e a interação.

## Sistema visual dos componentes novos

Os novos componentes seguem o tema dark gold do JUIF:

- superfícies escuras em níveis;
- bordas discretas;
- seleção dourada com baixo contraste de fundo;
- tipografia hierárquica;
- indicadores de navegação consistentes;
- áreas de toque adequadas;
- animações curtas para drawer e overlay;
- ausência de cards e bordas decorativas desnecessárias.

Componentes refinados:

- `top_app_bar`;
- `bottom_navigation`;
- `navigation_rail`;
- `navigation_drawer`;
- `tab_bar`;
- `search_bar`;
- `chip`;
- `chip_group`;
- `empty_state`;
- `loading_indicator`.

## Navegação

O shell aceita:

- `visible_pages` e `hidden_pages` para controlar onde cada elemento aparece;
- `target`, `active_pages`, `active_prefix` e `selected` para resolver seleção;
- `open_drawer` e `close_drawer`;
- títulos derivados da página por `use_page_title`;
- navegação por `navigate`, `replace`, `back` e `close`.

## Responsabilidade

- renderizar páginas e componentes;
- manter state em memória;
- emitir eventos estruturados;
- encaminhar eventos de negócio por Intent explícito quando `event_bridge` estiver habilitado;
- coordenar navegação do overlay;
- expor o estado inicial e os eventos no contrato universal.

## Não faz

- não lê nem grava arquivos;
- não instala artifacts;
- não persiste configurações;
- não acessa catálogo remoto;
- não contém regra de negócio de uma solution.

## Validação

```bash
python src/capabilities/java_ui_framework/scripts/validate_java_ui_framework_incremental.py
python src/scripts/validate_ui_capabilities_v1_0_0.py
```

A homologação em dispositivo continua obrigatória para confirmar dimensões, teclado, animações e comportamento do overlay no Android real.

## Hotfix de navegação do catálogo

A navegação que substitui a árvore visual não é executada diretamente dentro do `onClick`. O evento é publicado no próximo ciclo da main thread por `View.post`, evitando remover a própria barra que ainda processa o toque.

Eventos não navegacionais permanecem disponíveis nas variáveis de runtime e, quando configurado no contrato, são enviados à macro orquestradora pelo action `com.cdxms.solutions.EVENT`. O broadcast é restrito ao pacote do MacroDroid e inclui namespace, protocolo, sessão, `event_id`, origem, ação, página e JSON integral do evento.

A renderização também é transacional:

- a nova página é criada em um container de staging;
- todos os elementos do shell são construídos antes da limpeza dos hosts atuais;
- a árvore visível só é substituída depois que a construção completa termina;
- qualquer `Throwable` produz `UI_RUNTIME_ERROR`, Toast e banner inline sem fechar silenciosamente o overlay.
