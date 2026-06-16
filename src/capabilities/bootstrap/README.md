# [CDXMS] Bootstrap

Capability responsável por coordenar a inicialização local do ecossistema CDXMS.

## Responsabilidade

O Bootstrap valida e prepara o ambiente local usando o `[CDXMS] Json Config Manager`.

Ele não baixa arquivos, não instala artifacts remotos, não registra artifacts e não conhece GitHub/CDN.

## Dependência

- `[CDXMS] Json Config Manager >= 1.0.0`

## Operações

- `initialize_ecosystem`
- `verify_core`
- `repair_core`
- `ensure_runtime`
- `load_context`
- `get_status`

## Saída

Saída pública única:

```text
Resultado
```

Dados úteis sempre em:

```text
Resultado.data
```

## Diretriz de performance

O Bootstrap deve carregar settings, registry e config contextual uma única vez no começo do fluxo quando necessário. Capabilities chamadas depois devem receber config completa quando aplicável, evitando consultas repetidas ao JCM.

## Export MacroDroid

O export deve ficar em:

```text
capabilities/bootstrap/macrodroid/[CDXMS]_Bootstrap.ablock
```

Este package não inclui `.ablock` final porque o Action Block precisa ser criado/exportado pelo MacroDroid real para preservar IDs internos de `ActionBlockAction` ao chamar o JCM.
