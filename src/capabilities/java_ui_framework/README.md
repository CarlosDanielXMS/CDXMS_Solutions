# [CDXMS] Java UI Framework v1.0.0

Capability de apresentação responsável por renderizar contratos JUIF em overlay Android usando o `JavaAction` do MacroDroid.

## Estado

- definições do protótipo preservadas;
- 26 componentes anteriores mantidos;
- 10 componentes adicionados;
- shell declarativo opcional no fluxo rolável;
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
- tratar seleção em drawer inline e fechamento do overlay;
- renderizar componentes de shell sem reescrever a hierarquia-base das páginas legadas.

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


## Correção de contrato e runtime

- `Resultado` contém somente os campos permitidos por `core/result_contract.json`.
- O bridge interno do export funcional do protótipo foi preservado.
- O overlay e o `ScrollView` permanecem com a hierarquia original; barras de shell são renderizadas no conteúdo rolável.
- `navigation_rail` e `navigation_drawer` são componentes inline e podem ser combinados com `row`/`column`.
- A homologação no dispositivo continua obrigatória.
