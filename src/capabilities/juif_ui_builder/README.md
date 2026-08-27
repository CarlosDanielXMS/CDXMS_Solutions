# [CDXMS] JUIF UI Builder v1.0.0

Capability pura responsável por transformar `Config Json` e `UI Schema Json` em um contrato JUIF consumível pelo `[CDXMS] Java UI Framework`.

## Estado

- interface pública alinhada ao padrão CDXMS;
- saída pública única `Resultado`;
- catálogo JUIF v1.0.0 com 36 componentes;
- shell persistente opcional;
- UI padrão organizada como documentação interativa;
- fronteiras JSON protegidas pela `[CDXMS] String Utils`;
- passagem direta de JSON cru para o JavaScript removida;
- versão preservada em `1.0.0`, pois ainda não existe release.

## UI padrão

O schema padrão possui sete páginas:

1. `overview` — visão geral, arquitetura e fluxo;
2. `catalog_layout` — composição, superfícies e tipografia;
3. `catalog_forms` — entradas, filtros, bindings e state;
4. `catalog_data` — métricas, listas e conteúdo;
5. `catalog_feedback` — alertas, progresso e estados;
6. `catalog_navigation` — shell, rail e comportamento de navegação;
7. `playground` — code block e sandbox.

A navegação usa uma única `tab_bar` compartilhada entre as páginas do catálogo. O estado não é fragmentado em uma chave por página.

## Responsabilidade

- preparar os JSONs de entrada com `string_utils.escape_json_string`;
- validar os JSONs de entrada;
- hidratar componentes declarados com `bind`;
- montar `state` e `mapping_json`;
- normalizar pages, sections, fields, lists e componentes diretos;
- normalizar shell e itens de navegação;
- rejeitar tipos não suportados;
- gerar `juif_ui_json` cru;
- gerar `juif_ui_json_escaped` pela `String Utils`.

## Fronteira JSON

`Config Json` e `UI Schema Json` não são mais inseridos diretamente no código JavaScript. O Action Block chama `[CDXMS] String Utils` antes do motor principal e usa apenas os valores previamente escapados.

A mesma regra é aplicada à saída:

```text
JUIF UI Json cru
-> String Utils / escape_json_string
-> juif_ui_json_escaped
```

Isso centraliza o escape em uma única capability e elimina implementações manuais divergentes.

## Não faz

- não renderiza UI;
- não acessa arquivos;
- não persiste configuração;
- não chama JCM;
- não altera registry.

## Dependências

- `[CDXMS] Java UI Framework >= 1.0.0`;
- `[CDXMS] String Utils >= 1.0.0`.

## Validação

```bash
python src/capabilities/juif_ui_builder/scripts/validate_juif_ui_builder_incremental.py
python src/scripts/validate_ui_capabilities_v1_0_0.py
```

A homologação final do export continua obrigatória em dispositivo real após importação no MacroDroid.
