# Arquitetura — [CDXMS] Solutions Manager v1.0.0

## Objetivo

Oferecer uma única macro permanente para inicializar, diagnosticar e gerenciar o ecossistema CDXMS em um dispositivo vazio ou já preparado.

## Princípios

1. A primeira execução usa o runtime incorporado para preparar o core offline.
2. As execuções seguintes operam como gerenciador.
3. Não existe Installer separado na v1.
4. O Manager apenas orquestra capabilities.
5. JCM é o único executor físico de JSON e filesystem.
6. RSM baixa somente para staging; FI valida; DR planeja dependências; AM planeja lifecycle.
7. Copiar `.macro` ou `.ablock` não equivale a importá-los no MacroDroid.
8. Toda resposta pública segue `core/result_contract.json`.

## Unidade de entrada

O usuário importa uma única macro: o próprio Solutions Manager. O export incorpora a closure das 11 capabilities v1. Na primeira execução ele chama Bootstrap antes da interface. Nas execuções seguintes a mesma chamada idempotente apenas valida/repara a base mínima necessária.

Uma macro instaladora separada foi descartada porque download de arquivo não produz importação automática no MacroDroid.

## Pipeline de lançamento

```text
launch
  -> Bootstrap.initialize_ecosystem (idempotente, Load Context? = true)
  -> validate_ecosystem
  -> carregar cache local
  -> opcionalmente RSM.fetch_catalog + fetch_release_manifest
  -> compor modelo de dashboard
  -> JUIF UI Builder.build_ui
  -> Java UI Framework.render_ui
```

## Pipeline futuro de lifecycle

```text
seleção da UI
  -> event bridge
  -> RSM.fetch_remote_manifest
  -> FI.verify_file / verify_manifest
  -> DR.build_resolution_plan
  -> AM.build_install_plan
  -> JCM executa jcm_apply_plan
  -> AM.verify_local_apply
  -> atualizar registry
  -> atualizar UI
```

## Estado do event bridge

A UI publica eventos por broadcast Intent. O export atual recebe, valida e deduplica o envelope com `event_id`, `session_id`, `action`, `payload`, `current_page`, `state`, `created_at` e `consumed`.

O recebimento existe, mas o despacho das operações ainda não. Até a homologação em dispositivo e a implementação do pipeline de payload, `install_artifact`, `update_artifact`, `repair_artifact` e `uninstall_artifact` permanecem bloqueadas.
