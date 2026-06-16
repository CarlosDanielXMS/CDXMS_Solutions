# Corpo do Action Block — [CDXMS] Json Config Manager v1.0.0

## Entradas

| Entrada | Tipo | Obrigatória | Exemplos / opções | Descrição |
|---|---|---:|---|---|
| Operation | Texto | Sim | ensure_core, read_json, merge_json | Operação técnica executada pelo JCM. |
| File Path | Texto | Condicional | core/settings.json; capabilities/mdf/config.json | Arquivo JSON alvo, relativo ou absoluto dentro do base_path. |
| Folder Path | Texto | Condicional | core; capabilities/logger | Pasta usada por ensure_folder ou escrita. |
| Json Path | Texto | Não | $, settings.language, config.services[id="teste"].name | Caminho lógico dentro do JSON. Vazio/$ indica documento completo. |
| Value Json | Texto JSON | Condicional | {"enabled":false}, "pt-BR", true | Valor usado por validate_json, write_json e merge_json. |
| Default Json | Texto JSON | Condicional | {}, {"schema_version":1} | Conteúdo inicial para ensure_file. |
| Create If Missing? | Booleano | Não | true/false | Autoriza ensure_file a criar arquivo ausente. |
| Pretty Print? | Booleano | Não | true/false | Formata JSON gravado. |
| Merge Strategy | Texto | Condicional | deep_merge, preserve_existing, overwrite_existing, replace | Estratégia de merge_json. |

## Saída

| Saída | Tipo | Descrição |
|---|---|---|
| Resultado | Dicionário | Saída pública única no contrato universal. |

## Variáveis de trabalho

- Tmp_WorkJson
- Tmp_Work
- Tmp_FileContent
- Tmp_WriteWorkJson
- Tmp_WriteWork
- Tmp_ResultJson

Nenhuma variável `Tmp_*` é saída pública.

## Corpo passo a passo

1. **Action Group — Initialize Runtime**
   - JavaScriptAction: normaliza entradas, paths e opções; valida escopo do path; gera `Tmp_WorkJson`.
   - JsonParseAction: converte `Tmp_WorkJson` para `Tmp_Work`.

2. **Action Group — Dispatch Operation**
   - If/Else If por `Tmp_Work[operation]`, sem restrições repetidas.
   - Branches:
     - ensure_core
     - repair_core
     - ensure_folder
     - validate_json
     - read_json
     - exists
     - write_json
     - merge_json
     - ensure_file
     - backup_file
     - delete_file

3. **read_json / exists**
   - ReadFileAction lê `File Path` para `Tmp_FileContent`.
   - JavaScriptAction interpreta JSON, aplica JCM JsonPath Engine v1 e monta `Tmp_ResultJson`.
   - `Json Path` vazio/$ retorna documento completo.

4. **write_json / merge_json**
   - ReadFileAction lê arquivo atual quando existir.
   - JavaScriptAction valida `Value Json`, resolve JsonPath, bloqueia múltiplos alvos, prepara `Tmp_WriteWorkJson`.
   - JsonParseAction converte `Tmp_WriteWorkJson` para `Tmp_WriteWork`.
   - If `Tmp_WriteWork[should_write] = true`, WriteToFileAction grava `Tmp_WriteWork[write_content]`.
   - JavaScriptAction copia `Tmp_WriteWork[result_json]` para `Tmp_ResultJson`.

5. **Finalize Result**
   - JsonParseAction publica `Tmp_ResultJson` diretamente em `Resultado`.
   - ExitActionBlockAction encerra o bloco.
