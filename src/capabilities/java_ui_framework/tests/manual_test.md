# Teste manual — [CDXMS] Java UI Framework v1.0.0

## Preparação

1. Conceda ao MacroDroid a permissão para exibir sobre outros apps.
2. Importe `[CDXMS] Java UI Framework`.
3. Execute o Action Block sem alterar `JUIF UI Json`.

## Resultado inicial

Validar:

- `Resultado.success = true`;
- `Resultado.status = success`;
- `Resultado.artifact_id = java_ui_framework`;
- `Resultado.operation = render_ui`;
- `Resultado.data.current_page = overview`;
- `Resultado.data.using_default_ui = true`;
- `Resultado.data.supported_component_count = 36`;
- `Resultado.data.shell_enabled = true`;
- `Resultado.data.shell_mode = persistent_hosts`;
- `Resultado.data.drawer_available = true`;
- nenhum campo legado proibido existe no topo.

## Estrutura persistente

1. Role a página inicial até o final.
2. Confirme que Top App Bar, Tab Bar quando aplicável e Bottom Navigation não acompanham o conteúdo.
3. Troque de página e confirme que o conteúdo volta ao topo.
4. Abra o teclado em um input e confirme que o body é redimensionado sem sobrepor o campo ativo.

## Drawer

1. Toque no botão de menu da Top App Bar.
2. Confirme scrim escuro, painel lateral e animação de entrada.
3. Selecione cada categoria.
4. Confirme que a página muda, o drawer fecha e o item correspondente permanece selecionado.
5. Abra novamente e feche pelo botão `×` e pelo scrim.

## Catálogo

Percorra:

- Layout;
- Formulários;
- Dados;
- Feedback;
- Navegação.

Confirmar:

- existe uma única Tab Bar persistente;
- a seleção segue a página atual;
- a Bottom Navigation mantém `Catálogo` ativo em todas as cinco páginas;
- nenhuma categoria abre página inexistente;
- não há sobreposição, corte horizontal ou cards excessivamente estreitos.

## Componentes refinados

Validar visual e interação de:

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

Os estados selecionados devem usar dourado discreto, superfícies escuras e bordas mínimas.

## Formulários e state

- input e textarea atualizam `Tmp_JuifState`;
- search bar permite digitar, limpar e enviar;
- checkbox, switch, chip e chip group atualizam state;
- select e radio group preservam a seleção;
- eventos atualizam `Tmp_JuifAction`, `Tmp_JuifPayload` e `Resultado`.

## Laboratório

- Code Block formata e copia o schema;
- Sandbox formata, copia e renderiza o JSON;
- preview abre sem remover o shell principal;
- voltar ao início mantém a navegação funcional.

## Cenários de erro

1. Sem permissão de overlay → `PERMISSION_DENIED` e status `blocked`.
2. JSON inválido → `INVALID_JSON`.
3. Página inexistente → evento `navigation_error`.
4. Drawer ausente com ação `open_drawer` → evento `drawer_unavailable`.

## Regressão crítica — entrada no catálogo

1. Abra a UI padrão na página `overview`.
2. Toque em `Catálogo` na Bottom Navigation.
3. Confirme que o overlay permanece aberto e exibe `catalog_layout`.
4. Confirme que a Tab Bar aparece sem encerrar o Action Block.
5. Alterne por Layout, Formulários, Dados, Feedback e Navegação.
6. Volte para Início e depois acesse Laboratório.
7. Repita a entrada no Catálogo pelo botão da página inicial e pelo Navigation Drawer.

Resultado esperado:

- nenhuma navegação fecha o overlay;
- nenhuma exceção escapa do callback de toque;
- a página anterior só é removida após o commit da nova página;
- em falha recuperável, deve aparecer banner `Navegação não concluída`, Toast e `Resultado.error.code = UI_RUNTIME_ERROR`.
