# [CDXMS] Java UI Framework v1.0.0

Capability de apresentação responsável por renderizar contratos JUIF em overlay Android usando o `JavaAction` do MacroDroid.

## Estado

- definições do protótipo preservadas;
- 26 componentes anteriores mantidos;
- 10 componentes adicionados;
- shell persistente opcional;
- saída pública única `Resultado`;
- homologação em dispositivo ainda obrigatória.

## Novos componentes

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

O catálogo completo está em `component_catalog.json`.

## Responsabilidade

- renderizar pages e componentes;
- manter state da UI;
- emitir eventos estruturados;
- navegar por `navigate`, `replace` e `back`;
- abrir/fechar drawer e overlay;
- renderizar shell persistente sem quebrar páginas legadas.

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
