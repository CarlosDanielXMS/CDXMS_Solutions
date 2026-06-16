# Relatório de Validação — JCM v1.0.0

## Export MacroDroid

- macroExportVersion: 1
- macro.isActionBlock: True
- macro.m_name: [CDXMS] Json Config Manager
- globalVariables: 0
- entradas públicas: Operation, File Path, Folder Path, Json Path, Value Json, Default Json, Create If Missing?, Pretty Print?, Merge Strategy
- saídas públicas: Resultado
- total de ações: 119

## Contagem de ações

```json
{
  "ActionGroupAction": 3,
  "JavaScriptAction": 25,
  "JsonParseAction": 6,
  "ActionGroupEndAction": 3,
  "IfConditionAction": 13,
  "ShellScriptAction": 4,
  "WriteToFileAction": 26,
  "ElseIfConditionAction": 10,
  "ElseAction": 9,
  "EndIfAction": 13,
  "ReadFileAction": 6,
  "ExitActionBlockAction": 1
}
```

## Decisões validadas

- Saída pública única: `Resultado`.
- Nenhuma variável `Tmp_*` está marcada como saída.
- `Resultado.data` permanece dicionário oficial.
- Não há `data_json`, `error_code`, `error_message` ou `error_json` no contrato.
- Json Path vazio/$ retorna documento completo.
- `a.b[id="x"].name` é suportado pela engine.
- Escritas/merges ambíguos são bloqueados.
- Export fica em `capabilities/json_config_manager/macrodroid/`.

## Observação

Validação estrutural feita em JSON exportado e teste local da engine JavaScript de referência. A homologação final ainda exige importação e execução no MacroDroid real.
