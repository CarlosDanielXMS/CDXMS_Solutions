# [CDXMS] Bootstrap v1.0.0

Capability local de inicialização do ecossistema CDXMS usando o JCM como única dependência fundamental.

## Responsabilidade

- inicializar a estrutura mínima;
- verificar e reparar o core;
- preparar runtime/cache/logs/backups;
- carregar contexto local;
- reportar estado pelo contrato universal `Resultado`.

## Operações

- `initialize_ecosystem`;
- `verify_core`;
- `repair_core`;
- `ensure_runtime`;
- `load_context`;
- `get_status`.

## Papel na entrada única

Na arquitetura v1, o Bootstrap será incorporado à macro `[CDXMS] Solutions Manager` por `exportedActionBlocks`. Ele executará o modo bootstrap da primeira inicialização, mas não será uma macro Installer separada.

O bootstrap local deve funcionar sem rede e sem qualquer capability CDXMS previamente importada além das dependências incorporadas junto com a macro.

## Dependência

```json
{"json_config_manager": ">=1.0.0"}
```

## Distribuição

O export MacroDroid está em `macrodroid/[CDXMS]_Bootstrap.ablock`. A importação automática continua fora de escopo. O primeiro teste da entrada única usa versões TEMP com GUIDs exclusivos para impedir resolução acidental de componentes já existentes no dispositivo.
