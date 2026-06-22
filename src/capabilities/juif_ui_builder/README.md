# [CDXMS] JUIF UI Builder v1.0.0

Capability pura responsável por transformar `Config Json` e `UI Schema Json` em um contrato JUIF consumível pelo `[CDXMS] Java UI Framework`.

## Estado

- protótipo funcional preservado;
- interface pública adaptada ao padrão CDXMS;
- saída pública única `Resultado`;
- catálogo JUIF v1.0.0 com 36 componentes;
- shell persistente opcional;
- homologação em dispositivo ainda obrigatória.

## Responsabilidade

- validar os JSONs de entrada;
- hidratar componentes declarados com `bind`;
- montar `state` e `mapping_json`;
- normalizar pages, sections, fields, lists e componentes diretos;
- normalizar shell de navegação;
- rejeitar tipos não suportados;
- gerar JSON cru e escapado.

## Não faz

- não renderiza UI;
- não acessa arquivos;
- não persiste configuração;
- não chama JCM;
- não altera registry.

## Dependência

`[CDXMS] Java UI Framework >= 1.0.0`, pois o catálogo aceito pelo builder deve corresponder ao renderer.

## Validação

```bash
python src/capabilities/juif_ui_builder/scripts/validate_juif_ui_builder_incremental.py
python src/scripts/validate_ui_capabilities_v1_0_0.py
```
