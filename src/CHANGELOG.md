# Changelog

## 1.0.0 — Capabilities de UI preparadas para homologação

- Incorporados os protótipos `[CDXMS] Java UI Framework` e `[CDXMS] JUIF UI Builder` ao padrão de capability do ecossistema.
- Preservados os 26 componentes existentes e os contratos de pages, state, eventos, binding e mapping.
- Adicionados 10 componentes: `top_app_bar`, `bottom_navigation`, `navigation_rail`, `navigation_drawer`, `tab_bar`, `search_bar`, `chip`, `chip_group`, `empty_state` e `loading_indicator`.
- Adicionado `ui.shell` opcional para chrome persistente sem quebrar layouts legados.
- Entradas e variáveis de trabalho foram renomeadas para as convenções CDXMS.
- Saída pública única `Resultado` mantida em ambas as capabilities.
- Artifact id do renderer normalizado de `mdf` para `java_ui_framework`.
- Adicionados manifest, contract, config, remote manifest, catálogo de componentes, documentação e validações.
- As capabilities permanecem `ready_for_homologation`; nenhuma homologação real foi declarada.


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

## Histórico anterior

O histórico detalhado anterior permanece no repositório remoto e não foi alterado semanticamente por esta entrega.
