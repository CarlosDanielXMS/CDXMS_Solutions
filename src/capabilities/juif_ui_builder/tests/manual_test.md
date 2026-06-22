# Teste manual — [CDXMS] JUIF UI Builder v1.0.0

## Preparação

1. Importe `[CDXMS] JUIF UI Builder`.
2. Execute o Action Block com os valores padrão.

## Resultado

Validar:

- `Resultado.success = true`;
- `Resultado.status = success`;
- `Resultado.artifact_id = juif_ui_builder`;
- `Resultado.operation = build_ui`;
- `Resultado.data.supported_component_count = 36`;
- `Resultado.data.juif_ui_json` é JSON válido;
- `Resultado.data.mapping_json` contém 21 bindings;
- nenhum campo proibido existe no topo.

## Contrato padrão gerado

Validar:

- `initial_page = overview`;
- existem sete páginas;
- `pages` é normalizado como objeto indexado por id;
- `shell.top_app_bar.type = top_app_bar`;
- `shell.tab_bar.type = tab_bar`;
- `shell.bottom_navigation.type = bottom_navigation`;
- `shell.navigation_drawer.type = navigation_drawer`;
- a Tab Bar possui `visible_pages` com as cinco páginas do catálogo;
- Bottom Navigation usa `active_pages` para manter Catálogo selecionado;
- o drawer possui o mapa completo da documentação;
- todos os 36 tipos aparecem no contrato final.

## Catálogo e estado

- existe apenas uma chave `catalog_section`;
- não existem chaves `catalog_tabs_<pagina>`;
- cada item da Tab Bar aponta para uma página válida;
- cada item da Bottom Navigation aponta para uma página válida;
- listas `active_pages` contêm apenas ids existentes.

## Bindings

Confirmar hidratação de:

- métricas;
- perfil;
- pesquisa;
- chip;
- chip group;
- lista dinâmica;
- fluxo copiável;
- code block;
- sandbox.

## Cenários negativos

1. `Config Json` inválido → `INVALID_JSON`.
2. `UI Schema Json` vazio → `MISSING_REQUIRED_INPUT`.
3. Componente desconhecido → `INVALID_ENUM_VALUE`.
4. Página sem `id` → `MISSING_REQUIRED_INPUT`.
5. `pages` vazio → `MISSING_REQUIRED_INPUT`.
