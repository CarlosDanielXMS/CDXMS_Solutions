# Corpo — [CDXMS] Json Config Manager v1.0.0

## Entradas

- Conforme `contract.json`.

## Saída

- `Resultado`: dicionário no contrato universal CDXMS.

## Variáveis de trabalho

- Variável textual `Tmp_*Json` para o resultado serializado.
- Variáveis auxiliares `Tmp_*` somente quando necessárias ao fluxo.

## Corpo passo a passo

1. **Action Group — Processar**
   - Agrupa a execução da capability.
2. **JavaScriptAction — Motor interno**
   - Normaliza entradas.
   - Valida operação e parâmetros.
   - Executa a regra de domínio.
   - Monta Resultado textual.
3. **JsonParseAction — Publicar Resultado**
   - Converte o JSON textual na saída pública `Resultado`.
4. **ActionGroupEndAction**
   - Fecha o grupo.
5. **ExitActionBlockAction**
   - Encerra explicitamente o bloco.
