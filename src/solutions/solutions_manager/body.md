# Corpo — [CDXMS] Solutions Manager v1.0.0

## Tipo e responsabilidade

Macro permanente, orquestradora e idempotente. Na primeira execução inicializa o core local com as capabilities incorporadas; nas seguintes valida o ambiente e abre a interface. Não existe Installer descartável na v1.

## Entradas

Nenhuma entrada pública. A macro possui dois pontos de entrada:

| Gatilho | Configuração | Finalidade |
|---|---|---|
| `EmptyTrigger` | execução manual | inicializar e abrir o Manager |
| `IntentReceivedTrigger` | action `com.cdxms.solutions.EVENT` | receber evento publicado pela interface JUIF |

O Intent recebe os extras `cdxms_namespace`, `cdxms_protocol_version`, `cdxms_session_id`, `cdxms_event_id`, `cdxms_source_artifact_id`, `cdxms_action`, `cdxms_current_page` e `cdxms_event_json`.

## Saída

| Saída | Tipo | Descrição |
|---|---|---|
| `Resultado` | Dicionário | Último resultado lógico no contrato universal CDXMS. |

## Variáveis de trabalho

| Variável | Tipo | Descrição |
|---|---|---|
| `Tmp_SmViewModelJson` | Texto | Modelo de dados usado pelo Builder. |
| `Tmp_SmUiSchemaJson` | Texto | Schema declarativo da interface. |
| `Tmp_SmEventNamespace` | Texto | Namespace recebido pelo Intent. |
| `Tmp_SmEventProtocolVersion` | Texto | Versão do protocolo recebido. |
| `Tmp_SmEventSessionId` | Texto | Sessão do evento. |
| `Tmp_SmEventId` | Texto | Id idempotente do evento. |
| `Tmp_SmEventSourceArtifactId` | Texto | Artifact emissor. |
| `Tmp_SmEventAction` | Texto | Ação solicitada. |
| `Tmp_SmEventCurrentPage` | Texto | Página ativa no momento do evento. |
| `Tmp_SmEventJson` | Texto/JSON | Envelope completo do evento. |
| `Tmp_SmLastConsumedEventId` | Texto | Último evento aceito, usado contra duplicação. |
| `Tmp_SmResultJson` | Texto/JSON | Resultado serializado antes do `JSON Parse`. |

## Corpo completo — passo a passo

### Fluxo A — abertura manual

1. `If Clause` — executa somente quando o gatilho invocador é o `EmptyTrigger` de entrada manual.
2. `Action Block` — chama `[CDXMS] Bootstrap`, aguardando a conclusão, com:
   - `Operation = initialize_ecosystem`;
   - `Requested Artifact Type = solution`;
   - `Requested Artifact Id = solutions_manager`;
   - `Force Repair? = false`;
   - `Load Context? = true`;
   - `Session Id = solutions-manager-session-v1`;
   - `Correlation Id = solutions-manager-launch-v1`;
   - `Resultado -> Resultado`.
3. `If Clause` — continua somente quando `Resultado[success] = true`.
4. `Action Block` — chama `[CDXMS] JUIF UI Builder`, aguardando a conclusão, com:
   - `Config Json = {lv=Tmp_SmViewModelJson}`;
   - `UI Schema Json = {lv=Tmp_SmUiSchemaJson}`;
   - `Escape Json = false`;
   - `Resultado -> Resultado`.
5. `If Clause` — continua somente quando o Builder publicou `Resultado[success] = true`.
6. `Action Block` — chama `[CDXMS] Java UI Framework`, aguardando a conclusão, com `JUIF UI Json = {lv=Resultado[data][juif_ui_json]}`.
7. `Else` — ramo de falha do Builder.
8. `Toast` — exibe `Falha ao construir a interface` com a mensagem do Resultado.
9. `End If` — encerra a validação do Builder.
10. `Else` — ramo de falha do Bootstrap.
11. `Toast` — exibe `Falha ao inicializar` com a mensagem do Resultado.
12. `End If` — encerra a validação do Bootstrap.
13. `End If` — encerra o fluxo de abertura manual.

### Fluxo B — recebimento de evento JUIF

14. `If Clause` — executa somente quando o gatilho invocador é o `IntentReceivedTrigger` do protocolo CDXMS.
15. `JavaScript Code` — interpreta `Tmp_SmEventJson` e valida schema, namespace, protocolo, sessão, origem, allowlist, `event_id` e `consumed = false`.
16. `JSON Parse` — publica o texto validado em `Resultado`.
17. `JavaScript Code` — atualiza `Tmp_SmLastConsumedEventId` somente quando a validação é sucesso.
18. `Log Event` — registra id, ação e resultado para diagnóstico local.
19. `Toast` — fornece feedback visual da recepção do evento.
20. `End If` — encerra o fluxo de evento.

## Runtime incorporado

O export contém 11 Action Blocks em `macro.exportedActionBlocks`: JCM, Bootstrap, Result Manager, Logger, String Utils, Artifact Manager, Dependency Resolver, Remote Source Manager, File Integrity, JUIF UI Builder e Java UI Framework. Isso é obrigatório para uma importação em dispositivo sem componentes CDXMS previamente instalados.

## Limites deste incremento

- O bridge recebe, valida e deduplica eventos, mas ainda não despacha operações de negócio.
- Download de payload executável, lifecycle mutável e confirmação de importação continuam bloqueados.
- Copiar `.macro` ou `.ablock` para o filesystem não equivale a importá-lo no MacroDroid.
- O export exige homologação em dispositivo limpo após qualquer reconstrução.
