# Changelog

## 1.0.0 — Redesign profissional do JUIF

- Corrigida a arquitetura visual do shell: barras e navegação deixaram o conteúdo rolável e passaram a utilizar hosts persistentes.
- Implementados hosts para Top App Bar, Tab Bar, Navigation Rail, ScrollView, Bottom Navigation e Navigation Drawer.
- Navigation Drawer ganhou scrim, animação, fechamento contextual e itens descritivos.
- Refinados visualmente os dez componentes adicionados, alinhando-os ao tema dark gold do protótipo.
- Substituídas seleções genéricas por indicadores, superfícies e tipografia específicos de cada padrão de navegação.
- Catálogo padrão reorganizado em sete páginas.
- Removidas seis Tab Bars duplicadas e chaves `catalog_tabs_<pagina>`.
- Criada uma única chave `catalog_section`, com seleção resolvida pela página atual.
- Bottom Navigation passou a usar `active_pages` para manter Catálogo selecionado em todas as categorias.
- Shell passou a aceitar `visible_pages`, `hidden_pages`, `active_pages` e `active_prefix`.
- UI padrão cobre 36/36 componentes e 21 bindings.
- Default do Framework continua sendo gerado pelo JavaScript real do Builder.
- Parser BeanShell e validadores estruturais foram adicionados ao gate local.
- Homologação visual e interativa em dispositivo continua obrigatória.

## 1.0.0 — Correção das capabilities de UI

- Corrigidos Java UI Framework e JUIF UI Builder a partir do estado remoto atual.
- Removidos do Resultado os campos proibidos `data_json`, `error_code`, `error_message` e `error_json`.
- Resultado agora segue exatamente `core/result_contract.json`.
- Java UI Framework volta a usar a hierarquia-base e os bridges internos do protótipo funcional.
- Mantidos 26 componentes legados e 10 componentes adicionais.
- Shell passa a ser renderizado no conteúdo rolável nesta fase; rail/drawer permanecem componentes inline.
- Validadores passam a bloquear regressões no contrato universal.
- Homologação em dispositivo real continua obrigatória.

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
