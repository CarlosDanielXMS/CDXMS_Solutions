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
