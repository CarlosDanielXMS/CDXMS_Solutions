# Plano de testes manuais — Solutions Manager Foundation

## Fundação

- [ ] Manifest possui `artifact_type=solution` e id `solutions_manager`.
- [ ] Contrato publica apenas `Resultado`.
- [ ] Campos legados proibidos estão ausentes.
- [ ] As onze capabilities obrigatórias estão declaradas.
- [ ] Estado inicial é `starting`.
- [ ] Lifecycle mutável está bloqueado.

## Primeiro vertical slice

- [ ] Dispositivo vazio importa somente `[CDXMS] Solutions Manager`.
- [ ] A importação oferece/incorpora os 11 Action Blocks esperados sem GUIDs duplicados.
- [ ] Bootstrap e JCM incorporados executam sem componentes CDXMS preexistentes.
- [ ] São criados `.cdxms_root.json`, core mínimo e diretórios de runtime no path oficial.
- [ ] Segunda execução não recria nem reseta o core.
- [ ] Falha do Bootstrap exibe Toast e não tenta construir/renderizar a UI.
- [ ] Falha do Builder exibe Toast e não chama o renderer.
- [ ] A UI padrão abre, navega e fecha sem erro silencioso.
- [ ] A UI abre completa, com Dashboard, Catálogo, Detalhes, Instalados, Diagnóstico, Configurações, Sobre e Licenças.
- [ ] Execução sem rede continua abrindo a UI incorporada.

## Event bridge

- [ ] Evento contém `session_id` e `event_id`.
- [ ] Evento de outra sessão é ignorado.
- [ ] Evento duplicado é consumido uma única vez.
- [ ] Namespace, versão de protocolo, origem e allowlist divergentes são bloqueados.
- [ ] `Tmp_SmLastConsumedEventId` só muda após evento aceito.
- [ ] Falha de evento permanece visível e não fecha silenciosamente a UI.
- [ ] `download_test_solution` chega ao Manager por broadcast explícito e é despachado uma única vez.

## Download da Solution de Teste

- [ ] O botão de download chama `fetch_macrodroid_export` com o path oficial da Solution de Teste.
- [ ] O arquivo é salvo em `Documents/CDXMS_Solutions/packages/downloaded/test_solution` com extensão `.macro`.
- [ ] HTTP diferente de 200, falha de escrita ou JSON inválido produzem falha visível.
- [ ] O export baixado possui `macroExportVersion=1`, nome e tipo esperados.
- [ ] O Manager orienta a importação manual e não declara a solution como instalada antes dela.
- [ ] Após a importação manual, a Solution de Teste abre sua própria interface JUIF.

## Fora do aceite atual

- refresh real de catálogo;
- seleção/detalhes reais de artifact;
- instalação, atualização, reparo ou remoção;
- confirmação automática de importação de `.macro`/`.ablock`.

O download incremental da Solution de Teste está dentro do aceite; os demais itens exigem novos contratos e gates de homologação.
