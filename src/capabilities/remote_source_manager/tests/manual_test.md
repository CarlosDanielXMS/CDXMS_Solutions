# Homologação manual — [CDXMS] Remote Source Manager v1.0.0

## Resultado consolidado

- status: **homologado**;
- concluído em: `2026-06-20`;
- macro executada: `[CDXMS] Homologar Remote Source Manager v1.0.6 TEMP`;
- source ref: `aad55e5969b41c456bb92e096bde2c381101e385`;
- head remoto na formalização: `d79fa8cbed54048900fcb12fcb873408b7a70478`;
- verificações: `23/23` aprovadas;
- falhas: `0`.

A macro temporária é somente evidência de homologação e não integra catálogo, release ou runtime operacional.

## Pré-requisitos

1. Importar `[CDXMS] Json Config Manager`.
2. Importar `[CDXMS] Remote Source Manager`.
3. Conceder acesso a arquivos/documentos ao MacroDroid.
4. Garantir acesso à internet.

## Caso 1 — validate_source

- Operation: `validate_source`
- Source Json: vazio
- Source Id: `cdxms_official_github`

Esperado:

- `Resultado.success = true`;
- `Resultado.data.source.type = github_raw`;
- nenhuma chamada HTTP;
- nenhum arquivo criado.

## Caso 2 — fonte /blob/ inválida

Informar Source Json com `base_raw_url` contendo `/blob/`.

Esperado:

- `Resultado.success = false`;
- `Resultado.error.code = REMOTE_SOURCE_INVALID`;
- nenhuma chamada HTTP.

## Caso 3 — fetch_catalog

- Operation: `fetch_catalog`
- Source Json: vazio
- Remote Path: vazio

Esperado:

- HTTP status 200;
- `schema_version = 1`;
- `namespace = CDXMS`;
- `file_type = local_catalog`;
- `Resultado.data.validation.valid = true`;
- arquivo criado em `packages/downloaded/remote_source_manager/cdxms_official_github/`;
- `Resultado.data.cache.verified_by = json_config_manager`.

## Caso 4 — fetch_release_manifest

- Operation: `fetch_release_manifest`

Esperado:

- status 200;
- `artifact_type = package`;
- versão presente;
- staging verificado pelo JCM.

## Caso 5 — fetch_remote_manifest

- Operation: `fetch_remote_manifest`
- Remote Path: `capabilities/json_config_manager/remote_manifest.json`

Esperado:

- `file_type = remote_artifact_manifest`;
- sucesso e cache staging validado.

## Caso 6 — path inseguro

- Operation: `fetch_json`
- Remote Path: `../core/errors.json`

Esperado:

- erro antes do HTTP;
- `REMOTE_SOURCE_INVALID` ou erro de preflight com detalhe de Remote Path.

## Caso 7 — 404

- Operation: `fetch_json`
- Remote Path: `catalogs/inexistente.json`

Esperado:

- `Resultado.success = false`;
- `Resultado.error.code = HTTP_UNEXPECTED_STATUS`;
- status 404 registrado em `Resultado.data.http.status_code`.

## Caso 8 — confirmar ausência de efeitos indevidos

Após os testes:

- nenhum arquivo deve ter sido aplicado em `core/`, `capabilities/` ou `solutions/`;
- nenhum registry deve ter sido alterado;
- somente staging em `packages/downloaded/remote_source_manager/` é permitido.

## Critério de conclusão

Critério atendido: os casos 1–8 e as regressões complementares foram executados no dispositivo com `23/23` verificações aprovadas. `manual_homologation_required` permanece `false` para o escopo do plano de controle homologado.

## Regressões obrigatórias da homologação

- `validate_source` e `get_source_status` não podem retornar `HTTP_REQUEST_FAILED` nem executar rede.
- Nenhum JavaScriptAction pode gerar `Illegal return statement`.
- `Resultado.data.source` e `Resultado.data.request` não podem ficar vazios quando as entradas são válidas.
- O JCM deve aceitar paths válidos mesmo quando o idioma do MacroDroid exibe booleanos como `Verdadeiro`/`Falso`.

## Regressão — Resultado de preflight sem JSON aninhado

1. Execute `validate_source` com fonte válida.
2. Confirme que nenhuma ação HTTP é executada.
3. Confirme `Resultado.success = true` e a presença de `Resultado.data.source`.
4. Execute `get_source_status` e confirme o mesmo comportamento.
5. O export não pode conter `pre_result_json`; o contexto interno deve usar `pre_result` como objeto.

## Evidência do schema de salvamento HTTP

Um export mínimo criado diretamente no MacroDroid e executado com sucesso confirmou:

```json
{
  "saveResponseType": 2,
  "saveResponseUseAllFilesAccess": true,
  "saveResponseAllFilesAccessPath": "/caminho/completo/probe.json",
  "saveResponseFileName": ""
}
```

No RSM, o equivalente dinâmico obrigatório é:

```json
{
  "saveResponseAllFilesAccessPath": "{lv=Tmp_StagingFilePath}",
  "saveResponseFileName": ""
}
```

A homologação deve falhar se a action voltar a separar pasta e nome nesses dois campos.
