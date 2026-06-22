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
- [ ] Bootstrap e JCM incorporados executam sem componentes preexistentes.
- [ ] Segunda execução não recria nem reseta o core.
- [ ] Catálogo local abre sem rede.
- [ ] Falha remota mantém modo degradado quando o cache é válido.
- [ ] UI exibe dashboard, catálogo, instaladas e diagnóstico.

## Event bridge

- [ ] Evento contém `session_id` e `event_id`.
- [ ] Evento de outra sessão é ignorado.
- [ ] Evento duplicado é consumido uma única vez.
- [ ] Seleção de artifact devolve tipo e id.
- [ ] Atualização de catálogo retorna ao fluxo MacroDroid.
- [ ] Falha de evento permanece visível e não fecha silenciosamente a UI.
