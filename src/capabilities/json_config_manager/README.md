# [CDXMS] Json Config Manager v1.0.0

Tipo: capability / Action Block / kernel primitivo.  
Saída pública única: `Resultado`.

## Responsabilidade

O JCM manipula arquivos JSON locais dentro de `/storage/emulated/0/Documents/CDXMS_Solutions` e garante o core mínimo do ecossistema. Ele não instala artifacts, não registra artifacts e não resolve dependências; essas responsabilidades pertencem ao Bootstrap/Artifact Manager.

## Operações

- `ensure_core`
- `repair_core`
- `ensure_folder`
- `validate_json`
- `read_json`
- `exists`
- `write_json`
- `merge_json`
- `ensure_file`
- `backup_file`
- `delete_file`

## Entrada Json Path

`Json Path` vazio ou `$` retorna/opera sobre o documento completo.

Sintaxes suportadas pela JCM JsonPath Engine v1:

```text
$
settings.language
config.services[0]
config.services[id="teste"]
config.services[id="teste"].name
$.catalog.items[?(@.artifact_id=="mdf")].version
$..artifact_id
$.items[*].id
$.items[0:5]
$.items[0,2,4]
```

## Leitura de config completa

Para evitar custo de múltiplas chamadas, outras capabilities devem carregar config uma única vez:

```text
Operation = read_json
File Path = capabilities/mdf/config.json
Json Path = $
```

O documento completo retorna em:

```text
Resultado.data.value
Resultado.data.content
```

## Segurança de escrita

`read_json` e `exists` aceitam múltiplos matches. `write_json` e `merge_json` exigem raiz ou alvo único. Se o path resolver mais de um item, o JCM retorna `JSON_PATH_AMBIGUOUS_MATCH` e não grava.

## Contrato de Resultado

Não existem campos top-level como `data_json`, `error_code`, `error_message` ou `error_json`. Qualquer payload útil fica em `Resultado.data`.

## Saneamento pré-release v1.0.0

A capability permanece na versão `1.0.0`. Este ajuste registra a auditoria de ações nativas, JS e Shell antes da primeira release oficial.

- Política: `native_first_when_safe_clear_and_homologated`.
- JS: `25` ocorrência(s).
- Shell: `4` ocorrência(s).
- Decisão: Mantém ações nativas de leitura/escrita/parse onde elas já expressam a intenção; mantém JavaScript como engine interna de JsonPath/merge; mantém ShellScriptAction como fallback controlado para mkdir -p e rm -f até homologação real de FileOperationV21Action/FileOperationAllFilesAction com paths dinâmicos e criação recursiva.

