# Corpo — [CDXMS] String Utils v1.0.0

## Entradas

| Entrada | Tipo | Obrigatória | Descrição |
|---|---:|---:|---|
| Operation | Texto | Sim | Operação técnica da String Utils. |
| Text | Texto | Condicional | Texto principal usado pela operação. |
| Search Text | Texto | Condicional | Texto de busca usado por substituição/comparação. |
| Replace Text | Texto | Condicional | Texto substituto de `replace_text`. |
| Regex Pattern | Texto | Não | Regex opcional para `replace_text`. |
| Regex Flags | Texto | Não | Flags de regex; `g` é adicionado quando ausente. |
| Case Mode | Texto | Não | `none`, `lower`, `upper`, `title`. |
| Comparison Mode | Texto | Não | `case_sensitive`, `case_insensitive`, `normalized`. |
| Separator | Texto | Não | Reservado para compatibilidade. |
| Max Length | Texto | Não | Comprimento máximo opcional. |
| Allow Slash? | Booleano | Não | Permite preservar `/` em `sanitize_path_segment`. |
| Strict Mode? | Booleano | Não | Reservado para validação rígida. |
| Config Json | Texto JSON | Não | Configuração completa opcional. |
| Context Json | Texto JSON | Não | Contexto propagado ao Result Manager. |
| Session Id | Texto | Não | Sessão propagada para `Resultado.meta`. |
| Correlation Id | Texto | Não | Correlação propagada para `Resultado.meta`. |

## Saída

| Saída | Tipo | Descrição |
|---|---:|---|
| Resultado | Dicionário | Saída pública única conforme contrato universal CDXMS. |

## Variáveis de trabalho

| Variável | Tipo | Descrição |
|---|---:|---|
| Tmp_StringWorkJson | Texto | JSON intermediário com sucesso/status/mensagem/data/error. |
| Tmp_StringWork | Dicionário | Dicionário derivado de `Tmp_StringWorkJson` para mapear a chamada ao Result Manager. |

## Corpo passo a passo

### Ação 1 — Action Group: `01 — Transform Text`

Agrupa a transformação textual local. A capability permanece pura e sem efeitos colaterais.

Configurações:

- Nome do grupo: `01 — Transform Text`
- Logging: habilitado
- Restrições: nenhuma

### Ação 2 — JavaScript

Executa o dispatch por `Operation`, valida entradas estruturais e gera `Tmp_StringWorkJson`.

Configurações:

- Engine: `JetPack JavascriptEngine`
- Bloquear próxima ação até finalizar: `true`
- Variável de saída texto: `Tmp_StringWorkJson`
- Script: engine interna da String Utils v1.0.0
- Restrições: nenhuma

Responsabilidades:

- validar `Operation`;
- executar transformação/comparação;
- retornar `success`, `status`, `result_message`, `data_json` e `error_json`;
- não montar `Resultado` final manualmente.

### Ação 3 — JSON Parse

Converte o JSON intermediário para dicionário.

Configurações:

- Entrada string: `Tmp_StringWorkJson`
- Saída dicionário: `Tmp_StringWork`
- Keys: vazio, parse completo

### Ação 4 — End Action Group

Encerra o grupo `01 — Transform Text`.

### Ação 5 — Action Group: `02 — Build Resultado`

Agrupa a publicação do resultado final.

Configurações:

- Nome do grupo: `02 — Build Resultado`
- Logging: habilitado
- Restrições: nenhuma

### Ação 6 — Action Block: `[CDXMS] Registrar Resultado`

Finaliza a saída pública usando o Result Manager.

Configurações de entrada:

| Entrada do Result Manager | Valor |
|---|---|
| Operation | `build_result` |
| Source Artifact Type | `capability` |
| Source Artifact Id | `string_utils` |
| Source Operation | `{lv=Operation}` |
| Success? | `{lv=Tmp_StringWork[success]}` |
| Status | `{lv=Tmp_StringWork[status]}` |
| Message | `{lv=Tmp_StringWork[result_message]}` |
| Data Json | `{lv=Tmp_StringWork[data_json]}` |
| Error Json | `{lv=Tmp_StringWork[error_json]}` |
| Result Json | vazio |
| Context Json | `{lv=Context Json}` |
| Strict Mode? | `true` |
| Include Raw Result? | `false` |
| Session Id | `{lv=Session Id}` |
| Correlation Id | `{lv=Correlation Id}` |

Configurações de saída:

| Saída do Result Manager | Variável local |
|---|---|
| Resultado | `Resultado` |

### Ação 7 — End Action Group

Encerra o grupo `02 — Build Resultado`.

### Ação 8 — Exit Action Block

Encerra explicitamente após publicar `Resultado`.
