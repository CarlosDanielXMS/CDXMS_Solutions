# [CDXMS] JUIF UI Builder v1.0.0

Capability pura responsável por transformar `Config Json` e `UI Schema Json` em um contrato JUIF consumível pelo `[CDXMS] Java UI Framework`.

## Estado

- interface pública alinhada ao padrão CDXMS;
- saída pública única `Resultado`;
- catálogo JUIF v1.0.0 com 36 componentes;
- shell persistente opcional;
- UI padrão reorganizada como documentação interativa profissional;
- motor puro do Builder preservado.

## UI padrão

O schema padrão possui sete páginas:

1. `overview` — visão geral, arquitetura e fluxo;
2. `catalog_layout` — composição, superfícies e tipografia;
3. `catalog_forms` — entradas, filtros, bindings e state;
4. `catalog_data` — métricas, listas e conteúdo;
5. `catalog_feedback` — alertas, progresso e estados;
6. `catalog_navigation` — shell, rail e comportamento de navegação;
7. `playground` — code block e sandbox.

A navegação usa uma única `tab_bar` compartilhada entre as páginas do catálogo. O estado deixou de ser fragmentado em uma chave por página.

## Shell padrão

- Top App Bar com título contextual e acesso ao drawer;
- Tab Bar visível apenas nas páginas do catálogo;
- Bottom Navigation para Início, Catálogo e Laboratório;
- Navigation Drawer com o mapa completo da documentação;
- seleção resolvida por página atual e grupos `active_pages`.

## Responsabilidade

- validar os JSONs de entrada;
- hidratar componentes declarados com `bind`;
- montar `state` e `mapping_json`;
- normalizar pages, sections, fields, lists e componentes diretos;
- normalizar shell e itens de navegação;
- rejeitar tipos não suportados;
- gerar JSON cru e escapado.

## Não faz

- não renderiza UI;
- não acessa arquivos;
- não persiste configuração;
- não chama JCM;
- não altera registry.

## Dependência

`[CDXMS] Java UI Framework >= 1.0.0`, pois o catálogo aceito pelo Builder deve corresponder ao renderer.

## Validação

```bash
python src/capabilities/juif_ui_builder/scripts/validate_juif_ui_builder_incremental.py
python src/scripts/validate_ui_capabilities_v1_0_0.py
```
