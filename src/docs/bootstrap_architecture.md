# Bootstrap — Arquitetura de Entrada Única v1.0.0

## Decisão oficial

A distribuição v1 do CDXMS usa **uma única macro permanente** como ponto de entrada:

```text
[CDXMS] Solutions Manager
```

Não existe uma macro Installer separada na arquitetura v1. Na primeira execução, o Solutions Manager atua como orquestrador do bootstrap. Nas execuções seguintes, atua como manager do ecossistema.

```text
Primeira execução -> modo bootstrap
Execuções seguintes -> modo manager
```

## Papel do Bootstrap

`[CDXMS] Bootstrap` permanece uma capability local e minimalista. Ele:

- inicializa o core e a estrutura de runtime;
- verifica o core;
- repara o core de forma controlada;
- carrega contexto local;
- retorna o estado do ecossistema;
- depende diretamente somente do `[CDXMS] Json Config Manager`.

O Bootstrap não é uma macro instaladora, não baixa artifacts, não importa macros e não substitui o Solutions Manager.

## Dispositivo vazio

A macro `[CDXMS] Solutions Manager` deverá ser importável em um MacroDroid sem qualquer componente CDXMS pré-existente. Para isso, o export da macro conterá os Action Blocks essenciais em `exportedActionBlocks`.

O primeiro gate técnico é comprovar a cadeia mínima:

```text
uma macro importada
  -> Bootstrap incorporado
      -> Json Config Manager incorporado
          -> estrutura local criada e relida
```

Nenhuma dependência CDXMS previamente importada pode ser necessária para essa prova.

## Bootstrap offline

A inicialização local deve concluir sem internet. Recursos remotos entram somente após o core local estar válido.

```text
Solutions Manager
  -> Bootstrap.get_status
  -> Bootstrap.initialize_ecosystem
  -> Bootstrap.verify_core
  -> Bootstrap.ensure_runtime
  -> estado local ready
  -> sincronização remota opcional
```

## Idempotência

- `initialize_ecosystem` pode ser executado mais de uma vez;
- seeds válidos não devem ser destruídos;
- arquivos de usuário não devem ser sobrescritos sem política explícita;
- uma interrupção deve resultar em estado reparável;
- falha de internet não pode invalidar um runtime local saudável.

## Importação de artifacts

A arquitetura não presume importação automática de `.macro` ou `.ablock`. Até existir homologação específica, a instalação de solutions seguirá importação manual guiada e receipt de confirmação.

## Prova de arquitetura

A macro temporária `[CDXMS] Homologar Entrada Única Bootstrap v1.0.0 TEMP` incorpora versões temporárias, com GUIDs exclusivos, de Bootstrap e JCM. Ela comprova:

1. resolução do Bootstrap incorporado;
2. chamada transitiva do JCM incorporado;
3. inicialização idempotente;
4. verificação do core;
5. preparação do runtime;
6. releitura direta do marcador raiz pelo JCM;
7. estado final `ready`.

A prova não implementa o Solutions Manager final e não acessa o GitHub.
