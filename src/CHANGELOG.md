# Changelog

## 1.0.0 — Entrada única preparada para homologação

- Formalizada `[CDXMS] Solutions Manager` como única macro permanente da arquitetura v1.
- Removido o Installer separado do fluxo oficial da v1.
- Definido modo bootstrap na primeira execução e modo manager nas demais.
- Bootstrap permanece capability local, offline e dependente apenas do JCM.
- Preparada `[CDXMS] Homologar Entrada Única Bootstrap v1.0.0 TEMP` com Bootstrap e JCM incorporados por GUIDs exclusivos.
- A macro exige `7/7` verificações e não usa HTTP, Shell, payloads ou importação automática.
- File Integrity formalizado como homologado com `11/11` verificações.
- Solutions Manager completo, UI, payload verificado e importação guiada permanecem nas próximas fases.
- Base remota consultada: `feat/create-ecosystem-core@626c37a02fe0beb5b806b4df33f801749ba6bf9b`.

## 1.0.0 — File Integrity preparada para homologação

- Homologado `/system/bin/sha256sum` no dispositivo com `7/7` verificações.
- Contexto aprovado: non-root, sem MacroDroid Helper e sem Shizuku.
- Criada `[CDXMS] File Integrity` com `calculate_sha256` e `verify_sha256`.
- Paths ficam restritos ao base path CDXMS e caracteres de shell são bloqueados.
- O comando é fixo e o Resultado valida existência, leitura, exit code e digest de 64 hexadecimais.
- Mismatch retorna `CHECKSUM_MISMATCH` e nunca falso sucesso.
- JCM prepara e remove o relatório efêmero do bridge Shell Script.
- Adicionada macro TEMP com 11 verificações para homologar a capability de produção.
- RSM e payloads continuam bloqueados até essa homologação e integração posterior.

## 1.0.0 — Probe SHA-256 v1.0.1 corrige o contexto Shell Script

- A tentativa v1.0.0 foi inconclusiva: o relatório fallback não foi sobrescrito e nenhum candidato SHA-256 chegou a ser testado.
- O resultado anterior não significa ausência de SHA-256 no dispositivo.
- Corrigido `ShellScriptAction.useHelper` de `true` para `false`, alinhando o harness ao export nativo auditado do MacroDroid.
- Adicionados `probe_stage=fallback|shell_started|completed` e `shell_execution_confirmed` para diagnóstico observável.
- O shell sobrescreve o relatório no primeiro comando e grava o relatório completo apenas ao final.
- Mantidos non-root, sem Shizuku, sem instalação, sem registry e sem payloads remotos.

## 1.0.0 — Harness de homologação SHA-256 em runtime preparado

- Mantida versão pré-release `1.0.0`.
- Base: `feat/create-ecosystem-core@19564636b8eb90f97ed4c3460ebdea1648c3a444`.
- Adicionada a macro temporária `[CDXMS] Homologar SHA-256 Runtime v1.0.1 TEMP`.
- O harness testa cinco candidatos sem assumir previamente qual existe no dispositivo.
- Exige sete verificações: valor conhecido, determinismo, conteúdo alterado, arquivo vazio, path com espaços, arquivo multi-bloco e rejeição de arquivo inexistente.
- O shell é não-root, executa sem Helper e grava somente em `cache/`.
- Nenhuma capability de produção foi criada; payloads, instalação e registry permanecem bloqueados.
- Adicionado validador estático e de execução host para impedir regressões no harness.
- A homologação real permanece pendente até execução no dispositivo.

## 1.0.0 — Homologação do Remote Source Manager encerrada

- Mantida versão pré-release `1.0.0`.
- Homologação real concluída em `2026-06-20` com `[CDXMS] Homologar Remote Source Manager v1.0.6 TEMP`.
- Aprovadas `23/23` verificações: `0` falhas.
- Confirmados preflight sem rede, validações de segurança, HTTP 200, persistência física no staging, releitura JCM, tratamento de HTTP 404 e preservação do registry.
- Source ref exercitado: `aad55e5969b41c456bb92e096bde2c381101e385`.
- Head remoto na formalização: `d79fa8cbed54048900fcb12fcb873408b7a70478`.
- `manual_homologation_required` alterado para `false` somente para o escopo de documentos JSON do plano de controle.
- Payloads de artifacts, SHA-256 em runtime, instalação remota e importação automática permanecem fora do escopo homologado.
- A macro temporária de homologação permanece somente como evidência e não integra catálogo ou release.

## 1.0.0 — Persistência HTTP alinhada ao export real do MacroDroid

- Mantida versão pré-release `1.0.0`.
- Base revisada no head remoto `aad55e5969b41c456bb92e096bde2c381101e385`.
- Confirmado em export real e execução no dispositivo que `saveResponseAllFilesAccessPath` recebe o caminho completo do arquivo.
- `saveResponseFileName` permanece vazio no modo All Files Access.
- Corrigido o RSM para persistir efetivamente o corpo de respostas HTTP 200 no staging.
- Adicionadas regressões estáticas para impedir retorno ao formato pasta + nome separado.



- Corrigida a ponte interna do RSM: `pre_result` agora é objeto, eliminando `pre_result_json` e a perda de escapes ao interpolar Magic Text em JavaScript.
## 1.0.0 — Correção verificada do bridge RSM/JCM

- Base revisada diretamente no head remoto `aad55e5969b41c456bb92e096bde2c381101e385`.
- Corrigido o JCM: flags usadas por constraints booleanas nativas voltam a ser booleanas.
- JavaScripts do JCM interpretam também `Verdadeiro`/`Falso` quando recebem Magic Text localizado.
- Corrigido o RSM: preflight e finalização publicam resultado pela última expressão, sem depender de IIFE.
- Adicionada validação regressiva do bridge entre JavaScript, JsonParseAction e constraints nativas.
- Mantida versão pré-release `1.0.0`.

## 1.0.0 — Correções de homologação RSM/JCM

- Mantida versão pré-release `1.0.0`.
- Corrigido `Illegal return statement` no preflight do Remote Source Manager.
- Finalização do RSM agora retorna explicitamente o Resultado em todos os fluxos.
- Mantida ponte escalar para URL e paths usados pelas ações nativas.
- JCM passa a serializar flags internas como `true`/`false`, evitando localização `Verdadeiro`/`Falso` e falsos `PERMISSION_DENIED`.
- Adicionadas validações regressivas para esses dois pontos.

## 1.0.0 — Remote Source Manager

- Mantida versão pré-release `1.0.0`.
- Implementado `[CDXMS] Remote Source Manager` com HTTP Request nativo.
- Adicionadas operações de validação de fonte, status, catálogo, release manifest, remote manifest e JSON de controle.
- Downloads passam primeiro por staging em `packages/downloaded/remote_source_manager/`.
- Código HTTP e headers são capturados; schema, namespace e identidade são validados.
- Staging é relido/verificado pelo Json Config Manager.
- Nenhuma instalação, alteração de registry ou apply final é executada pela capability.
- Bulk payload download e checksum SHA-256 em runtime permanecem bloqueados até homologação específica, evitando falso senso de integridade.

## 1.0.0 — Remote distribution readiness corrigida

- Mantida versão pré-release `1.0.0`.
- Package reconstruído como base completa mesclada, não delta.
- Artifact Manager consolidado para apply físico exclusivamente via JCM.
- Remote manifests padronizados sem quebra do schema v1.
- Adicionados `catalogs/sources.json` e `catalogs/local_catalog.default.json`.
- Homologação remota definida em `develop`.
- `release.json` preserva `artifacts[].path` e adiciona `remote_manifest_path`.
- Removida a proposta prematura de três canais e múltiplos catálogos paralelos.
- Mantida distribuição por arquivos raw individuais; ZIP remoto e importação automática permanecem fora de escopo.

## 1.0.0 — Base anterior

- JCM, Bootstrap, Result Manager, Logger e String Utils.
- Artifact Manager e Dependency Resolver.
- Contrato universal `Resultado`.
- Auditoria e validações pré-release.
