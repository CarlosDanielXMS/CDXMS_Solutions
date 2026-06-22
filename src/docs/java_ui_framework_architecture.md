# Arquitetura — Java UI Framework v1.0.0

## Papel

Renderer declarativo da camada de apresentação. Recebe `JUIF UI Json`, cria o overlay Android, mantém state e navegação e publica eventos no contrato universal. Não persiste dados e não conhece lifecycle de artifacts.

## Fluxo

```text
JUIF UI Json
→ escape seguro no Action Block
→ Java Action
→ parse de state/pages/shell
→ criação dos hosts persistentes
→ renderização da página
→ interação e navegação
→ Resultado
```

## Hierarquia do overlay

```text
FrameLayout juifOverlay
├── LinearLayout juifRootContainer
│   ├── juifTopHost
│   ├── juifTabHost
│   ├── juifBodyContainer
│   │   ├── juifRailHost
│   │   └── juifContentScroll
│   │       └── juifPageContainer
│   └── juifBottomHost
└── juifDrawerLayer
    ├── scrim
    └── drawer panel
```

A hierarquia separa navegação estrutural de conteúdo. Apenas `juifContentScroll` rola.

## Shell

`ui.shell` é opcional. Quando presente:

- `top_app_bar` ocupa `juifTopHost`;
- `tab_bar` ocupa `juifTabHost`;
- `navigation_rail` ocupa a lateral do body;
- `bottom_navigation` ocupa `juifBottomHost`;
- `navigation_drawer` é aberto em `juifDrawerLayer`.

Cada componente pode usar:

- `visible_pages`;
- `hidden_pages`.

Cada item de navegação pode usar:

- `target`;
- `active_pages`;
- `active_prefix`;
- `selected`.

A página atual tem prioridade na resolução visual da seleção.

## Drawer

O drawer:

- usa scrim;
- abre e fecha com animação;
- fecha por item, botão ou toque no scrim;
- emite `drawer_opened`, `drawer_closed`, `drawer_error` ou `drawer_unavailable`.

## Compatibilidade

- contratos de página única continuam convertidos para `main`;
- os 26 renderers do protótipo permanecem;
- os dez renderers adicionais continuam com os mesmos ids;
- componentes de navegação podem ser usados inline;
- o contrato universal de `Resultado` permanece inalterado.

## Limites

- depende da permissão Android para overlays;
- precisa ser homologado em dispositivo após alterações no Java Action;
- não substitui UI nativa do MacroDroid em fluxos de recuperação crítica;
- não garante importação automática de artifacts.
