# Teste manual — [CDXMS] Bootstrap v1.0.0

## Testes do Action Block

1. Importe `macrodroid/[CDXMS]_Bootstrap.ablock` com o JCM correspondente.
2. Execute `initialize_ecosystem`.
3. Confirme `Resultado.success = true` e `bootstrap_status = initialized`.
4. Execute `verify_core` e confirme `data.valid = true`.
5. Execute `ensure_runtime` e confirme `bootstrap_status = runtime_ready`.
6. Execute `get_status` e confirme `data.ready = true`.
7. Repita `initialize_ecosystem` e confirme idempotência.

## Teste de entrada única

A prova oficial usa `[CDXMS] Homologar Entrada Única Bootstrap v1.0.0 TEMP`, que incorpora Bootstrap e JCM com GUIDs exclusivos.

Critério:

- nenhuma capability CDXMS TEMP pré-instalada;
- uma única macro importada;
- Bootstrap incorporado executado;
- JCM incorporado resolvido transitivamente;
- inicialização executada duas vezes sem falha;
- core válido;
- runtime pronto;
- marcador `.cdxms_root.json` relido diretamente pelo JCM;
- estado final `ready`.
