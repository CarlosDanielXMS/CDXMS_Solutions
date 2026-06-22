# Corpo — [CDXMS] Logger v1.0.0

## Entradas

- `Operation`: Operação técnica do Logger.
- `Level`: debug, info, warning, error ou critical.
- `Event Type`: Tipo lógico do evento.
- `Message`: Mensagem humana.
- `Source Artifact Type`: Tipo do artifact de origem.
- `Source Artifact Id`: Id do artifact de origem.
- `Source Operation`: Operação de origem.
- `Result Json`: Resultado completo para log_result.
- `Data Json`: Dados complementares.
- `Error Json`: Erro estruturado.
- `Tags Json`: Tags JSON.
- `Log Scope`: auto, events, results, errors, audit ou runtime.
- `Log File Name`: Nome opcional do .jsonl.
- `Config Json`: Config opcional.
- `Strict Mode?`: Bloqueia JSON inválido.
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

A persistência do log usa JCM para garantir a pasta e `WriteToFileAction` em modo append para JSON Lines.
