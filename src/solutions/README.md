# Solutions

Diretório das macros orquestradoras permanentes do ecossistema CDXMS.

## Regras

- macros são `solutions`;
- Action Blocks reutilizáveis são `capabilities`;
- uma solution coordena capabilities e não reimplementa seus domínios;
- toda solution publica somente `Resultado` no contrato universal CDXMS.

## Entrada permanente v1

`[CDXMS] Solutions Manager` é a única macro permanente importada pelo usuário.

## Solution de homologação

`[CDXMS] Test Solution` é o primeiro artifact baixável pelo Manager. Ela valida Bootstrap, Builder, renderer e identidade visual JUIF sem executar operações destrutivas.

## Unidades de distribuição

O ecossistema possui duas fronteiras diferentes:

| Unidade | Distribuição | Instalação |
|---|---|---|
| JSON, config, catálogo, assets e dados | GitHub raw/release | automática após staging e checksum |
| `.macro` e `.ablock` | Template Store ou release GitHub | importação explícita pelo usuário |

Baixar um export para `/Documents/CDXMS_Solutions` não o registra no MacroDroid. Nenhuma solution pode declarar-se instalada apenas porque o arquivo existe no filesystem.

## Padrão para solutions próprias ou de terceiros

Cada solution distribuível deve possuir, no mínimo:

```text
solutions/<solution_id>/
  manifest.json
  contract.json
  config.default.json
  body.md
  README.md
  macrodroid/
    [CDXMS]_Nome.macro
  tests/
    manual_test.md
```

Arquivos adicionais só devem existir quando houver uso real, como `ui_schema.default.json`, `rules.default.json`, `selectors.default.json` ou assets.

O manifest deve declarar:

- id em `snake_case` e versão SemVer;
- capabilities realmente invocadas pelo export;
- modo de entrega do export;
- permissões e efeitos colaterais;
- compatibilidade mínima do core e do MacroDroid;
- política de atualização e preservação de config;
- status de homologação.

## Regras de engenharia

1. Preferir ações nativas antes de JavaScript, Shell ou UI Interaction.
2. Usar Action Block somente para responsabilidade reutilizável e coesa.
3. Manter lógica de orquestração na macro e lógica técnica nas capabilities.
4. Usar variáveis locais; globais apenas para estado compartilhado mínimo.
5. Publicar uma única saída lógica `Resultado`.
6. Validar antes de qualquer side effect e verificar depois de toda persistência.
7. Tratar cancelamento, timeout, execução duplicada, modo offline e permissão negada.
8. Não armazenar segredos em config default, catálogo, log ou export público.
9. Não usar URLs GitHub `/blob/`; downloads usam `raw.githubusercontent.com` ou assets de release.
10. Não editar GUIDs e estrutura interna de exports sem validação e homologação no MacroDroid.

## Empacotamento de dependências

Uma solution que precisa funcionar em dispositivo vazio deve incorporar em `macro.exportedActionBlocks` a closure transitiva das capabilities usadas. O validador deve provar:

- nome e GUID das referências;
- ausência de dependência invocada e não incorporada;
- ausência de bloco incorporado duplicado;
- coerência entre `requires.capabilities` e chamadas `ActionBlockAction`;
- ausência de globais indevidas.

## Processo de publicação

```text
modelar contrato
  -> implementar no MacroDroid
  -> exportar
  -> validar estrutura e dependências
  -> testar importação limpa
  -> testar fluxo e rollback
  -> atualizar manifests/checksums
  -> publicar primeiro como pré-release
  -> promover para ref imutável após homologação
```
