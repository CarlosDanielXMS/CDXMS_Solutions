# Corpo — [CDXMS] String Utils v1.0.0

## Entradas

- `Operation`: Operação técnica da String Utils.
- `Text`: Texto principal.
- `Search Text`: Texto procurado.
- `Replacement Text`: Texto de substituição.
- `Regex Pattern`: Regex opcional.
- `Max Length`: Comprimento máximo.
- `Comparison Mode`: case_sensitive, case_insensitive ou normalized.
- `Case Mode`: none, lower, upper ou title.
- `Strict Mode?`: Validação rigorosa.
- `Session Id`: Id de sessão.
- `Correlation Id`: Id de correlação.

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
