# [CDXMS] Remote Source Manager v1.0.0

Capability responsável pela fronteira remota do ecossistema CDXMS durante a homologação com GitHub raw.

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
- download em lote de payloads;
- declaração falsa de checksum verificado.

## Escopo v1.0.0

A versão inicial cobre o plano de controle remoto: catálogo, release manifest, remote manifest e JSON CDXMS genérico. Payloads de artifact continuam bloqueados até a homologação de SHA-256 nativo ou de capability específica, conforme a Knowledge Base.

## Dependência

- `[CDXMS] Json Config Manager >= 1.0.0`.

## Saída

Saída pública única: `Resultado`.

## Correções de homologação no dispositivo

- O preflight e a finalização JavaScript são executados em IIFE, evitando `Illegal return statement`.
- URL, flag de execução e paths de staging são materializados em variáveis escalares antes das ações nativas.
- Operações `validate_source` e `get_source_status` retornam o preflight sem executar HTTP.

## Correção verificada na homologação remota

Os JavaScripts de preflight e finalização usam uma variável de saída e a última expressão do script. Não utilizam `return` no escopo principal nem dependem do valor de retorno de uma IIFE para preencher a variável configurada no `JavaScriptAction`.


## Ponte de Resultado de preflight

Operações sem rede armazenam o Resultado como objeto em `Tmp_RequestWork.pre_result`. O Resultado não é encapsulado como JSON textual dentro de outro JSON, porque o Magic Text do MacroDroid pode alterar escapes durante a interpolação em `JavaScriptAction`.

## Persistência HTTP validada por export real

A configuração interna da ação `HTTP Request` foi alinhada ao export produzido pela mesma versão do MacroDroid usada na homologação:

- `saveResponseType = 2`;
- `saveResponseUseAllFilesAccess = true`;
- `saveResponseAllFilesAccessPath = {lv=Tmp_StagingFilePath}`;
- `saveResponseFileName = ""`.

No modo **All Files Access**, o campo serializado `saveResponseAllFilesAccessPath` recebe o caminho completo do arquivo de destino. Separar pasta e nome do arquivo fez a requisição retornar HTTP 200 sem persistir o corpo.
