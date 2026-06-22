# Corpo — [CDXMS] Registrar Resultado v1.0.0

## Entradas

- `Operation`: Operação técnica do Result Manager.
- `Source Artifact Type`: Tipo do artifact de origem.
- `Source Artifact Id`: Id do artifact de origem.
- `Source Operation`: Operação original.
- `Success?`: Sucesso lógico.
- `Status`: Status padronizado.
- `Message`: Mensagem humana.
- `Data Json`: Objeto JSON para Resultado.data.
- `Error Json`: Erro estruturado ou null.
- `Result Json`: Resultado bruto.
- `Context Json`: Contexto adicional.
- `Strict Mode?`: Validação rigorosa.
- `Include Raw Result?`: Inclui bruto para debug.
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
