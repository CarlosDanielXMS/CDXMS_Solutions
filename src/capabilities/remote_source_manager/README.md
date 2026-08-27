# [CDXMS] Remote Source Manager v1.0.0

Capability da fronteira remota do ecossistema CDXMS via GitHub raw. O plano de controle está homologado; o download restrito de exports MacroDroid é candidato a homologação no dispositivo.

## Estado de homologação

- status: **homologado**;
- escopo: documentos JSON de controle;
- data: `2026-06-20`;
- macro de evidência: `[CDXMS] Homologar Remote Source Manager v1.0.6 TEMP`;
- verificações: `23/23` aprovadas;
- source ref exercitado: `aad55e5969b41c456bb92e096bde2c381101e385`;
- head remoto na formalização: `d79fa8cbed54048900fcb12fcb873408b7a70478`.

A homologação concluída cobre transporte, persistência em staging, validação estrutural/semântica e releitura pelo JCM para documentos de controle. A operação incremental `fetch_macrodroid_export` adiciona download restrito de `.macro`/`.ablock` para staging e ainda exige homologação específica no dispositivo. Não cobre instalação, alteração de registry ou importação automática.

## Responsabilidade

- validar a fonte remota;
- montar URL raw segura;
- baixar documentos JSON de controle por **HTTP Request nativo**;
- capturar código HTTP e headers;
- salvar primeiro em staging temporário;
- validar schema, namespace e identidade do documento;
- reler/verificar o staging pelo `[CDXMS] Json Config Manager`;
- retornar `Resultado`.

## Não faz

- instalação de artifact;
- atualização de registry;
- resolução de dependências;
- apply no destino final;
- importação automática de `.macro`/`.ablock`;
- download em lote de payloads ou payloads fora de `.macro`/`.ablock`;
- declaração falsa de checksum verificado.

## Escopo v1.0.0

A versão inicial cobre catálogo, `release.json`, `remote_manifest.json`, JSON CDXMS genérico e, neste incremento, um único export `.macro`/`.ablock` para staging validado. Outros payloads permanecem bloqueados; a importação continua manual.

## Dependência

- `[CDXMS] Json Config Manager >= 1.0.0`.

## Saída

Saída pública única: `Resultado`.

## Comportamentos confirmados no dispositivo

- preflight e finalização publicam pela última expressão do `JavaScriptAction`;
- `validate_source` e `get_source_status` não executam HTTP;
- `pre_result` é objeto e não JSON textual aninhado;
- URL, flag de execução e paths de staging são materializados em variáveis escalares;
- host inválido, `/blob/`, fonte desabilitada, `Source Id` divergente, traversal e JSON inválido são bloqueados antes da rede;
- HTTP 200 persiste o corpo no staging e o JCM relê o arquivo;
- HTTP 404 retorna `HTTP_UNEXPECTED_STATUS`;
- registry permanece inalterado.

## Persistência HTTP homologada

Configuração confirmada por export real do MacroDroid e execução no dispositivo:

- `saveResponseType = 2`;
- `saveResponseUseAllFilesAccess = true`;
- `saveResponseAllFilesAccessPath = {lv=Tmp_StagingFilePath}`;
- `saveResponseFileName = ""`.

No modo **All Files Access**, `saveResponseAllFilesAccessPath` recebe o caminho completo do arquivo de destino.


## SHA-256 runtime homologado

O dispositivo confirmou `/system/bin/sha256sum` com `7/7` verificações em contexto non-root, sem Helper e sem Shizuku. A nova operação de export MacroDroid realiza validação estrutural e releitura JCM, mas não declara verificação SHA-256 nem instalação. Essa integração permanece como etapa posterior.
