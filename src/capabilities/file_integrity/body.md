# Corpo do Action Block — [CDXMS] File Integrity v1.0.0

## Entradas

| Entrada | Tipo | Obrigatória | Descrição |
|---|---:|---:|---|
| `Operation` | Texto | Sim | `calculate_sha256` ou `verify_sha256`. |
| `File Path` | Texto | Sim | Caminho absoluto sob o base path CDXMS. |
| `Expected SHA-256` | Texto | Condicional | Obrigatório em `verify_sha256`; 64 hexadecimais. |
| `Session Id` | Texto | Não | Rastreabilidade. |
| `Correlation Id` | Texto | Não | Correlação. |

## Saída

| Saída | Tipo | Descrição |
|---|---:|---|
| `Resultado` | Dicionário | Contrato universal CDXMS. |

## Variáveis de trabalho

- `Tmp_WorkJson` — contexto interno e preflight;
- `Tmp_ShouldExecuteText` — gate textual das ações físicas;
- `Tmp_NormalizedFilePath` — path validado;
- `Tmp_ReportFolderPath` / `Tmp_ReportFilePath` — bridge efêmero;
- `Tmp_JcmEnsureResult` / `Tmp_JcmEnsureResultJson` — preparação JCM;
- `Tmp_JcmReadyText` — gate após JCM;
- `Tmp_ShellReportJson` — resultado bruto do executor;
- `Tmp_JcmDeleteResult` / `Tmp_JcmDeleteResultJson` — limpeza JCM;
- `Tmp_ResultJson` — Resultado serializado.

## Corpo passo a passo

### Grupo 01 — Preparar integridade

1. **JavaScript — Validar operação e caminho**
   - engine: `JetPack JavascriptEngine`;
   - saída: `Tmp_WorkJson`;
   - aceita somente `calculate_sha256` e `verify_sha256`;
   - normaliza barras;
   - restringe o path a `/storage/emulated/0/Documents/CDXMS_Solutions/`;
   - bloqueia traversal e caracteres capazes de alterar o shell;
   - valida `Expected SHA-256` em `verify_sha256`;
   - cria nome aleatório para o relatório temporário;
   - em erro, monta `pre_result` e desativa a execução física.

2. **JavaScript — Extrair flag de execução**
   - lê `Tmp_WorkJson.should_execute`;
   - grava `true` ou `false` em `Tmp_ShouldExecuteText`.

3. **JavaScript — Extrair caminho validado**
   - saída: `Tmp_NormalizedFilePath`.

4. **JavaScript — Extrair pasta temporária**
   - saída: `Tmp_ReportFolderPath`;
   - valor sob `cache/file_integrity/runtime`.

5. **JavaScript — Extrair relatório temporário**
   - saída: `Tmp_ReportFilePath`.

### Grupo 02 — Calcular SHA-256

6. **Action Block — `[CDXMS] Json Config Manager`**
   - operação: `ensure_folder`;
   - Folder Path: `Tmp_ReportFolderPath`;
   - executa somente quando `Tmp_ShouldExecuteText = true`;
   - saída: `Tmp_JcmEnsureResult`.

7. **JSON Output — Serializar preparação JCM**
   - `Tmp_JcmEnsureResult` → `Tmp_JcmEnsureResultJson`.

8. **JavaScript — Extrair disponibilidade do cache**
   - confirma `Tmp_JcmEnsureResult.success = true`;
   - saída: `Tmp_JcmReadyText`.

9. **Shell Script — Calcular SHA-256 homologado**
   - comando fixo: `/system/bin/sha256sum`;
   - non-root: `true`;
   - Helper: `false`;
   - Shizuku: `false`;
   - timeout: `30 segundos`;
   - constraints: `Tmp_ShouldExecuteText = true` e `Tmp_JcmReadyText = true`;
   - verifica existência, arquivo regular, leitura e disponibilidade do executor;
   - extrai o primeiro token, normaliza para lowercase e exige 64 hexadecimais;
   - escreve somente o relatório JSON efêmero.

10. **Read File — Ler relatório de integridade**
    - All Files Access: `true`;
    - path: `Tmp_ReportFilePath`;
    - saída: `Tmp_ShellReportJson`.

11. **Action Block — `[CDXMS] Json Config Manager`**
    - operação: `delete_file`;
    - File Path: `Tmp_ReportFilePath`;
    - saída: `Tmp_JcmDeleteResult`.

12. **JSON Output — Serializar limpeza JCM**
    - `Tmp_JcmDeleteResult` → `Tmp_JcmDeleteResultJson`.

### Grupo 03 — Finalizar Resultado

13. **JavaScript — Consolidar Resultado**
    - se houver `pre_result`, retorna-o sem executar checksum;
    - classifica `FILE_NOT_FOUND`, `PERMISSION_DENIED`, executor indisponível, falha de execução e saída inválida;
    - em `verify_sha256`, compara esperado e calculado;
    - mismatch retorna `CHECKSUM_MISMATCH` e nunca sucesso;
    - inclui estado de limpeza sem mascarar o resultado do hash;
    - saída: `Tmp_ResultJson`.

14. **JSON Parse — Publicar Resultado**
    - `Tmp_ResultJson` → `Resultado`.

15. **Exit Action Block**
    - encerramento explícito.
