# Corpo — [CDXMS] Bootstrap v1.0.0

## Entradas

- `Operation`: initialize_ecosystem, verify_core, repair_core, ensure_runtime, load_context ou get_status.
- `Requested Artifact Type`: contexto opcional do chamador.
- `Requested Artifact Id`: artifact opcional solicitado.
- `Force Repair?`: autoriza reparo do core.
- `Load Context?`: carrega contexto após inicialização.
- `Config Json`: configuração completa opcional.
- `Session Id` / `Correlation Id`: rastreabilidade.

## Saída

- `Resultado`: dicionário no contrato universal CDXMS.

## Variáveis de trabalho

Variáveis `Tmp_*` são internas e nunca expostas como saída pública.

## Corpo passo a passo

1. Normaliza operação, booleanos e contexto.
2. Chama `[CDXMS] Json Config Manager` para ensure/repair/read conforme a operação.
3. Garante runtime quando solicitado.
4. Consolida o estado do core e contexto.
5. Publica somente `Resultado`.
6. Encerra explicitamente o Action Block.
