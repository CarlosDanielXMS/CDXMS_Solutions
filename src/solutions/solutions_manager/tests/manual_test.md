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
- [ ] Execução sem rede continua abrindo a UI incorporada.

## Event bridge

- [ ] Evento contém `session_id` e `event_id`.
- [ ] Evento de outra sessão é ignorado.
- [ ] Evento duplicado é consumido uma única vez.
- [ ] Namespace, versão de protocolo, origem e allowlist divergentes são bloqueados.
- [ ] `Tmp_SmLastConsumedEventId` só muda após evento aceito.
- [ ] Falha de evento permanece visível e não fecha silenciosamente a UI.

## Fora do aceite atual

- refresh real de catálogo;
- seleção/detalhes reais de artifact;
- download de payload;
- instalação, atualização, reparo ou remoção;
- confirmação automática de importação de `.macro`/`.ablock`.

Esses itens só entram no plano de homologação quando `business_event_dispatch` e `remote_payload_pipeline` forem habilitados no contrato e no export.
