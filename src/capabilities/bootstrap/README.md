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

Este package inclui o export `[CDXMS]_Bootstrap.ablock`, criado a partir de export real do MacroDroid com referência interna ao `[CDXMS] Json Config Manager`. A homologação final deve ser feita por importação e testes no MacroDroid real.

## Saneamento pré-release v1.0.0

A capability permanece na versão `1.0.0`. Este ajuste registra a auditoria de ações nativas, JS e Shell antes da primeira release oficial.

- Política: `native_first_when_safe_clear_and_homologated`.
- JS: `9` ocorrência(s).
- Shell: `0` ocorrência(s).
- Decisão: Mantém o Bootstrap minimalista, com dependência direta apenas do JCM. Não foi adicionada dependência obrigatória do Result Manager para não fragilizar a inicialização limpa do core.

